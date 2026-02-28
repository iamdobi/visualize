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
6. **Visual restraint** — Professional designs avoid decorative elements that add noise. No floating gradient orbs, rainbow borders, or ornamental animations.

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

### Design Notes
- **Use inline SVG for icons, NOT emojis.** Simple path-based SVGs for a professional look. See the Icons section above.
- **Chart.js charts MUST be destroyed and recreated on theme toggle** — not just CSS variable swaps. Colors are read at render time, so the chart must be rebuilt with new computed values.
- **Chart.js: DISABLE default animation** — Add `Chart.defaults.animation = false;` before creating charts. Default animations cause charts to appear blank/broken in screenshots, Playwright tests, and initial renders. This is a recurring bug that caused "broken charts" in rounds 13-25.
- **Chart.js: Use explicit color values** — Don't concatenate CSS variable values with hex alpha suffixes (e.g., `c.remote + '18'`). Use explicit `rgba()` values instead: `'rgba(12, 206, 107, 0.15)'`.
- **Chart.js: Don't use resetCanvas** — Just reuse the same canvas element. Destroy the old chart instance with `.destroy()` then create a new one on the same canvas.
- **Chart.js: Build after layout is stable** — Use `window.addEventListener('load', ...)` with a short `setTimeout(200)` and trigger `window.dispatchEvent(new Event('resize'))` after building.

### Typography
- **Primary font:** Inter via Google Fonts CDN — `https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap`
- **Professional letter-spacing (Apple/Stripe-inspired):**
  - **Hero headings (h1):** `letter-spacing: -0.03em` — tight like Apple keynote titles
  - **Section headings (h2-h3):** `letter-spacing: -0.02em`
  - **Body text:** `letter-spacing: -0.011em` for refined readability
  - **Labels/caps:** `letter-spacing: 0.05em` for small uppercase text
  - **Font features:** `font-feature-settings: 'cv11', 'ss01';` for Inter's stylistic alternates
- **Font-weight hierarchy (Stripe-inspired):**
  - **h1:** `font-weight: 700` (bold, not 800 — optically cleaner at large sizes)
  - **h2:** `font-weight: 600` (semibold)
  - **Card titles:** `font-weight: 600`
  - **Body text:** `font-weight: 400` (regular)
  - **Labels:** `font-weight: 500` (medium)
- **Text colors (Vercel-inspired):** Never pure white. Use `#ededed` or `var(--text)` which maps to `#f5f5f7` in dark mode. Secondary text at 60% opacity feel (`#888` or `var(--text-secondary)`)
- **NO gradient text on headings** — use solid colors only. Gradient text looks cheap at scale.
- **Multilingual support:** When content includes non-Latin text (Korean, Japanese, Chinese, etc.), add the appropriate Google Fonts:
  - **Korean:** Noto Sans KR — `https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700;800;900&display=swap`
  - **Japanese:** Noto Sans JP — `https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;500;600;700;800;900&display=swap`
  - **Chinese (Simplified):** Noto Sans SC — `https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;600;700;800;900&display=swap`
  - **Arabic:** Noto Sans Arabic — `https://fonts.googleapis.com/css2?family=Noto+Sans+Arabic:wght@300;400;500;600;700;800;900&display=swap`
  - Set `font-family: 'Noto Sans KR', 'Inter', sans-serif;` (CJK font first, then Inter fallback for numbers/Latin)
  - Set `<html lang="ko">` (or appropriate language code)
- **Custom fonts:** When the user requests a specific font or vibe:
  - **Serif/editorial:** Lora, Playfair Display, Source Serif Pro
  - **Monospace/code:** JetBrains Mono, Fira Code, Source Code Pro
  - **Display/creative:** Space Grotesk, Outfit, Sora, Poppins
  - **Handwritten:** Caveat, Patrick Hand
  - Always load via Google Fonts CDN: `https://fonts.googleapis.com/css2?family=FONTNAME:wght@WEIGHTS&display=swap`
  - Update the `--font-primary` CSS var and `body { font-family: ... }` accordingly
- **Font detection:** Infer the right font from context:
  - Korean/Japanese/Chinese content → auto-add Noto Sans KR/JP/SC
  - Code-heavy content (cheat sheets) → add JetBrains Mono for code blocks
  - Formal/editorial content → consider a serif font for headings
  - Playful/creative content → consider display fonts
- **Monospace:** JetBrains Mono or system `'SF Mono', 'Fira Code', 'Consolas', monospace`
- **Fallback:** `-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif`
- **Type scale (dramatic):** Make hero titles bigger, body should breathe more — 14 → 16 → 20 → 25 → 31 → 39 → 49px
- **Line-height:** 1.5–1.7 for body, 1.1 for headings (tight for professional feel)
- **Max line width:** 65–75 characters for readability
- Use `clamp()` for fluid responsive sizing: `clamp(1rem, 2.5vw, 1.25rem)`

### Modern CSS Techniques (Chrome 105+)

Use these cutting-edge CSS features where supported for better UX:

**Popover API** (Chrome 114+) — Zero-JS tooltips, info panels, and modals:
```html
<button popovertarget="info-panel">ℹ Details</button>
<div id="info-panel" popover>
  <h3>More Information</h3>
  <p>Details shown on click, no JS needed.</p>
</div>
```
```css
[popover] {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 8px; padding: 16px; max-width: 320px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.2);
}
[popover]::backdrop { background: rgba(0,0,0,0.3); }
```
Use for: dashboard metric details, architecture node info, chart annotations.

**Exclusive `<details>` Accordion** (Chrome 120+) — Collapsible sections, no JS:
```html
<details name="faq" open><summary>Section 1</summary><p>Content</p></details>
<details name="faq"><summary>Section 2</summary><p>Content</p></details>
```
Same `name` attribute = only one open at a time. Use for: cheatsheets, process guides, FAQs, any content with collapsible groups.

