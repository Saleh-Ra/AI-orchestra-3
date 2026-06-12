from __future__ import annotations

from crewai import Agent, Task


def create_edit_task(
    agent: Agent,
    write_task: Task,
    plan_task: Task,
) -> Task:
    return Task(
        description=(
            "Edit the Markdown draft for {topic}. Verify it follows the chapter plan and "
            "assignment rubric. Fix repetition, gaps, and weak transitions."
        ),
        expected_output=(
            "Polished Markdown article plus a final section '## Rubric checklist' listing "
            "which assignment items the text supports (BiDi chapter, table, formula, etc.)."
        ),
        agent=agent,
        context=[write_task, plan_task],
    )
