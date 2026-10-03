$ErrorActionPreference = "Stop"

Set-Location $PSScriptRoot

# Sirf tab commit/push karo jab tracked ya untracked changes hon
git add -A

if (git diff --cached --quiet) {
    Write-Host "No changes to push."
    exit 0
}

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
git commit -m "Auto-save: $timestamp"

if ($LASTEXITCODE -ne 0) {
    throw "Commit failed. Please check Git status."
}

git push

if ($LASTEXITCODE -ne 0) {
    throw "Push failed. Check your internet or GitHub sync."
}

Write-Host "Changes pushed successfully."