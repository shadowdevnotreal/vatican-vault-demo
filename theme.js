/* Vatican Vault — Site-wide Light/Dark Theme Toggle v2
   Include with: <script src="/theme.js"></script> or <script src="../theme.js"></script> */
(function () {
  var KEY = 'vv-theme';
  var LIGHT = 'vv-light';
  var html = document.documentElement;

  /* ── Inject CSS ──────────────────────────────────────────────────────── */
  var css = `
html.vv-light { --bg:#f2f5f9; --surface:#ffffff; --border:#d1d8e0; --text:#1a202c; --text-muted:#64748b; --text-dim:#64748b; --text-mid:#374151; }
html.vv-light body { background:#f2f5f9 !important; color:#1a202c !important; }
html.vv-light .vv-nav { background:rgba(242,245,249,0.97) !important; border-bottom-color:#d1d8e0 !important; }
html.vv-light .vv-nav a { color:#475569 !important; }
html.vv-light .vv-nav a:hover { color:var(--accent,#0d6efd) !important; }
html.vv-light .vv-nav .logo { color:var(--accent,#0d6efd) !important; }
html.vv-light .report-header,html.vv-light header.report-header { background:linear-gradient(135deg,#e2e8f2 0%,#f2f5f9 100%) !important; border-bottom-color:#d1d8e0 !important; }
html.vv-light .report-header::before { opacity:0.3 !important; }
html.vv-light .vv-chart-card { background:#ffffff !important; border-color:#d1d8e0 !important; }
html.vv-light .vv-chart-lbl { color:#475569 !important; border-bottom-color:#d1d8e0 !important; }
html.vv-light .vv-chart-foot { color:#64748b !important; }
html.vv-light .stat-card { background:#ffffff !important; border-color:#d1d8e0 !important; }
html.vv-light .stat-card .lbl { color:#64748b !important; }
html.vv-light .meta-item { background:#ffffff !important; border-color:#d1d8e0 !important; }
html.vv-light .meta-label { color:#64748b !important; }
html.vv-light .toc { background:#ffffff !important; border-color:#d1d8e0 !important; }
html.vv-light .toc h3 { color:#64748b !important; }
html.vv-light .footer { background:#e8edf5 !important; border-color:#d1d8e0 !important; color:#475569 !important; }
html.vv-light .section-title { color:#1a202c !important; border-bottom-color:#d1d8e0 !important; }
html.vv-light p { color:#374151 !important; }
html.vv-light li { color:#374151 !important; }
html.vv-light h1,html.vv-light h2,html.vv-light h3,html.vv-light h4 { color:#1a202c !important; }
html.vv-light table { border-color:#d1d8e0 !important; }
html.vv-light thead tr { background:rgba(0,0,0,0.04) !important; }
html.vv-light th { color:#374151 !important; border-bottom-color:#d1d8e0 !important; }
html.vv-light td { border-bottom-color:rgba(209,216,224,0.6) !important; }
html.vv-light .vv-sig-block { background:#f9fafb !important; border-color:#d1d8e0 !important; }
html.vv-light .vv-sig-text { background:#ffffff !important; border-color:#d1d8e0 !important; color:#1a202c !important; }
html.vv-light .vv-sig-field-label { color:#64748b !important; }
html.vv-light .vv-filter-btn { background:#ffffff !important; border-color:#d1d8e0 !important; color:#374151 !important; }
html.vv-light .vv-filter-btn.active,html.vv-light .vv-filter-btn:hover { border-color:var(--accent,#0d6efd) !important; color:var(--accent,#0d6efd) !important; }
html.vv-light .finding { border-color:#d1d8e0 !important; background:rgba(0,0,0,0.02) !important; }
html.vv-light .finding h3 { color:#1a202c !important; }
html.vv-light .attestation { border-color:#d1d8e0 !important; background:#ffffff !important; }
html.vv-light .risk-bar-track { background:rgba(0,0,0,0.08) !important; }
html.vv-light strong { color:#1a202c !important; }
html.vv-light .section-number { color:var(--accent,#0d6efd) !important; }
html.vv-light .vv-collapsible > h2 { background:rgba(0,0,0,0.03) !important; }
html.vv-light .vv-collapsible > h2:hover { background:rgba(0,0,0,0.06) !important; }
html.vv-light .evidence-chain,html.vv-light .timeline-section { background:#ffffff !important; border-color:#d1d8e0 !important; }
/* ── Theme toggle button ── */
#vv-theme-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 5px 12px;
  background: rgba(0,212,255,0.10);
  border: 1px solid var(--accent, #00d4ff);
  color: var(--accent, #00d4ff);
  border-radius: 3px;
  font-family: 'Share Tech Mono', 'Courier New', monospace;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.1em;
  cursor: pointer;
  transition: background 0.2s, opacity 0.2s;
  text-transform: uppercase;
  white-space: nowrap;
  line-height: 1.4;
}
#vv-theme-btn:hover { background: rgba(0,212,255,0.2); }
html.vv-light #vv-theme-btn {
  background: rgba(13,110,253,0.08);
  border-color: var(--accent, #0d6efd);
  color: var(--accent, #0d6efd);
}
html.vv-light #vv-theme-btn:hover { background: rgba(13,110,253,0.15); }
/* Fallback: if nav not found, float it at top-right */
#vv-theme-btn.vv-theme-floating {
  position: fixed;
  top: 12px;
  right: 20px;
  z-index: 10000;
  padding: 7px 14px;
  font-size: 12px;
  box-shadow: 0 2px 12px rgba(0,212,255,0.25);
}
html.vv-light #vv-theme-btn.vv-theme-floating { box-shadow: 0 2px 12px rgba(13,110,253,0.18); }
@media print { #vv-theme-btn { display:none !important; } }
`;
  var styleEl = document.createElement('style');
  styleEl.id = 'vv-theme-styles';
  styleEl.textContent = css;
  (document.head || document.documentElement).appendChild(styleEl);

  /* ── Apply saved preference before first paint ───────────────────────── */
  if (localStorage.getItem(KEY) === 'light') {
    html.classList.add(LIGHT);
  }

  /* ── Create button ───────────────────────────────────────────────────── */
  function buildBtn() {
    if (document.getElementById('vv-theme-btn')) return;
    var isLight = html.classList.contains(LIGHT);

    var btn = document.createElement('button');
    btn.id = 'vv-theme-btn';
    btn.setAttribute('aria-label', 'Toggle light/dark mode');
    btn.innerHTML = isLight
      ? '<span style="font-size:14px">☀</span> LIGHT MODE'
      : '<span style="font-size:14px">◑</span> DARK MODE';
    btn.title = 'Toggle light / dark mode';

    btn.onclick = function () {
      var nowLight = html.classList.toggle(LIGHT);
      localStorage.setItem(KEY, nowLight ? 'light' : 'dark');
      btn.innerHTML = nowLight
        ? '<span style="font-size:14px">☀</span> LIGHT MODE'
        : '<span style="font-size:14px">◑</span> DARK MODE';
    };

    /* Try to inject into .vv-nav */
    var nav = document.querySelector('.vv-nav');
    if (nav) {
      /* Push to the far right of the nav */
      btn.style.marginLeft = 'auto';
      /* If logo already has margin-right:auto, we need a wrapper span */
      var logo = nav.querySelector('.logo');
      if (logo && logo.style.marginRight === 'auto') {
        logo.style.marginRight = '';
        btn.style.marginLeft = 'auto';
      }
      nav.appendChild(btn);
    } else {
      /* No nav — float it at top-right */
      btn.classList.add('vv-theme-floating');
      document.body.appendChild(btn);
    }
  }

  if (document.body) {
    buildBtn();
  } else {
    document.addEventListener('DOMContentLoaded', buildBtn);
  }
})();
