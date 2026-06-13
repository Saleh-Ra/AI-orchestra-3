"""Write docs/results.md and comparison charts from run summaries."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent.parent
DOCS_DIR = ROOT / "docs"
CHARTS_DIR = DOCS_DIR / "charts"


def _pick_comparison_rows(rows: list[dict[str, Any]], limit: int = 4) -> list[dict[str, Any]]:
    """Pick diverse successful runs, then fill with distinct topics."""
    seen: set[str] = set()
    picked: list[dict[str, Any]] = []
    for row in sorted(rows, key=lambda r: r["timestamp"], reverse=True):
        key = row["topic"].strip().lower()
        if key in seen:
            continue
        if not row["success"]:
            continue
        seen.add(key)
        picked.append(row)
        if len(picked) >= limit:
            return picked
    for row in sorted(rows, key=lambda r: r["timestamp"], reverse=True):
        key = row["topic"].strip().lower()
        if key in seen:
            continue
        seen.add(key)
        picked.append(row)
        if len(picked) >= limit:
            break
    return picked


def _write_chart(rows: list[dict[str, Any]], path: Path) -> None:
    labels = [r["topic"][:28] + ("…" if len(r["topic"]) > 28 else "") for r in rows]
    costs = [r["cost_usd"] for r in rows]
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.barh(labels, costs, color="#2563eb")
    ax.set_xlabel("Estimated cost (USD)")
    ax.set_title("Pipeline run cost by topic")
    fig.tight_layout()
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, dpi=150)
    plt.close(fig)


def write_results_report(rows: list[dict[str, Any]], out_md: Path | None = None) -> Path:
    out = out_md or DOCS_DIR / "results.md"
    compare = _pick_comparison_rows(rows)
    chart_path = CHARTS_DIR / "run_cost_comparison.png"
    if compare:
        _write_chart(compare, chart_path)

    total_cost = sum(r["cost_usd"] for r in rows)
    measured = sum(1 for r in rows if not r["estimated"])
    lines = [
        "# Research & cost analysis (Phase 9)",
        "",
        "Auto-generated from `output/logs/run_*.json`. Re-run:",
        "",
        "```powershell",
        "uv run python scripts/analyze_runs.py",
        "```",
        "",
        "## Summary",
        "",
        f"- **Runs analyzed:** {len(rows)}",
        f"- **Runs with measured token usage:** {measured}",
        f"- **Cumulative estimated spend:** ${total_cost:.4f} USD",
        "- **Default model:** `gpt-4.1-mini` (see `config/cost_rates.json`)",
        "",
        "Older logs without `token_usage` use a heuristic from per-agent `output_chars` "
        "(marked *est.* in the table). New runs log real CrewAI `token_usage` after kickoff.",
        "",
        "## Token & cost table",
        "",
        "| Timestamp | Topic | OK | Model | Prompt | Completion | Total | Cost (USD) |",
        "|-----------|-------|----|-------|--------|------------|-------|------------|",
    ]
    for r in rows:
        est = " *est.*" if r["estimated"] else ""
        topic = r["topic"].replace("|", "\\|")
        if len(topic) > 42:
            topic = topic[:39] + "…"
        lines.append(
            f"| {r['timestamp'][:16]} | {topic} | {'✓' if r['success'] else '✗'} | "
            f"{r['model']} | {r['prompt_tokens']:,}{est} | {r['completion_tokens']:,}{est} | "
            f"{r['total_tokens']:,}{est} | ${r['cost_usd']:.4f} |"
        )

    lines.extend(
        [
            "",
            "## Topic comparison",
            "",
            "Selected runs with distinct topics (prefer successful compiles):",
            "",
        ]
    )
    for r in compare:
        lines.append(
            f"- **{r['topic']}** — {r['total_tokens']:,} tokens, "
            f"${r['cost_usd']:.4f}, output {r['output_chars']:,} chars, "
            f"{'compiled OK' if r['success'] else 'agents OK / compile failed'}"
        )

    lines.extend(
        [
            "",
            "### Observations",
            "",
            "- **Repeatability:** Same topic (CrewAI default) produced similar agent output "
            "sizes across runs; compile success improved after LaTeX normalization hardening.",
            "- **Topic sensitivity:** Broader topics (e.g. AI industry) tend to produce longer "
            "agent outputs → higher token use and occasional LaTeX edge cases.",
            "- **Cost control:** Use `recompile_latex()` to retry PDF without new API calls; "
            "use `--skip-compile` during prompt iteration.",
            "",
            "## Visualization",
            "",
        ]
    )
    if compare:
        lines.append("![Run cost comparison](charts/run_cost_comparison.png)")
    else:
        lines.append("_No runs available for chart._")

    lines.extend(
        [
            "",
            "## Submission screenshots",
            "",
            "Exported from `output/final.pdf` into `docs/screenshots/`:",
            "",
            "| File | Page | Content |",
            "|------|------|---------|",
            "| `01_cover.png` | 1 | Cover (topic, author, course) |",
            "| `02_toc.png` | 2 | Table of contents |",
            "| `03_body_bidi.png` | 3+ | Body / BiDi sample |",
            "| `04_bibliography.png` | last | Bibliography & citation links |",
            "",
            "Regenerate:",
            "",
            "```powershell",
            "uv run python scripts/export_pdf_screenshots.py",
            "```",
            "",
        ]
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return out
