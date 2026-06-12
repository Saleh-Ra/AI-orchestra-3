# AI Orchestra — Assignment 03

CrewAI multi-agent pipeline that generates an article/book and compiles a PDF via LaTeX.

## Prerequisites

- Python 3.12+
- MiKTeX with `lualatex` and `biber` on PATH
- OpenAI API key

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
# Edit .env and set OPENAI_API_KEY
```

Use the project venv for every command (`Activate.ps1` first, or `.\.venv\Scripts\python.exe`).

## Phase 0 — smoke test

```powershell
.\.venv\Scripts\Activate.ps1
python -m src.smoke_test
```

## Phase 1 — two-agent POC

```powershell
.\.venv\Scripts\Activate.ps1
python -m src.crew_poc
# optional: python -m src.crew_poc --topic "Your topic"
```

Output: `output/markdown/draft.md`

## Phase 2 — LaTeX stub PDF

```powershell
.\.venv\Scripts\python.exe scripts\run_figures.py
powershell -ExecutionPolicy Bypass -File scripts\compile.ps1
```

Output: `output/final.pdf` (first MiKTeX compile may install packages and take several minutes).

## Phase 3 — full crew (6 agents)

Set cover fields in `.env` (see `.env.example`), then:

```powershell
.\.venv\Scripts\Activate.ps1
python -m src.crew_full
# optional: python -m src.crew_full --topic "Your topic" --skip-compile
```

Outputs: `output/markdown/article.md`, `output/latex/body.tex`, `output/final.pdf`

## Docs

- [plan.md](plan.md) — architecture and phases
- [TODO.md](TODO.md) — task checklist
