"""Phase 3: full six-agent crew → Markdown, LaTeX, figures, PDF."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from crewai import Crew, Process

from src.agents import (
    create_editor,
    create_latex_agent,
    create_planner,
    create_researcher,
    create_visualizer,
    create_writer,
)
from src.artifacts import (
    clear_latex_outputs,
    finalize_latex_outputs,
    write_latex_artifacts,
    write_visuals_artifacts,
)
from src.config import DEFAULT_TOPIC, get_llm, get_project_settings, load_env
from src.tasks import (
    create_edit_task,
    create_latex_task,
    create_plan_task,
    create_research_task,
    create_visuals_task,
    create_write_task,
)

ROOT = Path(__file__).resolve().parent.parent
MARKDOWN_OUT = ROOT / "output" / "markdown" / "article.md"
LATEX_DIR = ROOT / "output" / "latex"
FIGURES_DIR = ROOT / "output" / "figures"
TEMPLATE_MAIN = ROOT / "templates" / "main.tex"


def build_crew() -> Crew:
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


def _save_artifacts(result) -> None:
    outputs = result.tasks_output
    if len(outputs) < 6:
        raise RuntimeError(f"Expected 6 task outputs, got {len(outputs)}")

    debug_dir = ROOT / "output" / "debug"
    debug_dir.mkdir(parents=True, exist_ok=True)
    for i, out in enumerate(outputs):
        (debug_dir / f"task_{i}.txt").write_text(out.raw, encoding="utf-8")

    MARKDOWN_OUT.parent.mkdir(parents=True, exist_ok=True)
    MARKDOWN_OUT.write_text(outputs[3].raw, encoding="utf-8")

    clear_latex_outputs(LATEX_DIR)

    vis_written = write_visuals_artifacts(outputs[4].raw, FIGURES_DIR, LATEX_DIR)
    latex_written = write_latex_artifacts(outputs[5].raw, LATEX_DIR)
    finalize_latex_outputs(LATEX_DIR)

    if not (LATEX_DIR / "body.tex").is_file():
        raise RuntimeError(
            "LaTeX agent did not produce body.tex — see output/debug/task_5.txt"
        )
    if not (LATEX_DIR / "references.bib").is_file():
        raise RuntimeError("LaTeX agent did not produce references.bib")
    if not vis_written and not (LATEX_DIR / "tikz_diagram.tex").is_file():
        raise RuntimeError(
            "Visualizer did not produce tikz_diagram.tex — see output/debug/task_4.txt"
        )
    _ = latex_written


def _assert_template_unchanged() -> None:
    text = TEMPLATE_MAIN.read_text(encoding="utf-8")
    if "\\begin{document}" not in text or "\\documentclass" not in text:
        raise RuntimeError("templates/main.tex looks corrupted")
    if "body.tex" not in text and r"\input{body.tex}" not in text:
        raise RuntimeError("templates/main.tex must input body.tex only")


def _run_script(rel: str) -> None:
    path = ROOT / rel
    if rel.endswith(".ps1"):
        subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", str(path)],
            check=True,
            cwd=ROOT,
        )
    else:
        subprocess.run([sys.executable, str(path)], check=True, cwd=ROOT)


def main() -> int:
    load_env()
    settings = get_project_settings()

    parser = argparse.ArgumentParser(description="Phase 3 full six-agent pipeline")
    parser.add_argument("--topic", default=settings.topic, help="Article topic")
    parser.add_argument(
        "--skip-compile",
        action="store_true",
        help="Stop after saving LaTeX artifacts (no PDF)",
    )
    args = parser.parse_args()

    print(f"Topic: {args.topic}")
    print(f"Cover author: {settings.cover_author}")
    print(f"Serper search: {settings.use_serper}")

    crew = build_crew()
    result = crew.kickoff(inputs={"topic": args.topic})

    _save_artifacts(result)
    print(f"Markdown: {MARKDOWN_OUT}")
    print(f"LaTeX: {LATEX_DIR / 'body.tex'}")

    _assert_template_unchanged()

    _run_script("scripts/run_figures.py")
    if not args.skip_compile:
        _run_script("scripts/compile.ps1")
        print(f"PDF: {ROOT / 'output' / 'final.pdf'}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
