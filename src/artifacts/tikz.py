"""TikZ diagram normalization and safe rebuild."""

from __future__ import annotations

import re

from src.artifacts.patterns import TIKZPICTURE_RE
from src.artifacts.textenglish import sanitize_textenglish, wrap_textenglish

TIKZ_NODE_STYLE = (
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
    return len(labels) >= 2 and not positioned


def _build_simple_tikz(labels: list[str] | None = None) -> str:
    names = list(labels or [])
    defaults = ["Research", "Plan", "Write"]
    while len(names) < 3:
        names.append(defaults[len(names)])
    names = names[:5]
    ids = [f"n{i}" for i in range(len(names))]
    lines = [
        "\\begin{tikzpicture}[node distance=2.2cm and 1.8cm, "
        f"every node/.style={{{TIKZ_NODE_STYLE}}}, >=Stealth]",
    ]
    for i, (node_id, label) in enumerate(zip(ids, names)):
        inner = wrap_textenglish(label) if "\\textenglish" not in label else label
        if i == 0:
            lines.append(f"\\node ({node_id}) {{{inner}}};")
        else:
            lines.append(f"\\node[right=of {ids[i - 1]}] ({node_id}) {{{inner}}};")
    for i in range(1, len(ids)):
        lines.append(f"\\draw[->, thick] ({ids[i - 1]}) -- ({ids[i]});")
    lines.append("\\end{tikzpicture}")
    return "\n".join(lines) + "\n"


def normalize_tikz(tex: str) -> str:
    """Return a compile-safe tikzpicture block."""
    match = TIKZPICTURE_RE.search(tex)
    if match:
        tex = match.group(0)
    if r"\begin{tikzpicture}" not in tex:
        return _build_simple_tikz()
    if _needs_tikz_rebuild(tex):
        return _build_simple_tikz(_extract_tikz_labels(tex))
    tex = sanitize_textenglish(tex)
    tex = re.sub(r"\\+\[[^\]]*\]", " ", tex)
    tex = re.sub(r">=\s*stealth['\"]*", ">=Stealth", tex, flags=re.IGNORECASE)
    tex = tex.replace(r"\sffamily", "")
    tex = re.sub(r"\[agent[^\]]*\]", lambda _m: f"[{TIKZ_NODE_STYLE}]", tex)
    tex = tex.replace("[arrow]", "[->, thick]")
    tex = re.sub(r"\bright of=", "right=of ", tex)
    tex = re.sub(r"\\footnotesize\b", r"\\small", tex)
    tex = re.sub(
        r"\\begin\{tikzpicture\}\[[^\]]*\]",
        lambda _m: (
            "\\begin{tikzpicture}[node distance=2.2cm and 1.8cm, "
            f"every node/.style={{{TIKZ_NODE_STYLE}}}, >=Stealth]"
        ),
        tex,
        count=1,
    )
    tex = re.sub(
        r"\\draw\s*\(([^)]+)\)\s*--\s*\(([^)]+)\)",
        r"\\draw[->, thick] (\1) -- (\2)",
        tex,
    )
    return sanitize_textenglish(tex.strip()) + "\n"
