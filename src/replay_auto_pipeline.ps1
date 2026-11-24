$ErrorActionPreference = 'Continue'

$docsDir     = [Environment]::GetFolderPath('MyDocuments')
$demosDir    = Join-Path $docsDir 'My Games\Rocket League\TAGame\Demos'
$wikiRoot    = 'D:\projects\wiki-live-core'
$wikiRawDir  = Join-Path $wikiRoot 'replays\raw'
$wikiDocsDir = Join-Path $wikiRoot 'docs\replays'
$wikiTelDir  = Join-Path $wikiRoot 'docs\telemetry'
$engRoot     = 'D:\projects\fn_physics_engine'
$engRepDir   = Join-Path $engRoot 'replays'
$venvPython  = 'D:\envs\rl_py_env\Scripts\python.exe'
$pushScript  = Join-Path $wikiTelDir 'push_shm_to_wikilive_ollama.py'
$utf8NoBom   = New-Object System.Text.UTF8Encoding($false)

foreach ($d in @($demosDir, $wikiRawDir, $wikiDocsDir, $wikiTelDir, $engRepDir)) {
    if (-not (Test-Path $d)) { New-Item -ItemType Directory -Path $d -Force | Out-Null }
}

$logFile = Join-Path $wikiDocsDir 'replay_watcher.log'
function Write-WatcherLog([string]$msg) {
    $line = "[$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')] $msg"
    Add-Content -Path $logFile -Value $line -Encoding UTF8
    Write-Host $line -ForegroundColor Cyan
}

function Invoke-ProcessSavedReplay([string]$fullPath) {
    if (-not (Test-Path $fullPath)) { return }
    $fileName = [System.IO.Path]::GetFileName($fullPath)
    $baseName = [System.IO.Path]::GetFileNameWithoutExtension($fullPath)

    $ready = $false
    for ($i = 0; $i -lt 30; $i++) {
        try {
            $fs = [System.IO.File]::Open($fullPath, 'Open', 'Read', 'Read')
            $fs.Close()
            $ready = $true
            break
        } catch {
            Start-Sleep -Milliseconds 500
        }
    }
    if (-not $ready) {
        Write-WatcherLog "Timeout waiting for file lock release: $fileName"
        return
    }

    $ts = Get-Date -Format 'yyyyMMdd_HHmmss'
    $destWikiReplay = Join-Path $wikiRawDir "${ts}_${fileName}"
    $destEngReplay  = Join-Path $engRepDir  "${ts}_${fileName}"

    Copy-Item -Path $fullPath -Destination $destWikiReplay -Force
    Copy-Item -Path $fullPath -Destination $destEngReplay  -Force
    $sizeKB = [Math]::Round((Get-Item $destWikiReplay).Length / 1KB, 2)
    Write-WatcherLog "Archived replay -> $destWikiReplay ($sizeKB KB)"

    # Automatically run SHM -> WikiLive + Ollama telemetry push on replay save
    $telemetrySnapshotMd = Join-Path $wikiTelDir 'latest_live_curve_yusra.md'
    $telemetryStatus = "Telemetry script not found."
    if ((Test-Path $pushScript) -and (Test-Path $venvPython)) {
        try {
            & $venvPython $pushScript 2>&1 | Out-Null
            if (Test-Path $telemetrySnapshotMd) {
                $telemetryStatus = "Captured & pushed via push_shm_to_wikilive_ollama.py -> $telemetrySnapshotMd"
                Write-WatcherLog $telemetryStatus
            }
        } catch {
            $telemetryStatus = "Telemetry hook warning: $($_.Exception.Message)"
            Write-WatcherLog $telemetryStatus
        }
    }

    $jsonOut = Join-Path $wikiDocsDir "${ts}_${baseName}.json"
    $parser = Get-ChildItem -Path 'D:\projects', 'D:\Tools' -Include 'rrrocket*.exe','boxcars*.exe' -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
    $parsedSummary = "Binary size: ${sizeKB} KB | Parser: Built-in Header Inspector"
    if ($parser) {
        try {
            & $parser.FullName $destWikiReplay | Out-File -FilePath $jsonOut -Encoding UTF8
            $parsedSummary = "Parsed via $($parser.Name) -> $jsonOut ($sizeKB KB)"
        } catch {}
    }

    $plotScript = Get-ChildItem -Path $engRoot -Filter 'plot_telemetry_curves.py' -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($plotScript -and (Test-Path $venvPython)) {
        try {
            & $venvPython $plotScript.FullName --replay $destEngReplay 2>&1 | Out-Null
        } catch {}
    }

    $yusraReport = "Local Ollama offline; replay archived safely under WikiLive PATH02-BR04 / PATH04-BR12."
    try {
        $tags = Invoke-RestMethod -Uri 'http://127.0.0.1:11434/api/tags' -Method Get -TimeoutSec 2
        if ($tags.models.Count -gt 0) {
            $m = ($tags.models | Where-Object { $_.name -like 'wikilife-yusra*' } | Select-Object -First 1).name
            if (-not $m) { $m = $tags.models[0].name }
            $prompt = "As Yusra (WikiLive Core), generate a concise Arabic technical archival note for a newly saved Rocket League replay: File=$fileName, Size=${sizeKB}KB, CurveProfile=Pro 1.27 Harmonized. Give 3 actionable checkpoints for 1v1 speedflips, recoveries, and aerial consistency."
            $body = [System.Text.Encoding]::UTF8.GetBytes((@{ model=$m; prompt=$prompt; stream=$false } | ConvertTo-Json))
            $resp = Invoke-RestMethod -Uri 'http://127.0.0.1:11434/api/generate' -Method Post -Body $body -ContentType 'application/json; charset=utf-8' -TimeoutSec 30
            if ($resp.response) { $yusraReport = [string]$resp.response }
        }
    } catch {}

    $mdReportPath = Join-Path $wikiDocsDir "${ts}_${baseName}_wikilive_report.md"
    $mdContent = @(
        "# WikiLive Replay Analysis Report // $baseName",
        "- **Timestamp:** $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')",
        "- **Source Demo:** ``$fullPath``",
        "- **WikiLive Archive:** ``$destWikiReplay``",
        "- **Pipeline Status:** $parsedSummary",
        "- **Live SHM & Ollama Telemetry:** $telemetryStatus",
        "",
        "## Yusra Technical Review",
        $yusraReport
    ) -join "`r`n"
    [System.IO.File]::WriteAllText($mdReportPath, $mdContent, $utf8NoBom)
    Write-WatcherLog "WikiLive Markdown report created -> $mdReportPath"
}

$fsw = New-Object System.IO.FileSystemWatcher
$fsw.Path = $demosDir
$fsw.Filter = '*.replay'
$fsw.IncludeSubdirectories = $false
$fsw.NotifyFilter = [System.IO.NotifyFilters]'FileName, LastWrite, Size'
$fsw.EnableRaisingEvents = $true

Write-WatcherLog "WikiLive Replay Auto-Watcher ACTIVE (with SHM->Ollama Telemetry Hook) on: $demosDir -> $wikiRawDir"

$seen = @{}
while ($true) {
    $ev = $fsw.WaitForChanged([System.IO.WatcherChangeTypes]::Created -bor [System.IO.WatcherChangeTypes]::Renamed, 2000)
    if (-not $ev.TimedOut -and $ev.Name) {
        $target = Join-Path $demosDir $ev.Name
        if (-not $seen.ContainsKey($target)) {
            $seen[$target] = Get-Date
            Invoke-ProcessSavedReplay -fullPath $target
        }
    }
}