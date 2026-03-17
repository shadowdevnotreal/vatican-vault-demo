# Windows Setup Instructions - Vatican Vault Demo

## Why HTML Files Won't Open Directly

When you try to open HTML files directly using `file:///C:/Users/...` paths, modern browsers block:
- External JavaScript and CSS files (CORS security policy)
- Relative links between HTML files
- Dynamic content loading

This causes **blank pages** or **broken functionality** in the demo reports.

## ✅ Solution: Use a Local HTTP Server

### Quick Start (Windows)

1. **Make sure Python is installed**
   - Open Command Prompt and type: `python --version`
   - If not installed, download from: https://www.python.org/downloads/

2. **Navigate to the Promo directory**
   ```cmd
   cd C:\Users\Mishka\vatican_vault\Promo
   ```

3. **Run the demo server**

   **Option A: Use the batch file (easiest)**
   ```cmd
   START_DEMO_SERVER.bat
   ```

   **Option B: Manual command**
   ```cmd
   python -m http.server 8000
   ```

4. **Open your browser** and navigate to:
   - **Main Demo Package**: http://localhost:8000/VC_Materials/VC_DEMO_PACKAGE.html
   - **Test Reports**: http://localhost:8000/Sample_Outputs/reports/20260228_034136/index.html
   - **Coverage Report**: http://localhost:8000/Sample_Outputs/reports/20260228_034136/coverage_html/index.html

## URLs to Use

Once the server is running, replace your `file://` URLs with these `http://localhost:8000/` URLs:

| ❌ File Protocol (Won't Work) | ✅ HTTP Server (Works!) |
|-------------------------------|-------------------------|
| `file:///C:/Users/Mishka/vatican_vault/Promo/VC_Materials/VC_DEMO_PACKAGE.html` | `http://localhost:8000/VC_Materials/VC_DEMO_PACKAGE.html` |
| `file:///C:/Users/Mishka/vatican_vault/Promo/Sample_Outputs/reports/20260228_034136/index.html` | `http://localhost:8000/Sample_Outputs/reports/20260228_034136/index.html` |
| `file:///C:/Users/Mishka/vatican_vault/Promo/Sample_Outputs/reports/20260228_034136/coverage_html/index.html` | `http://localhost:8000/Sample_Outputs/reports/20260228_034136/coverage_html/index.html` |
| `file:///C:/Users/Mishka/vatican_vault/Promo/Sample_Outputs/reports/20260228_034136/pytest_report.html` | `http://localhost:8000/Sample_Outputs/reports/20260228_034136/pytest_report.html` |

## Troubleshooting

### "Python is not recognized..."
- Install Python from https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation

### Port 8000 already in use
Use a different port:
```cmd
python -m http.server 8001
```
Then use `http://localhost:8001/...` instead

### Still seeing blank pages
1. Check browser console (F12) for errors
2. Make sure you're using `http://localhost:8000/` not `file:///`
3. Try a different browser (Chrome, Firefox, Edge)

### Symlink warnings when extracting
This is normal on Windows. The `latest` symlink might not work, but the actual reports at `reports/20260228_034136/` will work fine.

## Why This Happens

Modern web browsers enforce **CORS (Cross-Origin Resource Sharing)** security policies that prevent:
- Loading external resources from `file://` URLs
- JavaScript modules from local files
- Relative navigation between HTML files

The solution is to serve files through HTTP (even locally), which browsers trust more than direct file access.

## Alternative: Use PowerShell

If you prefer PowerShell:
```powershell
cd C:\Users\Mishka\vatican_vault\Promo
python -m http.server 8000
```

Then open: http://localhost:8000/VC_Materials/VC_DEMO_PACKAGE.html

---

**Need Help?** If you encounter any issues, ensure:
1. Python 3.x is installed
2. You're in the correct directory (`Promo` folder)
3. Port 8000 is available
4. Your firewall allows local connections
