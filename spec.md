# Interface Spec

> This is the only file you edit. The agent reads this and builds the interface.
> Be specific where you have opinions. Be open where you want the agent to explore.
> The better this spec is, the better the output. Your taste lives here.

## What is this?

A personal task manager for a single user. Not a project management tool. Not a team collaboration app. Just one person keeping track of what they need to do today and this week.

Think: the digital equivalent of a well-organized notebook sitting on a desk. Not an enterprise dashboard.

## Who is it for?

A designer or developer who keeps things simple. Someone who has used Notion and Things and Linear and found them all slightly too much for what they actually need, which is a list they can glance at and know what to do next.

They value clarity over features. They want something that loads instantly and gets out of the way.

## Core interactions

1. **Add a task.** One input field, always visible. Type and press enter. That's it. No category pickers, no date selectors, no priority dropdowns cluttering the creation flow. Just text in, task created.

2. **Complete a task.** Click or tap it. It's done. Satisfying animation welcome but not required. Completed tasks move to a separate "done" section, collapsed by default.

3. **Delete a task.** Subtle. Not the primary action. Small icon or swipe or right-click. No confirmation dialog for single deletes.

4. **Reorder tasks.** Drag and drop. The order is the priority. First task is the most important. No priority labels needed when position IS priority.

5. **Sections.** Two fixed sections only: "Today" and "This Week." No custom sections. The constraint is the feature. It forces you to decide what actually matters today vs. what can wait.

## What it should feel like

- Fast. Instant load, instant response. No loading spinners for local operations.
- Quiet. Low visual noise. The interface disappears and the tasks are all you see.
- Tactile. Interactions should feel physical. Drag and drop should feel like moving a card on a desk. Checking off should feel like crossing something out.
- Opinionated. It does one thing well. It doesn't try to be flexible or extensible. The limitations are intentional.

## What it should NEVER feel like

- Busy. If there are more than 2 visual "zones" competing for attention on screen at once, something is wrong.
- Generic. If it looks like a Bootstrap todo app tutorial, start over.
- Feature-rich. If you're tempted to add filters, tags, search, or settings, resist. This is a tool for 10 tasks, not 10,000.
- Flat. Completely flat design without any depth cues feels sterile. Subtle shadows, slight texture, or gentle gradients are welcome. But subtle.

## Visual direction

- Warm neutral palette. Think paper, ink, and maybe one accent color that earns its place.
- Type-forward. The typography does most of the work. Big, confident task text. Smaller, quieter metadata.
- Generous spacing. Let it breathe. Cramped layouts feel stressful, which is the opposite of what a task manager should do.
- One accent color maximum. Used only for interactive affordances (add button, active states). Everything else is neutrals.

## Typography direction

- Something with character for task text. Not a geometric sans. Something that has warmth.
- System font stack is fine for UI elements.
- Clear size hierarchy: tasks are the biggest text. Section headers are quieter. Metadata is smallest.

## Layout

- Single column, centered, max-width 640px. No sidebar. No multi-pane layout.
- Task input at the top, always visible.
- "Today" section directly below.
- "This Week" section below that.
- "Done" section at the bottom, collapsed.
- On mobile: same layout, same logic, just tighter spacing.

## Hard constraints

- Single HTML file. All CSS and JS inline.
- Must work with no server, no API, no build step. Open the file in a browser and it works.
- All data stored in localStorage. Persistent across refreshes.
- No external dependencies. No frameworks, no CDNs, no Google Fonts loading. Everything self-contained.
- Must pass WCAG AA contrast ratios.
- Must work on latest Chrome, Firefox, and Safari.
- Page weight under 50KB.
- Time to interactive under 100ms.

## Reference energy

- The simplicity of a Paper by Dropbox note
- The typography confidence of iA Writer
- The tactile quality of Things 3 (but simpler)
- The restraint of a Muji product

## Anti-reference energy

- Notion (too many features, too much UI surface area)
- Todoist (too corporate, too many options)
- Any todo app tutorial with a gradient header and rounded cards
- Anything that looks like Material Design defaults
