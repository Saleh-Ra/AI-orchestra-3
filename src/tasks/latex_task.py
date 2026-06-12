from __future__ import annotations

from crewai import Agent, Task


def create_latex_task(
    agent: Agent,
    edit_task: Task,
    plan_task: Task,
    research_task: Task,
    visuals_task: Task,
) -> Task:
    return Task(
        description=(
            "Convert the polished Markdown article on {topic} into LaTeX body fragments. "
            "Use research sources for references.bib. Embed the TikZ diagram and plot.pdf. "
            "Do NOT output a preamble or \\documentclass."
        ),
        expected_output=(
            "EXACTLY two markdown fenced code blocks with these first-line labels:\n"
            "1. ```body.tex — full chapter with sections, equation, table, plot.pdf figure, "
            "tikz_diagram.tex input, and backslash-cite commands; no documentclass or preamble.\n"
            "2. ```references.bib — valid BibTeX for every cite key used in body.tex."
        ),
        agent=agent,
        context=[edit_task, plan_task, research_task, visuals_task],
    )
