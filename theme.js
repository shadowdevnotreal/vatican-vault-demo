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

/* ── Light mode: fix inline hardcoded colors across reports ── */
html.vv-light [style*="background:#1a1a1a"] { background:#f1f5f9 !important; border-color:#059669 !important; }
html.vv-light [style*="background:#ecfdf5"] { background:#e0f2fe !important; }
html.vv-light [style*="color:#0f0"] { color:#047857 !important; }
html.vv-light [style*="color:#ff6b6b"] { color:#dc2626 !important; }
html.vv-light [style*="color:#fff"] { color:#0f172a !important; }
html.vv-light [style*="background:rgba(255,255,255,0.04)"] { background:rgba(0,0,0,0.02) !important; }
html.vv-light [style*="color:var(--green,#0f0)"] { color:#047857 !important; }
html.vv-light [style*="color:var(--text-muted,#8899aa)"] { color:#475569 !important; }

/* ── Enhanced print stylesheet (all pages) ── */
@media print {
  @page { margin: 18mm 15mm 18mm 15mm; }
  body { background: #fff !important; color: #111 !important; font-size: 11pt !important; line-height: 1.5 !important; }
  .vv-nav, .nav, .nav-bar, #vv-print-btn, #vv-top-btn, #vv-theme-btn, .vv-lock-btn, .vv-sig-unlock-btn { display: none !important; }
  .vv-collapsed .section-body { display: block !important; }
  .section, .finding, .attestation, .vv-sig-block { break-inside: avoid; }
  table { break-inside: avoid; }
  h2, h3 { break-after: avoid; }
  .report-header, header.report-header { break-after: avoid; }
  .footer, .report-footer { break-before: avoid; page-break-before: avoid; }
  .vv-chart-c canvas { max-width: 100% !important; }
  .vv-sig-text { border-bottom: 1px solid rgba(0,0,0,0.3) !important; background: transparent !important; }
  .vv-date-input { border-bottom: 1px solid rgba(0,0,0,0.3) !important; background: transparent !important; }
  .stat-card, .meta-item, .card { border-color: #ccc !important; }
  a { color: #111 !important; text-decoration: underline !important; }
  pre, code { background: #f5f5f5 !important; border-color: #ccc !important; }
  * { box-shadow: none !important; text-shadow: none !important; }
}

/* ── LIVE data pulse indicator ── */
.vv-live-badge {
  display: inline-flex; align-items: center; gap: 6px;
  font-family: 'Share Tech Mono', monospace; font-size: 10px;
  letter-spacing: 1.5px; text-transform: uppercase;
  color: #10b981; opacity: 0.85;
}
.vv-live-dot {
  width: 7px; height: 7px; border-radius: 50%;
  background: #10b981;
  animation: vvPulse 2s ease-in-out infinite;
}
@keyframes vvPulse {
  0%, 100% { opacity: 1; box-shadow: 0 0 0 0 rgba(16,185,129,0.5); }
  50% { opacity: 0.6; box-shadow: 0 0 0 5px rgba(16,185,129,0); }
}
html.vv-light .vv-live-badge { color: #059669; }
html.vv-light .vv-live-dot { background: #059669; }
@media print { .vv-live-badge { display: none !important; } }

/* ── Smooth theme transition (only after first paint) ── */
html.vv-transitions, html.vv-transitions *, html.vv-transitions *::before, html.vv-transitions *::after {
  transition: background-color 0.25s ease, color 0.25s ease, border-color 0.25s ease, box-shadow 0.25s ease !important;
}

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
      html.classList.add('vv-transitions');
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

  /* ── Accessibility: aria attributes + skip-nav ──────────────────────── */
  function a11y() {
    /* Skip-nav link */
    var main = document.querySelector('main, .page, .report-body, .main');
    if (main && !document.getElementById('vv-skip')) {
      if (!main.id) main.id = 'vv-main-content';
      var skip = document.createElement('a');
      skip.id = 'vv-skip';
      skip.href = '#' + main.id;
      skip.textContent = 'Skip to main content';
      skip.style.cssText = 'position:absolute;top:-100px;left:8px;z-index:99999;background:#04080f;color:#00d4ff;padding:8px 16px;font-size:13px;border:1px solid #00d4ff;border-radius:2px;text-decoration:none;transition:top 0.2s;';
      skip.addEventListener('focus', function(){ skip.style.top = '8px'; });
      skip.addEventListener('blur', function(){ skip.style.top = '-100px'; });
      document.body.insertBefore(skip, document.body.firstChild);
    }

    /* aria-expanded on collapsible sections */
    document.querySelectorAll('.section').forEach(function(sec) {
      var h2 = sec.querySelector('h2.section-title');
      if (!h2) return;
      var isCollapsed = sec.classList.contains('vv-collapsed');
      h2.setAttribute('role', 'button');
      h2.setAttribute('tabindex', '0');
      h2.setAttribute('aria-expanded', !isCollapsed);
      var body = sec.querySelector('.section-body');
      if (body) {
        if (!body.id) body.id = 'vv-sec-' + Math.random().toString(36).substr(2,6);
        h2.setAttribute('aria-controls', body.id);
      }
      /* Update aria on toggle — wrap existing click handler */
      h2.addEventListener('click', function() {
        setTimeout(function() {
          h2.setAttribute('aria-expanded', !sec.classList.contains('vv-collapsed'));
        }, 10);
      });
      h2.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); h2.click(); }
      });
    });

    /* Nav landmark */
    var nav = document.querySelector('.vv-nav, .nav');
    if (nav && !nav.getAttribute('role')) nav.setAttribute('role', 'navigation');
    if (nav) nav.setAttribute('aria-label', 'Main navigation');
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', function(){ setTimeout(a11y, 100); });
  else setTimeout(a11y, 100);

  /* ── Inject LIVE badge into report nav ─────────────────────────────── */
  function addLiveBadge() {
    var nav = document.querySelector('.vv-nav-links');
    if (!nav || document.querySelector('.vv-live-badge')) return;
    var badge = document.createElement('span');
    badge.className = 'vv-live-badge';
    badge.innerHTML = '<span class="vv-live-dot"></span> LIVE DATA';
    badge.style.marginLeft = '10px';
    nav.appendChild(badge);
  }
  if (document.body) addLiveBadge();
  else document.addEventListener('DOMContentLoaded', addLiveBadge);
})();
