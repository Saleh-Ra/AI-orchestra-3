"""Phase 1 POC: Researcher → Writer via CrewAI sequential crew."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from crewai import Crew, Process

from src.agents import create_researcher, create_writer
from src.config import get_llm, load_env
from src.tasks import create_research_task, create_write_task

DEFAULT_TOPIC = "CrewAI multi-agent teams for document generation"
OUTPUT_PATH = Path("output/markdown/draft.md")


def build_crew() -> Crew:
    llm = get_llm()
    researcher = create_researcher(llm)
    writer = create_writer(llm)

    research_task = create_research_task(researcher)
    write_task = create_write_task(writer, research_task)

    return Crew(
        agents=[researcher, writer],
        tasks=[research_task, write_task],
        process=Process.sequential,
        verbose=True,
    )


def main() -> int:
    load_env()
    parser = argparse.ArgumentParser(description="Phase 1 two-agent CrewAI POC")
    parser.add_argument("--topic", default=DEFAULT_TOPIC, help="Article topic")
    args = parser.parse_args()

    print(f"Topic: {args.topic}")
    crew = build_crew()
    result = crew.kickoff(inputs={"topic": args.topic})

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(result.raw, encoding="utf-8")
    print(f"\nDraft saved to {OUTPUT_PATH.resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
