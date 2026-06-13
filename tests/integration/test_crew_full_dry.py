"""Integration-style tests with mocked external processes."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from crewai import LLM

from src import __version__
from src.config import get_openai_model, load_env
from src.pipeline.crew_build import build_full_crew
from src.shared.version import __version__ as shared_version


def test_package_version_exported() -> None:
    assert __version__ == "1.00"
    assert shared_version == "1.00"


def test_config_shim_reexports() -> None:
    load_env()
    assert isinstance(get_openai_model(), str)


@patch("src.pipeline.crew_build.get_llm")
def test_build_full_crew_six_tasks(mock_get_llm: MagicMock) -> None:
    mock_get_llm.return_value = LLM(model="gpt-4.1-mini")
    crew = build_full_crew()
    assert len(crew.agents) == 6
    assert len(crew.tasks) == 6


@patch("src.sdk.sdk.subprocess.run")
@patch("src.sdk.sdk.run_project_script")
@patch("src.sdk.sdk.save_full_crew_artifacts")
@patch("src.sdk.sdk.build_full_crew")
def test_run_full_validate_path(
    mock_build: MagicMock,
    mock_save: MagicMock,
    mock_script: MagicMock,
    mock_subproc: MagicMock,
) -> None:
    from src.sdk.sdk import run_full

    mock_result = MagicMock()
    mock_build.return_value.kickoff.return_value = mock_result
    mock_subproc.return_value.returncode = 0

    code = run_full("integration topic", validate=True)
    assert code == 0
    mock_save.assert_called_once()
    mock_script.assert_called()
