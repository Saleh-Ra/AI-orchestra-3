from __future__ import annotations

from crewai import Agent, LLM


def create_writer(llm: LLM) -> Agent:
    return Agent(
        role="Technical Writer",
        goal="Write a ~15-page Markdown article on {topic} from research and outline",
        backstory=(
            "You expand structured research into a full Hebrew technical article "
            "with clear chapters, following the architect's plan exactly."
        ),
        llm=llm,
        skills=["./skills/academic-writing"],
        verbose=True,
    )
