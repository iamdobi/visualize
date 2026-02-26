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

1. **Single-file HTML** — one `.html` file with inline CSS/JS. Opens in any browser, works offline, emails easily.
2. **Dark theme by default** — modern, premium feel. Light theme always available via toggle.
3. **Beautiful by default** — the first output should look professional with zero iteration.
4. **Content-first** — the visualization serves the message. Never sacrifice clarity for aesthetics.
5. **Responsive** — works on desktop, tablet, and mobile unless explicitly fixed-dimension (e.g., 16:9 slides).

## Philosophy

HTML is not a "website" — it's a visualization tool. Code is cheap. Everyone should feel empowered to visualize anything. This skill turns conversation context, URLs, articles, data, or raw ideas into something visual and digestible in seconds.

Users invoke this **mid-conversation** with Claude Code. Use the full conversation context — whatever they've been discussing, any links they've shared, any data they've pasted — as source material. When given a URL, crawl it and extract the content to visualize.

## Output Rules

- Write ONE `.html` file to the working directory (or user-specified path)
- Filename: descriptive kebab-case, e.g., `q4-revenue-dashboard.html`, `team-roadmap-deck.html`
- All custom styles in `<style>` after CDN imports
- **CDN libraries are encouraged** — use the best tool for the job:
  - **Tailwind CSS** — `https://cdn.tailwindcss.com` (utility-first styling, use freely)
  - **Chart.js** — `https://cdn.jsdelivr.net/npm/chart.js` (bar, line, pie, radar, doughnut)
  - **D3.js** — `https://cdn.jsdelivr.net/npm/d3@7` (complex/custom data viz, force graphs)
  - **Mermaid** — `https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js` (flowcharts, sequence diagrams)
  - **Three.js** — 3D when appropriate
  - **Reveal.js** — full-featured slide engine when needed
  - **Leaflet** — maps and geospatial data
- SVG for icons and simple graphics — never use external image URLs unless user provides them
- Prefer CSS animations over JS when possible

See [references/libraries.md](references/libraries.md) for detailed CDN links, patterns, and tips.

## Design System

Apply these defaults. They are opinionated and tested — override only when user requests it.

### Typography
- **Primary font:** Inter via Google Fonts CDN — `https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap`
- **Monospace:** JetBrains Mono or system `'SF Mono', 'Fira Code', 'Consolas', monospace`
- **Fallback:** `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
- **Type scale (1.25 ratio):** 14 → 16 → 20 → 25 → 31 → 39 → 49px
- **Line-height:** 1.5–1.7 for body, 1.1–1.2 for headings
- **Max line width:** 65–75 characters for readability
- Use `clamp()` for fluid responsive sizing: `clamp(1rem, 2.5vw, 1.25rem)`

### Color System (Dark-First)

Default dark palette — all derived from CSS custom properties:
```css
:root, .theme-dark {
  --bg: #030712;           /* gray-950 */
  --surface: #111827;       /* gray-900 */
  --surface-hover: #1f2937; /* gray-800 */
  --border: rgba(255,255,255,0.1);
  --text: #f9fafb;          /* gray-50 */
  --text-secondary: #9ca3af; /* gray-400 */
  --accent: #3b82f6;        /* blue-500 */
  --accent-secondary: #8b5cf6; /* violet-500 */
  --positive: #10b981;      /* emerald-500 */
  --negative: #f43f5e;      /* rose-500 */
  --warning: #f59e0b;       /* amber-500 */
}
```

Light theme override:
```css
.theme-light {
  --bg: #f9fafb;
  --surface: #ffffff;
  --surface-hover: #f3f4f6;
  --border: rgba(0,0,0,0.1);
  --text: #111827;
  --text-secondary: #6b7280;
}
```

Chart color sequence: `#3b82f6, #8b5cf6, #ec4899, #f59e0b, #10b981, #06b6d4, #f43f5e`

### Spacing
- **8px grid** — all spacing in multiples: 4, 8, 12, 16, 24, 32, 48, 64, 96px
- **Generous padding** — `p-6` to `p-8` on cards, `px-8` on containers
- **Container:** `max-w-7xl mx-auto px-4 sm:px-6 lg:px-8`
- **Card gaps:** `gap-6` minimum

### Visual Polish
- **Rounded corners:** `rounded-2xl` (16px) for cards, `rounded-xl` (12px) for smaller elements
- **Shadows:** `shadow-lg` or `0 4px 24px rgba(0,0,0,0.15)` for depth
- **Glass morphism cards:** `backdrop-blur-md bg-white/5 border border-white/10 rounded-2xl`
- **Gradient accents:** `bg-gradient-to-r from-blue-500 to-purple-500` on key elements
- **Transitions:** `transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1)` (Material standard)

### Animations
- **Entrance:** fade + translateY(20px) with staggered delays (100-150ms apart)
- **Duration:** 300-600ms (shorter for small elements, longer for large)
- **Easing:** `cubic-bezier(0.4, 0, 0.2, 1)` for standard, `cubic-bezier(0.34, 1.56, 0.64, 1)` for spring/bounce
- **Scroll-triggered:** use IntersectionObserver for elements entering viewport
- **Respect:** always include `@media (prefers-reduced-motion: reduce)` to disable animations

## Hamburger Menu (Required)

Every visualization MUST include a hamburger menu (☰) fixed top-right with:
1. **Theme toggle** — cycle Dark / Light / Auto, persisted to localStorage
2. **Download as PNG** — via `html-to-image` CDN at 2x retina quality
3. **Print / Save PDF** — `window.print()` with optimized `@media print` styles

