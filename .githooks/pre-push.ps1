# Ensure we're in the correct directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location (Join-Path $scriptDir "..")

# Run the format and check script with verbose output
$ErrorActionPreference = 'Stop'
try {
    & .\format_and_check.ps1 --verbose
    $formatCheckExitCode = $LASTEXITCODE
}
catch {
    Write-Host "Format and check script encountered an error."
    $formatCheckExitCode = 1
}

# Check the exit code
if ($formatCheckExitCode -ne 0) {
    Write-Host "Format and check failed. Push aborted."
    exit 1
}

exit 0 