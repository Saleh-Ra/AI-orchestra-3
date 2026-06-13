"""LaTeX artifact extraction and normalization (public API)."""

from src.artifacts.body import normalize_body
from src.artifacts.fences import extract_fenced_blocks, write_named_artifacts
from src.artifacts.io import (
    clear_latex_outputs,
    finalize_latex_outputs,
    write_latex_artifacts,
    write_visuals_artifacts,
)
from src.artifacts.tikz import normalize_tikz

__all__ = [
    "clear_latex_outputs",
    "extract_fenced_blocks",
    "finalize_latex_outputs",
    "normalize_body",
    "normalize_tikz",
    "write_latex_artifacts",
    "write_named_artifacts",
    "write_visuals_artifacts",
]
