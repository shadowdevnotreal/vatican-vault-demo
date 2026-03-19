#!/usr/bin/env python3
"""
Enhance all industry reports:
1. Add attestation & certification sections
2. Add universal interactivity (print, collapse, back-to-top)
3. Upgrade per-report interactivity
"""
import re, os

REPORTS_DIR = "Industry_Demo_Reports"

# ──────────────────────────────────────────────────────────────────────────────
# UNIVERSAL INTERACTIVITY JS + CSS
# Injected before </body> in every report
# ──────────────────────────────────────────────────────────────────────────────
UNIVERSAL_JS = """
<!-- Vatican Vault Universal Interactivity -->
<style>
/* Print button */
#vv-print-btn {
  position: fixed;
  bottom: 28px;
  right: 28px;
  z-index: 9999;
  background: var(--accent, #00d4ff);
  color: #000;
  border: none;
  padding: 10px 18px;
  font-family: 'Share Tech Mono', 'Courier New', monospace;
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.08em;
  cursor: pointer;
  border-radius: 3px;
  box-shadow: 0 0 18px rgba(0,212,255,0.35);
  transition: opacity 0.2s, box-shadow 0.2s;
}
#vv-print-btn:hover { opacity: 0.85; box-shadow: 0 0 28px rgba(0,212,255,0.55); }

/* Back-to-top */
#vv-top-btn {
  position: fixed;
  bottom: 28px;
  right: 130px;
  z-index: 9999;
  background: rgba(255,255,255,0.08);
  border: 1px solid var(--accent, #00d4ff);
  color: var(--accent, #00d4ff);
  padding: 10px 14px;
  font-size: 14px;
  cursor: pointer;
  border-radius: 3px;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.3s;
}
#vv-top-btn.visible { opacity: 1; pointer-events: auto; }

/* Collapsible sections */
.vv-collapsible > h2, .section > h2.section-title {
  cursor: pointer;
  user-select: none;
  position: relative;
}
.vv-collapsible > h2::after, .section > h2.section-title::after {
  content: '▼';
  position: absolute;
  right: 0;
  font-size: 11px;
  opacity: 0.5;
  transition: transform 0.25s;
}
.vv-collapsed > h2.section-title::after, .vv-collapsed > h2::after {
  transform: rotate(-90deg);
}
.vv-collapsed .section-body { display: none; }

/* Highlight search */
.vv-highlight { background: rgba(255,200,0,0.35); border-radius: 2px; }

/* Tab navigation */
.vv-tabs { display: flex; gap: 6px; margin: 18px 0 0 0; flex-wrap: wrap; }
.vv-tab-btn {
  padding: 8px 16px;
  background: rgba(255,255,255,0.06);
  border: 1px solid var(--border, #1e2a38);
  color: var(--text-muted, #8899aa);
  font-family: 'Share Tech Mono', monospace;
  font-size: 11px;
  letter-spacing: 0.06em;
  cursor: pointer;
  border-radius: 2px;
  transition: all 0.2s;
}
.vv-tab-btn.active {
  background: var(--accent, #00d4ff);
  color: #000;
  border-color: var(--accent, #00d4ff);
}
.vv-tab-panel { display: none; }
.vv-tab-panel.active { display: block; }

/* Filter buttons */
.vv-filter-row { display: flex; gap: 8px; margin: 14px 0; flex-wrap: wrap; }
.vv-filter-btn {
  padding: 6px 14px;
  background: rgba(255,255,255,0.04);
  border: 1px solid var(--border, #1e2a38);
  color: var(--text-muted, #8899aa);
  font-family: 'Share Tech Mono', monospace;
  font-size: 11px;
  cursor: pointer;
  border-radius: 2px;
  transition: all 0.2s;
}
.vv-filter-btn.active, .vv-filter-btn:hover {
  border-color: var(--accent, #00d4ff);
  color: var(--accent, #00d4ff);
}
[data-severity].hidden { display: none; }

/* Expandable table rows */
.vv-expandable { cursor: pointer; }
.vv-expandable:hover { background: rgba(255,255,255,0.04) !important; }
.vv-expand-row { display: none; background: rgba(0,0,0,0.25) !important; }
.vv-expand-row.open { display: table-row; }
.vv-expand-row td { padding: 14px 20px; font-size: 13px; color: var(--text-muted, #8899aa); }

@media print {
  #vv-print-btn, #vv-top-btn, .vv-nav { display: none !important; }
  .vv-collapsed .section-body { display: block !important; }
}
</style>

<button id="vv-print-btn" onclick="window.print()">⎙ PRINT / PDF</button>
<button id="vv-top-btn" onclick="window.scrollTo({top:0,behavior:'smooth'})">↑ TOP</button>

<script>
(function(){
  // Back to top visibility
  window.addEventListener('scroll', function(){
    var btn = document.getElementById('vv-top-btn');
    if (btn) btn.classList.toggle('visible', window.scrollY > 400);
  });

  // Make sections collapsible
  document.querySelectorAll('.section').forEach(function(sec){
    var h2 = sec.querySelector('h2.section-title');
    if (!h2) return;
    // Wrap children after h2 in a body div
    var body = document.createElement('div');
    body.className = 'section-body';
    var children = Array.from(sec.childNodes).filter(function(n){
      return n !== h2;
    });
    children.forEach(function(c){ body.appendChild(c); });
    sec.appendChild(body);
    h2.addEventListener('click', function(){
      sec.classList.toggle('vv-collapsed');
    });
  });

  // Tab navigation helper (call initTabs() after page load for reports that use them)
  window.vvInitTabs = function(containerSelector){
    var container = document.querySelector(containerSelector);
    if (!container) return;
    var buttons = container.querySelectorAll('.vv-tab-btn');
    var panels = container.querySelectorAll('.vv-tab-panel');
    buttons.forEach(function(btn, i){
      btn.addEventListener('click', function(){
        buttons.forEach(function(b){ b.classList.remove('active'); });
        panels.forEach(function(p){ p.classList.remove('active'); });
        btn.classList.add('active');
        panels[i] && panels[i].classList.add('active');
      });
    });
    if (buttons[0]) buttons[0].click();
  };

  // Severity filter helper
  window.vvInitFilter = function(attr){
    document.querySelectorAll('.vv-filter-btn').forEach(function(btn){
      btn.addEventListener('click', function(){
        var val = btn.dataset.filter;
        document.querySelectorAll('.vv-filter-btn').forEach(function(b){ b.classList.remove('active'); });
        btn.classList.add('active');
        document.querySelectorAll('[data-severity]').forEach(function(row){
          if (val === 'all' || row.dataset.severity === val) {
            row.classList.remove('hidden');
          } else {
            row.classList.add('hidden');
          }
        });
      });
    });
    var allBtn = document.querySelector('.vv-filter-btn[data-filter="all"]');
    if (allBtn) allBtn.click();
  };

  // Expandable table rows
  window.vvInitExpandRows = function(){
    document.querySelectorAll('.vv-expandable').forEach(function(row){
      row.addEventListener('click', function(){
        var next = row.nextElementSibling;
        if (next && next.classList.contains('vv-expand-row')) {
          next.classList.toggle('open');
        }
      });
    });
  };
})();
</script>
"""

