#!/usr/bin/env python3
"""Fix all remaining issues from the deep audit."""
import re, os

REPORTS = "Industry_Demo_Reports"

# ── 1. Convert remaining blank line placeholders to sig blocks ───────────────
# Pattern: blank line div + <p> label immediately after (single or multi)
# These weren't caught before because they use different spacing/structure

MINI_SIG = """<div class="vv-sig-block">
                        <div class="vv-sig-container">
                            <div class="vv-sig-fields">
                                <div>
                                    <div class="vv-sig-field-label">{label}</div>
                                    <input type="text" class="vv-sig-text" placeholder="Type full name to sign" autocomplete="off" spellcheck="false">
                                </div>
                                <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
                                    <div>
                                        <div class="vv-sig-field-label">DATE SIGNED</div>
                                        <input type="date" class="vv-date-input">
                                    </div>
                                    <div>
                                        <div class="vv-sig-field-label">TITLE / CREDENTIALS</div>
                                        <input type="text" class="vv-sig-text" placeholder="Title, certifications..." autocomplete="off">
                                    </div>
                                </div>
                            </div>
                            <button class="vv-lock-btn">🔐 &nbsp; SIGN &amp; LOCK ATTESTATION</button>
                        </div>
                        <div class="vv-locked-badge">
                            <span>✓ DIGITALLY SIGNED &amp; LOCKED</span>
                            <span class="vv-lock-timestamp"></span>
                            <button class="vv-sig-unlock-btn" title="Unlock">✕ unlock</button>
                        </div>
                    </div>"""

def replace_blank_lines(content):
    """Replace border-bottom blank lines + following label paragraph(s) with sig blocks."""
    # Pattern: blank line div followed by 1-2 label paragraphs
    pattern = re.compile(
        r'<div style="border-bottom:1px solid var\(--border[^>]*\);\s*height:3[46]px;[^>]*"></div>\s*'
        r'(<p style="[^>]*">([^<]+)</p>\s*)'
        r'(?:<p style="[^>]*">[^<]+</p>\s*)?',
        re.DOTALL
    )
    def replacer(m):
        # Extract the first label (most meaningful one)
        label_text = m.group(2).strip()
        # Clean up HTML entities
        label = label_text.replace('&amp;', '&').replace('&nbsp;', ' ').upper()
        # If it's just a date placeholder, make it a more sensible label
        if 'YYYY-MM-DD' in label or label.startswith('DATE'):
            label = 'DATE SIGNED'
        return MINI_SIG.format(label=label)
    return pattern.sub(replacer, content)


