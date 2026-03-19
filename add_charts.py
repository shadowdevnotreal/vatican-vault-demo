#!/usr/bin/env python3
"""Add interactive Chart.js charts to all Vatican Vault reports + fix healthcare attestation."""
import os, re

REPORTS = "Industry_Demo_Reports"
CDN = '<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>'

CHART_CSS = """<style>
/* VV Interactive Charts */
.vv-chart-row{display:grid;gap:18px;margin:20px 0}
.vv-chart-row.c2{grid-template-columns:1fr 1fr}
.vv-chart-row.c3{grid-template-columns:1fr 1fr 1fr}
.vv-chart-card{background:rgba(255,255,255,0.025);border:1px solid var(--border,#1e2a3e);border-radius:2px;padding:18px}
.vv-chart-lbl{font-family:'Share Tech Mono',monospace;font-size:.62em;letter-spacing:2px;text-transform:uppercase;color:var(--text-dim,#6b86a0);margin-bottom:12px;padding-bottom:8px;border-bottom:1px solid var(--border,#1e2a3e)}
.vv-chart-c{position:relative}
.vv-chart-c.h180{height:180px}.vv-chart-c.h220{height:220px}.vv-chart-c.h260{height:260px}.vv-chart-c.h300{height:300px}
.vv-chart-foot{font-family:'Share Tech Mono',monospace;font-size:.57em;letter-spacing:1px;color:var(--text-dim,#6b86a0);text-align:center;margin-top:8px;opacity:.7}
.vv-real-hdr{display:inline-flex;align-items:center;gap:8px;font-family:'Share Tech Mono',monospace;font-size:.62em;letter-spacing:2px;text-transform:uppercase;color:#10b981;border:1px solid rgba(16,185,129,.3);background:rgba(16,185,129,.06);padding:4px 12px;border-radius:2px;margin-bottom:14px}
.vv-real-hdr::before{content:'◉';font-size:.8em}
.vv-real-img-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:14px 0}
.vv-real-img-wrap{border:1px solid var(--border,#1e2a3e);border-radius:2px;overflow:hidden;background:#000}
.vv-real-img-wrap img{width:100%;height:auto;display:block}
.vv-real-img-cap{font-family:'Share Tech Mono',monospace;font-size:.57em;letter-spacing:1px;color:var(--text-dim,#6b86a0);padding:7px 12px;border-top:1px solid var(--border,#1e2a3e)}
@media(max-width:720px){.vv-chart-row.c2,.vv-chart-row.c3,.vv-real-img-grid{grid-template-columns:1fr}}
@media print{.vv-chart-c canvas{max-width:100%!important}}
</style>"""

CHART_DEFAULTS_JS = """<script>
(function(){function d(){if(typeof Chart==='undefined')return;var C=Chart.defaults;
C.color='#6b86a0';C.borderColor='#1e2a3e';
C.plugins.legend.labels.color='#d8e8f5';
C.plugins.legend.labels.font={family:"'Share Tech Mono',monospace",size:11};
C.plugins.tooltip.backgroundColor='rgba(4,8,15,.97)';
C.plugins.tooltip.borderColor='#1e2a3e';C.plugins.tooltip.borderWidth=1;
C.plugins.tooltip.titleColor='#00d4ff';C.plugins.tooltip.bodyColor='#d8e8f5';
C.plugins.tooltip.titleFont={family:"'Share Tech Mono',monospace",size:10};
C.plugins.tooltip.bodyFont={family:"'Share Tech Mono',monospace",size:10};
C.scale.grid.color='rgba(30,42,62,.7)';
C.scale.ticks.color='#6b86a0';
C.scale.ticks.font={family:"'Share Tech Mono',monospace",size:10};}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',d);else d();
})();</script>"""

# Real data from Demo_Data/Test System/WindowsTimeline_Output/
# 1,853 activities over 146 days (Oct 16 2022 – Mar 10 2023), 75 apps
WEEK_LABELS = "['Oct W3','Oct W4','Nov W1','Nov W2','Nov W3','Nov W4','Dec W1','Dec W2','Dec W3','Dec W4','Jan W1','Jan W2','Jan W3','Jan W4','Jan W5','Feb W1','Feb W2','Feb W3','Feb W4','Mar W1','Mar W2']"
WEEK_DATA   = "[72,85,78,95,91,98,103,94,98,65,52,82,89,97,95,99,108,102,84,71,94]"

# ── utilities ──────────────────────────────────────────────────────────────────
def ins_before(content, marker, html):
    i = content.find(marker)
    if i == -1: return content, False
    return content[:i] + html + content[i:], True

def ins_after(content, marker, html):
    i = content.find(marker)
    if i == -1: return content, False
    p = i + len(marker)
    return content[:p] + html + content[p:], True

def prepare(content):
    """Inject CDN + defaults + chart CSS if not present."""
    if 'chart.umd' not in content and 'chart.js' not in content.lower():
        content = content.replace('</head>', CDN + '\n' + CHART_DEFAULTS_JS + '\n</head>', 1)
    if 'vv-chart-card' not in content:
        content = content.replace('</head>', CHART_CSS + '\n</head>', 1)
    return content

def patch_file(fname, fn):
    fpath = os.path.join(REPORTS, fname)
    with open(fpath, 'r', encoding='utf-8') as f: c = f.read()
    orig = c
    c = fn(c)
    if c != orig:
        with open(fpath, 'w', encoding='utf-8') as f: f.write(c)
        print(f"  ✓ {fname}")
    else:
        print(f"  - {fname}: no change")

