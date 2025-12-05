# Security Vulnerability Check with OWASP Dependency Check
# PowerShell script for Windows

Write-Host "🔍 Starting OWASP Dependency Check for Phishing Detection Web App" -ForegroundColor Cyan
Write-Host "==================================================================" -ForegroundColor Cyan

# Check if Docker is running
try {
    docker info | Out-Null
    Write-Host "✅ Docker is running" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker is not running. Please start Docker Desktop first." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Get current directory (webapp folder)
$webappDir = Get-Location
$reportsDir = Join-Path $webappDir "security-reports"

Write-Host "📁 Scanning directory: $webappDir" -ForegroundColor Yellow
Write-Host "📅 Scan date: $(Get-Date)" -ForegroundColor Yellow

# Create reports directory if it doesn't exist
if (!(Test-Path $reportsDir)) {
    New-Item -ItemType Directory -Path $reportsDir -Force | Out-Null
    Write-Host "📁 Created reports directory: $reportsDir" -ForegroundColor Green
}

Write-Host ""
Write-Host "🚀 Running OWASP Dependency Check..." -ForegroundColor Cyan
Write-Host "This might take a few minutes on first run (downloading vulnerability database)" -ForegroundColor Yellow

# Convert Windows paths to Docker-compatible format
$dockerSrcPath = $webappDir.Path.Replace('\', '/').Replace('C:', '/c')
$dockerReportPath = $reportsDir.Replace('\', '/').Replace('C:', '/c')

try {
    # Run OWASP Dependency Check
    $dockerArgs = @(
        "run", "--rm",
        "--volume", "$($webappDir):/src",
        "--volume", "$reportsDir:/report",
        "owasp/dependency-check:latest",
        "--scan", "/src",
        "--format", "ALL",
        "--project", "Phishing-Detection-WebApp",
        "--out", "/report"
    )
    
    & docker @dockerArgs
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "✅ Vulnerability scan completed successfully!" -ForegroundColor Green
        Write-Host ""
        Write-Host "📊 Reports generated:" -ForegroundColor Cyan
        Write-Host "   - HTML Report: $reportsDir\dependency-check-report.html"
        Write-Host "   - JSON Report: $reportsDir\dependency-check-report.json" 
        Write-Host "   - XML Report:  $reportsDir\dependency-check-report.xml"
        Write-Host ""
        
        $htmlReport = Join-Path $reportsDir "dependency-check-report.html"
        if (Test-Path $htmlReport) {
            Write-Host "🌐 Opening HTML report in default browser..." -ForegroundColor Green
            Start-Process $htmlReport
        }
        
    } else {
        Write-Host "❌ Vulnerability scan failed. Check the output above for errors." -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
    
} catch {
    Write-Host "❌ Error running Docker command: $($_.Exception.Message)" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "🛡️  Security Scan Summary" -ForegroundColor Cyan
Write-Host "=========================" -ForegroundColor Cyan
Write-Host "Project: Phishing Detection Web App"
Write-Host "Scan Type: Dependency vulnerability check"
Write-Host "Tool: OWASP Dependency Check"
Write-Host "Status: Complete" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Review the HTML report for any HIGH or CRITICAL vulnerabilities"
Write-Host "2. Update vulnerable dependencies if found"
Write-Host "3. Re-run this script after updates to verify fixes"
Write-Host "4. Consider running this regularly (weekly/monthly)"
Write-Host ""

Read-Host "Press Enter to exit"