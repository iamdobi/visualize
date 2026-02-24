# Visualization Evaluation Framework

Systematic quality evaluation for generated HTML visualizations. Used by the `visualize-eval` skill to score outputs and drive iterative improvement.

## Evaluation Dimensions (10-point scale each)

### 1. Visual Design (weight: 25%)
- **Typography** — Hierarchy clear? Sizes appropriate? Line-height comfortable? Max 2 fonts?
- **Color** — Harmonious palette? WCAG AA contrast? Max 3 colors + neutrals? Dark/light both work?
- **Spacing** — Consistent rhythm? Nothing cramped? Generous breathing room?
- **Polish** — Subtle shadows? Rounded corners? Smooth transitions? Professional feel?
- **Score 9-10:** Could be in a design portfolio. Looks like a professional designer made it.
- **Score 7-8:** Clean and professional. Minor spacing or color issues.
- **Score 5-6:** Acceptable but generic. Default-looking.
- **Score 1-4:** Ugly, cramped, or broken visually.

### 2. Content Effectiveness (weight: 25%)
- **Clarity** — Is the message immediately obvious? Can you understand it in 5 seconds?
- **Information density** — Right amount of content? Not too sparse, not overwhelming?
- **Hierarchy** — Most important info stands out? Clear reading order?
- **Data accuracy** — Charts/numbers correct? Labels clear? Units shown?
- **No filler** — Zero placeholder text? All content meaningful?
- **Score 9-10:** Instantly digestible. A non-expert could understand the key message.
- **Score 7-8:** Clear with minor ambiguities.
- **Score 5-6:** Requires effort to parse. Some confusion.
- **Score 1-4:** Misleading, confusing, or mostly filler.

### 3. Technical Quality (weight: 20%)
- **Self-contained** — Single file? No broken external refs?
- **Performance** — Loads fast? No unnecessary JS? Efficient CSS?
- **Responsive** — Works at 1280px? 768px? 375px? (unless fixed-format like slides)
- **Browser compat** — Works in Chrome, Safari, Firefox?
- **Accessibility** — Semantic HTML? Sufficient contrast? Keyboard navigable?
- **Print** — `@media print` styles work? PDF output clean?
- **Score 9-10:** Production-grade. Zero console errors. Accessible.
- **Score 7-8:** Works well, minor issues (e.g., one breakpoint slightly off).
- **Score 5-6:** Functional but has noticeable issues.
- **Score 1-4:** Broken layout, console errors, or missing features.

### 4. Interactivity & UX (weight: 15%)
- **Menu** — Hamburger menu present? Theme toggle works? Download works? Print works?
- **Navigation** — (Slides) Keyboard, click, swipe all work? Progress indicator?
- **Hover states** — Interactive elements have feedback?
- **Animations** — Smooth? Purposeful? Not distracting?
- **Accessibility** — Focus states? `prefers-reduced-motion` respected?
- **Score 9-10:** Delightful interactions. Everything responsive and smooth.
- **Score 7-8:** All features work, minor polish missing.
- **Score 5-6:** Basic interactivity works, some features missing.
- **Score 1-4:** Broken interactions or missing required features.

### 5. Wow Factor (weight: 15%)
- **First impression** — Does it make you go "wow" in the first 2 seconds?
- **Shareability** — Would someone screenshot this and share it?
- **Memorability** — Would you remember this a day later?
- **Professionalism** — Could this be used in a real meeting/presentation?
- **Differentiation** — Does it look noticeably better than a typical PowerPoint/Canva output?
- **Score 9-10:** Jaw-dropping. People would ask "how did you make this?"
- **Score 7-8:** Impressive. Clearly better than typical tools.
- **Score 5-6:** Fine but forgettable. Comparable to standard tools.
- **Score 1-4:** Underwhelming. Worse than what you'd get from Gamma/Canva.

## Overall Score Calculation

```
overall = (visual × 0.25) + (content × 0.25) + (technical × 0.20) + (interactivity × 0.15) + (wow × 0.15)
```

### Quality Gates
- **Ship-ready (viral potential):** Overall ≥ 8.5, no dimension below 7
- **Good (publishable):** Overall ≥ 7.5, no dimension below 6
- **Needs work:** Overall ≥ 6.0 or any dimension below 6
- **Fail:** Overall < 6.0

## Evaluation Process

1. **Open the HTML** in a browser at 1280×720 (default) and 375×667 (mobile)
2. **5-second test** — What's your first impression? Can you grasp the message?
3. **Interactive test** — Click through all navigation, try theme toggle, test download/print
4. **Technical test** — Check console for errors, verify responsiveness, test print preview
5. **Score each dimension** with specific notes on what's good and what needs fixing
6. **Generate fix list** — Prioritized list of concrete changes to improve the score
7. **Re-evaluate** after fixes until quality gate is met

## Common Issues & Fixes

| Issue | Impact | Fix |
|-------|--------|-----|
| Text too small | Content -2 | Min 14px body, 20px+ headings |
| Colors clash | Visual -3 | Regenerate with single --hue base |
| No breathing room | Visual -2 | Add padding, increase gaps |
| Chart labels overlap | Content -2 | Rotate labels, reduce data points |
| Menu missing | Interactivity -4 | Add standard menu component |
| Print breaks layout | Technical -2 | Add @media print styles |
| Animations janky | Wow -2 | Use CSS transforms, not top/left |
| Dark mode broken | Technical -2 | Test all CSS vars in both themes |
| Too much text per slide | Content -3 | Max 6 bullets, use visuals |
| Placeholder content | Content -5 | Use real data, never lorem ipsum |
