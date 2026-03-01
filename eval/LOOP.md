# Visualize Improvement Loop (v2 — Git-First)

The git repo (`https://github.com/careerhackeralex/visualize`) is the **source of truth**.
Every loop iteration clones fresh from git, works in a temp directory, and pushes results back.

## Loop Steps

### 0. Setup — Clone Fresh
```bash
# Clone repo to temp working directory
WORK_DIR=$(mktemp -d)
cd "$WORK_DIR"
git clone https://github.com/careerhackeralex/visualize.git
cd visualize
```
- NEVER work directly in the workspace copy
- Always start from the latest git state
- This ensures the loop tests what users would actually get

### 1. Check State
- Read `eval/loop-state.json` for current round, scores, gate
- If gate is SHIP or VIRAL → skip (report status, exit)
- If `loopsSinceResearch >= 5` AND avg improved < 0.3 last round → do research phase instead

### 2. Install & Verify
- Verify the plugin structure is correct:
  - `.claude-plugin/plugin.json` exists and is valid JSON
  - `skills/visualize/SKILL.md` exists with valid YAML frontmatter
  - `skills/visualize/references/` has all expected files
- Open each example in browser, check for console errors
- This catches structural issues before scoring

### 3. Evaluate
- Spawn evaluator sub-agent (label: `eval-round-{N}`)
- Open each file in `examples/` in browser (profile=openclaw)
- Screenshot EVERY file in dark AND light theme
- Save screenshots to `eval/screenshots/round{N}/`
- Score all 8 dimensions per file
- Write results to `eval/eval-round{N}-raw.md`

### 4. Plan
- Read eval results, identify top 5 issues
- Categorize: systemic (fix SKILL.md/references) vs local (fix specific examples)
- Always fix systemic issues first — they prevent the same bug across all outputs

### 5. Build
- Apply fixes to `skills/visualize/SKILL.md` and `skills/visualize/references/`
- Regenerate affected examples from the updated skill
- Simplify code — fewer lines, more CSS, less JS
- Spawn sub-agent (label: `regen-round-{N}`) if needed

### 6. Validate
- Open each modified file in browser
- Screenshot post-fix state
- Check console for errors
- Compare before/after scores if possible

### 7. Commit & Push
```bash
git add -A
git commit -m "eval: round {N} — avg {score}, gate {GATE}

- {summary of changes}
- {key fixes applied}"
git push origin main
```
- ALL changes go through git — screenshots, eval results, skill fixes, example updates
- Clean atomic commits with descriptive messages

### 8. Update State
- Update `eval/loop-state.json` with new round, scores, gate
- Increment `loopsSinceResearch`
- This is part of the commit in step 7

### 9. Report
- Send Alex a WhatsApp summary: round number, scores, gate, key changes, trend
- Reference the git commit hash

## Research Phase (when triggered)
1. Web search for latest CSS/HTML/visualization techniques
2. Study award-winning data visualizations, design systems
3. Save findings to `research/` directory
4. Update `skills/visualize/SKILL.md` and references with new techniques
5. Reset `loopsSinceResearch = 0`
6. Commit & push research findings

## Quality Gates
- **SHIP** ≥9.0 avg (all ≥8) — ready for public use
- **VIRAL** ≥9.5 avg (all ≥9) — screenshot-worthy
- **ACCEPTABLE** ≥8.0 avg (all ≥7) — functional, decent
- **NEEDS WORK** ≥7.0 avg or any <7 — keep iterating
- **FAIL** <7.0 avg or any <5 — significant issues

## Rules
- Fix the SKILL, not just the output — every fix goes into SKILL.md/references
- The git repo is what users clone — it must always be in a working state
- Don't commit broken examples
- Simplify: fewer lines, more CSS, less JS
- Content visible by default (no hidden-by-CSS)
