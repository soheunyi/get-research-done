param(
  [string]$Root = "."
)

$ErrorActionPreference = "Stop"

New-Item -ItemType Directory -Force -Path $Root | Out-Null
$RootPath = (Resolve-Path $Root).Path
$PackDir = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

# Project-local skill locations (docs-aligned)
New-Item -ItemType Directory -Force -Path (Join-Path $RootPath ".agents/skills") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $RootPath ".claude/skills") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $RootPath ".opencode/skills") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $RootPath ".gemini/skills") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $RootPath ".grd/templates") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $RootPath ".grd/workflows") | Out-Null

# Core skills: shared across Codex/Claude/OpenCode/Gemini layouts.
Copy-Item -Recurse -Force (Join-Path $PackDir "skills/*") (Join-Path $RootPath ".agents/skills/")
Copy-Item -Recurse -Force (Join-Path $PackDir "skills/*") (Join-Path $RootPath ".claude/skills/")
Copy-Item -Recurse -Force (Join-Path $PackDir "skills/*") (Join-Path $RootPath ".opencode/skills/")
Copy-Item -Recurse -Force (Join-Path $PackDir "skills/*") (Join-Path $RootPath ".gemini/skills/")

Copy-Item -Recurse -Force (Join-Path $PackDir "templates/*") (Join-Path $RootPath ".grd/templates/")
Copy-Item -Recurse -Force (Join-Path $PackDir "workflows/*") (Join-Path $RootPath ".grd/workflows/")

Write-Host "Installed get-research-done pack into $RootPath"
Write-Host "Skill targets:"
Write-Host "  - $(Join-Path $RootPath '.agents/skills') (Codex/OpenCode)"
Write-Host "  - $(Join-Path $RootPath '.claude/skills') (Claude/OpenCode)"
Write-Host "  - $(Join-Path $RootPath '.opencode/skills') (OpenCode)"
Write-Host "  - $(Join-Path $RootPath '.gemini/skills') (Gemini CLI workspace skills)"
Write-Host "Runtime docs: $(Join-Path $RootPath '.grd/workflows/research-pipeline.md')"
Write-Host 'Use GRD skills: $grd-hypothesis-designer, $grd-experiment-planner, $grd-evaluation-analyst'
