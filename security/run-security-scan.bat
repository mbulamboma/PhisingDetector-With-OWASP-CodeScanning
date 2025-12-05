@echo off
REM OWASP Dependency Check for Flask Web App (Windows)
REM This script scans the webapp folder for known security vulnerabilities

echo 🔍 Starting OWASP Dependency Check for Phishing Detection Web App
echo ==================================================================

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running. Please start Docker Desktop first.
    pause
    exit /b 1
)

REM Get webapp directory (one level up from security folder)
set WEBAPP_DIR=%cd%\..\webapp
set SECURITY_DIR=%cd%

echo 📁 Scanning directory: %WEBAPP_DIR%
echo 📁 Reports will be saved to: %SECURITY_DIR%\security-reports
echo 📅 Scan date: %date% %time%

REM Create reports directory if it doesn't exist
if not exist "%SECURITY_DIR%\security-reports" mkdir "%SECURITY_DIR%\security-reports"

echo.
echo 🚀 Running OWASP Dependency Check...
echo This might take a few minutes on first run (downloading vulnerability database)

REM Run OWASP Dependency Check with Windows paths
docker run --rm ^
    --volume "%WEBAPP_DIR%":/src ^
    --volume "%SECURITY_DIR%\security-reports":/report ^
    owasp/dependency-check:latest ^
    --scan /src ^
    --format "ALL" ^
    --project "Phishing-Detection-WebApp" ^
    --out /report

REM Check if scan completed successfully
if %errorlevel% equ 0 (
    echo.
    echo ✅ Vulnerability scan completed successfully!
    echo.
    echo 📊 Reports generated:
    echo    - HTML Report: %SECURITY_DIR%\security-reports\dependency-check-report.html
    echo    - JSON Report: %SECURITY_DIR%\security-reports\dependency-check-report.json
    echo    - XML Report:  %SECURITY_DIR%\security-reports\dependency-check-report.xml
    echo.
    echo 💡 Opening HTML report in default browser...
    start "" "%SECURITY_DIR%\security-reports\dependency-check-report.html"
    echo.
) else (
    echo.
    echo ❌ Vulnerability scan failed. Check the output above for errors.
    pause
    exit /b 1
)

echo 🛡️  Security Scan Summary
echo =========================
echo Project: Phishing Detection Web App
echo Scan Type: Dependency vulnerability check
echo Tool: OWASP Dependency Check
echo Status: Complete
echo.
echo Next steps:
echo 1. Review the HTML report for any HIGH or CRITICAL vulnerabilities
echo 2. Update vulnerable dependencies if found
echo 3. Re-run this script after updates to verify fixes
echo 4. Consider running this regularly (weekly/monthly)
echo.
pause