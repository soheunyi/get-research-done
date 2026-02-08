param(
  [string]$Root = "."
)

$ErrorActionPreference = "Stop"

New-Item -ItemType Directory -Force -Path "$Root/.agent/skills" | Out-Null
New-Item -ItemType Directory -Force -Path "$Root/.codex/skills" | Out-Null
New-Item -ItemType Directory -Force -Path "$Root/.gsd/templates" | Out-Null

Copy-Item -Recurse -Force "get-research-done/.agents/skills/*" "$Root/.agent/skills/"
Copy-Item -Recurse -Force "get-research-done/.codex/skills/*" "$Root/.codex/skills/"
Copy-Item -Force "get-research-done/templates/research-notes.md" "$Root/.gsd/templates/research-notes.md"
Copy-Item -Force "get-research-done/templates/wandb-config.md" "$Root/.gsd/templates/wandb-config.md"

Write-Host "Installed get-research-done pack into $Root"
Write-Host 'Use Codex skills: $grd-research-hypothesis-designer, $grd-research-experiment-planner, $grd-research-evaluation-analyst'
