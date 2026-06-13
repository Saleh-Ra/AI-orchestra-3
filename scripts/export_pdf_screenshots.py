"""Export key PDF pages as PNG screenshots for the submission packet."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PDF = ROOT / "output" / "final.pdf"
OUT_DIR = ROOT / "docs" / "screenshots"


def main() -> int:
    if not PDF.is_file():
        print(f"Missing {PDF} — compile first.", file=sys.stderr)
        return 1
    try:
        import fitz  # pymupdf
    except ImportError:
        print("Install pymupdf: uv sync --extra dev", file=sys.stderr)
        return 1

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(PDF)
    page_count = doc.page_count
    exports = [
        ("01_cover.png", 0),
        ("02_toc.png", 1),
        ("03_body_bidi.png", min(2, page_count - 1)),
        ("04_bibliography.png", page_count - 1),
    ]
    for name, index in exports:
        path = OUT_DIR / name
        doc[index].get_pixmap(matrix=fitz.Matrix(2, 2)).save(path)
        print(f"Wrote {path}")
    doc.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
