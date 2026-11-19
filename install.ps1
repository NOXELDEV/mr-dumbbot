# DumbBot skill installer (by noxeldev). Copies the skill to every agent found on this PC.
# Usage: powershell -ExecutionPolicy Bypass -File install.ps1
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$targets = @{
  'claude-code' = Join-Path $HOME '.claude\skills'
  'opencode'    = Join-Path $HOME '.config\opencode\skill'
  'codex'       = Join-Path $HOME '.codex\skills'
  'hermes'      = Join-Path $env:LOCALAPPDATA 'hermes\skills'
}
foreach ($k in $targets.Keys) {
  $parent = Split-Path -Parent $targets[$k]
  if (-not (Test-Path $parent)) { Write-Host "skip $k (not installed)"; continue }
  $dest = Join-Path $targets[$k] 'dumbbot'
  New-Item -ItemType Directory -Force $dest | Out-Null
  Copy-Item -Recurse -Force (Join-Path $root "adapters\$k\dumbbot\*") $dest
  Write-Host "installed $k -> $dest"
}
