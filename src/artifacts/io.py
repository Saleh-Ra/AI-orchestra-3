"""Write and finalize LaTeX/visual artifact files from agent output."""

from __future__ import annotations

from pathlib import Path

from src.artifacts.body import normalize_body
from src.artifacts.fences import extract_fenced_blocks, match_label, write_named_artifacts
from src.artifacts.tikz import normalize_tikz


def finalize_latex_outputs(latex_dir: Path) -> None:
    """Normalize body.tex and tikz_diagram.tex in place."""
    body = latex_dir / "body.tex"
    tikz = latex_dir / "tikz_diagram.tex"
    if body.is_file():
        body.write_text(
            normalize_body(body.read_text(encoding="utf-8")),
            encoding="utf-8",
        )
    if tikz.is_file():
        tikz.write_text(
            normalize_tikz(tikz.read_text(encoding="utf-8")),
            encoding="utf-8",
        )


def clear_latex_outputs(latex_dir: Path) -> None:
    for name in ("body.tex", "references.bib", "tikz_diagram.tex"):
        path = latex_dir / name
        if path.is_file():
            path.unlink()


def write_visuals_artifacts(text: str, figures_dir: Path, latex_dir: Path) -> list[Path]:
    mapping = {
        "plot_script.py": figures_dir / "plot_script.py",
        "tikz_diagram.tex": latex_dir / "tikz_diagram.tex",
        "image_spec.txt": figures_dir / "image_spec.txt",
    }
    written = write_named_artifacts(text, mapping)
    for label, body in extract_fenced_blocks(text):
        if label and "tikz" in label.lower():
            path = latex_dir / "tikz_diagram.tex"
            path.write_text(body + "\n", encoding="utf-8")
            if path not in written:
                written.append(path)
        elif label in (None, "python", "py") and (
            "matplotlib" in body or "plot.pdf" in body
        ):
            path = figures_dir / "plot_script.py"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(body + "\n", encoding="utf-8")
            if path not in written:
                written.append(path)
    return written


def write_latex_artifacts(text: str, latex_dir: Path) -> list[Path]:
    latex_dir.mkdir(parents=True, exist_ok=True)
    mapping = {
        "body.tex": latex_dir / "body.tex",
        "references.bib": latex_dir / "references.bib",
        "plot_script.py": latex_dir.parent / "figures" / "plot_script.py",
        "tikz_diagram.tex": latex_dir / "tikz_diagram.tex",
    }
    written = write_named_artifacts(text, mapping)
    for label, body in extract_fenced_blocks(text):
        if match_label(label, "references.bib", ".bib", "bibtex"):
            path = latex_dir / "references.bib"
            path.write_text(body + "\n", encoding="utf-8")
            if path not in written:
                written.append(path)
        elif match_label(label, "body.tex", "body", "latex") or (
            label and "tex" in label.lower() and "tikz" not in label.lower()
        ):
            if "\\section" in body or "\\chapter" in body or "\\begin{" in body:
                path = latex_dir / "body.tex"
                path.write_text(body + "\n", encoding="utf-8")
                if path not in written:
                    written.append(path)
        elif label and "tikz" in label.lower():
            path = latex_dir / "tikz_diagram.tex"
            path.write_text(body + "\n", encoding="utf-8")
            if path not in written:
                written.append(path)
    if not any(p.name == "body.tex" for p in written):
        start = -1
        for marker in ("\\section", "\\chapter"):
            pos = text.find(marker)
            if pos != -1 and (start == -1 or pos < start):
                start = pos
        if start != -1:
            path = latex_dir / "body.tex"
            path.write_text(text[start:].strip() + "\n", encoding="utf-8")
            written.append(path)
    finalize_latex_outputs(latex_dir)
    return written
