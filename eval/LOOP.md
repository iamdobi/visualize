# Visualize Improvement Loop (v5 — Install & Invoke)

The git repo (`https://github.com/careerhackeralex/visualize`) is the **source of truth**.
Every iteration installs the plugin from GitHub, invokes it through Claude Code, evaluates real output, fixes the skill, and pushes improvements back.

## Architecture

```
Cron fires (hourly)
  └── Isolated sub-agent starts
        │
        ├── Step 0: Install plugin from GitHub
        ├── Step 1: Check state (skip if SHIP/VIRAL)
        ├── Step 2: Generate — invoke skill via Claude Code CLI
        ├── Step 3: Evaluate — screenshot + score generated outputs
        ├── Step 4: Analyze — root cause, trace to SKILL.md
        ├── Step 5: Uninstall plugin
        ├── Step 6: Clone repo, fix SKILL.md + references
        ├── Step 7: Push fixes to git
        ├── Step 8: Re-install from git (gets updated version)
        ├── Step 9: Re-generate worst prompts to verify fixes
        ├── Step 10: Validate — screenshot, console check
        ├── Step 11: Commit final results & push
        └── Step 12: Cleanup & report
```

## Steps in Detail

### Step 0: Install Plugin from GitHub
```bash
# Add marketplace (if not already added)
claude plugin marketplace add careerhackeralex/visualize

# Install the plugin
claude plugin install visualize@careerhackeralex
```
This is exactly what a real user does. We test what they get.

### Step 1: Check State
```bash
# Clone repo separately just to read state
WORK_DIR=$(mktemp -d)
cd "$WORK_DIR"
git clone https://github.com/careerhackeralex/visualize.git
```
- Read `eval/loop-state.json`
- If gate is SHIP or VIRAL → report status, cleanup, exit
- If `loopsSinceResearch >= 5` AND score plateau → research phase

### Step 2: Generate ⭐⭐ (The Real Test)
Create a temp output directory and invoke the skill through Claude Code:
```bash
mkdir -p "$WORK_DIR/outputs"
cd "$WORK_DIR/outputs"
```

For each test prompt (pick 5-8 diverse ones from stress-tests.md):
```bash
claude -p \
  --dangerously-skip-permissions \
  --allow-dangerously-skip-permissions \
  --model sonnet \
  "{test prompt}. Save as {filename}.html"
```

**No `--plugin-dir`.** The skill is installed as a real plugin. Claude Code discovers it automatically, just like a real user.

**Test prompt selection — always include:**
- 1 slide deck / presentation
- 1 dashboard with data
- 1 infographic / visual storytelling
- 1 timeline
- 1 non-English (Korean, Japanese, etc.)
- 2-3 rotating types (cheatsheet, comparison, flowchart, poster, carousel, etc.)

### Step 3: Evaluate
Open every generated file in browser (profile=openclaw):
- Screenshot each in **dark** and **light** theme
- Save to `eval/screenshots/round{N}/`
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

Write results to `eval/eval-round{N}-raw.md`.

**Calibration anchors (use these to stay consistent):**
| Score | Benchmark |
|-------|-----------|
| 10 | Apple.com product page |
| 9 | Stripe dashboard, Linear UI |
| 8 | Well-designed SaaS landing page |
| 7 | Decent Bootstrap template |
| 6 | Generic HTML template |
| 5 | Unstyled HTML with some CSS |

### Step 4: Analyze
Don't jump to fixes. Think first:
1. **Weakest dimensions** across all outputs
2. **Worst outputs** — which prompts produced bad results?
3. **Skill compliance** — did Claude Code actually follow SKILL.md? If not, WHY?
4. **Root cause** — trace every issue to a specific SKILL.md instruction (missing, unclear, wrong, buried, contradictory)
5. **Tag each fix:** `SKILL` / `REF:skeleton` / `REF:design-system` / `REF:other`

### Step 5: Uninstall Plugin
```bash
claude plugin uninstall visualize@careerhackeralex
```
Clean slate before we make fixes.

### Step 6: Fix SKILL.md + References ⭐
Work in the cloned repo from Step 1 (`$WORK_DIR/visualize`).

**SKILL.md (most important):**
- Add missing instructions with concrete examples
- Clarify vague instructions ("use 2rem" not "use appropriate sizing")
- Add anti-patterns ("DON'T: gradient text on headings")
- Simplify verbose instructions
- Make ignored instructions more prominent ("CRITICAL:" prefix)
- Keep under **5,000 words**

**References (priority order):**
1. `skeleton.md` — the HTML template, affects every output
2. `design-system.md` — typography, colors, spacing
3. `types.md`, `menu.md`, `libraries.md`, `css-techniques.md`