**`::details-content` Styling** (Chrome 131+) — Animate accordion open/close:
```css
details { overflow: hidden; }
::details-content {
  transition: block-size 0.3s ease, opacity 0.3s ease;
  block-size: 0; opacity: 0;
}
details[open]::details-content {
  block-size: auto; opacity: 1;
}
```

**CSS Anchor Positioning** (Chrome 125+) — Position tooltips relative to elements:
```css
.node { anchor-name: --node-tooltip; }
.tooltip {
  position: fixed; position-anchor: --node-tooltip;
  position-area: block-start; margin-bottom: 8px;
}
```
Use for: architecture diagrams, org charts, any element needing positioned annotations.

**Container Queries** — Size elements based on their container, not viewport:
```css
.card-container {
  container-type: inline-size;
  container-name: card;
}
@container card (width > 400px) {
  .card-title { font-size: clamp(1.25rem, 4cqi, 2rem); }
}
```

**:has() Parent Selector** — Style elements based on their children:
```css
/* Style card if it contains an image */
.card:has(img) { padding-block: 2rem; }
/* Reduce spacing on headings followed by subheadings */
h1:has(+ h2) { margin-bottom: 0.25rem; }
```

**color-mix() Function** — Dynamic color generation:
```css
background: color-mix(in oklch, var(--accent), transparent 20%);
border-color: color-mix(in srgb, var(--text), var(--bg) 85%);
```

**light-dark() Function** (Chrome 123+) — Single-property theme switching:
```css
:root { color-scheme: light dark; }
background: light-dark(white, #1a1a1a);
color: light-dark(#333, #fff);
```

**@starting-style** (Chrome 117+) — Entry animations for new elements:
```css
.modal {
  opacity: 1; transform: scale(1);
  transition: opacity 0.3s, transform 0.3s;
  @starting-style {
    opacity: 0; transform: scale(0.8);
  }
}
```

### Color System (Dark-First with CSS Detection)

Default dark palette — all derived from CSS custom properties with CSS `prefers-color-scheme` detection to prevent flash:
```css
/* CSS prefers-color-scheme for flash-free theme switching */
@media (prefers-color-scheme: dark) {
  :root {
    --bg: #030712;           /* gray-950 */
    --surface: #111827;       /* gray-900 */
    --surface-hover: #1f2937; /* gray-800 */
    --border: rgba(255,255,255,0.1);
    --text: #f9fafb;          /* gray-50 */
    --text-secondary: #d1d5db; /* gray-300 — bumped from gray-400 for WCAG AA contrast */
    --accent: #3b82f6;        /* blue-500 */
    --accent-secondary: #8b5cf6; /* violet-500 */
    --positive: #10b981;      /* emerald-500 */
    --negative: #f43f5e;      /* rose-500 */
    --warning: #f59e0b;       /* amber-500 */
  }
}

@media (prefers-color-scheme: light) {
  :root {
    --bg: #f8fafc;
    --surface: #ffffff;
    --surface-hover: #f1f5f9;
    --border: rgba(0,0,0,0.08);
    --text: #0f172a;
    --text-secondary: #64748b;
    --accent: #2563eb;
    --accent-secondary: #7c3aed;
    --positive: #059669;
    --negative: #e11d48;
    --warning: #d97706;
  }
}

/* Manual theme override classes (JS controlled) */
.theme-dark {
  --bg: #030712; --surface: #111827; --surface-hover: #1f2937;
  --border: rgba(255,255,255,0.08);
  --text: #f9fafb; --text-secondary: #d1d5db;
  --accent: #3b82f6; --accent-secondary: #8b5cf6;
  --positive: #10b981; --negative: #f43f5e; --warning: #f59e0b;
}
.theme-light {
  --bg: #f8fafc; --surface: #ffffff; --surface-hover: #f1f5f9;
  --border: rgba(0,0,0,0.08);
  --text: #0f172a; --text-secondary: #64748b;
  --accent: #2563eb; --accent-secondary: #7c3aed;
  --positive: #059669; --negative: #e11d48; --warning: #d97706;
}
```

Chart color sequence: `#3b82f6, #8b5cf6, #ec4899, #f59e0b, #10b981, #06b6d4, #f43f5e`

### Spacing
- **8px grid** — all spacing in multiples: 4, 8, 12, 16, 24, 32, 48, 64, 96px
- **Generous padding** — `p-6` to `p-8` on cards, `px-8` on containers
- **Container:** `max-w-7xl mx-auto px-4 sm:px-6 lg:px-8`
- **Card gaps:** `gap-6` minimum

### Card Hover Microinteractions
All cards should have subtle hover effects — shadow elevation ONLY, no transforms:
```css
.card, .stat-card, .kpi-card, .stat-item, .chart-container {
  transition: box-shadow 0.2s ease;
}
.card:hover, .stat-card:hover, .kpi-card:hover, .stat-item:hover {
  box-shadow: 0 0 0 1px var(--border), 0 8px 16px rgba(0,0,0,0.08);
}
```
- NO `translateY` or `scale` on card hover — it looks cheap
- Timeline items: subtle background highlight on hover
- Architecture nodes: subtle shadow elevation on hover
- List items: subtle background tint on hover, not translateX

### :focus-visible Standard
Every file MUST include:
```css
*:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
  border-radius: 4px;
}
```

### SVG Chart Hover Pattern
For inline SVG chart elements (bars, donut segments, data points):
```css
svg rect, svg circle, svg path.data-element {
  transition: opacity 0.2s, transform 0.2s;
}
svg rect:hover, svg circle:hover {
  opacity: 0.8;
  filter: brightness(1.1);
}
```
Always add `<title>` elements inside SVG shapes for native browser tooltips:
```html
<rect x="10" y="20" width="50" height="100">
  <title>Revenue: $142K</title>
</rect>
```

