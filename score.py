"""
score.py — Interface design scoring.

Evaluates a generation's interface against the spec and real design
principles using a vision model. The model sees the actual screenshots,
not just the code. It judges what users would see.

Returns a score (0-100) and a written critique that gets fed back
into the next generation as creative direction.

The scoring criteria encode real design judgment. Edit them if you
disagree. That's your taste showing up in a different place.
"""

import anthropic
import base64
import json
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
SCORE_MODEL = os.getenv("AUTOINTERFACE_SCORE_MODEL", "claude-sonnet-4-20250514")
SPEC_PATH = Path("spec.md")

client = anthropic.Anthropic()

# ---------------------------------------------------------------------------
# Scoring prompt — where design taste gets encoded
# ---------------------------------------------------------------------------

SCORING_PROMPT = """You are a senior interface design critic with 15 years of experience.

You are evaluating a generated interface. You have:
1. The original interface spec
2. Screenshots of the interface at three viewport sizes (desktop, tablet, mobile)
3. The raw HTML source code

Score this interface on a scale of 0-100 using the criteria below. Each criterion
is weighted. Be ruthlessly honest. A score of 50 means "it works but feels like a
tutorial project." A score of 70 means "solid work with clear areas for improvement."
A score of 85+ means "this is genuinely well-designed." Don't grade inflate.

CRITERIA:

**Spec Alignment (25 points)**
- Does it implement what the spec described? Every interaction, every constraint?
- Does it capture the FEELING the spec asked for, not just the features?
- Does it respect the "never" constraints and anti-references?
- Would the described user actually want to use this?

**Visual Hierarchy (15 points)**
- Is there a clear reading order on each screen?
- Do the most important elements (primary actions, key content) draw attention first?
- Is hierarchy achieved through size, weight, contrast, and spacing? Not just color?
- Can you scan the interface and understand the structure in 2 seconds?

**Layout & Spacing (15 points)**
- Is whitespace intentional or just leftover?
- Does the grid feel consistent? Are elements aligned to a system?
- Is there rhythm to the vertical spacing?
- Does the layout breathe? Or is it cramped or wastefully sparse?

**Typography (10 points)**
- Is there a clear type scale with hierarchy (heading, body, label, caption)?
- Are line-heights comfortable for reading?
- Is the measure (line length) reasonable? Not too wide, not too narrow?
- Do font choices match the spec's personality?

**Color & Contrast (10 points)**
- Are colors purposeful? Each color should have a job.
- Does the palette meet WCAG AA contrast ratios?
- Is the palette restrained or chaotic?
- Does color usage match the spec's intended mood?

**Responsiveness (10 points)**
- Does it work well at ALL three viewports (desktop, tablet, mobile)?
- Not just "doesn't break" but genuinely good use of each screen size?
- Are touch targets appropriate on mobile (min 44px)?
- Does the layout adapt intelligently, not just shrink?

**Interaction & Polish (10 points)**
- Do interactive elements have hover states? Focus states? Active states?
- Are there smooth transitions where they matter?
- Does it feel finished or half-done?
- Are there any broken interactions or dead-end states?

**Code Quality (5 points)**
- Is the HTML semantic (proper elements, not div soup)?
- Is the CSS organized and not repetitive?
- Is the JavaScript minimal and clean?
- Would a developer reviewing this code nod approvingly?

Return ONLY valid JSON:
{
  "score": 0-100,
  "breakdown": {
    "spec_alignment": {"score": 0-25, "notes": "specific observations"},
    "visual_hierarchy": {"score": 0-15, "notes": "..."},
    "layout_spacing": {"score": 0-15, "notes": "..."},
    "typography": {"score": 0-10, "notes": "..."},
    "color_contrast": {"score": 0-10, "notes": "..."},
    "responsiveness": {"score": 0-10, "notes": "..."},
    "interaction_polish": {"score": 0-10, "notes": "..."},
    "code_quality": {"score": 0-5, "notes": "..."}
  },
  "strengths": ["specific thing that works well", "another strength"],
  "weaknesses": ["specific thing to fix", "another issue"],
  "critique": "A 4-6 sentence overall design critique. Be specific. Name elements, point to problems, acknowledge what works. This gets fed directly to the next generation as creative direction, so write it as actionable design feedback, like you're talking to a junior designer in a review.",
  "suggestion": "One specific, concrete change to make in the next generation. Not vague ('improve spacing') but specific ('the gap between the input field and the first task is 32px but should be 16px to visually connect them as a group'). Reference exact elements, sizes, colors, or behaviors."
}

---

INTERFACE SPEC:
{spec}

---

HTML SOURCE (first 8000 chars for code quality assessment):
{html_preview}
"""


# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------

def load_spec() -> str:
    if not SPEC_PATH.exists():
        print("ERROR: spec.md not found.")
        sys.exit(1)
    return SPEC_PATH.read_text()


def load_screenshot(path: Path) -> dict | None:
    """Load a screenshot as a base64-encoded image for the vision model."""
    if not path.exists():
        return None
    with open(path, "rb") as f:
        data = base64.standard_b64encode(f.read()).decode("utf-8")
    return {
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": "image/png",
            "data": data,
        },
    }


def score_generation(
    spec: str,
    gen_dir: Path,
    html_content: str | None = None,
) -> dict:
    """Score a generation's interface against the spec. Returns score dict."""

    # load HTML if not provided
    if html_content is None:
        html_path = gen_dir / "app.html"
        if html_path.exists():
            html_content = html_path.read_text()
        else:
            html_content = "(HTML file not found)"

    # build message content: screenshots + text prompt
    content = []

    # add screenshots (these are what the model actually judges)
    for name in ["desktop", "tablet", "mobile"]:
        img = load_screenshot(gen_dir / f"{name}.png")
        if img:
            content.append({"type": "text", "text": f"[{name.upper()} VIEWPORT]"})
            content.append(img)

    # add the scoring prompt with spec and HTML preview
    html_preview = html_content[:8000] if html_content else "(no HTML)"
    prompt = SCORING_PROMPT.format(spec=spec, html_preview=html_preview)
    content.append({"type": "text", "text": prompt})

    response = client.messages.create(
        model=SCORE_MODEL,
        max_tokens=3000,
        messages=[{"role": "user", "content": content}],
    )

    text = response.content[0].text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)

    return json.loads(text)


def save_score(gen_dir: Path, score_data: dict) -> None:
    """Save score data to a generation directory."""
    (gen_dir / "score.json").write_text(json.dumps(score_data, indent=2))


# ---------------------------------------------------------------------------
# CLI: score a specific generation
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: uv run score.py <gen_dir>")
        print("Example: uv run score.py history/gen_001")
        sys.exit(1)

    gen_dir = Path(sys.argv[1])
    if not gen_dir.exists():
        print(f"ERROR: {gen_dir} not found.")
        sys.exit(1)

    spec = load_spec()
    print(f"scoring {gen_dir}...")
    score_data = score_generation(spec, gen_dir)
    save_score(gen_dir, score_data)

    print(f"\nscore: {score_data['score']}/100\n")
    print("breakdown:")
    for k, v in score_data.get("breakdown", {}).items():
        print(f"  {k}: {v['score']} — {v['notes'][:80]}")
    print(f"\ncritique: {score_data.get('critique', '')}")
    print(f"\nsuggestion: {score_data.get('suggestion', '')}")
    print(f"\nsaved to {gen_dir}/score.json")
