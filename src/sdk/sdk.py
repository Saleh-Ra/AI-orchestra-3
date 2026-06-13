"""Single entry point for pipeline operations (submission guidelines SDK layer)."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from crewai import Crew, Process

from src.agents import create_researcher, create_writer
from src.artifacts import finalize_latex_outputs
from src.pipeline.compile_runner import assert_template_unchanged, run_project_script
from src.pipeline.crew_build import build_full_crew
from src.pipeline.paths import FIGURES_DIR, FINAL_PDF, LATEX_DIR, MARKDOWN_OUT, ROOT
from src.pipeline.save import save_full_crew_artifacts
from src.run_log import log_failure, write_run_log
from src.shared.config import get_project_settings, load_env
from src.shared.gatekeeper import get_llm
from src.tasks import create_research_task, create_write_task_poc

POC_DRAFT = ROOT / "output" / "markdown" / "draft.md"


def build_poc_crew() -> Crew:
    llm = get_llm()
    researcher = create_researcher(llm)
    writer = create_writer(llm)
    research_task = create_research_task(researcher)
    write_task = create_write_task_poc(writer, research_task)
    return Crew(
        agents=[researcher, writer],
        tasks=[research_task, write_task],
        process=Process.sequential,
        verbose=True,
    )


def recompile_latex(latex_dir: Path | None = None) -> None:
    """Normalize LaTeX artifacts and compile PDF without calling the LLM."""
    target = latex_dir or LATEX_DIR
    finalize_latex_outputs(target)
    run_project_script("scripts/run_figures.py")
    run_project_script("scripts/compile.ps1")


def run_poc(topic: str) -> int:
    load_env()
    crew = build_poc_crew()
    result = crew.kickoff(inputs={"topic": topic})
    POC_DRAFT.parent.mkdir(parents=True, exist_ok=True)
    POC_DRAFT.write_text(result.raw, encoding="utf-8")
    print(f"\nDraft saved to {POC_DRAFT.resolve()}")
    return 0


def run_full(
    topic: str,
    *,
    skip_compile: bool = False,
    validate: bool = False,
) -> int:
    load_env()
    settings = get_project_settings()
    print(f"Topic: {topic}")
    print(f"Cover author: {settings.cover_author}")
    print(f"Serper search: {settings.use_serper}")

    result = None
    try:
        result = build_full_crew().kickoff(inputs={"topic": topic})
        save_full_crew_artifacts(result)
    except Exception as exc:
        log_path = log_failure(topic, exc, result)
        print(f"Run failed — log: {log_path}", file=sys.stderr)
        raise

    print(f"Markdown: {MARKDOWN_OUT}")
    print(f"LaTeX: {LATEX_DIR / 'body.tex'}")
    assert_template_unchanged()

    run_project_script("scripts/run_figures.py")
    compile_ok = True
    compile_error: str | None = None
    if not skip_compile:
        try:
            run_project_script("scripts/compile.ps1")
            print(f"PDF: {FINAL_PDF}")
        except subprocess.CalledProcessError as exc:
            compile_ok = False
            compile_error = str(exc)

    artifacts = {
        "article_md": str(MARKDOWN_OUT),
        "body_tex": str(LATEX_DIR / "body.tex"),
        "references_bib": str(LATEX_DIR / "references.bib"),
        "plot_pdf": str(FIGURES_DIR / "plot.pdf"),
        "final_pdf": str(FINAL_PDF) if FINAL_PDF.is_file() else "",
    }
    log_path = write_run_log(
        topic=topic,
        success=compile_ok if not skip_compile else True,
        result=result,
        artifacts=artifacts,
        error=compile_error,
    )
    print(f"Run log: {log_path}")

    if compile_error:
        return 1
    if validate or not skip_compile:
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_outputs.py")],
            cwd=ROOT,
        )
        if proc.returncode != 0:
            return proc.returncode
    return 0
