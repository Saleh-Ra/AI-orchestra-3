---
name: figures-and-diagrams
description: matplotlib plot scripts and TikZ block diagrams for LaTeX documents
metadata:
  author: ai-orchestra
  version: "1.0"
---

## Figure deliverables

Output exactly three fenced code blocks:

1. `plot_script.py` — runnable matplotlib script saving to `plot.pdf` in the same directory.
2. `tikz_diagram.tex` — a complete `tikzpicture` (no `\begin{document}`).
3. `image_spec.txt` — one line: path `assets/sample.png` or note to reuse existing asset.

Plot script must use only matplotlib + stdlib. TikZ should be a simple RTL-friendly flow (3–4 nodes).

TikZ rules for Hebrew documents: output only `\begin{tikzpicture}...\end{tikzpicture}`; no
`\documentclass`, `\sffamily`, `\tikzstyle`, or tutorial flowchart keys like `startstop`,
`process`, `decision`, or `[agent]`; use plain `\node` with `right=of` (not `right of=`);
**one short line per node label** — never `\\` or `\\[4pt]` inside labels; wrap English in
`\textenglish{...}`; use `\draw[->, thick]` for arrows. Keep diagrams to a simple 3-node
horizontal flow — complex automata or polytope drawings belong in body prose, not TikZ.
