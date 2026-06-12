"""Shared environment, LLM, and project settings."""

from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import date

from dotenv import load_dotenv
from crewai import LLM

DEFAULT_TOPIC = "CrewAI multi-agent teams for document generation"


def load_env() -> None:
    load_dotenv()


def get_openai_model() -> str:
    return (
        os.getenv("OPENAI_MODEL")
        or os.getenv("OPENAI_MODEL_NAME")
        or "gpt-4.1-mini"
    )


def get_llm() -> LLM:
    load_env()
    return LLM(model=get_openai_model())


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
        topic=(os.getenv("ARTICLE_TOPIC") or "").strip() or DEFAULT_TOPIC,
        cover_author=(os.getenv("COVER_AUTHOR") or "").strip() or "שם הסטודנט",
        cover_course=(os.getenv("COVER_COURSE") or "").strip()
        or "ייצור המוני של סוכני AI",
        cover_semester=(os.getenv("COVER_SEMESTER") or "").strip() or "סמסטר א׳ 2026",
        cover_date=cover_date,
        use_serper=_env_bool("USE_SERPER", default=False),
    )
