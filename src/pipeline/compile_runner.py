"""Run compile scripts and validate LaTeX template."""

from __future__ import annotations

import subprocess
import sys

from src.pipeline.paths import ROOT, TEMPLATE_MAIN


def assert_template_unchanged() -> None:
    text = TEMPLATE_MAIN.read_text(encoding="utf-8")
    if "\\begin{document}" not in text or "\\documentclass" not in text:
        raise RuntimeError("templates/main.tex looks corrupted")
    if "body.tex" not in text and r"\input{body.tex}" not in text:
        raise RuntimeError("templates/main.tex must input body.tex only")


def run_project_script(rel: str) -> None:
    path = ROOT / rel
    if rel.endswith(".ps1"):
        subprocess.run(
            ["powershell", "-ExecutionPolicy", "Bypass", "-File", str(path)],
            check=True,
            cwd=ROOT,
        )
    else:
        subprocess.run([sys.executable, str(path)], check=True, cwd=ROOT)
