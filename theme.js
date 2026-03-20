/* Vatican Vault — Site-wide Light/Dark Theme Toggle v3 */
(function () {
  var KEY   = 'vv-theme';
  var LIGHT = 'vv-light';
  var html  = document.documentElement;

  /* ── CSS ─────────────────────────────────────────────────────────────── */
  var css = `
/* ── Dark mode nav — high-visibility buttons ── */
.nav-links a { color: #e2e8f0 !important; border-color: rgba(0,212,255,0.50) !important; background: rgba(0,212,255,0.06) !important; }
.nav-links a:hover, .nav-links a.active { color: #00d4ff !important; border-color: #00d4ff !important; background: rgba(0,212,255,0.14) !important; box-shadow: 0 0 12px rgba(0,212,255,0.2) !important; }
.vv-nav-links a { color: #e2e8f0 !important; border-color: rgba(0,212,255,0.50) !important; background: rgba(0,212,255,0.06) !important; }
.vv-nav-links a:hover { color: #00d4ff !important; border-color: #00d4ff !important; background: rgba(0,212,255,0.14) !important; box-shadow: 0 0 12px rgba(0,212,255,0.2) !important; }
.vv-nav-back { color: #00d4ff !important; border-color: rgba(0,212,255,0.50) !important; }
#vv-theme-btn { border-color: #00d4ff !important; }

html.vv-light { --bg:#f2f5f9; --surface:#ffffff; --border:#c8d3e0; --text:#0f172a; --text-muted:#0f172a; --text-dim:#0f172a; --text-mid:#0f172a; }
html.vv-light body { background:#f2f5f9 !important; color:#0f172a !important; }
html.vv-light .nav,html.vv-light .vv-nav,html.vv-light .nav-bar { background:rgba(242,245,249,0.97) !important; border-bottom-color:#c8d3e0 !important; }
html.vv-light .nav-links a { color:#0f172a !important; border-color:#475569 !important; background:rgba(15,23,42,0.04) !important; }
html.vv-light .nav-links a:hover,html.vv-light .nav-links a.active { color:#0d6efd !important; border-color:#0d6efd !important; background:rgba(13,110,253,0.10) !important; box-shadow:0 0 8px rgba(13,110,253,0.15) !important; }
html.vv-light .vv-nav a { color:#0f172a !important; }
html.vv-light .vv-nav a:hover { color:#0d6efd !important; }
html.vv-light .vv-nav-links a { color:#0f172a !important; border-color:#475569 !important; background:rgba(15,23,42,0.04) !important; }
html.vv-light .vv-nav-links a:hover { color:#0d6efd !important; border-color:#0d6efd !important; background:rgba(13,110,253,0.10) !important; box-shadow:0 0 8px rgba(13,110,253,0.15) !important; }
html.vv-light .vv-nav-back { color:#1d4ed8 !important; border-color:#1d4ed8 !important; }
html.vv-light #vv-theme-btn { border-color:#0d6efd !important; }
html.vv-light .vv-nav .logo { color:var(--accent,#0d6efd) !important; }
html.vv-light .nav-logo { color:var(--accent,#00d4ff) !important; }
html.vv-light .report-header,html.vv-light header.report-header { background:linear-gradient(135deg,#e2e8f2 0%,#f2f5f9 100%) !important; border-bottom-color:#c8d3e0 !important; }
html.vv-light .report-header::before { opacity:0.3 !important; }
html.vv-light .vv-chart-card { background:#ffffff !important; border-color:#c8d3e0 !important; }
html.vv-light .vv-chart-lbl { color:#0f172a !important; border-bottom-color:#c8d3e0 !important; }
html.vv-light .vv-chart-foot { color:#0f172a !important; }
html.vv-light .stat-card { background:#ffffff !important; border-color:#c8d3e0 !important; }
html.vv-light .stat-card .lbl { color:#0f172a !important; }
html.vv-light .meta-item { background:#ffffff !important; border-color:#c8d3e0 !important; }
html.vv-light .meta-label { color:#0f172a !important; }
html.vv-light .toc { background:#ffffff !important; border-color:#c8d3e0 !important; }
html.vv-light .toc h3 { color:#0f172a !important; }
html.vv-light .footer { background:#e2e8f0 !important; border-color:#c8d3e0 !important; color:#0f172a !important; }
html.vv-light .section-title { color:#0f172a !important; border-bottom-color:#c8d3e0 !important; }
html.vv-light p { color:#0f172a !important; }
html.vv-light li { color:#0f172a !important; }
html.vv-light h1,html.vv-light h2,html.vv-light h3,html.vv-light h4 { color:#0f172a !important; }
html.vv-light table { border-color:#c8d3e0 !important; }
html.vv-light thead tr { background:rgba(0,0,0,0.05) !important; }
html.vv-light th { color:#0f172a !important; border-bottom-color:#c8d3e0 !important; }
html.vv-light td { border-bottom-color:rgba(200,211,224,0.7) !important; }
html.vv-light .vv-sig-block { background:#f1f5f9 !important; border-color:#c8d3e0 !important; }
html.vv-light .vv-sig-text { background:#ffffff !important; border-color:#c8d3e0 !important; color:#0f172a !important; }
html.vv-light .vv-sig-field-label { color:#0f172a !important; }
html.vv-light .vv-filter-btn { background:#ffffff !important; border-color:#c8d3e0 !important; color:#0f172a !important; }
html.vv-light .vv-filter-btn.active,html.vv-light .vv-filter-btn:hover { border-color:var(--accent,#0d6efd) !important; color:var(--accent,#0d6efd) !important; }
html.vv-light .finding { border-color:#c8d3e0 !important; background:rgba(0,0,0,0.02) !important; }
html.vv-light .finding h3 { color:#0f172a !important; }
html.vv-light .attestation { border-color:#c8d3e0 !important; background:#ffffff !important; }
html.vv-light .risk-bar-track { background:rgba(0,0,0,0.1) !important; }
html.vv-light strong { color:#0f172a !important; }
html.vv-light .section-number { color:var(--accent,#0d6efd) !important; }
html.vv-light .card { background:rgba(0,0,0,0.02) !important; border-color:#c8d3e0 !important; }
html.vv-light .evidence-chain,html.vv-light .timeline-section,html.vv-light .methodology { background:#f1f5f9 !important; border-color:#c8d3e0 !important; }
html.vv-light .evidence-chain h4 { color:#7c2d12 !important; }
html.vv-light .timeline-section h4 { color:#1e3a8a !important; }
html.vv-light .methodology { background:#eff6ff !important; border-color:#2563eb !important; }
html.vv-light .hero-tagline { color:#0f172a !important; }
html.vv-light .hero-sub { color:#0f172a !important; }
html.vv-light .stat-label { color:#0f172a !important; }
html.vv-light .section-note { color:#0f172a !important; }
html.vv-light .card p { color:#0f172a !important; }
html.vv-light .card-arrow { color:#0f172a !important; }
html.vv-light .badge-dim { color:#0f172a !important; background:rgba(30,41,59,0.08) !important; border-color:rgba(30,41,59,0.2) !important; }
html.vv-light .footer-meta { color:#0f172a !important; }
html.vv-light .btn-primary { color:#ffffff !important; background:#0d6efd !important; }
html.vv-light .btn-primary:hover { box-shadow:0 0 24px rgba(13,110,253,0.35) !important; }
html.vv-light .btn-outline { color:#0d6efd !important; border-color:#0d6efd !important; }
html.vv-light .btn-outline:hover { background:rgba(13,110,253,0.07) !important; }
html.vv-light tr:hover td { background:rgba(0,0,0,0.03) !important; }
html.vv-light pre { background:#f1f5f9 !important; border-color:#c8d3e0 !important; color:#0f172a !important; }
html.vv-light pre code { color:#0f172a !important; }
html.vv-light code { background:rgba(13,110,253,0.07) !important; color:#0d6efd !important; border-color:rgba(13,110,253,0.2) !important; }
html.vv-light .info-box { background:rgba(13,110,253,0.06) !important; border-color:#2563eb !important; color:#0f172a !important; }
html.vv-light .warning-box { background:rgba(245,158,11,0.08) !important; border-color:#d97706 !important; color:#0f172a !important; }
html.vv-light .success-box { background:rgba(16,185,129,0.08) !important; border-color:#059669 !important; color:#0f172a !important; }
html.vv-light .vv-real-img-wrap { background:#e2e8f0 !important; }
html.vv-light blockquote { background:rgba(13,110,253,0.04) !important; color:#0f172a !important; border-left-color:#0d6efd !important; }
html.vv-light .phi-badge { background:rgba(220,38,38,0.08) !important; color:#991b1b !important; }
html.vv-light .compliance-badge { background:rgba(5,150,105,0.08) !important; color:#065f46 !important; }
html.vv-light .methodology { color:#0f172a !important; }
html.vv-light .callout-evidence .callout-title { color:#9a3412 !important; }
html.vv-light .callout-info .callout-title { color:#1e40af !important; }
html.vv-light .nav-logo { color:#0d6efd !important; }

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
  border-color: #0d6efd;
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
