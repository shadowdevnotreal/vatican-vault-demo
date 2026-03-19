#!/usr/bin/env python3
"""
Fix three things across all HTML files:
1. Convert old light-theme reports to dark theme
2. Add target="_blank" to card/content links that need it
3. Add interactive signature/date/lock widget to all attestation sections
"""
import re, os

REPORTS_DIR = "Industry_Demo_Reports"

# ─── Dark theme CSS variable replacements ───────────────────────────────────
LIGHT_TO_DARK_VARS = {
    "--bg:         #f7f8fa":   "--bg:         #04080f",
    "--bg:        #f7f8fa":    "--bg:        #04080f",
    "--surface:    #ffffff":   "--surface:    #0a1220",
    "--surface:   #ffffff":    "--surface:   #0a1220",
    "--border:     #e4e8ef":   "--border:     #1e2a3e",
    "--border:    #e4e8ef":    "--border:    #1e2a3e",
    "--text:       #1a2030":   "--text:       #d8e8f5",
    "--text:      #1a2030":    "--text:      #d8e8f5",
    "--text-mid:   #4a5568":   "--text-mid:   #8899aa",
    "--text-mid:  #4a5568":    "--text-mid:  #8899aa",
    "--text-dim:   #8896a8":   "--text-dim:   #6b86a0",
    "--text-dim:  #8896a8":    "--text-dim:  #6b86a0",
}

# Also replace hardcoded light values in CSS blocks
LIGHT_CSS_REPLACEMENTS = [
    # case-info box
    (r'background:\s*#f1f4f8', 'background: rgba(255,255,255,0.04)'),
    (r'background:\s*#f8f9fa', 'background: rgba(255,255,255,0.04)'),
    (r'background:\s*#eff6ff', 'background: rgba(26,86,219,0.08)'),
    (r'background:\s*#fef2f2', 'background: rgba(220,38,38,0.08)'),
    (r'background:\s*#f0fdf4', 'background: rgba(16,185,129,0.08)'),
    (r'background:\s*#fefce8', 'background: rgba(245,158,11,0.08)'),
    (r'box-shadow:\s*0 4px 24px rgba\(0,0,0,0\.06\)', 'box-shadow: 0 4px 24px rgba(0,0,0,0.5)'),
    # text colors that reference hardcoded light-theme colors
    (r'color:\s*#1a2030\b', 'color: var(--text)'),
    (r'color:\s*#4a5568\b', 'color: var(--text-mid)'),
    (r'color:\s*#8896a8\b', 'color: var(--text-dim)'),
    # table backgrounds
    (r'background:\s*#f8fafc', 'background: rgba(255,255,255,0.04)'),
    (r'background-color:\s*#f1f4f8', 'background-color: rgba(255,255,255,0.04)'),
    # border colors
    (r'border-color:\s*#e4e8ef', 'border-color: var(--border)'),
    # link color override for dark bg
    (r'color:\s*#2563eb\b', 'color: var(--accent)'),
    # body padding (keep, but fix background)
    (r'(body\s*\{[^}]*?)background:\s*var\(--bg\);(\s*color:\s*var\(--text\))',
     r'\1background: var(--bg);\2'),
]


