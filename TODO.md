# TODO

Action items for Assignment 03. Rationale and agent roles → [plan.md](plan.md).

**North star:** 6 agents, 6 tasks, sequential `context` handoffs — each agent does only its job.

When a phase **gate** passes, its items are checked off and the gate is moved to **Done** with the date.

---

## Blockers — before Phase 3 ✓

- [x] Article topic → `ARTICLE_TOPIC` in `.env`
- [x] LLM: OpenAI (`gpt-4.1-mini`)
- [x] `OPENAI_API_KEY` in `.env`
- [x] Cover metadata → `COVER_*` in `.env` (edit `COVER_AUTHOR` to your name)
- [x] Serper → `USE_SERPER=false` (set `true` + `SERPER_API_KEY` to enable)

---

## Phase 0 — Foundation ✓

_All items complete — see **Done**._

---

## Phase 1 — CrewAI POC ✓

_All items complete — see **Done**._

---

## Phase 2 — LaTeX spine ✓

_All items complete — see **Done**._

---

## Phase 3 — Submission crew (6 agents, 6 tasks) ✓

_All items complete — see **Done**._

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
- **Phase 2** — stub `output/final.pdf` compiles (LuaLaTeX + biber, all rubric element types) (2026-06-12).
- **Phase 3** — `python -m src.crew_full` passed; 6 agents → `article.md`, `body.tex`, `references.bib`, figures, `output/final.pdf` (2026-06-12).
