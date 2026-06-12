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


def normalize_tikz(tex: str) -> str:
    match = TIKZPICTURE_RE.search(tex)
    if match:
        tex = match.group(0)
    tex = tex.replace(r"\sffamily", "")
    tex = tex.replace("node distance=4cm and 3cm", "node distance=2.2cm and 1.8cm")
    tex = tex.replace("minimum width=3.5cm", "minimum width=2.4cm")
    tex = re.sub(
        r"\\node(\[[^\]]*\])?\s*(\([^)]+\))?\s*\{([^}]+)\}",
        lambda m: (
            f"\\node{m.group(1) or ''}{m.group(2) or ''}"
            f"{{{_wrap_textenglish(m.group(3))}}}"
        ),
        tex,
    )
    return tex.strip() + "\n"


def normalize_body(tex: str) -> str:
    tex = tex.replace(r"\chapter{", r"\section{")
    tex = tex.replace("\u2192", r"$\rightarrow$")
    tex = INCLUDEGRAPHICS_RE.sub(
        lambda m: m.group(0)
        if m.group(2) == "plot.pdf"
        else f"{m.group(1)}sample.png{m.group(3)}",
        tex,
    )
    if r"\textenglish" not in tex:
        bidi = (
            r"\section{דוגמה ל-BiDi: עברית ואנגלית בפסקה אחת}"
            "\n\nבפרק זה מודגמת ערבוב נכון של עברית ואנגלית: מערכת "
            r"\textenglish{CrewAI} משלבת סוכני \textenglish{AI} עם "
            r"\textenglish{Large Language Models (LLM)} בתהליך "
            r"\textenglish{multi-agent orchestration}. מונחים טכניים כמו "
            r"\textenglish{context handoff} ו-\textenglish{sequential process} "
            "מופיעים בתוך משפט בעברית תוך שמירה על כיווניות "
            r"\textenglish{RTL/LTR}.\n\n"
        )
        insert_at = tex.find(r"\section{")
        if insert_at != -1:
            end = tex.find(r"\section{", insert_at + 1)
            if end == -1:
                end = len(tex)
            tex = tex[:end] + "\n" + bidi + tex[end:]
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
