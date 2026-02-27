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

### Animations (Motion — Framer Motion for Vanilla JS)

**Motion is included in the skeleton** (`https://cdn.jsdelivr.net/npm/motion@12/dist/motion.js`). Use it for ALL animations. It provides spring physics, scroll-triggered reveals, stagger, and orchestration — far superior to raw CSS keyframes.

See [references/animations.md](references/animations.md) for complete API, recipes, and patterns.

**Key APIs:**
- `Motion.animate(target, keyframes, options)` — animate any element with spring physics
- `Motion.inView(target, callback)` — trigger animations on scroll (replaces IntersectionObserver)
- `Motion.stagger(delay)` — stagger animations across child elements
- `Motion.spring({ stiffness, damping })` — spring physics easing
- `Motion.scroll(animation)` — link animations to scroll progress

**Default animation patterns:**
- **Hero entrance:** spring fade+slide with orchestrated title → subtitle → CTA (150ms stagger)
- **Card grids:** `Motion.stagger(0.08)` with spring ease, `y: [40, 0]`, `scale: [0.95, 1]`
- **Scroll reveals:** `Motion.inView()` with spring ease — BUT set `opacity: 0` via JS, not CSS (so content is visible without JS)
- **Stat counters:** animate numbers from 0 to target on scroll-in
- **Hover micro-interactions:** `scale: 1.02, y: -4` on mouseenter with spring
- **Slide transitions:** spring-based translateX with orchestrated exit/enter

**Rules:**
- Always check `prefers-reduced-motion` before running animations — show everything immediately if reduced
- Never hide content via CSS for scroll animations — hide via JS so print/screenshot shows all content
- Prefer animating `opacity`, `transform`, `scale`, `x`, `y` (GPU-accelerated)
- Avoid animating `width`, `height`, `margin` (triggers layout reflow)

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

## Mandatory HTML Skeleton

**EVERY visualization MUST start from this skeleton.** Do not write HTML from scratch. Copy this, then add content. This ensures light theme, print styles, Inter font, animations, reduced-motion, and menu are never missing.

