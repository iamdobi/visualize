# CLAUDE.md

This is the **Visualize** plugin — an open-source Claude Code plugin that turns any idea, data, or content into beautiful, self-contained HTML visualizations.

## Repo Structure

```
visualize/
├── .claude-plugin/
│   └── plugin.json           # Plugin manifest (name, version, author)
├── skills/
│   └── visualize/
│       ├── SKILL.md           # Main skill file (loaded by Claude Code)
│       └── references/        # Detailed specs (progressive disclosure Level 3)
│           ├── design-system.md
│           ├── skeleton.md
│           ├── types.md
│           ├── libraries.md
│           ├── menu.md
│           ├── css-techniques.md
│           ├── animations.md
│           └── eval.md
├── examples/                  # 15 example HTML files
├── eval/                      # Eval loop infrastructure
│   ├── SKILL.md              # Evaluator skill
│   ├── LOOP.md               # Loop methodology
│   ├── loop-state.json       # Current round + score history
│   └── stress-tests.md       # 40 test cases
├── research/                  # Design research notes
├── CLAUDE.md                  # This file
├── README.md                  # GitHub-facing docs
└── LICENSE                    # MIT
```

## Installation

```bash
# Via Claude Code plugin system
/plugin marketplace add careerhackeralex/visualize
/plugin install visualize@careerhackeralex

# Or clone directly
git clone https://github.com/careerhackeralex/visualize.git
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

When editing skills/visualize/SKILL.md:
- Keep it under **5,000 words** (Anthropic best practice for progressive disclosure)
- Move detailed specs to `skills/visualize/references/` and link from SKILL.md
- YAML frontmatter must have `name` and `description` with trigger phrases

When editing examples:
- Always start from the skeleton in `skills/visualize/references/skeleton.md`
- Test both dark and light themes
- Verify hamburger menu (theme toggle, PNG download, print)

When running eval:
- `eval/loop-state.json` tracks round number and score history
- Quality gates: SHIP ≥9.0, ACCEPTABLE ≥8.0, NEEDS WORK ≥7.0

## Common Pitfalls

- Chart.js: must add `Chart.defaults.animation = false` before creating charts
- Theme toggle: charts must be destroyed and recreated (colors read at render time)
- `let`/`const` at top level → TDZ errors. Always use `var`.
- `@media (prefers-color-scheme)` fights with `.theme-dark` class → class-only theming
