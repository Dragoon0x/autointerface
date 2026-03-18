"""
screenshot.py — Render HTML to screenshots at multiple viewports.

Uses Playwright to open the generated app.html in a headless browser
and capture what users would actually see. These screenshots are what
the scoring model evaluates.

Why screenshots instead of raw HTML? Because design is visual.
The model needs to see what the user sees, not read what the developer wrote.
"""

import asyncio
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
VIEWPORTS = [
    {"width": 1440, "height": 900, "name": "desktop"},
    {"width": 768, "height": 1024, "name": "tablet"},
    {"width": 375, "height": 812, "name": "mobile"},
]

# wait for page to settle (fonts, transitions, initial renders)
SETTLE_MS = 1500


# ---------------------------------------------------------------------------
# Core
# ---------------------------------------------------------------------------

async def take_screenshots(html_path: Path, output_dir: Path) -> list[Path]:
    """Render the HTML file at multiple viewports and save screenshots."""
    from playwright.async_api import async_playwright

    html_path = html_path.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    screenshots = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        for vp in VIEWPORTS:
            context = await browser.new_context(
                viewport={"width": vp["width"], "height": vp["height"]},
                device_scale_factor=2,  # retina for better scoring
            )
            page = await context.new_page()

            # load the file
            await page.goto(f"file://{html_path}")

            # wait for page to settle
            await page.wait_for_timeout(SETTLE_MS)

            # take full page screenshot
            output_path = output_dir / f"{vp['name']}.png"
            await page.screenshot(
                path=str(output_path),
                full_page=True,
                type="png",
            )
            screenshots.append(output_path)

            await context.close()
            print(f"  captured {vp['name']} ({vp['width']}x{vp['height']})")

        await browser.close()

    return screenshots


def screenshot_sync(html_path: Path, output_dir: Path) -> list[Path]:
    """Synchronous wrapper around take_screenshots."""
    return asyncio.run(take_screenshots(html_path, output_dir))


# ---------------------------------------------------------------------------
# CLI: screenshot a specific HTML file
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: uv run screenshot.py <path_to_html> [output_dir]")
        print("Example: uv run screenshot.py history/gen_001/app.html history/gen_001")
        sys.exit(1)

    html_path = Path(sys.argv[1])
    if not html_path.exists():
        print(f"ERROR: {html_path} not found.")
        sys.exit(1)

    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else html_path.parent
    print(f"screenshotting {html_path}...")

    paths = screenshot_sync(html_path, output_dir)
    print(f"\ndone. {len(paths)} screenshots saved to {output_dir}/")
    for p in paths:
        print(f"  {p}")