# ──────────────────────────────────────────────────────────────────────────────
# ATTESTATION SECTIONS per report
# ──────────────────────────────────────────────────────────────────────────────

ATTESTATIONS = {

"financial_report.html": """
        <div class="section">
            <h2 class="section-title"><span class="section-number">7.</span>SOX Attestation &amp; Certification</h2>
            <div class="section-body">
            <div style="background:rgba(255,255,255,0.04); border:1px solid var(--border,#1e2a38); border-left:4px solid var(--accent,#1e40af); padding:24px; border-radius:2px; margin-bottom:20px;">
                <p style="font-size:11px; letter-spacing:0.12em; color:var(--text-muted,#8899aa); margin-bottom:12px; font-family:'Share Tech Mono',monospace;">SOX §302 — DISCLOSURE CONTROLS CERTIFICATION (15 U.S.C. §7241)</p>
                <p style="font-size:13px; line-height:1.9;">Based on my knowledge, this report does not contain any untrue statement of a material fact or omit to state a material fact necessary in order to make the statements made, in light of the circumstances under which such statements were made, not misleading. The disclosure controls and procedures described herein are designed to ensure that information required to be disclosed is recorded, processed, summarized, and reported within the time periods specified by SEC rules and regulations. Vatican Vault's forensic audit trail has been reviewed and assessed as accurate and complete for purposes of this certification.</p>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:30px; margin-top:28px; padding-top:20px; border-top:1px solid var(--border,#1e2a38);">
                    <div>
                        <p style="font-size:12px; color:var(--text-muted,#8899aa); margin-bottom:8px;">CHIEF EXECUTIVE OFFICER</p>
                        <div style="border-bottom:1px solid var(--border,#1e2a38); height:36px; margin-bottom:8px;"></div>
                        <p style="font-size:11px; color:var(--text-muted,#8899aa);">Signature &amp; Title</p>
                        <div style="border-bottom:1px solid var(--border,#1e2a38); height:36px; margin:16px 0 8px;"></div>
                        <p style="font-size:11px; color:var(--text-muted,#8899aa);">Date (YYYY-MM-DD)</p>
                    </div>
                    <div>
                        <p style="font-size:12px; color:var(--text-muted,#8899aa); margin-bottom:8px;">CHIEF FINANCIAL OFFICER</p>
                        <div style="border-bottom:1px solid var(--border,#1e2a38); height:36px; margin-bottom:8px;"></div>
                        <p style="font-size:11px; color:var(--text-muted,#8899aa);">Signature &amp; Title</p>
                        <div style="border-bottom:1px solid var(--border,#1e2a38); height:36px; margin:16px 0 8px;"></div>
                        <p style="font-size:11px; color:var(--text-muted,#8899aa);">Date (YYYY-MM-DD)</p>
                    </div>
                </div>
            </div>

            <div style="background:rgba(255,255,255,0.04); border:1px solid var(--border,#1e2a38); border-left:4px solid #dc2626; padding:24px; border-radius:2px; margin-bottom:20px;">
                <p style="font-size:11px; letter-spacing:0.12em; color:var(--text-muted,#8899aa); margin-bottom:12px; font-family:'Share Tech Mono',monospace;">SOX §906 — CRIMINAL CERTIFICATION (18 U.S.C. §1350)</p>
                <p style="font-size:13px; line-height:1.9;">The periodic report containing the financial statements and audit data fully complies with the requirements of section 13(a) or 15(d) of the Securities Exchange Act of 1934, and the information contained in the periodic report fairly presents, in all material respects, the financial condition and results of operations of the issuer. <strong>Knowingly certifying a report that does not comply subjects the certifying officer to criminal penalties of up to $1,000,000 or 10 years imprisonment, or both (18 U.S.C. §1350(c)).</strong></p>
                <div style="margin-top:20px; padding-top:16px; border-top:1px solid var(--border,#1e2a38);">
                    <p style="font-size:12px; color:var(--text-muted,#8899aa);">COMPLIANCE OFFICER / GENERAL COUNSEL</p>
                    <div style="border-bottom:1px solid var(--border,#1e2a38); height:36px; margin:12px 0 8px;"></div>
                    <p style="font-size:11px; color:var(--text-muted,#8899aa);">Signature, Bar Number, Date</p>
                </div>
            </div>

            <div style="background:rgba(255,255,255,0.04); border:1px solid var(--border,#1e2a38); padding:18px; border-radius:2px;">
                <p style="font-size:11px; letter-spacing:0.12em; color:var(--text-muted,#8899aa); margin-bottom:10px; font-family:'Share Tech Mono',monospace;">AUDIT INTEGRITY SEAL</p>
                <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:16px; font-family:'Share Tech Mono',monospace; font-size:11px;">
                    <div><span style="color:var(--text-muted,#8899aa);">AUDIT ID</span><br><span style="color:var(--accent,#1e40af);">DEMO-2026-030-SOX</span></div>
                    <div><span style="color:var(--text-muted,#8899aa);">HASH (SHA-256)</span><br><span style="color:var(--accent,#1e40af);">a8f3c1...d4e92b</span></div>
                    <div><span style="color:var(--text-muted,#8899aa);">GENERATED</span><br><span style="color:var(--accent,#1e40af);">2026-03-01T09:00:00Z</span></div>
                    <div><span style="color:var(--text-muted,#8899aa);">PCAOB STANDARD</span><br><span style="color:var(--accent,#1e40af);">AS 2201</span></div>
                    <div><span style="color:var(--text-muted,#8899aa);">SEC RULE</span><br><span style="color:var(--accent,#1e40af);">17a-4 (7-yr retention)</span></div>
                    <div><span style="color:var(--text-muted,#8899aa);">COSO FRAMEWORK</span><br><span style="color:var(--accent,#1e40af);">2013 Internal Control</span></div>
                </div>
            </div>
            </div>
        </div>
""",

"law_enforcement_report.html": """
        <div class="section">
            <h2 class="section-title"><span class="section-number">7.</span>Chain of Custody &amp; Examiner Certification</h2>
            <div class="section-body">
            <div style="background:rgba(255,255,255,0.04); border:1px solid var(--border,#1e2a38); border-left:4px solid var(--accent,#1e3a5f); padding:24px; border-radius:2px; margin-bottom:20px;">
                <p style="font-size:11px; letter-spacing:0.12em; color:var(--text-muted,#8899aa); margin-bottom:12px; font-family:'Share Tech Mono',monospace;">EXPERT WITNESS DECLARATION — FRE 702 / DAUBERT STANDARD</p>
                <p style="font-size:13px; line-height:1.9;">I am a qualified expert in digital forensics with demonstrable experience in Windows forensic artifact analysis. I hold the following professional certifications: EnCE (EnCase Certified Examiner, Opentext), GCFE (GIAC Certified Forensic Examiner, SANS), CFCE (Certified Forensic Computer Examiner, IACIS). My opinions in this report are based upon my review of the evidence, my training and experience, and the application of generally accepted forensic principles validated by NIST CFTT (Computer Forensics Tool Testing). The methodology employed is the same used by practitioners in this field and has been tested, peer-reviewed, and accepted in federal and state courts under the Daubert standard (509 U.S. 579 (1993)).</p>
            </div>

            <div style="background:rgba(255,255,255,0.04); border:1px solid var(--border,#1e2a38); border-left:4px solid #10b981; padding:24px; border-radius:2px; margin-bottom:20px;">
                <p style="font-size:11px; letter-spacing:0.12em; color:var(--text-muted,#8899aa); margin-bottom:16px; font-family:'Share Tech Mono',monospace;">CHAIN OF CUSTODY LOG — FRE 901(b)(9) / FRE 902(14)</p>
                <table style="width:100%; border-collapse:collapse; font-size:12px; font-family:'Share Tech Mono',monospace;">
                    <thead>
                        <tr style="background:rgba(255,255,255,0.06);">
                            <th style="padding:8px 12px; text-align:left; border-bottom:1px solid var(--border,#1e2a38);">STEP</th>
                            <th style="padding:8px 12px; text-align:left; border-bottom:1px solid var(--border,#1e2a38);">DATE/TIME (UTC)</th>
                            <th style="padding:8px 12px; text-align:left; border-bottom:1px solid var(--border,#1e2a38);">CUSTODIAN</th>
                            <th style="padding:8px 12px; text-align:left; border-bottom:1px solid var(--border,#1e2a38);">ACTION</th>
                            <th style="padding:8px 12px; text-align:left; border-bottom:1px solid var(--border,#1e2a38);">HASH VERIFIED</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style="border-bottom:1px solid var(--border,#1e2a38);">
                            <td style="padding:8px 12px;">1</td>
                            <td style="padding:8px 12px;">2026-02-20 14:32:00Z</td>
                            <td style="padding:8px 12px;">Det. Badge #4471</td>
                            <td style="padding:8px 12px;">Evidence seizure — write-blocker applied</td>
                            <td style="padding:8px 12px; color:#10b981;">✓ SHA-256 recorded</td>
                        </tr>
                        <tr style="border-bottom:1px solid var(--border,#1e2a38);">
                            <td style="padding:8px 12px;">2</td>
                            <td style="padding:8px 12px;">2026-02-20 16:00:00Z</td>
                            <td style="padding:8px 12px;">Evidence Custodian</td>
                            <td style="padding:8px 12px;">Secured in Evidence Locker #12-B</td>
                            <td style="padding:8px 12px; color:#10b981;">✓ Verified on receipt</td>
                        </tr>
                        <tr style="border-bottom:1px solid var(--border,#1e2a38);">
                            <td style="padding:8px 12px;">3</td>
                            <td style="padding:8px 12px;">2026-02-21 09:15:00Z</td>
                            <td style="padding:8px 12px;">Forensic Examiner</td>
                            <td style="padding:8px 12px;">Forensic imaging — Vatican Vault acquisition</td>
                            <td style="padding:8px 12px; color:#10b981;">✓ Source = Image hash</td>
                        </tr>
                        <tr style="border-bottom:1px solid var(--border,#1e2a38);">
                            <td style="padding:8px 12px;">4</td>
                            <td style="padding:8px 12px;">2026-02-21 11:30:00Z</td>
                            <td style="padding:8px 12px;">Evidence Custodian</td>
                            <td style="padding:8px 12px;">Return to Evidence Locker — post-imaging</td>
                            <td style="padding:8px 12px; color:#10b981;">✓ Re-verified</td>
                        </tr>
                        <tr>
                            <td style="padding:8px 12px;">5</td>
                            <td style="padding:8px 12px;">2026-03-01 08:00:00Z</td>
                            <td style="padding:8px 12px;">Forensic Examiner</td>
                            <td style="padding:8px 12px;">Report finalized — submitted to Prosecutor</td>
                            <td style="padding:8px 12px; color:#10b981;">✓ Final hash confirmed</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div style="background:rgba(255,255,255,0.04); border:1px solid var(--border,#1e2a38); padding:20px; border-radius:2px;">
                <p style="font-size:11px; letter-spacing:0.12em; color:var(--text-muted,#8899aa); margin-bottom:14px; font-family:'Share Tech Mono',monospace;">FORENSIC EXAMINER CERTIFICATION</p>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:24px;">
                    <div>
                        <p style="font-size:12px; margin-bottom:6px; color:var(--text-muted,#8899aa);">PRIMARY EXAMINER</p>
                        <div style="border-bottom:1px solid var(--border,#1e2a38); height:34px; margin-bottom:6px;"></div>
                        <p style="font-size:11px; color:var(--text-muted,#8899aa);">Signature, Badge/ID Number</p>
                        <div style="border-bottom:1px solid var(--border,#1e2a38); height:34px; margin:14px 0 6px;"></div>
                        <p style="font-size:11px; color:var(--text-muted,#8899aa);">Certifications (EnCE / GCFE / CFCE)</p>
                    </div>
                    <div>
                        <p style="font-size:12px; margin-bottom:6px; color:var(--text-muted,#8899aa);">SUPERVISING OFFICER / PROSECUTOR</p>
                        <div style="border-bottom:1px solid var(--border,#1e2a38); height:34px; margin-bottom:6px;"></div>
                        <p style="font-size:11px; color:var(--text-muted,#8899aa);">Signature &amp; Title</p>
                        <div style="border-bottom:1px solid var(--border,#1e2a38); height:34px; margin:14px 0 6px;"></div>
                        <p style="font-size:11px; color:var(--text-muted,#8899aa);">Date Received (YYYY-MM-DD)</p>
                    </div>
                </div>
                <div style="margin-top:20px; padding-top:14px; border-top:1px solid var(--border,#1e2a38); font-family:'Share Tech Mono',monospace; font-size:11px; display:grid; grid-template-columns:repeat(3,1fr); gap:12px;">
                    <div><span style="color:var(--text-muted,#8899aa);">CASE NUMBER</span><br><span style="color:var(--accent,#1e3a5f);">DEMO-2026-LE-001</span></div>
                    <div><span style="color:var(--text-muted,#8899aa);">NIST CFTT TOOL</span><br><span style="color:var(--accent,#1e3a5f);">Vatican Vault v2.0</span></div>
                    <div><span style="color:var(--text-muted,#8899aa);">JURISDICTION</span><br><span style="color:var(--accent,#1e3a5f);">Federal District Court</span></div>
                </div>
            </div>
            </div>
        </div>
""",

"hr_employment_report.html": """
        <div class="section">
            <h2 class="section-title"><span class="section-number">7.</span>Investigator Certification &amp; Legal Review</h2>
            <div class="section-body">
            <div style="background:rgba(255,255,255,0.04); border:1px solid var(--border,#1e2a38); border-left:4px solid var(--accent,#7c3aed); padding:24px; border-radius:2px; margin-bottom:20px;">
                <p style="font-size:11px; letter-spacing:0.12em; color:var(--text-muted,#8899aa); margin-bottom:12px; font-family:'Share Tech Mono',monospace;">CONFIDENTIALITY NOTICE — ATTORNEY WORK PRODUCT / PRIVILEGED</p>
                <p style="font-size:13px; line-height:1.9;">This investigation report is <strong>CONFIDENTIAL</strong> and prepared in anticipation of litigation under the attorney work product doctrine and/or attorney-client privilege. Distribution is restricted to those with a legitimate need to know. I certify that this workplace investigation was conducted impartially, in accordance with company policy, applicable employment law (Title VII, 42 U.S.C. §2000e; ADA, 42 U.S.C. §12101; ADEA, 29 U.S.C. §621), EEOC Enforcement Guidance on Harassment Investigations (1999), and EEOC Uniform Guidelines on Employee Selection Procedures (29 CFR Part 1607). All interviews were conducted in good faith. No adverse employment action should be taken solely on the basis of this report without review by Human Resources and Legal Counsel.</p>
            </div>

            <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-bottom:20px;">
                <div style="background:rgba(255,255,255,0.04); border:1px solid var(--border,#1e2a38); padding:20px; border-radius:2px;">
                    <p style="font-size:11px; letter-spacing:0.1em; color:var(--text-muted,#8899aa); margin-bottom:14px; font-family:'Share Tech Mono',monospace;">HR DIRECTOR CERTIFICATION</p>
                    <div style="border-bottom:1px solid var(--border,#1e2a38); height:34px; margin-bottom:8px;"></div>
                    <p style="font-size:11px; color:var(--text-muted,#8899aa);">Signature</p>
                    <div style="border-bottom:1px solid var(--border,#1e2a38); height:34px; margin:16px 0 8px;"></div>
                    <p style="font-size:11px; color:var(--text-muted,#8899aa);">Title / SHRM-SCP / SPHR</p>
                    <div style="border-bottom:1px solid var(--border,#1e2a38); height:34px; margin:16px 0 8px;"></div>
                    <p style="font-size:11px; color:var(--text-muted,#8899aa);">Date (YYYY-MM-DD)</p>
                </div>
                <div style="background:rgba(255,255,255,0.04); border:1px solid var(--border,#1e2a38); padding:20px; border-radius:2px;">
                    <p style="font-size:11px; letter-spacing:0.1em; color:var(--text-muted,#8899aa); margin-bottom:14px; font-family:'Share Tech Mono',monospace;">LEGAL COUNSEL REVIEW</p>
                    <div style="border-bottom:1px solid var(--border,#1e2a38); height:34px; margin-bottom:8px;"></div>
                    <p style="font-size:11px; color:var(--text-muted,#8899aa);">Signature</p>
                    <div style="border-bottom:1px solid var(--border,#1e2a38); height:34px; margin:16px 0 8px;"></div>
                    <p style="font-size:11px; color:var(--text-muted,#8899aa);">Attorney Name / Bar Number</p>
                    <div style="border-bottom:1px solid var(--border,#1e2a38); height:34px; margin:16px 0 8px;"></div>
                    <p style="font-size:11px; color:var(--text-muted,#8899aa);">Date Reviewed (YYYY-MM-DD)</p>
                </div>
            </div>

            <div style="background:rgba(255,255,255,0.04); border:1px solid var(--border,#1e2a38); padding:18px; border-radius:2px;">
                <p style="font-size:11px; letter-spacing:0.12em; color:var(--text-muted,#8899aa); margin-bottom:10px; font-family:'Share Tech Mono',monospace;">INVESTIGATION METADATA</p>
                <div style="font-family:'Share Tech Mono',monospace; font-size:11px; display:grid; grid-template-columns:repeat(3,1fr); gap:14px;">
                    <div><span style="color:var(--text-muted,#8899aa);">CASE ID</span><br><span style="color:var(--accent,#7c3aed);">HR-INV-2026-007</span></div>
                    <div><span style="color:var(--text-muted,#8899aa);">EEOC REF</span><br><span style="color:var(--accent,#7c3aed);">29 CFR §1607.4(D)</span></div>
                    <div><span style="color:var(--text-muted,#8899aa);">RETENTION</span><br><span style="color:var(--accent,#7c3aed);">7 years (litigation hold)</span></div>
                    <div><span style="color:var(--text-muted,#8899aa);">DIGITAL EVIDENCE</span><br><span style="color:var(--accent,#7c3aed);">Hash-verified</span></div>
                    <div><span style="color:var(--text-muted,#8899aa);">WEINGARTEN NOTICE</span><br><span style="color:var(--accent,#7c3aed);">Provided (420 U.S. 251)</span></div>
                    <div><span style="color:var(--text-muted,#8899aa);">LEGAL HOLD</span><br><span style="color:var(--accent,#7c3aed);">Active since 2026-02-01</span></div>
                </div>
            </div>
            </div>
        </div>
""",

"irm_report.html": """
        <div class="section">
            <h2 class="section-title"><span class="section-number">7.</span>Incident Commander Certification &amp; CIRCIA Compliance</h2>
            <div class="section-body">
            <div style="background:rgba(255,255,255,0.04); border:1px solid var(--border,#1e2a38); border-left:4px solid var(--accent,#ea580c); padding:24px; border-radius:2px; margin-bottom:20px;">
                <p style="font-size:11px; letter-spacing:0.12em; color:var(--text-muted,#8899aa); margin-bottom:12px; font-family:'Share Tech Mono',monospace;">POST-INCIDENT REVIEW CERTIFICATION — NIST SP 800-61 Rev. 3</p>
                <p style="font-size:13px; line-height:1.9;">This Post-Incident Review (PIR) was completed in accordance with NIST SP 800-61 Rev. 3 (April 2025) and the organization's Incident Response Policy. Incident ID: <strong>INC-2026-0301-001</strong>. Severity: <strong>HIGH (P2)</strong>. All root cause determinations represent the collective assessment of the Incident Response team. This report has been reviewed by the CISO and all recommendations have been accepted for implementation per the attached remediation schedule. The Vatican Vault analysis platform provided forensic-grade artifact extraction enabling complete timeline reconstruction.</p>
            </div>

            <div style="background:rgba(255,255,255,0.04); border:1px solid var(--border,#1e2a38); border-left:4px solid #f59e0b; padding:22px; border-radius:2px; margin-bottom:20px;">
                <p style="font-size:11px; letter-spacing:0.12em; color:var(--text-muted,#8899aa); margin-bottom:12px; font-family:'Share Tech Mono',monospace;">CIRCIA REPORTING COMPLIANCE (P.L. 117-263, §§2240–2244)</p>
                <p style="font-size:13px; line-height:1.9;">In accordance with the Cyber Incident Reporting for Critical Infrastructure Act of 2022 (CIRCIA), this covered cyber incident has been reported to CISA within the required 72-hour window. Ransom payment was <strong>NOT</strong> made. CISA Case Number: <strong>CISA-2026-DEMO-001</strong>. Regulatory notifications have also been submitted to applicable sector-specific agencies per DHS CIRCIA Final Rule requirements.</p>
                <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:14px; margin-top:16px; padding-top:14px; border-top:1px solid var(--border,#1e2a38); font-family:'Share Tech Mono',monospace; font-size:11px;">
                    <div><span style="color:var(--text-muted,#8899aa);">DETECTION TIME</span><br><span style="color:#f59e0b;">2026-02-28 22:14Z</span></div>
                    <div><span style="color:var(--text-muted,#8899aa);">REPORT SUBMITTED</span><br><span style="color:#10b981;">2026-03-01 14:30Z (within 72h)</span></div>
                    <div><span style="color:var(--text-muted,#8899aa);">RANSOM PAID</span><br><span style="color:#10b981;">NO — Not applicable</span></div>
                </div>
            </div>

            <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-bottom:20px;">
                <div style="background:rgba(255,255,255,0.04); border:1px solid var(--border,#1e2a38); padding:20px; border-radius:2px;">
                    <p style="font-size:11px; letter-spacing:0.1em; color:var(--text-muted,#8899aa); margin-bottom:14px; font-family:'Share Tech Mono',monospace;">INCIDENT COMMANDER</p>
                    <div style="border-bottom:1px solid var(--border,#1e2a38); height:34px; margin-bottom:8px;"></div>
                    <p style="font-size:11px; color:var(--text-muted,#8899aa);">Signature / GCIH / ECIR</p>
                    <div style="border-bottom:1px solid var(--border,#1e2a38); height:34px; margin:16px 0 8px;"></div>
                    <p style="font-size:11px; color:var(--text-muted,#8899aa);">Date (YYYY-MM-DD)</p>
                </div>
                <div style="background:rgba(255,255,255,0.04); border:1px solid var(--border,#1e2a38); padding:20px; border-radius:2px;">
                    <p style="font-size:11px; letter-spacing:0.1em; color:var(--text-muted,#8899aa); margin-bottom:14px; font-family:'Share Tech Mono',monospace;">CISO APPROVAL</p>
                    <div style="border-bottom:1px solid var(--border,#1e2a38); height:34px; margin-bottom:8px;"></div>
                    <p style="font-size:11px; color:var(--text-muted,#8899aa);">Signature / CISSP / CISM</p>
                    <div style="border-bottom:1px solid var(--border,#1e2a38); height:34px; margin:16px 0 8px;"></div>
                    <p style="font-size:11px; color:var(--text-muted,#8899aa);">Date Approved (YYYY-MM-DD)</p>
                </div>
            </div>
            </div>
        </div>
""",

"mssp_report.html": """
        <div class="section">
            <h2 class="section-title"><span class="section-number">7.</span>Service Provider Attestation &amp; SOC 2 Compliance</h2>
            <div class="section-body">
            <div style="background:rgba(255,255,255,0.04); border:1px solid var(--border,#1e2a38); border-left:4px solid var(--accent,#7e22ce); padding:24px; border-radius:2px; margin-bottom:20px;">
                <p style="font-size:11px; letter-spacing:0.12em; color:var(--text-muted,#8899aa); margin-bottom:12px; font-family:'Share Tech Mono',monospace;">MSSP SERVICE ATTESTATION — SSAE 18 / SOC 2 TYPE II</p>
                <p style="font-size:13px; line-height:1.9;">This report has been prepared in accordance with SSAE No. 18, Attestation Standards: Clarification and Recodification (AT-C Section 320) and the AICPA Trust Services Criteria for Security, Availability, and Confidentiality. The Managed Security Service Provider hereby attests that all monitoring, analysis, and reporting activities described herein were conducted by certified personnel in accordance with the service level agreement (SLA) and the contractual security standards. Vatican Vault's forensic capabilities have been assessed and verified as meeting the technical requirements for SOC 2 Type II compliant security monitoring.</p>
            </div>

            <div style="background:rgba(255,255,255,0.04); border:1px solid var(--border,#1e2a38); padding:20px; border-radius:2px; margin-bottom:20px;">
                <p style="font-size:11px; letter-spacing:0.12em; color:var(--text-muted,#8899aa); margin-bottom:14px; font-family:'Share Tech Mono',monospace;">TRUST SERVICES CRITERIA COVERAGE</p>
                <table style="width:100%; border-collapse:collapse; font-size:12px;">
                    <thead>
                        <tr style="background:rgba(255,255,255,0.06);">
                            <th style="padding:8px 12px; text-align:left; border-bottom:1px solid var(--border,#1e2a38);">CRITERIA</th>
                            <th style="padding:8px 12px; text-align:left; border-bottom:1px solid var(--border,#1e2a38);">DESCRIPTION</th>
                            <th style="padding:8px 12px; text-align:left; border-bottom:1px solid var(--border,#1e2a38);">STATUS</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style="border-bottom:1px solid var(--border,#1e2a38);">
                            <td style="padding:8px 12px; font-family:'Share Tech Mono',monospace; font-size:11px;">CC6.1</td>
                            <td style="padding:8px 12px;">Logical access security — authentication controls</td>
                            <td style="padding:8px 12px; color:#10b981; font-family:'Share Tech Mono',monospace; font-size:11px;">✓ EFFECTIVE</td>
                        </tr>
                        <tr style="border-bottom:1px solid var(--border,#1e2a38);">
                            <td style="padding:8px 12px; font-family:'Share Tech Mono',monospace; font-size:11px;">CC7.2</td>
                            <td style="padding:8px 12px;">Security event monitoring and response</td>
                            <td style="padding:8px 12px; color:#10b981; font-family:'Share Tech Mono',monospace; font-size:11px;">✓ EFFECTIVE</td>
                        </tr>
                        <tr style="border-bottom:1px solid var(--border,#1e2a38);">
                            <td style="padding:8px 12px; font-family:'Share Tech Mono',monospace; font-size:11px;">CC7.4</td>
                            <td style="padding:8px 12px;">Incident identification, classification, response</td>
                            <td style="padding:8px 12px; color:#10b981; font-family:'Share Tech Mono',monospace; font-size:11px;">✓ EFFECTIVE</td>
                        </tr>
                        <tr style="border-bottom:1px solid var(--border,#1e2a38);">
                            <td style="padding:8px 12px; font-family:'Share Tech Mono',monospace; font-size:11px;">A1.1</td>
                            <td style="padding:8px 12px;">Availability — current processing capacity</td>
                            <td style="padding:8px 12px; color:#10b981; font-family:'Share Tech Mono',monospace; font-size:11px;">✓ EFFECTIVE</td>
                        </tr>
                        <tr>
                            <td style="padding:8px 12px; font-family:'Share Tech Mono',monospace; font-size:11px;">C1.1</td>
                            <td style="padding:8px 12px;">Confidentiality — data classification and protection</td>
                            <td style="padding:8px 12px; color:#10b981; font-family:'Share Tech Mono',monospace; font-size:11px;">✓ EFFECTIVE</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px;">
                <div style="background:rgba(255,255,255,0.04); border:1px solid var(--border,#1e2a38); padding:20px; border-radius:2px;">
                    <p style="font-size:11px; letter-spacing:0.1em; color:var(--text-muted,#8899aa); margin-bottom:14px; font-family:'Share Tech Mono',monospace;">SERVICE DELIVERY MANAGER</p>
                    <div style="border-bottom:1px solid var(--border,#1e2a38); height:34px; margin-bottom:8px;"></div>
                    <p style="font-size:11px; color:var(--text-muted,#8899aa);">Signature / CISA / CISSP</p>
                    <div style="border-bottom:1px solid var(--border,#1e2a38); height:34px; margin:16px 0 8px;"></div>
                    <p style="font-size:11px; color:var(--text-muted,#8899aa);">Date (YYYY-MM-DD)</p>
                </div>
                <div style="background:rgba(255,255,255,0.04); border:1px solid var(--border,#1e2a38); padding:20px; border-radius:2px;">
                    <p style="font-size:11px; letter-spacing:0.1em; color:var(--text-muted,#8899aa); margin-bottom:14px; font-family:'Share Tech Mono',monospace;">CLIENT ACKNOWLEDGMENT</p>
                    <div style="border-bottom:1px solid var(--border,#1e2a38); height:34px; margin-bottom:8px;"></div>
                    <p style="font-size:11px; color:var(--text-muted,#8899aa);">Authorized Client Representative</p>
                    <div style="border-bottom:1px solid var(--border,#1e2a38); height:34px; margin:16px 0 8px;"></div>
                    <p style="font-size:11px; color:var(--text-muted,#8899aa);">Date Acknowledged (YYYY-MM-DD)</p>
                </div>
            </div>
            </div>
        </div>
""",

"generic_compliance_report.html": """
        <div class="section">
            <h2 class="section-title"><span class="section-number">7.</span>Compliance Officer Attestation &amp; Certification</h2>
            <div class="section-body">
            <div style="background:rgba(255,255,255,0.04); border:1px solid var(--border,#1e2a38); border-left:4px solid var(--accent,#0f766e); padding:24px; border-radius:2px; margin-bottom:20px;">
                <p style="font-size:11px; letter-spacing:0.12em; color:var(--text-muted,#8899aa); margin-bottom:12px; font-family:'Share Tech Mono',monospace;">COMPLIANCE OFFICER CERTIFICATION</p>
                <p style="font-size:13px; line-height:1.9;">I, the undersigned Compliance Officer, hereby certify that this audit was conducted in accordance with applicable regulatory requirements, internal compliance policies, and industry standards. The Vatican Vault analysis was performed using forensically sound methodologies, and the findings presented herein accurately reflect the digital evidence reviewed. All data handling procedures comply with applicable privacy laws and data protection regulations. This report is suitable for regulatory submission and board-level review.</p>
            </div>

            <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-bottom:20px;">
                <div style="background:rgba(255,255,255,0.04); border:1px solid var(--border,#1e2a38); padding:20px; border-radius:2px;">
                    <p style="font-size:11px; letter-spacing:0.1em; color:var(--text-muted,#8899aa); margin-bottom:14px; font-family:'Share Tech Mono',monospace;">CHIEF COMPLIANCE OFFICER</p>
                    <div style="border-bottom:1px solid var(--border,#1e2a38); height:34px; margin-bottom:8px;"></div>
                    <p style="font-size:11px; color:var(--text-muted,#8899aa);">Signature / CCEP / CHC</p>
                    <div style="border-bottom:1px solid var(--border,#1e2a38); height:34px; margin:16px 0 8px;"></div>
                    <p style="font-size:11px; color:var(--text-muted,#8899aa);">Date Certified (YYYY-MM-DD)</p>
                </div>
                <div style="background:rgba(255,255,255,0.04); border:1px solid var(--border,#1e2a38); padding:20px; border-radius:2px;">
                    <p style="font-size:11px; letter-spacing:0.1em; color:var(--text-muted,#8899aa); margin-bottom:14px; font-family:'Share Tech Mono',monospace;">INDEPENDENT AUDITOR REVIEW</p>
                    <div style="border-bottom:1px solid var(--border,#1e2a38); height:34px; margin-bottom:8px;"></div>
                    <p style="font-size:11px; color:var(--text-muted,#8899aa);">Auditor Firm / License Number</p>
                    <div style="border-bottom:1px solid var(--border,#1e2a38); height:34px; margin:16px 0 8px;"></div>
                    <p style="font-size:11px; color:var(--text-muted,#8899aa);">Date of Independent Review</p>
                </div>
            </div>

            <div style="background:rgba(255,255,255,0.04); border:1px solid var(--border,#1e2a38); padding:18px; border-radius:2px;">
                <p style="font-size:11px; letter-spacing:0.12em; color:var(--text-muted,#8899aa); margin-bottom:10px; font-family:'Share Tech Mono',monospace;">AUDIT TRAIL INTEGRITY</p>
                <div style="font-family:'Share Tech Mono',monospace; font-size:11px; display:grid; grid-template-columns:repeat(3,1fr); gap:14px;">
                    <div><span style="color:var(--text-muted,#8899aa);">REPORT ID</span><br><span style="color:var(--accent,#0f766e);">COMP-2026-030-001</span></div>
                    <div><span style="color:var(--text-muted,#8899aa);">HASH (SHA-256)</span><br><span style="color:var(--accent,#0f766e);">c7d2f9...a1b4e8</span></div>
                    <div><span style="color:var(--text-muted,#8899aa);">GENERATED</span><br><span style="color:var(--accent,#0f766e);">2026-03-01T09:00:00Z</span></div>
                    <div><span style="color:var(--text-muted,#8899aa);">FRAMEWORK</span><br><span style="color:var(--accent,#0f766e);">NIST CSF / ISO 27001</span></div>
                    <div><span style="color:var(--text-muted,#8899aa);">RETENTION</span><br><span style="color:var(--accent,#0f766e);">7 years (regulatory)</span></div>
                    <div><span style="color:var(--text-muted,#8899aa);">CLASSIFICATION</span><br><span style="color:var(--accent,#0f766e);">CONFIDENTIAL</span></div>
                </div>
            </div>
            </div>
        </div>
""",
}

