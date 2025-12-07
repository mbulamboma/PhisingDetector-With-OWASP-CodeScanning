<#
Procédure d'analyse de vulnérabilités sécuritaires
Implémentation OWASP Dependency Check pour l'audit de sécurité de l'application
Auteur: Mbula Mboma Jean Gilbert (MikaelX)
Année: 2024-2025
#>

Write-Host "🔍 Initialisation du processus d'analyse de vulnérabilités..." -ForegroundColor Cyan
Write-Host "===============================================" -ForegroundColor Cyan

# Vérification de disponibilité du service Docker
try {
    docker info | Out-Null
    Write-Host "✅ Service Docker opérationnel" -ForegroundColor Green
} catch {
    Write-Host "❌ Service Docker non disponible. Veuillez démarrer Docker Desktop." -ForegroundColor Red
    Read-Host "Appuyez sur Entrée pour terminer"
    exit 1
}

# Configuration des répertoires de travail (dossier security et webapp)
$securityDir = Get-Location
$webappDir = Join-Path $securityDir "..\webapp" | Resolve-Path
$reportsDir = Join-Path $securityDir "security-reports"

Write-Host "📁 Scanning directory: $webappDir" -ForegroundColor Yellow
Write-Host "📁 Reports directory: $reportsDir" -ForegroundColor Yellow
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
Write-Host "🛡️  Rapport d'Exécution de l'Analyse Sécuritaire" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Projet : Système de Détection de Phishing"
Write-Host "Type d'Analyse : Vérification des Dépendances"
Write-Host "Outil Utilisé : OWASP Dependency Check"
Write-Host "Statut : Analyse Complétée" -ForegroundColor Green
Write-Host ""
Write-Host "Procédures Post-Analyse :" -ForegroundColor Yellow
Write-Host "1. Examiner le rapport HTML pour détecter les vulnérabilités critiques"
Write-Host "2. Procéder aux mises à jour des dépendances si requis"
Write-Host "3. Re-exécuter le processus d'analyse après modifications"
Write-Host "4. Implémenter une cadence d'exécution régulière"
Write-Host ""

Read-Host "Appuyez sur Entrée pour terminer"