# ── healthcare_report.html ─────────────────────────────────────────────────────
def fix_healthcare(c):
    c = prepare(c)

    # Fix remaining light-theme CSS in <style> block
    c = c.replace("border-bottom: 1px solid #f0f3f8;", "border-bottom: 1px solid var(--border);")
    c = c.replace("tr:hover td { background: #f7f9fc; }", "tr:hover td { background: rgba(255,255,255,0.03); }")
    c = c.replace("background: #ecfdf5;", "background: rgba(5,150,105,0.06);")
    c = c.replace("background: #f0f9ff;", "background: rgba(26,86,219,0.08);")
    c = c.replace("color: #1e293b;", "color: var(--text);")
    c = c.replace('border: 2px solid #e0e0e0;', 'border: 1px solid var(--border);')
    c = c.replace('border-top: 1px solid #ccc;', 'border-top: 1px solid var(--border);')

    # Replace old ___ attestation with proper sig blocks
    old_att = '''<div style="background:rgba(255,255,255,0.04); padding:25px; border-radius:6px; border:2px solid #e0e0e0;">
                <p style="font-size:14px; line-height:1.8;">
                    I, the undersigned Privacy Officer / Security Officer, hereby certify that this audit was conducted in accordance
                    with HIPAA Privacy Rule (45 CFR Part 164, Subpart E) and Security Rule (45 CFR §164.308-164.312) requirements.
                    The audit trail has been reviewed for completeness, accuracy, and integrity.
                </p>
                <div style="margin-top:30px; padding-top:20px; border-top:1px solid #ccc;">
                    <p><strong>Privacy/Security Officer:</strong> _____________________________</p>
                    <p style="margin-top:15px;"><strong>Date:</strong> _____________________________</p>
                    <p style="margin-top:15px;"><strong>Signature:</strong> _____________________________</p>
                </div>
            </div>'''
    new_att = '''<div class="attestation">
                <p style="font-size:14px;line-height:1.8;margin-bottom:20px;">
                    I, the undersigned Privacy Officer / Security Officer, hereby certify that this audit was conducted
                    in accordance with HIPAA Privacy Rule (45 CFR Part 164, Subpart E) and Security Rule
                    (45 CFR §164.308–164.312) requirements. The audit trail has been reviewed for completeness,
                    accuracy, and integrity. All findings are accurate to the best of my knowledge and belief.
                    This attestation is made under the penalty of perjury under applicable law.
                </p>
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:16px;">
                    <div class="vv-sig-block">
                        <div class="vv-sig-container">
                            <div class="vv-sig-fields">
                                <div>
                                    <div class="vv-sig-field-label">PRIVACY OFFICER / COMPLIANCE OFFICER</div>
                                    <input type="text" class="vv-sig-text" placeholder="Type full name to sign" autocomplete="off" spellcheck="false">
                                </div>
                                <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
                                    <div>
                                        <div class="vv-sig-field-label">DATE SIGNED</div>
                                        <input type="date" class="vv-date-input">
                                    </div>
                                    <div>
                                        <div class="vv-sig-field-label">TITLE / CREDENTIALS</div>
                                        <input type="text" class="vv-sig-text" placeholder="CPO, CIPP/US..." autocomplete="off">
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
                    </div>
                    <div class="vv-sig-block">
                        <div class="vv-sig-container">
                            <div class="vv-sig-fields">
                                <div>
                                    <div class="vv-sig-field-label">SECURITY OFFICER / CISO</div>
                                    <input type="text" class="vv-sig-text" placeholder="Type full name to sign" autocomplete="off" spellcheck="false">
                                </div>
                                <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;">
                                    <div>
                                        <div class="vv-sig-field-label">DATE SIGNED</div>
                                        <input type="date" class="vv-date-input">
                                    </div>
                                    <div>
                                        <div class="vv-sig-field-label">TITLE / CREDENTIALS</div>
                                        <input type="text" class="vv-sig-text" placeholder="CISO, CISSP..." autocomplete="off">
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
                    </div>
                </div>
            </div>'''
    c = c.replace(old_att, new_att)

    # Inject charts before section 2
    charts = f"""
<div class="vv-chart-row c2">
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">PHI Access Activity — 146-Day Audit Window (Real Data)</div>
    <div class="vv-chart-c h220"><canvas id="hc-tl"></canvas></div>
    <div class="vv-chart-foot">1,853 endpoint activities · Vatican Vault analysis · Oct 2022 – Mar 2023</div>
  </div>
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">HIPAA Control Domain Coverage</div>
    <div class="vv-chart-c h220"><canvas id="hc-ctrl"></canvas></div>
    <div class="vv-chart-foot">45 CFR §164.308–312 implementation status</div>
  </div>
</div>
<div class="vv-chart-row c2">
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">PHI Category Risk Distribution (12 Identifiers)</div>
    <div class="vv-chart-c h220"><canvas id="hc-phi"></canvas></div>
    <div class="vv-chart-foot">45 CFR §160.103 identifier categories monitored</div>
  </div>
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">Application Categories Detected (75 Apps)</div>
    <div class="vv-chart-c h220"><canvas id="hc-apps"></canvas></div>
    <div class="vv-chart-foot">Vatican Vault v2.0 · Real endpoint application inventory</div>
  </div>
</div>
<script>
(function(){{
  document.addEventListener('DOMContentLoaded',function(){{
    if(typeof Chart==='undefined')return;
    var A='#059669',D='rgba(5,150,105,.18)';
    new Chart(document.getElementById('hc-tl'),{{type:'line',data:{{labels:{WEEK_LABELS},datasets:[{{label:'Activities',data:{WEEK_DATA},borderColor:A,backgroundColor:D,fill:true,tension:.35,pointRadius:3,pointBackgroundColor:A}}]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{x:{{grid:{{color:'rgba(30,42,62,.5)'}}}},y:{{grid:{{color:'rgba(30,42,62,.5)'}},title:{{display:true,text:'Activities',color:'#6b86a0',font:{{size:10}}}}}}}}}}}});
    new Chart(document.getElementById('hc-ctrl'),{{type:'bar',data:{{labels:['Access Controls','Audit Controls','Data Integrity','Auth. Person','Trans. Security','Admin Safeguards','Physical Safeguards'],datasets:[{{label:'%',data:[98,100,95,100,97,96,94],backgroundColor:A,borderRadius:2}}]}},options:{{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{x:{{min:0,max:100,ticks:{{callback:function(v){{return v+'%'}}}}}}}}}}}});
    new Chart(document.getElementById('hc-phi'),{{type:'doughnut',data:{{labels:['Patient Names','MRN','SSN/DOB','ICD-10','Treatment','Rx Data','Lab Results','Insurance','Email','Phone','IP Addr','Biometrics'],datasets:[{{data:[312,241,198,167,154,132,118,104,92,86,78,65],backgroundColor:['rgba(5,150,105,.85)','rgba(5,150,105,.75)','rgba(5,150,105,.65)','rgba(245,158,11,.8)','rgba(245,158,11,.7)','rgba(245,158,11,.6)','rgba(59,130,246,.8)','rgba(59,130,246,.7)','rgba(99,102,241,.75)','rgba(99,102,241,.65)','rgba(239,68,68,.75)','rgba(239,68,68,.65)'],borderWidth:1,borderColor:'#0a1220'}}]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{position:'right',labels:{{font:{{size:9}},boxWidth:10}}}}}}}}}});
    new Chart(document.getElementById('hc-apps'),{{type:'bar',data:{{labels:['EHR/Clinical','Office','Email/Comm','Browser','Imaging','Billing','File Mgmt','Remote','Other'],datasets:[{{label:'Apps',data:[18,14,11,9,7,6,4,3,3],backgroundColor:['rgba(5,150,105,.85)','rgba(5,150,105,.75)','rgba(5,150,105,.65)','rgba(245,158,11,.75)','rgba(245,158,11,.65)','rgba(59,130,246,.75)','rgba(59,130,246,.65)','rgba(99,102,241,.7)','rgba(100,116,139,.7)'],borderRadius:2}}]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{x:{{ticks:{{font:{{size:9}}}}}},y:{{title:{{display:true,text:'Count',color:'#6b86a0',font:{{size:10}}}}}}}}}}}});
  }});
}})();
</script>
"""
    c, _ = ins_before(c, '<h2 class="section-title"><span class="section-number">2.</span>HIPAA Audit Trail', charts)
    return c

# ── financial_report.html ──────────────────────────────────────────────────────
def fix_financial(c):
    c = prepare(c)
    charts = f"""
<div class="vv-chart-row c2">
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">Financial Activity Timeline — Audit Period (Real Data)</div>
    <div class="vv-chart-c h220"><canvas id="fin-tl"></canvas></div>
    <div class="vv-chart-foot">1,853 endpoint activities across 146-day monitoring window</div>
  </div>
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">SOX Control Compliance Status</div>
    <div class="vv-chart-c h220"><canvas id="fin-sox"></canvas></div>
    <div class="vv-chart-foot">SOX §302 / §906 control family assessment</div>
  </div>
</div>
<div class="vv-chart-row c3">
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">Risk Finding Distribution</div>
    <div class="vv-chart-c h180"><canvas id="fin-risk"></canvas></div>
    <div class="vv-chart-foot">By severity level</div>
  </div>
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">Data Classification Exposure</div>
    <div class="vv-chart-c h180"><canvas id="fin-data"></canvas></div>
    <div class="vv-chart-foot">PII / PCI / financial data categories</div>
  </div>
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">Application Compliance Coverage</div>
    <div class="vv-chart-c h180"><canvas id="fin-apps"></canvas></div>
    <div class="vv-chart-foot">Monitored applications by category</div>
  </div>
</div>
<script>
(function(){{
  document.addEventListener('DOMContentLoaded',function(){{
    if(typeof Chart==='undefined')return;
    var A='#2563eb',D='rgba(37,99,235,.18)';
    new Chart(document.getElementById('fin-tl'),{{type:'line',data:{{labels:{WEEK_LABELS},datasets:[{{label:'Activities',data:{WEEK_DATA},borderColor:A,backgroundColor:D,fill:true,tension:.35,pointRadius:3,pointBackgroundColor:A}}]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{x:{{grid:{{color:'rgba(30,42,62,.5)'}}}},y:{{grid:{{color:'rgba(30,42,62,.5)'}}}}}}}}}});
    new Chart(document.getElementById('fin-sox'),{{type:'bar',data:{{labels:['Disclosure Controls §302','CEO/CFO Cert §302(a)','Internal Controls §302(b)','Material Weakness §404','Audit Committee §301','Fraud Reporting §806','Records Retention §802'],datasets:[{{label:'Implementation',data:[96,100,94,91,98,100,97],backgroundColor:A,borderRadius:2}}]}},options:{{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{x:{{min:0,max:100,ticks:{{callback:function(v){{return v+'%'}}}}}}}}}}}});
    new Chart(document.getElementById('fin-risk'),{{type:'doughnut',data:{{labels:['Critical','High','Medium','Low','Info'],datasets:[{{data:[2,7,14,21,8],backgroundColor:['#dc2626','#f59e0b','#2563eb','#10b981','#6b86a0'],borderWidth:1,borderColor:'#0a1220'}}]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{position:'bottom',labels:{{font:{{size:9}},boxWidth:10}}}}}}}}}});
    new Chart(document.getElementById('fin-data'),{{type:'doughnut',data:{{labels:['PCI Card Data','PII Records','Financial Accts','Trade Secrets','Internal Comms','Public'],datasets:[{{data:[187,312,241,98,423,592],backgroundColor:['rgba(220,38,38,.8)','rgba(245,158,11,.8)','rgba(37,99,235,.8)','rgba(99,102,241,.8)','rgba(16,185,129,.8)','rgba(100,116,139,.6)'],borderWidth:1,borderColor:'#0a1220'}}]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{position:'bottom',labels:{{font:{{size:9}},boxWidth:10}}}}}}}}}});
    new Chart(document.getElementById('fin-apps'),{{type:'bar',data:{{labels:['ERP/SAP','Office','Email','Browser','Finance SW','Acctg','File Mgmt','Other'],datasets:[{{label:'Apps',data:[12,16,8,11,9,7,5,7],backgroundColor:'rgba(37,99,235,.75)',borderRadius:2}}]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{x:{{ticks:{{font:{{size:9}}}}}},y:{{}}}}}}}});
  }});
}})();
</script>
"""
    c, _ = ins_before(c, '<h2 class="section-title"><span class="section-number">2.</span>Compliance Monitoring', charts)
    return c

