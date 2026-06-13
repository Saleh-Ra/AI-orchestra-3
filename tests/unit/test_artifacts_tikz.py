"""TikZ normalization regression tests."""

from __future__ import annotations

from src.artifacts.tikz import normalize_tikz


def test_empty_input_builds_default_diagram() -> None:
    out = normalize_tikz("")
    assert r"\begin{tikzpicture}" in out
    assert r"\node (n0)" in out
    assert r"\textenglish{Research}" in out


def test_startstop_style_rebuilds() -> None:
    raw = r"""
\begin{tikzpicture}
\node[startstop] (a) {Input Processing};
\node[startstop, right=of a] (b) {Output};
\draw (a) -- (b);
\end{tikzpicture}
"""
    out = normalize_tikz(raw)
    assert "startstop" not in out
    assert r"\textenglish{Input Processing}" in out
    assert r"right=of n0" in out


def test_stealth_typo_sanitized() -> None:
    raw = r"""
\begin{tikzpicture}[>=stealth']
\node (a) {A};
\node[right=of a] (b) {B};
\draw (a) -- (b);
\end{tikzpicture}
"""
    out = normalize_tikz(raw)
    assert "stealth'" not in out
    assert ">=Stealth" in out


def test_unpositioned_nodes_rebuild() -> None:
    raw = r"""
\begin{tikzpicture}
\node (a) {One};
\node (b) {Two};
\node (c) {Three};
\end{tikzpicture}
"""
    out = normalize_tikz(raw)
    assert r"right=of n0" in out


def test_valid_positioned_tikz_sanitized_not_rebuilt() -> None:
    raw = r"""
\begin{tikzpicture}[node distance=2cm, >=stealth']
\node (a) {Alpha};
\node[right=of a] (b) {Beta};
\draw (a) -- (b);
\end{tikzpicture}
"""
    out = normalize_tikz(raw)
    assert r"\textenglish{Alpha}" in out
    assert r"\draw[->, thick]" in out
    assert "startstop" not in out
