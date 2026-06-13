"""Pipeline path and compile runner tests."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from src.pipeline.compile_runner import assert_template_unchanged, run_project_script
from src.pipeline.paths import FINAL_PDF, LATEX_DIR, ROOT


def test_paths_under_project_root() -> None:
    assert ROOT.name == "AI-orchestra-3" or ROOT.exists()
    assert LATEX_DIR.is_relative_to(ROOT)
    assert FINAL_PDF.parent == ROOT / "output"


def test_assert_template_unchanged() -> None:
    assert_template_unchanged()


@patch("src.pipeline.compile_runner.subprocess.run")
def test_run_project_script_python(mock_run: MagicMock) -> None:
    run_project_script("scripts/run_figures.py")
    mock_run.assert_called_once()
    args = mock_run.call_args
    assert "run_figures.py" in str(args)


@patch("src.pipeline.compile_runner.subprocess.run")
def test_run_project_script_ps1(mock_run: MagicMock) -> None:
    run_project_script("scripts/compile.ps1")
    mock_run.assert_called_once()
    assert mock_run.call_args[0][0][0] == "powershell"
