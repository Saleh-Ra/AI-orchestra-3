"""API gatekeeper rate-limit and execute tests."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from src.shared.gatekeeper import ApiGatekeeper


def test_execute_increments_call_count() -> None:
    gk = ApiGatekeeper()
    gk._rpm = 100  # noqa: SLF001
    assert gk.execute("test", lambda: 42) == 42
    assert gk.call_count == 1


def test_rate_limit_blocks_excess_calls() -> None:
    gk = ApiGatekeeper()
    gk._rpm = 2  # noqa: SLF001
    gk.execute("a", lambda: None)
    gk.execute("b", lambda: None)
    with pytest.raises(RuntimeError, match="rate limit"):
        gk.execute("c", lambda: None)


@patch("src.shared.gatekeeper.LLM")
def test_get_llm_routes_through_execute(mock_llm: MagicMock) -> None:
    mock_llm.return_value = MagicMock()
    gk = ApiGatekeeper()
    gk._rpm = 100  # noqa: SLF001
    gk.get_llm()
    mock_llm.assert_called_once()


def test_load_rate_limits_missing_file(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(
        "src.shared.gatekeeper.RATE_LIMITS_PATH",
        tmp_path / "missing.json",
    )
    gk = ApiGatekeeper()
    assert gk._rpm == 30  # noqa: SLF001
