"""Phase 0 gate: CrewAI imports and OpenAI connectivity."""

from __future__ import annotations

import os
import sys

from dotenv import load_dotenv


def main() -> int:
    load_dotenv()

    api_key = (os.getenv("OPENAI_API_KEY") or "").strip().strip('"').strip("'")
    if not api_key or api_key.startswith("sk-your-key"):
        print(
            "ERROR: Set OPENAI_API_KEY in .env (copy from .env.example).",
            file=sys.stderr,
        )
        return 1

    try:
        from crewai import Agent, Crew, LLM, Process, Task  # noqa: F401
    except ImportError as exc:
        print(f"ERROR: CrewAI import failed: {exc}", file=sys.stderr)
        return 1

    model = (
        os.getenv("OPENAI_MODEL")
        or os.getenv("OPENAI_MODEL_NAME")
        or "gpt-4.1-mini"
    )
    llm = LLM(model=model)

    print(f"Calling OpenAI ({model})...")
    reply = llm.call("Reply with exactly one word: ok")
    snippet = (reply or "").strip()[:80]
    print(f"Response: {snippet!r}")
    print("Phase 0 smoke test passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