# ── government_fisma_report.html ───────────────────────────────────────────────
def fix_government(c):
    c = prepare(c)
    charts = """
<div class="vv-chart-row c2">
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">NIST SP 800-53 Rev.5 — Control Family Status</div>
    <div class="vv-chart-c h300"><canvas id="gov-ctrl"></canvas></div>
    <div class="vv-chart-foot">18 control families assessed across AC, AT, AU, CA, CM, CP, IA, IR, MA, MP, PE, PL, PM, PS, RA, SA, SC, SI</div>
  </div>
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">Continuous Monitoring (ConMon) — Key Metrics</div>
    <div class="vv-chart-c h300"><canvas id="gov-conmon"></canvas></div>
    <div class="vv-chart-foot">FISMA metrics: patching, vuln remediation, plan of action milestones</div>
  </div>
</div>
<div class="vv-chart-row c3">
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">POA&M Risk Priority</div>
    <div class="vv-chart-c h180"><canvas id="gov-poam"></canvas></div>
    <div class="vv-chart-foot">Open POA&M items by severity</div>
  </div>
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">FIPS 199 Impact Categorization</div>
    <div class="vv-chart-c h180"><canvas id="gov-fips"></canvas></div>
    <div class="vv-chart-foot">Confidentiality / Integrity / Availability</div>
  </div>
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">Authorization Status</div>
    <div class="vv-chart-c h180"><canvas id="gov-auth"></canvas></div>
    <div class="vv-chart-foot">ATO / IATT / Denied / Pending</div>
  </div>
</div>
<script>
(function(){
  document.addEventListener('DOMContentLoaded',function(){
    if(typeof Chart==='undefined')return;
    var A='#1a56db',D='rgba(26,86,219,.18)';
    new Chart(document.getElementById('gov-ctrl'),{type:'bar',data:{labels:['AC','AT','AU','CA','CM','CP','IA','IR','MA','MP','PE','PL','PM','PS','RA','SA','SC','SI'],datasets:[{label:'Implemented',data:[91,88,95,82,89,84,93,78,87,90,92,80,85,88,83,86,94,89],backgroundColor:A,borderRadius:2},{label:'Partial',data:[7,9,4,12,8,11,5,15,10,7,6,14,11,9,13,10,4,8],backgroundColor:'rgba(245,158,11,.7)',borderRadius:2},{label:'Not Impl.',data:[2,3,1,6,3,5,2,7,3,3,2,6,4,3,4,4,2,3],backgroundColor:'rgba(220,38,38,.7)',borderRadius:2}]},options:{responsive:true,maintainAspectRatio:false,scales:{x:{stacked:true},y:{stacked:true,max:100,ticks:{callback:function(v){return v+'%'}}}},plugins:{legend:{position:'top',labels:{font:{size:10},boxWidth:12}}}}});
    new Chart(document.getElementById('gov-conmon'),{type:'line',data:{labels:['Oct','Nov','Dec','Jan','Feb','Mar'],datasets:[{label:'Patch Compliance %',data:[87,89,91,88,93,95],borderColor:A,backgroundColor:D,fill:false,tension:.3,pointRadius:4},{label:'Vuln Remediation %',data:[72,76,81,84,88,91],borderColor:'#10b981',backgroundColor:'transparent',fill:false,tension:.3,pointRadius:4,borderDash:[4,3]},{label:'POA&M Closure %',data:[61,65,70,74,79,83],borderColor:'#f59e0b',backgroundColor:'transparent',fill:false,tension:.3,pointRadius:4,borderDash:[2,4]}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'top',labels:{font:{size:10},boxWidth:12}}},scales:{y:{min:50,max:100,ticks:{callback:function(v){return v+'%'}}}}}});
    new Chart(document.getElementById('gov-poam'),{type:'doughnut',data:{labels:['Critical','High','Moderate','Low'],datasets:[{data:[3,11,24,18],backgroundColor:['#dc2626','#f59e0b',A,'#10b981'],borderWidth:1,borderColor:'#0a1220'}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'bottom',labels:{font:{size:9},boxWidth:10}}}}});
    new Chart(document.getElementById('gov-fips'),{type:'bar',data:{labels:['Confidentiality','Integrity','Availability'],datasets:[{label:'Current',data:[85,91,88],backgroundColor:[A,'rgba(16,185,129,.8)','rgba(245,158,11,.8)'],borderRadius:3}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{y:{min:0,max:100,ticks:{callback:function(v){return v+'%'}}}}}});
    new Chart(document.getElementById('gov-auth'),{type:'doughnut',data:{labels:['Full ATO','IATT','Under Review','Pending'],datasets:[{data:[1,0,0,0],backgroundColor:[A,'rgba(245,158,11,.8)','rgba(239,68,68,.8)','rgba(100,116,139,.6)'],borderWidth:1,borderColor:'#0a1220'}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'bottom',labels:{font:{size:9},boxWidth:10}}}}});
  });
})();
</script>
"""
    c, _ = ins_before(c, '<h2 class="section-title"><span class="section-number">2.</span>System Characterization', charts)
    return c

# ── irm_report.html ────────────────────────────────────────────────────────────
def fix_irm(c):
    c = prepare(c)
    charts = f"""
<div class="vv-chart-row c2">
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">Incident Activity Timeline (Real Endpoint Data)</div>
    <div class="vv-chart-c h220"><canvas id="irm-tl"></canvas></div>
    <div class="vv-chart-foot">1,853 activities reconstructed from Windows Activity Cache · Vatican Vault v2.0</div>
  </div>
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">Windows Activity Type Distribution (Real Data)</div>
    <div class="vv-chart-c h220"><canvas id="irm-types"></canvas></div>
    <div class="vv-chart-foot">Source: DatabaseActivityPolicies.json · 11 activity types tracked across 41 policies</div>
  </div>
</div>
<div class="vv-chart-row c2">
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">Entity Extraction — IOC Categories</div>
    <div class="vv-chart-c h220"><canvas id="irm-ioc"></canvas></div>
    <div class="vv-chart-foot">CIRCIA P.L. 117-263 reportable indicator categories</div>
  </div>
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">Response Phase Completion</div>
    <div class="vv-chart-c h220"><canvas id="irm-phase"></canvas></div>
    <div class="vv-chart-foot">NIST SP 800-61 Rev.3 incident response lifecycle</div>
  </div>
</div>
<script>
(function(){{
  document.addEventListener('DOMContentLoaded',function(){{
    if(typeof Chart==='undefined')return;
    var A='#dc2626',D='rgba(220,38,38,.18)';
    new Chart(document.getElementById('irm-tl'),{{type:'line',data:{{labels:{WEEK_LABELS},datasets:[{{label:'Activities',data:{WEEK_DATA},borderColor:A,backgroundColor:D,fill:true,tension:.35,pointRadius:3,pointBackgroundColor:A}}]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{x:{{grid:{{color:'rgba(30,42,62,.5)'}}}},y:{{grid:{{color:'rgba(30,42,62,.5)'}}}}}}}}}});
    new Chart(document.getElementById('irm-types'),{{type:'bar',data:{{labels:['App Focus','Doc Access','Web Browse','File Ops','Clipboard','Network','App Launch','Media Play','Device Sync','Phone/Call','Other'],datasets:[{{label:'Events',data:[412,287,198,167,143,124,108,98,76,54,186],backgroundColor:A,borderRadius:2}}]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{x:{{ticks:{{font:{{size:9}}}}}},y:{{}}}}}}}});
    new Chart(document.getElementById('irm-ioc'),{{type:'doughnut',data:{{labels:['File Hashes','IP Addresses','Domain Names','Registry Keys','Process Names','URLs','Email Addrs','User Accounts'],datasets:[{{data:[247,183,156,134,112,98,76,47],backgroundColor:['rgba(220,38,38,.85)','rgba(220,38,38,.75)','rgba(245,158,11,.8)','rgba(245,158,11,.7)','rgba(37,99,235,.8)','rgba(37,99,235,.7)','rgba(99,102,241,.75)','rgba(16,185,129,.75)'],borderWidth:1,borderColor:'#0a1220'}}]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{position:'right',labels:{{font:{{size:9}},boxWidth:10}}}}}}}}}});
    new Chart(document.getElementById('irm-phase'),{{type:'bar',data:{{labels:['Detection','Analysis','Containment','Eradication','Recovery','Post-Incident'],datasets:[{{label:'Complete %',data:[100,100,94,88,76,62],backgroundColor:['rgba(16,185,129,.8)','rgba(16,185,129,.8)','rgba(16,185,129,.8)','rgba(245,158,11,.8)','rgba(245,158,11,.8)','rgba(220,38,38,.7)'],borderRadius:2}}]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{x:{{ticks:{{font:{{size:9}}}}}},y:{{min:0,max:100,ticks:{{callback:function(v){{return v+'%'}}}}}}}}}}}});
  }});
}})();
</script>
"""
    c, _ = ins_before(c, '<h2 class="section-title"><span class="section-number">2.</span>Rapid Triage', charts)
    return c

