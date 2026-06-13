"""Configuration loading tests — secrets from env only."""

from __future__ import annotations

import json
from pathlib import Path

from src.shared.config import (
    default_topic,
    get_openai_model,
    get_project_settings,
    load_env,
)


def test_default_topic_from_env(env_override: None, monkeypatch) -> None:
    monkeypatch.setenv("ARTICLE_TOPIC", "custom topic")
    assert default_topic() == "custom topic"


def test_openai_model_env_override(env_override: None, monkeypatch) -> None:
    monkeypatch.setenv("OPENAI_MODEL", "gpt-test")
    assert get_openai_model() == "gpt-test"


def test_project_settings_cover_fields(env_override: None) -> None:
    load_env()
    s = get_project_settings()
    assert s.cover_author == "Test Author"
    assert s.topic == "test topic"
    assert s.use_serper is False


def test_setup_json_exists(project_root: Path) -> None:
    path = project_root / "config" / "setup.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["version"] == "1.00"
    assert "default_topic" in data
