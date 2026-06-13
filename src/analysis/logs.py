"""Load and summarize crew_full run JSON logs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.shared.cost import estimate_cost_usd

LOG_DIR = Path(__file__).resolve().parent.parent.parent / "output" / "logs"
SKIP_TOPICS = {"integration topic"}


def load_run_logs(log_dir: Path | None = None) -> list[dict[str, Any]]:
    root = log_dir or LOG_DIR
    if not root.is_dir():
        return []
    runs: list[dict[str, Any]] = []
    for path in sorted(root.glob("run_*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("topic") in SKIP_TOPICS:
            continue
        if not data.get("tasks"):
            continue
        data["_source"] = path.name
        runs.append(data)
    return runs


def _estimate_usage(tasks: list[dict[str, Any]]) -> dict[str, Any]:
    output_chars = sum(int(t.get("output_chars", 0)) for t in tasks)
    completion = max(output_chars // 4, 0)
    prompt = 0
    cumulative = 0
    for task in tasks:
        prompt += 900 + cumulative // 4
        cumulative += int(task.get("output_chars", 0))
    return {
        "prompt_tokens": prompt,
        "completion_tokens": completion,
        "total_tokens": prompt + completion,
        "estimated": True,
    }


def _usage_for_run(run: dict[str, Any]) -> dict[str, Any]:
    usage = run.get("token_usage")
    if usage and int(usage.get("total_tokens", 0)) > 0:
        return {**usage, "estimated": False}
    return _estimate_usage(run.get("tasks", []))


def summarize_runs(runs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for run in runs:
        tasks = run.get("tasks", [])
        usage = _usage_for_run(run)
        model = run.get("model") or "gpt-4.1-mini"
        prompt = int(usage.get("prompt_tokens", 0))
        completion = int(usage.get("completion_tokens", 0))
        rows.append(
            {
                "timestamp": run.get("timestamp", ""),
                "topic": run.get("topic", ""),
                "success": bool(run.get("success")),
                "model": model,
                "prompt_tokens": prompt,
                "completion_tokens": completion,
                "total_tokens": int(usage.get("total_tokens", prompt + completion)),
                "estimated": bool(usage.get("estimated")),
                "output_chars": sum(int(t.get("output_chars", 0)) for t in tasks),
                "cost_usd": estimate_cost_usd(model, prompt, completion),
                "source": run.get("_source", ""),
            }
        )
    return rows
