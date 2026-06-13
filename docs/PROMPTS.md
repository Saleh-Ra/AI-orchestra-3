# Prompt Engineering Log

**Project:** AI Orchestra  
**Purpose:** Document agent instructions, skills, and iterative fixes (per submission guidelines §8.3).

---

## 1. Architecture principle

> One agent → one task → one deliverable. Context handoffs replace copy-paste.

Prompts live in `src/tasks/*.py` (`description`, `expected_output`) and `skills/*/SKILL.md`.

---

## 2. Agent tasks (summary)

| Task | Key prompt constraints |
|------|------------------------|
| `research_task` | Facts, sources, figure/formula/table ideas; JSON-shaped output |
| `plan_task` | ~15-page chapter structure; flags for BiDi, visuals |
| `write_task` | Hebrew article from research + plan; English terms inline |
| `edit_task` | Rubric check against plan; polish only |
| `visuals_task` | **Exactly three** fenced blocks: `plot_script.py`, `tikz_diagram.tex`, `image_spec.txt` |
| `latex_task` | `body.tex` + `references.bib` only; no preamble; fenced blocks |

**CrewAI template fix:** Removed bare `{key}` braces from `expected_output` strings (CrewAI interprets `{}` as template variables).

---

## 3. Skills (system-level instructions)

| Skill | Agents | Critical rules added during hardening |
|-------|--------|--------------------------------------|
| `academic-writing` | Writer, Editor | ~15 pages; Hebrew + English terms |
| `assignment-rubric` | Editor | Checklist before LaTeX pass |
| `figures-and-diagrams` | Visualizer | No `startstop`/`process`/`decision`; no `\\` in labels; `right=of` |
| `latex-bidi` | LaTeX | No `\bibliography` in body; always `\node` full command; `\textenglish{}` |

---

## 4. Iteration log (compile failures → prompt/code fixes)

| Date | Issue | Change |
|------|-------|--------|
| 2026-06-12 | LaTeX agent output not saved | `clear_latex_outputs`, better fence parsing, `task_5.txt` debug |
| 2026-06-12 | `\chapter` in article class | `normalize_body`: `\chapter` → `\section` |
| 2026-06-12 | TikZ `\\[4pt]` in labels | Strip line breaks in `\textenglish{}` |
| 2026-06-13 | `\node` → `ode` (regex) | Safe `\n` replacement; `ode` repair line |
| 2026-06-13 | `No shape named '0'` | Same as above |
| 2026-06-13 | Invalid `startstop` TikZ | `normalize_tikz` rebuild from labels |
| 2026-06-13 | Tabular column mismatch | `fix_tabular_columns` |
| 2026-06-13 | Broken `\foreach \x/\y` | Regex rewrite to `\point` form |

---

## 5. Recommended prompt patterns

- **Structured fences:** LaTeX/Visualizer must use markdown code fences with explicit first-line labels.
- **Negative constraints:** List forbidden LaTeX (`\documentclass`, `\bibliography`, tutorial TikZ styles).
- **Length hints:** “~15 pages” in Writer/Planner — soft target; Editor should not aggressively trim.
- **Topic injection:** `{topic}` in task descriptions via CrewAI `kickoff(inputs={"topic": ...})`.

---

## 6. Models & tools

| Setting | Default |
|---------|---------|
| `OPENAI_MODEL` | `gpt-4.1-mini` |
| Web search | `USE_SERPER=false` (optional Serper on Researcher) |

---

## 7. Future logging

- Phase 9: token counts per run from `output/logs/*.json`
- Phase 8: snapshot tests for normalize functions with fixtures from `output/debug/`

---

*Last updated: 2026-06-13*
