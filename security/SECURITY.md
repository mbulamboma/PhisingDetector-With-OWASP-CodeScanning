# Vulnerability Management Guide

## Quick Start

Run a security scan on the webapp:

**Windows (PowerShell):**
```powershell
cd security
.\Run-SecurityScan.ps1
```

**Windows (Command Prompt):**
```cmd
cd security
run-security-scan.bat
```

**Linux/Mac:**
```bash
cd security
./run-security-scan.sh
```

## What This Does

Uses OWASP Dependency Check to scan your Python dependencies for known security vulnerabilities. The tool:

1. Downloads the latest vulnerability database
2. Scans all packages in `webapp/requirements.txt`
3. Checks against CVE (Common Vulnerabilities and Exposures) database
4. Generates detailed reports in `security/security-reports/`

## Prerequisites

- **Docker**: Must be installed and running
- **Internet connection**: For downloading vulnerability database (first run)
- **Disk space**: ~500MB for vulnerability database

## Understanding the Results

The scan generates reports in `security/security-reports/`:

### Report Severity Levels
- **CRITICAL (9.0-10.0)**: Drop everything and fix immediately
- **HIGH (7.0-8.9)**: Fix within days
- **MEDIUM (4.0-6.9)**: Fix within weeks  
- **LOW (0.1-3.9)**: Fix when convenient

### Common Issues Found
- **Outdated Flask**: Often has XSS vulnerabilities
- **Old Jinja2**: Template injection risks
- **Insecure requests/urllib3**: SSL/TLS issues
- **Development tools**: Should not be in production requirements

## Fixing Vulnerabilities

### 1. Update Specific Package
```bash
pip install --upgrade package-name==safe-version
```

### 2. Update All Packages
```bash
pip install --upgrade -r requirements.txt
```

### 3. Update requirements.txt
After testing, pin the safe versions:
```
Flask==2.3.2  # was 2.0.1 (vulnerable)
Jinja2==3.1.2  # was 3.0.3 (vulnerable)
```

### 4. Test and Re-scan
```bash
# Test the app still works
python app.py

# Re-run security scan
.\Run-SecurityScan.ps1
```

## CI/CD Integration

Add to your build pipeline:

```yaml
# Example GitHub Actions
- name: Security Scan
  run: |
    docker run --rm -v $(pwd):/src -v $(pwd)/reports:/report \
      owasp/dependency-check:latest \
      --scan /src --format JSON --project MyApp --out /report
```

## Best Practices

### Regular Scanning
- **Development**: Weekly or before each release
- **Production**: Monthly or when new vulnerabilities announced
- **Critical systems**: Daily automated scans

### Dependency Management
- Pin specific versions in `requirements.txt`
- Separate dev/test dependencies from production
- Use virtual environments
- Keep dependencies minimal

### Response Plan
1. **Critical/High**: Fix within 24-48 hours
2. **Medium**: Fix within 2 weeks
3. **Low**: Fix in next planned release
4. **Document**: Track what was fixed and when

## Limitations

OWASP Dependency Check only finds **known** vulnerabilities:
- Won't catch zero-day exploits
- Won't find logic flaws in your code
- Won't detect misconfigurations
- Only scans dependencies, not your actual code

## Additional Security Tools

Consider also using:
- **Bandit**: Scans Python code for security issues
- **Safety**: Python-specific vulnerability checker
- **Snyk**: Commercial tool with more features
- **CodeQL**: Static analysis for code vulnerabilities

## Troubleshooting

**"Docker not found"**: Install Docker Desktop and make sure it's running

**"Permission denied"**: Run as administrator (Windows) or use `sudo` (Linux)

**"Network timeout"**: First run downloads ~500MB, may take time on slow connections

**"No vulnerabilities found"**: Either you have very up-to-date dependencies (good!) or the scan didn't work properly

**"Too many vulnerabilities"**: Focus on CRITICAL and HIGH first, others can wait

## Getting Help

- **OWASP Dependency Check docs**: https://owasp.org/www-project-dependency-check/
- **CVE database**: https://cve.mitre.org/
- **Python security advisories**: https://github.com/pypa/advisory-database