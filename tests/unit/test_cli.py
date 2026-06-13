"""CLI entry point tests."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from src.crew_full import main as crew_full_main
from src.crew_poc import main as crew_poc_main


@patch("src.crew_full.run_full", return_value=0)
def test_crew_full_main_default(mock_run: MagicMock) -> None:
    with patch("sys.argv", ["crew_full"]):
        assert crew_full_main() == 0
    mock_run.assert_called_once()


@patch("src.crew_full.run_full", return_value=0)
def test_crew_full_main_validate(mock_run: MagicMock) -> None:
    with patch("sys.argv", ["crew_full", "--validate", "--topic", "T"]):
        assert crew_full_main() == 0
    mock_run.assert_called_once_with("T", skip_compile=False, validate=True)


@patch("src.crew_poc.run_poc", return_value=0)
def test_crew_poc_main(mock_run: MagicMock) -> None:
    with patch("sys.argv", ["crew_poc", "--topic", "POC"]):
        assert crew_poc_main() == 0
    mock_run.assert_called_once_with("POC")
