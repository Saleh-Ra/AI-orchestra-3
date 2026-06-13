# PRD — LaTeX Normalization & Compile Hardening

**Mechanism:** `src/artifacts.py` → `finalize_latex_outputs()`  
**Compile:** `scripts/run_figures.py`, `scripts/compile.ps1`  
**Version:** 1.00

---

## 1. Description

LLM-generated LaTeX and TikZ is often almost valid but breaks LuaLaTeX. A **deterministic post-processor** runs after agents finish (and before every compile) to repair common patterns without re-invoking the LLM.

---

## 2. Inputs / outputs

| Step | Input | Output |
|------|--------|--------|
| `normalize_tikz` | `tikz_diagram.tex` (and inline `\begin{tikzpicture}` in body) | Safe 3–5 node flow or sanitized TikZ |
| `normalize_body` | `body.tex` | Rubric fallbacks, stripped duplicate `\bibliography`, fixed tables |
| `fix_tabular_columns` | `tabular` blocks | Column spec padded to match `&` count |
| `run_figures.py` | `plot_script.py` | `output/figures/plot.pdf` |
| `compile.ps1` | `templates/main.tex` + latex dir | `output/final.pdf` |

---

## 3. Normalization rules (critical)

### 3.1 Must not corrupt valid commands

- Literal `\n` cleanup must **not** match `\node`, `\newcommand`, etc.  
  Use `(?<![a-zA-Z])\\n(?![a-zA-Z])` only.
- Repair corrupted `ode` → `\node` at line start.

### 3.2 TikZ

- Rebuild diagram when: `startstop`/`process`/`decision` styles, invalid `stealth'`, unpositioned multi-node graphs, broken `\foreach \x/\y`.
- Normalize: `>=Stealth`, `right=of`, `below left of=` → `below left=of`.
- `templates/main.tex` loads `arrows.meta`, `positioning`, `automata`.

### 3.3 Body

- `\chapter` → `\section` (article class).
- Strip agent-emitted `\bibliographystyle` / `\bibliography` (handled in template).
- Inject rubric fallbacks if missing: BiDi sample, equation, `sample.png`, `\input{tikz_diagram.tex}`.

### 3.4 Tables

- Auto-expand `\begin{tabular}{...}` when header/data rows have more columns than spec.

---

## 4. Known failure history (regression targets for Phase 8 tests)

| Symptom | Root cause | Fix location |
|---------|------------|--------------|
| `No shape named '0'` | `\node` → `ode` via bad `\n` regex | `normalize_body` |
| `Unknown key '/tikz/startstop'` | Flowchart styles without definitions | `normalize_tikz` rebuild |
| `Extra alignment tab` | 6 columns, 5-col tabular spec | `fix_tabular_columns` |
| `Giving up on this path` | `\filldraw \x/\y` in foreach | foreach rewrite |
| Undefined citations pass 1 | Normal until biber runs | full compile cycle |

---

## 5. Requirements

- `finalize_latex_outputs()` called from `crew_full` after artifact write.
- Recompile-only path must call same function before `compile.ps1`.
- Do not modify `templates/main.tex` preamble from agent output.
- Compile: LuaLaTeX ×2 + biber + LuaLaTeX ×2 (see `compile.ps1`).

---

## 6. Success criteria

- [x] Multiple topics compile after normalize (CrewAI default, algorithms, AI industry)
- [x] `scripts/validate_outputs.py` passes on successful compile
- [ ] Unit tests lock normalize behavior (Phase 8)

---

## 7. Alternatives considered

| Alternative | Why not chosen |
|-------------|----------------|
| Ask LaTeX agent to “fix until compile works” | Expensive, non-deterministic |
| Disable all inline TikZ in body | Would drop assignment richness |
| XeLaTeX only | Assignment allows LuaLaTeX; polyglossia setup is Lua-focused |

---

*Skill reference: `skills/latex-bidi/SKILL.md`, `skills/figures-and-diagrams/SKILL.md`*
