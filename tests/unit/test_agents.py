"""Agent factory smoke tests."""

from __future__ import annotations

from crewai import LLM

from src.agents import (
    create_editor,
    create_latex_agent,
    create_planner,
    create_researcher,
    create_visualizer,
    create_writer,
)


def test_all_agent_factories() -> None:
    llm = LLM(model="gpt-4.1-mini")
    for factory in (
        create_researcher,
        create_planner,
        create_writer,
        create_editor,
        create_visualizer,
        create_latex_agent,
    ):
        agent = factory(llm)
        assert agent.role
        assert agent.llm is llm
