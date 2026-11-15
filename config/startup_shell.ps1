$Repo = "D:\projects\wiki-live-core"
if (Test-Path $Repo) { Set-Location $Repo }
function global:prompt { "[FN-WIKILIFE | ADMIN] PS $($executionContext.SessionState.Path.CurrentLocation)> " }
$LockOk = (Test-Path "$Repo\Gemini.md") -and (Test-Path "$Repo\README.md") -and (Test-Path "$Repo\config\mutual_lock.json")
$State = if ($LockOk) { "LOCKED_OK" } else { "CHECK_REQ" }
$Br = git branch --show-current 2>$null
$Ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
Add-Content "$Repo\config\startup.log" "[$Ts] SHELL_ON_STARTUP | Trunk: $Br | MutualLock: $State" -Encoding utf8
Write-Host "[FN-WIKILIFE | SHELL ON STARTUP] Trunk: $Br | Gemini-README Lock: $State | Log: config/startup.log" -ForegroundColor Cyan
