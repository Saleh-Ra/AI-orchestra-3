"""Validate Assignment 03 outputs against the technical rubric."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LATEX_DIR = ROOT / "output" / "latex"
FIGURES_DIR = ROOT / "output" / "figures"
FINAL_PDF = ROOT / "output" / "final.pdf"
MAIN_LOG = LATEX_DIR / "main.log"
COVER_TEX = LATEX_DIR / "cover.tex"
BODY_TEX = LATEX_DIR / "body.tex"
BIB_TEX = LATEX_DIR / "references.bib"
TIKZ_TEX = LATEX_DIR / "tikz_diagram.tex"


def _page_count() -> int | None:
    if not MAIN_LOG.is_file():
        return None
    match = re.search(r"Output written on main\.pdf \((\d+) pages", MAIN_LOG.read_text(encoding="utf-8", errors="replace"))
    return int(match.group(1)) if match else None


def _cite_bib_keys(body: str, bib: str) -> tuple[set[str], set[str]]:
    cite_keys: set[str] = set()
    for match in re.finditer(r"\\cite\{([^}]+)\}", body):
        for key in match.group(1).split(","):
            cite_keys.add(key.strip())
    bib_keys = set(re.findall(r"@\w+\{([^,]+),", bib))
    return cite_keys, bib_keys


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    if not FINAL_PDF.is_file():
        errors.append(f"Missing {FINAL_PDF}")
    for path in (BODY_TEX, BIB_TEX, TIKZ_TEX, FIGURES_DIR / "plot.pdf", FIGURES_DIR / "plot_script.py"):
        if not path.is_file():
            errors.append(f"Missing {path}")

    if COVER_TEX.is_file():
        cover = COVER_TEX.read_text(encoding="utf-8")
        for macro in ("coversubject", "coverauthor", "covercourse", "coversemester", "coverdate"):
            if macro not in cover:
                errors.append(f"cover.tex missing \\{macro}")
        if "שם הסטודנט" in cover or "Your Name" in cover:
            warnings.append("COVER_AUTHOR still looks like a placeholder — set your real name in .env")

    body = BODY_TEX.read_text(encoding="utf-8") if BODY_TEX.is_file() else ""
    bib = BIB_TEX.read_text(encoding="utf-8") if BIB_TEX.is_file() else ""
    cite_keys, bib_keys = _cite_bib_keys(body, bib)
    missing = cite_keys - bib_keys
    if missing:
        errors.append(f"Cite keys missing from references.bib: {sorted(missing)}")

    checks = {
        "sections": r"\section" in body,
        "equation": r"\begin{equation}" in body,
        "table": r"\begin{tabular}" in body,
        "plot.pdf": "plot.pdf" in body,
        "tikz input": r"\input{tikz_diagram.tex}" in body,
        "static image": "sample.png" in body,
        "bidi textenglish": r"\textenglish" in body,
        "bibliography command": r"\printbibliography" in (ROOT / "templates" / "main.tex").read_text(encoding="utf-8"),
    }
    for name, ok in checks.items():
        if not ok:
            errors.append(f"Rubric element missing: {name}")

    pages = _page_count()
    if pages is None:
        warnings.append("Could not read page count from main.log — run compile.ps1 first")
    elif pages < 13:
        warnings.append(f"PDF has {pages} pages; rubric targets ~15 (incl. cover)")
    elif pages > 20:
        warnings.append(f"PDF has {pages} pages — unusually long")

    toc = LATEX_DIR / "main.toc"
    if not toc.is_file() or len(toc.read_text(encoding="utf-8").strip()) < 20:
        errors.append("Table of contents (main.toc) empty or missing")

    if MAIN_LOG.is_file():
        log = MAIN_LOG.read_text(encoding="utf-8", errors="replace")
        if "!  ==> Fatal error" in log or "! LaTeX Error:" in log:
            errors.append("main.log contains LaTeX errors")
        if "undefined on input" in log and "Citation" in log:
            warnings.append("Unresolved citations in log — rerun full compile (lualatex + biber)")

    print("=== Assignment 03 output validation ===")
    print(f"PDF: {FINAL_PDF} ({'ok' if FINAL_PDF.is_file() else 'missing'})")
    if pages:
        print(f"Pages: {pages}")
    print(f"Cite keys: {len(cite_keys)} | Bib keys: {len(bib_keys)}")
    for name, ok in checks.items():
        print(f"  [{('ok' if ok else 'FAIL')}] {name}")

    if warnings:
        print("\nWarnings:")
        for w in warnings:
            print(f"  - {w}")
    if errors:
        print("\nErrors:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print("\nAll rubric checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
