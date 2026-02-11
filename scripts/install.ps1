param(
  [string]$Root = "."
)

$ErrorActionPreference = "Stop"

New-Item -ItemType Directory -Force -Path "$Root/.agent/skills" | Out-Null
New-Item -ItemType Directory -Force -Path "$Root/.codex/skills" | Out-Null
New-Item -ItemType Directory -Force -Path "$Root/.grd/templates" | Out-Null

Copy-Item -Recurse -Force "get-research-done/agy/skills/*" "$Root/.agent/skills/"
Copy-Item -Recurse -Force "get-research-done/codex/skills/*" "$Root/.codex/skills/"
Copy-Item -Recurse -Force "get-research-done/templates/*" "$Root/.grd/templates/"

Write-Host "Installed get-research-done pack into $Root"
Write-Host 'Use Codex skills: $grd-hypothesis-designer, $grd-experiment-planner, $grd-evaluation-analyst'