```html
<!DOCTYPE html>
<html lang="en" class="theme-dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>YOUR TITLE HERE</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
  <!-- ADD CDN LIBRARIES HERE (Chart.js, Mermaid, etc.) -->
  <script src="https://cdn.jsdelivr.net/npm/motion@12/dist/motion.js"></script>
  <script src="https://cdn.jsdelivr.net/npm/html-to-image@1.11.11/dist/html-to-image.js"></script>
  <style>
    /* ===== RESET & BASE ===== */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    
    /* ===== THEME SYSTEM (REQUIRED — both themes must exist) ===== */
    :root, .theme-dark {
      --bg: #030712;
      --surface: #111827;
      --surface-hover: #1f2937;
      --border: rgba(255,255,255,0.08);
      --text: #f9fafb;
      --text-secondary: #9ca3af;
      --accent: #3b82f6;
      --accent-secondary: #8b5cf6;
      --positive: #10b981;
      --negative: #f43f5e;
      --warning: #f59e0b;
    }
    .theme-light {
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
    
    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background: var(--bg);
      color: var(--text);           /* CRITICAL: always use var(--text), never rely on defaults */
      line-height: 1.6;
      -webkit-font-smoothing: antialiased;
      transition: background 0.3s, color 0.3s;
    }
    
    /* ===== GLASS CARD (reuse everywhere) ===== */
    .card {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 24px;
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
    }
    
    /* ===== TEXT COLORS (NEVER use raw white/black — always CSS vars) ===== */
    h1, h2, h3, h4, h5, h6 { color: var(--text); }
    p, li, td, th, span, label { color: var(--text); }
    .text-secondary { color: var(--text-secondary); }
    
    /* ===== ANIMATIONS (Motion.js handles these — CSS fallback only) ===== */
    /* Motion.js provides spring physics via JS. These CSS classes are fallbacks. */
    @keyframes fadeInUp {
      from { opacity: 0; transform: translateY(24px); }
      to { opacity: 1; transform: translateY(0); }
    }
    
    /* ===== REDUCED MOTION (REQUIRED) ===== */
    @media (prefers-reduced-motion: reduce) {
      *, *::before, *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
      }
    }
    
    /* ===== PRINT STYLES (REQUIRED) ===== */
    @media print {
      body { background: white !important; color: black !important; }
      .viz-menu { display: none !important; }
      .card { break-inside: avoid; border: 1px solid #ddd; box-shadow: none; }
      * { print-color-adjust: exact; -webkit-print-color-adjust: exact; }
    }
    
    /* ===== HAMBURGER MENU ===== */
    .viz-menu { position: fixed; top: 16px; right: 16px; z-index: 9999; }
    .viz-menu-toggle {
      width: 44px; height: 44px; border-radius: 12px;
      background: var(--surface); border: 1px solid var(--border);
      color: var(--text); cursor: pointer; display: flex;
      align-items: center; justify-content: center;
      backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
      transition: all 0.2s;
    }
    .viz-menu-toggle:hover { background: var(--surface-hover); }
    .viz-menu-dropdown {
      position: absolute; top: 52px; right: 0; min-width: 200px;
      background: var(--surface); border: 1px solid var(--border);
      border-radius: 12px; padding: 8px; opacity: 0; visibility: hidden;
      transform: translateY(-8px); transition: all 0.2s;
      backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
    }
    .viz-menu-dropdown.open { opacity: 1; visibility: visible; transform: translateY(0); }
    .viz-menu-dropdown button {
      width: 100%; padding: 10px 14px; border: none; border-radius: 8px;
      background: transparent; color: var(--text); font-size: 14px;
      font-family: inherit; cursor: pointer; text-align: left;
      display: flex; align-items: center; gap: 10px; transition: background 0.15s;
    }
    .viz-menu-dropdown button:hover { background: var(--surface-hover); }
    
    /* ===== YOUR CUSTOM STYLES BELOW ===== */
  </style>
</head>
<body>

  <!-- MENU (REQUIRED — copy exactly) -->
  <div class="viz-menu">
    <button class="viz-menu-toggle" onclick="toggleMenu()" aria-label="Menu">
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
        <line x1="3" y1="5" x2="17" y2="5"/>
        <line x1="3" y1="10" x2="17" y2="10"/>
        <line x1="3" y1="15" x2="17" y2="15"/>
      </svg>
    </button>
    <div class="viz-menu-dropdown" id="vizMenuDropdown">
      <button onclick="cycleTheme()">
        <span id="themeIcon">🌙</span>
        <span id="themeLabel">Dark</span>
      </button>
      <button onclick="downloadImage()">
        <span>📥</span>
        <span>Download PNG</span>
      </button>
      <button onclick="window.print()">
        <span>🖨️</span>
        <span>Print / PDF</span>
      </button>
    </div>
  </div>

  <!-- YOUR CONTENT HERE -->

  <script>
    // Menu
    function toggleMenu() {
      document.getElementById('vizMenuDropdown').classList.toggle('open');
    }
    document.addEventListener('click', e => {
      if (!e.target.closest('.viz-menu')) {
        document.getElementById('vizMenuDropdown').classList.remove('open');
      }
    });
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape') document.getElementById('vizMenuDropdown').classList.remove('open');
    });

    // Theme
    const themes = ['dark', 'light'];
    const themeIcons = { dark: '🌙', light: '☀️' };
    let currentTheme = localStorage.getItem('viz-theme') || 'dark';
    function applyTheme(t) {
      document.documentElement.className = 'theme-' + t;
      document.getElementById('themeIcon').textContent = themeIcons[t];
      document.getElementById('themeLabel').textContent = t.charAt(0).toUpperCase() + t.slice(1);
      localStorage.setItem('viz-theme', t);
      currentTheme = t;
    }
    function cycleTheme() {
      const next = themes[(themes.indexOf(currentTheme) + 1) % themes.length];
      applyTheme(next);
    }
    applyTheme(currentTheme);

    // Motion.js animations (spring physics, scroll reveals)
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (!prefersReducedMotion && typeof Motion !== 'undefined') {
      // Staggered entrance for cards/sections
      Motion.animate('.card, .animate-in',
        { opacity: [0, 1], y: [30, 0] },
        { delay: Motion.stagger(0.08), duration: 0.5, ease: Motion.spring({ stiffness: 200, damping: 22 }) }
      );
      // Hover micro-interactions on cards
      document.querySelectorAll('.card').forEach(card => {
        card.addEventListener('mouseenter', () => Motion.animate(card, { scale: 1.02, y: -4 }, { duration: 0.2 }));
        card.addEventListener('mouseleave', () => Motion.animate(card, { scale: 1, y: 0 }, { duration: 0.3 }));
      });
      // Add more Motion animations for your specific content here
    }

    // Download PNG
    async function downloadImage() {
      const menu = document.querySelector('.viz-menu');
      menu.style.display = 'none';
      try {
        const dataUrl = await htmlToImage.toPng(document.body, {
          quality: 1, pixelRatio: 2,
          filter: n => !n.classList?.contains('viz-menu')
        });
        const a = document.createElement('a');
        a.href = dataUrl;
        a.download = document.title.replace(/\s+/g, '-').toLowerCase() + '.png';
        a.click();
      } catch(e) { console.error('Download failed:', e); }
      menu.style.display = '';
    }
  </script>
</body>
</html>
```

