"""Artifact I/O and fence extraction tests."""

from __future__ import annotations

from pathlib import Path

from src.artifacts.fences import extract_fenced_blocks, match_label, write_named_artifacts
from src.artifacts.io import (
    clear_latex_outputs,
    finalize_latex_outputs,
    write_latex_artifacts,
    write_visuals_artifacts,
)
from src.artifacts.textenglish import sanitize_textenglish, wrap_textenglish


def test_extract_fenced_blocks() -> None:
    text = "```body.tex\n\\section{A}\n```\n```python\nprint(1)\n```"
    blocks = extract_fenced_blocks(text)
    assert len(blocks) == 2
    assert blocks[0][0] == "body.tex"
    assert r"\section{A}" in blocks[0][1]


def test_match_label() -> None:
    assert match_label("references.bib", "references.bib", ".bib")
    assert not match_label(None, "bib")


def test_wrap_and_sanitize_textenglish() -> None:
    assert r"\textenglish{Hello}" in wrap_textenglish("Hello")
    assert wrap_textenglish("שלום") == "שלום"
    dirty = r"\textenglish{foo\\nbar}"
    assert sanitize_textenglish(dirty) == r"\textenglish{foo bar}"


def test_finalize_and_clear_latex(tmp_path: Path) -> None:
    body = tmp_path / "body.tex"
    tikz = tmp_path / "tikz_diagram.tex"
    body.write_text("ode (x) {}\n", encoding="utf-8")
    tikz.write_text(r"\node[startstop] (a) {A};", encoding="utf-8")
    finalize_latex_outputs(tmp_path)
    assert r"\node" in body.read_text(encoding="utf-8")
    assert r"\begin{tikzpicture}" in tikz.read_text(encoding="utf-8")
    clear_latex_outputs(tmp_path)
    assert not body.exists()
    assert not tikz.exists()


def test_write_latex_artifacts(tmp_path: Path) -> None:
    text = (
        "```body.tex\n"
        r"\section{Intro}" + "\n"
        "```\n"
        "```references.bib\n"
        "@article{a, title={T}}\n"
        "```"
    )
    written = write_latex_artifacts(text, tmp_path)
    names = {p.name for p in written}
    assert "body.tex" in names
    assert "references.bib" in names
    assert r"\section{Intro}" in (tmp_path / "body.tex").read_text(encoding="utf-8")


def test_write_visuals_artifacts(tmp_path: Path) -> None:
    figures = tmp_path / "figures"
    latex = tmp_path / "latex"
    text = (
        "```tikz_diagram.tex\n"
        r"\begin{tikzpicture}\node (a) {A};\end{tikzpicture}" + "\n"
        "```\n"
        "```python\n"
        "import matplotlib.pyplot as plt\nplt.savefig('plot.pdf')\n"
        "```"
    )
    written = write_visuals_artifacts(text, figures, latex)
    assert any(p.name == "plot_script.py" for p in written)
    assert (latex / "tikz_diagram.tex").is_file()


def test_write_named_artifacts(tmp_path: Path) -> None:
    mapping = {"body.tex": tmp_path / "body.tex"}
    write_named_artifacts("```body.tex\n\\section{X}\n```", mapping)
    assert (tmp_path / "body.tex").is_file()
