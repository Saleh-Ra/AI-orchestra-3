"""BiDi textenglish sanitization helpers."""

from __future__ import annotations

import re


def wrap_textenglish(label: str) -> str:
    if "\\textenglish" in label or not re.search(r"[A-Za-z]", label):
        return label
    return rf"\textenglish{{{label}}}"


def sanitize_textenglish(tex: str) -> str:
    def fix(match: re.Match[str]) -> str:
        inner = match.group(1)
        inner = re.sub(r"\\+\[[^\]]*\]", " ", inner)
        inner = re.sub(r"\\+n", " ", inner)
        inner = re.sub(r"\\+", " ", inner)
        inner = re.sub(r"\s+", " ", inner).strip()
        return rf"\textenglish{{{inner}}}"

    return re.sub(r"\\textenglish\{([^}]*)\}", fix, tex)
