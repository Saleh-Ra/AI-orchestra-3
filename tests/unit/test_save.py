"""save_full_crew_artifacts persistence tests."""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from src.pipeline import save as save_mod


class _Out:
    def __init__(self, raw: str) -> None:
        self.raw = raw


def _six_outputs() -> list[_Out]:
    return [
        _Out("research"),
        _Out("plan"),
        _Out("write"),
        _Out("# edited article"),
        _Out(
            "```tikz_diagram.tex\n"
            r"\begin{tikzpicture}\node (a) {A};\end{tikzpicture}" + "\n"
            "```\n"
            "```python\nimport matplotlib.pyplot as plt\n```"
        ),
        _Out(
            "```body.tex\n\\section{Intro}\n```\n"
            "```references.bib\n@article{a, title={T}}\n```"
        ),
    ]


def test_save_full_crew_artifacts(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(save_mod, "ROOT", tmp_path)
    monkeypatch.setattr(save_mod, "MARKDOWN_OUT", tmp_path / "markdown" / "article.md")
    monkeypatch.setattr(save_mod, "LATEX_DIR", tmp_path / "latex")
    monkeypatch.setattr(save_mod, "FIGURES_DIR", tmp_path / "figures")

    result = SimpleNamespace(tasks_output=_six_outputs())
    save_mod.save_full_crew_artifacts(result)

    assert (tmp_path / "markdown" / "article.md").is_file()
    assert (tmp_path / "latex" / "body.tex").is_file()
    assert (tmp_path / "latex" / "references.bib").is_file()
    assert (tmp_path / "output" / "debug" / "task_0.txt").is_file()


def test_save_requires_six_outputs(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(save_mod, "ROOT", tmp_path)
    result = SimpleNamespace(tasks_output=[_Out("x")] * 3)
    with pytest.raises(RuntimeError, match="Expected 6"):
        save_mod.save_full_crew_artifacts(result)
