"""Task factory smoke tests."""

from __future__ import annotations

from crewai import LLM, Agent, Task

from src.tasks import (
    create_edit_task,
    create_latex_task,
    create_plan_task,
    create_research_task,
    create_visuals_task,
    create_write_task,
    create_write_task_poc,
)


def _agent(name: str) -> Agent:
    return Agent(role=name, goal="g", backstory="b", llm=LLM(model="gpt-4.1-mini"))


def test_task_factories_chain() -> None:
    researcher = _agent("Researcher")
    planner = _agent("Planner")
    writer = _agent("Writer")
    editor = _agent("Editor")
    visualizer = _agent("Visualizer")
    latex = _agent("LaTeX")

    research_task = create_research_task(researcher)
    plan_task = create_plan_task(planner, research_task)
    write_task = create_write_task(writer, research_task, plan_task)
    edit_task = create_edit_task(editor, write_task, plan_task)
    visuals_task = create_visuals_task(visualizer, edit_task, plan_task)
    latex_task = create_latex_task(latex, edit_task, plan_task, research_task, visuals_task)
    poc_write = create_write_task_poc(writer, research_task)

    for task in (
        research_task,
        plan_task,
        write_task,
        edit_task,
        visuals_task,
        latex_task,
        poc_write,
    ):
        assert isinstance(task, Task)
