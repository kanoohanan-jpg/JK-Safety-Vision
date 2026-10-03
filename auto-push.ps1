$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

# Remote branch ki latest information lo
git fetch origin
if ($LASTEXITCODE -ne 0) {
    throw "GitHub fetch failed. Check your internet connection."
}

# Remote par local mein na hone wale commits hain toh stop
$behind = git rev-list --count HEAD..origin/main
if ($LASTEXITCODE -ne 0) {
    throw "Could not check GitHub sync status."
}
if ([int]$behind -gt 0) {
    throw "GitHub has newer commits. Sync manually before auto-push."
}

# Changes stage karo
git add -A
if ($LASTEXITCODE -ne 0) {
    throw "Git add failed."
}

# Koi change nahi hai toh exit
git diff --cached --quiet
if ($LASTEXITCODE -eq 0) {
    Write-Host "No changes to push."
    exit 0
}

# Commit aur push
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
git commit -m "Auto-save: $timestamp"
if ($LASTEXITCODE -ne 0) {
    throw "Commit failed. Check Git status."
}

git push origin main
if ($LASTEXITCODE -ne 0) {
    throw "Push failed. Check GitHub sync and try again."
}

Write-Host "Changes pushed successfully."