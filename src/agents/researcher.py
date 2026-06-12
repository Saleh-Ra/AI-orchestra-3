from __future__ import annotations

from crewai import Agent, LLM


def create_researcher(llm: LLM) -> Agent:
    return Agent(
        role="Market Research Analyst",
        goal="Find accurate, relevant information on the given topic",
        backstory=(
            "You are a meticulous research analyst. You identify key concepts, "
            "credible sources, and facts that others can turn into clear writing."
        ),
        llm=llm,
        verbose=True,
    )