### Visual Polish (Stripe/Vercel-level)
- **Border radius:** `8px` consistently (not 12px, not 16px — Stripe uses 8px)
- **Shadows (dark mode):** Almost none — `box-shadow: 0 0 0 1px var(--border)` is sufficient. Let borders do the work.
- **Shadows (light mode):** Subtle layers — `box-shadow: 0 0 0 1px rgba(0,0,0,0.03), 0 2px 4px rgba(0,0,0,0.05)`
- **Card hover:** Shadow deepens slightly. NO translateY, NO scale transforms. Just: `box-shadow: 0 0 0 1px rgba(0,0,0,0.03), 0 8px 16px rgba(0,0,0,0.08)`
- **Clean card borders:** `border: 1px solid var(--border)` — no gradient borders, no colored left/top borders
- **Glass morphism:** Use sparingly, only for floating UI elements (menus, tooltips), not cards
- **Restrained accents:** Use accent color for ONE thing per section (a button, a link, an icon) — not everywhere
- **Transitions:** `transition: box-shadow 0.2s ease` — only animate what changes

### Background Atmosphere (Avoid Generic Dark)
Every visualization should have a SUBTLE background personality. Avoid flat `--bg` backgrounds that look like every dark template. Choose ONE technique per file:

1. **Subtle radial gradient** — a single, very faint radial gradient from the center:
   ```css
   body { background: var(--bg); }
   body::before {
     content: ''; position: fixed; inset: 0; z-index: -1;
     background: radial-gradient(ellipse 80% 50% at 50% 20%, 
       color-mix(in srgb, var(--accent), transparent 92%), transparent);
   }
   ```
2. **Noise/grain texture** (Vercel-style): use a tiny inline SVG noise filter:
   ```css
   body::after {
     content: ''; position: fixed; inset: 0; z-index: -1; opacity: 0.03;
     background: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
   }
   ```
3. **Dot grid** (use sparingly, only for tech/architecture files):
   ```css
   body { background-image: radial-gradient(circle, rgba(255,255,255,0.03) 1px, transparent 1px);
     background-size: 24px 24px; }
   ```

Choose the technique that matches the content personality. Timelines → radial gradient. Dashboards → grain. Architecture → dot grid. Slide decks → radial gradient with content-specific accent color.

### Dropdown Menu Styling (Mandatory)
The settings/export dropdown MUST look polished:
```css
.dropdown-menu {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3), 0 0 0 1px rgba(255,255,255,0.05);
  padding: 4px;
  min-width: 160px;
  animation: dropdownIn 0.15s ease;
}
.dropdown-menu button {
  width: 100%; text-align: left; padding: 8px 12px;
  border-radius: 6px; border: none; background: transparent;
  color: var(--text-secondary); font-size: 0.875rem; cursor: pointer;
  transition: background 0.15s, color 0.15s;
}
.dropdown-menu button:hover {
  background: var(--surface-hover); color: var(--text);
}
@keyframes dropdownIn {
  from { opacity: 0; transform: translateY(-4px); }
  to { opacity: 1; transform: translateY(0); }
}
```

### Entrance Animations (Mandatory for All Files)
Every file MUST have subtle entrance animations. Static-feeling pages score low on interactivity. Use CSS-only `@keyframes` on page load:
```css
@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}
.card, .step, .quote-card, section > * {
  animation: fadeInUp 0.5s ease both;
}
/* Stagger children */
.card:nth-child(1) { animation-delay: 0s; }
.card:nth-child(2) { animation-delay: 0.08s; }
.card:nth-child(3) { animation-delay: 0.16s; }
.card:nth-child(4) { animation-delay: 0.24s; }
```
Also add hover states on ALL cards/items — even "static" content like cheatsheets and quote cards:
```css
.card:hover, .command-group:hover, blockquote:hover {
  background: var(--surface-hover);
  box-shadow: 0 0 0 1px var(--border), 0 8px 16px rgba(0,0,0,0.08);
}
```

### Theme-Adaptive Content (Carousels, Posters)
When cards use decorative gradients (e.g., Instagram-style pastel slides), the gradients MUST adapt to the theme. Don't use fixed pastel colors that look identical in dark/light mode:
```css
/* BAD — same gradient in both themes */
.card { background: linear-gradient(135deg, #ff9a9e, #fecfef); }

/* GOOD — theme-adaptive gradients */
.theme-dark .card-1 { background: linear-gradient(135deg, #1a1a2e, #16213e); }
.theme-light .card-1 { background: linear-gradient(135deg, #ff9a9e, #fecfef); }
```

### Slide Deck Light Mode
Slide decks are designed dark-first, but light mode must NOT feel like an afterthought. For presentations in light mode:
- Use a subtle warm gray background (`#f5f5f0`) not pure white
- Add a faint top-down gradient for depth
- Ensure headings use dark text with sufficient weight
- Grid/glow backgrounds should switch to subtle dot patterns or soft gradients in light mode

### Chart Accessibility (Mandatory)
All CSS-only charts (bars, radar, donut) and Chart.js charts MUST expose data to screen readers:
```html
<div role="img" aria-label="Bar chart showing React at 85%, Vue at 72%, Angular at 58%">
  <!-- visual chart here -->
  <div class="sr-only">React: 85%. Vue: 72%. Angular: 58%.</div>
</div>
```
Add `.sr-only { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0,0,0,0); }` to every file.

### Visual Restraint Anti-Patterns (NEVER DO)
- ❌ **Floating gradient orbs** — decorative blurred circles behind content look amateurish
- ❌ **Rainbow/gradient borders** — colored top-borders or left-borders on cards scream "template"
- ❌ **Gradient text** on headings — use solid colors. Gradient text is a 2020 trend that aged poorly
- ❌ **Scale transforms on hover** — `scale(1.02)` on cards feels janky, not premium
- ❌ **Glow effects** — `box-shadow: 0 0 20px rgba(blue)` never looks good
- ❌ **Decorative animations** — spinning rings, floating particles, pulsing dots are noise
- ❌ **Color-coded borders** — left/top colored borders on cards feel like Bootstrap components
- ❌ **Stat numbers with gradient text** — use a solid accent color or var(--text) instead

