# AI Orchestra — Assignment 03

**Course:** Mass Production of AI Agents (L06) — Dr. Yoram Segal  
**Goal:** A CrewAI multi-agent team writes an article on a chosen topic and compiles a polished Hebrew/English PDF via LuaLaTeX.

## What it does

Six agents run in sequence (`Process.sequential`). Each agent has one job and passes its output to the next via CrewAI `context`:

| Agent | Output |
|-------|--------|
| Researcher | Research brief (facts, sources, figure ideas) |
| Planner | Chapter outline (~15-page structure) |
| Writer | Full Markdown article |
| Editor | Polished Markdown (rubric check) |
| Visualizer | `plot_script.py`, `tikz_diagram.tex`, image spec |
| LaTeX | `body.tex`, `references.bib` |

Scripts then normalize LaTeX, run matplotlib, and compile with LuaLaTeX + biber → **`output/final.pdf`**.

## Prerequisites

| Requirement | Notes |
|-------------|--------|
| Python 3.12+ | Use the project `.venv` for all commands |
| MiKTeX | `lualatex` and `biber` on PATH |
| OpenAI API key | [platform.openai.com](https://platform.openai.com/api-keys) |
| Optional: Serper | `pip install crewai-tools` + `SERPER_API_KEY` if `USE_SERPER=true` |

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\pip.exe install -r requirements.txt
copy .env.example .env
# Edit .env — at minimum OPENAI_API_KEY and COVER_AUTHOR
```

**Windows:** If `Activate.ps1` is blocked, call the venv Python directly (recommended):

```powershell
.\.venv\Scripts\python.exe -m src.smoke_test
```

System Python will miss `crewai` and other dependencies.

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | Yes | OpenAI API key |
| `OPENAI_MODEL` | No | Default `gpt-4.1-mini` |
| `ARTICLE_TOPIC` | No | Default article subject (overridable with `--topic`) |
| `COVER_AUTHOR` | Yes (submit) | Your name on the cover |
| `COVER_COURSE` | No | Course title (Hebrew default in `.env.example`) |
| `COVER_SEMESTER` | No | Semester string |
| `COVER_DATE` | No | Cover date (`YYYY-MM-DD`) |
| `USE_SERPER` | No | `true` to enable web search on Researcher |
| `SERPER_API_KEY` | If Serper | Required when `USE_SERPER=true` |

## Quick start (submission pipeline)

```powershell
.\.venv\Scripts\python.exe -m src.crew_full --validate
```

Custom topic:

```powershell
.\.venv\Scripts\python.exe -m src.crew_full --topic "Your topic here" --validate
```

This runs all six agents, compiles the PDF, and checks the technical rubric.  
**Open `output/final.pdf` in a browser or PDF viewer** — opening it inside the IDE shows raw PDF bytes, not the rendered document.

Target length is **~15 pages including cover**; shorter PDFs (e.g. 9 pages) still compile and pass technical checks but are below the stated goal.

## `crew_poc` vs `crew_full`

| | `crew_poc` | `crew_full` |
|---|------------|-------------|
| **Purpose** | Learn CrewAI wiring (Phase 1) | Submission pipeline (Phase 3+) |
| **Agents** | 2 — Researcher, Writer | 6 — + Planner, Editor, Visualizer, LaTeX |
| **Output** | `output/markdown/draft.md` | `article.md`, `body.tex`, `references.bib`, `final.pdf` |
| **LaTeX / PDF** | No | Yes — runs figures + compile |

## Commands

### Smoke test (Phase 0)

```powershell
.\.venv\Scripts\python.exe -m src.smoke_test
```

### Two-agent POC (Phase 1)

```powershell
.\.venv\Scripts\python.exe -m src.crew_poc
.\.venv\Scripts\python.exe -m src.crew_poc --topic "Your topic"
```

### Full six-agent pipeline (Phase 3+)

```powershell
.\.venv\Scripts\python.exe -m src.crew_full
.\.venv\Scripts\python.exe -m src.crew_full --topic "Your topic"
.\.venv\Scripts\python.exe -m src.crew_full --skip-compile    # agents only, no PDF
.\.venv\Scripts\python.exe -m src.crew_full --validate        # compile + rubric validation
```

**Outputs:**

- `output/markdown/article.md` — edited article
- `output/latex/body.tex`, `references.bib`, `tikz_diagram.tex`
- `output/figures/plot_script.py`, `plot.pdf`
- `output/final.pdf`
- `output/logs/latest.json` — per-agent run summary
- `output/debug/task_*.txt` — raw agent outputs

### Validate rubric (Phase 4+)

```powershell
.\.venv\Scripts\python.exe scripts\validate_outputs.py
```

Checks: PDF exists, cite/bib keys match, table, equation, plot, TikZ, BiDi, bibliography. Page count &lt; 13 prints a warning (target ~15 incl. cover) but is not a hard fail.

### Recompile only (no API cost)

After agents finish, or to retry compile without re-running the crew:

```powershell
.\.venv\Scripts\python.exe -c "from pathlib import Path; from src.artifacts import finalize_latex_outputs; finalize_latex_outputs(Path('output/latex'))"
.\.venv\Scripts\python.exe scripts\run_figures.py
powershell -ExecutionPolicy Bypass -File scripts\compile.ps1
.\.venv\Scripts\python.exe scripts\validate_outputs.py
```

First MiKTeX run may download packages and take several minutes. Run one compile at a time.

## Assignment deliverables (technical rubric)

The PDF should include:

- Cover sheet (topic, author, date, course, semester)
- Table of contents, headers/footers
- Hebrew body with English technical terms (`\textenglish{...}`) — BiDi chapter
- At least one table, math equation, Python-generated plot, static image, TikZ diagram
- Bibliography with working `\cite{}` → bibliography links
- Clean compile (LuaLaTeX + biber, ~4 passes)

Grading focuses on **technical correctness** (compile, citations, BiDi, layout), not content quality.

## Project layout

```
AI-orchestra-3/
├── src/                 # agents, tasks, crew_poc.py, crew_full.py
├── templates/main.tex   # LaTeX shell (do not put article body here)
├── scripts/             # compile.ps1, run_figures.py, validate_outputs.py
├── skills/              # CrewAI agent skills (LaTeX, figures, rubric)
├── assets/sample.png    # static image for rubric
├── output/              # generated markdown, latex, figures, final.pdf
├── plan.md              # full architecture
└── TODO.md              # phase checklist
```

## Troubleshooting

- **`ModuleNotFoundError: crewai`** — wrong Python; use `.\.venv\Scripts\python.exe`.
- **PowerShell blocks `Activate.ps1`** — skip activation; use venv `python.exe` directly.
- **CrewAI emoji / charmap warnings on Windows** — harmless console noise.
- **LaTeX compile failed** — see `output/latex/main.log`; try recompile-only commands above.
- **LaTeX agent missing `body.tex`** — inspect `output/debug/task_5.txt`; re-run `crew_full`.
- **Parallel `lualatex` hangs** — run a single `compile.ps1` at a time.

## Docs

- [plan.md](plan.md) — architecture, agent roles, design decisions
- [TODO.md](TODO.md) — phase checklist and gates
