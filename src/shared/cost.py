"""Token cost estimation from config/cost_rates.json."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
RATES_PATH = ROOT / "config" / "cost_rates.json"


def load_cost_rates() -> dict:
    if not RATES_PATH.is_file():
        return {"models": {"gpt-4.1-mini": {"input_per_million": 0.4, "output_per_million": 1.6}}}
    return json.loads(RATES_PATH.read_text(encoding="utf-8"))


def estimate_cost_usd(
    model: str,
    prompt_tokens: int,
    completion_tokens: int,
) -> float:
    """Return estimated USD cost for a run."""
    rates = load_cost_rates().get("models", {})
    model_rates = rates.get(model) or rates.get("gpt-4.1-mini", {})
    input_rate = float(model_rates.get("input_per_million", 0.4))
    output_rate = float(model_rates.get("output_per_million", 1.6))
    return (prompt_tokens * input_rate + completion_tokens * output_rate) / 1_000_000
