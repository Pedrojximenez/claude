#!/usr/bin/env python3
"""日次レポート生成スクリプト

ソース（優先度順）:
1. Gmail subject:[gods] の直近24時間分（最も信頼できるソース）
2. session_log.md（補足情報）
"""

import base64
import datetime
import json
import os
import re
import sys
from email.utils import parsedate_to_datetime
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
TOKEN_PATH = Path(__file__).parent / "token.json"
CREDENTIALS_PATH = Path(__file__).parent / "credentials.json"
SESSION_LOG_PATH = Path(__file__).parent / "session_log.md"
OUTPUT_PATH = Path(__file__).parent / "daily_report.md"


def get_gmail_service():
    """Gmail API サービスを認証・取得する。"""
    creds = None
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_PATH), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CREDENTIALS_PATH.exists():
                print(
                    f"エラー: {CREDENTIALS_PATH} が見つかりません。"
                    "Google Cloud Console から OAuth クライアント ID の JSON をダウンロードして配置してください。",
                    file=sys.stderr,
                )
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_PATH), SCOPES
            )
            creds = flow.run_local_server(port=0)
        TOKEN_PATH.write_text(creds.to_json())
    return build("gmail", "v1", credentials=creds)


def fetch_gmail_gods_messages(service):
    """Gmail から subject:[gods] の直近24時間分のメールを取得する。"""
    now = datetime.datetime.now(datetime.timezone.utc)
    since = now - datetime.timedelta(hours=24)
    after_epoch = int(since.timestamp())

    query = f"subject:[gods] after:{after_epoch}"
    results = (
        service.users()
        .messages()
        .list(userId="me", q=query, maxResults=100)
        .execute()
    )

    messages = results.get("messages", [])
    if not messages:
        return []

    entries = []
    for msg_meta in messages:
        msg = (
            service.users()
            .messages()
            .get(userId="me", id=msg_meta["id"], format="full")
            .execute()
        )
        headers = {h["name"]: h["value"] for h in msg["payload"]["headers"]}
        subject = headers.get("Subject", "(no subject)")
        sender = headers.get("From", "")
        date_str = headers.get("Date", "")
        try:
            date = parsedate_to_datetime(date_str)
        except Exception:
            date = None

        body = _extract_body(msg["payload"])

        entries.append(
            {
                "subject": subject,
                "from": sender,
                "date": date,
                "body": body,
            }
        )

    entries.sort(key=lambda e: e["date"] or datetime.datetime.min.replace(tzinfo=datetime.timezone.utc))
    return entries


def _extract_body(payload):
    """メール本文をプレーンテキストで抽出する。"""
    if payload.get("body", {}).get("data"):
        return base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8", errors="replace")

    parts = payload.get("parts", [])
    for part in parts:
        if part.get("mimeType") == "text/plain" and part.get("body", {}).get("data"):
            return base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8", errors="replace")

    for part in parts:
        result = _extract_body(part)
        if result:
            return result

    return ""


def read_session_log():
    """session_log.md を読み込む。なければ空文字列を返す。"""
    if SESSION_LOG_PATH.exists():
        return SESSION_LOG_PATH.read_text(encoding="utf-8")
    return ""


def generate_report(gmail_entries, session_log):
    """Gmail エントリと session_log からレポートを生成する。"""
    today = datetime.date.today().isoformat()
    lines = [
        f"# Daily Report — {today}",
        "",
    ]

    # Gmail セクション（最優先ソース）
    lines.append("## Gmail [gods] （直近24時間）")
    lines.append("")
    if gmail_entries:
        for entry in gmail_entries:
            ts = entry["date"].strftime("%Y-%m-%d %H:%M") if entry["date"] else "不明"
            lines.append(f"### {entry['subject']}")
            lines.append(f"- **From:** {entry['from']}")
            lines.append(f"- **Date:** {ts}")
            lines.append("")
            body = entry["body"].strip()
            if body:
                lines.append(body)
            lines.append("")
    else:
        lines.append("該当メールなし。")
        lines.append("")

    # Session Log セクション（補足）
    lines.append("## Session Log（補足情報）")
    lines.append("")
    if session_log.strip():
        lines.append(session_log.strip())
    else:
        lines.append("session_log.md が見つからないか、空です。")
    lines.append("")

    return "\n".join(lines)


def main():
    print("Gmail [gods] メールを取得中...")
    service = get_gmail_service()
    gmail_entries = fetch_gmail_gods_messages(service)
    print(f"  → {len(gmail_entries)} 件取得")

    print("session_log.md を読み込み中...")
    session_log = read_session_log()

    report = generate_report(gmail_entries, session_log)
    OUTPUT_PATH.write_text(report, encoding="utf-8")
    print(f"レポートを {OUTPUT_PATH} に出力しました。")


if __name__ == "__main__":
    main()
