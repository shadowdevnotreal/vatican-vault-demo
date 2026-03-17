# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repository Is

This is the **Vatican Vault demo/investor package** — a standalone promotional and demonstration bundle for Vatican Vault, an AI-powered Windows forensic analysis platform. It contains pre-generated HTML reports, VC investor materials, demo scripts, and sample data. It is NOT the main application codebase (which lives separately).

## Viewing the Demo

HTML files must be served over HTTP (not opened as `file://`) due to browser CORS restrictions:

```bash
# Start local server (from repo root)
python -m http.server 8000
# Then open: http://localhost:8000/
```

On Windows: double-click `START_DEMO_SERVER.bat` — it starts the server and opens the browser automatically.

Key URLs once the server is running:
- `http://localhost:8000/` — Main demo hub
- `http://localhost:8000/VC_Materials/VC_DEMO_PACKAGE.html` — Full investor package
- `http://localhost:8000/Industry_Demo_Reports/index.html` — 12 industry reports

## Tests

The demo test suite in `Demo_Tests/` is a showcase test suite (demonstrates test reporting, not business logic):

```bash
# Run from repo root
pytest Demo_Tests/ -v

# Run a single test
pytest Demo_Tests/test_demo.py::TestBasicFunctionality::test_addition -v
```

## Converting Markdown to HTML

When `.md` files are updated, regenerate their HTML counterparts:

```bash
python convert_md_to_html.py
```

This requires the `markdown` Python package (`pip install markdown`).

## Demo Scripts

`Demo_Scripts/demo.py` and `Demo_Scripts/entity_extraction_demo.py` import from the main Vatican Vault backend (`backend.app.core.*`). These scripts only run when the main Vatican Vault application is installed and on the Python path — they are not self-contained.

## Repository Structure

```
├── VC_Materials/           # Investor documents (HTML)
├── Industry_Demo_Reports/  # 12 industry-specific forensic reports (HTML)
├── Articles/               # Narrative pitch and history documents (HTML)
├── Demo_Data/              # Sample Windows Timeline DB and outputs
├── Demo_Scripts/           # Python demo scripts (require main Vatican Vault backend)
├── Demo_Tests/             # Showcase pytest suite for reporting demos
├── Sample_Outputs/         # Pre-generated test reports and coverage HTML
├── convert_md_to_html.py   # Converts .md files to styled HTML
└── START_DEMO_SERVER.bat   # Windows shortcut to start HTTP server
```

## GitHub Actions

Two Claude-powered workflows are active:
- **`claude.yml`** — Responds to `@claude` mentions in issues/PRs
- **`claude-code-review.yml`** — Automatically reviews PRs using Claude
