"""Persist crew task outputs to disk."""

from __future__ import annotations

from src.artifacts import (
    clear_latex_outputs,
    finalize_latex_outputs,
    write_latex_artifacts,
    write_visuals_artifacts,
)
from src.pipeline.paths import FIGURES_DIR, LATEX_DIR, MARKDOWN_OUT, ROOT


def save_full_crew_artifacts(result) -> None:
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
    write_latex_artifacts(outputs[5].raw, LATEX_DIR)
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