**Non-negotiable rules for the skeleton:**
- NEVER omit `.theme-light` — both themes must exist
- NEVER use raw colors like `white`, `#fff`, `black` — always `var(--text)`, `var(--bg)`, etc.
- NEVER omit `@media print` or `@media (prefers-reduced-motion: reduce)`
- NEVER use a menu class other than `.viz-menu`, `.viz-menu-toggle`, `.viz-menu-dropdown`
- ALWAYS include `html-to-image` CDN and the download function
- ALWAYS set `<html lang="en" class="theme-dark">`
- ALWAYS use Inter font — it's loaded in the skeleton

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
- **Minimum chart height:** 300px on desktop, 250px on mobile
- **Set `maintainAspectRatio: false`** and control size via CSS container
- **Use theme-aware colors:** read CSS vars at render time, re-render on theme change
- **Chart text colors:** set `Chart.defaults.color = getComputedStyle(root).getPropertyValue('--text-secondary').trim()`
- **Grid line colors:** use `var(--border)` value
- **Legend position:** 'top' for horizontal charts, 'right' for vertical with space
- **Responsive:** `responsive: true` is default, but container must have explicit dimensions

```javascript
// Theme-aware Chart.js setup (include in every chart visualization)
function getChartColors() {
  const s = getComputedStyle(document.documentElement);
  return {
    text: s.getPropertyValue('--text').trim(),
    textSecondary: s.getPropertyValue('--text-secondary').trim(),
    border: s.getPropertyValue('--border').trim(),
    surface: s.getPropertyValue('--surface').trim(),
    accent: s.getPropertyValue('--accent').trim(),
  };
}
// Call this and update charts whenever theme changes
```

## Process

1. **Understand** — what's the message? Who's the audience? What format fits?
2. **Start from skeleton** — copy the Mandatory HTML Skeleton above. NEVER start from a blank file.
3. **Structure** — outline content/sections BEFORE filling in the skeleton
4. **Build** — add content, charts, styles. Keep all colors as CSS vars.
5. **Verify checklist:**
   - [ ] Both `.theme-dark` and `.theme-light` defined?
   - [ ] All text uses `var(--text)` or `var(--text-secondary)`?
   - [ ] `@media print` hides menu, forces white bg?
   - [ ] `@media (prefers-reduced-motion: reduce)` present?
   - [ ] `.viz-menu` with toggle, theme, download, print?
   - [ ] Inter font loaded and applied?
   - [ ] Entrance animations with staggered delays?
   - [ ] All charts have explicit container sizing (≥300px height)?
   - [ ] Hero/title text visible on both themes?

The quality bar: **"good, period"** — not "good for AI-generated."
