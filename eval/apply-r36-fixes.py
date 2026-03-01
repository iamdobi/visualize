#!/usr/bin/env python3
"""Round 36 fixes: apply accent colors, force dark default, bolder accents, wow interactions."""
import re, os

EXAMPLES = "/Users/alxahn/.openclaw/workspace/visualize/examples"

# Fix 1: Unique accent colors per file
ACCENTS = {
    "ai-timeline": ("#14b8a6", "#0d9488"),  # teal
    "carousel-infographic": ("#8b5cf6", "#7c3aed"),  # violet
    "carousel-korean": ("#8b5cf6", "#7c3aed"),  # violet
    "carousel-threads": ("#f43f5e", "#e11d48"),  # rose
    "cheatsheet-claude-code": ("#f97316", "#ea580c"),  # orange
    "cheatsheet-git": ("#ef4444", "#dc2626"),  # red
    "comparison-infographic": ("#6366f1", "#4f46e5"),  # indigo
    "event-poster": ("#ec4899", "#db2777"),  # pink
    "process-guide": ("#06b6d4", "#0891b2"),  # cyan
    "quote-card": ("#f59e0b", "#d97706"),  # amber
    "saas-dashboard": ("#10b981", "#059669"),  # emerald
    "slide-deck-demo": ("#0ea5e9", "#0284c7"),  # sky
    "startup-pitch-deck": ("#8b5cf6", "#7c3aed"),  # violet
    "status-report": ("#3b82f6", "#2563eb"),  # blue
    "system-architecture": ("#6366f1", "#4f46e5"),  # indigo
}

for fname in os.listdir(EXAMPLES):
    if not fname.endswith(".html"):
        continue
    name = fname.replace(".html", "")
    if name not in ACCENTS:
        continue
    
    fpath = os.path.join(EXAMPLES, fname)
    with open(fpath, "r") as f:
        html = f.read()
    
    accent, accent2 = ACCENTS[name]
    
    # Fix 1: Replace accent colors in theme-dark and theme-light
    # Replace --accent: #0070f3 (or similar) with new accent
    html = re.sub(r'(--accent:\s*)#[0-9a-fA-F]{3,6}', rf'\g<1>{accent}', html)
    html = re.sub(r'(--accent-secondary:\s*)#[0-9a-fA-F]{3,6}', rf'\g<1>{accent2}', html)
    
    # Fix 2: Remove prefers-color-scheme auto-detection
    # Remove blocks like: if (window.matchMedia(...light...).matches) { ...replace...theme-light... }
    html = re.sub(
        r"if\s*\(window\.matchMedia\(['\"].*?prefers-color-scheme:\s*light.*?['\"\)]+\.matches\)\s*\{[^}]*\}",
        "/* prefers-color-scheme detection removed - dark theme is default */",
        html,
        flags=re.DOTALL
    )
    # Also handle: const prefersDark = ... if (!prefersDark) patterns
    html = re.sub(
        r"const\s+prefersDark\s*=.*?;\s*if\s*\(!prefersDark\)\s*\{[^}]*\}",
        "/* prefers-color-scheme detection removed */",
        html,
        flags=re.DOTALL
    )
    # Also: const prefersLight = ... if (prefersLight) patterns  
    html = re.sub(
        r"const\s+prefersLight\s*=.*?;\s*if\s*\(prefersLight\)\s*\{[^}]*\}",
        "/* prefers-color-scheme detection removed */",
        html,
        flags=re.DOTALL
    )
    # Handle saved theme check that may restore light
    # Keep localStorage restore but remove system preference fallback
    html = re.sub(
        r"else\s+if\s*\(window\.matchMedia\(['\"].*?prefers-color-scheme:\s*light.*?['\"\)]+\.matches\)\s*\{[^}]*\}",
        "/* system preference detection removed */",
        html,
        flags=re.DOTALL
    )

    # Fix 4: Bolder accent in section headers - add CSS if not present
    # Add a subtle pulse animation for timeline dots (Fix 5 for timelines)
    if "timeline" in name:
        if "@keyframes pulse" not in html:
            pulse_css = """
    @keyframes pulse { 0%, 100% { box-shadow: 0 0 0 0 var(--accent); } 50% { box-shadow: 0 0 0 8px transparent; } }
    .timeline-dot, .era-marker { animation: pulse 2s ease-in-out infinite; }"""
            html = html.replace("</style>", pulse_css + "\n  </style>")
    
    # Fix 5: Hover scale on stat cards (dashboards, reports)
    if any(x in name for x in ["dashboard", "report", "comparison"]):
        if "hover-lift" not in html:
            hover_css = """
    .stat-card, .metric-card, .kpi-card { transition: transform 0.2s ease, box-shadow 0.2s ease; }
    .stat-card:hover, .metric-card:hover, .kpi-card:hover { transform: translateY(-2px); box-shadow: 0 8px 25px rgba(0,0,0,0.15); } /* hover-lift */"""
            html = html.replace("</style>", hover_css + "\n  </style>")
    
    # Fix 5: Quote card hover lift
    if "quote" in name:
        if "hover-lift" not in html:
            hover_css = """
    .quote-card { transition: transform 0.2s ease, box-shadow 0.2s ease; }
    .quote-card:hover { transform: translateY(-4px); box-shadow: 0 12px 30px rgba(0,0,0,0.12); } /* hover-lift */"""
            html = html.replace("</style>", hover_css + "\n  </style>")
    
    # Fix 3: Bolder carousel covers - increase SVG opacity
    if any(x in name for x in ["carousel", "slide-deck", "pitch"]):
        # Increase faint SVG opacity
        html = re.sub(r'opacity:\s*0\.\d{1,2}(?=\s*[;}])', lambda m: 
            m.group().replace(m.group().split(':')[1].strip().rstrip(';'), ' 0.5') 
            if float(m.group().split(':')[1].strip().rstrip(';')) < 0.2 
            else m.group(), html)
        # Actually simpler: just find very low opacities and bump them
        def bump_opacity(match):
            val = float(match.group(1))
            if val < 0.15:
                return f"opacity: 0.5"
            return match.group(0)
        html = re.sub(r'opacity:\s*(0\.\d+)', bump_opacity, html)
    
    with open(fpath, "w") as f:
        f.write(html)
    
    print(f"✅ {fname} — accent={accent}")

print("\nDone! All 15 files updated.")
