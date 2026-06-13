# PRD — CrewAI Pipeline Mechanism

**Mechanism:** Six-agent sequential crew (`src/crew_full.py`)  
**Version:** 1.00

---

## 1. Description

Orchestrates six CrewAI agents in a fixed order. Each agent consumes prior task outputs via `context` and produces one artifact type. After the crew completes, Python scripts normalize LaTeX, run matplotlib, and compile PDF — agents do not invoke the compiler.

---

## 2. Inputs / outputs

| Stage | Input | Output |
|-------|--------|--------|
| Kickoff | `topic` (CLI or `ARTICLE_TOPIC`) | — |
| Researcher | `topic` | Research brief (JSON-like text) |
| Planner | research | Chapter outline |
| Writer | research, plan | Markdown draft |
| Editor | write, plan | Polished Markdown |
| Visualizer | edit, plan | `plot_script.py`, `tikz_diagram.tex`, `image_spec.txt` |
| LaTeX | edit, plan, research, visuals | `body.tex`, `references.bib` |
| Post-crew | agent files | `output/final.pdf` |

---

## 3. Context wiring (must not change without updating tests)

| Task | `context` |
|------|-----------|
| `research_task` | — |
| `plan_task` | `research_task` |
| `write_task` | `research_task`, `plan_task` |
| `edit_task` | `write_task`, `plan_task` |
| `visuals_task` | `edit_task`, `plan_task` |
| `latex_task` | `edit_task`, `plan_task`, `research_task`, `visuals_task` |

---

## 4. Requirements

- Exactly **one task per agent** in submission crew.
- `Process.sequential`, `verbose=True`.
- Skills wired per agent (`skills/academic-writing`, `assignment-rubric`, `figures-and-diagrams`, `latex-bidi`).
- Optional `SerperDevTool` on Researcher when `USE_SERPER=true`.
- Raw outputs saved to `output/debug/task_{0..5}.txt`.
- Run summary: `output/logs/latest.json` (success, per-agent char counts, error).

---

## 5. Failure modes & handling

| Failure | Detection | Mitigation |
|---------|-----------|------------|
| Missing `body.tex` | File check after task 5 | Inspect `task_5.txt`; re-run crew |
| Compile error | `compile.ps1` non-zero | `finalize_latex_outputs` + recompile; see LaTeX PRD |
| LLM timeout / API error | Crew exception | Logged in `latest.json`; fix key/network |
| Template overwrite | Assert `main.tex` unchanged | LaTeX agent must not emit `\documentclass` |

---

## 6. Success criteria

- [x] `python -m src.crew_full` completes 6 tasks
- [x] `output/markdown/article.md` and `output/latex/body.tex` non-empty
- [x] With `--validate`, `scripts/validate_outputs.py` exits 0

---

## 7. Alternatives considered

| Alternative | Why not chosen |
|-------------|----------------|
| Single mega-prompt | Violates assignment (multi-agent organization) |
| Parallel agents | Breaks narrative dependency (write needs plan) |
| Agent runs compile | Non-deterministic; MiKTeX belongs in scripts |

---

*See [PLAN.md](PLAN.md) §5 for agent role descriptions.*