### Accessibility (Mandatory)

Every visualization MUST meet these baseline accessibility requirements:

**Minimum Accessibility Checklist:**
- [ ] Skip-to-content link present
- [ ] `role="region"` on all major sections with `aria-label`
- [ ] `role="group"` on comparison sections, architecture layers, slide groups
- [ ] `role="list"` / `role="listitem"` on timeline sections and items
- [ ] `aria-label` on all icon-only buttons
- [ ] `aria-describedby` on chart sections linking to data descriptions
- [ ] `:focus-visible` with `border-radius: 4px` on all interactive elements
- [ ] `aria-live="polite"` on slide counters / dynamic content

- **Skip navigation:** Add `<a href="#main-content" class="skip-link">Skip to content</a>` at the top of `<body>`. Style: visually hidden, visible on focus.
- **Landmark roles:** Use `<main>`, `<nav>`, `<header>`, `<footer>`, `<section>` with `aria-label` where there are multiple of the same landmark.
- **Interactive elements:** All buttons, links, and controls must have `aria-label` if their text content is not descriptive (e.g., icon-only buttons).
- **Focus indicators:** Add visible `:focus-visible` styles on all interactive elements: `outline: 2px solid var(--accent); outline-offset: 2px;`
- **Color-only indicators:** Status dots, colored badges, etc. MUST have a text alternative. E.g., a green status dot should also show "Healthy" text or `aria-label="Status: Healthy"`.
- **Charts and diagrams (MANDATORY):** 
  - Wrap chart canvas in container with `role="img" aria-label="Description of what the chart shows"`
  - **ALL charts MUST have hover tooltips enabled** — never disable Chart.js tooltips
  - Include data table alternative or visually-hidden summary for screen readers
  - Use high contrast colors with sufficient color difference between data series
- **Screen reader descriptions:** Add `aria-description` or visually-hidden text describing key takeaways for complex visualizations.
- **Slide decks:** Use `aria-live="polite"` on the slide counter, and `aria-label` on navigation buttons.

### Icons (Inline SVG Only)

Use inline SVG for all icons. **Never use emoji as icons** — they look unprofessional and render inconsistently.

Use simple Lucide-style paths: 24x24 viewBox, stroke-based, `stroke="currentColor" fill="none" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"`.

Common icons to use:
- Moon/Sun for theme toggle
- Download arrow for PNG export  
- Printer for print
- Arrow left/right for navigation
- Check/X for pros/cons
- Globe, Smartphone, Monitor for device types

### Animations (CSS-First with Modern Features)

**CSS animations are the primary system.** They're reliable, performant, and never break from JS scoping issues.

See [references/animations.md](references/animations.md) for complete patterns.

**Modern CSS Animation Features (Progressive Enhancement):**

**Scroll-driven animations** (Chrome 115+) — Replace JS scroll listeners:
```css
.scroll-reveal {
  animation: fadeInUp 1ms linear;
  animation-timeline: view(); /* Animates based on viewport visibility */
}
.progress-bar {
  animation: grow 1ms linear;  
  animation-timeline: scroll(root inline); /* Animates based on page scroll */
}
```

**Three animation techniques (all baked into the skeleton):**

1. **Page-load entrance:** Add class `animate` (+ `delay-1` through `delay-6` for stagger)
   ```html
   <h1 class="animate">Title</h1>
   <div class="card animate delay-1">Card 1</div>
   <div class="card animate delay-2">Card 2</div>
   ```

2. **Scroll reveal:** Add `data-reveal` attribute. JS adds `.reveal` class (opacity:0), then `.visible` on scroll.
   ```html
   <section data-reveal>This fades in when scrolled into view</section>
   ```

3. **Number counters:** Add `data-count` attribute. JS animates from 0 to target.
   ```html
   <span data-count="77" data-suffix="%">77%</span>
   ```

**Hover effects** are pure CSS, baked into `.card` (translateY + scale on :hover).

**Rules:**
- Content is ALWAYS visible in CSS — JS animations are progressive enhancement
- Use `@keyframes` for page-load animations, CSS `transition` for hover/state changes
- `data-reveal` elements show their final content if JS fails (no blank sections)
- `prefers-reduced-motion` disables all animations automatically
- `data-reveal` elements MUST have `opacity: 1` as their default CSS state. JS adds `.reveal` class (which sets `opacity: 0`), then `.visible` restores it. If JS fails, content stays visible.
- On page load, trigger ALL reveal elements visible after a short delay (500ms) so full-page screenshots and PNG exports capture all content:
  ```javascript
  setTimeout(function() { document.querySelectorAll('.reveal').forEach(function(el) { el.classList.add('visible'); }); }, 500);
  ```

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
| **Carousel Cards** | Social media (IG/LinkedIn) | 1080×1080 per card, swipeable, bold text |
| **Event Poster** | Conferences, meetups, webinars | Portrait A4/letter, bold headline, date/venue |
| **Resume/CV** | Job applications | One-page, two-column, print-optimized |
| **Banner/Header** | Email, blog, social cover | 1200×630 or 1500×500, centered text on visual bg |
| **Quote Card** | Social proof, testimonials | Portrait/square, large quote, attribution |
| **Process Guide** | How-to, step-by-step | Numbered steps, icons, clear flow |
| **Status Report** | Executive updates | KPIs + progress bars + highlights, one-page |
| **Org Chart** | Team structure | Hierarchical tree, photos/avatars, roles |
| **Data Story** | Narrative + data | Scrollytelling, charts woven with narrative text |
| **Product Card** | Feature highlight, launch | Hero image area, feature pills, CTA |