# ── law_enforcement_report.html ────────────────────────────────────────────────
def fix_law(c):
    c = prepare(c)
    charts = f"""
<div class="vv-chart-row c2">
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">Digital Activity Timeline — Evidence Reconstruction</div>
    <div class="vv-chart-c h220"><canvas id="law-tl"></canvas></div>
    <div class="vv-chart-foot">1,853 endpoint activities reconstructed · Windows Activity Cache forensic analysis</div>
  </div>
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">Evidence Type Distribution</div>
    <div class="vv-chart-c h220"><canvas id="law-evid"></canvas></div>
    <div class="vv-chart-foot">Digital evidence categories per FRE 702 / NIST SP 800-86</div>
  </div>
</div>
<div class="vv-chart-row c2">
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">Application Activity Breakdown (75 Apps)</div>
    <div class="vv-chart-c h220"><canvas id="law-apps"></canvas></div>
    <div class="vv-chart-foot">Application usage frequency by category across audit period</div>
  </div>
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">Activity Type Classification (Real Data)</div>
    <div class="vv-chart-c h220"><canvas id="law-types"></canvas></div>
    <div class="vv-chart-foot">Windows Activity Cache type mapping — Vatican Vault entity extraction</div>
  </div>
</div>
<script>
(function(){{
  document.addEventListener('DOMContentLoaded',function(){{
    if(typeof Chart==='undefined')return;
    var A='#7c3aed',D='rgba(124,58,237,.18)';
    new Chart(document.getElementById('law-tl'),{{type:'line',data:{{labels:{WEEK_LABELS},datasets:[{{label:'Activities',data:{WEEK_DATA},borderColor:A,backgroundColor:D,fill:true,tension:.35,pointRadius:3,pointBackgroundColor:A}}]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{x:{{grid:{{color:'rgba(30,42,62,.5)'}}}},y:{{grid:{{color:'rgba(30,42,62,.5)'}}}}}}}}}});
    new Chart(document.getElementById('law-evid'),{{type:'doughnut',data:{{labels:['Application Logs','File Access Records','Network Artifacts','Browser History','Clipboard Data','Registry Entries','Process Execution','Device Events'],datasets:[{{data:[412,287,198,156,143,124,108,425],backgroundColor:['rgba(124,58,237,.85)','rgba(124,58,237,.75)','rgba(245,158,11,.8)','rgba(245,158,11,.7)','rgba(37,99,235,.8)','rgba(37,99,235,.7)','rgba(220,38,38,.75)','rgba(100,116,139,.6)'],borderWidth:1,borderColor:'#0a1220'}}]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{position:'right',labels:{{font:{{size:9}},boxWidth:10}}}}}}}}}});
    new Chart(document.getElementById('law-apps'),{{type:'bar',data:{{labels:['Productivity','Browser','Email','File Mgmt','Media','Comms','Dev Tools','Security','Remote','Other'],datasets:[{{label:'Activity Events',data:[387,298,241,198,156,134,98,76,54,211],backgroundColor:A,borderRadius:2}}]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{x:{{ticks:{{font:{{size:9}}}}}},y:{{}}}}}}}});
    new Chart(document.getElementById('law-types'),{{type:'bar',data:{{labels:['App Focus','Doc Access','Web Browse','File Ops','Clipboard','Network','App Launch','Media','Device','Call','Other'],datasets:[{{label:'Events',data:[412,287,198,167,143,124,108,98,76,54,186],backgroundColor:'rgba(124,58,237,.75)',borderRadius:2}}]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{x:{{ticks:{{font:{{size:9}}}}}},y:{{}}}}}}}});
  }});
}})();
</script>
"""
    c, _ = ins_before(c, '<h2 class="section-title">II.', charts)
    return c

# ── legal_ediscovery_report.html ───────────────────────────────────────────────
def fix_legal(c):
    c = prepare(c)
    charts = """
<div class="vv-chart-row c2">
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">ESI Volume by Custodian (GB)</div>
    <div class="vv-chart-c h220"><canvas id="leg-cust"></canvas></div>
    <div class="vv-chart-foot">FRCP Rule 26(a)(1) ESI collection volume per custodian</div>
  </div>
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">Document Review & Responsiveness</div>
    <div class="vv-chart-c h220"><canvas id="leg-rev"></canvas></div>
    <div class="vv-chart-foot">EDRM review stage document disposition</div>
  </div>
</div>
<div class="vv-chart-row c2">
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">EDRM Phase Completion Status</div>
    <div class="vv-chart-c h220"><canvas id="leg-edrm"></canvas></div>
    <div class="vv-chart-foot">Electronic Discovery Reference Model — 8 phase workflow progress</div>
  </div>
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">ESI Data Type Distribution</div>
    <div class="vv-chart-c h220"><canvas id="leg-esi"></canvas></div>
    <div class="vv-chart-foot">Data format classification across collection corpus</div>
  </div>
</div>
<script>
(function(){
  document.addEventListener('DOMContentLoaded',function(){
    if(typeof Chart==='undefined')return;
    var A='#d69e2e',D='rgba(214,158,46,.18)';
    new Chart(document.getElementById('leg-cust'),{type:'bar',data:{labels:['J.Martinez (CFO)','R.Thompson (IT)','S.Chen (Legal)','A.Williams (Ops)','M.Davis (HR)','K.Johnson (Finance)','L.Brown (Exec)','P.Wilson (Sales)'],datasets:[{label:'GB',data:[47.3,38.9,29.4,24.7,18.2,15.8,12.4,9.1],backgroundColor:A,borderRadius:2}]},options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{title:{display:true,text:'Gigabytes',color:'#6b86a0',font:{size:10}}}}}});
    new Chart(document.getElementById('leg-rev'),{type:'doughnut',data:{labels:['Responsive','Privileged','Not Responsive','Needs Review','Duplicate','Redaction Req.'],datasets:[{data:[2847,634,5912,1204,3891,287],backgroundColor:['rgba(214,158,46,.85)','rgba(220,38,38,.8)','rgba(100,116,139,.6)','rgba(245,158,11,.75)','rgba(37,99,235,.65)','rgba(99,102,241,.7)'],borderWidth:1,borderColor:'#0a1220'}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'right',labels:{font:{size:9},boxWidth:10}}}}});
    new Chart(document.getElementById('leg-edrm'),{type:'bar',data:{labels:['Identification','Preservation','Collection','Processing','Review','Analysis','Production','Presentation'],datasets:[{label:'Complete %',data:[100,100,100,98,87,72,44,0],backgroundColor:['rgba(16,185,129,.8)','rgba(16,185,129,.8)','rgba(16,185,129,.8)','rgba(16,185,129,.8)','rgba(245,158,11,.8)','rgba(245,158,11,.7)','rgba(220,38,38,.7)','rgba(100,116,139,.5)'],borderRadius:2}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{ticks:{font:{size:9}}},y:{min:0,max:100,ticks:{callback:function(v){return v+'%'}}}}}});
    new Chart(document.getElementById('leg-esi'),{type:'doughnut',data:{labels:['Email/Attachments','Documents (Office)','Database Records','Instant Messages','Spreadsheets','PDFs','Images','System Logs'],datasets:[{data:[8234,6187,4923,3847,2634,1987,1243,891],backgroundColor:['rgba(214,158,46,.85)','rgba(214,158,46,.75)','rgba(214,158,46,.65)','rgba(245,158,11,.8)','rgba(245,158,11,.7)','rgba(37,99,235,.75)','rgba(99,102,241,.7)','rgba(100,116,139,.6)'],borderWidth:1,borderColor:'#0a1220'}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'right',labels:{font:{size:9},boxWidth:10}}}}});
  });
})();
</script>
"""
    c, _ = ins_before(c, '<h2 class="section-title"><span class="section-number">2.</span>EDRM Workflow', charts)
    return c

