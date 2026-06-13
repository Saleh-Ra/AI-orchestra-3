"""Extract fenced code blocks from agent outputs into project files."""

from __future__ import annotations

import re
from pathlib import Path

FENCE_RE = re.compile(
    r"```([^\n`]*)\n(.*?)```",
    re.DOTALL,
)
TIKZPICTURE_RE = re.compile(
    r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}",
    re.DOTALL,
)
INCLUDEGRAPHICS_RE = re.compile(
    r"(\\includegraphics(?:\[[^\]]*\])?\{)([^}]+)(\})",
)
TABULAR_RE = re.compile(
    r"\\begin\{tabular\}\{([^}]+)\}(.*?)\\end\{tabular\}",
    re.DOTALL,
)


def _tabular_spec_column_count(spec: str) -> int:
    return len(re.findall(r"[lcr]", spec, re.IGNORECASE))


def _max_tabular_row_columns(content: str) -> int:
    max_cols = 0
    for line in content.splitlines():
        line = line.strip()
        if not line or line.startswith("%") or line.startswith("\\hline"):
            continue
        if "&" in line:
            max_cols = max(max_cols, line.count("&") + 1)
    return max_cols


def fix_tabular_columns(tex: str) -> str:
    def repl(match: re.Match[str]) -> str:
        spec, content = match.group(1), match.group(2)
        needed = _max_tabular_row_columns(content)
        current = _tabular_spec_column_count(spec)
        if current >= needed:
            return match.group(0)
        extra = needed - current
        if spec.endswith("|"):
            new_spec = spec.rstrip("|") + "|l|" * extra + "|"
        else:
            new_spec = spec + "l" * extra
        return rf"\begin{{tabular}}{{{new_spec}}}{content}\end{{tabular}}"

    return TABULAR_RE.sub(repl, tex)


def extract_fenced_blocks(text: str) -> list[tuple[str | None, str]]:
    blocks: list[tuple[str | None, str]] = []
    for match in FENCE_RE.finditer(text):
        label = (match.group(1) or "").strip() or None
        body = match.group(2).strip()
        if body:
            blocks.append((label, body))
    return blocks


def _match_label(label: str | None, *needles: str) -> bool:
    if not label:
        return False
    norm = label.lower().replace("\\", "/")
    return any(n in norm for n in needles)


def write_named_artifacts(
    text: str,
    mapping: dict[str, Path],
) -> list[Path]:
    written: list[Path] = []
    for label, body in extract_fenced_blocks(text):
        if not label:
            continue
        norm = label.lower().replace("\\", "/")
        for key, path in mapping.items():
            if key.lower() in norm or norm.endswith(key.lower()):
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(body + "\n", encoding="utf-8")
                written.append(path)
                break
    return written


def _wrap_textenglish(label: str) -> str:
    if "\\textenglish" in label or not re.search(r"[A-Za-z]", label):
        return label
    return rf"\textenglish{{{label}}}"


def _sanitize_textenglish(tex: str) -> str:
    def fix(match: re.Match[str]) -> str:
        inner = match.group(1)
        inner = re.sub(r"\\+\[[^\]]*\]", " ", inner)
        inner = re.sub(r"\\+n", " ", inner)
        inner = re.sub(r"\\+", " ", inner)
        inner = re.sub(r"\s+", " ", inner).strip()
        return rf"\textenglish{{{inner}}}"

    return re.sub(r"\\textenglish\{([^}]*)\}", fix, tex)


def _sanitize_tikz_labels(tex: str) -> str:
    tex = _sanitize_textenglish(tex)
    tex = re.sub(r"\\+\[[^\]]*\]", " ", tex)
    return tex


_TIKZ_NODE_STYLE = (
    "draw, rounded corners, align=center, font=\\small, "
    "minimum width=2.2cm, minimum height=1cm"
)
_INVALID_FLOWCHART_STYLES = re.compile(
    r"\b(?:startstop|process|decision|io|cloud|database|storage|connector|"
    r"preparation|predefinedprocess|dashedbox)\b",
    re.IGNORECASE,
)
_NODE_LABEL_PATTERNS = (
    r"\\node\s*(?:\[[^\]]*\]\s*)?(?:\([^)]+\)\s*)?\{([^}]+)\}",
    r"\\node\s*(?:\([^)]+\)\s*)?(?:\[[^\]]*\]\s*)?\{([^}]+)\}",
)


def _extract_tikz_labels(tex: str) -> list[str]:
    labels: list[str] = []
    for pattern in _NODE_LABEL_PATTERNS:
        for match in re.finditer(pattern, tex):
            label = match.group(1).strip()
            if label and label not in labels:
                labels.append(label)
    return labels


