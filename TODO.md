# TODO

Action items for Assignment 03. Rationale and agent roles → [plan.md](plan.md).

**North star:** 6 agents, 6 tasks, sequential `context` handoffs — each agent does only its job.

When a phase **gate** passes, check off its items with `[x]` and add a one-line summary to **Done** with the date.

---

## Blockers — before Phase 3 ✓

- [x] Article topic → `ARTICLE_TOPIC` in `.env`
- [x] LLM: OpenAI (`gpt-4.1-mini`)
- [x] `OPENAI_API_KEY` in `.env`
- [x] Cover metadata → `COVER_*` in `.env` (edit `COVER_AUTHOR` to your name)
- [x] Serper → `USE_SERPER=false` (set `true` + `SERPER_API_KEY` to enable)

---

## Phase 0 — Foundation ✓

- [x] Scaffold dirs per `plan.md` (incl. `assets/`)
- [x] `requirements.txt` + install into `.venv`
- [x] `.env.example` + local `.env`
- [x] `.gitignore` — `.venv/`, `.env`, `__pycache__/`, `output/`
- [x] `README.md` (run instructions)
- [x] **MiKTeX** installed; `lualatex` + `biber` on PATH
- [x] `src/smoke_test.py` — CrewAI import + one LLM call
- [x] Smoke test run passes

**Gate:** `python -m src.smoke_test` ✓

---

## Phase 1 — CrewAI POC (2 agents, learning only) ✓

- [x] `src/agents/researcher.py`, `src/agents/writer.py`
- [x] `src/tasks/research_task.py`, `src/tasks/write_task.py` — `context=[research_task]` on write
- [x] `src/crew_poc.py` — `Process.sequential`, `kickoff(inputs={"topic": ...})`
- [x] Save → `output/markdown/draft.md`

**Gate:** two agents collaborate; context handoff works ✓  
_Not submission — proves CrewAI wiring._

---

## Phase 2 — LaTeX spine (infrastructure only — no agents) ✓

- [x] `templates/main.tex` — LuaLaTeX, Hebrew RTL, cover, headers/footers, ToC
- [x] Stub `body.tex` + `references.bib`
- [x] Stub includes: formula, table, **TikZ diagram**, static image (`assets/`), BiDi paragraph, `\cite{}`
- [x] `scripts/run_figures.py` + stub `plot_script.py` → `output/figures/plot.pdf`
- [x] `scripts/compile.ps1` — LuaLaTeX + biber (~4 passes)
- [x] Compile stub → `output/final.pdf`

**Gate:** every rubric *element type* appears in stub PDF ✓

---

## Phase 3 — Submission crew (6 agents, 6 tasks) ✓

One row = one agent = one task. Wire `context` as in plan.

| Agent | Task file | `context` |
|-------|-----------|-----------|
| Researcher | `research_task` | kickoff `topic` |
| Planner | `plan_task` | `research_task` |
| Writer | `write_task` | `research_task`, `plan_task` |
| Editor | `edit_task` | `write_task`, `plan_task` |
| Visualizer | `visuals_task` | `edit_task`, `plan_task` |
| LaTeX | `latex_task` | `edit_task`, `plan_task`, `research_task`, `visuals_task` |

- [x] All 6 agents in `src/agents/`
- [x] All 6 tasks in `src/tasks/` with structured `expected_output`
- [x] `src/crew_full.py` — full crew, `verbose=True`
- [x] Skills (each `SKILL.md` with YAML `name` + `description`):
  - [x] `skills/academic-writing/`
  - [x] `skills/assignment-rubric/`
  - [x] `skills/figures-and-diagrams/`
  - [x] `skills/latex-bidi/`
- [x] Per-agent `skills=[...]` wiring
- [x] Optional: `SerperDevTool` on researcher only
- [x] Visualizer output → `output/figures/plot_script.py` + `tikz_diagram.tex`
- [x] LaTeX agent → `output/latex/body.tex` + `references.bib` (uses template, no free preamble)
- [x] Verify agent output does not overwrite `templates/main.tex` preamble — only fills body slot
- [x] Post-crew: `run_figures.py` → `compile.ps1` → `output/final.pdf`

**Gate:** full `crew_full.py` run completes; each agent executed exactly one task ✓

---

## Phase 4 — Submission rubric (manual PDF check) ✓

- [x] ~15 pages incl. cover
- [x] Cover: topic, author, date, course, semester
- [x] Table of contents populated
- [x] Headers / footers on body pages
- [x] Static image present
- [x] Python-generated graph present (from Visualizer’s script)
- [x] TikZ block diagram present (§13.2 recommended — not a separate §13.1 minimum)
- [x] Table present — no page overflow
- [x] Fancy math formula (LaTeX env, not plain text)
- [x] BiDi chapter renders correctly
- [x] Bibliography at end
- [x] Click in-text citation → jumps to bibliography entry (after full compile cycle)
- [x] No broken refs / unfixable compile errors

**Gate:** `output/final.pdf` ready to submit ✓

---

## Phase 5 — Hardening ✓

- [x] Second full pipeline run — `crew_full --validate` (repeatability; hardened `artifacts.py` post-process)
- [x] Log per-agent failures; tune prompts — `output/logs/latest.json`; TikZ/BiDi/rubric fallbacks in `finalize_latex_outputs`
- [x] `scripts/validate_outputs.py` — PDF exists, bib keys ⊆ `\cite{}`, compile exit 0
- [x] README: prerequisites, env vars, `crew_poc` vs `crew_full`, compile steps

**Gate:** second run + validation pass ✓

---

---

## Done

- **Phase 0** — `python -m src.smoke_test` passed (2026-06-12). Use project `.venv`, not system Python.
- **Phase 1** — `python -m src.crew_poc` passed; draft at `output/markdown/draft.md` (2026-06-12).
- **Phase 2** — stub `output/final.pdf` compiles (LuaLaTeX + biber, all rubric element types) (2026-06-12).
- **Phase 3** — `python -m src.crew_full` passed; 6 agents → `article.md`, `body.tex`, `references.bib`, figures, `output/final.pdf` (2026-06-12).
- **Phase 4** — `scripts/validate_outputs.py` passed; `output/final.pdf` 13 pp., all rubric elements present (2026-06-12). Set `COVER_AUTHOR` in `.env` before submit.
- **Phase 5** — second `crew_full` run; per-agent logs + hardened LaTeX normalize; README + validate pass (2026-06-12).
