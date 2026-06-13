"""Tabular column spec repair."""

from __future__ import annotations

import re

from src.artifacts.patterns import TABULAR_RE


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
    """Pad tabular column spec when data rows have more & than header spec."""

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