### Carousel Card Rules

Carousel cards are huge for social media. Get these right:

- **Square format** — `1080×1080px` (or configurable via CSS var)
- **One idea per card** — bold headline + 1-2 supporting points max
- **Swipe nav** — arrows + dots + touch swipe + keyboard
- **Card counter** — "3 / 8" visible
- **Download all** — PNG export of individual cards or full set
- **Typography dominates** — headline at 2.5-4rem, minimal body text
- **Color-coded** — each card can have a subtle accent shift
- **Print layout** — grid of all cards for printing
- **Max 10 cards** — keep it focused

### Event Poster Rules

- **Portrait orientation** — A4/letter ratio or square
- **Visual hierarchy** — Event name (largest) → Date/Time → Location → Description → CTA
- **Bold headline** — 3-5rem, max 6 words
- **Date/time prominent** — styled as a badge or highlighted block
- **QR code area** — placeholder box for registration link
- **Print-first** — looks great printed, dark or light theme

### Quote Card Rules

- **Large quotation marks** — decorative " " in accent color, oversized
- **Quote text** — 1.5-2.5rem, serif or italic weight for contrast
- **Attribution** — name, title, company below quote
- **Square or portrait** — optimized for social sharing
- **Minimal design** — quote is the hero, everything else is subtle

## Slide Deck Rules

Slides are the most common request. Get these right:

- **16:9 aspect ratio** — `100vw × 100vh`, content centered
- **Responsive breakpoints** — Use `clamp()` and container queries for mobile-friendly slides:
  ```css
  .slide-container { container-type: inline-size; }
  .slide-title { font-size: clamp(2rem, 8vw, 4rem); }
  @container (width < 768px) { .slide-content { padding: 1rem; } }
  ```
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

### Theme-Aware Slide Gradients (CRITICAL)

Slide decks MUST look visually distinct in dark vs light themes. Gradient backgrounds must change:

```css
/* Dark theme: deep, saturated gradients */
.theme-dark .slide-title { background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #1e3a5f 100%); }
.theme-dark .slide-content { background: var(--bg); }

/* Light theme: soft, pastel gradients */
.theme-light .slide-title { background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 50%, #dbeafe 100%); }
.theme-light .slide-content { background: var(--bg); }
```

Rules:
- Title/section slides: use theme-specific gradient pairs (dark=deep+saturated, light=soft+pastel)
- Content slides: use `var(--bg)` or `var(--surface)` — NOT hardcoded dark backgrounds
- Data cards on slides: use `var(--surface)` with `var(--border)` — they auto-adapt
- Never hardcode `#1a1a2e` or similar dark colors on slide content — use CSS variables
- Test: toggle theme and every slide should look intentionally designed for that mode

### Slide Types
1. **Title** — theme-aware gradient background, big headline, subtitle. Center aligned.
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

## Type-Specific Interactivity (Mandatory)

Every file MUST have at least ONE meaningful interaction beyond theme toggle + menu. Static-feeling pages score low on interactivity.

| Type | Required Interaction |
|------|---------------------|
| **Cheatsheet** | Search/filter input + copy-to-clipboard on code blocks. Use `<details name="...">` for collapsible groups. |
| **Dashboard** | Filter toolbar or metric drill-down. At minimum: date range or category filter. |
| **Status Report** | Collapsible detail sections (use `<details>`). Progress bars animate on scroll. |
| **Quote Card** | Auto-cycling quotes OR swipeable carousel. Share/copy button. |
| **Event Poster** | Animated countdown timer (days/hours/min/sec). RSVP/register button. |
| **Process Guide** | Steps as exclusive accordion (`<details name="steps">`). Or interactive progress tracker. |
| **Architecture** | Clickable nodes with popover details (use Popover API). Hover highlights connections. |
| **Timeline** | Filter by era/category. Or click to expand event details. |
| **Comparison** | Toggle categories on/off. Or highlight winner per row. |
| **Carousel** | Touch swipe + keyboard + auto-advance option. Card counter always visible. |
| **Slide Deck** | Already interactive (nav). Add: presenter timer, slide overview grid. |

If a type isn't listed, add at minimum: a filter, search, sort, or expand/collapse interaction.

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
- **Animate to auto** — `interpolate-size: allow-keywords` on `:root` enables smooth `height: auto` transitions (Chrome 129+)
- **CSS counters** — auto-numbering for step-by-step processes
- **View Transitions API** — smooth theme switching animations
- **Inline SVG icons** — draw simple icons as `<svg>` paths, no icon library needed

## Mandatory HTML Skeleton

**EVERY visualization MUST start from this skeleton.** Copy it, then add content. This gives you themes, print styles, Inter font, animations, menu, and hover effects — all working out of the box.

**Design philosophy: CSS-first, JS-minimal.** Animations use CSS `@keyframes` and `transition` (always reliable). JavaScript is only for: menu, theme toggle, scroll observer, number counters, and PNG download. No animation libraries required.

