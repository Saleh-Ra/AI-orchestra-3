# AI Orchestra — Assignment 03 Development Plan

Automated article/book generation with **CrewAI** and **LaTeX/PDF** output.  
Course: Mass Production of AI Agents (L06) — Dr. Yoram Segal.

---

## Table of Contents

1. [Assignment Requirements](#1-assignment-requirements)
2. [Design Principle — Why CrewAI](#2-design-principle--why-crewai)
3. [System Architecture and Design Decisions](#3-system-architecture-and-design-decisions)
4. [Detailed Development Plan](#4-detailed-development-plan)
5. [Agent Pipeline](#5-agent-pipeline)
6. [Project Structure](#6-project-structure)
7. [Open Decisions](#7-open-decisions)

> **Task tracking:** [TODO.md](TODO.md)

---

## 1. Assignment Requirements

**Goal:** Build a **CrewAI agent team** that writes an article/book on a chosen topic and produces a polished PDF via LaTeX.

### Content requirements

| Requirement | Details |
|-------------|---------|
| Length | ~15 pages including cover (Hebrew may need more) |
| Cover sheet | Topic, author name, date, course and semester |
| Structure | Table of contents, chapters, headers/footers |
| Visuals | ≥1 image, ≥1 **Python-generated** graph, ≥1 table, ≥1 math formula |
| BiDi | ≥1 chapter with correct Hebrew ↔ English RTL/LTR switching |
| Bibliography | At end, with working linked citations |

### Technical requirements

- Extend the CrewAI pipeline with a **LaTeX file generator** agent.
- Prototype content in **Markdown** first; convert to `.tex` when stable.
- **Compiler:** MiKTeX + **LuaLaTeX** (XeLaTeX acceptable) for Hebrew support.
- **Bibliography:** `.bib` + `biber`/BibTeX — expect **~4 compile passes** for refs/citations.
- **Graphics:** matplotlib plot required (§13.1); TikZ block diagrams recommended (§13.2 workflow).
- **Math:** Proper LaTeX math environments — not plain-text formulas.

### Grading focus

Evaluation is **technical**, not content quality:

- Links and citations resolve (click in-text cite → bibliography entry)
- BiDi renders correctly
- Tables do not overflow the page
- Formulas render properly (fancy LaTeX, not plain text)
- PDF compiles without errors

---

## 2. Design Principle — Why CrewAI

The assignment is not “one prompt writes a book.” It is a **multi-agent organization**: each specialist does **one job**, hands results to the next via CrewAI **`context`**, orchestrated by a **`Crew`** with **`Process.sequential`**.

| Rule | Meaning |
|------|---------|
| **One agent → one Task** | Each agent has exactly one task in the submission crew |
| **One deliverable per task** | `expected_output` defines a single artifact type |
| **No role overlap** | Researcher does not write prose; Writer does not produce `.tex` |
| **Context = handoff** | Prior task output is the next agent’s input — no manual copy-paste |
| **Tools + Skills** | Tools = *what* (search, files); Skills = *how* (style, LaTeX, rubric) |

**Submission crew:** 6 agents, 6 tasks (see [Agent Pipeline](#5-agent-pipeline)).  
Phase 1 uses 2 agents only as a **learning POC** — not the final deliverable.

**Infrastructure (templates, compile scripts)** supports the agents; it does **not** replace their work. Agents produce content and LaTeX body; scripts compile PDF and execute agent-authored figure code.

---

## 3. System Architecture and Design Decisions

### Hybrid pipeline (reliability + multi-agent)

| Layer | Responsibility |
|-------|----------------|
| **CrewAI agents (6)** | Each owns one stage: research → plan → write → edit → figures → LaTeX |
| **Fixed LaTeX template** | Preamble, fonts, BiDi, headers/footers, `\tableofcontents` shell |
| **Post-crew scripts** | Run Visualizer’s matplotlib script, compile with LuaLaTeX + biber |
| **LaTeX agent** | Body `.tex`, tables, equations, `\cite{}`, embed figure paths — not free-form preamble |

### Locked defaults

| Decision | Default |
|----------|---------|
| Process type | `Process.sequential` |
| Intermediate format | Markdown → `.tex` fragments |
| Primary language | Hebrew body + one dedicated BiDi chapter |
| Agent count | **6** (full submission crew) |
| Skills wiring | Per-agent `skills=[...]` (appendix pattern) |
| Search tool | Optional `SerperDevTool` on Researcher only |

### Agent → Task → output (submission crew)

| Agent | Task | `context` from | Produces |
|-------|------|----------------|----------|
| Researcher | `research_task` | `kickoff` inputs (`topic`) | Research JSON |
| Planner | `plan_task` | `research_task` | Outline JSON |
| Writer | `write_task` | `research_task`, `plan_task` | Markdown draft |
| Editor | `edit_task` | `write_task`, `plan_task` | Polished Markdown + rubric check |
| Visualizer | `visuals_task` | `edit_task`, `plan_task` | Plot `.py`, TikZ snippet, image spec |
| LaTeX | `latex_task` | `edit_task`, `plan_task`, `research_task`, `visuals_task` | `body.tex`, `references.bib` |

### Structured output shapes

```
Research   → JSON: { facts[], sources[{title, author, year, url}], figure_ideas[], formula_ideas[], table_ideas[] }
Planner    → JSON: { title, chapters[{ title, sections[], needs_figure, needs_formula, needs_table, bidi_chapter? }] }
Writer     → Markdown: full article body (~15 pages of content)
Editor     → Markdown: polished draft + rubric checklist (all assignment items addressed)
Visualizer → JSON + files: { plot_script.py, tikz_diagram.tex, image_path_or_include_spec }
LaTeX      → files: body.tex (or chapters/*.tex), references.bib, embed directives for visuals
```

### Skills (CrewAI)

Each skill is a folder with **`SKILL.md`** — YAML frontmatter (`name`, `description`) + Markdown instructions. Wire via per-agent `skills=["./skills/<name>"]`.

| Skill folder | Agent(s) | Purpose |
|--------------|----------|---------|
| `skills/academic-writing/` | Writer, Editor | Style, chapter flow, tone |
| `skills/assignment-rubric/` | Editor | Verify rubric before LaTeX pass |
| `skills/figures-and-diagrams/` | Visualizer | matplotlib plots, TikZ block diagrams, image inclusion |
| `skills/latex-bidi/` | LaTeX | Hebrew/English, polyglossia/babel, fancy math |

### Pipeline diagram

```mermaid
flowchart LR
  R[Researcher] --> P[Planner]
  P --> W[Writer]
  W --> E[Editor]
  E --> V[Visualizer]
  V --> L[LaTeX Agent]
  L --> OUT[body.tex + .bib]
  OUT --> RUN[run figures + compile]
  RUN --> PDF[final.pdf]
```

### Environment prerequisites

- Python 3.12 + `.venv` (CrewAI 1.14.7 installed)
- **MiKTeX** with LuaLaTeX and **biber**
- LLM API key (or local model via CrewAI LLM config)

---

## 4. Detailed Development Plan

### Phase 0 — Foundation (~½ day)

- Project layout, `requirements.txt`, `.env`, smoke test
- Confirm MiKTeX + `lualatex` + `biber` on PATH

**Deliverable:** `python -m src.smoke_test` succeeds.

---

### Phase 1 — Minimal crew POC (~1 day)

**Purpose:** Learn CrewAI — not the submission artifact.

- 2 agents, 2 tasks: Researcher → Writer
- `context=[research_task]`, `Process.sequential`, `crew.kickoff(inputs={"topic": ...})`
- Save to `output/markdown/draft.md`

**Deliverable:** short Markdown article; context handoff verified.

---

### Phase 2 — LaTeX spine (~1–2 days)

**Purpose:** Validate PDF toolchain **before** full AI content. **No agents in this phase** — infrastructure only.

- `templates/main.tex` — LuaLaTeX, Hebrew RTL, cover, headers/footers, ToC
- Stub with: formula, table, matplotlib plot, **TikZ diagram**, static image, citation, BiDi paragraph
- `scripts/run_figures.py` — execute plot script → `output/figures/plot.pdf`
- `scripts/compile.ps1` — LuaLaTeX + biber (~4 passes)

**Deliverable:** stub `output/final.pdf` compiles with every rubric element type.

---

### Phase 3 — Full submission crew (~1–2 days)

- Implement all **6 agents**, each with **exactly one Task**
- Skills with proper `SKILL.md` YAML frontmatter
- Optional `SerperDevTool` on Researcher
- `src/crew_full.py`: `kickoff` → agent chain → run figures → compile

**Deliverable:** one full pipeline run: topic → PDF.

---

### Phase 4 — Assignment rubric pass (~1 day)

Manual verification per [TODO.md](TODO.md) Phase 4 (technical grading items).

**Deliverable:** submission-ready `output/final.pdf`.

---

### Phase 5 — Hardening

- Second full pipeline run (repeatability)
- Per-agent failure logging; prompt fixes
- README: env, run commands, compile steps
- Optional: `scripts/validate_outputs.py` — bib keys match `\cite{}`, PDF exists, compile exit 0

---

## 5. Agent Pipeline

### Research Agent

- **Task:** `research_task`
- **Tools:** `SerperDevTool` (optional)
- **Does:** Gather facts and sources; suggest figures, tables, formulas
- **Does not:** Write chapters or LaTeX

### Planner Agent

- **Task:** `plan_task`
- **Does:** Title, chapter structure, flags for visuals/BiDi/formulas
- **Does not:** Write prose or format LaTeX

### Writer Agent

- **Task:** `write_task`
- **Skill:** `academic-writing`
- **Does:** Expand outline into ~15 pages of Markdown
- **Does not:** Research from scratch or edit for rubric

### Editor Agent

- **Task:** `edit_task`
- **Context:** `write_task`, `plan_task` — checks draft against planned structure
- **Skill:** `assignment-rubric`, `academic-writing`
- **Does:** Polish prose; confirm assignment requirements and outline coverage
- **Does not:** Produce LaTeX or generate plots

### Visualizer Agent

- **Task:** `visuals_task`
- **Skill:** `figures-and-diagrams`
- **Does:** Author matplotlib Python script, TikZ block diagram, static image include spec
- **Does not:** Write article body or full LaTeX document

### LaTeX Agent

- **Task:** `latex_task`
- **Skill:** `latex-bidi`
- **Does:** Convert polished Markdown to `body.tex`, build `references.bib`, embed visuals into template shell
- **Does not:** Invent preamble; does not run compile (script does)

---

## 6. Project Structure

```
AI-orchestra-3/
├── .env / .env.example
├── requirements.txt
├── plan.md
├── TODO.md
├── README.md
├── src/
│   ├── smoke_test.py
│   ├── crew_poc.py          # Phase 1 — 2 agents
│   ├── crew_full.py         # Phase 3 — 6 agents
│   ├── agents/              # one module per agent
│   ├── tasks/               # one module per task
│   └── models/              # optional Pydantic schemas
├── skills/
│   ├── academic-writing/SKILL.md
│   ├── assignment-rubric/SKILL.md
│   ├── figures-and-diagrams/SKILL.md
│   └── latex-bidi/SKILL.md
├── templates/
│   └── main.tex
├── scripts/
│   ├── run_figures.py       # executes Visualizer’s plot script
│   ├── compile.ps1
│   └── validate_outputs.py  # optional post-run checks
├── assets/                  # static images (e.g. cover logo)
└── output/
    ├── markdown/
    ├── latex/
    ├── figures/
    └── final.pdf
```

---

## 7. Open Decisions

Fill before Phase 3:

| Item | Value |
|------|-------|
| **Topic** | _TBD_ |
| **LLM provider / model** | _TBD_ |
| **Author name (cover)** | _TBD_ |
| **Course name** | _TBD_ |
| **Semester** | _TBD_ |
| **Cover date** | _TBD_ |
| **Web search (Serper)?** | _TBD_ |

---

*Last updated: pre-implementation — full multi-agent crew locked.*
