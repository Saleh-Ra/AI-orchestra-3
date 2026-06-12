from __future__ import annotations

from crewai import Agent, LLM


def create_planner(llm: LLM) -> Agent:
    return Agent(
        role="Document Architect",
        goal="Design a clear chapter structure for a ~15-page article on {topic}",
        backstory=(
            "You plan long technical documents. You decide chapter titles, section flow, "
            "and which chapters need figures, tables, formulas, or a BiDi English mix."
        ),
        llm=llm,
        verbose=True,
    )