```html
<!DOCTYPE html>
<html lang="en" class="theme-dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>YOUR TITLE HERE</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
  <!-- ADD LANGUAGE FONTS IF NEEDED: e.g. Noto Sans KR for Korean, Noto Sans JP for Japanese -->
  <!-- <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet"> -->
  <!-- ADD CDN LIBRARIES HERE (Chart.js, Mermaid, etc.) -->
  <script src="https://cdn.jsdelivr.net/npm/html-to-image@1.11.11/dist/html-to-image.js"></script>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    :root { interpolate-size: allow-keywords; } /* Enable smooth height:auto transitions (Chrome 129+) */

    /* ===== THEMES ===== */
    /* CSS prefers-color-scheme for flash-free theme detection */
    @media (prefers-color-scheme: dark) {
      :root {
        --bg: #030712; --surface: #111827; --surface-hover: #1f2937;
        --border: rgba(255,255,255,0.08);
        --text: #f9fafb; --text-secondary: #9ca3af;
        --accent: #3b82f6; --accent-secondary: #8b5cf6;
        --positive: #10b981; --negative: #f43f5e; --warning: #f59e0b;
      }
    }
    @media (prefers-color-scheme: light) {
      :root {
        --bg: #f8fafc; --surface: #ffffff; --surface-hover: #f1f5f9;
        --border: rgba(0,0,0,0.08);
        --text: #0f172a; --text-secondary: #64748b;
        --accent: #2563eb; --accent-secondary: #7c3aed;
        --positive: #059669; --negative: #e11d48; --warning: #d97706;
      }
    }
    /* Manual theme override classes (JS controlled) */
    .theme-dark {
      --bg: #030712; --surface: #111827; --surface-hover: #1f2937;
      --border: rgba(255,255,255,0.08);
      --text: #f9fafb; --text-secondary: #9ca3af;
      --accent: #3b82f6; --accent-secondary: #8b5cf6;
      --positive: #10b981; --negative: #f43f5e; --warning: #f59e0b;
    }
    .theme-light {
      --bg: #f8fafc; --surface: #ffffff; --surface-hover: #f1f5f9;
      --border: rgba(0,0,0,0.08);
      --text: #0f172a; --text-secondary: #64748b;
      --accent: #2563eb; --accent-secondary: #7c3aed;
      --positive: #059669; --negative: #e11d48; --warning: #d97706;
    }

    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: var(--bg); color: var(--text);
      line-height: 1.6; -webkit-font-smoothing: antialiased;
      letter-spacing: -0.01em; font-feature-settings: 'cv11', 'ss01';
      transition: background 0.3s, color 0.3s;
    }
    h1,h2,h3,h4,h5,h6 { 
      color: var(--text); 
      letter-spacing: -0.03em; 
      line-height: 1.08;
    }
    h1 { font-weight: 700; }
    h2 { font-weight: 600; }
    body, p, li, td, th, span, label { font-weight: 400; }
    p,li,td,th,span,label { color: var(--text); }
    .text-secondary { color: var(--text-secondary); }

    /* ===== CARD ===== */
    .card {
      background: var(--surface); border: 1px solid var(--border);
      border-radius: 8px; padding: 24px;
      transition: box-shadow 0.2s ease;
    }
    .card:hover {
      box-shadow: 0 0 0 1px var(--border), 0 8px 16px rgba(0,0,0,0.08);
    }

    /* ===== ANIMATIONS (CSS-first — always reliable) ===== */
    @keyframes fadeInUp {
      from { opacity: 0; transform: translateY(24px); }
      to { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeIn {
      from { opacity: 0; }
      to { opacity: 1; }
    }
    @keyframes slideInLeft {
      from { opacity: 0; transform: translateX(-40px); }
      to { opacity: 1; transform: translateX(0); }
    }
    @keyframes slideInRight {
      from { opacity: 0; transform: translateX(40px); }
      to { opacity: 1; transform: translateX(0); }
    }
    .animate { animation: fadeInUp 0.6s ease-out both; }
    .animate.delay-1 { animation-delay: 0.1s; }
    .animate.delay-2 { animation-delay: 0.2s; }
    .animate.delay-3 { animation-delay: 0.3s; }
    .animate.delay-4 { animation-delay: 0.4s; }
    .animate.delay-5 { animation-delay: 0.5s; }
    .animate.delay-6 { animation-delay: 0.6s; }

    /* Scroll-triggered: JS adds .reveal, then .visible on scroll */
    .reveal { opacity: 0; transform: translateY(24px); transition: opacity 0.6s ease, transform 0.6s ease; }
    .reveal.visible { opacity: 1; transform: translateY(0); }

    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after { animation: none !important; transition: none !important; }
      .reveal { opacity: 1; transform: none; }
    }

    /* ===== PRINT ===== */
    @media print {
      body { background: white !important; color: black !important; }
      .viz-menu, .reveal { display: revert; opacity: 1 !important; transform: none !important; }
      .card { break-inside: avoid; border: 1px solid #ddd; box-shadow: none; }
      * { print-color-adjust: exact; -webkit-print-color-adjust: exact; }
    }
    @page { margin: 1in; @bottom-center { content: "Page " counter(page); font-size: 9pt; color: #666; } }

    /* ===== MENU ===== */
    .viz-menu { position: fixed; top: 16px; right: 16px; z-index: 9999; }
    .viz-menu-toggle {
      width: 44px; height: 44px; border-radius: 12px;
      background: var(--surface); border: 1px solid var(--border);
      color: var(--text); cursor: pointer; display: flex;
      align-items: center; justify-content: center;
      backdrop-filter: blur(12px); transition: all 0.2s;
    }
    .viz-menu-toggle:hover { background: var(--surface-hover); }
    .viz-menu-dropdown {
      position: absolute; top: 52px; right: 0; min-width: 200px;
      background: var(--surface); border: 1px solid var(--border);
      border-radius: 12px; padding: 8px;
      opacity: 0; visibility: hidden; transform: translateY(-8px);
      transition: all 0.2s; backdrop-filter: blur(16px);
    }
    .viz-menu-dropdown.open { opacity: 1; visibility: visible; transform: translateY(0); }
    .viz-menu-dropdown button {
      width: 100%; padding: 10px 14px; border: none; border-radius: 8px;
      background: transparent; color: var(--text); font-size: 14px;
      font-family: inherit; cursor: pointer; text-align: left;
      display: flex; align-items: center; gap: 10px; transition: background 0.15s;
    }
    .viz-menu-dropdown button:hover { background: var(--surface-hover); }

    /* ===== ADD YOUR STYLES BELOW ===== */
  </style>
</head>
<body>
  <main>

  <!-- MENU -->
  <div class="viz-menu">
    <button class="viz-menu-toggle" onclick="toggleMenu()" aria-label="Menu">
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
        <line x1="3" y1="5" x2="17" y2="5"/><line x1="3" y1="10" x2="17" y2="10"/><line x1="3" y1="15" x2="17" y2="15"/>
      </svg>
    </button>
    <div class="viz-menu-dropdown" id="vizMenuDropdown">
      <button onclick="cycleTheme()"><span id="themeIcon">🌙</span><span id="themeLabel">Dark</span></button>
      <button onclick="downloadImage()"><span>📥</span><span>Download PNG</span></button>
      <button onclick="window.print()"><span>🖨️</span><span>Print / PDF</span></button>
    </div>
  </div>

  <!-- YOUR CONTENT HERE (use <section>, <header>, <article> for semantics) -->

  </main>
  <script>
    // === Menu ===
    function toggleMenu() { document.getElementById('vizMenuDropdown').classList.toggle('open'); }
    document.addEventListener('click', e => { if (!e.target.closest('.viz-menu')) document.getElementById('vizMenuDropdown').classList.remove('open'); });
    document.addEventListener('keydown', e => { if (e.key === 'Escape') document.getElementById('vizMenuDropdown').classList.remove('open'); });

    // === Theme ===
    var currentTheme = localStorage.getItem('viz-theme') || 'dark';
    function applyTheme(t) {
      document.documentElement.className = 'theme-' + t;
      document.getElementById('themeIcon').textContent = t === 'dark' ? '🌙' : '☀️';
      document.getElementById('themeLabel').textContent = t === 'dark' ? 'Dark' : 'Light';
      localStorage.setItem('viz-theme', t);
      currentTheme = t;
      if (typeof onThemeChange === 'function') onThemeChange(); // hook for chart re-render
    }
    function cycleTheme() { applyTheme(currentTheme === 'dark' ? 'light' : 'dark'); }
    applyTheme(currentTheme);

    // === Scroll Reveal (adds .reveal then .visible — content visible without JS) ===
    document.querySelectorAll('[data-reveal]').forEach(el => el.classList.add('reveal'));
    var revealObserver = new IntersectionObserver(function(entries) {
      entries.forEach(function(e) { if (e.isIntersecting) { e.target.classList.add('visible'); revealObserver.unobserve(e.target); } });
    }, { threshold: 0.15 });
    document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

    // === Number Counter (use data-count="77" data-suffix="%" on elements) ===
    function animateCounters() {
      document.querySelectorAll('[data-count]').forEach(function(el) {
        if (el.dataset.counted) return;
        el.dataset.counted = '1';
        var target = parseFloat(el.dataset.count), prefix = el.dataset.prefix || '', suffix = el.dataset.suffix || '';
        var start = performance.now(), duration = 1200;
        (function tick(now) {
          var p = Math.min((now - start) / duration, 1), eased = 1 - Math.pow(1 - p, 3);
          el.textContent = prefix + Math.round(target * eased).toLocaleString() + suffix;
          if (p < 1) requestAnimationFrame(tick);
        })(start);
      });
    }
    var counterEl = document.querySelector('[data-count]');
    if (counterEl) {
      var cObs = new IntersectionObserver(function(entries) {
        entries.forEach(function(e) { if (e.isIntersecting) { animateCounters(); cObs.disconnect(); } });
      }, { threshold: 0.3 });
      cObs.observe(counterEl);
    }

    // === Download PNG ===
    async function downloadImage() {
      var menu = document.querySelector('.viz-menu');
      menu.style.display = 'none';
      try {
        var url = await htmlToImage.toPng(document.body, { quality: 1, pixelRatio: 2, filter: function(n) { return !n.classList || !n.classList.contains('viz-menu'); } });
        var a = document.createElement('a'); a.href = url;
        a.download = document.title.replace(/\s+/g, '-').toLowerCase() + '.png'; a.click();
      } catch(e) { console.error('Download failed:', e); }
      menu.style.display = '';
    }

    // === YOUR SCRIPTS BELOW (use var for top-level variables, define onThemeChange for chart re-renders) ===
  </script>
</body>
</html>
```

