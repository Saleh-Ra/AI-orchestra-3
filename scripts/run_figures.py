"""Run figure-generation scripts before LaTeX compile."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIGURES = ROOT / "output" / "figures"
ASSETS = ROOT / "assets"
PLOT_SCRIPT = FIGURES / "plot_script.py"


def ensure_asset_image() -> None:
    """Create a small static PNG in assets/ if missing."""
    target = ASSETS / "sample.png"
    if target.exists():
        return
    ASSETS.mkdir(parents=True, exist_ok=True)
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches

    fig, ax = plt.subplots(figsize=(3, 3))
    ax.add_patch(mpatches.Circle((0.5, 0.5), 0.35, color="#0d9488", alpha=0.85))
    ax.text(0.5, 0.5, "AI", ha="center", va="center", fontsize=28, color="white", weight="bold")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    fig.savefig(target, dpi=120, bbox_inches="tight", transparent=True)
    plt.close(fig)
    print(f"Wrote {target}")


def main() -> int:
    if not PLOT_SCRIPT.is_file():
        print(f"ERROR: missing {PLOT_SCRIPT}", file=sys.stderr)
        return 1
    subprocess.run([sys.executable, str(PLOT_SCRIPT)], check=True)
    ensure_asset_image()
    return 0


if __name__ == "__main__":
    sys.exit(main())
