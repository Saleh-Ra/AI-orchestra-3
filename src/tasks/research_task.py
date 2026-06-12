from __future__ import annotations

from crewai import Agent, Task


def create_research_task(agent: Agent) -> Task:
    return Task(
        description=(
            "Research the topic: {topic}. "
            "Collect key facts, definitions, and notable points. "
            "List any sources you rely on."
        ),
        expected_output=(
            "A structured research brief with bullet-point facts and a short "
            "list of sources (title and URL or author when known)."
        ),
        agent=agent,
    )
