"""Lightroom 写真解析パイプライン.

1回の Claude API 呼び出しで全メタデータを取得し、
バッチ完了後に投稿プランを自動生成する。
"""

import base64
import json
import logging
import os
import re
import sys
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path

import anthropic
from PIL import Image, ImageOps

from config import (
    CAROUSEL_GROUP_SIZE,
    CAROUSEL_SIMILARITY_THRESHOLD,
    IMAGE_EXTENSIONS,
    INPUT_DIR,
    MODEL,
    OUTPUT_DIR,
    SCORE_SINGLE_MIN,
    SCORE_SKIP_MAX,
    SCORE_STORY_MIN,
)
from cost_tracker import BatchCostTracker, estimate_request_cost

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# 画像リサイズ
# ---------------------------------------------------------------------------

def resize_for_analysis(image_path: str, width: int = 640, height: int = 360) -> bytes:
    """画像を 640x360 にリサイズし、JPEG bytes を返す（元ファイルは変更しない）."""
    with Image.open(image_path) as img:
        img = ImageOps.exif_transpose(img) or img
        img = ImageOps.pad(img, (width, height), color=(0, 0, 0))
        buf = BytesIO()
        img.convert("RGB").save(buf, format="JPEG", quality=80)
        return buf.getvalue()


# ---------------------------------------------------------------------------
# プロンプト
# ---------------------------------------------------------------------------

ANALYSIS_SYSTEM_PROMPT = """\
あなたは写真解析のエキスパートです。
与えられた写真を分析し、以下の JSON を **そのまま** 返してください。
JSON 以外のテキストは一切出力しないでください。

{
  "preset": {
    "name": "Lightroom プリセット名（例: Fuji Classic Chrome）",
    "adjustments": {
      "exposure": 0.0,
      "contrast": 0,
      "highlights": 0,
      "shadows": 0,
      "whites": 0,
      "blacks": 0,
      "clarity": 0,
      "vibrance": 0,
      "saturation": 0,
      "white_balance_temp": 0,
      "white_balance_tint": 0
    }
  },
  "caption_ja": "日本語キャプション（詩的・3〜4行、改行は \\n で）",
  "caption_en": "English caption (2-3 lines, \\n separated)",
  "hashtags": ["#tag1", "#tag2", "... 合計30個、日英混合"],
  "post_score": 8,
  "recommended_format": "single | carousel | story | reels",
  "color_palette": ["#HEXCOL", "#HEXCOL", "#HEXCOL"],
  "theme_tags": ["keyword1", "keyword2", "keyword3"]
}

### ルール
- preset.adjustments の値は Lightroom のスライダー範囲に準拠
- caption_ja は詩的で感情に訴える表現（3〜4行）
- caption_en は簡潔で魅力的（2〜3行）
- hashtags は **必ず30個**（日本語タグと英語タグを混合、各 # 付き）
- post_score は 1（低品質）〜 10（傑作）で評価
- recommended_format: 写真の構図・内容に基づき single/carousel/story/reels から選択
- color_palette: 写真の支配的な3色を HEX で抽出
- theme_tags: 写真のテーマを表す英語キーワード 3〜5個
"""


# ---------------------------------------------------------------------------
# API 呼び出し（1写真 = 1コール）
# ---------------------------------------------------------------------------

def ai_analyze_photo(
    image_path: str,
    client: anthropic.Anthropic,
) -> tuple[dict, int, int]:
    """1回の API 呼び出しで全メタデータを取得する.

    Returns:
        (metadata_dict, input_tokens, output_tokens)
    """
    image_bytes = resize_for_analysis(image_path)
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")

    response = client.messages.create(
        model=MODEL,
        max_tokens=2000,
        system=ANALYSIS_SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image_b64,
                        },
                    },
                    {
                        "type": "text",
                        "text": "この写真を分析してください。",
                    },
                ],
            }
        ],
    )

    raw_text = response.content[0].text
    input_tokens = response.usage.input_tokens
    output_tokens = response.usage.output_tokens

    # JSON パース（マークダウンコードフェンス対応）
    cleaned = re.sub(r"^```(?:json)?\s*", "", raw_text.strip())
    cleaned = re.sub(r"\s*```$", "", cleaned)

    try:
        metadata = json.loads(cleaned)
    except json.JSONDecodeError as e:
        logger.error("JSON parse error for %s: %s\nRaw: %s", image_path, e, raw_text[:500])
        raise

    return metadata, input_tokens, output_tokens