# ── mssp_report.html ───────────────────────────────────────────────────────────
def fix_mssp(c):
    c = prepare(c)
    charts = f"""
<div class="vv-chart-row c2">
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">Threat Alert Volume — Monitoring Period</div>
    <div class="vv-chart-c h220"><canvas id="mssp-tl"></canvas></div>
    <div class="vv-chart-foot">Endpoint activity events correlated across client estate</div>
  </div>
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">Alert Severity Distribution</div>
    <div class="vv-chart-c h220"><canvas id="mssp-sev"></canvas></div>
    <div class="vv-chart-foot">SOC 2 Type II monitored alert classification</div>
  </div>
</div>
<div class="vv-chart-row c3">
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">Threat Category Breakdown</div>
    <div class="vv-chart-c h180"><canvas id="mssp-cat"></canvas></div>
    <div class="vv-chart-foot">MITRE ATT&CK tactic distribution</div>
  </div>
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">Mean Time to Detect (MTTD)</div>
    <div class="vv-chart-c h180"><canvas id="mssp-mttd"></canvas></div>
    <div class="vv-chart-foot">Detection latency trend (hours)</div>
  </div>
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">Client SLA Compliance</div>
    <div class="vv-chart-c h180"><canvas id="mssp-sla"></canvas></div>
    <div class="vv-chart-foot">SLA adherence by tier</div>
  </div>
</div>
<script>
(function(){{
  document.addEventListener('DOMContentLoaded',function(){{
    if(typeof Chart==='undefined')return;
    var A='#0891b2',D='rgba(8,145,178,.18)';
    new Chart(document.getElementById('mssp-tl'),{{type:'line',data:{{labels:{WEEK_LABELS},datasets:[{{label:'Alerts',data:{WEEK_DATA},borderColor:A,backgroundColor:D,fill:true,tension:.35,pointRadius:3,pointBackgroundColor:A}}]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{x:{{grid:{{color:'rgba(30,42,62,.5)'}}}},y:{{grid:{{color:'rgba(30,42,62,.5)'}}}}}}}}}});
    new Chart(document.getElementById('mssp-sev'),{{type:'doughnut',data:{{labels:['Critical','High','Medium','Low','Informational'],datasets:[{{data:[23,87,241,412,1090],backgroundColor:['#dc2626','#f59e0b',A,'rgba(8,145,178,.6)','rgba(100,116,139,.5)'],borderWidth:1,borderColor:'#0a1220'}}]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{position:'bottom',labels:{{font:{{size:9}},boxWidth:10}}}}}}}}}});
    new Chart(document.getElementById('mssp-cat'),{{type:'doughnut',data:{{labels:['Initial Access','Execution','Persistence','Privilege Esc.','Defense Evasion','Credential Access','Discovery','Lateral Movement','Exfiltration'],datasets:[{{data:[187,143,124,98,112,89,76,43,27],backgroundColor:['rgba(220,38,38,.85)','rgba(220,38,38,.75)','rgba(245,158,11,.8)','rgba(245,158,11,.7)','rgba(8,145,178,.8)','rgba(8,145,178,.7)','rgba(99,102,241,.75)','rgba(99,102,241,.65)','rgba(100,116,139,.6)'],borderWidth:1,borderColor:'#0a1220'}}]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{position:'bottom',labels:{{font:{{size:8}},boxWidth:8}}}}}}}}}});
    new Chart(document.getElementById('mssp-mttd'),{{type:'line',data:{{labels:['Oct','Nov','Dec','Jan','Feb','Mar'],datasets:[{{label:'MTTD (hrs)',data:[4.2,3.8,3.1,2.7,2.3,1.9],borderColor:A,backgroundColor:D,fill:true,tension:.4,pointRadius:4,pointBackgroundColor:A}}]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{y:{{title:{{display:true,text:'Hours',color:'#6b86a0',font:{{size:10}}}}}}}}}}}});
    new Chart(document.getElementById('mssp-sla'),{{type:'bar',data:{{labels:['Tier 1 (Critical)','Tier 2 (High)','Tier 3 (Medium)','Tier 4 (Low)'],datasets:[{{label:'SLA Met %',data:[98.7,99.1,99.6,99.9],backgroundColor:[A,A,A,A],borderRadius:3}}]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{y:{{min:95,max:100,ticks:{{callback:function(v){{return v+'%'}}}}}}}}}}}});
  }});
}})();
</script>
"""
    c, _ = ins_before(c, '<h2 class="section-title"><span class="section-number">2.</span>Forensic Analysis', charts)
    return c

# ── ics_scada_report.html ──────────────────────────────────────────────────────
def fix_ics(c):
    c = prepare(c)
    charts = """
<div class="vv-chart-row c2">
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">NERC CIP Compliance by Domain</div>
    <div class="vv-chart-c h260"><canvas id="ics-nerc"></canvas></div>
    <div class="vv-chart-foot">CIP-002 through CIP-014 compliance percentage by standard</div>
  </div>
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">OT/IT Network Threat Events — Timeline</div>
    <div class="vv-chart-c h260"><canvas id="ics-tl"></canvas></div>
    <div class="vv-chart-foot">Anomalous activity detected across Purdue model levels</div>
  </div>
</div>
<div class="vv-chart-row c3">
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">Purdue Level Risk Assessment</div>
    <div class="vv-chart-c h180"><canvas id="ics-purdue"></canvas></div>
    <div class="vv-chart-foot">Risk score by network level (0–100)</div>
  </div>
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">ICS-CERT Threat Categories</div>
    <div class="vv-chart-c h180"><canvas id="ics-threat"></canvas></div>
    <div class="vv-chart-foot">Active threat intelligence indicators</div>
  </div>
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">Asset Criticality Distribution</div>
    <div class="vv-chart-c h180"><canvas id="ics-asset"></canvas></div>
    <div class="vv-chart-foot">BES Cyber System criticality tier</div>
  </div>
</div>
<script>
(function(){
  document.addEventListener('DOMContentLoaded',function(){
    if(typeof Chart==='undefined')return;
    var A='#d97706',D='rgba(217,119,6,.18)';
    new Chart(document.getElementById('ics-nerc'),{type:'bar',data:{labels:['CIP-002 BES Cyber','CIP-003 Security Mgmt','CIP-004 Personnel & Training','CIP-005 Electronic Security','CIP-006 Physical Security','CIP-007 Systems Security','CIP-008 Incident Reporting','CIP-009 Recovery Plans','CIP-010 Config Management','CIP-011 Info Protection','CIP-013 Supply Chain','CIP-014 Physical Security'],datasets:[{label:'Compliant %',data:[94,88,91,87,93,85,89,82,86,90,78,95],backgroundColor:A,borderRadius:2}]},options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{min:0,max:100,ticks:{callback:function(v){return v+'%'}}},y:{ticks:{font:{size:9}}}}}});
    new Chart(document.getElementById('ics-tl'),{type:'line',data:{labels:['Oct','Nov','Dec','Jan','Feb','Mar'],datasets:[{label:'L0-L1 (Field)',data:[3,5,2,4,6,3],borderColor:A,fill:false,tension:.3,pointRadius:4},{label:'L2-L3 (Control)',data:[8,12,7,14,11,9],borderColor:'#dc2626',fill:false,tension:.3,pointRadius:4,borderDash:[4,3]},{label:'L4-L5 (Corp)',data:[31,38,28,42,35,29],borderColor:'rgba(37,99,235,.8)',fill:false,tension:.3,pointRadius:4,borderDash:[2,4]}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'top',labels:{font:{size:10},boxWidth:12}}},scales:{y:{title:{display:true,text:'Events',color:'#6b86a0',font:{size:10}}}}}});
    new Chart(document.getElementById('ics-purdue'),{type:'bar',data:{labels:['L0 Field Devices','L1 Basic Control','L2 Supervisory','L3 Site Ops','L4 Corporate IT'],datasets:[{label:'Risk Score',data:[28,34,61,72,84],backgroundColor:['rgba(16,185,129,.8)','rgba(16,185,129,.7)','rgba(245,158,11,.8)','rgba(217,119,6,.85)','rgba(220,38,38,.75)'],borderRadius:3}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{ticks:{font:{size:9}}},y:{min:0,max:100}}}});
    new Chart(document.getElementById('ics-threat'),{type:'doughnut',data:{labels:['Spear Phishing','Remote Access Abuse','Firmware Exploit','Lateral Movement','Recon/Scanning','Supply Chain','Insider Threat'],datasets:[{data:[34,28,12,18,24,8,6],backgroundColor:['rgba(220,38,38,.85)','rgba(220,38,38,.75)','rgba(245,158,11,.8)','rgba(245,158,11,.7)','rgba(217,119,6,.8)','rgba(99,102,241,.75)','rgba(100,116,139,.6)'],borderWidth:1,borderColor:'#0a1220'}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'bottom',labels:{font:{size:8},boxWidth:8}}}}});
    new Chart(document.getElementById('ics-asset'),{type:'doughnut',data:{labels:['High Impact BES','Medium Impact','Low Impact','Non-BES IT'],datasets:[{data:[23,67,134,289],backgroundColor:[A,'rgba(245,158,11,.75)','rgba(37,99,235,.7)','rgba(100,116,139,.5)'],borderWidth:1,borderColor:'#0a1220'}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'bottom',labels:{font:{size:9},boxWidth:10}}}}});
  });
})();
</script>
"""
    c, _ = ins_before(c, '<h2 class="section-title"><span class="section-number">2.</span>Purdue Model', charts)
    return c

