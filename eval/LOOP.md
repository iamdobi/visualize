# Visualize Improvement Loop (v3 — Git-First, Complete)

The git repo (`https://github.com/careerhackeralex/visualize`) is the **source of truth**.
Every iteration clones fresh, works in isolation, and pushes all changes back.

## Architecture

```
Cron fires (hourly)
  └── Isolated sub-agent starts
        │
        ├── Step 0: Clone fresh from git
        ├── Step 1: Check state (skip if SHIP/VIRAL)
        ├── Step 2: Verify plugin structure
        ├── Step 3: Evaluate (screenshot + score all examples)
        ├── Step 4: Analyze (identify root causes, categorize issues)
        ├── Step 5: Fix SKILL.md (the most important step)
        ├── Step 6: Fix references (design-system, skeleton, etc.)
        ├── Step 7: Rebuild examples (regenerate from updated skill)
        ├── Step 8: Simplify (reduce complexity, remove dead code)
        ├── Step 9: Validate (re-screenshot, console check)
        ├── Step 10: Commit & push to git
        └── Step 11: Report to Alex via WhatsApp
```

## Steps in Detail

### Step 0: Clone Fresh
```bash
WORK_DIR=$(mktemp -d)
cd "$WORK_DIR"
git clone https://github.com/careerhackeralex/visualize.git
cd visualize
```
- Never touch the workspace copy
- Always test exactly what users would get

### Step 1: Check State
- Read `eval/loop-state.json`
- If gate is SHIP or VIRAL → report status, exit
- If `loopsSinceResearch >= 5` AND score plateau (< 0.3 improvement over last 3 rounds) → research phase (see below)

### Step 2: Verify Plugin Structure
Confirm the repo is a valid Claude Code plugin:
```
✓ .claude-plugin/plugin.json — exists, valid JSON, has name + version
✓ skills/visualize/SKILL.md — exists, valid YAML frontmatter, < 5000 words
✓ skills/visualize/references/ — all expected files present
✓ examples/*.html — all open without console errors
```
If any check fails → fix it before proceeding, or abort with error report.

### Step 3: Evaluate
Open every file in `examples/` in the browser (profile=openclaw):
- Screenshot each file in **dark** and **light** theme
- Save to `eval/screenshots/round{N}/{name}-dark.png` and `{name}-light.png`
- For slide decks: also screenshot slides 1, 3, 5
- Check browser console for JS errors
- Score all **8 dimensions** per file:
  1. First Impression (15%) — instant "wow" factor
  2. Typography (15%) — hierarchy, spacing, readability
  3. Color (10%) — palette cohesion, contrast, theme consistency
  4. Layout (15%) — grid, whitespace, responsive
  5. Content (15%) — data quality, labels, realistic content
  6. Interactivity (10%) — hover states, animations, transitions
  7. Technical (10%) — no errors, performance, accessibility
  8. Shareability (10%) — would someone screenshot this?
- Write results to `eval/eval-round{N}-raw.md`

### Step 4: Analyze
This is the thinking step. Read all scores and identify:
1. **Weakest dimensions** across all files (e.g., "Interactivity avg 5.8")
2. **Worst files** that drag the average down
3. **Recurring patterns** — same issue in 3+ files = systemic
4. **Root cause analysis** — WHY is the score low? Is the instruction unclear? Missing? Wrong?

