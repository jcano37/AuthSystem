# Debugging pre-commit hook
Write-Host "Starting pre-commit hook..."

# Ensure we're in the correct directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location (Join-Path $scriptDir "..")
Write-Host "Current directory: $((Get-Location).Path)"

# Run the format and check script with verbose output
Write-Host "Running format_and_check.ps1..."
$process = powershell.exe -Command "& .\format_and_check.ps1 --verbose" -PassThru -Wait -NoNewWindow
$formatCheckExitCode = $process.ExitCode

Write-Host "Exit code from format_and_check.ps1: $formatCheckExitCode"

# Check the exit code
if ($formatCheckExitCode -ne 0) {
    Write-Host "❌ Format and check failed. Commit aborted." -ForegroundColor Red
    Write-Host "Detailed error information:" -ForegroundColor Yellow
    powershell.exe -Command "& .\format_and_check.ps1 --verbose"
    exit 1
}

Write-Host "✅ Pre-commit hook completed successfully." -ForegroundColor Green
exit 0 