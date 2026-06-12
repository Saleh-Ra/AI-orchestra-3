from __future__ import annotations

from crewai import Agent, Task


def create_research_task(agent: Agent) -> Task:
    return Task(
        description=(
            "Research the topic: {topic}. Return structured findings only — not a full article."
        ),
        expected_output=(
            "Valid JSON with keys: facts (string array), sources (array of objects with "
            "title, author, year, url), figure_ideas, formula_ideas, table_ideas (string arrays)."
        ),
        agent=agent,
    )
