"""Generate docs/results.md and cost chart from output/logs."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.analysis.logs import load_run_logs, summarize_runs  # noqa: E402
from src.analysis.report import write_results_report  # noqa: E402


def main() -> int:
    runs = load_run_logs()
    if not runs:
        print("No run logs in output/logs/ — run crew_full first.", file=sys.stderr)
        return 1
    rows = summarize_runs(runs)
    out = write_results_report(rows)
    print(f"Wrote {out} ({len(rows)} runs)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
