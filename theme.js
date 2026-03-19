/* Vatican Vault — Site-wide Light/Dark Theme Toggle v3 */
(function () {
  var KEY   = 'vv-theme';
  var LIGHT = 'vv-light';
  var html  = document.documentElement;

  /* ── CSS ─────────────────────────────────────────────────────────────── */
  var css = `
html.vv-light { --bg:#f2f5f9; --surface:#ffffff; --border:#d1d8e0; --text:#1a202c; --text-muted:#374151; --text-dim:#374151; --text-mid:#1a202c; }
html.vv-light body { background:#f2f5f9 !important; color:#1a202c !important; }
html.vv-light .nav,html.vv-light .vv-nav { background:rgba(242,245,249,0.97) !important; border-bottom-color:#d1d8e0 !important; }
html.vv-light .nav-links a { color:#374151 !important; }
html.vv-light .nav-links a:hover,html.vv-light .nav-links a.active { color:var(--accent,#0d6efd) !important; background:rgba(13,110,253,0.06) !important; border-color:#d1d8e0 !important; }
html.vv-light .vv-nav a { color:#374151 !important; }
html.vv-light .vv-nav a:hover { color:var(--accent,#0d6efd) !important; }
html.vv-light .vv-nav .logo { color:var(--accent,#0d6efd) !important; }
html.vv-light .nav-logo { color:var(--accent,#00d4ff) !important; }
html.vv-light .report-header,html.vv-light header.report-header { background:linear-gradient(135deg,#e2e8f2 0%,#f2f5f9 100%) !important; border-bottom-color:#d1d8e0 !important; }
html.vv-light .report-header::before { opacity:0.3 !important; }
html.vv-light .vv-chart-card { background:#ffffff !important; border-color:#d1d8e0 !important; }
html.vv-light .vv-chart-lbl { color:#374151 !important; border-bottom-color:#d1d8e0 !important; }
html.vv-light .vv-chart-foot { color:#374151 !important; }
html.vv-light .stat-card { background:#ffffff !important; border-color:#d1d8e0 !important; }
html.vv-light .stat-card .lbl { color:#374151 !important; }
html.vv-light .meta-item { background:#ffffff !important; border-color:#d1d8e0 !important; }
html.vv-light .meta-label { color:#374151 !important; }
html.vv-light .toc { background:#ffffff !important; border-color:#d1d8e0 !important; }
html.vv-light .toc h3 { color:#374151 !important; }
html.vv-light .footer { background:#e8edf5 !important; border-color:#d1d8e0 !important; color:#374151 !important; }
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
html.vv-light .vv-sig-field-label { color:#374151 !important; }
html.vv-light .vv-filter-btn { background:#ffffff !important; border-color:#d1d8e0 !important; color:#374151 !important; }
html.vv-light .vv-filter-btn.active,html.vv-light .vv-filter-btn:hover { border-color:var(--accent,#0d6efd) !important; color:var(--accent,#0d6efd) !important; }
html.vv-light .finding { border-color:#d1d8e0 !important; background:rgba(0,0,0,0.02) !important; }
html.vv-light .finding h3 { color:#1a202c !important; }
html.vv-light .attestation { border-color:#d1d8e0 !important; background:#ffffff !important; }
html.vv-light .risk-bar-track { background:rgba(0,0,0,0.08) !important; }
html.vv-light strong { color:#1a202c !important; }
html.vv-light .section-number { color:var(--accent,#0d6efd) !important; }
html.vv-light .card { background:rgba(0,0,0,0.03) !important; border-color:#d1d8e0 !important; }
html.vv-light .evidence-chain,html.vv-light .timeline-section,html.vv-light .methodology { background:#f8fafc !important; border-color:#d1d8e0 !important; }
html.vv-light .evidence-chain h4 { color:#92400e !important; }
html.vv-light .timeline-section h4 { color:#1e40af !important; }
html.vv-light .methodology { background:#f0f9ff !important; border-color:#3b82f6 !important; }
html.vv-light .hero-tagline { color:#374151 !important; }
html.vv-light .hero-sub { color:#374151 !important; }
html.vv-light .stat-label { color:#374151 !important; }
html.vv-light .section-note { color:#374151 !important; }
html.vv-light .card p { color:#374151 !important; }
html.vv-light .card-arrow { color:#374151 !important; }
html.vv-light .badge-dim { color:#374151 !important; background:rgba(55,65,81,0.1) !important; border-color:rgba(55,65,81,0.25) !important; }
html.vv-light .footer-meta { color:#4b5563 !important; }

/* ── Theme toggle button base style ── */
#vv-theme-btn {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  padding: 5px 13px;
  background: rgba(0,212,255,0.08);
  border: 1px solid rgba(0,212,255,0.55);
  color: #00d4ff;
  border-radius: 3px;
  font-family: 'Share Tech Mono', 'Courier New', monospace;
  font-size: 0.68em;
  font-weight: 700;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  cursor: pointer;
  white-space: nowrap;
  line-height: 1.5;
  transition: background 0.2s, border-color 0.2s;
  flex-shrink: 0;
}
#vv-theme-btn:hover { background: rgba(0,212,255,0.18); }
html.vv-light #vv-theme-btn {
  background: rgba(13,110,253,0.07);
  border-color: rgba(13,110,253,0.45);
  color: #0d6efd;
}
html.vv-light #vv-theme-btn:hover { background: rgba(13,110,253,0.14); }
@media print { #vv-theme-btn { display:none !important; } }
`;
  var styleEl = document.createElement('style');
  styleEl.id = 'vv-theme-styles';
  styleEl.textContent = css;
  (document.head || document.documentElement).appendChild(styleEl);

  /* ── Apply saved theme before first paint ────────────────────────────── */
  if (localStorage.getItem(KEY) === 'light') html.classList.add(LIGHT);

  /* ── Build button ────────────────────────────────────────────────────── */
  function buildBtn() {
    if (document.getElementById('vv-theme-btn')) return;
    var isLight = html.classList.contains(LIGHT);

    var btn = document.createElement('button');
    btn.id = 'vv-theme-btn';
    btn.setAttribute('aria-label', 'Toggle light/dark mode');
    btn.innerHTML = isLight
      ? '<span style="font-size:13px;line-height:1">☀</span> Light'
      : '<span style="font-size:13px;line-height:1">◑</span> Dark';

    btn.onclick = function () {
      var nowLight = html.classList.toggle(LIGHT);
      localStorage.setItem(KEY, nowLight ? 'light' : 'dark');
      btn.innerHTML = nowLight
        ? '<span style="font-size:13px;line-height:1">☀</span> Light'
        : '<span style="font-size:13px;line-height:1">◑</span> Dark';
    };

    /* ── Try to inject into nav ─────────────────────────────────────────
       Priority order:
       1. .nav-links  (index.html style — append as last link)
       2. .vv-nav     (report pages  — append at far right)
       3. Floating fallback at top-right
    ──────────────────────────────────────────────────────────────────── */
    var navLinks = document.querySelector('.nav-links');
    var vvNav    = document.querySelector('.vv-nav');

    if (navLinks) {
      /* Separate the button slightly from the nav links */
      btn.style.marginLeft = '12px';
      navLinks.appendChild(btn);
    } else if (vvNav) {
      /* Push to far right — logo already has margin-right:auto */
      vvNav.appendChild(btn);
    } else {
      /* Fallback: fixed top-right, well clear of any nav */
      btn.style.cssText = [
        'position:fixed', 'top:12px', 'right:20px', 'z-index:10000',
        'padding:6px 14px', 'font-size:11px',
        'box-shadow:0 2px 12px rgba(0,212,255,0.25)'
      ].join(';');
      document.body.appendChild(btn);
    }
  }

  if (document.body) buildBtn();
  else document.addEventListener('DOMContentLoaded', buildBtn);
})();
