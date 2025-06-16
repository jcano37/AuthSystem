#!/usr/bin/env pwsh
# Script de PowerShell para formatear y verificar código Python
# Autor: Asistente IA
# Uso: .\format_and_check.ps1 [--check-only] [--fix] [--verbose]

param(
    [switch]$CheckOnly,      # Solo verificar, no formatear
    [switch]$Fix,            # Formatear y arreglar problemas automáticamente  
    [switch]$Verbose,        # Salida detallada
    [switch]$Help            # Mostrar ayuda
)

# Colores para output
$Green = "Green"
$Red = "Red"
$Yellow = "Yellow"
$Blue = "Blue"
$Magenta = "Magenta"

function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

function Show-Help {
    Write-ColorOutput "=== SCRIPT DE FORMATEO Y VERIFICACIÓN DE CÓDIGO PYTHON ===" $Blue
    Write-ColorOutput ""
    Write-ColorOutput "DESCRIPCIÓN:" $Yellow
    Write-ColorOutput "  Este script automatiza el formateo y verificación de código Python usando:"
    Write-ColorOutput "  • Black (formateo de código)"
    Write-ColorOutput "  • isort (ordenamiento de imports)"
    Write-ColorOutput "  • flake8 (linting y verificación de estilo)"
    Write-ColorOutput "  • mypy (verificación de tipos)"
    Write-ColorOutput ""
    Write-ColorOutput "USO:" $Yellow
    Write-ColorOutput "  .\format_and_check.ps1 [OPCIONES]"
    Write-ColorOutput ""
    Write-ColorOutput "OPCIONES:" $Yellow
    Write-ColorOutput "  --check-only    Solo verificar código, no hacer cambios"
    Write-ColorOutput "  --fix          Formatear y arreglar automáticamente"
    Write-ColorOutput "  --verbose      Mostrar salida detallada"
    Write-ColorOutput "  --help         Mostrar esta ayuda"
    Write-ColorOutput ""
    Write-ColorOutput "EJEMPLOS:" $Yellow
    Write-ColorOutput "  .\format_and_check.ps1                    # Verificar y formatear"
    Write-ColorOutput "  .\format_and_check.ps1 --check-only       # Solo verificar"
    Write-ColorOutput "  .\format_and_check.ps1 --fix --verbose    # Formatear con detalles"
    exit 0
}

