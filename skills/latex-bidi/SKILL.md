---
name: latex-bidi
description: LuaLaTeX body fragments with Hebrew RTL, English inline, and biblatex citations
metadata:
  author: ai-orchestra
  version: "1.0"
---

## LaTeX rules

1. Output **only** `body.tex` and `references.bib` fenced blocks — never a full document or preamble.
2. Document class is **article** — use `\section` / `\subsection` only (never `\chapter`).
3. Never use `\bibliographystyle` or `\bibliography` — bibliography is in `templates/main.tex`.
4. Use `\textenglish{...}` for English terms and `\cite{key}` for sources.
5. Always write `\node` (full command) — never broken forms like `ode`.
4. Static images: `\includegraphics{sample.png}` only; plot: `\includegraphics{plot.pdf}`.
5. Math: use `\begin{equation}...\end{equation}` — never plain-text formulas.
6. Include `\input{tikz_diagram.tex}` where the diagram belongs.
7. One section must demonstrate Hebrew + English BiDi in the same paragraph.
8. Tables: use `booktabs` (`\toprule`, `\midrule`, `\bottomrule`); keep columns narrow.
9. `references.bib` keys must match every `\cite{}` in body.tex.
