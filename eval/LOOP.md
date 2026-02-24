# The Improvement Loop

How to systematically improve the Visualize skill to viral quality.

## The Ralph Loop (Generate → Evaluate → Fix → Repeat)

```
┌─────────────────────────────────────────┐
│                                         │
│   1. GENERATE                           │
│   Run 5-10 stress tests                 │
│   from stress-tests.md                  │
│           │                             │
│           ▼                             │
│   2. EVALUATE                           │
│   Score each output (eval skill)        │
│   Log in eval-results.md                │
│           │                             │
│           ▼                             │
│   3. ANALYZE                            │
│   Find SYSTEMIC patterns:               │
│   - Same issue across tests?            │
│   - Specific type struggling?           │
│   - Missing guidance in SKILL.md?       │
│           │                             │
│           ▼                             │
│   4. FIX THE SKILL (not the output)     │
│   Update SKILL.md, references,          │
│   or templates to fix the ROOT CAUSE    │
│           │                             │
│           ▼                             │
│   5. RE-RUN failed tests                │
│   Did the skill-level fix work?         │
│   Score improved?                       │
│           │                             │
│     ┌─────┴─────┐                       │
│     │           │                       │
│   < 8.5      ≥ 8.5                      │
│     │           │                       │
│     ▼           ▼                       │
│   Loop back   Next batch                │
│   to Step 4   of tests                  │
│                                         │
└─────────────────────────────────────────┘
```

## Key Principle: Fix the SKILL, Not the Output

When a test scores low, DON'T just fix that one HTML file. Ask:
- **Why** did the skill produce this? What instruction was missing?
- **Would** this same issue happen for a different prompt?
- **How** can I change SKILL.md or references to prevent this systemically?

Examples:
- ❌ "This chart is too small" → manually resize the chart
- ✅ "Charts default too small" → add "Charts: minimum 60% of container width, 300px height" to SKILL.md

- ❌ "This slide has too much text" → manually trim text
- ✅ "Slides allow too much text" → add "Hard limit: 40 words per slide. If more, split or use visuals" to SKILL.md

## Batch Strategy

### Batch 1: Core Types (T01, T06, T11, T16, T20)
One test per major type. Establishes baseline. Fix systemic issues before going deeper.

### Batch 2: Deck Deep-Dive (T02, T03, T04, T05, T07, T08)
Slides are the most common use case. Make them bulletproof.

### Batch 3: Data Visualizations (T12, T15, T27, T28, T29, T30, T38)
Data ingestion and chart rendering. The "killer feature" batch.

### Batch 4: Edge Cases (T31, T32, T33, T34, T35, T36, T37)
Break it. Find the limits. Harden.

### Batch 5: Wow Tests (T19, T21, T40)
The viral quality tests. These determine if the skill is ready for launch.

## When to Ship

All 40 tests scored. Results meet:
- **Average overall ≥ 8.5**
- **No test below 7.0**
- **"Wow" tests (T08, T40) ≥ 9.0**
- **All 5 dimensions average ≥ 8.0**

## Tracking

After each batch, update:
1. `eval-results.md` — scores and notes
2. `SKILL.md` — skill improvements
3. `references/` — new patterns or fixes
4. `CHANGELOG.md` — what changed and why

This creates a clear paper trail of how the skill evolved from v0 to viral-ready.
