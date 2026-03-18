"""
evolve.py — The evolution loop.

Generate → screenshot → score → keep or discard → mutate → repeat.

Run this and walk away. Check /history in the morning.
"""

import csv
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from generate import generate_interface, load_spec, save_generation
from screenshot import screenshot_sync
from score import score_generation, save_score

# ---------------------------------------------------------------------------
# Config — tweak these
# ---------------------------------------------------------------------------
GENERATIONS = int(os.getenv("AUTOINTERFACE_GENERATIONS", "500"))
KEEP_TOP_N = 3              # survivors per generation
SCORE_THRESHOLD = 15        # minimum score to survive
HISTORY_DIR = Path("history")

# ---------------------------------------------------------------------------
# State management
# ---------------------------------------------------------------------------

def load_state() -> dict:
    """Load evolution state from disk (supports resume)."""
    state_path = HISTORY_DIR / "state.json"
    if state_path.exists():
        return json.loads(state_path.read_text())
    return {
        "current_gen": 0,
        "best_score": 0,
        "best_gen": None,
        "survivors": [],
    }


def save_state(state: dict) -> None:
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    (HISTORY_DIR / "state.json").write_text(json.dumps(state, indent=2))


def append_csv(gen_num: int, score: int, parent: int | None, critique: str) -> None:
    csv_path = HISTORY_DIR / "evolution.csv"
    write_header = not csv_path.exists()
    with open(csv_path, "a", newline="") as f:
        writer = csv.writer(f)
        if write_header:
            writer.writerow(["gen", "score", "parent", "timestamp", "critique_preview"])
        writer.writerow([
            gen_num,
            score,
            parent or "",
            datetime.now(timezone.utc).isoformat(),
            critique[:120] if critique else "",
        ])


def update_best(state: dict, gen_num: int, score: int) -> None:
    if score > state["best_score"]:
        state["best_score"] = score
        state["best_gen"] = gen_num
        (HISTORY_DIR / "best.json").write_text(json.dumps({
            "gen": gen_num,
            "score": score,
            "path": f"gen_{gen_num:03d}",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }, indent=2))


# ---------------------------------------------------------------------------
# Parent selection
# ---------------------------------------------------------------------------

def pick_parent(state: dict) -> tuple[str | None, str | None, int | None, str | None]:
    """
    Pick the best survivor as parent.
    Returns: (critique, suggestion, parent_score, previous_html)
    """
    if not state["survivors"]:
        return None, None, None, None

    best = max(state["survivors"], key=lambda s: s["score"])
    gen_dir = HISTORY_DIR / f"gen_{best['gen']:03d}"

    # load critique
    critique = None
    suggestion = None
    score_path = gen_dir / "score.json"
    if score_path.exists():
        score_data = json.loads(score_path.read_text())
        critique = score_data.get("critique", "")
        suggestion = score_data.get("suggestion", "")

    # load HTML
    previous_html = None
    html_path = gen_dir / "app.html"
    if html_path.exists():
        previous_html = html_path.read_text()

    return critique, suggestion, best["score"], previous_html


# ---------------------------------------------------------------------------
# Summary generation
# ---------------------------------------------------------------------------

