"""Shared environment and LLM configuration."""

from __future__ import annotations

import os

from dotenv import load_dotenv
from crewai import LLM


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