# ─── Signature / Date / Lock Widget JS ─────────────────────────────────────
SIG_WIDGET_JS = """
<!-- VV Signature & Lock Widget -->
<style>
.vv-sig-block {
  border: 1px solid var(--border, #1e2a3e);
  padding: 0;
  margin: 4px 0 0 0;
  border-radius: 2px;
  transition: all 0.3s;
  position: relative;
  overflow: hidden;
}
.vv-sig-block.locked {
  border-color: #10b981;
  background: rgba(16,185,129,0.04);
}
.vv-sig-input-row {
  display: flex; align-items: center; gap: 0;
}
.vv-sig-text {
  flex: 1;
  background: transparent;
  border: none;
  border-bottom: 1px solid var(--border, #1e2a3e);
  color: var(--text, #d8e8f5);
  font-family: 'Georgia', serif;
  font-size: 16px;
  font-style: italic;
  padding: 8px 12px;
  outline: none;
  transition: border-color 0.2s;
  width: 100%;
  display: block;
}
.vv-sig-text:focus { border-color: var(--accent, #00d4ff); }
.vv-sig-text::placeholder { font-family: 'Share Tech Mono', monospace; font-size: 12px; font-style: normal; color: var(--text-muted, #6b86a0); }
.vv-sig-text[readonly] {
  color: #10b981;
  font-style: italic;
  font-size: 18px;
  border-bottom-color: #10b981;
  cursor: not-allowed;
}
.vv-date-input {
  background: transparent;
  border: none;
  border-bottom: 1px solid var(--border, #1e2a3e);
  color: var(--text, #d8e8f5);
  font-family: 'Share Tech Mono', monospace;
  font-size: 12px;
  padding: 8px 12px;
  outline: none;
  width: 100%;
  display: block;
  transition: border-color 0.2s;
  color-scheme: dark;
}
.vv-date-input:focus { border-color: var(--accent, #00d4ff); }
.vv-date-input[readonly] {
  color: #10b981;
  border-bottom-color: #10b981;
  cursor: not-allowed;
}
.vv-lock-btn {
  display: block;
  width: 100%;
  margin-top: 12px;
  padding: 10px 0;
  background: transparent;
  border: 1px solid var(--accent, #00d4ff);
  color: var(--accent, #00d4ff);
  font-family: 'Share Tech Mono', monospace;
  font-size: 11px;
  letter-spacing: 0.18em;
  cursor: pointer;
  border-radius: 2px;
  transition: all 0.2s;
}
.vv-lock-btn:hover { background: rgba(0,212,255,0.08); }
.vv-lock-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  pointer-events: none;
}
.vv-locked-badge {
  display: none;
  align-items: center;
  gap: 10px;
  padding: 8px 14px;
  background: rgba(16,185,129,0.1);
  border-top: 1px solid rgba(16,185,129,0.3);
  font-family: 'Share Tech Mono', monospace;
  font-size: 10px;
  letter-spacing: 0.14em;
  color: #10b981;
}
.vv-locked-badge.visible { display: flex; }
.vv-sig-container { padding: 16px; }
.vv-sig-fields { display: grid; gap: 12px; margin-bottom: 12px; }
.vv-sig-field-label {
  font-family: 'Share Tech Mono', monospace;
  font-size: 10px;
  letter-spacing: 0.12em;
  color: var(--text-muted, #6b86a0);
  margin-bottom: 4px;
}
.vv-sig-unlock-btn {
  font-family: 'Share Tech Mono', monospace;
  font-size: 10px;
  letter-spacing: 0.12em;
  background: none;
  border: none;
  color: rgba(16,185,129,0.5);
  cursor: pointer;
  margin-left: auto;
  padding: 2px 6px;
}
.vv-sig-unlock-btn:hover { color: #10b981; }
@media print {
  .vv-lock-btn, .vv-sig-unlock-btn { display: none !important; }
  .vv-sig-text { border-bottom: 1px solid rgba(0,0,0,0.2) !important; }
}
</style>
<script>
(function(){
  // Initialize all signature blocks
  document.addEventListener('DOMContentLoaded', function() {
    initSigBlocks();
    loadSigState();
  });
  // Also try immediately in case DOM is ready
  if (document.readyState !== 'loading') {
    setTimeout(function() { initSigBlocks(); loadSigState(); }, 50);
  }

  function initSigBlocks() {
    document.querySelectorAll('.vv-sig-block').forEach(function(block) {
      var lockBtn = block.querySelector('.vv-lock-btn');
      if (!lockBtn) return;
      lockBtn.addEventListener('click', function() { lockBlock(block); });

      var unlockBtn = block.querySelector('.vv-sig-unlock-btn');
      if (unlockBtn) {
        unlockBtn.addEventListener('click', function(e) {
          e.stopPropagation();
          if (confirm('Unlock and clear this signature?')) { unlockBlock(block); }
        });
      }

      // Set today's date on any date inputs
      var today = new Date().toISOString().split('T')[0];
      block.querySelectorAll('.vv-date-input:not([readonly])').forEach(function(d) {
        if (!d.value) d.value = today;
      });
    });
  }

  function lockBlock(block) {
    var sigs = block.querySelectorAll('.vv-sig-text');
    var dates = block.querySelectorAll('.vv-date-input');
    var hasAllSigs = true;

    sigs.forEach(function(s) {
      if (!s.value.trim()) hasAllSigs = false;
    });
    if (!hasAllSigs) {
      alert('Please enter all required signatures before locking.');
      return;
    }

    // Lock all inputs
    sigs.forEach(function(s) { s.readOnly = true; });
    dates.forEach(function(d) { d.readOnly = true; });

    // Visual lock state
    block.classList.add('locked');
    var lockBtn = block.querySelector('.vv-lock-btn');
    if (lockBtn) lockBtn.disabled = true;

    var badge = block.querySelector('.vv-locked-badge');
    if (badge) {
      badge.classList.add('visible');
      var ts = badge.querySelector('.vv-lock-timestamp');
      if (ts) ts.textContent = new Date().toISOString().replace('T',' ').slice(0,19) + ' UTC';
    }

    // Save state to localStorage
    saveSigState();
  }

  function unlockBlock(block) {
    block.querySelectorAll('.vv-sig-text').forEach(function(s) { s.readOnly = false; s.value = ''; });
    block.querySelectorAll('.vv-date-input').forEach(function(d) { d.readOnly = false; });
    block.classList.remove('locked');
    var lockBtn = block.querySelector('.vv-lock-btn');
    if (lockBtn) lockBtn.disabled = false;
    var badge = block.querySelector('.vv-locked-badge');
    if (badge) badge.classList.remove('visible');
    saveSigState();
  }

  function getSigKey() {
    return 'vv_sigs_' + window.location.pathname.replace(/[^a-z0-9]/gi, '_');
  }

  function saveSigState() {
    var state = [];
    document.querySelectorAll('.vv-sig-block').forEach(function(block, i) {
      var entry = { idx: i, locked: block.classList.contains('locked'), sigs: [], dates: [] };
      block.querySelectorAll('.vv-sig-text').forEach(function(s) { entry.sigs.push(s.value); });
      block.querySelectorAll('.vv-date-input').forEach(function(d) { entry.dates.push(d.value); });
      var badge = block.querySelector('.vv-lock-timestamp');
      entry.timestamp = badge ? badge.textContent : '';
      state.push(entry);
    });
    try { localStorage.setItem(getSigKey(), JSON.stringify(state)); } catch(e) {}
  }

  function loadSigState() {
    var raw;
    try { raw = localStorage.getItem(getSigKey()); } catch(e) { return; }
    if (!raw) return;
    var state;
    try { state = JSON.parse(raw); } catch(e) { return; }
    var blocks = document.querySelectorAll('.vv-sig-block');
    state.forEach(function(entry) {
      var block = blocks[entry.idx];
      if (!block) return;
      var sigs = block.querySelectorAll('.vv-sig-text');
      var dates = block.querySelectorAll('.vv-date-input');
      entry.sigs.forEach(function(v, i) { if (sigs[i]) sigs[i].value = v; });
      entry.dates.forEach(function(v, i) { if (dates[i]) dates[i].value = v; });
      if (entry.locked) {
        sigs.forEach(function(s) { s.readOnly = true; });
        dates.forEach(function(d) { d.readOnly = true; });
        block.classList.add('locked');
        var lockBtn = block.querySelector('.vv-lock-btn');
        if (lockBtn) lockBtn.disabled = true;
        var badge = block.querySelector('.vv-locked-badge');
        if (badge) {
          badge.classList.add('visible');
          var ts = badge.querySelector('.vv-lock-timestamp');
          if (ts && entry.timestamp) ts.textContent = entry.timestamp;
        }
      }
    });
  }
})();
</script>
"""


