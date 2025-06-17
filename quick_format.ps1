#!/usr/bin/env pwsh
# Quick script to format Python code
# Usage: .\quick_format.ps1

Write-Host "🐍 Formatting Python code..." -ForegroundColor Blue

# Verify that we are in the correct directory
if (-not (Test-Path "app")) {
    Write-Host "❌ Error: Run this script from the project root." -ForegroundColor Red
    exit 1
}

try {
    Write-Host "🔄 Sorting imports..." -ForegroundColor Yellow
    python -m isort app

    Write-Host "🔄 Formatting code..." -ForegroundColor Yellow  
    python -m black app

    Write-Host "✅ Formatting complete!" -ForegroundColor Green
    Write-Host "💡 For a full check, use: .\format_and_check.ps1" -ForegroundColor Cyan
}
catch {
    Write-Host "❌ Error during formatting: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
