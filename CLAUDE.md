# CLAUDE.md

This is the **Visualize** skill — an open-source Claude Code skill that turns any idea, data, or content into beautiful, self-contained HTML visualizations.

## Repo Structure

```
visualize/
├── SKILL.md              # Main skill file (loaded by Claude Code)
├── CLAUDE.md             # This file
├── README.md             # GitHub-facing docs
├── references/           # Detailed specs (progressive disclosure Level 3)
│   ├── design-system.md  # Full typography, color, spacing, animation specs
│   ├── skeleton.md       # Mandatory HTML skeleton (copy-paste template)
│   ├── types.md          # Visualization type patterns
│   ├── libraries.md      # CDN library links and usage
│   ├── menu.md           # Hamburger menu implementation
│   ├── css-techniques.md # Advanced CSS patterns
│   ├── animations.md     # Animation system reference
│   └── eval.md           # Eval scoring dimensions
├── eval/                 # Eval loop infrastructure
│   ├── SKILL.md          # Evaluator skill
│   ├── LOOP.md           # Loop methodology
│   ├── loop-state.json   # Current round + score history
│   └── stress-tests.md   # 40 test cases
├── examples/             # 15 example HTML files
└── research/             # Design research notes
```

## Key Decisions

- **Single-file HTML output** — inline CSS/JS, opens in any browser
- **Dark theme default** — class-based theming (NO @media prefers-color-scheme)
- **CSS-first animations** — no Motion.js, pure @keyframes + vanilla JS
- **`var` for all top-level JS** — prevents TDZ errors (root cause of many past bugs)
- **CDN libraries encouraged** — Chart.js, D3, Tailwind, Mermaid, Reveal.js, html-to-image
- **Inter font** via Google Fonts + Noto Sans for CJK/Arabic
- **Visual restraint** — no floating orbs, gradient text, scale transforms, glow effects

## Working on This Repo

When editing SKILL.md:
- Keep it under **5,000 words** (Anthropic best practice for progressive disclosure)
- Move detailed specs to `references/` and link from SKILL.md
- YAML frontmatter must have `name` and `description` with trigger phrases
- No XML angle brackets (`<` `>`) in frontmatter

When editing examples:
- Always start from the skeleton in `references/skeleton.md`
- Test both dark and light themes
- Check for console errors
- Verify hamburger menu (theme toggle, PNG download, print)

When running eval:
- `eval/loop-state.json` tracks round number and score history
- Scores use 8 dimensions: First Impression, Typography, Color, Layout, Content, Interactivity, Technical, Shareability
- Quality gates: SHIP ≥9.0, ACCEPTABLE ≥8.0, NEEDS WORK ≥7.0, FAIL <7.0

## Common Pitfalls

- Chart.js: must add `Chart.defaults.animation = false` before creating charts
- Theme toggle: charts must be destroyed and recreated (colors are read at render time)
- Canvas reuse: just `.destroy()` old chart, create new on same canvas (don't replace DOM)
- `let`/`const` at top level → TDZ errors. Always use `var`.
- `@media (prefers-color-scheme)` fights with `.theme-dark` class → use class-only theming
