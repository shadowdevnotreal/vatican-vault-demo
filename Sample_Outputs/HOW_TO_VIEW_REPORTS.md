# How to View Test Reports

## Quick Start

After downloading and extracting the repository, you have several options to view the HTML reports:

### Option 1: Use Python's Built-in HTTP Server (Recommended)

```bash
cd vatican_vault-main/Promo/Sample_Outputs
python -m http.server 8000
```

Then open your browser and navigate to:
- Main Report: `http://localhost:8000/reports/20260228_034136/index.html`
- Coverage Report: `http://localhost:8000/reports/20260228_034136/coverage_html/index.html`
- Pytest Report: `http://localhost:8000/reports/20260228_034136/pytest_report.html`

### Option 2: Use the Latest Symlink

The `latest` directory is a symbolic link pointing to the most recent test report:

```bash
cd vatican_vault-main/Promo/Sample_Outputs
python -m http.server 8000
```

Then navigate to: `http://localhost:8000/latest/index.html`

### Option 3: Direct File Access (Limited)

You can try opening the HTML files directly in your browser, but some features may not work due to browser security restrictions with the `file://` protocol:

- `file:///path/to/vatican_vault-main/Promo/Sample_Outputs/reports/20260228_034136/index.html`

**Note:** Coverage reports require external CSS/JS files and will appear blank when opened via `file://` protocol. Use Option 1 or 2 instead.

## Available Reports

### 1. Main Test Report (`index.html`)
- Overview of test results
- Test suite breakdown
- Pass/fail statistics
- Links to detailed reports

### 2. Coverage Report (`coverage_html/index.html`)
- Code coverage metrics
- Line-by-line coverage analysis
- Function and class coverage

### 3. Pytest HTML Report (`pytest_report.html`)
- Detailed pytest output
- Test execution details
- Error traces and logs

### 4. Demo Report
View the investor-focused demo report at:
`Promo/VC_Materials/VC_DEMO_REPORT_2026-02-28.html`

## Troubleshooting

### Blank Pages When Opening HTML Files

**Problem:** HTML files show blank screens when opened directly.

**Solution:** Use a local HTTP server (see Option 1 above). Browser security prevents some features from working with `file://` URLs.

### Symlink Issues on Windows

**Problem:** "Dangerous link path was ignored" error when extracting on Windows.

**Solution:**
1. Extract the ZIP file normally
2. Navigate to `Promo/Sample_Outputs/reports/20260228_034136/`
3. Use a local HTTP server as described in Option 1

Alternatively, on Windows you can use:
```cmd
cd vatican_vault-main\Promo\Sample_Outputs
python -m http.server 8000
```

### JavaScript Errors

**Problem:** Console shows CORS or module loading errors.

**Solution:** Always use a local HTTP server for viewing reports. Never open HTML files directly via `file://` protocol.

## Directory Structure

```
Promo/Sample_Outputs/
├── latest → reports/20260228_034136  (symlink)
├── reports/
│   ├── 20260228_034136/
│   │   ├── index.html              (Main report)
│   │   ├── pytest_report.html      (Pytest details)
│   │   ├── coverage_html/
│   │   │   └── index.html          (Coverage report)
│   │   ├── coverage.json
│   │   └── junit.xml
│   └── index.html                   (Reports index)
└── TEST_REPORTS_README.md
```

## Need Help?

If you encounter any issues viewing the reports, please ensure:
1. Python 3.x is installed
2. You're running the HTTP server from the correct directory
3. Port 8000 is not already in use (or use a different port: `python -m http.server 8001`)
