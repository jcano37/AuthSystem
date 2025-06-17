# Ensure we're in the correct directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location (Join-Path $scriptDir "..")

# Run the format and check script
& .\format_and_check.ps1

# Check the exit code
if ($LASTEXITCODE -ne 0) {
    Write-Host "Format and check failed. Commit aborted."
    exit 1
}

exit 0 