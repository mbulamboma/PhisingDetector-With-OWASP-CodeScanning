#!/bin/bash

# OWASP Dependency Check for Flask Web App
# This script scans the webapp folder for known security vulnerabilities

echo "🔍 Starting OWASP Dependency Check for Phishing Detection Web App"
echo "=================================================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Get the absolute path to the security and webapp directories
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SECURITY_DIR="$SCRIPT_DIR"
WEBAPP_DIR="$SCRIPT_DIR/../webapp"

echo "📁 Scanning directory: $WEBAPP_DIR"
echo "📁 Reports directory: $SECURITY_DIR/security-reports"
echo "📅 Scan date: $(date)"

# Create reports directory if it doesn't exist
mkdir -p "$SECURITY_DIR/security-reports"

# Run OWASP Dependency Check
echo ""
echo "🚀 Running OWASP Dependency Check..."
echo "This might take a few minutes on first run (downloading vulnerability database)"

docker run --rm \
    -e user=$USER \
    -u $(id -u ${USER}):$(id -g ${USER}) \
    --volume "$WEBAPP_DIR":/src:z \
    --volume "$SECURITY_DIR/security-reports":/report:z \
    owasp/dependency-check:latest \
    --scan /src \
    --format "ALL" \
    --project "Phishing-Detection-WebApp" \
    --out /report

# Check if scan completed successfully
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Vulnerability scan completed successfully!"
    echo ""
    echo "📊 Reports generated:"
    echo "   - HTML Report: $SECURITY_DIR/security-reports/dependency-check-report.html"
    echo "   - JSON Report: $SECURITY_DIR/security-reports/dependency-check-report.json"
    echo "   - XML Report:  $SECURITY_DIR/security-reports/dependency-check-report.xml"
    echo ""
    echo "💡 To view the HTML report:"
    echo "   Open: file://$SECURITY_DIR/security-reports/dependency-check-report.html"
    echo ""
    
    # Try to open the report automatically (works on some systems)
    if command -v xdg-open > /dev/null; then
        echo "🌐 Opening report in default browser..."
        xdg-open "$SECURITY_DIR/security-reports/dependency-check-report.html"
    elif command -v open > /dev/null; then
        echo "🌐 Opening report in default browser..."
        open "$SECURITY_DIR/security-reports/dependency-check-report.html"
    fi
    
else
    echo ""
    echo "❌ Vulnerability scan failed. Check the output above for errors."
    exit 1
fi

echo ""
echo "🛡️  Security Scan Summary"
echo "========================="
echo "Project: Phishing Detection Web App"
echo "Scan Type: Dependency vulnerability check"
echo "Tool: OWASP Dependency Check"
echo "Status: Complete"
echo ""
echo "Next steps:"
echo "1. Review the HTML report for any HIGH or CRITICAL vulnerabilities"
echo "2. Update vulnerable dependencies if found"
echo "3. Re-run this script after updates to verify fixes"
echo "4. Consider running this regularly (weekly/monthly)"