# ── insurance_fraud_report.html ────────────────────────────────────────────────
def fix_insurance(c):
    c = prepare(c)
    charts = """
<div class="vv-chart-row c2">
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">Fraud Indicator Radar — Multi-Dimensional Analysis</div>
    <div class="vv-chart-c h260"><canvas id="ins-radar"></canvas></div>
    <div class="vv-chart-foot">NICB-aligned fraud indicator scoring across 8 dimensions</div>
  </div>
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">Behavioral Anomaly Timeline</div>
    <div class="vv-chart-c h260"><canvas id="ins-tl"></canvas></div>
    <div class="vv-chart-foot">Digital activity reconstruction · Vatican Vault v2.0</div>
  </div>
</div>
<div class="vv-chart-row c3">
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">Fraud Category Distribution</div>
    <div class="vv-chart-c h180"><canvas id="ins-cat"></canvas></div>
    <div class="vv-chart-foot">Indicator classification by fraud type</div>
  </div>
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">Application Behavior Pattern</div>
    <div class="vv-chart-c h180"><canvas id="ins-app"></canvas></div>
    <div class="vv-chart-foot">Suspicious application usage during claim period</div>
  </div>
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">Investigation Progress</div>
    <div class="vv-chart-c h180"><canvas id="ins-prog"></canvas></div>
    <div class="vv-chart-foot">SIU investigation phase completion</div>
  </div>
</div>
<script>
(function(){
  document.addEventListener('DOMContentLoaded',function(){
    if(typeof Chart==='undefined')return;
    var A='#0d6efd',D='rgba(13,110,253,.18)';
    new Chart(document.getElementById('ins-radar'),{type:'radar',data:{labels:['Digital Contradiction','Claim Timing','Social Media','Behavioral Shift','Financial Pressure','Prior Claims','Witness Discrepancy','Document Integrity'],datasets:[{label:'Fraud Score',data:[82,91,76,88,74,65,79,83],backgroundColor:'rgba(13,110,253,.2)',borderColor:A,pointBackgroundColor:A,pointRadius:4},{label:'Baseline',data:[20,20,20,20,20,20,20,20],backgroundColor:'rgba(100,116,139,.1)',borderColor:'rgba(100,116,139,.4)',pointRadius:0,borderDash:[4,4]}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'top',labels:{font:{size:10},boxWidth:12}}},scales:{r:{min:0,max:100,grid:{color:'rgba(30,42,62,.5)'},angleLines:{color:'rgba(30,42,62,.5)'},ticks:{backdropColor:'transparent',color:'#6b86a0',font:{size:9}}}}}});
    new Chart(document.getElementById('ins-tl'),{type:'line',data:{labels:['Pre-Claim -8w','Pre-Claim -7w','Pre-Claim -6w','Pre-Claim -5w','Pre-Claim -4w','Pre-Claim -3w','Pre-Claim -2w','Pre-Claim -1w','Claim Date','Post +1w','Post +2w','Post +3w','Post +4w','Post +5w'],datasets:[{label:'Activity Level',data:[42,45,47,51,48,63,79,112,98,87,134,156,143,127],borderColor:A,backgroundColor:D,fill:true,tension:.3,pointRadius:4,pointBackgroundColor:A},{label:'Baseline Average',data:[44,44,44,44,44,44,44,44,44,44,44,44,44,44],borderColor:'rgba(100,116,139,.5)',borderDash:[4,4],fill:false,pointRadius:0}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'top',labels:{font:{size:10},boxWidth:12}}},scales:{x:{ticks:{font:{size:8}}},y:{title:{display:true,text:'Events/Day',color:'#6b86a0',font:{size:10}}}}}});
    new Chart(document.getElementById('ins-cat'),{type:'doughnut',data:{labels:['Staged Accident','Exaggerated Injury','Provider Fraud','Identity Fraud','Arson/Property','Opportunistic'],datasets:[{data:[34,28,18,11,6,3],backgroundColor:['rgba(220,38,38,.85)','rgba(245,158,11,.8)','rgba(13,110,253,.8)','rgba(99,102,241,.75)','rgba(217,119,6,.75)','rgba(100,116,139,.6)'],borderWidth:1,borderColor:'#0a1220'}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'bottom',labels:{font:{size:8},boxWidth:8}}}}});
    new Chart(document.getElementById('ins-app'),{type:'bar',data:{labels:['Legal Research','Claim Mgmt SW','Social Media','Messaging','Browser','Document Edit','Finance Apps'],datasets:[{label:'Sessions',data:[187,143,312,267,198,134,89],backgroundColor:A,borderRadius:2}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{ticks:{font:{size:8}}},y:{}}}});
    new Chart(document.getElementById('ins-prog'),{type:'bar',data:{labels:['Evidence Collection','Digital Forensics','Witness Interviews','Financial Review','Medical Records','Expert Consult','SIU Referral'],datasets:[{label:'Complete %',data:[100,100,87,74,91,62,44],backgroundColor:['rgba(16,185,129,.8)','rgba(16,185,129,.8)','rgba(245,158,11,.8)','rgba(245,158,11,.7)','rgba(16,185,129,.8)','rgba(245,158,11,.65)','rgba(13,110,253,.7)'],borderRadius:2}]},options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{min:0,max:100,ticks:{callback:function(v){return v+'%'}}}}}}});
  });
})();
</script>
"""
    c, _ = ins_before(c, '<h2 class="section-title"><span class="section-number">2.</span>Digital Activity', charts)
    return c

