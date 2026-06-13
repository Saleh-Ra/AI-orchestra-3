from __future__ import annotations

from crewai import LLM, Agent


def create_editor(llm: LLM) -> Agent:
    return Agent(
        role="Senior Editor",
        goal="Polish the article and verify it meets the assignment rubric",
        backstory=(
            "You edit for clarity, consistency, and completeness. You check the draft "
            "against the planned outline and flag missing rubric elements."
        ),
        llm=llm,
        skills=["./skills/assignment-rubric", "./skills/academic-writing"],
        verbose=True,
    )
