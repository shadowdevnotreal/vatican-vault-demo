/* Vatican Vault — Site-wide Light/Dark Theme Toggle
   Include with: <script src="/theme.js"></script> or <script src="../theme.js"></script>
   Adjust path depth via data-depth attribute: <script src="../theme.js" data-depth="1"></script> */
(function () {
  var KEY = 'vv-theme';
  var LIGHT = 'vv-light';
  var html = document.documentElement;

  /* ── Inject light-theme CSS ─────────────────────────────────────────── */
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
/* Theme toggle button */
#vv-theme-btn { position:fixed; bottom:28px; right:240px; z-index:9999; background:rgba(255,255,255,0.08); border:1px solid var(--accent,#00d4ff); color:var(--accent,#00d4ff); padding:9px 13px; font-size:15px; cursor:pointer; border-radius:3px; opacity:0.85; transition:opacity 0.2s,background 0.2s; font-family:monospace; line-height:1; }
#vv-theme-btn:hover { opacity:1; background:rgba(0,212,255,0.08); }
html.vv-light #vv-theme-btn { background:rgba(0,0,0,0.06); border-color:var(--accent,#0d6efd); color:var(--accent,#0d6efd); }
@media print { #vv-theme-btn { display:none !important; } }
`;
  var styleEl = document.createElement('style');
  styleEl.id = 'vv-theme-styles';
  styleEl.textContent = css;
  (document.head || document.documentElement).appendChild(styleEl);

  /* ── Apply saved preference immediately (before render) ─────────────── */
  if (localStorage.getItem(KEY) === 'light') {
    html.classList.add(LIGHT);
  }

  /* ── Create toggle button ────────────────────────────────────────────── */
  function buildBtn() {
    if (document.getElementById('vv-theme-btn')) return;
    var btn = document.createElement('button');
    btn.id = 'vv-theme-btn';
    btn.title = 'Toggle light / dark mode';
    btn.setAttribute('aria-label', 'Toggle light/dark mode');
    btn.textContent = html.classList.contains(LIGHT) ? '☀' : '◑';
    btn.onclick = function () {
      var isLight = html.classList.toggle(LIGHT);
      localStorage.setItem(KEY, isLight ? 'light' : 'dark');
      btn.textContent = isLight ? '☀' : '◑';
    };
    document.body.appendChild(btn);
  }

  if (document.body) {
    buildBtn();
  } else {
    document.addEventListener('DOMContentLoaded', buildBtn);
  }
})();
