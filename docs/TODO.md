# TODO

Action items for Assignment 03 and professional submission standards (Dr. Segal, *Software Submission Guidelines* v3).  
Rationale and agent roles → [PLAN.md](PLAN.md) · Requirements → [PRD.md](PRD.md)

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

## Phase 6 — Professional documentation (`docs/`) ✓

Per submission guidelines §2: PRD → PLAN → TODO before/alongside code; all under `docs/`.

- [x] Create `docs/` directory
- [x] `docs/PRD.md` — product requirements (goals, user stories, acceptance criteria, constraints)
- [x] `docs/PLAN.md` — architecture & planning (migrate from root `plan.md`; C4/UML diagrams, ADRs)
- [x] `docs/TODO.md` — task tracking (canonical copy in `docs/`)
- [x] Per-mechanism PRDs:
  - [x] `docs/PRD_crew_pipeline.md` — 6-agent CrewAI orchestration
  - [x] `docs/PRD_latex_normalize.md` — LaTeX post-processing & compile hardening
- [x] `docs/PROMPTS.md` — prompt engineering log (agents, skills, iterative fixes)
- [x] README: license & credits, link to `docs/`

**Gate:** `docs/` contains PRD, PLAN, TODO, and at least two mechanism PRDs ✓

---

## Phase 7 — Code structure (150-line rule, SDK, gatekeeper) ✓

Per guidelines §3–§5, §14: modular packages, max 150 lines per `.py` file, SDK entry point, API gatekeeper.

- [x] Split `src/artifacts.py` → `src/artifacts/` (`tikz.py`, `body.py`, `io.py`, …)
- [x] Trim `src/crew_full.py` / `crew_poc.py` — thin CLIs → `src/sdk/sdk.py`
- [x] `src/sdk/sdk.py` — `run_full`, `run_poc`, `recompile_latex`
- [x] `src/shared/gatekeeper.py` — LLM creation via `ApiGatekeeper`
- [x] `src/shared/config.py` — load from `config/setup.json` + `.env`
- [x] `src/shared/version.py` — `__version__ = "1.00"`
- [x] `src/__init__.py` exports version; `src/config.py` backward-compat shim
- [x] `config/setup.json` + `config/rate_limits.json`
- [x] Docstrings on new public modules
- [ ] `ruff check` clean — deferred to Phase 8

**Gate:** every `src/**/*.py` ≤ 150 lines ✓; SDK entry for crew/recompile ✓

---

## Phase 8 — Tooling & tests (uv, Ruff, TDD, 85% coverage)

Per guidelines §6–§8: `uv` (not pip/venv), Ruff zero errors, tests with ≥85% coverage.

- [ ] Migrate `requirements.txt` → `pyproject.toml` + `uv.lock` (`uv sync`)
- [ ] `[tool.ruff]` in `pyproject.toml` — zero errors (`uv run ruff check`)
- [ ] `[tool.coverage]` — `fail_under = 85`, `source = ["src"]`
- [ ] `tests/unit/` — mirror `src/` structure
  - [ ] `test_artifacts_tikz.py` — TikZ normalize/rebuild (startstop, `\node`, etc.)
  - [ ] `test_artifacts_body.py` — body normalize, tabular fix, inline TikZ
  - [ ] `test_config.py` — env loading, no secrets in code
  - [ ] `test_gatekeeper.py` — rate limits, queue/mock (when gatekeeper exists)
- [ ] `tests/integration/` — `test_crew_full_dry.py` or compile-only path (mock LLM)
- [ ] `tests/conftest.py` — shared fixtures
- [ ] Update README commands → `uv run python -m src.crew_full --validate`

**Gate:** `uv run pytest tests/ --cov` ≥ 85%; `uv run ruff check` passes ✓

---

## Phase 9 — Research & cost analysis

Per guidelines §9, §11: experiments, results notebook, visualizations, token cost table.

- [ ] Token/cost table from `output/logs/*.json` (model, input/output tokens, est. cost)
- [ ] Compare 2–3 runs (topics or models) — sensitivity / repeatability notes
- [ ] `notebooks/results_analysis.ipynb` (or `docs/results.md`) — charts + short write-up
- [ ] Screenshots: cover PDF, ToC, BiDi page, bibliography links (for submission packet)

**Gate:** cost table + at least one comparison chart or table in `docs/` or `notebooks/` ✓

---

## Guidelines quick reference

| Rule | Target | Phase |
|------|--------|-------|
| `docs/PRD.md`, `PLAN.md`, `TODO.md` | Mandatory | 6 |
| Max 150 lines per `.py` | Auto-check in CI or script | 7 |
| SDK + API gatekeeper | All external API via gatekeeper | 7 |
| `uv` + `pyproject.toml` | No `pip install` in docs | 8 |
| Ruff | 0 errors | 8 |
| Test coverage | ≥ 85% | 8 |
| Prompt log | `docs/PROMPTS.md` | 6 |
| Token cost analysis | Table + optimization notes | 9 |

_Not every guidelines item is mandatory for a grade; more criteria met = higher quality score (guidelines §19)._

---

## Done

- **Phase 0** — `python -m src.smoke_test` passed (2026-06-12). Use project `.venv`, not system Python.
- **Phase 1** — `python -m src.crew_poc` passed; draft at `output/markdown/draft.md` (2026-06-12).
- **Phase 2** — stub `output/final.pdf` compiles (LuaLaTeX + biber, all rubric element types) (2026-06-12).
- **Phase 3** — `python -m src.crew_full` passed; 6 agents → `article.md`, `body.tex`, `references.bib`, figures, `output/final.pdf` (2026-06-12).
- **Phase 4** — `scripts/validate_outputs.py` passed; `output/final.pdf` 13 pp., all rubric elements present (2026-06-12). Set `COVER_AUTHOR` in `.env` before submit.
- **Phase 5** — second `crew_full` run; per-agent logs + hardened LaTeX normalize; README + validate pass (2026-06-12).
- **Phase 6** — `docs/` with PRD, PLAN, TODO, mechanism PRDs, PROMPTS; README docs + license (2026-06-13).
- **Phase 7** — split `artifacts/` package, SDK + gatekeeper + `config/`; all `src/**/*.py` ≤ 150 lines; recompile + validate pass (2026-06-13).