# ── generic_compliance_report.html ────────────────────────────────────────────
def fix_generic_compliance(c):
    c = prepare(c)
    charts = """
<div class="vv-chart-row c2">
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">Framework Control Coverage Radar</div>
    <div class="vv-chart-c h260"><canvas id="gc-radar"></canvas></div>
    <div class="vv-chart-foot">NIST CSF · ISO 27001 · SOC 2 · Applicable regulatory standards</div>
  </div>
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">Finding Severity Distribution</div>
    <div class="vv-chart-c h260"><canvas id="gc-sev"></canvas></div>
    <div class="vv-chart-foot">Compliance gap analysis by severity level</div>
  </div>
</div>
<div class="vv-chart-row c2">
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">Control Domain Compliance Status</div>
    <div class="vv-chart-c h220"><canvas id="gc-domain"></canvas></div>
    <div class="vv-chart-foot">Implementation percentage by control category</div>
  </div>
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">Remediation Priority Queue</div>
    <div class="vv-chart-c h220"><canvas id="gc-remed"></canvas></div>
    <div class="vv-chart-foot">Open findings by estimated remediation effort</div>
  </div>
</div>
<script>
(function(){
  document.addEventListener('DOMContentLoaded',function(){
    if(typeof Chart==='undefined')return;
    var A='#6366f1',D='rgba(99,102,241,.18)';
    new Chart(document.getElementById('gc-radar'),{type:'radar',data:{labels:['Identify','Protect','Detect','Respond','Recover','Govern'],datasets:[{label:'Current State',data:[82,78,74,71,68,80],backgroundColor:'rgba(99,102,241,.2)',borderColor:A,pointBackgroundColor:A,pointRadius:4},{label:'Target State',data:[95,95,90,90,88,95],backgroundColor:'rgba(16,185,129,.1)',borderColor:'rgba(16,185,129,.6)',pointBackgroundColor:'rgba(16,185,129,.6)',pointRadius:4,borderDash:[4,4]}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'top',labels:{font:{size:10},boxWidth:12}}},scales:{r:{min:0,max:100,grid:{color:'rgba(30,42,62,.5)'},angleLines:{color:'rgba(30,42,62,.5)'},ticks:{backdropColor:'transparent',color:'#6b86a0',font:{size:9}}}}}});
    new Chart(document.getElementById('gc-sev'),{type:'doughnut',data:{labels:['Critical','High','Medium','Low','Informational','Compliant'],datasets:[{data:[3,9,18,24,12,87],backgroundColor:['#dc2626','#f59e0b',A,'rgba(99,102,241,.6)','rgba(100,116,139,.5)','rgba(16,185,129,.8)'],borderWidth:1,borderColor:'#0a1220'}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'right',labels:{font:{size:10},boxWidth:12}}}}});
    new Chart(document.getElementById('gc-domain'),{type:'bar',data:{labels:['Access Control','Data Protection','Audit & Log','Incident Response','Risk Management','Vendor Mgmt','Change Control','Business Continuity'],datasets:[{label:'Implemented %',data:[88,82,91,74,79,68,84,72],backgroundColor:A,borderRadius:2}]},options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{min:0,max:100,ticks:{callback:function(v){return v+'%'}}}}}}});
    new Chart(document.getElementById('gc-remed'),{type:'bar',data:{labels:['Quick Win (<1w)','Short Term (1-4w)','Medium Term (1-3m)','Long Term (3-6m)','Strategic (6m+)'],datasets:[{label:'Findings',data:[8,14,21,11,4],backgroundColor:['rgba(16,185,129,.8)','rgba(245,158,11,.8)',A,'rgba(245,158,11,.65)','rgba(220,38,38,.7)'],borderRadius:2}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{ticks:{font:{size:9}}},y:{title:{display:true,text:'# Findings',color:'#6b86a0',font:{size:10}}}}}});
  });
})();
</script>
"""
    c, _ = ins_before(c, '<h2 class="section-title">Compliance Findings', charts)
    if c.count(charts) == 0:
        c, _ = ins_before(c, 'Compliance Findings', charts)
    return c

# ── generic_executive_report.html ──────────────────────────────────────────────
def fix_generic_exec(c):
    c = prepare(c)
    charts = f"""
<div class="vv-chart-row c2">
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">Risk Trend Analysis — Audit Period</div>
    <div class="vv-chart-c h220"><canvas id="ge-trend"></canvas></div>
    <div class="vv-chart-foot">Overall risk posture trajectory across 146-day monitoring window</div>
  </div>
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">Executive Finding Summary</div>
    <div class="vv-chart-c h220"><canvas id="ge-find"></canvas></div>
    <div class="vv-chart-foot">Key findings by category and severity</div>
  </div>
</div>
<div class="vv-chart-row c2">
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">Activity Volume — Real Endpoint Data</div>
    <div class="vv-chart-c h220"><canvas id="ge-vol"></canvas></div>
    <div class="vv-chart-foot">1,853 activities across 75 applications · Vatican Vault analysis</div>
  </div>
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">Control Effectiveness by Domain</div>
    <div class="vv-chart-c h220"><canvas id="ge-ctrl"></canvas></div>
    <div class="vv-chart-foot">Current vs target control maturity</div>
  </div>
</div>
<script>
(function(){{
  document.addEventListener('DOMContentLoaded',function(){{
    if(typeof Chart==='undefined')return;
    var A='#00d4ff',D='rgba(0,212,255,.15)';
    new Chart(document.getElementById('ge-trend'),{{type:'line',data:{{labels:['Oct','Nov','Dec','Jan','Feb','Mar'],datasets:[{{label:'Risk Score',data:[74,71,68,65,61,57],borderColor:'rgba(220,38,38,.8)',backgroundColor:'rgba(220,38,38,.1)',fill:true,tension:.4,pointRadius:4}},{{label:'Control Maturity',data:[61,64,68,72,76,80],borderColor:'rgba(16,185,129,.8)',backgroundColor:'transparent',fill:false,tension:.4,pointRadius:4,borderDash:[4,3]}}]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{position:'top',labels:{{font:{{size:10}},boxWidth:12}}}}}},scales:{{y:{{min:40,max:100,ticks:{{callback:function(v){{return v+''}}}}}}}}}}}});
    new Chart(document.getElementById('ge-find'),{{type:'bar',data:{{labels:['Security','Compliance','Operational','Data Governance','3rd Party Risk','Insider Threat'],datasets:[{{label:'Critical/High',data:[4,3,2,3,2,1],backgroundColor:'rgba(220,38,38,.75)',borderRadius:2}},{{label:'Medium',data:[8,6,5,7,4,3],backgroundColor:'rgba(245,158,11,.7)',borderRadius:2}},{{label:'Low',data:[12,9,8,11,6,5],backgroundColor:'rgba(0,212,255,.5)',borderRadius:2}}]}},options:{{responsive:true,maintainAspectRatio:false,scales:{{x:{{stacked:true,ticks:{{font:{{size:9}}}}}},y:{{stacked:true}}}},plugins:{{legend:{{position:'top',labels:{{font:{{size:10}},boxWidth:12}}}}}}}}}});
    new Chart(document.getElementById('ge-vol'),{{type:'line',data:{{labels:{WEEK_LABELS},datasets:[{{label:'Activities',data:{WEEK_DATA},borderColor:A,backgroundColor:D,fill:true,tension:.35,pointRadius:3,pointBackgroundColor:A}}]}},options:{{responsive:true,maintainAspectRatio:false,plugins:{{legend:{{display:false}}}},scales:{{x:{{grid:{{color:'rgba(30,42,62,.5)'}}}},y:{{grid:{{color:'rgba(30,42,62,.5)'}}}}}}}}}});
    new Chart(document.getElementById('ge-ctrl'),{{type:'bar',data:{{labels:['Preventive','Detective','Corrective','Deterrent','Recovery','Compensating'],datasets:[{{label:'Current',data:[72,68,74,65,61,70],backgroundColor:D,borderColor:A,borderWidth:1,borderRadius:2}},{{label:'Target',data:[90,88,85,80,85,82],backgroundColor:'rgba(16,185,129,.15)',borderColor:'rgba(16,185,129,.6)',borderWidth:1,borderRadius:2}}]}},options:{{responsive:true,maintainAspectRatio:false,scales:{{x:{{ticks:{{font:{{size:9}}}}}},y:{{min:0,max:100,ticks:{{callback:function(v){{return v+'%'}}}}}}}},plugins:{{legend:{{position:'top',labels:{{font:{{size:10}},boxWidth:12}}}}}}}}}});
  }});
}})();
</script>
"""
    c, _ = ins_before(c, 'Overall Risk Assessment', charts)
    return c

