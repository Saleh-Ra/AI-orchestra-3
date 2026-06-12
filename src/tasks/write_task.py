from __future__ import annotations

from crewai import Agent, Task


def create_write_task(
    agent: Agent,
    research_task: Task,
    plan_task: Task,
) -> Task:
    return Task(
        description=(
            "Write the full article on {topic} in Markdown using the research and chapter plan. "
            "Target ~15 pages of substantive Hebrew content with English technical terms where needed."
        ),
        expected_output=(
            "Complete Markdown article: title, introduction, all planned chapters with ## headings, "
            "conclusion. Include placeholder notes like [TABLE], [FORMULA] where the plan requires them."
        ),
        agent=agent,
        context=[research_task, plan_task],
    )


def create_write_task_poc(agent: Agent, research_task: Task) -> Task:
    """Shorter write task for Phase 1 POC."""
    return Task(
        description=(
            "Using only the research brief, write a short article (~2 pages) about {topic}. "
            "Use Markdown with title, introduction, 2–3 sections, conclusion."
        ),
        expected_output="A Markdown article ready for human review.",
        agent=agent,
        context=[research_task],
    )
