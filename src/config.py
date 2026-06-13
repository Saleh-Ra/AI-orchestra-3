"""Backward-compatible config imports — prefer src.shared.config."""

from src.shared.config import (  # noqa: F401
    ProjectSettings,
    default_topic,
    get_openai_model,
    get_project_settings,
    load_env,
)
from src.shared.gatekeeper import get_llm  # noqa: F401
