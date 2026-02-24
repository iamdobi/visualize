---
name: visualize
description: >
  Create beautiful, self-contained HTML visualizations from any content or idea.
  Use for: slide decks, presentations, infographics, dashboards, flowcharts, diagrams,
  timelines, comparison tables, data visualizations, landing pages, one-pagers, org charts,
  mind maps, process flows, kanban boards, report summaries, or any visual that helps
  humans digest information faster. Trigger on requests like "visualize this," "make a deck,"
  "create a slide," "build an infographic," "show me a dashboard," "make this visual,"
  or any request to present information in a visual HTML format.
---

# Visualize

Turn any idea, data, or content into a stunning single-file HTML visualization.

## Core Principles

1. **Single-file HTML** — everything inline (CSS, JS, SVG). Zero external dependencies. Opens in any browser.
2. **Beautiful by default** — modern design, generous whitespace, professional typography, subtle animations.
3. **Content-first** — the visualization serves the message. Never sacrifice clarity for aesthetics.
4. **Responsive** — works on desktop and mobile unless explicitly a fixed-dimension format (e.g., 16:9 slides).

## Philosophy

HTML is not a "website" — it's a visualization tool. Code is cheap. Everyone should feel empowered to visualize anything. This skill turns conversation context, URLs, articles, data, or raw ideas into something visual and digestible in seconds.

Users invoke this **mid-conversation** with Claude Code. Use the full conversation context — whatever they've been discussing, any links they've shared, any data they've pasted — as source material. When given a URL, crawl it and extract the content to visualize.

## Output Rules

- Write ONE `.html` file to the working directory (or user-specified path)
- Filename: descriptive kebab-case, e.g., `q4-revenue-dashboard.html`, `team-roadmap-deck.html`
- All custom styles in `<style>` — no external CSS
- **CDN libraries are encouraged** — use the best tool for the job:
  - **Chart.js** — bar, line, pie, radar, polar charts (simple, beautiful defaults)
  - **D3.js** — complex/custom data visualizations, force graphs, maps
  - **Three.js** — 3D visualizations when appropriate
  - **Mermaid** — flowcharts, sequence diagrams, Gantt charts from text definitions
  - **Reveal.js** — when a full-featured slide deck engine is needed
  - **Leaflet** — maps and geospatial data
  - Any well-known library via CDN that makes the output better
- Use `<script src="https://cdn.jsdelivr.net/npm/...">` for libraries
- Inline custom JS in `<script>` after library loads
- SVG for icons and simple graphics
- Use CSS Grid/Flexbox for layout, CSS custom properties for theming
- Prefer CSS animations over JS when possible

## Design System

Apply these defaults unless the user specifies otherwise:

### Typography
- System font stack: `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
- Monospace: `'SF Mono', 'Fira Code', 'Consolas', monospace`
- Generous line-height (1.5–1.7 for body, 1.1–1.3 for headings)
- Clear hierarchy: use font size, weight, and color — not just bold

### Color
- Default palette: dark text on light background with one accent color
- Use HSL for easy theming: define `--hue` and derive all colors
- Ensure WCAG AA contrast (4.5:1 minimum)
- Support `prefers-color-scheme: dark` when appropriate

### Spacing
- Use 8px grid system (multiples of 0.5rem)
- Generous padding: never let content touch edges
- Breathing room between sections

### Visual Polish
- Subtle shadows (`box-shadow: 0 1px 3px rgba(0,0,0,0.1)`)
- Rounded corners (`border-radius: 8px–12px`)
- Smooth transitions (`transition: all 0.2s ease`)
- Subtle gradients over flat colors when appropriate

## Hamburger Menu (Required)

Every visualization MUST include a hamburger menu (☰) fixed in the top-right corner with:
1. **Theme toggle** — cycle between Dark / Light / Auto modes
2. **Download as PNG** — export via `html-to-image` library (2x retina quality)
3. **Print / Save PDF** — triggers `window.print()` with optimized `@media print` styles

See [references/menu.md](references/menu.md) for the complete implementation (HTML + CSS + JS), theme CSS pattern, print styles, and slide deck special handling. Copy this component into every output.

Required CDN: `https://cdn.jsdelivr.net/npm/html-to-image@1.11.11/dist/html-to-image.js`

