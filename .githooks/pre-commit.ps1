# Extensive Pre-Commit Hook Debugging
$ErrorActionPreference = 'Stop'

try {
    # Detailed logging setup
    $logFile = "C:\temp\pre-commit-hook-log.txt"
    New-Item -Path $logFile -Force | Out-Null

    # Log start of hook
    Add-Content -Path $logFile -Value "$(Get-Date): Pre-commit hook started"
    Add-Content -Path $logFile -Value "Current directory: $((Get-Location).Path)"

    # Explicitly set working directory
    $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
    Set-Location (Join-Path $scriptDir "..")
    Add-Content -Path $logFile -Value "Changed to directory: $((Get-Location).Path)"

    # Run format and check script with full error capture
    $process = Start-Process powershell.exe -ArgumentList "-Command `"& .\format_and_check.ps1 --verbose`"" -PassThru -Wait -NoNewWindow -RedirectStandardOutput "$logFile.stdout" -RedirectStandardError "$logFile.stderr"
    
    # Log process details
    Add-Content -Path $logFile -Value "Process Exit Code: $($process.ExitCode)"
    Add-Content -Path $logFile -Value "STDOUT: $(Get-Content "$logFile.stdout")"
    Add-Content -Path $logFile -Value "STDERR: $(Get-Content "$logFile.stderr")"

    # Check exit code
    if ($process.ExitCode -ne 0) {
        Add-Content -Path $logFile -Value "❌ Format and check failed. Commit aborted."
        Write-Host "❌ Format and check failed. Commit aborted." -ForegroundColor Red
        exit 1
    }

    Add-Content -Path $logFile -Value "✅ Pre-commit hook completed successfully."
    exit 0
}
catch {
    # Capture any unexpected errors
    $errorMessage = $_.Exception.Message
    Add-Content -Path $logFile -Value "❌ Unexpected error: $errorMessage"
    Add-Content -Path $logFile -Value "Full error details: $($_.Exception | Format-List * | Out-String)"
    Write-Host "❌ Unexpected error in pre-commit hook: $errorMessage" -ForegroundColor Red
    exit 1
} 