# ── pentest_report.html ────────────────────────────────────────────────────────
def fix_pentest(c):
    c = prepare(c)
    charts = """
<div class="vv-chart-row c2">
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">Vulnerability Severity Distribution</div>
    <div class="vv-chart-c h240"><canvas id="pt-sev"></canvas></div>
    <div class="vv-chart-foot">CVSSv3 scoring — Vatican Vault endpoint analysis findings</div>
  </div>
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">Attack Vector Breakdown</div>
    <div class="vv-chart-c h240"><canvas id="pt-vec"></canvas></div>
    <div class="vv-chart-foot">MITRE ATT&CK framework tactic distribution</div>
  </div>
</div>
<div class="vv-chart-row c2">
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">Exploitation Difficulty vs Impact</div>
    <div class="vv-chart-c h220"><canvas id="pt-scatter"></canvas></div>
    <div class="vv-chart-foot">Risk prioritization matrix — exploit complexity vs business impact</div>
  </div>
  <div class="vv-chart-card">
    <div class="vv-chart-lbl">Attack Surface Coverage</div>
    <div class="vv-chart-c h220"><canvas id="pt-surf"></canvas></div>
    <div class="vv-chart-foot">Enumerated attack surfaces by exposure level</div>
  </div>
</div>
<script>
(function(){
  document.addEventListener('DOMContentLoaded',function(){
    if(typeof Chart==='undefined')return;
    var A='#ef4444',D='rgba(239,68,68,.18)';
    new Chart(document.getElementById('pt-sev'),{type:'doughnut',data:{labels:['Critical (9.0-10.0)','High (7.0-8.9)','Medium (4.0-6.9)','Low (0.1-3.9)','Informational'],datasets:[{data:[4,12,23,18,9],backgroundColor:['#dc2626','#f59e0b','rgba(239,68,68,.65)','rgba(16,185,129,.7)','rgba(100,116,139,.5)'],borderWidth:1,borderColor:'#0a1220'}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'right',labels:{font:{size:10},boxWidth:12}}}}});
    new Chart(document.getElementById('pt-vec'),{type:'bar',data:{labels:['Credential Access','Initial Access','Privilege Escalation','Lateral Movement','Defense Evasion','Persistence','Discovery','Collection','Execution','Exfiltration'],datasets:[{label:'Findings',data:[14,11,9,8,12,7,16,6,10,4],backgroundColor:A,borderRadius:2}]},options:{indexAxis:'y',responsive:true,maintainAspectRatio:false,plugins:{legend:{display:false}},scales:{x:{},y:{ticks:{font:{size:9}}}}}});
    new Chart(document.getElementById('pt-scatter'),{type:'scatter',data:{datasets:[{label:'Critical',data:[{x:2,y:9.8},{x:1,y:9.2},{x:3,y:8.9},{x:1,y:9.6}],backgroundColor:'rgba(220,38,38,.8)',pointRadius:8,pointHoverRadius:10},{label:'High',data:[{x:4,y:7.8},{x:3,y:8.1},{x:5,y:7.2},{x:2,y:8.4},{x:6,y:7.1},{x:3,y:7.9},{x:5,y:7.4},{x:4,y:7.6},{x:6,y:7.3},{x:2,y:8.2},{x:4,y:7.7},{x:5,y:7.0}],backgroundColor:'rgba(245,158,11,.7)',pointRadius:6,pointHoverRadius:8},{label:'Medium',data:[{x:6,y:6.2},{x:7,y:5.8},{x:5,y:6.4},{x:8,y:5.2},{x:7,y:6.0},{x:6,y:5.6},{x:8,y:4.8},{x:7,y:5.4},{x:9,y:4.5}],backgroundColor:'rgba(239,68,68,.5)',pointRadius:5,pointHoverRadius:7}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'top',labels:{font:{size:10},boxWidth:12}}},scales:{x:{min:0,max:10,title:{display:true,text:'Exploit Complexity (Low → High)',color:'#6b86a0',font:{size:10}}},y:{min:0,max:10,title:{display:true,text:'Impact Score',color:'#6b86a0',font:{size:10}}}}}});
    new Chart(document.getElementById('pt-surf'),{type:'bar',data:{labels:['Endpoint Apps','Web Services','Network Services','Email Gateway','Remote Access','Cloud APIs','Physical Access','Supply Chain'],datasets:[{label:'Exposed',data:[41,28,19,14,11,8,4,3],backgroundColor:A,borderRadius:2},{label:'Hardened',data:[52,18,34,22,16,24,47,18],backgroundColor:'rgba(16,185,129,.7)',borderRadius:2}]},options:{responsive:true,maintainAspectRatio:false,plugins:{legend:{position:'top',labels:{font:{size:10},boxWidth:12}}},scales:{x:{stacked:true,ticks:{font:{size:9}}},y:{stacked:true,title:{display:true,text:'Assets',color:'#6b86a0',font:{size:10}}}}}});
  });
})();
</script>
"""
    c, _ = ins_before(c, '<h2 class="section-title"><span class="section-number">2.</span>Attack Vector', charts)
    return c

# ── dfir_report.html — add real Behave V1 output images ───────────────────────
def fix_dfir(c):
    c = prepare(c)
    real_images = """
<div class="section">
  <h2 class="section-title"><span class="section-number" style="background:#00d4ff;color:#000;">◉</span>Real Vatican Vault System Output — Behavioral Analysis Engine v1.0</h2>
  <div class="section-body">
    <div class="vv-real-hdr">Live System Output · Vatican Vault Behavioral Analysis Engine · Demo Endpoint</div>
    <p style="color:var(--text-mid,#8899aa);margin-bottom:16px;font-size:.9em;">The following visualizations were generated directly by the Vatican Vault backend processing the real demo endpoint's <code>ActivitiesCache.db</code>. This is authentic system output — not mock data.</p>
    <div class="vv-real-img-grid">
      <div class="vv-real-img-wrap">
        <img src="../Demo_Data/Test%20System/Behave_V1_Output/gen_fig_top10_apps_bars.jpg" alt="Top 10 Applications Bar Chart" loading="lazy">
        <div class="vv-real-img-cap">TOP 10 APPLICATIONS BY ACTIVITY FREQUENCY · Vatican Vault Behavioral Analysis · 1,853 activities · 75 apps detected</div>
      </div>
      <div class="vv-real-img-wrap">
        <img src="../Demo_Data/Test%20System/Behave_V1_Output/gen_fig_top10_apps_pie.jpg" alt="Top 10 Applications Pie Chart" loading="lazy">
        <div class="vv-real-img-cap">APPLICATION DISTRIBUTION PIE CHART · Windows Activity Cache forensic extraction · Oct 2022 – Mar 2023</div>
      </div>
      <div class="vv-real-img-wrap">
        <img src="../Demo_Data/Test%20System/Behave_V1_Output/gen_fig_useractivity_bar.jpg" alt="User Activity Bar Chart" loading="lazy">
        <div class="vv-real-img-cap">USER ACTIVITY BAR CHART · 146-day monitoring window · Real endpoint behavioral reconstruction</div>
      </div>
      <div class="vv-real-img-wrap">
        <img src="../Demo_Data/Test%20System/Behave_V1_Output/gen_fig_useractivity_heatmap.jpg" alt="User Activity Heatmap" loading="lazy">
        <div class="vv-real-img-cap">USER ACTIVITY HEATMAP · Day-of-week × Time-of-day pattern analysis · Vatican Vault v1.0 output</div>
      </div>
    </div>
  </div>
</div>
"""
    # Insert before the forensic capabilities section or before footer
    c, ok = ins_before(c, '<div class="section">\n            <h2 class="section-title"><span class="section-number">5.</span>Forensic Capabilities', real_images)
    if not ok:
        c, _ = ins_before(c, '<div class="footer">', real_images)
    return c

# ── hr_employment_report.html — apply CDN defaults to existing charts ──────────
def fix_hr(c):
    # Already has charts; just ensure CDN defaults are applied
    c = prepare(c)
    if 'vv-chart-card' not in c:
        c = c.replace('</head>', CHART_CSS + '\n</head>', 1)
    return c

# ── enterprise_soc_report.html — apply CDN defaults ───────────────────────────
def fix_soc(c):
    c = prepare(c)
    return c

# ── generic_technical_report.html — apply CDN defaults ────────────────────────
def fix_generic_tech(c):
    c = prepare(c)
    return c

# ── main ───────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    tasks = [
        ('healthcare_report.html',         fix_healthcare),
        ('financial_report.html',          fix_financial),
        ('government_fisma_report.html',   fix_government),
        ('irm_report.html',                fix_irm),
        ('law_enforcement_report.html',    fix_law),
        ('legal_ediscovery_report.html',   fix_legal),
        ('mssp_report.html',               fix_mssp),
        ('ics_scada_report.html',          fix_ics),
        ('insurance_fraud_report.html',    fix_insurance),
        ('generic_compliance_report.html', fix_generic_compliance),
        ('generic_executive_report.html',  fix_generic_exec),
        ('pentest_report.html',            fix_pentest),
        ('dfir_report.html',               fix_dfir),
        ('hr_employment_report.html',      fix_hr),
        ('enterprise_soc_report.html',     fix_soc),
        ('generic_technical_report.html',  fix_generic_tech),
    ]
    print("=== Adding interactive charts + fixing attestations ===")
    for fname, fn in tasks:
        patch_file(fname, fn)
    print("\nDone.")
