# Security

This folder contains all security-related tools and reports for the Phishing Detection project.

## Contents

- `run-security-scan.bat` - Windows batch script for vulnerability scanning
- `Run-SecurityScan.ps1` - Windows PowerShell script for vulnerability scanning  
- `run-security-scan.sh` - Linux/Mac bash script for vulnerability scanning
- `SECURITY.md` - Complete vulnerability management guide
- `security-reports/` - Generated vulnerability scan reports

## Quick Start

Choose the script for your operating system:

**Windows (PowerShell - Recommended):**
```powershell
.\Run-SecurityScan.ps1
```

**Windows (Command Prompt):**
```cmd
run-security-scan.bat
```

**Linux/Mac:**
```bash
./run-security-scan.sh
```

## What It Does

Scans the `webapp` folder for security vulnerabilities in Python dependencies using OWASP Dependency Check. Reports are saved to `security-reports/` with detailed findings.

## Prerequisites

- Docker Desktop installed and running
- Internet connection for vulnerability database download

## First Run

The first scan will take 10-15 minutes to download the vulnerability database (~500MB). Subsequent scans will be much faster.

## Reports

After scanning, check `security-reports/dependency-check-report.html` for detailed results. Focus on CRITICAL and HIGH severity vulnerabilities first.