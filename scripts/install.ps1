param(
  [string]$Root = "."
)

$ErrorActionPreference = "Stop"

New-Item -ItemType Directory -Force -Path $Root | Out-Null
$RootPath = (Resolve-Path $Root).Path
$PackDir = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

# Project-local skill locations (official docs + compatibility)
New-Item -ItemType Directory -Force -Path (Join-Path $RootPath ".agents/skills") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $RootPath ".claude/skills") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $RootPath ".opencode/skills") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $RootPath ".gemini/skills") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $RootPath ".codex/skills") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $RootPath ".agent/skills") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $RootPath ".grd/templates") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $RootPath ".grd/workflows") | Out-Null

# Core skills: shared across Codex/Claude/OpenCode/Gemini layouts.
Copy-Item -Recurse -Force (Join-Path $PackDir "skills/*") (Join-Path $RootPath ".agents/skills/")
Copy-Item -Recurse -Force (Join-Path $PackDir "skills/*") (Join-Path $RootPath ".claude/skills/")
Copy-Item -Recurse -Force (Join-Path $PackDir "skills/*") (Join-Path $RootPath ".opencode/skills/")
Copy-Item -Recurse -Force (Join-Path $PackDir "skills/*") (Join-Path $RootPath ".gemini/skills/")
Copy-Item -Recurse -Force (Join-Path $PackDir "skills/*") (Join-Path $RootPath ".codex/skills/")
Copy-Item -Recurse -Force (Join-Path $PackDir "agy/skills/*") (Join-Path $RootPath ".agent/skills/")

Copy-Item -Recurse -Force (Join-Path $PackDir "templates/*") (Join-Path $RootPath ".grd/templates/")
Copy-Item -Recurse -Force (Join-Path $PackDir "workflows/*") (Join-Path $RootPath ".grd/workflows/")

# Copy workflow references (without copying .git or unrelated repo files).
New-Item -ItemType Directory -Force -Path (Join-Path $RootPath "get-research-done/agy") | Out-Null
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue (Join-Path $RootPath "get-research-done/agy/workflows")
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue (Join-Path $RootPath "get-research-done/workflows")
Copy-Item -Recurse -Force (Join-Path $PackDir "agy/workflows") (Join-Path $RootPath "get-research-done/agy/")
Copy-Item -Recurse -Force (Join-Path $PackDir "workflows") (Join-Path $RootPath "get-research-done/")

# Keep templates/scripts/readme available in target pack path for manual transplant.
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue (Join-Path $RootPath "get-research-done/templates")
Remove-Item -Recurse -Force -ErrorAction SilentlyContinue (Join-Path $RootPath "get-research-done/scripts")
Copy-Item -Recurse -Force (Join-Path $PackDir "templates") (Join-Path $RootPath "get-research-done/")
Copy-Item -Recurse -Force (Join-Path $PackDir "scripts") (Join-Path $RootPath "get-research-done/")
Copy-Item -Force (Join-Path $PackDir "README.md") (Join-Path $RootPath "get-research-done/README.md")

Write-Host "Installed get-research-done pack into $RootPath"
Write-Host "Skill targets:"
Write-Host "  - $(Join-Path $RootPath '.agents/skills') (Codex/OpenCode)"
Write-Host "  - $(Join-Path $RootPath '.claude/skills') (Claude/OpenCode)"
Write-Host "  - $(Join-Path $RootPath '.opencode/skills') (OpenCode)"
Write-Host "  - $(Join-Path $RootPath '.gemini/skills') (Gemini CLI workspace skills)"
Write-Host "  - $(Join-Path $RootPath '.codex/skills') (legacy compatibility)"
Write-Host "Runtime docs: $(Join-Path $RootPath '.grd/workflows/research-pipeline.md')"
Write-Host 'Use GRD skills: $grd-hypothesis-designer, $grd-experiment-planner, $grd-evaluation-analyst'
