#!/usr/bin/env pwsh
# PowerShell script to format and check Python code
# Author: Jerry Cano
# Usage: .\format_and_check.ps1 [--check-only] [--fix] [--verbose]

param(
    [switch]$CheckOnly,      # Only check, do not format
    [switch]$Fix,            # Format and fix issues automatically
    [switch]$Verbose,        # Verbose output
    [switch]$Help            # Show help
)

# Colors for output
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
    Write-ColorOutput "=== PYTHON CODE FORMATTING AND CHECKING SCRIPT ===" $Blue
    Write-ColorOutput ""
    Write-ColorOutput "DESCRIPTION:" $Yellow
    Write-ColorOutput "  This script automates formatting and checking of Python code using:"
    Write-ColorOutput "  • Black (code formatting)"
    Write-ColorOutput "  • isort (import sorting)"
    Write-ColorOutput "  • flake8 (linting and style checking)"
    Write-ColorOutput "  • mypy (type checking)"
    Write-ColorOutput ""
    Write-ColorOutput "USAGE:" $Yellow
    Write-ColorOutput "  .\format_and_check.ps1 [OPTIONS]"
    Write-ColorOutput ""
    Write-ColorOutput "OPTIONS:" $Yellow
    Write-ColorOutput "  --check-only    Only check code, do not make changes"
    Write-ColorOutput "  --fix          Format and fix automatically"
    Write-ColorOutput "  --verbose      Show verbose output"
    Write-ColorOutput "  --help         Show this help message"
    Write-ColorOutput ""
    Write-ColorOutput "EXAMPLES:" $Yellow
    Write-ColorOutput "  .\format_and_check.ps1                    # Check and format"
    Write-ColorOutput "  .\format_and_check.ps1 --check-only       # Only check"
    Write-ColorOutput "  .\format_and_check.ps1 --fix --verbose    # Format with details"
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
        Write-ColorOutput "Executing: $Command" $Magenta
    }
    
    try {
        $result = Invoke-Expression $Command
        $exitCode = $LASTEXITCODE
        
        if ($exitCode -eq 0) {
            Write-ColorOutput "✅ $Description completed successfully" $Green
            if ($Verbose -and $result) {
                Write-ColorOutput $result
            }
            return $true
        } else {
            Write-ColorOutput "❌ $Description failed (code: $exitCode)" $Red
            if ($result) {
                Write-ColorOutput $result $Red
            }
            if (-not $ContinueOnError) {
                throw "The command failed: $Command"
            }
            return $false
        }
    }
    catch {
        Write-ColorOutput "❌ Error executing $Description`: $($_.Exception.Message)" $Red
        if (-not $ContinueOnError) {
            throw
        }
        return $false
    }
}

# Show help if requested
if ($Help) {
    Show-Help
}

# Initial banner
Write-ColorOutput ""
Write-ColorOutput "==========================================" $Blue
Write-ColorOutput "  🐍 CODE FORMATTING AND CHECKING  " $Blue  
Write-ColorOutput "==========================================" $Blue
Write-ColorOutput ""

# Verify that we are in the correct directory
if (-not (Test-Path "app")) {
    Write-ColorOutput "❌ Error: 'app' directory not found. Run this script from the project root." $Red
    exit 1
}

Write-ColorOutput "📁 Project directory: $(Get-Location)" $Yellow
Write-ColorOutput "⚙️  Mode: $(if ($CheckOnly) { 'Check only' } elseif ($Fix) { 'Auto-fix' } else { 'Check and format' })" $Yellow

# Display Python path
$pythonPath = (Get-Command python).Source
Write-ColorOutput "🐍 Using Python at: $pythonPath" $Yellow
Write-ColorOutput ""

# Check installed tools
Write-ColorOutput "🔍 Checking installed tools..." $Yellow

$tools = @(
    @{Name = "black"; Command = "python -m black --version" },
    @{Name = "isort"; Command = "python -m isort --version" },
    @{Name = "flake8"; Command = "python -m flake8 --version" },
    @{Name = "mypy"; Command = "python -m mypy --version" }
)

$missingTools = @()
foreach ($tool in $tools) {
    if (Test-Command "python") {
                Invoke-Expression $tool.Command 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "  ✅ $($tool.Name) is installed" $Green
        }
        else {
            Write-ColorOutput "  ❌ $($tool.Name) is not installed" $Red
            $missingTools += $tool.Name
        }
    } else {
        Write-ColorOutput "❌ Python is not available in PATH" $Red
        exit 1
    }
}

if ($missingTools.Count -gt 0) {
    Write-ColorOutput "❌ Missing tools: $($missingTools -join ', ')" $Red
    Write-ColorOutput "💡 Install them with: python -m pip install $($missingTools -join ' ')" $Yellow
    exit 1
}

Write-ColorOutput ""

# Variables for error tracking
$hasErrors = $false
$results = @()

# 1. isort - Sort imports
if ($CheckOnly) {
    $success = Run-Command "python -m isort --check-only --diff app" "Checking import sorting" -ContinueOnError
} else {
    $success = Run-Command "python -m isort app" "Sorting imports" -ContinueOnError
}
$results += @{Tool = "isort"; Success = $success}
if (-not $success) { $hasErrors = $true }

# 2. Black - Code formatting
if ($CheckOnly) {
    $success = Run-Command "python -m black --check --diff app" "Checking code formatting" -ContinueOnError
} else {
    $success = Run-Command "python -m black app" "Formatting code" -ContinueOnError
}
$results += @{Tool = "black"; Success = $success}
if (-not $success) { $hasErrors = $true }

# 3. Flake8 - Linting
$success = Run-Command "python -m flake8 app" "Running linting (flake8)" -ContinueOnError
$results += @{Tool = "flake8"; Success = $success}
if (-not $success) { $hasErrors = $true }

# 4. MyPy - Type checking
$success = Run-Command "python -m mypy app" "Checking types (mypy)" -ContinueOnError
$results += @{Tool = "mypy"; Success = $success}
if (-not $success) { $hasErrors = $true }

# Final summary
Write-ColorOutput ""
Write-ColorOutput "========================================" $Blue
Write-ColorOutput "           📊 FINAL SUMMARY             " $Blue
Write-ColorOutput "========================================" $Blue

foreach ($result in $results) {
    $status = if ($result.Success) { "✅ SUCCESS" } else { "❌ FAILED" }
    $color = if ($result.Success) { $Green } else { $Red }
    Write-ColorOutput "  $($result.Tool.PadRight(10)) : $status" $color
}

Write-ColorOutput ""

if ($hasErrors) {
    Write-ColorOutput "❌ Errors were found in the code. Review the messages above." $Red
    Write-ColorOutput "💡 Tips:" $Yellow
    Write-ColorOutput "   • Use '--fix' to automatically correct formatting issues" $Yellow
    Write-ColorOutput "   • Manually review flake8 and mypy errors" $Yellow
    Write-ColorOutput "   • Use '--verbose' for more details" $Yellow
    return $false
} else {
    Write-ColorOutput "🎉 All code is clean and well-formatted!" $Green
    Write-ColorOutput "✨ Your project meets code quality standards" $Green
    return $true
}
