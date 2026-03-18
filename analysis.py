"""
analysis.py — Plot evolution progress.

Reads history/evolution.csv and generates a progress chart.
Run after evolve.py (or mid-run for a progress check).

Usage: uv run analysis.py
"""

import csv
import sys
from pathlib import Path

CSV_PATH = Path("history/evolution.csv")
OUTPUT_PATH = Path("history_preview.png")


def load_scores() -> list[dict]:
    if not CSV_PATH.exists():
        print("ERROR: history/evolution.csv not found. Run evolve.py first.")
        sys.exit(1)
    rows = []
    with open(CSV_PATH) as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append({"gen": int(row["gen"]), "score": int(row["score"])})
    return rows


def plot(rows: list[dict]) -> None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib not installed. Run: uv add matplotlib")
        text_summary(rows)
        return

    gens = [r["gen"] for r in rows]
    scores = [r["score"] for r in rows]

    # rolling average
    window = min(10, len(scores))
    rolling = []
    for i in range(len(scores)):
        start = max(0, i - window + 1)
        rolling.append(sum(scores[start:i+1]) / (i - start + 1))

    # best so far
    best = []
    current_best = 0
    for s in scores:
        current_best = max(current_best, s)
        best.append(current_best)

    fig, ax = plt.subplots(1, 1, figsize=(14, 6))

    ax.scatter(gens, scores, s=10, alpha=0.25, color="#8B7355", label="individual", zorder=2)
    ax.plot(gens, rolling, color="#2D2016", linewidth=2, label=f"rolling avg ({window})", zorder=3)
    ax.plot(gens, best, color="#C4592A", linewidth=1.5, linestyle="--", label="best so far", zorder=3)

    ax.set_xlabel("generation", fontsize=12)
    ax.set_ylabel("design score (0-100)", fontsize=12)
    ax.set_title("autointerface — evolution progress", fontsize=14, fontweight="bold")
    ax.legend(loc="lower right", fontsize=10)
    ax.set_ylim(0, 105)
    ax.grid(True, alpha=0.15)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    fig.patch.set_facecolor("#FAFAF7")
    ax.set_facecolor("#FAFAF7")

    fig.tight_layout()
    fig.savefig(OUTPUT_PATH, dpi=150, bbox_inches="tight")
    print(f"saved chart to {OUTPUT_PATH}")


def text_summary(rows: list[dict]) -> None:
    scores = [r["score"] for r in rows]
    print(f"generations: {len(rows)}")
    print(f"best: {max(scores)}")
    print(f"worst: {min(scores)}")
    print(f"avg: {sum(scores)/len(scores):.1f}")
    bars = "▁▂▃▄▅▆▇█"
    bucket_size = max(1, len(scores) // 40)
    spark = ""
    for i in range(0, len(scores), bucket_size):
        chunk = scores[i:i+bucket_size]
        avg = sum(chunk) / len(chunk)
        spark += bars[int(avg / 100 * (len(bars) - 1))]
    print(f"trajectory: {spark}")


if __name__ == "__main__":
    rows = load_scores()
    print(f"loaded {len(rows)} generations")
    plot(rows)
