# Interface Spec: Product Landing Page

> A landing page for a fictional tool called "Tempo" — a writing app that adapts its interface
> to your energy level. Not a real product. But the page should feel like it could be.

## What is this?

A single-page marketing site for Tempo. One page. No navigation to other pages. The goal: someone lands here from a tweet, understands what Tempo does in 10 seconds, feels something in 30 seconds, and either signs up for the waitlist or leaves. That's it.

## Who is landing here?

Writers who feel overwhelmed by their tools. People who have tried Notion, Google Docs, Obsidian, and iA Writer and keep switching because nothing feels right all the time. They write in different modes: sometimes deep-focus long-form, sometimes scattered brainstorming, sometimes just capturing fleeting ideas. They want one tool that adapts to how they're working, not the other way around.

They're skeptical of new tools. They've seen too many "revolutionary writing apps" that turn out to be Markdown editors with a dark mode. They need to feel like this one is different before they'll give it their email.

## Page structure (top to bottom)

1. **Hero.** Headline + subheadline + waitlist email input. No hero image. The typography IS the hero. The headline should feel like something you'd underline in a book, not something you'd put on a billboard.

2. **The problem.** 2-3 short paragraphs (not bullets) describing the pain. Written in second person. "You've tried everything..." energy. Empathetic, not dramatic.

3. **The idea.** One clear section explaining what Tempo does differently. Not features. The core concept: your writing tool should match your energy, not fight it. One visual element here: three interface states shown side by side or animated (focus mode, brainstorm mode, capture mode). These can be abstract/simplified representations, not full screenshots.

4. **How it works.** Three steps, kept dead simple. Each step: a short title, one sentence, and a subtle visual. No icons from an icon library. Custom illustrations or abstract shapes only.

5. **Social proof.** Not testimonials (product doesn't exist yet). Instead, logos of tools it integrates with, or a "from the makers of..." line, or early supporter quotes. Keep it minimal. One row.

6. **Final CTA.** Waitlist signup repeated. Same email input as the hero. A short line underneath: something warm, not pressuring. "We'll let you know when it's ready. No spam, obviously."

## What it should feel like

- Literary. Like a well-designed book jacket, not a tech startup page.
- Confident and quiet. No exclamation marks. No "revolutionary." No "game-changing."
- The page should scroll at a rhythm. Each section should feel like turning a page.
- Warm. This is a tool for writers, and the page should feel like it was made by people who care about words.

## What it should NEVER feel like

- A Y Combinator demo day slide. No startup jargon.
- Aggressive. No countdown timers, no "limited spots," no urgency tactics.
- Over-designed. If the design competes with the copy for attention, the design is wrong.
- Template-y. If someone could guess which Framer template this started from, start over.

## Visual direction

- Light background. Off-white, not pure white. Think aged paper.
- Black text with one accent color. The accent is used exactly twice: the CTA button and one highlight in the hero.
- Lots of vertical whitespace between sections. Let the page breathe.
- Subtle textures or grain welcome. Not mandatory but adds warmth.

## Typography direction

- A serif for the hero headline and section headings. Something with personality. Not a geometric sans.
- A clean sans-serif for body text. Readable at 18-20px.
- Generous line-height (1.6+). Comfortable reading measure (max 65 characters per line).

## Hard constraints

- Single HTML file. All CSS and JS inline.
- No external fonts. Use a system font stack that includes good serifs (Georgia, Charter, etc).
- No images. All visual elements must be CSS, SVG, or HTML.
- Smooth scroll behavior.
- The waitlist form doesn't need to actually submit. Just a styled input + button with a success state on click.
- Must work beautifully on desktop (1440px) and mobile (375px).
- Page weight under 30KB.
- WCAG AA contrast on all text.
- No JavaScript frameworks. Vanilla JS for interactions only.