# Healthcare upgrade
HEALTHCARE_ATTESTATION_UPGRADE = """        <div class="section">
            <h2 class="section-title"><span class="section-number">7.</span>HIPAA Attestation &amp; Privacy Officer Certification</h2>
            <div class="section-body">
            <div style="background:rgba(255,255,255,0.04); border:1px solid var(--border,#1e2a38); border-left:4px solid var(--accent,#059669); padding:24px; border-radius:2px; margin-bottom:20px;">
                <p style="font-size:11px; letter-spacing:0.12em; color:var(--text-muted,#8899aa); margin-bottom:12px; font-family:'Share Tech Mono',monospace;">HIPAA ATTESTATION — 45 CFR §164.308 / §164.312 / HITECH ACT §13401</p>
                <p style="font-size:13px; line-height:1.9;">I, the undersigned Privacy Officer/Security Officer, hereby certify that this audit was conducted in accordance with the HIPAA Privacy Rule (45 CFR Part 164, Subpart E), the HIPAA Security Rule (45 CFR §164.308 Administrative Safeguards, §164.310 Physical Safeguards, §164.312 Technical Safeguards), and the HITECH Act §13401 security provisions. The audit trail has been reviewed for completeness, accuracy, and integrity. PHI handling procedures comply with the Minimum Necessary standard (45 CFR §164.514(d)). This report is suitable for OCR (Office for Civil Rights) inquiry response and Board Privacy/Security Committee review.</p>
            </div>

            <div style="background:rgba(255,255,255,0.04); border:1px solid var(--border,#1e2a38); padding:20px; border-radius:2px; margin-bottom:20px;">
                <p style="font-size:11px; letter-spacing:0.12em; color:var(--text-muted,#8899aa); margin-bottom:14px; font-family:'Share Tech Mono',monospace;">REQUIRED SAFEGUARD ASSESSMENT</p>
                <table style="width:100%; border-collapse:collapse; font-size:12px;">
                    <thead>
                        <tr style="background:rgba(255,255,255,0.06);">
                            <th style="padding:8px 12px; text-align:left; border-bottom:1px solid var(--border,#1e2a38);">SAFEGUARD</th>
                            <th style="padding:8px 12px; text-align:left; border-bottom:1px solid var(--border,#1e2a38);">CFR CITATION</th>
                            <th style="padding:8px 12px; text-align:left; border-bottom:1px solid var(--border,#1e2a38);">IMPLEMENTATION</th>
                            <th style="padding:8px 12px; text-align:left; border-bottom:1px solid var(--border,#1e2a38);">STATUS</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style="border-bottom:1px solid var(--border,#1e2a38);">
                            <td style="padding:8px 12px;">Access Control</td>
                            <td style="padding:8px 12px; font-family:'Share Tech Mono',monospace; font-size:11px;">§164.312(a)(1)</td>
                            <td style="padding:8px 12px;">Unique user ID, automatic logoff, encryption</td>
                            <td style="padding:8px 12px; color:#10b981; font-family:'Share Tech Mono',monospace; font-size:11px;">✓ COMPLIANT</td>
                        </tr>
                        <tr style="border-bottom:1px solid var(--border,#1e2a38);">
                            <td style="padding:8px 12px;">Audit Controls</td>
                            <td style="padding:8px 12px; font-family:'Share Tech Mono',monospace; font-size:11px;">§164.312(b)</td>
                            <td style="padding:8px 12px;">Hardware/software activity logging</td>
                            <td style="padding:8px 12px; color:#10b981; font-family:'Share Tech Mono',monospace; font-size:11px;">✓ COMPLIANT</td>
                        </tr>
                        <tr style="border-bottom:1px solid var(--border,#1e2a38);">
                            <td style="padding:8px 12px;">Integrity Controls</td>
                            <td style="padding:8px 12px; font-family:'Share Tech Mono',monospace; font-size:11px;">§164.312(c)(1)</td>
                            <td style="padding:8px 12px;">Hash verification, tamper detection</td>
                            <td style="padding:8px 12px; color:#10b981; font-family:'Share Tech Mono',monospace; font-size:11px;">✓ COMPLIANT</td>
                        </tr>
                        <tr>
                            <td style="padding:8px 12px;">Transmission Security</td>
                            <td style="padding:8px 12px; font-family:'Share Tech Mono',monospace; font-size:11px;">§164.312(e)(1)</td>
                            <td style="padding:8px 12px;">Encryption in transit (TLS 1.3)</td>
                            <td style="padding:8px 12px; color:#10b981; font-family:'Share Tech Mono',monospace; font-size:11px;">✓ COMPLIANT</td>
                        </tr>
                    </tbody>
                </table>
            </div>

            <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px;">
                <div style="background:rgba(255,255,255,0.04); border:1px solid var(--border,#1e2a38); padding:20px; border-radius:2px;">
                    <p style="font-size:11px; letter-spacing:0.1em; color:var(--text-muted,#8899aa); margin-bottom:14px; font-family:'Share Tech Mono',monospace;">PRIVACY OFFICER</p>
                    <div style="border-bottom:1px solid var(--border,#1e2a38); height:34px; margin-bottom:8px;"></div>
                    <p style="font-size:11px; color:var(--text-muted,#8899aa);">Signature / CHPC / RHIA</p>
                    <div style="border-bottom:1px solid var(--border,#1e2a38); height:34px; margin:16px 0 8px;"></div>
                    <p style="font-size:11px; color:var(--text-muted,#8899aa);">Date (YYYY-MM-DD)</p>
                </div>
                <div style="background:rgba(255,255,255,0.04); border:1px solid var(--border,#1e2a38); padding:20px; border-radius:2px;">
                    <p style="font-size:11px; letter-spacing:0.1em; color:var(--text-muted,#8899aa); margin-bottom:14px; font-family:'Share Tech Mono',monospace;">SECURITY OFFICER</p>
                    <div style="border-bottom:1px solid var(--border,#1e2a38); height:34px; margin-bottom:8px;"></div>
                    <p style="font-size:11px; color:var(--text-muted,#8899aa);">Signature / CISM / CISSP-ISSMP</p>
                    <div style="border-bottom:1px solid var(--border,#1e2a38); height:34px; margin:16px 0 8px;"></div>
                    <p style="font-size:11px; color:var(--text-muted,#8899aa);">Date (YYYY-MM-DD)</p>
                </div>
            </div>
            </div>
        </div>"""

