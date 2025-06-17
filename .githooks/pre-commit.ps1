# Strict Pre-Commit Hook
$ErrorActionPreference = 'Stop'

# Ensure we're in the correct directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location (Join-Path $scriptDir "..")

# Run format and check script
$output = & .\format_and_check.ps1 --verbose 2>&1

# Capture the exit code
$exitCode = $LASTEXITCODE

# Write detailed log
$logPath = "C:\temp\pre-commit-debug.log"
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Add-Content -Path $logPath -Value "--- Commit Attempt at $timestamp ---"
Add-Content -Path $logPath -Value "Exit Code: $exitCode"
Add-Content -Path $logPath -Value "Output:"
$output | ForEach-Object { Add-Content -Path $logPath -Value $_ }

# If exit code is not 0, abort the commit
if ($exitCode -ne 0) {
    Write-Host "❌ Code quality checks failed. Commit aborted." -ForegroundColor Red
    Add-Content -Path $logPath -Value "COMMIT BLOCKED"
    exit 1
}

# If we get here, commit is allowed
Add-Content -Path $logPath -Value "COMMIT ALLOWED"
exit 0 