**Simplify everything:**
- Remove unused CSS rules
- Consolidate duplicates
- Replace JS with CSS where possible
- All top-level JS uses `var`

### Step 7: Push Fixes to Git
```bash
cd "$WORK_DIR/visualize"
git add -A
git commit -m "eval: round {N} fixes — {summary of SKILL.md changes}"
git push origin main
```

### Step 8: Re-install from Git
```bash
# Update marketplace to get latest
claude plugin marketplace update careerhackeralex

# Re-install (gets the fixed version)
claude plugin install visualize@careerhackeralex
```
Now the installed plugin has our fixes.

### Step 9: Re-generate (Verify Fixes)
Re-run the **worst 2-3 prompts** from Step 2:
```bash
cd "$WORK_DIR/outputs-fixed"
claude -p \
  --dangerously-skip-permissions \
  --allow-dangerously-skip-permissions \
  --model sonnet \
  "{same prompt}. Save as {filename}.html"
```
Compare before/after. Fixes should produce noticeably better output.

### Step 10: Validate
- Screenshot the re-generated files
- Zero console errors
- Both dark and light themes work
- Hamburger menu works (toggle, download, print)
- Save post-fix screenshots to `eval/screenshots/round{N}-fixed/`

### Step 11: Commit Final Results & Push
Copy good re-generated outputs to `examples/` if they're better than existing ones:
```bash
cd "$WORK_DIR/visualize"
# Copy improved outputs
cp "$WORK_DIR/outputs-fixed/"*.html examples/
git add -A
git commit -m "eval: round {N} — avg {score} ({delta}), gate {GATE}

Key SKILL.md changes:
- {change 1}
- {change 2}

Generated via: claude -p (installed plugin, sonnet)
Weakest: {dim} ({score}), Strongest: {dim} ({score})"
git push origin main
```

Update `eval/loop-state.json` in this commit.

### Step 12: Cleanup & Report
```bash
# Uninstall plugin
claude plugin uninstall visualize@careerhackeralex
claude plugin marketplace remove careerhackeralex

# Delete temp directory
rm -rf "$WORK_DIR"
```

Send WhatsApp to Alex (+16507097191):
- Round number and gate
- Average score and delta
- Per-dimension averages
- Top 3 SKILL.md changes made
- Before/after for worst file
- Git commit hash

## Research Phase
Triggered when: `loopsSinceResearch >= 5` AND score plateau (< 0.3 improvement over 3 rounds).

1. Web search latest CSS/visualization techniques
2. Study award-winning designs (Stripe, Linear, Apple)
3. Analyze Gamma/Canva — what makes their output look professional?
4. Document in `research/round{N}-research.md`
5. Update SKILL.md + references
6. Reset `loopsSinceResearch = 0`

## Test Prompts (from eval/stress-tests.md, rotate through)

### Core (always include 1-2)
- "Create a pitch deck for an AI startup called NeuralChef"
- "Build a dashboard showing SaaS metrics: MRR $450K, churn 2.1%, NPS 72"
- "Make an infographic about remote work trends in 2024"
- "Create a timeline of 5 major AI milestones from 2012-2024"

### Rotation
- "Build a git commands cheat sheet"
- "Compare React vs Vue vs Svelte visually"
- "Create a flowchart of a CI/CD pipeline"
- "AI 스타트업 피치덱을 만들어줘" (Korean)
- "Visualize quarterly revenue: Q1 $1.2M, Q2 $1.5M, Q3 $1.8M, Q4 $2.1M"
- "Create a status report for Project Phoenix: 73% complete"
- "Make a carousel about 5 productivity tips"
- "Create an event poster for AI Summit 2024"

## Quality Gates

| Gate | Avg | Min | Meaning |
|------|-----|-----|---------|
| VIRAL | ≥ 9.5 | all ≥ 9 | Screenshot-worthy |
| SHIP | ≥ 9.0 | all ≥ 8 | Ready for public |
| ACCEPTABLE | ≥ 8.0 | all ≥ 7 | Functional, decent |
| NEEDS WORK | ≥ 7.0 | or any < 7 | Keep iterating |
| FAIL | < 7.0 | or any < 5 | Significant issues |

## Invariants (Never Break These)

1. Git repo always in working state
2. SKILL.md under 5,000 words
3. All top-level JS uses `var`
4. Class-based theming only (no @media prefers-color-scheme)
5. Content visible by default
6. Every fix goes into SKILL.md or references
7. Plugin structure valid (`.claude-plugin/plugin.json` + `skills/visualize/`)
8. **All evaluated outputs generated by invoking the installed skill, never hand-crafted**
9. **Plugin installed from GitHub, not local path**
