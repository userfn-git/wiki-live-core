param([string]$Id="SNAP-0002",[string]$Topic="Session Update",[string]$Note="Synced with main")
Set-Location $PSScriptRoot
python -c "from src.core.snapshot import YusraSnapshot; s=YusraSnapshot().capture('$Id','$Topic',['$Note']); print('[SNAPSHOT SAVED]', s['id'], s['commit'][:8])"
git add docs/snapshots; git commit -m "docs(snapshot): record $Id - $Topic" -q; git push origin main -q
Write-Host "[OK] $Id pushed to GitHub main!" -ForegroundColor Green
