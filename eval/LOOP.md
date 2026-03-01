# Visualize Improvement Loop (v4 — Real Skill Invocation)

The git repo (`https://github.com/careerhackeralex/visualize`) is the **source of truth**.
Every iteration clones fresh, installs the skill via Claude Code, generates visualizations by invoking the skill, and evaluates the real output.

## Architecture

```
Cron fires (hourly)
  └── Isolated sub-agent starts
        │
        ├── Step 0: Clone fresh from git
        ├── Step 1: Check state (skip if SHIP/VIRAL)
        ├── Step 2: Validate plugin structure
        ├── Step 3: Generate — invoke Claude Code with the skill to produce outputs
        ├── Step 4: Evaluate — screenshot + score the generated outputs
        ├── Step 5: Analyze — root cause analysis
        ├── Step 6: Fix SKILL.md ⭐ (most important)
        ├── Step 7: Fix references (skeleton, design-system, etc.)
        ├── Step 8: Re-generate — rebuild from updated skill to verify fixes
        ├── Step 9: Simplify — reduce complexity
        ├── Step 10: Validate — re-screenshot, console check
        ├── Step 11: Commit & push to git
        └── Step 12: Report to Alex via WhatsApp
```

## Steps in Detail

### Step 0: Clone Fresh
```bash
WORK_DIR=$(mktemp -d)
cd "$WORK_DIR"
git clone https://github.com/careerhackeralex/visualize.git
cd visualize
```

### Step 1: Check State
- Read `eval/loop-state.json`
- If gate is SHIP or VIRAL → report status, exit
- If `loopsSinceResearch >= 5` AND score plateau → research phase

### Step 2: Validate Plugin Structure
```bash
claude plugin validate .
```
Must pass. Also verify:
- `.claude-plugin/plugin.json` — valid JSON, has name + version
- `skills/visualize/SKILL.md` — valid YAML frontmatter, < 5000 words
- `skills/visualize/references/` — all expected files present

### Step 3: Generate ⭐⭐ (The Real Test)
**This is the critical new step.** Instead of evaluating pre-made examples, we invoke the skill through Claude Code and evaluate what it actually produces.

Create a temp output directory:
```bash
mkdir -p "$WORK_DIR/outputs"
```

For each test prompt from `eval/stress-tests.md` (pick 5-8 diverse ones per round):
```bash
cd "$WORK_DIR/outputs"
claude -p \
  --plugin-dir "$WORK_DIR/visualize" \
  --dangerously-skip-permissions \
  --allow-dangerously-skip-permissions \
  --model sonnet \
  "{test prompt}. Save as {filename}.html"
```

**Test prompt selection strategy:**
- Always include 1 slide deck, 1 dashboard, 1 infographic, 1 timeline
- Rotate through other types (cheatsheet, comparison, flowchart, etc.)
- Include 1 non-English prompt (Korean, Japanese, etc.)
- Include 1 "messy real-world data" prompt

**What we're testing:**
- Does the skill trigger correctly?
- Does Claude Code follow SKILL.md instructions?
- Does the output use the skeleton (dark theme, menu, Inter font)?
- Is the output quality actually good?

### Step 4: Evaluate
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

Use the calibration rubric:
| Score | Meaning | Benchmark |
|-------|---------|-----------|
| 10 | Perfect | Apple.com product page |
| 9 | Excellent | Stripe dashboard, Linear UI |
| 8 | Very good | Well-designed SaaS landing page |
| 7 | Good | Decent Bootstrap template |
| 6 | Okay | Generic HTML template |
| 5 | Below average | Unstyled HTML with some CSS |

Write results to `eval/eval-round{N}-raw.md`.

### Step 5: Analyze
Read all scores and identify:
1. **Weakest dimensions** across all generated files
2. **Worst outputs** — which prompts produced bad results?
3. **Recurring patterns** — same issue in 3+ outputs = systemic SKILL.md problem
4. **Skill compliance** — did Claude Code actually follow SKILL.md? If not, the instruction is unclear.
5. **Root cause** — trace every issue to a specific SKILL.md instruction (missing, unclear, wrong, buried)

Tag each fix: `SKILL` / `REF` / `SKELETON`

### Step 6: Fix SKILL.md ⭐ (Most Important Step)
Read `skills/visualize/SKILL.md` carefully. For each issue:
- Missing instruction? → Add it with concrete examples
- Unclear instruction? → Rewrite with specifics ("use 2rem" not "use appropriate sizing")
- Too verbose / buried? → Simplify, move up
- Claude Code ignored it? → Make it more prominent, add "CRITICAL:" prefix
- Contradictory? → Resolve the conflict

