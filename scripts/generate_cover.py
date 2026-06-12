"""Write output/latex/cover.tex from .env cover metadata."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.config import get_project_settings  # noqa: E402


def _tex_escape(value: str) -> str:
    return (
        value.replace("\\", r"\textbackslash{}")
        .replace("{", r"\{")
        .replace("}", r"\}")
        .replace("#", r"\#")
        .replace("%", r"\%")
        .replace("&", r"\&")
    )


def main() -> int:
    s = get_project_settings()
    out = ROOT / "output" / "latex" / "cover.tex"
    out.parent.mkdir(parents=True, exist_ok=True)
    content = f"""% Auto-generated from .env — do not edit by hand
\\renewcommand{{\\coversubject}}{{{_tex_escape(s.topic)}}}
\\renewcommand{{\\coverauthor}}{{{_tex_escape(s.cover_author)}}}
\\renewcommand{{\\covercourse}}{{{_tex_escape(s.cover_course)}}}
\\renewcommand{{\\coversemester}}{{{_tex_escape(s.cover_semester)}}}
\\renewcommand{{\\coverdate}}{{{_tex_escape(s.cover_date)}}}
"""
    out.write_text(content, encoding="utf-8")
    print(f"Wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