def _needs_tikz_rebuild(tex: str) -> bool:
    if re.search(r"stealth['\"]|\\tikzstyle|every node/.style=\{font=", tex):
        return True
    if _INVALID_FLOWCHART_STYLES.search(tex):
        return True
    if re.search(r"\\foreach\s+\\x/\\y", tex):
        return True
    labels = _extract_tikz_labels(tex)
    positioned = any(
        token in tex
        for token in ("right=of", "below=of", "above=of", "left=of", "below right=of")
    )
    if len(labels) >= 2 and not positioned:
        return True
    return False


def _build_simple_tikz(labels: list[str] | None = None) -> str:
    names = list(labels or [])
    defaults = ["Research", "Plan", "Write"]
    while len(names) < 3:
        names.append(defaults[len(names)])
    names = names[:5]
    ids = [f"n{i}" for i in range(len(names))]
    lines = [
        "\\begin{tikzpicture}[node distance=2.2cm and 1.8cm, "
        f"every node/.style={{{_TIKZ_NODE_STYLE}}}, >=Stealth]",
    ]
    for i, (node_id, label) in enumerate(zip(ids, names)):
        inner = label
        if "\\textenglish" not in inner:
            inner = _wrap_textenglish(inner)
        if i == 0:
            lines.append(f"\\node ({node_id}) {{{inner}}};")
        else:
            prev = ids[i - 1]
            lines.append(f"\\node[right=of {prev}] ({node_id}) {{{inner}}};")
    for i in range(1, len(ids)):
        lines.append(f"\\draw[->, thick] ({ids[i - 1]}) -- ({ids[i]});")
    lines.append("\\end{tikzpicture}")
    return "\n".join(lines) + "\n"


def _sanitize_tikz_picture_block(tex: str) -> str:
    return normalize_tikz(tex)


def normalize_tikz(tex: str) -> str:
    match = TIKZPICTURE_RE.search(tex)
    if match:
        tex = match.group(0)
    if r"\begin{tikzpicture}" not in tex:
        return _build_simple_tikz()
    if _needs_tikz_rebuild(tex):
        return _build_simple_tikz(_extract_tikz_labels(tex))
    tex = _sanitize_tikz_labels(tex)
    tex = re.sub(r">=\s*stealth['\"]*", ">=Stealth", tex, flags=re.IGNORECASE)
    tex = tex.replace(r"\sffamily", "")
    tex = re.sub(r"\[agent[^\]]*\]", lambda _m: f"[{_TIKZ_NODE_STYLE}]", tex)
    tex = tex.replace("[arrow]", "[->, thick]")
    tex = re.sub(r"\bright of=", "right=of ", tex)
    tex = re.sub(r"\\footnotesize\b", r"\\small", tex)
    tex = re.sub(
        r"\\begin\{tikzpicture\}\[[^\]]*\]",
        lambda _m: (
            "\\begin{tikzpicture}[node distance=2.2cm and 1.8cm, "
            f"every node/.style={{{_TIKZ_NODE_STYLE}}}, >=Stealth]"
        ),
        tex,
        count=1,
    )
    tex = re.sub(
        r"\\draw\s*\(([^)]+)\)\s*--\s*\(([^)]+)\)",
        r"\\draw[->, thick] (\1) -- (\2)",
        tex,
    )
    return _sanitize_tikz_labels(tex.strip()) + "\n"


def normalize_body(tex: str) -> str:
    tex = tex.replace(r"\chapter{", r"\section{")
    tex = tex.replace("\u2192", r"$\rightarrow$")
    # LLM literal \n only — do not match the "\n" prefix of \node, \newcommand, etc.
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
    tex = fix_tabular_columns(tex)
    tex = TIKZPICTURE_RE.sub(
        lambda m: _sanitize_tikz_picture_block(m.group(0)),
        tex,
    )
    return tex.strip() + "\n"


def finalize_latex_outputs(latex_dir: Path) -> None:
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
        if _match_label(label, "references.bib", ".bib", "bibtex"):
            path = latex_dir / "references.bib"
            path.write_text(body + "\n", encoding="utf-8")
            if path not in written:
                written.append(path)
        elif _match_label(label, "body.tex", "body", "latex") or (
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


def clear_latex_outputs(latex_dir: Path) -> None:
    for name in ("body.tex", "references.bib", "tikz_diagram.tex"):
        path = latex_dir / name
        if path.is_file():
            path.unlink()
