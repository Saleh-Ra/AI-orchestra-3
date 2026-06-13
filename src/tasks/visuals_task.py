from __future__ import annotations

from crewai import Agent, Task


def create_visuals_task(
    agent: Agent,
    edit_task: Task,
    plan_task: Task,
) -> Task:
    return Task(
        description=(
            "Create figure assets for the article on {topic}. The plot should relate to the "
            "subject (e.g. agent pipeline stages). TikZ: simple 3-node horizontal flow."
        ),
        expected_output=(
            "EXACTLY three markdown fenced code blocks with these first-line labels:\n"
            "1. ```plot_script.py — matplotlib script that saves plot.pdf\n"
            "2. ```tikz_diagram.tex — standalone TikZ picture (3-node flow); one-line labels only, no line breaks; no startstop/process/decision styles\n"
            "3. ```image_spec.txt — caption/alt text for the static image"
        ),
        agent=agent,
        context=[edit_task, plan_task],
    )