def generate_summary(state: dict) -> None:
    csv_path = HISTORY_DIR / "evolution.csv"
    if not csv_path.exists():
        return

    rows = []
    with open(csv_path) as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        return

    scores = [int(r["score"]) for r in rows]
    avg = sum(scores) / len(scores)
    best = max(scores)
    worst = min(scores)

    early = scores[:10]
    late = scores[-10:]
    early_avg = sum(early) / len(early) if early else 0
    late_avg = sum(late) / len(late) if late else 0

    summary = f"""# Evolution Summary

**Total generations:** {len(rows)}
**Best score:** {best}/100 (gen {state.get('best_gen', '?')})
**Worst score:** {worst}/100
**Average score:** {avg:.1f}/100

## Trajectory

- First 10 generations avg: {early_avg:.1f}
- Last 10 generations avg: {late_avg:.1f}
- Improvement: {late_avg - early_avg:+.1f} points

## Best generation

Open `gen_{state.get('best_gen', 0):03d}/app.html` in your browser to see the highest-scoring interface.

## Score distribution

| Range | Count |
|-------|-------|
| 80-100 | {sum(1 for s in scores if s >= 80)} |
| 60-79 | {sum(1 for s in scores if 60 <= s < 80)} |
| 40-59 | {sum(1 for s in scores if 40 <= s < 60)} |
| 20-39 | {sum(1 for s in scores if 20 <= s < 40)} |
| 0-19 | {sum(1 for s in scores if s < 20)} |

---

*Generated by autointerface at {datetime.now(timezone.utc).isoformat()}*
"""
    (HISTORY_DIR / "summary.md").write_text(summary)


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def run():
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    state = load_state()
    spec = load_spec()
    start_gen = state["current_gen"] + 1

    print("=" * 60)
    print("autointerface — autonomous interface evolution")
    print("=" * 60)
    print(f"spec: {len(spec)} chars")
    print(f"starting from generation {start_gen}")
    print(f"target: {GENERATIONS} generations")
    if state["best_gen"]:
        print(f"current best: {state['best_score']}/100 (gen {state['best_gen']})")
    print("=" * 60)
    print()

    for gen_num in range(start_gen, GENERATIONS + 1):
        cycle_start = time.time()

        print(f"--- generation {gen_num}/{GENERATIONS} ---")

        # select parent
        critique, suggestion, parent_score, previous_html = pick_parent(state)
        parent_gen = None

        if previous_html:
            parent_gen = max(state["survivors"], key=lambda s: s["score"])["gen"]
            print(f"  parent: gen {parent_gen} (score {parent_score})")
        else:
            print("  no parent (fresh generation)")

        # --- GENERATE ---
        print("  generating interface...")
        try:
            html = generate_interface(
                spec,
                critique=critique,
                suggestion=suggestion,
                score=parent_score,
                previous_html=previous_html,
            )
        except Exception as e:
            print(f"  ERROR in generation: {e}")
            continue

        gen_dir = save_generation(gen_num, html, HISTORY_DIR)
        size_kb = len(html.encode("utf-8")) / 1024
        print(f"  generated app.html ({size_kb:.1f} KB)")

        # --- SCREENSHOT ---
        print("  taking screenshots...")
        try:
            screenshots = screenshot_sync(gen_dir / "app.html", gen_dir)
        except Exception as e:
            print(f"  ERROR in screenshots: {e}")
            # score without screenshots (text-only, lower quality scoring)
            screenshots = []

        # --- SCORE ---
        print("  scoring...")
        try:
            score_data = score_generation(spec, gen_dir, html_content=html)
            save_score(gen_dir, score_data)
        except Exception as e:
            print(f"  ERROR in scoring: {e}")
            score_data = {"score": 0, "critique": f"Scoring failed: {e}", "suggestion": ""}
            save_score(gen_dir, score_data)

        score = score_data.get("score", 0)
        critique_text = score_data.get("critique", "")

        # --- METADATA ---
        meta = {
            "gen": gen_num,
            "parent": parent_gen,
            "score": score,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "html_size_kb": round(size_kb, 1),
            "screenshots": len(screenshots),
        }
        (gen_dir / "meta.json").write_text(json.dumps(meta, indent=2))

        # --- SELECTION ---
        append_csv(gen_num, score, parent_gen, critique_text)

        if score >= SCORE_THRESHOLD:
            state["survivors"].append({"gen": gen_num, "score": score})
            state["survivors"] = sorted(
                state["survivors"], key=lambda s: s["score"], reverse=True
            )[:KEEP_TOP_N]

        update_best(state, gen_num, score)
        state["current_gen"] = gen_num
        save_state(state)

        # --- REPORT ---
        elapsed = time.time() - cycle_start
        print(f"  score: {score}/100")
        if score_data.get("suggestion"):
            print(f"  next: {score_data['suggestion'][:100]}")
        print(f"  best so far: {state['best_score']}/100 (gen {state['best_gen']})")
        print(f"  cycle: {elapsed:.1f}s")
        print()

    # final
    generate_summary(state)
    print("=" * 60)
    print("evolution complete.")
    print(f"best: gen {state['best_gen']} — score {state['best_score']}/100")
    print(f"open history/gen_{state['best_gen']:03d}/app.html in your browser")
    print(f"see history/summary.md for the full report")
    print("=" * 60)


if __name__ == "__main__":
    run()
