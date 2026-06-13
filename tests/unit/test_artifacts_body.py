"""body.tex normalization regression tests."""

from __future__ import annotations

from src.artifacts.body import normalize_body
from src.artifacts.tabular import fix_tabular_columns


def test_node_ode_repair_and_literal_backslash_n() -> None:
    tex = r"\section{X}" + "\n" + "ode (0) {0};" + r"\n\textenglish{ok}"
    out = normalize_body(tex)
    lines = out.splitlines()
    assert r"\node (0) {0};" in lines
    assert "ode (0) {0};" not in lines


def test_tabular_column_padding() -> None:
    tex = (
        r"\begin{tabular}{|l|l|}"
        "\n"
        r"A & B & C \\"
        "\n"
        r"\end{tabular}"
    )
    fixed = fix_tabular_columns(tex)
    assert "|l|l|l|" in fixed


def test_rubric_fallbacks_injected() -> None:
    out = normalize_body(r"\section{Only}")
    assert r"\begin{equation}" in out
    assert "sample.png" in out
    assert r"\input{tikz_diagram.tex}" in out
    assert r"\textenglish" in out


def test_bibliography_stripped() -> None:
    tex = r"\section{A}" + "\n" + r"\bibliography{refs}" + "\n" + r"\bibliographystyle{plain}"
    out = normalize_body(tex)
    assert r"\bibliography" not in out
    assert r"\bibliographystyle" not in out


def test_foreach_xy_repair() -> None:
    tex = (
        r"\section{T}"
        "\n"
        r"\foreach \x/\y in {(0,0),(1,1)} {\filldraw[black] \x/\y circle (3pt);}"
    )
    out = normalize_body(tex)
    assert r"\foreach \point in" in out
    assert r"\x/\y" not in out
