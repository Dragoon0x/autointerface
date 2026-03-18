"""
generate.py — Interface generation.

Reads spec.md and produces a single self-contained app.html file.
HTML, CSS, and JS all inline. No dependencies, no build step.
Can also mutate a previous generation using critique feedback.

This file is NOT edited by the agent. The agent only edits spec.md.
"""

import anthropic
import json
import os
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
MODEL = os.getenv("AUTOINTERFACE_MODEL", "claude-sonnet-4-20250514")
SPEC_PATH = Path("spec.md")

client = anthropic.Anthropic()

# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------

GENERATE_PROMPT = """You are an expert interface designer and frontend developer.

Read the interface spec below carefully. Your job: produce a single, complete, self-contained HTML file that implements this interface exactly as described.

Rules:
- SINGLE FILE. All HTML, CSS, and JavaScript inline. No external dependencies.
- The file must work when opened directly in a browser. No server required.
- Use localStorage for persistence if the spec calls for it.
- Write clean, semantic HTML. Use appropriate elements (button, input, section, etc).
- CSS should be thoughtful. Not just functional but well-designed. Typography, spacing, color, transitions.
- JavaScript should be minimal and clean. No frameworks.
- Follow every constraint in the spec. If it says max-width 640px, mean it. If it says no CDNs, mean it.
- The interface should feel finished, not prototyped. Hover states, focus states, transitions, responsive behavior.
- Make it work on desktop (1440px), tablet (768px), and mobile (375px).

Return ONLY the complete HTML file content. Start with <!DOCTYPE html>. No markdown fences. No explanation before or after. Just the code.

INTERFACE SPEC:
{spec}

{mutation_context}"""

MUTATE_PROMPT_SECTION = """
EVOLUTION CONTEXT:
This is generation N+1. The previous generation scored {score}/100.

The design critic's feedback was:
{critique}

Specific suggestion for this generation:
{suggestion}

Here is the previous generation's HTML for reference (evolve it, don't start from scratch):

```html
{previous_html}
```

Use the feedback to improve. Keep what the critic praised. Fix what they called out. Apply the specific suggestion. Don't throw everything away. Evolve it. The goal is a higher score, not a different interface.
"""


# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------

def load_spec() -> str:
    """Load the interface spec from spec.md."""
    if not SPEC_PATH.exists():
        print("ERROR: spec.md not found. Create your interface spec first.")
        sys.exit(1)
    return SPEC_PATH.read_text()


def call_model(prompt: str, max_tokens: int = 16000) -> str:
    """Call the model and return the text response."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text.strip()


def clean_html(text: str) -> str:
    """Strip markdown fences if the model wrapped the output."""
    text = re.sub(r"^```(?:html)?\s*\n?", "", text)
    text = re.sub(r"\n?\s*```$", "", text)
    return text.strip()


def build_mutation_context(
    critique: str | None,
    suggestion: str | None,
    score: int | None,
    previous_html: str | None,
) -> str:
    """Build mutation context from previous generation feedback."""
    if not critique or not previous_html:
        return ""

    # truncate HTML if massive (keep first and last sections)
    html = previous_html
    if len(html) > 30000:
        html = html[:15000] + "\n\n<!-- ... middle truncated for context ... -->\n\n" + html[-15000:]

    return MUTATE_PROMPT_SECTION.format(
        score=score or "?",
        critique=critique or "No critique available.",
        suggestion=suggestion or "No specific suggestion.",
        previous_html=html,
    )


def generate_interface(
    spec: str,
    critique: str | None = None,
    suggestion: str | None = None,
    score: int | None = None,
    previous_html: str | None = None,
) -> str:
    """Generate a complete interface as a single HTML file."""
    mutation_ctx = build_mutation_context(critique, suggestion, score, previous_html)
    prompt = GENERATE_PROMPT.format(spec=spec, mutation_context=mutation_ctx)
    result = call_model(prompt)
    return clean_html(result)


def save_generation(gen_num: int, html: str, output_dir: Path = Path("history")) -> Path:
    """Save a generation's HTML to disk."""
    gen_dir = output_dir / f"gen_{gen_num:03d}"
    gen_dir.mkdir(parents=True, exist_ok=True)
    (gen_dir / "app.html").write_text(html)
    return gen_dir


# ---------------------------------------------------------------------------
# CLI: run a single generation
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    spec = load_spec()
    print(f"loaded spec ({len(spec)} chars)")
    print("generating interface...")

    html = generate_interface(spec)
    gen_dir = save_generation(1, html)

    size_kb = len(html.encode("utf-8")) / 1024
    print(f"\ndone. saved to {gen_dir}/app.html ({size_kb:.1f} KB)")
    print(f"open it in your browser: file://{gen_dir.resolve()}/app.html")
