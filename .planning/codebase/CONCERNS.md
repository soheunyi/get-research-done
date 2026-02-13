# Codebase Concerns

**Analysis Date:** 2025-02-14

## Tech Debt

**Lack of Automated Tests:**
- Issue: No unit or integration tests for core Python logic and synchronization scripts.
- Files: `src/get_research_done/installer.py`, `scripts/sync_skill_boilerplate.py`, `scripts/sync_codex_wrappers.py`, `scripts/sync_agy_wrappers.py`
- Why: Focus on rapid prototyping of research skills and templates.
- Impact: High risk of regressions when modifying installation logic or skill synchronization. Hard to verify the correctness of path resolution and file transformations.
- Fix approach: Implement a test suite using `pytest`. Add unit tests for `installer.py` using `unittest.mock` to simulate file system operations. Add integration tests that verify the full installation and synchronization cycle.

**Destructive Synchronization Pattern:**
- Issue: Synchronization scripts delete the entire target directory before regenerating it.
- Files: `scripts/sync_codex_wrappers.py`, `scripts/sync_agy_wrappers.py`
- Why: Simplicity of ensuring the target state matches the source of truth exactly.
- Impact: Any manual changes or accidental file additions in `codex/` or `agy/` directories are permanently lost during synchronization.
- Fix approach: Modify scripts to use a more surgical update approach (e.g., syncing only changed files) or add a warning/prompt if untracked changes are detected.

## Known Bugs

**None detected.**
- Symptoms: No active bugs identified during initial codebase mapping.
- Trigger: N/A
- Workaround: N/A

## Security Considerations

**Unchecked File System Operations:**
- Risk: Installer and sync scripts perform recursive copies and deletions without explicit checks for symlink attacks or restricted path access.
- Files: `src/get_research_done/installer.py`, `scripts/install.sh`, `scripts/sync_skill_boilerplate.py`
- Current mitigation: Standard library `shutil` and `cp -R` usage.
- Recommendations: Add checks to ensure that destination paths are within expected boundaries. Use safer file operation patterns to avoid race conditions.

## Performance Bottlenecks

**None detected.**
- Problem: The codebase primarily consists of static templates and lightweight file-moving scripts.
- Measurement: N/A
- Cause: N/A
- Improvement path: N/A

## Fragile Areas

**Skill File Build Dependency:**
- Why fragile: `SKILL.md` is a generated file that depends on `SKILL.src.md` and `skills/_shared/BASE.md`. If `SKILL.md` is edited directly, changes are lost on the next sync.
- Common failures: Developers modifying `SKILL.md` directly instead of the source files.
- Safe modification: Always edit `SKILL.src.md` or `_shared/BASE.md`, then run `make sync-skills`.
- Test coverage: 0% - No automated check to ensure files are in sync beyond manual `make check-skills`.

**Installer Path Resolution:**
- Why fragile: `installer.py` uses relative path lookups from `__file__` to find assets when not running as a package.
- Files: `src/get_research_done/installer.py` (line ~135)
- Common failures: Failure to locate assets if the script is invoked from an unexpected location or if the directory structure changes.
- Safe modification: Ensure the repository structure remains consistent with the assumed `parents[2]` logic.
- Test coverage: 0%

## Scaling Limits

**Local Filesystem Only:**
- Current capacity: Limited by local disk space and filesystem performance.
- Limit: N/A - The project is designed for local repository use.
- Symptoms at limit: N/A
- Scaling path: N/A

## Dependencies at Risk

**None detected.**
- Risk: Minimal external dependencies (`hatchling` for building).
- Impact: Low
- Migration plan: N/A

## Missing Critical Features

**Skill Versioning:**
- Problem: Individual research skills do not have version metadata.
- Current workaround: Relying on git commit history.
- Blocks: Difficult to track compatibility between specific skill versions and the research pipeline.
- Implementation complexity: Low - Add version fields to skill frontmatter.

**Undo/Rollback for Installer:**
- Problem: No automated way to undo an installation or revert to a previous state if an install fails halfway.
- Current workaround: Manual deletion or use of `grd-uninstall`.
- Blocks: Hard to recover from partial installations.
- Implementation complexity: Medium - Implement a transaction-like log of file operations.

## Test Coverage Gaps

**Core Installer and CLI:**
- What's not tested: All logic in `src/get_research_done/`
- Files: `src/get_research_done/installer.py`, `src/get_research_done/cli.py`, `src/get_research_done/uninstall_cli.py`
- Risk: Silent failures during installation or uninstallation in certain environments.
- Priority: High

**Skill Synchronization Scripts:**
- What's not tested: Markdown transformation and block insertion logic.
- Files: `scripts/sync_skill_boilerplate.py`, `scripts/sync_codex_wrappers.py`, `scripts/sync_agy_wrappers.py`
- Risk: Incorrectly rendered skill files providing misleading instructions to agents.
- Priority: Medium

---

*Concerns audit: 2025-02-14*
