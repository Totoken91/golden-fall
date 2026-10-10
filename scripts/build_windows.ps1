param([Parameter(Mandatory=$true)][string]$GodotPath)
$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$enginePath = (Resolve-Path -LiteralPath $GodotPath).Path
$cliPath = $enginePath
if ($enginePath.EndsWith('_console.exe')) {
    $enginePath = $enginePath.Replace('_console.exe','.exe')
    if (-not (Test-Path -LiteralPath $enginePath)) { throw 'The full Godot executable is required.' }
}
if (-not $cliPath.EndsWith('_console.exe')) {
    $consoleCandidate = $enginePath.Replace('.exe','_console.exe')
    if (-not (Test-Path -LiteralPath $consoleCandidate)) { throw 'Pass the Godot 4.6 _console.exe distributed alongside its full executable.' }
    $cliPath = $consoleCandidate
}
$versionText = & $cliPath --headless --version
if (-not ($versionText -match '^4\.6\.')) { throw 'This prototype was verified with Godot 4.6.' }
$gamePath = Join-Path $projectRoot 'game'
$playPath = Join-Path $projectRoot 'play'
New-Item -ItemType Directory -Path $playPath -Force | Out-Null
& $cliPath --headless --path $gamePath --editor --import --quit
if ($LASTEXITCODE -ne 0) { throw 'Godot resource import failed.' }
& $cliPath --headless --path $gamePath --script 'res://scripts/room_review.gd' --check-only
if ($LASTEXITCODE -ne 0) { throw 'Room controller parsing failed.' }
& $cliPath --headless --path $gamePath --export-pack 'Windows Desktop' (Join-Path $playPath 'LesHeuresCreuses.pck')
if ($LASTEXITCODE -ne 0) { throw 'Godot pack export failed.' }
Copy-Item -LiteralPath $enginePath -Destination (Join-Path $playPath 'LesHeuresCreuses.exe') -Force
Write-Output 'Ready: play/LesHeuresCreuses.exe (keep its PCK alongside it).'
