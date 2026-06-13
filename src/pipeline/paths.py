"""Project root and output paths."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
MARKDOWN_OUT = ROOT / "output" / "markdown" / "article.md"
LATEX_DIR = ROOT / "output" / "latex"
FIGURES_DIR = ROOT / "output" / "figures"
TEMPLATE_MAIN = ROOT / "templates" / "main.tex"
FINAL_PDF = ROOT / "output" / "final.pdf"
