#!/usr/bin/env python3
"""Remove @media prefers-color-scheme blocks from all files to force class-based theming."""
import re, os

EXAMPLES = "/Users/alxahn/.openclaw/workspace/visualize/examples"

for fname in os.listdir(EXAMPLES):
    if not fname.endswith(".html"):
        continue
    fpath = os.path.join(EXAMPLES, fname)
    with open(fpath, "r") as f:
        html = f.read()
    
    original = html
    
    # Remove @media (prefers-color-scheme: dark) { :root { ... } } blocks
    html = re.sub(
        r'@media\s*\(prefers-color-scheme:\s*(?:dark|light)\)\s*\{\s*:root\s*\{[^}]*\}\s*\}',
        '',
        html
    )
    
    # Also remove JS-based prefers-color-scheme detection
    # Pattern: if (window.matchMedia...) or const saved = localStorage... with prefers-color-scheme fallback
    html = re.sub(
        r"if\s*\(!saved\s*&&\s*window\.matchMedia\(['\"].*?prefers-color-scheme.*?\)\.matches\)\s*\{[^}]*\}",
        "",
        html,
        flags=re.DOTALL
    )
    
    if html != original:
        with open(fpath, "w") as f:
            f.write(html)
        removed = len(original) - len(html)
        print(f"✅ {fname} — removed {removed} chars of prefers-color-scheme")
    else:
        print(f"⏭️  {fname} — no prefers-color-scheme blocks found")

print("\nDone!")
