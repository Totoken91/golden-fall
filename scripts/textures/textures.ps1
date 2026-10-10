param([Parameter(ValueFromRemainingArguments = $true)][string[]]$PipelineArgs)
$ErrorActionPreference = 'Stop'
$textureScript = Join-Path $PSScriptRoot 'pipeline.py'
$texturePython = Get-Command python -ErrorAction SilentlyContinue
if ($texturePython) {
    & $texturePython.Source $textureScript @PipelineArgs
} else {
    $textureLauncher = Get-Command py -ErrorAction SilentlyContinue
    if (-not $textureLauncher) { throw 'Python 3.11+ requis ; installer Pillow avec scripts/textures/requirements.txt.' }
    & $textureLauncher.Source -3 $textureScript @PipelineArgs
}
exit $LASTEXITCODE
