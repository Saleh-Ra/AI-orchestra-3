"""Environment and project settings — values from config files and .env only."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent.parent
SETUP_PATH = ROOT / "config" / "setup.json"


def _load_setup() -> dict:
    if not SETUP_PATH.is_file():
        return {}
    return json.loads(SETUP_PATH.read_text(encoding="utf-8"))


def load_env() -> None:
    """Load `.env` from project root."""
    load_dotenv(ROOT / ".env")


def get_openai_model() -> str:
    """Resolve model: env overrides config/setup.json."""
    load_env()
    return (
        os.getenv("OPENAI_MODEL")
        or os.getenv("OPENAI_MODEL_NAME")
        or _load_setup().get("openai_model")
        or "gpt-4.1-mini"
    )


def default_topic() -> str:
    load_env()
    setup = _load_setup()
    return (os.getenv("ARTICLE_TOPIC") or "").strip() or setup.get(
        "default_topic", "CrewAI multi-agent teams for document generation"
    )


def _env_bool(name: str, default: bool = False) -> bool:
    raw = (os.getenv(name) or "").strip().lower()
    if not raw:
        return default
    return raw in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class ProjectSettings:
    topic: str
    cover_author: str
    cover_course: str
    cover_semester: str
    cover_date: str
    use_serper: bool


def get_project_settings() -> ProjectSettings:
    load_env()
    cover_date = (os.getenv("COVER_DATE") or "").strip() or date.today().isoformat()
    return ProjectSettings(
        topic=default_topic(),
        cover_author=(os.getenv("COVER_AUTHOR") or "").strip() or "שם הסטודנט",
        cover_course=(os.getenv("COVER_COURSE") or "").strip()
        or "ייצור המוני של סוכני AI",
        cover_semester=(os.getenv("COVER_SEMESTER") or "").strip() or "סמסטר א׳ 2026",
        cover_date=cover_date,
        use_serper=_env_bool("USE_SERPER", default=False),
    )
