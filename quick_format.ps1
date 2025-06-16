#!/usr/bin/env pwsh
# Script rápido para formatear código Python
# Uso: .\quick_format.ps1

Write-Host "🐍 Formateando código Python..." -ForegroundColor Blue

# Verificar que estamos en el directorio correcto
if (-not (Test-Path "app")) {
    Write-Host "❌ Error: Ejecuta este script desde la raíz del proyecto." -ForegroundColor Red
    exit 1
}

try {
    Write-Host "🔄 Ordenando imports..." -ForegroundColor Yellow
    python -m isort app

    Write-Host "🔄 Formateando código..." -ForegroundColor Yellow  
    python -m black app

    Write-Host "✅ ¡Formateo completado!" -ForegroundColor Green
    Write-Host "💡 Para verificación completa usa: .\format_and_check.ps1" -ForegroundColor Cyan
}
catch {
    Write-Host "❌ Error durante el formateo: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
} 