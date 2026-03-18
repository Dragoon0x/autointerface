# I Wrote a Spec, Went to Sleep, and Woke Up to a Working Interface

Last week Andrej Karpathy published [autoresearch](https://github.com/karpathy/autoresearch), a repo where an AI agent runs ML experiments autonomously overnight. You write a `program.md`. The agent reads it, modifies training code, runs experiments, checks if the result improved, keeps or discards, and repeats. You wake up to a log of experiments and a better model.

39k stars in a week. Not because the code is complex. Because the idea is simple and the implication is massive: the researcher doesn't write Python anymore. The researcher writes instructions for the thing that writes Python. The skill moved up one layer.

That got me thinking.

If this works for ML research, what does it look like for interface design?

## So I built it

[autointerface](https://github.com/Dragoon0x/autointerface) works like this:

1. You write a `spec.md` describing what the interface should do and who it's for.
2. An AI agent reads the spec and generates a complete, self-contained `app.html`.
3. Playwright renders the HTML and takes screenshots at three viewport sizes.
4. A vision model scores the screenshots against the spec and real design principles.
5. The scoring model writes a critique. That critique gets fed back into the next generation.
6. Better score? Keep and evolve. Worse? Discard.
7. Repeat. Overnight. 500+ generations.

You wake up to a `/history` folder containing every generation's HTML, screenshots, scores, and critiques. Open the best one in a browser. It works. Buttons click. States change. Interactions respond. It's not a mockup. It's a real interface.

## What actually happened

I wrote a spec for a personal task manager. Nothing fancy. Single column, two sections (Today and This Week), one input field, warm neutrals, generous spacing. The kind of thing a designer would sketch in an afternoon.

Then I ran it.

Generation 1 looked like every Bootstrap todo tutorial you've ever seen. Gray background, system font, no personality. Score: 28 out of 100.

The scoring model's critique was direct: "Visual hierarchy needs work. The section headers compete with task text for attention. There's no sense of warmth or editorial quality. This looks like a homework assignment."

Generation 2 took that feedback. Introduced a serif for task text. Warmed up the palette. Added spacing between sections. Still rough, but you could feel it reaching toward something. Score: 52.

By generation 3, something clicked. The typography had character. The spacing felt intentional. The input field had a subtle focus state with the accent color. The completed section collapsed with a clean toggle. It looked like something a designer made on purpose. Score: 74.

The evolution chart tells the story better than I can. It's a noisy climb with occasional regressions, the agent tries something that doesn't work, backs off, tries a different direction. By generation 40 it's consistently in the 75-85 range. The plateau is the interesting part. That's where the spec ran out of specificity and the agent started oscillating between equally valid interpretations.

## What I learned

Three things became obvious watching this happen.

**The spec is the design.** A vague spec produces a generic interface. Every time. The scoring model can critique execution all day, but it can't invent taste that isn't in the spec. When I wrote "warm neutrals, think paper and ink," the agent knew what to do. When I wrote "make it look good," it floundered. The quality of the output is a direct function of the quality of the spec. This is not a new insight for anyone who has written a design brief. But it is new to see it demonstrated in such a tight feedback loop.

**The critique loop is everything.** Random mutation produces random results. Directed mutation, where each generation gets specific, actionable feedback from the previous score, produces convergent results. The scoring model isn't just judging. It's art directing. "The gap between the input and the first task is too large, it breaks the visual connection between creation and content." That's not a number. That's a design review. And it happens 500 times in one night.

**The evolution log is the portfolio piece.** Nobody cares about a static screenshot. But watching an interface evolve from tutorial project to something with genuine taste? That's a story. Generation 1 vs generation 47, side by side. The progression from default styles to intentional design decisions. The moments where the agent made a bold move that worked. The regressions where it tried something weird and the score dropped. This is more interesting than any Behance case study because it shows the process at a resolution no human process could match.

## What this means for designers

I don't think this replaces designers. I think it relocates what designers do.

For the last 30 years, a designer's value was split between taste (knowing what good looks like) and execution (making the thing). These two skills were bundled together because they had to be. You couldn't separate your sense of visual hierarchy from your ability to arrange elements in Figma. They were the same action.

They're not the same action anymore.

Execution is becoming automated. Not perfectly. Not yet. But directionally. What's left when execution is handled is the thing that was always the harder skill anyway: taste. Judgment. Knowing what to ask for. Knowing what good feels like before you see it. Knowing who the user is and what they need and how the interface should make them feel.

That's spec-writing. And it's harder than pushing pixels. Because you have to articulate things you used to just feel your way through.

The designer who can write a spec that produces a great interface from an AI agent is more valuable than the designer who can only produce a great interface by hand. Because the first one can produce 500 in a night.

## Try it

The repo is here: [github.com/Dragoon0x/autointerface](https://github.com/Dragoon0x/autointerface)

It's MIT licensed. Clone it, write your own spec, run it overnight. The included spec is a task manager, but there are example specs for a dashboard, a landing page, and a settings panel.

I want to see what happens when people with different tastes write different specs for the same problem. Two designers writing specs for the same app, running them overnight, comparing what the machine converged on. That's a design competition I'd actually want to watch.

The spec is the design. The spec is the product. The spec is the portfolio.

Write a good one.