def make_sig_block(role_label, sig_placeholder="Type full name to sign", show_certnum=False):
    """Return an interactive signature block HTML."""
    return f"""<div class="vv-sig-block">
                    <div class="vv-sig-container">
                        <div class="vv-sig-fields">
                            <div>
                                <div class="vv-sig-field-label">{role_label.upper()} — SIGNATURE</div>
                                <input type="text" class="vv-sig-text" placeholder="{sig_placeholder}" autocomplete="off" spellcheck="false">
                            </div>
                            <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
                                <div>
                                    <div class="vv-sig-field-label">DATE SIGNED</div>
                                    <input type="date" class="vv-date-input">
                                </div>
                                <div>
                                    <div class="vv-sig-field-label">TITLE / CERTIFICATION{' / LICENSE NO.' if show_certnum else ''}</div>
                                    <input type="text" class="vv-sig-text" placeholder="Title, credentials..." autocomplete="off">
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


# ─── Process old light-theme reports ───────────────────────────────────────

OLD_REPORTS = [
    "dfir_report.html",
    "enterprise_soc_report.html",
    "financial_report.html",
    "generic_compliance_report.html",
    "generic_executive_report.html",
    "generic_technical_report.html",
    "healthcare_report.html",
    "hr_employment_report.html",
    "irm_report.html",
    "law_enforcement_report.html",
    "mssp_report.html",
    "pentest_report.html",
]

def convert_to_dark(content, fname):
    """Replace light CSS vars and hardcoded light colors."""
    # Replace CSS variable values
    for old, new in LIGHT_TO_DARK_VARS.items():
        content = content.replace(old, new)

    # Replace hardcoded light colors inside <style> blocks
    style_match = re.search(r'(<style>)(.*?)(</style>)', content, re.DOTALL)
    if style_match:
        css = style_match.group(2)
        for pattern, replacement in LIGHT_CSS_REPLACEMENTS:
            css = re.sub(pattern, replacement, css)
        # Also flip any remaining white/light backgrounds in inline styles
        css = css.replace('background: white', 'background: var(--surface)')
        css = css.replace('background: #fff', 'background: var(--surface)')
        css = css.replace('background:#fff', 'background:var(--surface)')
        css = css.replace('color: #333', 'color: var(--text)')
        css = css.replace('color: #000', 'color: var(--text)')
        content = content[:style_match.start(2)] + css + content[style_match.end(2):]

    # Fix inline styles in HTML body (the case-info / info boxes)
    content = content.replace('background:#f1f4f8', 'background:rgba(255,255,255,0.04)')
    content = content.replace('background: #f1f4f8', 'background: rgba(255,255,255,0.04)')
    content = content.replace('background:#f8f9fa', 'background:rgba(255,255,255,0.04)')
    content = content.replace('background: #f8f9fa', 'background: rgba(255,255,255,0.04)')
    content = content.replace('background:#eff6ff', 'background:rgba(26,86,219,0.08)')
    content = content.replace('background: #eff6ff', 'background: rgba(26,86,219,0.08)')
    content = content.replace('background:#fef2f2', 'background:rgba(220,38,38,0.08)')
    content = content.replace('background: #fef2f2', 'background: rgba(220,38,38,0.08)')

    return content


def add_sig_widget_js(content):
    """Add signature widget JS before </body>."""
    if 'vv-sig-block' in content:
        return content  # already added
    return content.replace('</body>', SIG_WIDGET_JS + '\n</body>', 1)


def inject_sig_blocks(content, fname):
    """Replace static signature line placeholders with interactive sig blocks."""
    if 'vv-sig-block' in content:
        return content  # already done

    # Pattern: a signature area consisting of blank line divs + label paragraphs
    # Replace the interior of each signature column in attestation sections
    # Strategy: find <div style="border-bottom:1px solid...height:34px"> followed by
    # <p style="font-size:11px...">Signature... and replace the pair

    # Replace individual "blank line + label" signature placeholders
    sig_line_pattern = re.compile(
        r'<div style="border-bottom:1px solid var\(--border[^>]*\);\s*height:34px;[^>]*"></div>\s*'
        r'<p style="[^"]*">(Signature[^<]*)</p>',
        re.DOTALL
    )

    def sig_replacer(m):
        label_text = m.group(1).strip()
        # Determine role from context — just use the label text
        role = label_text.replace(' &amp; Title', '').replace(' / Title', '').strip()
        return f"""<div class="vv-sig-block">
                    <div class="vv-sig-container">
                        <div class="vv-sig-fields">
                            <div>
                                <div class="vv-sig-field-label">{role.upper()}</div>
                                <input type="text" class="vv-sig-text" placeholder="Type full name to sign" autocomplete="off" spellcheck="false">
                            </div>
                            <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
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

    new_content = sig_line_pattern.sub(sig_replacer, content)

    # Also handle multi-line signature blocks in new reports (where we have 3 separate blank divs + paragraphs)
    # Pattern for the newer attestation sections we built:
    # border-bottom + height:34px + margin...></div> + <p ...>Signature/Title/Date

    # More aggressive approach - find all signature line pairs
    sig_line2 = re.compile(
        r'<div style="border-bottom:1px solid var\(--border[^>]*\);\s*height:34px;[^>]*"></div>\s*'
        r'<p style="font-family:[^>]*">((?:Signature|Date|Title|Certif|Bar |Attorney|Auditor|License|Agency|Division)[^<]*)</p>',
        re.DOTALL
    )
    new_content = sig_line2.sub(sig_replacer, new_content)

    return new_content


