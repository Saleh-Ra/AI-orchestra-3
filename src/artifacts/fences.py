"""Fence parsing and named artifact extraction."""

from __future__ import annotations

from pathlib import Path

from src.artifacts.patterns import FENCE_RE


def extract_fenced_blocks(text: str) -> list[tuple[str | None, str]]:
    blocks: list[tuple[str | None, str]] = []
    for match in FENCE_RE.finditer(text):
        label = (match.group(1) or "").strip() or None
        body = match.group(2).strip()
        if body:
            blocks.append((label, body))
    return blocks


def match_label(label: str | None, *needles: str) -> bool:
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
