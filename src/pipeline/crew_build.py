"""Build the six-agent submission crew."""

from __future__ import annotations

from crewai import Crew, Process

from src.agents import (
    create_editor,
    create_latex_agent,
    create_planner,
    create_researcher,
    create_visualizer,
    create_writer,
)
from src.shared.gatekeeper import get_llm
from src.tasks import (
    create_edit_task,
    create_latex_task,
    create_plan_task,
    create_research_task,
    create_visuals_task,
    create_write_task,
)


def build_full_crew() -> Crew:
    llm = get_llm()
    researcher = create_researcher(llm)
    planner = create_planner(llm)
    writer = create_writer(llm)
    editor = create_editor(llm)
    visualizer = create_visualizer(llm)
    latex_agent = create_latex_agent(llm)

    research_task = create_research_task(researcher)
    plan_task = create_plan_task(planner, research_task)
    write_task = create_write_task(writer, research_task, plan_task)
    edit_task = create_edit_task(editor, write_task, plan_task)
    visuals_task = create_visuals_task(visualizer, edit_task, plan_task)
    latex_task = create_latex_task(
        latex_agent, edit_task, plan_task, research_task, visuals_task
    )

    return Crew(
        agents=[researcher, planner, writer, editor, visualizer, latex_agent],
        tasks=[
            research_task,
            plan_task,
            write_task,
            edit_task,
            visuals_task,
            latex_task,
        ],
        process=Process.sequential,
        verbose=True,
    )
