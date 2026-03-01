#!/usr/bin/env node
// R38 Fix Script: Apply research findings systematically across all 15 HTML files
const fs = require('fs');
const path = require('path');

const dir = path.join(__dirname, '..', 'examples');
const files = fs.readdirSync(dir).filter(f => f.endsWith('.html'));

let totalChanges = 0;

files.forEach(file => {
  const fp = path.join(dir, file);
  let html = fs.readFileSync(fp, 'utf8');
  const original = html;
  let changes = [];

  // 1. Typography: font-weight 800 → 700 (except for labels/eyebrows where 800 → 700 too)
  const before800 = (html.match(/font-weight:\s*800/g) || []).length;
  html = html.replace(/font-weight:\s*800/g, 'font-weight: 700');
  if (before800 > 0) changes.push(`font-weight 800→700 (${before800}x)`);

  // 2. Add font-feature-settings to body if missing
  if (!html.includes('font-feature-settings')) {
    // Add it after -webkit-font-smoothing if present, otherwise after font-family in body
    if (html.includes('-webkit-font-smoothing: antialiased;')) {
      html = html.replace(
        '-webkit-font-smoothing: antialiased;',
        "-webkit-font-smoothing: antialiased;\n      font-feature-settings: 'cv11', 'ss01';"
      );
      changes.push('added font-feature-settings');
    }
  }

  // 3. Remove colored left borders on cards (anti-pattern)
  // Replace border-left: 3px solid var(--accent) etc with just removing them
  // Be careful not to remove structural borders
  const borderLeftPattern = /border-left:\s*[234]px\s+solid\s+(?:var\(--(?:accent|positive|negative|warning|accent-secondary)\)|#[0-9a-fA-F]{3,8})/g;
  const blMatches = html.match(borderLeftPattern);
  if (blMatches) {
    html = html.replace(borderLeftPattern, 'border-left: 3px solid transparent');
    changes.push(`colored left-borders → transparent (${blMatches.length}x)`);
  }

  // 4. Ensure Inter font weight range includes 300-900 (some only have 300-700)
  html = html.replace(
    /family=Inter:wght@300;400;500;600;700(?:;800;900)?&/g,
    'family=Inter:wght@300;400;500;600;700&'
  );

  // 5. Add letter-spacing: -0.011em to body if not present (refined body text)
  if (!html.includes('letter-spacing: -0.01') && !html.includes('letter-spacing:-0.01')) {
    // Add to body style block
    if (html.includes("line-height: 1.6;") && !html.includes('letter-spacing: -0.01')) {
      html = html.replace(
        'line-height: 1.6;',
        'line-height: 1.6; letter-spacing: -0.011em;'
      );
      changes.push('added body letter-spacing -0.011em');
    }
  }

  if (html !== original) {
    fs.writeFileSync(fp, html);
    totalChanges += changes.length;
    console.log(`✅ ${file}: ${changes.join(', ')}`);
  } else {
    console.log(`⏭️  ${file}: no changes needed`);
  }
});

console.log(`\n📊 Total: ${totalChanges} changes across ${files.length} files`);
