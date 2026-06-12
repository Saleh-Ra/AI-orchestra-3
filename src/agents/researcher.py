from __future__ import annotations

from crewai import Agent, LLM

from src.config import get_project_settings


def _research_tools() -> list:
    if not get_project_settings().use_serper:
        return []
    try:
        from crewai_tools import SerperDevTool
    except ImportError:
        return []
    return [SerperDevTool()]


def create_researcher(llm: LLM) -> Agent:
    return Agent(
        role="Academic Researcher",
        goal="Gather structured research on {topic} with citable sources",
        backstory=(
            "You collect facts, definitions, and credible sources. You suggest where "
            "figures, tables, and formulas would strengthen the article."
        ),
        llm=llm,
        tools=_research_tools(),
        verbose=True,
    )
