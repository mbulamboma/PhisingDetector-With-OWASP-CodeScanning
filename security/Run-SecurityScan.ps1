# OWASP Dependency Check - Analyse de sécurité
# Lance un scan des vulnérabilités des dépendances webapp

Write-Host "Démarrage de l'analyse de sécurité..." -ForegroundColor Cyan

# Vérifier que Docker est démarré
try {
    docker info | Out-Null
} catch {
    Write-Host "Erreur : Docker n'est pas démarré. Lancez Docker Desktop." -ForegroundColor Red
    exit 1
}

$webappDir = Resolve-Path "..\webapp"
$reportsDir = "security-reports"

if (!(Test-Path $reportsDir)) {
    New-Item -ItemType Directory -Path $reportsDir -Force | Out-Null
}

Write-Host "Exécution de OWASP Dependency Check (première fois ~5min pour télécharger la BD)..." -ForegroundColor Yellow

try {
    docker run --rm `
        --volume "$($webappDir):/src" `
        --volume "$reportsDir:/report" `
        owasp/dependency-check:latest `
        --scan /src `
        --format ALL `
        --project "Phishing-Detection-WebApp" `
        --out /report
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Scan terminé ! Ouverture du rapport..." -ForegroundColor Green
        
        $htmlReport = Join-Path $reportsDir "dependency-check-report.html"
        if (Test-Path $htmlReport) {
            Start-Process $htmlReport
        }
    } else {
        Write-Host "Échec du scan. Vérifiez les messages ci-dessus." -ForegroundColor Red
        exit 1
    }
    
} catch {
    Write-Host "Erreur : $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}