"""共有設定 - lr_pipeline / scheduler 共通定数."""

import os

# Claude API
MODEL = "claude-sonnet-4-20250514"
INPUT_COST_PER_MTOK = 3.0      # $/MTok
OUTPUT_COST_PER_MTOK = 15.0    # $/MTok
BUDGET_LIMIT_USD = 1.00

# 画像リサイズ（トークン節約用）
RESIZE_WIDTH = 640
RESIZE_HEIGHT = 360

# ディレクトリ
INPUT_DIR = os.environ.get("LR_INPUT_DIR", "input")
OUTPUT_DIR = os.environ.get("LR_OUTPUT_DIR", "output")

# 投稿スコア閾値
SCORE_SINGLE_MIN = 8       # >= 8 → single
SCORE_STORY_MIN = 5        # 5-7  → story (or carousel)
SCORE_SKIP_MAX = 4         # <= 4 → skip

# カルーセル
CAROUSEL_GROUP_SIZE = 4
CAROUSEL_SIMILARITY_THRESHOLD = 0.3  # 最低類似度

# 対応画像拡張子
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}
