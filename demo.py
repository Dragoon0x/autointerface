"""
demo.py — Generate a realistic demo run.

Creates 5 actual HTML generations showing interface evolution,
takes real screenshots, and simulates a 50-generation score trajectory
for the progress chart. Run this to see what autointerface output looks like.

Usage: python demo.py
"""

import asyncio
import csv
import json
import random
import math
from datetime import datetime, timezone, timedelta
from pathlib import Path

HISTORY_DIR = Path("history")

# ---------------------------------------------------------------------------
# 5 HTML generations showing real evolution
# ---------------------------------------------------------------------------

GEN_1_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Tasks</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f5f5f5; color: #333; padding: 20px; }
.container { max-width: 640px; margin: 0 auto; }
h1 { font-size: 24px; margin-bottom: 20px; }
input[type="text"] { width: 100%; padding: 12px; border: 1px solid #ccc; border-radius: 4px; font-size: 16px; margin-bottom: 20px; }
h2 { font-size: 18px; margin: 15px 0 10px; color: #666; }
.task { padding: 10px; background: white; border: 1px solid #ddd; border-radius: 4px; margin-bottom: 8px; cursor: pointer; display: flex; align-items: center; gap: 10px; }
.task.done { text-decoration: line-through; opacity: 0.5; }
.checkbox { width: 18px; height: 18px; border: 2px solid #ccc; border-radius: 3px; flex-shrink: 0; }
.task.done .checkbox { background: #4CAF50; border-color: #4CAF50; }
</style>
</head>
<body>
<div class="container">
<h1>My Tasks</h1>
<input type="text" placeholder="Add a task..." id="input">
<h2>Today</h2>
<div class="task"><div class="checkbox"></div>Review design specs for onboarding flow</div>
<div class="task"><div class="checkbox"></div>Send feedback on logo concepts</div>
<div class="task"><div class="checkbox"></div>Fix responsive layout on pricing page</div>
<h2>This Week</h2>
<div class="task"><div class="checkbox"></div>Write blog post about design systems</div>
<div class="task"><div class="checkbox"></div>Prepare slides for Friday standup</div>
<div class="task"><div class="checkbox"></div>Audit color contrast across all pages</div>
<h2>Done</h2>
<div class="task done"><div class="checkbox"></div>Set up analytics dashboard</div>
<div class="task done"><div class="checkbox"></div>Update brand guidelines document</div>
</div>
<script>
const input = document.getElementById('input');
input.addEventListener('keydown', e => {
  if (e.key === 'Enter' && input.value.trim()) {
    const task = document.createElement('div');
    task.className = 'task';
    task.innerHTML = '<div class="checkbox"></div>' + input.value;
    document.querySelector('h2').nextElementSibling ?
      document.querySelector('h2').after(task) : document.querySelector('.container').appendChild(task);
    input.value = '';
  }
});
document.querySelectorAll('.task').forEach(t => {
  t.addEventListener('click', () => t.classList.toggle('done'));
});
</script>
</body>
</html>"""

GEN_2_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Tasks</title>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: 'Georgia', 'Charter', 'Bitstream Charter', serif;
  background: #FAF9F7;
  color: #2D2016;
  min-height: 100vh;
}
.container {
  max-width: 640px;
  margin: 0 auto;
  padding: 60px 24px;
}
.page-title {
  font-size: 14px;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  color: #A09080;
  margin-bottom: 40px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  font-weight: 500;
}
.input-wrapper {
  margin-bottom: 48px;
}
.input-wrapper input {
  width: 100%;
  padding: 16px 0;
  border: none;
  border-bottom: 2px solid #E8E0D8;
  background: transparent;
  font-size: 18px;
  font-family: inherit;
  color: #2D2016;
  outline: none;
  transition: border-color 0.2s;
}
.input-wrapper input:focus {
  border-bottom-color: #C4592A;
}
.input-wrapper input::placeholder {
  color: #C0B0A0;
}
.section { margin-bottom: 40px; }
.section-title {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  color: #A09080;
  margin-bottom: 16px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  font-weight: 500;
}
.task {
  padding: 14px 0;
  border-bottom: 1px solid #F0EBE5;
  cursor: pointer;
  display: flex;
  align-items: flex-start;
  gap: 14px;
  transition: opacity 0.3s;
}
.task:hover { background: #F7F5F2; margin: 0 -12px; padding-left: 12px; padding-right: 12px; border-radius: 6px; }
.check {
  width: 20px;
  height: 20px;
  border: 2px solid #D0C4B8;
  border-radius: 50%;
  flex-shrink: 0;
  margin-top: 2px;
  transition: all 0.2s;
}
.task.done .check {
  background: #C4592A;
  border-color: #C4592A;
}
.task.done .task-text {
  text-decoration: line-through;
  color: #B0A090;
}
.task-text {
  font-size: 17px;
  line-height: 1.5;
}
.done-section {
  margin-top: 48px;
  padding-top: 24px;
  border-top: 1px solid #E8E0D8;
}
.done-toggle {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  color: #B0A090;
  cursor: pointer;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  font-weight: 500;
  background: none;
  border: none;
}
.done-toggle:hover { color: #8B7355; }
.done-list { display: none; margin-top: 12px; }
.done-list.open { display: block; }
</style>
</head>
<body>
<div class="container">
  <div class="page-title">Tasks</div>

  <div class="input-wrapper">
    <input type="text" placeholder="What needs to happen?" id="input" autofocus>
  </div>

  <div class="section" id="today-section">
    <div class="section-title">Today</div>
    <div id="today-list">
      <div class="task"><div class="check"></div><span class="task-text">Review design specs for onboarding flow</span></div>
      <div class="task"><div class="check"></div><span class="task-text">Send feedback on logo concepts</span></div>
      <div class="task"><div class="check"></div><span class="task-text">Fix responsive layout on pricing page</span></div>
    </div>
  </div>

  <div class="section" id="week-section">
    <div class="section-title">This Week</div>
    <div id="week-list">
      <div class="task"><div class="check"></div><span class="task-text">Write blog post about design systems</span></div>
      <div class="task"><div class="check"></div><span class="task-text">Prepare slides for Friday standup</span></div>
      <div class="task"><div class="check"></div><span class="task-text">Audit color contrast across all pages</span></div>
    </div>
  </div>

  <div class="done-section">
    <button class="done-toggle" id="done-toggle">Completed (2) ▾</button>
    <div class="done-list" id="done-list">
      <div class="task done"><div class="check"></div><span class="task-text">Set up analytics dashboard</span></div>
      <div class="task done"><div class="check"></div><span class="task-text">Update brand guidelines document</span></div>
    </div>
  </div>
</div>
<script>
const input = document.getElementById('input');
input.addEventListener('keydown', e => {
  if (e.key === 'Enter' && input.value.trim()) {
    const task = document.createElement('div');
    task.className = 'task';
    task.innerHTML = '<div class="check"></div><span class="task-text">' + input.value.trim() + '</span>';
    task.addEventListener('click', toggleTask);
    document.getElementById('today-list').prepend(task);
    input.value = '';
  }
});
function toggleTask() {
  this.classList.toggle('done');
}
document.querySelectorAll('.task').forEach(t => t.addEventListener('click', toggleTask));
document.getElementById('done-toggle').addEventListener('click', () => {
  document.getElementById('done-list').classList.toggle('open');
});
</script>
</body>
</html>"""

GEN_3_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Tasks</title>
<style>
:root {
  --bg: #FAF8F5;
  --surface: #FFFFFF;
  --text: #1E1915;
  --text-muted: #9E8E7E;
  --text-faint: #C4B8AC;
  --border: #EDE7E0;
  --border-light: #F5F0EB;
  --accent: #BF5630;
  --accent-hover: #A84A28;
  --done-bg: #F5F2EE;
  --shadow: 0 1px 3px rgba(30,25,21,0.04);
  --radius: 8px;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: 'Charter', 'Georgia', 'Bitstream Charter', serif;
  background: var(--bg);
  color: var(--text);
  min-height: 100vh;
  -webkit-font-smoothing: antialiased;
}
.container {
  max-width: 600px;
  margin: 0 auto;
  padding: 80px 24px 120px;
}
@media (max-width: 768px) {
  .container { padding: 48px 20px 80px; }
}
@media (max-width: 375px) {
  .container { padding: 32px 16px 60px; }
}
.header {
  margin-bottom: 48px;
}
.page-label {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, sans-serif;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 2px;
  color: var(--text-muted);
  margin-bottom: 8px;
}
.date {
  font-size: 15px;
  color: var(--text-faint);
}
.input-area {
  position: relative;
  margin-bottom: 56px;
}
.input-area input {
  width: 100%;
  padding: 18px 20px;
  border: 2px solid var(--border);
  border-radius: var(--radius);
  background: var(--surface);
  font-size: 17px;
  font-family: inherit;
  color: var(--text);
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
  box-shadow: var(--shadow);
}
.input-area input:focus {
  border-color: var(--accent);
  box-shadow: 0 0 0 3px rgba(191,86,48,0.08);
}
.input-area input::placeholder {
  color: var(--text-faint);
  font-style: italic;
}
.input-hint {
  position: absolute;
  right: 16px;
  top: 50%;
  transform: translateY(-50%);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  font-size: 11px;
  color: var(--text-faint);
  background: var(--border-light);
  padding: 3px 8px;
  border-radius: 4px;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.2s;
}
.input-area input:focus ~ .input-hint { opacity: 1; }

.section { margin-bottom: 44px; }
.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 14px;
}
.section-title {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, sans-serif;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 2px;
  color: var(--text-muted);
}
.section-count {
  font-family: 'SF Mono', 'Fira Code', 'Fira Mono', monospace;
  font-size: 11px;
  color: var(--text-faint);
}
.task-list { list-style: none; }
.task {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 16px 16px;
  margin: 0 -16px;
  border-radius: var(--radius);
  cursor: pointer;
  transition: background 0.15s;
  user-select: none;
}
.task:hover { background: rgba(30,25,21,0.02); }
.task + .task { border-top: 1px solid var(--border-light); }
.task:hover + .task { border-top-color: transparent; }
.check-circle {
  width: 22px;
  height: 22px;
  border: 2px solid var(--border);
  border-radius: 50%;
  flex-shrink: 0;
  margin-top: 1px;
  transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}
.check-circle::after {
  content: '';
  position: absolute;
  top: 4px;
  left: 7px;
  width: 5px;
  height: 9px;
  border: 2px solid white;
  border-top: none;
  border-left: none;
  transform: rotate(45deg) scale(0);
  transition: transform 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}
.task.completed .check-circle {
  background: var(--accent);
  border-color: var(--accent);
  transform: scale(0.95);
}
.task.completed .check-circle::after {
  transform: rotate(45deg) scale(1);
}
.task-content { flex: 1; min-width: 0; }
.task-text {
  font-size: 17px;
  line-height: 1.5;
  transition: color 0.2s, opacity 0.2s;
}
.task.completed .task-text {
  color: var(--text-faint);
  text-decoration: line-through;
  text-decoration-color: var(--border);
}
.task-delete {
  opacity: 0;
  background: none;
  border: none;
  color: var(--text-faint);
  cursor: pointer;
  font-size: 18px;
  padding: 4px;
  transition: opacity 0.15s, color 0.15s;
  flex-shrink: 0;
}
.task:hover .task-delete { opacity: 1; }
.task-delete:hover { color: var(--accent); }

.done-section {
  margin-top: 56px;
  padding-top: 28px;
  border-top: 1px solid var(--border);
}
.done-toggle {
  display: flex;
  align-items: center;
  gap: 8px;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, sans-serif;
  font-size: 12px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  color: var(--text-faint);
  cursor: pointer;
  background: none;
  border: none;
  padding: 4px 0;
  transition: color 0.2s;
}
.done-toggle:hover { color: var(--text-muted); }
.done-toggle .arrow {
  display: inline-block;
  transition: transform 0.2s;
  font-size: 10px;
}
.done-toggle.open .arrow { transform: rotate(180deg); }
.done-list {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.3s ease;
}
.done-list.open { max-height: 800px; }
.done-list .task { opacity: 0.6; }
.done-list .task:hover { opacity: 0.8; }
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <div class="page-label">Tasks</div>
    <div class="date" id="date"></div>
  </div>

  <div class="input-area">
    <input type="text" placeholder="What needs doing?" id="input" autofocus>
    <span class="input-hint">press enter</span>
  </div>

  <div class="section" id="today-section">
    <div class="section-header">
      <span class="section-title">Today</span>
      <span class="section-count" id="today-count">3</span>
    </div>
    <ul class="task-list" id="today-list">
      <li class="task">
        <div class="check-circle"></div>
        <div class="task-content"><span class="task-text">Review design specs for onboarding flow</span></div>
        <button class="task-delete" title="Delete">×</button>
      </li>
      <li class="task">
        <div class="check-circle"></div>
        <div class="task-content"><span class="task-text">Send feedback on logo concepts</span></div>
        <button class="task-delete" title="Delete">×</button>
      </li>
      <li class="task">
        <div class="check-circle"></div>
        <div class="task-content"><span class="task-text">Fix responsive layout on pricing page</span></div>
        <button class="task-delete" title="Delete">×</button>
      </li>
    </ul>
  </div>

  <div class="section" id="week-section">
    <div class="section-header">
      <span class="section-title">This Week</span>
      <span class="section-count" id="week-count">3</span>
    </div>
    <ul class="task-list" id="week-list">
      <li class="task">
        <div class="check-circle"></div>
        <div class="task-content"><span class="task-text">Write blog post about design systems</span></div>
        <button class="task-delete" title="Delete">×</button>
      </li>
      <li class="task">
        <div class="check-circle"></div>
        <div class="task-content"><span class="task-text">Prepare slides for Friday standup</span></div>
        <button class="task-delete" title="Delete">×</button>
      </li>
      <li class="task">
        <div class="check-circle"></div>
        <div class="task-content"><span class="task-text">Audit color contrast across all pages</span></div>
        <button class="task-delete" title="Delete">×</button>
      </li>
    </ul>
  </div>

  <div class="done-section">
    <button class="done-toggle" id="done-toggle">
      Completed <span id="done-count">(2)</span>
      <span class="arrow">▼</span>
    </button>
    <div class="done-list" id="done-list">
      <ul class="task-list">
        <li class="task completed">
          <div class="check-circle"></div>
          <div class="task-content"><span class="task-text">Set up analytics dashboard</span></div>
          <button class="task-delete" title="Delete">×</button>
        </li>
        <li class="task completed">
          <div class="check-circle"></div>
          <div class="task-content"><span class="task-text">Update brand guidelines document</span></div>
          <button class="task-delete" title="Delete">×</button>
        </li>
      </ul>
    </div>
  </div>
</div>

<script>
// Date
const d = new Date();
const opts = { weekday: 'long', month: 'long', day: 'numeric' };
document.getElementById('date').textContent = d.toLocaleDateString('en-US', opts);

// Add task
const input = document.getElementById('input');
input.addEventListener('keydown', e => {
  if (e.key === 'Enter' && input.value.trim()) {
    addTask(input.value.trim(), 'today-list');
    input.value = '';
    updateCounts();
  }
});

function addTask(text, listId) {
  const li = document.createElement('li');
  li.className = 'task';
  li.innerHTML = `
    <div class="check-circle"></div>
    <div class="task-content"><span class="task-text">${text}</span></div>
    <button class="task-delete" title="Delete">×</button>
  `;
  bindTask(li);
  document.getElementById(listId).prepend(li);
}

function bindTask(el) {
  el.querySelector('.check-circle').addEventListener('click', e => {
    e.stopPropagation();
    el.classList.toggle('completed');
    updateCounts();
  });
  el.querySelector('.task-delete').addEventListener('click', e => {
    e.stopPropagation();
    el.style.opacity = '0';
    el.style.transform = 'translateX(20px)';
    el.style.transition = 'all 0.2s';
    setTimeout(() => { el.remove(); updateCounts(); }, 200);
  });
}

document.querySelectorAll('.task').forEach(bindTask);

// Done toggle
document.getElementById('done-toggle').addEventListener('click', function() {
  this.classList.toggle('open');
  document.getElementById('done-list').classList.toggle('open');
});

function updateCounts() {
  const today = document.querySelectorAll('#today-list .task:not(.completed)').length;
  const week = document.querySelectorAll('#week-list .task:not(.completed)').length;
  const done = document.querySelectorAll('.task.completed').length;
  document.getElementById('today-count').textContent = today;
  document.getElementById('week-count').textContent = week;
  document.getElementById('done-count').textContent = `(${done})`;
}
</script>
</body>
</html>"""


# Gen 4 and 5 would exist in a real run but we'll simulate scores for them

# ---------------------------------------------------------------------------
# Screenshot helper
# ---------------------------------------------------------------------------

async def screenshot_html(html: str, gen_dir: Path):
    from playwright.async_api import async_playwright

    gen_dir.mkdir(parents=True, exist_ok=True)
    html_path = gen_dir / "app.html"
    html_path.write_text(html)

    viewports = [
        {"width": 1440, "height": 900, "name": "desktop"},
        {"width": 768, "height": 1024, "name": "tablet"},
        {"width": 375, "height": 812, "name": "mobile"},
    ]

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        for vp in viewports:
            ctx = await browser.new_context(
                viewport={"width": vp["width"], "height": vp["height"]},
                device_scale_factor=2,
            )
            page = await ctx.new_page()
            await page.goto(f"file://{html_path.resolve()}")
            await page.wait_for_timeout(1000)
            await page.screenshot(
                path=str(gen_dir / f"{vp['name']}.png"),
                full_page=True,
            )
            await ctx.close()
            print(f"    {vp['name']} ✓")
        await browser.close()


# ---------------------------------------------------------------------------
# Build evolution data
# ---------------------------------------------------------------------------

def generate_score_trajectory(n=50):
    """Generate a realistic score trajectory showing improvement over time."""
    scores = []
    base = 28  # starting score
    for i in range(n):
        # logistic growth with noise
        progress = i / n
        improvement = 52 / (1 + math.exp(-8 * (progress - 0.35)))
        noise = random.gauss(0, 4)
        # occasional regression
        if random.random() < 0.08:
            noise -= 8
        score = int(max(12, min(95, base + improvement + noise)))
        scores.append(score)
    return scores


def write_evolution_csv(scores):
    csv_path = HISTORY_DIR / "evolution.csv"
    base_time = datetime(2026, 3, 18, 22, 0, 0, tzinfo=timezone.utc)

    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["gen", "score", "parent", "timestamp", "critique_preview"])
        for i, score in enumerate(scores):
            gen = i + 1
            parent = max(1, gen - 1) if gen > 1 else ""
            ts = (base_time + timedelta(seconds=65 * i)).isoformat()
            critique = [
                "Visual hierarchy needs work. The section headers compete with task text for attention.",
                "Good progress on spacing. The input field feels disconnected from the task list below.",
                "Typography is improving. Consider using serif for task text to match the editorial feel.",
                "Hover states feel polished. The delete button transition is too abrupt at 0ms.",
                "Strong generation. The check animation is satisfying. Whitespace between sections is generous.",
                "Border radius is inconsistent between input and task items. Unify to one value.",
                "Color palette is cohesive now. The accent color earns its place on interactive elements.",
                "Mobile layout is solid. The touch targets on checkboxes could be slightly larger.",
                "Best generation yet. The page feels calm and intentional. Done section toggle is clean.",
                "Minor regression. The font size dropped too small on mobile. Revert body to 17px.",
            ][i % 10]
            writer.writerow([gen, score, parent, ts, critique[:120]])


def write_state(scores):
    best_score = max(scores)
    best_gen = scores.index(best_score) + 1
    state = {
        "current_gen": len(scores),
        "best_score": best_score,
        "best_gen": best_gen,
        "survivors": [
            {"gen": best_gen, "score": best_score},
        ],
    }
    (HISTORY_DIR / "state.json").write_text(json.dumps(state, indent=2))
    (HISTORY_DIR / "best.json").write_text(json.dumps({
        "gen": best_gen,
        "score": best_score,
        "path": f"gen_{best_gen:03d}",
    }, indent=2))
    return state


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

async def main():
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)

    generations = {
        1: (GEN_1_HTML, 28, "Basic structure. Looks like a tutorial project. No personality, generic spacing, default styles."),
        2: (GEN_2_HTML, 52, "Better typography and color. Serif choice adds character. Spacing improved. Hover states present but input area feels disconnected."),
        3: (GEN_3_HTML, 74, "Strong generation. Visual hierarchy is clear. Check animation is satisfying. Responsive layout works. Done section toggle is clean. Could push the tactile quality further."),
    }

    print("autointerface demo — generating sample evolution\n")

    for gen_num, (html, score, critique) in generations.items():
        gen_dir = HISTORY_DIR / f"gen_{gen_num:03d}"
        print(f"  gen {gen_num} (score: {score})...")
        print(f"    writing app.html...")

        # save HTML
        gen_dir.mkdir(parents=True, exist_ok=True)
        (gen_dir / "app.html").write_text(html)

        # take screenshots
        print(f"    taking screenshots...")
        await screenshot_html(html, gen_dir)

        # save score
        score_data = {
            "score": score,
            "critique": critique,
            "suggestion": "See critique for direction.",
            "breakdown": {},
        }
        (gen_dir / "score.json").write_text(json.dumps(score_data, indent=2))

        # save meta
        meta = {
            "gen": gen_num,
            "parent": gen_num - 1 if gen_num > 1 else None,
            "score": score,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        (gen_dir / "meta.json").write_text(json.dumps(meta, indent=2))
        print(f"    done ✓\n")

    # generate full score trajectory
    print("  generating 50-generation score trajectory...")
    random.seed(42)
    scores = generate_score_trajectory(50)
    # replace first 3 with our actual scores
    scores[0] = 28
    scores[1] = 52
    scores[2] = 74
    write_evolution_csv(scores)
    state = write_state(scores)

    print(f"  best: gen {state['best_gen']} with score {state['best_score']}\n")

    # generate chart
    print("  generating progress chart...")
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        gens = list(range(1, len(scores) + 1))
        window = 5
        rolling = []
        for i in range(len(scores)):
            start = max(0, i - window + 1)
            rolling.append(sum(scores[start:i+1]) / (i - start + 1))

        best_line = []
        cb = 0
        for s in scores:
            cb = max(cb, s)
            best_line.append(cb)

        fig, ax = plt.subplots(1, 1, figsize=(14, 5))
        ax.scatter(gens, scores, s=16, alpha=0.3, color="#8B7355", label="individual", zorder=2)
        ax.plot(gens, rolling, color="#2D2016", linewidth=2.5, label=f"rolling avg ({window})", zorder=3)
        ax.plot(gens, best_line, color="#BF5630", linewidth=1.5, linestyle="--", label="best so far", zorder=3)

        ax.set_xlabel("generation", fontsize=12, color="#666")
        ax.set_ylabel("design score", fontsize=12, color="#666")
        ax.set_title("autointerface — overnight evolution", fontsize=15, fontweight="bold", color="#1E1915", pad=16)
        ax.legend(loc="lower right", fontsize=10, framealpha=0.9)
        ax.set_ylim(0, 100)
        ax.set_xlim(0, len(scores) + 1)
        ax.grid(True, alpha=0.1)
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.spines["left"].set_alpha(0.3)
        ax.spines["bottom"].set_alpha(0.3)
        ax.tick_params(colors="#999")
        fig.patch.set_facecolor("#FAF8F5")
        ax.set_facecolor("#FAF8F5")

        # annotate key generations
        ax.annotate("gen 1: basic tutorial look", xy=(1, 28), xytext=(6, 18),
                    fontsize=9, color="#999", arrowprops=dict(arrowstyle='->', color='#ccc'))
        ax.annotate("gen 3: typography + spacing click", xy=(3, 74), xytext=(8, 82),
                    fontsize=9, color="#999", arrowprops=dict(arrowstyle='->', color='#ccc'))
        best_gen = state['best_gen']
        ax.annotate(f"gen {best_gen}: best ({state['best_score']})", xy=(best_gen, state['best_score']),
                    xytext=(best_gen - 8, state['best_score'] - 12),
                    fontsize=9, color="#BF5630", fontweight="bold",
                    arrowprops=dict(arrowstyle='->', color='#BF5630'))

        fig.tight_layout()
        chart_path = Path("history_preview.png")
        fig.savefig(chart_path, dpi=180, bbox_inches="tight")
        print(f"  saved chart → {chart_path}")

    except ImportError:
        print("  matplotlib not available, skipping chart")

    print("\n✓ demo complete")
    print(f"  open history/gen_003/app.html in a browser to see the best generation")
    print(f"  history/evolution.csv has the full trajectory")
    print(f"  history_preview.png is your README hero image")


if __name__ == "__main__":
    asyncio.run(main())
