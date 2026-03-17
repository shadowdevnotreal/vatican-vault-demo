@echo off
REM Vatican Vault - Demo Report Server Launcher
REM This script starts a local HTTP server to view HTML reports properly

echo ========================================
echo Vatican Vault - Demo Server Launcher
echo ========================================
echo.
echo Checking Python installation...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Python is not installed or not in PATH!
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

echo Python found! Starting local HTTP server on port 8000...
echo.

REM Ensure we serve from the Promo directory (where this bat file lives)
cd /d "%~dp0"

echo ========================================
echo Server Starting...
echo ========================================
echo.
echo Serving from: %CD%
echo.
echo Your browser will open automatically to:
echo http://localhost:8000/
echo.
echo Available Pages:
echo   - Main Demo Hub:  http://localhost:8000/
echo   - Demo Package:   http://localhost:8000/VC_Materials/VC_DEMO_PACKAGE.html
echo   - Test Reports:   http://localhost:8000/Sample_Outputs/reports/20260228_034136/index.html
echo   - Coverage:       http://localhost:8000/Sample_Outputs/reports/20260228_034136/coverage_html/index.html
echo   - Pytest Report:  http://localhost:8000/Sample_Outputs/reports/20260228_034136/pytest_report.html
echo.
echo Press Ctrl+C to stop the server when done.
echo ========================================
echo.

REM Open browser then start server
start "" http://localhost:8000/

REM Start Python HTTP server from Promo directory
python -m http.server 8000
