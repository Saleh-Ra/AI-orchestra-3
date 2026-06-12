from __future__ import annotations

from crewai import Agent, LLM


def create_writer(llm: LLM) -> Agent:
    return Agent(
        role="Technical Writer",
        goal="Turn research notes into a clear, readable short article",
        backstory=(
            "You transform structured research into accessible prose. "
            "You write in Markdown with headings and short paragraphs."
        ),
        llm=llm,
        verbose=True,
    )
