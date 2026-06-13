"""Phase 3 CLI — delegates to SDK."""

from __future__ import annotations

import argparse
import sys

from src.shared.config import get_project_settings, load_env
from src.sdk import run_full


def main() -> int:
    load_env()
    settings = get_project_settings()
    parser = argparse.ArgumentParser(description="Full six-agent pipeline")
    parser.add_argument("--topic", default=settings.topic, help="Article topic")
    parser.add_argument(
        "--skip-compile",
        action="store_true",
        help="Stop after saving LaTeX artifacts (no PDF)",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Run scripts/validate_outputs.py after compile",
    )
    args = parser.parse_args()
    return run_full(
        args.topic,
        skip_compile=args.skip_compile,
        validate=args.validate,
    )


if __name__ == "__main__":
    sys.exit(main())