Key requirements:
- Frosted glass backdrop-filter on the menu
- Smooth open/close animation (scale + opacity)
- Close on outside click and Escape key
- Theme persisted to localStorage
- Hide menu/nav during image capture
- `print-color-adjust: exact` for faithful PDF output
- For slide decks: export captures current slide only; print outputs all slides with page breaks

## Libraries

Use CDN libraries freely. See [references/libraries.md](references/libraries.md) for CDN links, patterns, and tips for Chart.js, D3.js, Three.js, Mermaid, Reveal.js, and Leaflet.

## Visualization Types

Choose the right format based on the request. See [references/types.md](references/types.md) for detailed patterns and examples for each type.

### Quick Reference
| Type | When to Use |
|------|-------------|
| **Slide Deck** | Presentations, pitches, sequential storytelling |
| **Infographic** | Summarizing data/concepts in a single scrollable visual |
| **Dashboard** | Metrics, KPIs, real-time-style data displays |
| **Flowchart/Diagram** | Processes, decision trees, system architecture |
| **Timeline** | Chronological events, roadmaps, project milestones |
| **Comparison** | Side-by-side features, pros/cons, options analysis |
| **Data Viz** | Charts, graphs, data stories (use SVG, not canvas) |
| **One-Pager** | Landing pages, summaries, briefs |
| **Mind Map** | Brainstorming, concept relationships |
| **Kanban/Board** | Status tracking, categorized items |

## Slide Deck Specifics

Slide decks are the most common request. Get these right:

- Fixed 16:9 aspect ratio (1280×720 viewport)
- Keyboard navigation (← →) and click/tap navigation
- Slide counter (e.g., "3 / 12")
- Smooth transitions between slides (CSS transforms)
- Title slide, content slides, section dividers, closing slide
- Max 6–8 bullet points per slide; prefer visuals over text
- Speaker notes support via `data-notes` attribute (hidden, printable)

## Process

1. **Understand** — what's the message? Who's the audience? What format fits best?
2. **Structure** — outline the content/sections before coding
3. **Build** — write the complete HTML file
4. **Verify** — mentally review: Is it readable? Is the hierarchy clear? Would YOU present this?

## Context Awareness

This skill is used mid-conversation. Leverage everything available:

- **Conversation context** — summarize, structure, or visualize what's been discussed
- **URLs/links** — crawl and extract content, then visualize the key information
- **Pasted data** — CSV, JSON, tables, lists → charts, dashboards, infographics
- **Ideas/concepts** — turn abstract discussions into visual diagrams or decks
- **Code/architecture** — visualize system designs, data flows, API structures

Always use real content from the conversation. Never generate placeholder data when real context exists.

## Anti-Patterns

- ❌ Walls of text — if it looks like a document, it's not a visualization
- ❌ Tiny fonts — minimum 14px body, 18px+ for presentations
- ❌ Rainbow colors — stick to 2-3 colors max
- ❌ Placeholder content — use real data from conversation, never "Lorem ipsum"
- ❌ Over-engineering — pick the simplest approach that looks great

## Advanced Features (use when appropriate)

- **Print-friendly**: Add `@media print` styles for clean printing
- **Animations**: Entrance animations for slide elements, micro-interactions for dashboards
- **Interactivity**: Tooltips, hover states, expandable sections, filters for dashboards
- **Export hints**: Include a "Save as PDF" note for slide decks (Cmd+P → Save as PDF)
- **Embedding**: Data can be embedded as JSON in a `<script>` tag for data-driven visualizations
