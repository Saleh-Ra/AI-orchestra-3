# TODO

Action items for Assignment 03. Rationale and agent roles → [plan.md](plan.md).

**North star:** 6 agents, 6 tasks, sequential `context` handoffs — each agent does only its job.

When a phase **gate** passes, its items are checked off and the gate is moved to **Done** with the date.

---

## Blockers — before Phase 3

- [ ] Article topic
- [x] LLM provider: OpenAI (`gpt-4.1-mini` default)
- [x] `OPENAI_API_KEY` in local `.env`
- [ ] Cover metadata: author, course, semester, date
- [ ] Serper for researcher: yes / no

---

## Phase 0 — Foundation ✓

_All items complete — see **Done**._

---

## Phase 1 — CrewAI POC ✓

_All items complete — see **Done**._

---

## Phase 2 — LaTeX spine (infrastructure only — no agents)

- [ ] `templates/main.tex` — LuaLaTeX, Hebrew RTL, cover, headers/footers, ToC
- [ ] Stub `body.tex` + `references.bib`
- [ ] Stub includes: formula, table, **TikZ diagram**, static image (`assets/`), BiDi paragraph, `\cite{}`
- [ ] `scripts/run_figures.py` + stub `plot_script.py` → `output/figures/plot.pdf`
- [ ] `scripts/compile.ps1` — LuaLaTeX + biber (~4 passes)
- [ ] Compile stub → `output/final.pdf`

**Gate:** every rubric *element type* appears in stub PDF ✓

---

## Phase 3 — Submission crew (6 agents, 6 tasks)

One row = one agent = one task. Wire `context` as in plan.

| Agent | Task file | `context` |
|-------|-----------|-----------|
| Researcher | `research_task` | kickoff `topic` |
| Planner | `plan_task` | `research_task` |
| Writer | `write_task` | `research_task`, `plan_task` |
| Editor | `edit_task` | `write_task`, `plan_task` |
| Visualizer | `visuals_task` | `edit_task`, `plan_task` |
| LaTeX | `latex_task` | `edit_task`, `plan_task`, `research_task`, `visuals_task` |

- [ ] All 6 agents in `src/agents/`
- [ ] All 6 tasks in `src/tasks/` with structured `expected_output`
- [ ] `src/crew_full.py` — full crew, `verbose=True`
- [ ] Skills (each `SKILL.md` with YAML `name` + `description`):
  - [ ] `skills/academic-writing/`
  - [ ] `skills/assignment-rubric/`
  - [ ] `skills/figures-and-diagrams/`
  - [ ] `skills/latex-bidi/`
- [ ] Per-agent `skills=[...]` wiring
- [ ] Optional: `SerperDevTool` on researcher only
- [ ] Visualizer output → `output/figures/plot_script.py` + `tikz_diagram.tex`
- [ ] LaTeX agent → `output/latex/body.tex` + `references.bib` (uses template, no free preamble)
- [ ] Verify agent output does not overwrite `templates/main.tex` preamble — only fills body slot
- [ ] Post-crew: `run_figures.py` → `compile.ps1` → `output/final.pdf`

**Gate:** full `crew_full.py` run completes; each agent executed exactly one task ✓

---

## Phase 4 — Submission rubric (manual PDF check)

- [ ] ~15 pages incl. cover
- [ ] Cover: topic, author, date, course, semester
- [ ] Table of contents populated
- [ ] Headers / footers on body pages
- [ ] Static image present
- [ ] Python-generated graph present (from Visualizer’s script)
- [ ] TikZ block diagram present (§13.2 recommended — not a separate §13.1 minimum)
- [ ] Table present — no page overflow
- [ ] Fancy math formula (LaTeX env, not plain text)
- [ ] BiDi chapter renders correctly
- [ ] Bibliography at end
- [ ] Click in-text citation → jumps to bibliography entry (after full compile cycle)
- [ ] No broken refs / unfixable compile errors

**Gate:** `output/final.pdf` ready to submit ✓

---

## Phase 5 — Hardening

- [ ] Second full pipeline run
- [ ] Log per-agent failures; tune prompts
- [ ] `scripts/validate_outputs.py` — PDF exists, bib keys ⊆ `\cite{}`, compile exit 0
- [ ] README: prerequisites, env vars, `crew_poc` vs `crew_full`, compile steps

---

## Done

- **Phase 0** — `python -m src.smoke_test` passed (2026-06-12). Use project `.venv`, not system Python.
- **Phase 1** — `python -m src.crew_poc` passed; draft at `output/markdown/draft.md` (2026-06-12).
