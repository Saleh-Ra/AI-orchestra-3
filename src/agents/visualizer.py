from __future__ import annotations

from crewai import Agent, LLM


def create_visualizer(llm: LLM) -> Agent:
    return Agent(
        role="Scientific Visualizer",
        goal="Produce matplotlib and TikZ figure assets for the article",
        backstory=(
            "You create data visualizations and block diagrams. You write Python plotting "
            "code and TikZ snippets that LaTeX can include directly."
        ),
        llm=llm,
        skills=["./skills/figures-and-diagrams"],
        verbose=True,
    )