# ---------------------------------------------------------------------------
# カルーセルグルーピング
# ---------------------------------------------------------------------------

def _hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    h = hex_color.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


def _color_distance(palette_a: list[str], palette_b: list[str]) -> float:
    """2つのカラーパレット間の平均 RGB 距離（0〜1 に正規化）."""
    if not palette_a or not palette_b:
        return 1.0
    total = 0.0
    count = 0
    for ca in palette_a:
        for cb in palette_b:
            ra, ga, ba = _hex_to_rgb(ca)
            rb, gb, bb = _hex_to_rgb(cb)
            dist = ((ra - rb) ** 2 + (ga - gb) ** 2 + (ba - bb) ** 2) ** 0.5
            total += dist
            count += 1
    max_dist = (255**2 * 3) ** 0.5  # ≈ 441.67
    return (total / count) / max_dist if count else 1.0


def _theme_similarity(tags_a: list[str], tags_b: list[str]) -> float:
    """Jaccard 類似度."""
    sa, sb = set(tags_a), set(tags_b)
    if not sa and not sb:
        return 0.0
    intersection = sa & sb
    union = sa | sb
    return len(intersection) / len(union) if union else 0.0


def _photo_similarity(a: dict, b: dict) -> float:
    """色味 + テーマの総合類似度（0〜1、高いほど類似）."""
    color_sim = 1.0 - _color_distance(
        a.get("color_palette", []), b.get("color_palette", [])
    )
    theme_sim = _theme_similarity(
        a.get("theme_tags", []), b.get("theme_tags", [])
    )
    return color_sim * 0.5 + theme_sim * 0.5


def find_carousel_groups(photos: list[dict]) -> list[list[dict]]:
    """色味・テーマが近い写真を4枚ずつグループ化."""
    candidates = [
        p for p in photos
        if SCORE_STORY_MIN <= p.get("post_score", 0) <= (SCORE_SINGLE_MIN - 1)
    ]
    if len(candidates) < CAROUSEL_GROUP_SIZE:
        return []

    used = set()
    groups = []

    for i, base in enumerate(candidates):
        if i in used:
            continue
        similarities = []
        for j, other in enumerate(candidates):
            if j <= i or j in used:
                continue
            sim = _photo_similarity(base, other)
            if sim >= CAROUSEL_SIMILARITY_THRESHOLD:
                similarities.append((j, sim))
        similarities.sort(key=lambda x: x[1], reverse=True)

        if len(similarities) >= CAROUSEL_GROUP_SIZE - 1:
            group_indices = [i] + [s[0] for s in similarities[: CAROUSEL_GROUP_SIZE - 1]]
            groups.append([candidates[idx] for idx in group_indices])
            used.update(group_indices)

    return groups


# ---------------------------------------------------------------------------
# 投稿プラン生成
# ---------------------------------------------------------------------------

def generate_post_plan(photos: list[dict]) -> dict:
    """全写真のメタデータから post_plan.json を生成."""
    plans: list[dict] = []
    carousel_filenames: set[str] = set()

    # reels 推奨は除外（動画向け）
    photos_filtered = [
        p for p in photos if p.get("recommended_format") != "reels"
    ]

    # カルーセルグループを先に検出
    carousel_groups = find_carousel_groups(photos_filtered)
    for group in carousel_groups:
        filenames = [p["filename"] for p in group]
        carousel_filenames.update(filenames)
        # 最高スコアの写真からキャプションを採用
        best = max(group, key=lambda p: p.get("post_score", 0))
        # ハッシュタグを統合（重複排除、30個上限）
        all_tags: list[str] = []
        seen_tags: set[str] = set()
        for p in group:
            for tag in p.get("hashtags", []):
                if tag not in seen_tags:
                    seen_tags.add(tag)
                    all_tags.append(tag)
        plans.append(
            {
                "type": "carousel",
                "photos": filenames,
                "group_reason": "Similar color palette and theme",
                "caption_ja": best.get("caption_ja", ""),
                "caption_en": best.get("caption_en", ""),
                "hashtags": all_tags[:30],
                "score": best.get("post_score", 0),
            }
        )

    # 残りの写真をスコアで振り分け
    for p in photos_filtered:
        fn = p["filename"]
        if fn in carousel_filenames:
            continue
        score = p.get("post_score", 0)
        if score >= SCORE_SINGLE_MIN:
            plans.append(
                {
                    "type": "single",
                    "photos": [fn],
                    "caption_ja": p.get("caption_ja", ""),
                    "caption_en": p.get("caption_en", ""),
                    "hashtags": p.get("hashtags", []),
                    "score": score,
                }
            )
        elif score >= SCORE_STORY_MIN:
            plans.append(
                {
                    "type": "story",
                    "photos": [fn],
                    "score": score,
                }
            )
        else:
            plans.append(
                {
                    "type": "skip",
                    "photos": [fn],
                    "score": score,
                }
            )

    # スコア降順ソート（skip は末尾）
    type_priority = {"single": 0, "carousel": 1, "story": 2, "skip": 3}
    plans.sort(key=lambda p: (type_priority.get(p["type"], 9), -p.get("score", 0)))

    return {
        "batch_id": datetime.now(timezone.utc).isoformat(),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "plans": plans,
    }


