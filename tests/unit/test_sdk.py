"""SDK helpers without live LLM calls."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

from crewai import LLM

from src.sdk.sdk import build_poc_crew, recompile_latex


@patch("src.sdk.sdk.run_project_script")
@patch("src.sdk.sdk.finalize_latex_outputs")
def test_recompile_latex(mock_finalize: MagicMock, mock_run: MagicMock, tmp_path: Path) -> None:
    recompile_latex(tmp_path)
    mock_finalize.assert_called_once_with(tmp_path)
    assert mock_run.call_count == 2


@patch("src.sdk.sdk.get_llm")
def test_build_poc_crew_wiring(mock_get_llm: MagicMock) -> None:
    mock_get_llm.return_value = LLM(model="gpt-4.1-mini")
    crew = build_poc_crew()
    assert len(crew.agents) == 2
    assert len(crew.tasks) == 2
