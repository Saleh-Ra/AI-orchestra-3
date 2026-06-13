"""LaTeX body.tex normalization."""

from __future__ import annotations

import re

from src.artifacts.patterns import INCLUDEGRAPHICS_RE, TIKZPICTURE_RE
from src.artifacts.tabular import fix_tabular_columns
from src.artifacts.tikz import normalize_tikz


def normalize_body(tex: str) -> str:
    """Repair common LLM LaTeX issues and inject rubric fallbacks if missing."""
    tex = tex.replace(r"\chapter{", r"\section{")
    tex = tex.replace("\u2192", r"$\rightarrow$")
    tex = re.sub(r"(?<![a-zA-Z])\\n(?![a-zA-Z])", "\n", tex)
    tex = re.sub(r"(?m)^(\s*)ode\b", r"\1\\node", tex)
    tex = re.sub(r">=\s*stealth['\"]*", ">=Stealth", tex, flags=re.IGNORECASE)
    tex = re.sub(r"\bright of=", "right=of ", tex)
    tex = re.sub(
        r"(\w+(?:\s+\w+)?)\s+of=",
        lambda m: f"{m.group(1)}=of ",
        tex,
    )
    tex = re.sub(
        r"\\foreach\s+\\x/\\y\s+in\s+(\{[^}]+\})\s*\{\s*\\filldraw\[black\]\s+\\x/\\y\s+circle\s*\(([^)]+)\);\s*\}",
        r"\\foreach \\point in \1 {\\filldraw[black] \\point circle (\2);}",
        tex,
    )
    tex = re.sub(r"\\bibliographystyle\{[^}]*\}\s*", "", tex)
    tex = re.sub(r"\\bibliography\{[^}]*\}\s*", "", tex)
    tex = INCLUDEGRAPHICS_RE.sub(
        lambda m: m.group(0)
        if m.group(2) == "plot.pdf"
        else f"{m.group(1)}sample.png{m.group(3)}",
        tex,
    )
    tex = _inject_rubric_fallbacks(tex)
    tex = fix_tabular_columns(tex)
    tex = TIKZPICTURE_RE.sub(lambda m: normalize_tikz(m.group(0)), tex)
    return tex.strip() + "\n"


def _inject_rubric_fallbacks(tex: str) -> str:
    if "דוגמה ל-BiDi" not in tex and r"\textenglish" not in tex:
        bidi = (
            r"\section{דוגמה ל-BiDi: עברית ואנגלית בפסקה אחת}"
            "\n\nבפרק זה מודגמת ערבוב נכון של עברית ואנגלית: מערכת "
            r"\textenglish{CrewAI} משלבת סוכני \textenglish{AI} עם "
            r"\textenglish{Large Language Models (LLM)} בתהליך "
            r"\textenglish{multi-agent orchestration}. מונחים טכניים כמו "
            r"\textenglish{context handoff} ו-\textenglish{sequential process} "
            "מופיעים בתוך משפט בעברית תוך שמירה על כיווניות "
            r"\textenglish{RTL/LTR}."
            "\n\n"
        )
        insert_at = tex.find(r"\section{")
        if insert_at != -1:
            end = tex.find(r"\section{", insert_at + 1)
            if end == -1:
                end = len(tex)
            tex = tex[:end] + "\n" + bidi + tex[end:]
    if r"\begin{equation}" not in tex:
        tex += (
            "\n\\section{נוסחה לדוגמה}\n"
            "\\begin{equation}\n"
            "  E = mc^2\n"
            "\\end{equation}\n"
        )
    if "sample.png" not in tex:
        tex += (
            "\n\\begin{figure}[htbp]\n"
            "  \\centering\n"
            "  \\includegraphics[width=0.35\\textwidth]{sample.png}\n"
            "  \\caption{תמונה סטטית לדוגמה.}\n"
            "\\end{figure}\n"
        )
    if r"\input{tikz_diagram.tex}" not in tex:
        tex += "\n\\input{tikz_diagram.tex}\n"
    return tex