Output: a prioritized list of 3-5 fixes, each tagged as:
- `SKILL` — fix in skills/visualize/SKILL.md
- `REF` — fix in skills/visualize/references/*.md
- `EXAMPLE` — fix in a specific example file
- `SKELETON` — fix in references/skeleton.md (affects all future outputs)

### Step 5: Fix SKILL.md ⭐ (Most Important Step)
**Every issue should trace back to a SKILL.md improvement.**

Read `skills/visualize/SKILL.md` carefully. For each identified issue:
- Is the instruction missing? → Add it
- Is it unclear? → Rewrite with concrete examples
- Is it too verbose? → Simplify
- Is it contradictory? → Resolve the conflict
- Is it buried? → Move to a more prominent position

Rules:
- Keep SKILL.md under **5,000 words** (move details to references)
- Use **concrete examples** not abstract guidelines ("use 2rem" not "use appropriate sizing")
- Add **anti-patterns** for common mistakes ("DON'T: gradient text on headings")
- Every instruction should be **testable** — you should be able to look at output and verify compliance

### Step 6: Fix References
Update files in `skills/visualize/references/` as needed:
- `design-system.md` — typography, colors, spacing, animations
- `skeleton.md` — the HTML template all outputs start from
- `menu.md` — hamburger menu implementation
- `types.md` — visualization type patterns
- `libraries.md` — CDN library usage
- `css-techniques.md` — advanced CSS patterns

Priority: `skeleton.md` > `design-system.md` > others (skeleton affects every output).

### Step 7: Rebuild Examples
Regenerate affected examples using the updated SKILL.md:
- Read the updated SKILL.md + references
- For each affected example, regenerate from scratch following the skill instructions
- Don't patch — rebuild. The skill should produce correct output from its instructions alone.
- If rebuilding all 15 is too expensive, focus on the 3-5 worst-scoring files

### Step 8: Simplify
For every modified file, actively reduce complexity:
- Remove unused CSS rules
- Consolidate duplicate styles
- Replace JS with CSS where possible (transitions, animations, visibility)
- Remove dead code paths
- Ensure all top-level JS uses `var` (not let/const)
- Target: each example should be as short as possible while maintaining quality

Use Claude Code's approach: read the file, identify what can be removed or simplified, rewrite.

### Step 9: Validate
Re-open every modified file in browser:
- Screenshot post-fix (save to `eval/screenshots/round{N}-fixed/`)
- Check console for zero JS errors
- Verify dark and light themes both work
- Verify hamburger menu (theme toggle, PNG download, print)
- Quick eyeball: does it look better than before?

If validation fails → fix and re-validate before committing.

### Step 10: Commit & Push
```bash
git add -A
git commit -m "eval: round {N} — avg {score} ({delta}), gate {GATE}

Key changes:
- {SKILL.md change 1}
- {SKILL.md change 2}
- {reference/example changes}

Weakest: {dimension} ({score}), Strongest: {dimension} ({score})"

git push origin main
```

### Step 11: Report
Send WhatsApp summary to Alex (+16507097191):
- Round number and gate
- Average score and delta from last round
- Per-dimension averages
- Top 3 changes made
- Git commit hash
- What to focus on next round

## Research Phase

Triggered when: `loopsSinceResearch >= 5` AND score plateau.

1. **Web search** — latest CSS/HTML techniques, award-winning visualizations, design trends
2. **Study references** — Stripe, Linear, Apple design patterns
3. **Analyze competition** — what makes Gamma/Canva output look professional?
4. **Document findings** in `research/round{N}-research.md`
5. **Update SKILL.md and references** with actionable techniques
6. **Reset** `loopsSinceResearch = 0`
7. Commit & push

## Quality Gates

| Gate | Avg Score | Min Score | Meaning |
|------|-----------|-----------|---------|
| VIRAL | ≥ 9.5 | all ≥ 9 | Screenshot-worthy, people ask "how?" |
| SHIP | ≥ 9.0 | all ≥ 8 | Ready for public use |
| ACCEPTABLE | ≥ 8.0 | all ≥ 7 | Functional, decent |
| NEEDS WORK | ≥ 7.0 | or any < 7 | Keep iterating |
| FAIL | < 7.0 | or any < 5 | Significant issues |

## Scoring Rubric (Calibration)

To reduce score drift between rounds, use these anchors:

| Score | Meaning | Example |
|-------|---------|---------|
| 10 | Perfect, can't improve | Apple.com product page level |
| 9 | Excellent, minor nitpicks only | Stripe dashboard, Linear UI |
| 8 | Very good, 1-2 noticeable issues | Well-designed SaaS landing page |
| 7 | Good, several things to improve | Decent Bootstrap template |
| 6 | Okay, clearly amateur | Generic HTML template |
| 5 | Below average, multiple problems | Unstyled HTML with some CSS |
| 4 | Poor | Broken layout, wrong colors |
| 3 | Bad | Barely functional |
| 1-2 | Broken | Doesn't render or unusable |

## Invariants (Never Break These)

1. Git repo is always in a working state — don't push broken examples
2. SKILL.md stays under 5,000 words
3. All top-level JS uses `var`
4. Class-based theming only (no @media prefers-color-scheme for CSS vars)
5. Content visible by default (no hidden-by-CSS for print/screenshot)
6. Every fix goes into SKILL.md or references, not just individual files
7. Plugin structure stays valid (.claude-plugin/plugin.json + skills/visualize/)
