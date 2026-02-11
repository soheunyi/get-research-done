# get-research-done

Portable research workflow pack for AI/statistics projects.

## Install (Recommended: Python CLI)

Install the package, then run `grd-install` from anywhere.

`pipx` (recommended for isolated CLI tools):

```bash
pipx install "git+https://github.com/soheunyi/get-research-done.git"
```

`pip`:

```bash
python3 -m pip install "git+https://github.com/soheunyi/get-research-done.git"
```

From a local checkout during development:

```bash
python3 -m pip install -e .
```

Install into a target repository:

```bash
# Default target is "core" (runtime + codex/claude/opencode/gemini)
grd-install /path/to/target-repo

# Runtime docs/templates only
grd-install /path/to/target-repo --target runtime

# Per-tool
grd-install /path/to/target-repo --target codex
grd-install /path/to/target-repo --target claude
grd-install /path/to/target-repo --target opencode
grd-install /path/to/target-repo --target gemini

# Multiple targets
grd-install /path/to/target-repo --target runtime,codex

# Show valid target names
grd-install --list-targets
```

Uninstall from a target repository:

```bash
# Remove all GRD-installed skills (keeps .grd runtime artifacts by default)
grd-uninstall /path/to/target-repo

# Remove specific skill targets
grd-uninstall /path/to/target-repo --target codex,claude

# Also remove runtime docs/templates
grd-uninstall /path/to/target-repo --include-runtime

# Show valid uninstall target names
grd-uninstall --list-targets
```

## Install (Make Alternative)

Run from this repository checkout:

```bash
# Show all install targets
make install-help

# Install all supported targets + runtime docs/templates
make install-all DEST=/path/to/target-repo
```

Per-target install:

```bash
# Runtime docs/templates only
make install-runtime DEST=/path/to/target-repo

# Skills by tool
make install-codex DEST=/path/to/target-repo
make install-claude DEST=/path/to/target-repo
make install-opencode DEST=/path/to/target-repo
make install-gemini DEST=/path/to/target-repo

# Core set (runtime + codex/claude/opencode/gemini)
make install-core DEST=/path/to/target-repo
```

## Installed Paths

- Runtime docs/templates:
  - `.grd/workflows/research-pipeline.md`
  - `.grd/templates/*`
- Skills:
  - Codex/OpenCode: `.agents/skills/*/SKILL.md`
  - Claude Code: `.claude/skills/*/SKILL.md`
  - OpenCode native: `.opencode/skills/*/SKILL.md`
  - Gemini CLI: `.gemini/skills/*/SKILL.md`

## Source Of Truth

- Core skills: `skills/*`
- Core workflow: `workflows/research-pipeline.md`
- Templates: `templates/*`
- Shared blocks: `skills/_shared/COMMON_BLOCKS.md`

`codex/` and `agy/` are generated compatibility views and are intentionally git-ignored.

## Dev Sync Commands

```bash
# Sync shared boilerplate into skills
make sync-skills

# Validate shared boilerplate sync
make check-skills

# Regenerate compatibility views locally (git-ignored)
make sync-codex
make sync-agy
```

## Script Installer (Optional)

Shell:

```bash
bash scripts/install.sh /path/to/target-repo
```

PowerShell:

```powershell
.\scripts\install.ps1 -Root "C:\path\to\target-repo"
```
