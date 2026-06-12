from __future__ import annotations

from crewai import Agent, Task


def create_plan_task(agent: Agent, research_task: Task) -> Task:
    return Task(
        description=(
            "Using the research JSON, plan a ~15-page article on {topic}. "
            "Mark exactly one chapter as bidi_chapter for Hebrew+English mix."
        ),
        expected_output=(
            "Valid JSON: title (string), chapters (array of objects with title, sections "
            "(string array), needs_figure, needs_formula, needs_table, bidi_chapter booleans)."
        ),
        agent=agent,
        context=[research_task],
    )
