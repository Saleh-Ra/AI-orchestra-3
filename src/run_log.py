"""Structured per-agent run logs for crew_full."""

from __future__ import annotations

import json
import traceback
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

AGENT_LABELS = (
    "Researcher",
    "Planner",
    "Writer",
    "Editor",
    "Visualizer",
    "LaTeX",
)

LOG_DIR = Path(__file__).resolve().parent.parent / "output" / "logs"


def _utc_stamp() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _usage_payload(result: Any | None) -> dict[str, Any] | None:
    usage = getattr(result, "token_usage", None) if result else None
    if usage is None:
        return None
    if hasattr(usage, "model_dump"):
        data = usage.model_dump()
        if not isinstance(data, dict):
            return None
    elif isinstance(usage, dict):
        data = usage
    else:
        data = {
            "total_tokens": getattr(usage, "total_tokens", 0),
            "prompt_tokens": getattr(usage, "prompt_tokens", 0),
            "completion_tokens": getattr(usage, "completion_tokens", 0),
            "successful_requests": getattr(usage, "successful_requests", 0),
        }
    try:
        total_i = int(data.get("total_tokens", 0))
    except (TypeError, ValueError):
        return None
    if total_i <= 0:
        return None
    return data


def _task_entries(result: Any | None) -> list[dict[str, Any]]:
    if result is None:
        return []
    entries: list[dict[str, Any]] = []
    outputs = getattr(result, "tasks_output", None) or []
    for i, out in enumerate(outputs):
        raw = getattr(out, "raw", None) or ""
        agent = getattr(getattr(out, "agent", None), "role", None)
        if not agent and i < len(AGENT_LABELS):
            agent = AGENT_LABELS[i]
        elif not agent:
            agent = f"task_{i}"
        entries.append(
            {
                "task_index": i,
                "agent": agent,
                "output_chars": len(raw),
                "status": "ok" if raw.strip() else "empty",
            }
        )
    return entries


def write_run_log(
    *,
    topic: str,
    success: bool,
    result: Any | None = None,
    artifacts: dict[str, str] | None = None,
    error: str | None = None,
    phase: str = "crew_full",
    failed_task_index: int | None = None,
    model: str | None = None,
) -> Path:
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    tasks = _task_entries(result)
    if failed_task_index is not None and 0 <= failed_task_index < len(tasks):
        tasks[failed_task_index]["status"] = "failed"
    payload: dict[str, Any] = {
        "timestamp": _utc_stamp(),
        "phase": phase,
        "topic": topic,
        "success": success,
        "model": model,
        "tasks": tasks,
        "artifacts": artifacts or {},
        "error": error,
    }
    usage = _usage_payload(result)
    if usage:
        payload["token_usage"] = usage
    ts = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    path = LOG_DIR / f"run_{ts}.json"
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    path.write_text(text, encoding="utf-8")
    (LOG_DIR / "latest.json").write_text(text, encoding="utf-8")
    return path


def log_failure(
    topic: str,
    exc: BaseException,
    result: Any | None = None,
    model: str | None = None,
) -> Path:
    tasks = _task_entries(result)
    failed_idx = len(tasks) - 1 if tasks else None
    return write_run_log(
        topic=topic,
        success=False,
        result=result,
        error=f"{type(exc).__name__}: {exc}\n{traceback.format_exc()}",
        failed_task_index=failed_idx,
        model=model,
    )
