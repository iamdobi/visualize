# Visualize Improvement Loop (Ralph Loop v2)

## The Cycle

Every iteration runs these 4 phases in order:

### Phase 1: Evaluate
- Spawn fresh evaluator (zero prior context)
- Score all examples against 8 dimensions
- Benchmark: Apple keynotes, Stripe, NYT interactive, Vercel
- Standards increase each round (scores that passed last round may not pass this round)
- Write results to `eval/eval-round{N}-raw.md`

### Phase 2: Plan
- Read eval results, identify top issues (bugs > visual > interactivity > polish)
- Categorize: CRITICAL (broken), HIGH (visible quality gap), MEDIUM (polish), LOW (nice-to-have)
- Fix the SKILL.md / references, not just individual files
- Plan should simplify code, not add complexity

### Phase 3: Build
- Fix SKILL.md skeleton/references first (systemic fixes)
- Regenerate all examples from updated skeleton
- Simplify: fewer lines of JS, more CSS, fewer libraries
- Every fix must make code simpler OR the same complexity, never more complex

### Phase 4: Validate
- Open each file in browser, screenshot, check console for errors
- Verify: both themes work, menu works, print CSS present, animations fire
- Quick smoke test before next eval round

### Research Gate (every ~5 loops)
When scores plateau (avg improvement < 0.3 between rounds), run deep research:
- Study latest CSS/animation techniques
- Analyze top-rated data viz sites
- Look for new CDN libraries or patterns
- Update references/ with findings
- Then resume the loop

## Quality Gates
- 🚀 VIRAL: ≥9.5 overall, all ≥9 → STOP: ship and promote
- ✅ SHIP: ≥9.0 overall, all ≥8 → STOP: push to GitHub, announce
- ⚠️ ACCEPTABLE: ≥8.0 overall, all ≥7 → CONTINUE looping
- 🔧 NEEDS WORK: ≥7.0 or any <7 → CONTINUE looping (prioritize failures)
- ❌ FAIL: <7.0 or any <5 → CONTINUE looping (fix critical bugs first)

## State Tracking
Track loop state in `eval/loop-state.json`:
```json
{
  "currentRound": 4,
  "loopsSinceResearch": 1,
  "lastAverage": 7.54,
  "gate": "NEEDS WORK",
  "history": [
    { "round": 1, "avg": 6.40, "gate": "FAIL" },
    { "round": 2, "avg": 7.41, "gate": "NEEDS WORK" },
    { "round": 3, "avg": 7.54, "gate": "NEEDS WORK" }
  ]
}
```