function Test-Command {
    param([string]$Command)
    
    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

function Run-Command {
    param(
        [string]$Command,
        [string]$Description,
        [switch]$ContinueOnError
    )
    
    Write-ColorOutput "🔄 $Description..." $Blue
    
    if ($Verbose) {
        Write-ColorOutput "Ejecutando: $Command" $Magenta
    }
    
    try {
        $result = Invoke-Expression $Command
        $exitCode = $LASTEXITCODE
        
        if ($exitCode -eq 0) {
            Write-ColorOutput "✅ $Description completado exitosamente" $Green
            if ($Verbose -and $result) {
                Write-ColorOutput $result
            }
            return $true
        } else {
            Write-ColorOutput "❌ $Description falló (código: $exitCode)" $Red
            if ($result) {
                Write-ColorOutput $result $Red
            }
            if (-not $ContinueOnError) {
                throw "El comando falló: $Command"
            }
            return $false
        }
    }
    catch {
        Write-ColorOutput "❌ Error ejecutando $Description`: $($_.Exception.Message)" $Red
        if (-not $ContinueOnError) {
            throw
        }
        return $false
    }
}

# Mostrar ayuda si se solicita
if ($Help) {
    Show-Help
}

# Banner inicial
Write-ColorOutput ""
Write-ColorOutput "==========================================" $Blue
Write-ColorOutput "  🐍 FORMATEO Y VERIFICACIÓN DE CÓDIGO  " $Blue  
Write-ColorOutput "==========================================" $Blue
Write-ColorOutput ""

# Verificar que estamos en el directorio correcto
if (-not (Test-Path "app")) {
    Write-ColorOutput "❌ Error: No se encontró el directorio 'app'. Ejecuta este script desde la raíz del proyecto." $Red
    exit 1
}

Write-ColorOutput "📁 Directorio del proyecto: $(Get-Location)" $Yellow
Write-ColorOutput "⚙️  Modo: $(if ($CheckOnly) { 'Solo verificación' } elseif ($Fix) { 'Formateo automático' } else { 'Verificación y formateo' })" $Yellow
Write-ColorOutput ""

# Verificar herramientas instaladas
Write-ColorOutput "🔍 Verificando herramientas instaladas..." $Yellow

$tools = @(
    @{Name = "black"; Command = "python -m black --version" },
    @{Name = "isort"; Command = "python -m isort --version" },
    @{Name = "flake8"; Command = "python -m flake8 --version" },
    @{Name = "mypy"; Command = "python -m mypy --version" }
)

$missingTools = @()
foreach ($tool in $tools) {
    if (Test-Command "python") {
        try {
            $null = Invoke-Expression $tool.Command
            Write-ColorOutput "  ✅ $($tool.Name) está instalado" $Green
        }
        catch {
            Write-ColorOutput "  ❌ $($tool.Name) no está instalado" $Red
            $missingTools += $tool.Name
        }
    } else {
        Write-ColorOutput "❌ Python no está disponible en PATH" $Red
        exit 1
    }
}

if ($missingTools.Count -gt 0) {
    Write-ColorOutput "❌ Faltan herramientas: $($missingTools -join ', ')" $Red
    Write-ColorOutput "💡 Instálalas con: python -m pip install $($missingTools -join ' ')" $Yellow
    exit 1
}

Write-ColorOutput ""

# Variables para el seguimiento de errores
$hasErrors = $false
$results = @()

# 1. isort - Ordenar imports
if ($CheckOnly) {
    $success = Run-Command "python -m isort --check-only --diff app" "Verificando ordenamiento de imports" -ContinueOnError
} else {
    $success = Run-Command "python -m isort app" "Ordenando imports" -ContinueOnError
}
$results += @{Tool = "isort"; Success = $success}
if (-not $success) { $hasErrors = $true }

# 2. Black - Formateo de código
if ($CheckOnly) {
    $success = Run-Command "python -m black --check --diff app" "Verificando formateo de código" -ContinueOnError
} else {
    $success = Run-Command "python -m black app" "Formateando código" -ContinueOnError
}
$results += @{Tool = "black"; Success = $success}
if (-not $success) { $hasErrors = $true }

# 3. Flake8 - Linting
$success = Run-Command "python -m flake8 app" "Ejecutando linting (flake8)" -ContinueOnError
$results += @{Tool = "flake8"; Success = $success}
if (-not $success) { $hasErrors = $true }

# 4. MyPy - Verificación de tipos
$success = Run-Command "python -m mypy app" "Verificando tipos (mypy)" -ContinueOnError
$results += @{Tool = "mypy"; Success = $success}
if (-not $success) { $hasErrors = $true }

# Resumen final
Write-ColorOutput ""
Write-ColorOutput "========================================" $Blue
Write-ColorOutput "           📊 RESUMEN FINAL             " $Blue
Write-ColorOutput "========================================" $Blue

foreach ($result in $results) {
    $status = if ($result.Success) { "✅ ÉXITO" } else { "❌ FALLÓ" }
    $color = if ($result.Success) { $Green } else { $Red }
    Write-ColorOutput "  $($result.Tool.PadRight(10)) : $status" $color
}

Write-ColorOutput ""

if ($hasErrors) {
    Write-ColorOutput "❌ Se encontraron errores en el código. Revisa los mensajes anteriores." $Red
    Write-ColorOutput "💡 Consejos:" $Yellow
    Write-ColorOutput "   • Usa '--fix' para corregir automáticamente problemas de formato" $Yellow
    Write-ColorOutput "   • Revisa manualmente los errores de flake8 y mypy" $Yellow
    Write-ColorOutput "   • Usa '--verbose' para más detalles" $Yellow
    exit 1
} else {
    Write-ColorOutput "🎉 ¡Todo el código está limpio y bien formateado!" $Green
    Write-ColorOutput "✨ Tu proyecto cumple con los estándares de calidad de código" $Green
    exit 0
} 