Rules:
- Keep under **5,000 words**
- Every instruction must be **testable**
- Add **anti-patterns** for common mistakes
- Add **examples** of what good output looks like

### Step 7: Fix References
Update `skills/visualize/references/` as needed:
- `skeleton.md` (highest priority — every output starts here)
- `design-system.md`
- `types.md`, `menu.md`, `libraries.md`, `css-techniques.md`

### Step 8: Re-generate (Verify Fixes)
Re-run the **worst 2-3 prompts** from Step 3 using the updated skill:
```bash
cd "$WORK_DIR/outputs-fixed"
claude -p \
  --plugin-dir "$WORK_DIR/visualize" \
  --dangerously-skip-permissions \
  --allow-dangerously-skip-permissions \
  --model sonnet \
  "{same prompt}. Save as {filename}.html"
```
Compare before/after. The fixes should produce noticeably better output.

### Step 9: Simplify
For every modified file (SKILL.md, references, regenerated examples):
- Remove unused CSS rules
- Consolidate duplicate styles
- Replace JS with CSS where possible
- Remove dead code
- All top-level JS uses `var`

### Step 10: Validate
Re-open regenerated files in browser:
- Screenshot post-fix
- Zero console errors
- Both themes work
- Menu works (theme toggle, PNG download, print)

### Step 11: Commit & Push
Copy improved outputs to `examples/` (replace existing or add new):
```bash
git add -A
git commit -m "eval: round {N} — avg {score} ({delta}), gate {GATE}

Key SKILL.md changes:
- {change 1}
- {change 2}

Generated via: claude -p --plugin-dir . --model sonnet
Weakest: {dim} ({score}), Strongest: {dim} ({score})"
git push origin main
```

### Step 12: Report
Send WhatsApp to Alex (+16507097191):
- Round number and gate
- Average score and delta
- Per-dimension averages
- Top 3 SKILL.md changes
- Before/after comparison for worst file
- Git commit hash

## Research Phase
Triggered when: `loopsSinceResearch >= 5` AND score plateau.
1. Web search latest CSS/visualization techniques
2. Study award-winning designs (Stripe, Linear, Apple)
3. Analyze: what makes Gamma/Canva output look professional?
4. Document in `research/round{N}-research.md`
5. Update SKILL.md + references
6. Reset `loopsSinceResearch = 0`

## Test Prompts (rotate through these)

### Core (always include 1-2)
- "Create a pitch deck for an AI startup called NeuralChef"
- "Build a dashboard showing SaaS metrics: MRR $450K, churn 2.1%, NPS 72"
- "Make an infographic about remote work trends in 2024"
- "Create a timeline of 5 major AI milestones from 2012-2024"

### Rotation
- "Build a git commands cheat sheet for beginners"
- "Compare React vs Vue vs Svelte in a visual comparison"
- "Create a flowchart of a CI/CD pipeline"
- "AI 스타트업 피치덱을 만들어줘" (Korean)
- "Visualize this data as a dashboard: Q1 revenue $1.2M, Q2 $1.5M, Q3 $1.8M, Q4 $2.1M, expenses $800K/quarter"
- "Create a status report for Project Phoenix: 73% complete, 12 tasks done, 4 in progress, 2 blocked"
- "Make a carousel infographic about 5 productivity tips"
- "Create an event poster for a tech conference called AI Summit 2024"

## Quality Gates

| Gate | Avg | Min | Meaning |
|------|-----|-----|---------|
| VIRAL | ≥ 9.5 | all ≥ 9 | Screenshot-worthy |
| SHIP | ≥ 9.0 | all ≥ 8 | Ready for public |
| ACCEPTABLE | ≥ 8.0 | all ≥ 7 | Functional, decent |
| NEEDS WORK | ≥ 7.0 | or any < 7 | Keep iterating |
| FAIL | < 7.0 | or any < 5 | Significant issues |

## Invariants (Never Break These)

1. Git repo always in working state — don't push broken examples
2. SKILL.md stays under 5,000 words
3. All top-level JS uses `var`
4. Class-based theming only (no @media prefers-color-scheme for CSS vars)
5. Content visible by default
6. Every fix goes into SKILL.md or references, not just individual files
7. Plugin structure stays valid
8. **Generated outputs must come from actual skill invocation, not hand-crafted**