### Skeleton Rules

**Do:**
- Use `var` for all top-level variables (avoids TDZ errors when functions are hoisted)
- Use `data-reveal` attribute on sections/cards for scroll animation
- Use `data-count="77" data-suffix="%"` for animated number counters
- Use `.animate.delay-N` classes for page-load entrance animations
- Use CSS `:hover` for hover effects (baked into `.card` already)
- Define `function onThemeChange() {}` to re-render charts on theme toggle
- Use `<main>`, `<section>`, `<header>`, `<article>` for semantic HTML
- Keep all chart variables as `var` (not `let`/`const`) at script top level

**Don't:**
- Don't include Motion.js unless you specifically need spring physics
- Don't hide content via JS/CSS for animation — use `data-reveal` pattern instead
- Don't use `let`/`const` for variables that might be referenced before declaration
- Don't use `.finished` Promise chains for sequencing — use `setTimeout`
- Don't put animation logic that could crash before nav/chart setup code

## Minimum Sizing Rules

Elements must be large enough to read and feel substantial:

- **Timeline cards:** minimum width 280px, minimum padding 20px
- **Chart containers:** minimum 60% of parent width, minimum height 300px
- **Stat numbers:** minimum font-size 2rem (32px), bold/extrabold weight
- **Card content area:** minimum padding 24px
- **Section spacing:** minimum 48px between major sections
- **Slide headings:** minimum 2rem (32px), maximum 6 words
- **Body text:** minimum 1rem (16px), never smaller

**If content feels too small, it IS too small. Err on the side of larger.**

## Text Visibility Rules

