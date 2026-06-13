# Product Requirements Document — AI Orchestra

**Product:** AI Orchestra (Assignment 03)  
**Course:** Mass Production of AI Agents (L06) — Dr. Yoram Segal  
**Author:** Saleh (set `COVER_AUTHOR` in `.env`)  
**Version:** 1.00  
**Status:** Assignment pipeline complete; professional hardening in progress (Phases 7–9)

---

## 1. Overview

### 1.1 Problem

Students must demonstrate a **multi-agent CrewAI team** that produces a **technical Hebrew/English article** and compiles it to a **polished PDF** via LaTeX — not a single monolithic prompt.

### 1.2 Solution

A sequential six-agent pipeline: Research → Plan → Write → Edit → Visualize → LaTeX, followed by deterministic post-processing (figure run + LuaLaTeX + biber) and optional rubric validation.

### 1.3 Target users

| User | Need |
|------|------|
| Student (author) | Run one command → `output/final.pdf` for submission |
| Instructor / grader | Verify technical rubric (BiDi, citations, plot, TikZ, compile) |
| Developer (future) | Extend agents, skills, or normalization without breaking PDF |

---

## 2. Goals & success metrics

| Goal | KPI / acceptance |
|------|------------------|
| Multi-agent handoff | 6 agents, 6 tasks; each runs exactly once per `crew_full` run |
| PDF compiles | `scripts/compile.ps1` exits 0; no fatal LaTeX errors in `main.log` |
| Rubric elements | Cover, ToC, table, equation, `plot.pdf`, TikZ, static image, BiDi, bibliography |
| Citations resolve | Every `\cite{key}` has matching `references.bib` entry; biber completes |
| Repeatability | Second run with `--validate` passes after normalization hardening |
| Length (soft) | ~15 pages incl. cover; 9–14 acceptable if all technical checks pass |

Grading is **technical**, not literary quality.

---

## 3. User stories

1. **As a student**, I set `OPENAI_API_KEY` and `COVER_AUTHOR`, run `crew_full --validate`, and get `output/final.pdf`.
2. **As a student**, I pass `--topic "..."` to override the default article subject without editing code.
3. **As a student**, if compile fails after agents finish, I re-run normalize + compile without paying for another crew run.
4. **As a grader**, I open the PDF in a real viewer and click citations to reach the bibliography.
5. **As a developer**, I read agent skills under `skills/` and mechanism PRDs under `docs/PRD_*.md`.

---

## 4. Functional requirements

### 4.1 Crew pipeline (`crew_full`)

- `Process.sequential` with explicit `context` per task (see [PRD_crew_pipeline.md](PRD_crew_pipeline.md)).
- Persist: `article.md`, `body.tex`, `references.bib`, `tikz_diagram.tex`, `plot_script.py`, run logs.
- Flags: `--topic`, `--skip-compile`, `--validate`.

### 4.2 LaTeX & PDF

- Fixed shell: `templates/main.tex` (preamble, cover, ToC, headers/footers).
- Agent fills `body.tex` + `references.bib` only.
- Post-process: `finalize_latex_outputs()` → `run_figures.py` → `compile.ps1` (see [PRD_latex_normalize.md](PRD_latex_normalize.md)).

### 4.3 Learning POC (`crew_poc`)

- Two agents (Researcher, Writer) → `output/markdown/draft.md`; no PDF.

### 4.4 Validation

- `scripts/validate_outputs.py` checks artifacts and rubric elements; page count warning if &lt; 13.

---

## 5. Non-functional requirements

| Area | Requirement |
|------|-------------|
| Language | Hebrew RTL body; English technical terms via `\textenglish{}` |
| Compiler | LuaLaTeX + biber (MiKTeX on Windows) |
| LLM | OpenAI via CrewAI; model from `OPENAI_MODEL` |
| Secrets | `.env` only; `.env.example` committed |
| Logs | `output/logs/latest.json`, `output/debug/task_*.txt` |
| Portability | Windows PowerShell primary; paths via `pathlib` |

---

## 6. Constraints & assumptions

- **In scope:** Assignment 03 PDF rubric, CrewAI 6-agent crew, Hebrew BiDi article.
- **Out of scope (v1):** GUI, REST API, real-time collaboration, guaranteed 15-page length every run.
- **Assumptions:** MiKTeX installed; user has OpenAI API access; LLM output may need normalization before compile.
- **Dependencies:** CrewAI, OpenAI API, optional Serper for Researcher.

---

## 7. Out of scope / future (Phases 7–9)

- SDK layer + API gatekeeper ([PLAN.md](PLAN.md) Phase 7)
- `uv`, Ruff, pytest ≥85% coverage (Phase 8)
- Token cost notebook and parameter experiments (Phase 9)

---

## 8. Related documents

| Document | Purpose |
|----------|---------|
| [PLAN.md](PLAN.md) | Architecture and development phases |
| [TODO.md](TODO.md) | Task checklist and gates |
| [PRD_crew_pipeline.md](PRD_crew_pipeline.md) | Crew orchestration mechanism |
| [PRD_latex_normalize.md](PRD_latex_normalize.md) | LaTeX post-processing mechanism |
| [PROMPTS.md](PROMPTS.md) | Prompt and skill engineering log |

---

*Last updated: 2026-06-13*
