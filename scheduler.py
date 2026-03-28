"""投稿スケジューラ - post_plan.json / photo_meta.json を読んで投稿を実行.

Claude API 呼び出しは一切行わない。
lr_pipeline.py が生成した JSON ファイルのみを参照する。
"""

import json
import logging
import os
import sys
from pathlib import Path

from config import OUTPUT_DIR

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# データ読み込み
# ---------------------------------------------------------------------------

def load_post_plan(output_dir: str = OUTPUT_DIR) -> dict:
    """post_plan.json を読み込む."""
    path = os.path.join(output_dir, "post_plan.json")
    if not os.path.exists(path):
        raise FileNotFoundError(f"post_plan.json not found: {path}")
    with open(path, encoding="utf-8") as f:
        plan = json.load(f)
    if "plans" not in plan:
        raise ValueError("post_plan.json is missing 'plans' key")
    logger.info("Loaded post plan: %d entries", len(plan["plans"]))
    return plan


def load_photo_meta(output_dir: str = OUTPUT_DIR) -> dict[str, dict]:
    """photo_meta.json を読み込み、ファイル名→メタデータの辞書を返す."""
    path = os.path.join(output_dir, "photo_meta.json")
    if not os.path.exists(path):
        raise FileNotFoundError(f"photo_meta.json not found: {path}")
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    meta_by_file: dict[str, dict] = {}
    for photo in data.get("photos", []):
        fn = photo.get("filename")
        if fn:
            meta_by_file[fn] = photo
    logger.info("Loaded photo meta: %d photos", len(meta_by_file))
    return meta_by_file


# ---------------------------------------------------------------------------
# 投稿タスク構築
# ---------------------------------------------------------------------------

def schedule_posts(plan: dict, meta: dict[str, dict]) -> list[dict]:
    """post_plan から投稿タスクリストを構築する（skip を除外）."""
    tasks: list[dict] = []

    for entry in plan.get("plans", []):
        post_type = entry.get("type", "skip")
        if post_type == "skip":
            logger.debug("Skipping: %s", entry.get("photos"))
            continue

        photos = entry.get("photos", [])
        if not photos:
            continue

        if post_type == "carousel":
            # カルーセルはプランにキャプション・ハッシュタグが含まれている
            task = {
                "type": "carousel",
                "photos": photos,
                "caption_ja": entry.get("caption_ja", ""),
                "caption_en": entry.get("caption_en", ""),
                "hashtags": entry.get("hashtags", []),
                "score": entry.get("score", 0),
            }
        elif post_type in ("single", "story"):
            # single / story は photo_meta から取得
            primary_file = photos[0]
            photo_meta = meta.get(primary_file, {})
            task = {
                "type": post_type,
                "photos": photos,
                "caption_ja": photo_meta.get("caption_ja", entry.get("caption_ja", "")),
                "caption_en": photo_meta.get("caption_en", entry.get("caption_en", "")),
                "hashtags": photo_meta.get("hashtags", entry.get("hashtags", [])),
                "score": entry.get("score", photo_meta.get("post_score", 0)),
            }
        else:
            logger.warning("Unknown post type: %s", post_type)
            continue

        tasks.append(task)

    # スコア降順
    tasks.sort(key=lambda t: -t.get("score", 0))
    logger.info("Scheduled %d posts", len(tasks))
    return tasks


# ---------------------------------------------------------------------------
# 投稿実行（アダプタ）
# ---------------------------------------------------------------------------

def build_caption(task: dict, lang: str = "ja") -> str:
    """投稿用キャプションを組み立てる."""
    caption = task.get(f"caption_{lang}", "") or task.get("caption_ja", "")
    hashtags = task.get("hashtags", [])
    if hashtags:
        caption += "\n\n" + " ".join(hashtags)
    return caption


def execute_post(task: dict, input_dir: str = "input") -> bool:
    """投稿を実行する（現在はログ出力のみ、実API連携はここに実装）.

    実際の Instagram API 連携（instagrapi 等）はこの関数内に実装する。
    """
    post_type = task["type"]
    photos = task["photos"]
    caption = build_caption(task, lang="ja")

    # 画像ファイルの存在確認
    missing = [f for f in photos if not Path(input_dir, f).exists()]
    if missing:
        logger.error("Missing image files: %s", missing)
        return False

    if post_type == "single":
        logger.info("[POST:single] %s (score=%d)", photos[0], task.get("score", 0))
        logger.info("  Caption: %s", caption[:80] + "..." if len(caption) > 80 else caption)
        # TODO: Instagram API single post
        return True

    elif post_type == "carousel":
        logger.info(
            "[POST:carousel] %d photos: %s (score=%d)",
            len(photos),
            photos,
            task.get("score", 0),
        )
        logger.info("  Caption: %s", caption[:80] + "..." if len(caption) > 80 else caption)
        # TODO: Instagram API carousel post (全画像を1投稿にまとめる)
        return True

    elif post_type == "story":
        logger.info("[POST:story] %s (score=%d)", photos[0], task.get("score", 0))
        # TODO: Instagram API story post
        return True

    else:
        logger.warning("Unsupported post type: %s", post_type)
        return False


# ---------------------------------------------------------------------------
# メイン
# ---------------------------------------------------------------------------

def run(output_dir: str = OUTPUT_DIR, input_dir: str = "input") -> None:
    """メインエントリポイント: プラン読み込み → 投稿実行."""
    plan = load_post_plan(output_dir)
    meta = load_photo_meta(output_dir)
    tasks = schedule_posts(plan, meta)

    success = 0
    fail = 0
    for task in tasks:
        try:
            if execute_post(task, input_dir):
                success += 1
            else:
                fail += 1
        except Exception:
            logger.exception("Failed to execute post: %s", task.get("photos"))
            fail += 1

    logger.info("Done: %d success, %d failed", success, fail)


if __name__ == "__main__":
    out_dir = sys.argv[1] if len(sys.argv) > 1 else OUTPUT_DIR
    in_dir = sys.argv[2] if len(sys.argv) > 2 else "input"
    run(out_dir, in_dir)
