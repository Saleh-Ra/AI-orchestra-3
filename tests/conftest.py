"""Shared pytest fixtures."""

from __future__ import annotations

from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture
def project_root() -> Path:
    return ROOT


@pytest.fixture
def sample_body_tex() -> str:
    return (
        r"\section{Test}"
        "\n"
        r"\node[state] (0) {0};"
        "\n"
        r"\begin{tabular}{|l|l|}"
        "\nA & B & C \\\\\n"
        r"\end{tabular}"
    )


@pytest.fixture
def env_override(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENAI_MODEL", "gpt-4.1-mini")
    monkeypatch.setenv("ARTICLE_TOPIC", "test topic")
    monkeypatch.setenv("COVER_AUTHOR", "Test Author")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