# ─── Fix target="_blank" on card links ─────────────────────────────────────

def fix_target_blank_in_file(fpath):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Add target="_blank" to <a href="..." class="card"> that don't have it
    def add_target(m):
        tag = m.group(0)
        if 'target=' not in tag:
            tag = tag.replace('<a ', '<a target="_blank" ')
        return tag

    new_content = re.sub(r'<a\s+href="[^"]+\.html"[^>]*class="card"[^>]*>', add_target, new_content := content)
    # Also handle reversed attribute order
    new_content = re.sub(r'<a\s+[^>]*class="card"[^>]*href="[^"]+\.html"[^>]*>', add_target, new_content)

    if new_content != content:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False


def process_file(fpath, fname):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    changed = []

    # 1. Dark theme for old reports
    is_old_report = fname in OLD_REPORTS
    if is_old_report and '--bg:         #f7f8fa' in content or '--bg:        #f7f8fa' in content:
        content = convert_to_dark(content, fname)
        changed.append('dark-theme')

    # 2. Inject sig widget JS (all reports with attestation sections)
    if 'Attestation' in content and 'vv-sig-block' not in content:
        content = inject_sig_blocks(content, fname)
        content = add_sig_widget_js(content)
        changed.append('sig-widget')
    elif 'vv-sig-block' in content and 'vv-sig-block' in content:
        # Already has sig blocks, ensure JS is there
        if 'initSigBlocks' not in content:
            content = add_sig_widget_js(content)
            changed.append('sig-js')

    # 3. Fix target="_blank" on card links
    def add_target(m):
        tag = m.group(0)
        if 'target=' not in tag:
            return tag.replace('<a ', '<a target="_blank" ')
        return tag
    new_content = re.sub(r'<a\s+href="[^"#]+\.html"[^>]*class="card"[^>]*>', add_target, content)
    new_content = re.sub(r'<a\s+[^>]*class="card"[^>]*href="[^"#]+\.html"[^>]*>', add_target, new_content)
    if new_content != content:
        content = new_content
        changed.append('target-blank')

    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  ✓ {fname}: {', '.join(changed)}")
    else:
        print(f"  - {fname}: no changes")


