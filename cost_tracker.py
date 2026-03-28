"""バッチコスト管理 - 予算追跡・超過制御."""

import json
import logging
import os
from datetime import datetime, timezone

from config import (
    BUDGET_LIMIT_USD,
    INPUT_COST_PER_MTOK,
    OUTPUT_COST_PER_MTOK,
    RESIZE_HEIGHT,
    RESIZE_WIDTH,
)

logger = logging.getLogger(__name__)


def estimate_image_tokens(width: int = RESIZE_WIDTH, height: int = RESIZE_HEIGHT) -> int:
    """画像のトークン数を推定（Claude Vision の概算）."""
    return (width * height) // 750


def estimate_request_cost(
    num_images: int = 1,
    system_tokens: int = 500,
    user_text_tokens: int = 50,
    estimated_output_tokens: int = 800,
) -> float:
    """1回のAPI呼び出しの推定コスト（USD）を返す."""
    image_tokens = estimate_image_tokens() * num_images
    input_tokens = system_tokens + user_text_tokens + image_tokens
    cost = (
        input_tokens * INPUT_COST_PER_MTOK + estimated_output_tokens * OUTPUT_COST_PER_MTOK
    ) / 1_000_000
    # 20% のマージンを加算
    return cost * 1.2


class BatchCostTracker:
    """バッチ全体の予算を追跡する."""

    def __init__(self, budget_limit: float = BUDGET_LIMIT_USD):
        self.budget_limit = budget_limit
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.records: list[dict] = []

    @property
    def total_cost(self) -> float:
        return (
            self.total_input_tokens * INPUT_COST_PER_MTOK
            + self.total_output_tokens * OUTPUT_COST_PER_MTOK
        ) / 1_000_000

    @property
    def remaining_budget(self) -> float:
        return max(0.0, self.budget_limit - self.total_cost)

    def can_afford(self, estimated_cost: float) -> bool:
        return self.remaining_budget >= estimated_cost

    def record_usage(self, filename: str, input_tokens: int, output_tokens: int) -> None:
        cost = (
            input_tokens * INPUT_COST_PER_MTOK + output_tokens * OUTPUT_COST_PER_MTOK
        ) / 1_000_000
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens
        self.records.append(
            {
                "filename": filename,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "cost_usd": round(cost, 6),
            }
        )
        logger.info(
            "Cost: %s - $%.4f (remaining: $%.4f)",
            filename,
            cost,
            self.remaining_budget,
        )

    def get_summary(self) -> dict:
        return {
            "total_input_tokens": self.total_input_tokens,
            "total_output_tokens": self.total_output_tokens,
            "total_cost_usd": round(self.total_cost, 6),
            "budget_limit_usd": self.budget_limit,
            "remaining_usd": round(self.remaining_budget, 6),
            "files_processed": len(self.records),
            "per_file": self.records,
        }

    def save_cost_log(self, output_dir: str) -> None:
        summary = self.get_summary()
        summary["timestamp"] = datetime.now(timezone.utc).isoformat()
        path = os.path.join(output_dir, "cost_log.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(summary, f, ensure_ascii=False, indent=2)
        logger.info(
            "Batch cost: $%.4f / $%.2f (%d files)",
            self.total_cost,
            self.budget_limit,
            len(self.records),
        )