# ---------------------------------------------------------------------------
# バッチ処理メイン
# ---------------------------------------------------------------------------

def process_batch(input_dir: str = INPUT_DIR, output_dir: str = OUTPUT_DIR) -> None:
    """input/ 内の写真を一括解析し、メタ・プラン・コストを output/ に保存."""
    os.makedirs(output_dir, exist_ok=True)

    # 処理対象ファイル一覧
    files = sorted(
        p
        for p in Path(input_dir).iterdir()
        if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
    )

    # pending_queue があれば先頭に追加
    pending_path = os.path.join(output_dir, "pending_queue.json")
    if os.path.exists(pending_path):
        with open(pending_path, encoding="utf-8") as f:
            pending = json.load(f)
        pending_files = [
            Path(input_dir) / fn
            for fn in pending.get("pending_files", [])
            if (Path(input_dir) / fn).exists()
        ]
        logger.info("Pending queue loaded: %d files", len(pending_files))
        existing_names = {p.name for p in files}
        for pf in pending_files:
            if pf.name not in existing_names:
                files.insert(0, pf)
        os.remove(pending_path)

    if not files:
        logger.info("No images found in %s", input_dir)
        return

    logger.info("Processing %d images", len(files))

    client = anthropic.Anthropic()
    tracker = BatchCostTracker()
    photos: list[dict] = []
    pending_files_overflow: list[str] = []

    for i, filepath in enumerate(files):
        est_cost = estimate_request_cost(num_images=1)
        if not tracker.can_afford(est_cost):
            pending_files_overflow = [f.name for f in files[i:]]
            logger.warning(
                "Budget limit reached. %d files deferred to pending queue.",
                len(pending_files_overflow),
            )
            break

        logger.info("[%d/%d] Analyzing: %s", i + 1, len(files), filepath.name)
        try:
            metadata, in_tok, out_tok = ai_analyze_photo(str(filepath), client)
            metadata["filename"] = filepath.name
            tracker.record_usage(filepath.name, in_tok, out_tok)
            photos.append(metadata)
        except Exception:
            logger.exception("Failed to analyze %s - skipping", filepath.name)

    # photo_meta.json
    meta_output = {
        "batch_id": datetime.now(timezone.utc).isoformat(),
        "photos": photos,
    }
    meta_path = os.path.join(output_dir, "photo_meta.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta_output, f, ensure_ascii=False, indent=2)
    logger.info("Saved %s (%d photos)", meta_path, len(photos))

    # post_plan.json
    if photos:
        plan = generate_post_plan(photos)
        plan_path = os.path.join(output_dir, "post_plan.json")
        with open(plan_path, "w", encoding="utf-8") as f:
            json.dump(plan, f, ensure_ascii=False, indent=2)
        logger.info("Saved %s", plan_path)

    # pending_queue.json
    if pending_files_overflow:
        pq = {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "reason": "budget_exceeded",
            "budget_used_usd": round(tracker.total_cost, 6),
            "budget_limit_usd": tracker.budget_limit,
            "pending_files": pending_files_overflow,
        }
        with open(pending_path, "w", encoding="utf-8") as f:
            json.dump(pq, f, ensure_ascii=False, indent=2)
        logger.info("Saved pending queue: %d files", len(pending_files_overflow))

    # コストログ
    tracker.save_cost_log(output_dir)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    in_dir = sys.argv[1] if len(sys.argv) > 1 else INPUT_DIR
    out_dir = sys.argv[2] if len(sys.argv) > 2 else OUTPUT_DIR
    process_batch(in_dir, out_dir)