# ─── Also fix index.html ───────────────────────────────────────────────────

def fix_hub_index():
    fpath = 'index.html'
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    def add_target(m):
        tag = m.group(0)
        if 'target=' not in tag:
            return tag.replace('<a ', '<a target="_blank" ')
        return tag

    # Card links without target="_blank"
    content = re.sub(r'<a\s+href="[^"#]+\.html"[^>]*class="card"[^>]*>', add_target, content)
    content = re.sub(r'<a\s+[^>]*class="card"[^>]*href="[^"#]+\.html"[^>]*>', add_target, content)

    # btn-outline "Browse Reports" link should open in new tab too
    content = content.replace(
        '<a href="Industry_Demo_Reports/index.html" class="btn-outline">Browse Reports</a>',
        '<a href="Industry_Demo_Reports/index.html" class="btn-outline" target="_blank">Browse Reports</a>'
    )

    if content != original:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print("  ✓ index.html: target-blank fixes")
    else:
        print("  - index.html: no changes")


if __name__ == '__main__':
    print("Processing all HTML files...")

    fix_hub_index()

    for fname in sorted(os.listdir(REPORTS_DIR)):
        if not fname.endswith('.html'):
            continue
        fpath = os.path.join(REPORTS_DIR, fname)
        process_file(fpath, fname)

    print("Done.")