def fix_file(fname):
    fpath = os.path.join(REPORTS, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    # Count before
    before = len(re.findall(r'border-bottom:1px solid.*?height:3[46]px', content))

    content = replace_blank_lines(content)

    after = len(re.findall(r'border-bottom:1px solid.*?height:3[46]px', content))

    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ {fname}: converted {before - after} blank lines ({after} remaining)")
    else:
        if after > 0:
            print(f"  ! {fname}: {after} blank lines NOT converted (pattern may differ)")
        else:
            print(f"  - {fname}: no changes needed")


# ── 2. Fix stale "12" count references ──────────────────────────────────────
def fix_stale_counts():
    # index.html hub
    fpath = 'index.html'
    with open(fpath, 'r') as f:
        c = f.read()
    orig = c
    c = c.replace('12 specialized forensic demonstrations', '16 specialized forensic demonstrations')
    c = c.replace('>All 12 Reports<', '>All 16 Reports<')
    c = c.replace('All 12 Reports', 'All 16 Reports')
    if c != orig:
        with open(fpath, 'w') as f:
            f.write(c)
        print("  ✓ index.html: stale '12' counts updated")

    # Industry_Demo_Reports/index.html
    fpath2 = os.path.join(REPORTS, 'index.html')
    with open(fpath2, 'r') as f:
        c = f.read()
    orig = c
    c = c.replace('12 professional forensic reports', '16 professional forensic reports')
    if c != orig:
        with open(fpath2, 'w') as f:
            f.write(c)
        print("  ✓ Industry_Demo_Reports/index.html: stale '12' updated")


# ── 3. Fix CLAUDE.md ─────────────────────────────────────────────────────────
def fix_claude_md():
    fpath = 'CLAUDE.md'
    with open(fpath, 'r') as f:
        c = f.read()
    orig = c
    c = c.replace('— 12 industry reports', '— 16 industry reports')
    c = c.replace('# 12 industry-specific forensic reports', '# 16 industry-specific forensic reports')
    if c != orig:
        with open(fpath, 'w') as f:
            f.write(c)
        print("  ✓ CLAUDE.md: report counts updated")


# ── 4. Remove duplicate .attestation CSS in government_fisma_report.html ────
def fix_duplicate_css():
    fpath = os.path.join(REPORTS, 'government_fisma_report.html')
    with open(fpath, 'r') as f:
        c = f.read()
    orig = c
    # The duplicate is two identical .attestation rules — remove the second one
    dupe = '.attestation { border: 1px solid var(--border); padding: 24px; margin: 20px 0; border-radius: 2px; }'
    idx1 = c.find(dupe)
    if idx1 != -1:
        idx2 = c.find(dupe, idx1 + 1)
        if idx2 != -1:
            c = c[:idx2] + c[idx2 + len(dupe):]
            with open(fpath, 'w') as f:
                f.write(c)
            print("  ✓ government_fisma_report.html: duplicate .attestation CSS removed")
        else:
            print("  - government_fisma_report.html: no duplicate found")


# ── 5. Standardize Google Fonts weights across all reports ──────────────────
def fix_font_weights():
    STANDARD_FONTS = 'https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Rajdhani:wght@400;600;700&family=Share+Tech+Mono&family=Outfit:wght@300;400;500&display=swap'
    fixed = []
    for fname in os.listdir(REPORTS):
        if not fname.endswith('.html') or fname == 'index.html':
            continue
        fpath = os.path.join(REPORTS, fname)
        with open(fpath, 'r') as f:
            c = f.read()
        orig = c
        # Replace any variant of the Google Fonts URL
        c = re.sub(
            r'https://fonts\.googleapis\.com/css2\?family=Orbitron[^"]+',
            STANDARD_FONTS,
            c
        )
        if c != orig:
            with open(fpath, 'w') as f:
                f.write(c)
            fixed.append(fname)
    if fixed:
        print(f"  ✓ Standardized fonts in: {', '.join(fixed)}")
    else:
        print("  - Fonts already standardized")


# ── 6. Add missing footer to generic_compliance_report.html ─────────────────
def fix_missing_footer():
    fpath = os.path.join(REPORTS, 'generic_compliance_report.html')
    with open(fpath, 'r') as f:
        c = f.read()
    if '<div class="footer">' in c or 'class="footer"' in c:
        print("  - generic_compliance_report.html: footer already present")
        return
    # Find the closing container div before </body>
    footer_html = """
        <div class="footer">
            <p><strong>Vatican Vault v2.0</strong> — Compliance &amp; Audit Platform</p>
            <p>Generated: 2026-03-01 | Audit ID: COMP-2026-030-001</p>
            <p style="margin-top:8px; font-size:11px;">CONFIDENTIAL — For authorized compliance personnel only</p>
            <p style="font-size:11px; margin-top:4px; color:#999;">Framework: NIST CSF · ISO 27001 · SOC 2 · Applicable Regulatory Standards</p>
        </div>"""
    # Insert before the last </div></body>
    c = c.replace('</div>\n</body>', footer_html + '\n    </div>\n</body>', 1)
    if 'class="footer"' not in c:
        # Try alternate pattern
        c = c.replace('</div>\r\n</body>', footer_html + '\n    </div>\r\n</body>', 1)
    with open(fpath, 'w') as f:
        f.write(c)
    print("  ✓ generic_compliance_report.html: footer HTML added")


if __name__ == '__main__':
    print("=== Fixing blank line placeholders ===")
    for fname in ['financial_report.html', 'generic_compliance_report.html',
                  'hr_employment_report.html', 'irm_report.html',
                  'law_enforcement_report.html', 'legal_ediscovery_report.html',
                  'mssp_report.html']:
        fix_file(fname)

    print("\n=== Fixing stale counts ===")
    fix_stale_counts()

    print("\n=== Fixing CLAUDE.md ===")
    fix_claude_md()

    print("\n=== Fixing duplicate CSS ===")
    fix_duplicate_css()

    print("\n=== Standardizing fonts ===")
    fix_font_weights()

    print("\n=== Fixing missing footer ===")
    fix_missing_footer()

    print("\nDone.")
