from __future__ import annotations

from crewai import Agent, Task


def create_write_task(agent: Agent, research_task: Task) -> Task:
    return Task(
        description=(
            "Using only the research brief from the previous task, write a short "
            "article (~2 pages) about {topic}. Use Markdown: title, introduction, "
            "2–3 sections with ## headings, and a brief conclusion."
        ),
        expected_output="A Markdown article ready for human review.",
        agent=agent,
        context=[research_task],
    )