# ──────────────────────────────────────────────────────────────────────────────
# PROCESS REPORTS
# ──────────────────────────────────────────────────────────────────────────────

def insert_before_footer(content, insertion):
    """Insert content before the .footer div."""
    marker = '<div class="footer">'
    idx = content.rfind(marker)
    if idx == -1:
        # Try </body>
        idx = content.rfind('</body>')
        if idx == -1:
            return content
    return content[:idx] + insertion + '\n        ' + content[idx:]

def add_universal_js(content):
    """Add universal interactivity JS before </body>."""
    if 'vv-print-btn' in content:
        return content  # already added
    return content.replace('</body>', UNIVERSAL_JS + '\n</body>', 1)

def process_all_reports():
    print("Processing industry reports...")

    for fname in os.listdir(REPORTS_DIR):
        if not fname.endswith('.html') or fname == 'index.html':
            continue
        fpath = os.path.join(REPORTS_DIR, fname)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Add attestation section if applicable
        HAS_ATTEST_SECTION = 'section-title">.*Attestation' in content or \
                              bool(re.search(r'section-number.*7.*Attestation', content))
        if fname == 'healthcare_report.html':
            # Always upgrade healthcare attestation if not already upgraded
            if '45 CFR §164.308' not in content:
                old_pattern = r'<div class="section">\s*<h2 class="section-title"><span class="section-number">7\.</span>Attestation.*?</div>\s*</div>'
                replaced = re.sub(old_pattern, HEALTHCARE_ATTESTATION_UPGRADE, content, flags=re.DOTALL)
                if replaced != content:
                    content = replaced
                    print(f"  ✓ Upgraded attestation: {fname}")
                else:
                    # No match, append
                    content = insert_before_footer(content, HEALTHCARE_ATTESTATION_UPGRADE)
                    print(f"  ✓ Added upgraded attestation: {fname}")
        elif fname in ATTESTATIONS and not HAS_ATTEST_SECTION:
            content = insert_before_footer(content, ATTESTATIONS[fname])
            print(f"  ✓ Added attestation: {fname}")

        # Add universal JS
        content = add_universal_js(content)

        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)

    print("Done processing reports.")

if __name__ == '__main__':
    process_all_reports()
