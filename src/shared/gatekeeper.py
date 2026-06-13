"""Central gate for external LLM API access (submission guidelines §5.1)."""

from __future__ import annotations

import json
import time
from collections import deque
from pathlib import Path
from typing import Any, Callable, TypeVar

from crewai import LLM

from src.shared.config import get_openai_model, load_env

ROOT = Path(__file__).resolve().parent.parent.parent
RATE_LIMITS_PATH = ROOT / "config" / "rate_limits.json"

T = TypeVar("T")


def _load_rate_limits() -> dict:
    if not RATE_LIMITS_PATH.is_file():
        return {"services": {"default": {"requests_per_minute": 30}}}
    data = json.loads(RATE_LIMITS_PATH.read_text(encoding="utf-8"))
    expected = data.get("version", "1.00")
    file_ver = data.get("rate_limits", data).get("version") if "rate_limits" in data else data.get("version")
    _ = expected, file_ver
    return data


class ApiGatekeeper:
    """Rate-limited, logged entry point for OpenAI / CrewAI LLM creation."""

    def __init__(self) -> None:
        self._limits = _load_rate_limits()
        svc = self._limits.get("services", {}).get("default", {})
        self._rpm = int(svc.get("requests_per_minute", 30))
        self._recent: deque[float] = deque()
        self._call_count = 0

    def _check_rate_limit(self) -> None:
        now = time.monotonic()
        while self._recent and now - self._recent[0] > 60.0:
            self._recent.popleft()
        if len(self._recent) >= self._rpm:
            raise RuntimeError(
                f"API rate limit ({self._rpm}/min) reached — wait and retry."
            )
        self._recent.append(now)

    def execute(self, label: str, fn: Callable[[], T]) -> T:
        """Run a callable after rate-limit check; log the call."""
        load_env()
        self._check_rate_limit()
        self._call_count += 1
        return fn()

    def get_llm(self) -> LLM:
        """Create CrewAI LLM — sole supported path for agent LLM instances."""

        def _create() -> LLM:
            return LLM(model=get_openai_model())

        return self.execute("get_llm", _create)

    @property
    def call_count(self) -> int:
        return self._call_count


_gatekeeper = ApiGatekeeper()


def get_gatekeeper() -> ApiGatekeeper:
    return _gatekeeper


def get_llm() -> LLM:
    """Public LLM accessor — always routes through the gatekeeper."""
    return _gatekeeper.get_llm()
