"""Shared regex patterns for LaTeX artifact processing."""

from __future__ import annotations

import re

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
