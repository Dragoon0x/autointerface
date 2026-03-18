# Interface Spec: Analytics Dashboard

> A personal analytics dashboard for a solo creator tracking their content performance.
> Not a business intelligence tool. Not a team dashboard. One person, their numbers, at a glance.

## What is this?

A single-screen dashboard that shows a content creator their key metrics across platforms. Think: someone who publishes a newsletter, posts on X/Twitter, and has a YouTube channel. They want to open one page and know how things are going without logging into three different apps.

## Who is it for?

A solo creator who cares about trends more than exact numbers. They check this once a day, usually in the morning with coffee. They don't need drill-down analytics or export features. They need a mood check: are things going up, down, or sideways?

## Core sections

1. **Today's snapshot.** One horizontal row at the top. 3-4 key numbers with sparkline trends (7-day). Subscribers, views, engagement rate, revenue. Big numbers, small labels. Glanceable in 2 seconds.

2. **Weekly trend.** One clean line chart showing the primary metric (views or subscribers, user's choice) over the last 30 days. No gridlines. Minimal axis labels. The shape of the line is the information, not the exact values. Hover shows the value for that day.

3. **Content performance.** A simple list of recent posts/videos ranked by performance. Each row: title (truncated), platform icon, one metric (views or engagement), and a subtle bar showing relative performance against the user's average. No more than 8 items visible.

4. **Milestone tracker.** A single progress bar at the bottom. "1,247 / 2,000 subscribers." Simple. Motivating without being gamified.

## What it should feel like

- Morning newspaper. Informative, calm, scannable.
- The data should feel like a story, not a spreadsheet.
- Confident typography doing most of the visual work.
- Dark mode by default. This is a tool for focus, not decoration.

## What it should NEVER feel like

- A SaaS dashboard with 15 cards and 8 filters.
- Anything that requires scrolling to get the full picture.
- Colorful for the sake of being colorful. Data visualization colors should be functional, not festive.
- Cluttered. If you can't understand the page in 5 seconds, it's too complex.

## Visual direction

- Dark background, warm. Not pure black. Think #1A1A1A or #0F0E0D.
- One accent color for positive trends. One muted color for negative. One neutral for flat.
- Monospaced numbers. Proportional text for everything else.
- Minimal borders. Use spacing and subtle background shifts to create separation.

## Hard constraints

- Single HTML file. No external dependencies.
- Must work with no real data. Use realistic dummy data that's hardcoded.
- Responsive: must work on a laptop (1440px) and an iPad (768px). Mobile is secondary.
- No animations that distract. Subtle transitions only.
- All charts rendered in SVG or Canvas. No charting libraries.
- Page weight under 50KB.
- WCAG AA contrast on all text.
