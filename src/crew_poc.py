"""Phase 1 POC CLI — delegates to SDK."""

from __future__ import annotations

import argparse
import sys

from src.sdk import run_poc
from src.shared.config import default_topic, load_env


def main() -> int:
    load_env()
    parser = argparse.ArgumentParser(description="Two-agent CrewAI POC")
    parser.add_argument("--topic", default=default_topic(), help="Article topic")
    args = parser.parse_args()
    return run_poc(args.topic)


if __name__ == "__main__":
    sys.exit(main())