**Text must ALWAYS be visible.** This is the #1 cause of broken outputs.

- Dark theme: text MUST use `var(--text)` which resolves to `#f9fafb` (near-white)
- Light theme: text MUST use `var(--text)` which resolves to `#0f172a` (near-black)
- On gradient backgrounds: add `text-shadow: 0 1px 3px rgba(0,0,0,0.3)` for readability
- On hero slides with gradient/image backgrounds: use a dark overlay (`rgba(0,0,0,0.5)`)
- NEVER set text color to a value close to the background color
- Test mentally: "would this text be visible on BOTH dark (#030712) and light (#f8fafc) backgrounds?"

## Chart.js Integration Rules

Charts are the second most common failure. Follow these rules:

- **Always wrap in a container div** with explicit `width` and `height` or `aspect-ratio`
- **MANDATORY: Add accessibility container** with `role="img"` and descriptive `aria-label`:
  ```html
  <div role="img" aria-label="Bar chart showing Q4 revenue increased 23% to $2.4M across 4 product lines">
    <div class="chart-container"><canvas id="myChart"></canvas></div>
  </div>
  ```
- **MANDATORY: Hover tooltips enabled** — never disable Chart.js tooltips:
  ```javascript
  options: {
    plugins: {
      tooltip: {
        enabled: true, // NEVER set to false
        mode: 'index',
        intersect: false
      }
    }
  }
  ```
- **Minimum chart height:** 300px on desktop, 250px on mobile
- **Font size defaults:** Axis tick labels at 13px minimum, axis titles at 14px, chart titles at 16px minimum. Legend at 13px.
- **Chart padding:** Add `layout: { padding: { top: 20, right: 20, bottom: 20, left: 20 } }` for breathing room
- **Axis tick config:** `maxRotation: 0` to keep labels horizontal. If labels overflow, use `maxTicksLimit` to reduce count
- **Grid lines:** Very faint — `rgba(255,255,255,0.04)` in dark, `rgba(0,0,0,0.06)` in light
- **Tooltip styling:** `padding: 12`, `cornerRadius: 8`, `titleFont: { size: 14 }`, `bodyFont: { size: 13 }`
- **Point radius:** 0 by default, 6 on hover — cleaner line charts
- **Set `maintainAspectRatio: false`** and control size via CSS container
- **Use theme-aware colors:** read CSS vars at render time, re-render on theme change
- **Chart text colors:** set `Chart.defaults.color = getComputedStyle(root).getPropertyValue('--text-secondary').trim()`
- **Grid line colors:** use `var(--border)` value
- **Legend position:** 'top' for horizontal charts, 'right' for vertical with space
- **Axis labels:** Keep horizontal when possible - avoid rotation unless absolutely necessary
- **Donut/pie charts:** Always include percentage labels on segments
- **Responsive:** `responsive: true` is default, but container must have explicit dimensions
- **High contrast colors:** Ensure sufficient color difference between data series for accessibility

```javascript
// Theme-aware Chart.js setup (include in every chart visualization)
function getChartColors() {
  var s = getComputedStyle(document.documentElement);
  return {
    text: s.getPropertyValue('--text').trim(),
    textSecondary: s.getPropertyValue('--text-secondary').trim(),
    border: s.getPropertyValue('--border').trim(),
    surface: s.getPropertyValue('--surface').trim(),
    accent: s.getPropertyValue('--accent').trim(),
  };
}

// REQUIRED: Reset canvas before rebuilding charts (prevents "Canvas already in use" errors)
function resetCanvas(id) {
  var old = document.getElementById(id);
  var parent = old.parentNode;
  var canvas = document.createElement('canvas');
  canvas.id = id;
  parent.replaceChild(canvas, old);
  return canvas;
}

// Usage in buildCharts():
//   try { if (myChart) myChart.destroy(); } catch(e) {}
//   myChart = new Chart(resetCanvas('myChart'), { ... });
```

## Process

1. **Understand** — what's the message? Who's the audience? What format fits?
2. **Start from skeleton** — copy the Mandatory HTML Skeleton above. NEVER start from a blank file.
3. **Structure** — outline content/sections BEFORE filling in the skeleton
4. **Build** — add content, charts, styles. Keep all colors as CSS vars.
5. **Verify checklist:**
   - [ ] CSS `@media (prefers-color-scheme)` for flash-free theme detection?
   - [ ] Both `.theme-dark` and `.theme-light` manual override classes defined?
   - [ ] All text uses `var(--text)` or `var(--text-secondary)`?
   - [ ] `@media print` hides menu, shows all content?
   - [ ] `@media (prefers-reduced-motion: reduce)` present?
   - [ ] `.viz-menu` with toggle, theme, download, print?
   - [ ] Correct font loaded? (Inter default, Noto Sans KR for Korean, etc.)
   - [ ] Non-Latin content has appropriate CJK/RTL font?
   - [ ] Entrance animations via `.animate` classes (CSS @keyframes)?
   - [ ] Scroll sections use `data-reveal` (visible without JS)?
   - [ ] `.card:hover` has transform effect?
   - [ ] All top-level JS variables use `var` (not `let`/`const`)?
   - [ ] Charts use `var` declarations + `onThemeChange` hook?
   - [ ] **MANDATORY:** All charts wrapped with `role="img" aria-label="..."`?
   - [ ] **MANDATORY:** All charts have hover tooltips enabled (never disabled)?
   - [ ] Animated number counters use `data-count` where stats exist?
   - [ ] Semantic HTML: `<main>`, `<section>`, `<header>`, `<article>`?
   - [ ] All charts have explicit container sizing (≥300px height)?
   - [ ] Hero/title text visible on both themes?
   - [ ] Minimum sizing rules followed (cards 280px+, text 16px+)?
   - [ ] Zero console errors on load?

The quality bar: **"good, period"** — not "good for AI-generated."
