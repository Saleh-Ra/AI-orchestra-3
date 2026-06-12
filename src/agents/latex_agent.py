from __future__ import annotations

from crewai import Agent, LLM


def create_latex_agent(llm: LLM) -> Agent:
    return Agent(
        role="LaTeX Specialist",
        goal="Convert the polished article into body.tex and references.bib for LuaLaTeX",
        backstory=(
            "You format Hebrew/English technical documents in LaTeX. You never write "
            "preambles — only chapter body fragments and bibliography entries."
        ),
        llm=llm,
        skills=["./skills/latex-bidi"],
        verbose=True,
    )
