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
| Python 3.12+ | Managed with [uv](https://docs.astral.sh/uv/) (`pyproject.toml` + `uv.lock`) |
| MiKTeX | `lualatex` and `biber` on PATH |
| OpenAI API key | [platform.openai.com](https://platform.openai.com/api-keys) |
| Optional: Serper | `pip install crewai-tools` + `SERPER_API_KEY` if `USE_SERPER=true` |

## Setup

Install [uv](https://docs.astral.sh/uv/getting-started/installation/), then from the project root:

```powershell
uv sync --extra dev
copy .env.example .env
# Edit .env — at minimum OPENAI_API_KEY and COVER_AUTHOR
```

This creates `.venv` and installs locked dependencies from `uv.lock`.

**Windows:** If `Activate.ps1` is blocked, use `uv run` (recommended):

```powershell
uv run python -m src.smoke_test
```

Legacy pip workflow (still works): `python -m venv .venv` + `pip install -r requirements.txt`.

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
uv run python -m src.crew_full --validate
```

Custom topic:

```powershell
uv run python -m src.crew_full --topic "Your topic here" --validate
```

Equivalent with explicit venv Python: `.\.venv\Scripts\python.exe -m src.crew_full --validate`

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
uv run python -m src.smoke_test
```

### Two-agent POC (Phase 1)

```powershell
uv run python -m src.crew_poc
uv run python -m src.crew_poc --topic "Your topic"
```

### Full six-agent pipeline (Phase 3+)

```powershell
uv run python -m src.crew_full
uv run python -m src.crew_full --topic "Your topic"
uv run python -m src.crew_full --skip-compile    # agents only, no PDF
uv run python -m src.crew_full --validate        # compile + rubric validation
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
uv run python scripts\validate_outputs.py
```

Checks: PDF exists, cite/bib keys match, table, equation, plot, TikZ, BiDi, bibliography. Page count &lt; 13 prints a warning (target ~15 incl. cover) but is not a hard fail.

### Recompile only (no API cost)

After agents finish, or to retry compile without re-running the crew:

```powershell
uv run python -c "from src.sdk import recompile_latex; recompile_latex()"
uv run python scripts\validate_outputs.py
```

Legacy (equivalent):

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
├── config/              # setup.json, rate_limits.json (versioned)
├── src/
│   ├── sdk/             # run_full, run_poc, recompile_latex
│   ├── shared/          # config, gatekeeper, version
│   ├── pipeline/        # crew build, save, compile helpers
│   ├── artifacts/       # LaTeX normalize (split modules)
│   ├── agents/          # CrewAI agents
│   └── tasks/           # CrewAI tasks
├── templates/main.tex   # LaTeX shell (do not put article body here)
├── scripts/             # compile.ps1, run_figures.py, validate_outputs.py
├── skills/              # CrewAI agent skills (LaTeX, figures, rubric)
├── docs/                # PRD, PLAN, TODO, mechanism PRDs (canonical)
├── assets/sample.png    # static image for rubric
├── output/              # generated markdown, latex, figures, final.pdf
├── plan.md              # → docs/PLAN.md
└── TODO.md              # → docs/TODO.md
```

## Tests & lint (Phase 8)

```powershell
uv run ruff check src tests
uv run pytest tests/ --cov=src
```

Coverage gate: **≥85%** on `src/` (configured in `pyproject.toml`).

## Research & cost (Phase 9)

After `crew_full` runs, analyze token spend and export submission screenshots:

```powershell
uv run python scripts/analyze_runs.py
uv run python scripts/export_pdf_screenshots.py
```

- Report: [docs/results.md](docs/results.md)
- Notebook: [notebooks/results_analysis.ipynb](notebooks/results_analysis.ipynb)
- Screenshots: `docs/screenshots/`

## Documentation

Canonical project docs (per course submission guidelines):

| Document | Description |
|----------|-------------|
| [docs/PRD.md](docs/PRD.md) | Product requirements, user stories, acceptance criteria |
| [docs/PLAN.md](docs/PLAN.md) | Architecture, C4, ADRs, development phases |
| [docs/TODO.md](docs/TODO.md) | Phase checklist and gates |
| [docs/PRD_crew_pipeline.md](docs/PRD_crew_pipeline.md) | Six-agent CrewAI mechanism |
| [docs/PRD_latex_normalize.md](docs/PRD_latex_normalize.md) | LaTeX post-processing mechanism |
| [docs/PROMPTS.md](docs/PROMPTS.md) | Prompt and skill engineering log |
| [docs/results.md](docs/results.md) | Phase 9 — token cost table & run comparison |

Root [plan.md](plan.md) and [TODO.md](TODO.md) point to `docs/`.

## License & credits

- **Course:** Mass Production of AI Agents (L06), University of Haifa — Dr. Yoram Segal  
- **Assignment:** CrewAI multi-agent article generation with LuaLaTeX PDF output  
- **Stack:** [CrewAI](https://www.crewai.com/), OpenAI API, MiKTeX (LuaLaTeX + biber), matplotlib, TikZ  
- **License:** Academic course submission — see instructor for redistribution terms  

## Troubleshooting

- **`ModuleNotFoundError: crewai`** — wrong Python; use `.\.venv\Scripts\python.exe`.
- **PowerShell blocks `Activate.ps1`** — skip activation; use venv `python.exe` directly.
- **CrewAI emoji / charmap warnings on Windows** — harmless console noise.
- **LaTeX compile failed** — see `output/latex/main.log`; try recompile-only commands above.
- **LaTeX agent missing `body.tex`** — inspect `output/debug/task_5.txt`; re-run `crew_full`.
- **Parallel `lualatex` hangs** — run a single `compile.ps1` at a time.