See [references/menu.md](references/menu.md) for the complete copy-paste implementation.

Required CDN: `https://cdn.jsdelivr.net/npm/html-to-image@1.11.11/dist/html-to-image.js`

Key: frosted glass style, smooth open/close, close on outside click + Escape, hide UI during capture, `print-color-adjust: exact`, slide decks export current slide only.

## Visualization Types

Choose the right format. See [references/types.md](references/types.md) for detailed patterns.

| Type | When to Use | Key Feature |
|------|-------------|-------------|
| **Slide Deck** | Presentations, pitches | 16:9, keyboard nav, transitions |
| **Infographic** | Data summaries, visual stories | Long scroll, big numbers, sections |
| **Dashboard** | Metrics, KPIs | Grid of cards + charts |
| **Flowchart** | Processes, architecture | Mermaid or SVG diagrams |
| **Timeline** | Chronological events | Alternating left/right, scroll-triggered |
| **Comparison** | Side-by-side analysis | Feature matrix, pros/cons |
| **Data Viz** | Charts, data stories | Chart.js or D3 |
| **One-Pager** | Summaries, briefs | Single viewport, print-friendly |
| **Mind Map** | Concept relationships | Radial SVG layout |
| **Kanban** | Status tracking | Column-based cards |

## Slide Deck Rules

Slides are the most common request. Get these right:

- **16:9 aspect ratio** — `100vw × 100vh`, content centered
- **One idea per slide** — if you need a second thought, make a second slide
- **Max 40 words per slide** — more than that, split or use visuals
- **Headlines max 6 words** — short, punchy, memorable
- **Big number + small label** for stat slides — number at 3-5rem, label at 0.875rem
- **Keyboard nav** — ← → arrows, Space, Enter
- **Touch nav** — swipe left/right
- **Click nav** — left third = prev, right two-thirds = next
- **Progress bar** — thin gradient bar at top showing position
- **Slide counter** — "3 / 12" in bottom nav
- **Smooth transitions** — `transform: translateX()` with 500ms cubic-bezier
- **Entrance animations** — elements within slides animate in with staggered delays
- **Speaker notes** — `data-notes` attribute, visible in print only

### Slide Types
1. **Title** — gradient background, big headline, subtitle. Center aligned.
2. **Content** — heading + bullets OR heading + visual. Never text-heavy.
3. **Section divider** — full-bleed accent color, section title only.
4. **Stat** — one big number, one label, one insight sentence.
5. **Chart** — Chart.js visualization with title and key takeaway.
6. **Two-column** — split layout for comparisons, text+visual.
7. **Quote** — large pull quote with attribution.
8. **Closing** — CTA, contact info, or summary + social links.

## Data Ingestion

When user provides data:
- **CSV** — parse with JS, auto-detect headers, render appropriate chart type
- **JSON** — extract keys as labels, values as data, nested objects as series
- **Tables** — convert to visual comparison or chart
- **Numbers in text** — extract and highlight as stat cards
- **URLs** — crawl, extract key info, visualize as summary

## Context Awareness

This skill is used mid-conversation. Leverage everything:

- **Conversation context** — summarize, structure, or visualize what's been discussed
- **URLs/links** — crawl and extract content, then visualize
- **Pasted data** — CSV, JSON, tables → charts, dashboards
- **Ideas/concepts** — turn abstract discussions into visual diagrams
- **Code/architecture** — visualize system designs, data flows

Always use real content. Never generate placeholder data when real context exists.

## Anti-Patterns

- ❌ Walls of text — if it reads like a document, it's not a visualization
- ❌ Tiny fonts — minimum 14px body, 20px+ for presentation headings
- ❌ Rainbow colors — stick to 2-3 colors from the palette + neutrals
- ❌ Placeholder content — never use "Lorem ipsum" or fake data
- ❌ Over-engineering — simplest approach that looks stunning
- ❌ Cramped layouts — when in doubt, add more whitespace
- ❌ Generic design — each visualization should feel intentional, not templated
- ❌ Missing menu — every output needs the hamburger menu
- ❌ Broken print — always include `@media print` styles

## Advanced Techniques

Use these when they add value. See [references/css-techniques.md](references/css-techniques.md) for code snippets.

- **Glass morphism** — `backdrop-blur-md bg-white/5 border border-white/10` for floating cards
- **Gradient text** — `background: linear-gradient(...); -webkit-background-clip: text` for hero headlines
- **Scroll-snap** — `scroll-snap-type: y mandatory` as alternative slide navigation (no JS needed)
- **Conic gradients** — `conic-gradient()` for pure CSS pie/donut charts
- **Number animations** — animate counters from 0 to target value on scroll
- **Spring easing** — `cubic-bezier(0.34, 1.56, 0.64, 1)` for playful micro-interactions
- **CSS counters** — auto-numbering for step-by-step processes
- **View Transitions API** — smooth theme switching animations
- **Inline SVG icons** — draw simple icons as `<svg>` paths, no icon library needed

## Process

1. **Understand** — what's the message? Who's the audience? What format fits?
2. **Structure** — outline content/sections BEFORE writing code
3. **Build** — write the complete HTML file with all features
4. **Verify** — is it readable at a glance? Would you present this? Would someone screenshot and share it?

The quality bar: **"good, period"** — not "good for AI-generated."
