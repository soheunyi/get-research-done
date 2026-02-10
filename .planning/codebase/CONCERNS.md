# Codebase Concerns

**Analysis Date:** 2026-02-10

## Tech Debt

**Boilerplate Synchronization Mechanism:**
- Issue: Shared skill boilerplate requires manual synchronization across 12+ Codex skill files
- Files: `scripts/sync_skill_boilerplate.py`, `codex/skills/_shared/COMMON_BLOCKS.md`, all `codex/skills/grd-*/SKILL.md`
- Impact: Risk of skill files drifting from canonical boilerplate blocks; new blocks added to COMMON_BLOCKS.md only sync after running `make sync-skills`
- Current state: Sync script verifies and applies 7 standard blocks (`context_budget`, `intent_lock`, `precision_contract`, `anti_enterprise`, `delivery_rule`, `output_format`, `action_policy`)
- Fix approach: Automate synchronization check in CI/CD, or generate skill files from templates rather than maintaining duplicated boilerplate

**Uncommitted New Skills:**
- Issue: Two new skills are untracked in git (untracked status `??`)
- Files: `codex/skills/grd-codebase-mapper/SKILL.md`, `codex/skills/grd-phase-researcher/SKILL.md`
- Impact: Skills exist and are referenced in README.md but not version-controlled; risk of loss if working directory is cleaned
- Current state: Both files are complete with all required boilerplate sections
- Fix approach: Commit these skills to main branch with appropriate commit message

**Pending Modifications to Multiple Skills:**
- Issue: 12 Codex skill files have staged modifications that have not been committed
- Files: All modified files listed in `git status --short`
- Impact: Cannot determine if changes are intentional refactoring or incomplete work; unclear review/merge status
- Current state: Recent commits show consolidation work (merge stability/ops skills, add boilerplate, add new skills)
- Fix approach: Review diffs, finalize changes, and commit with clear messages; or revert if changes are exploratory

## Known Issues

**Skill File Size Inconsistency:**
- Symptoms: Two newly created Codex skills are significantly larger than existing skills
  - `grd-codebase-mapper`: 139 lines
  - `grd-phase-researcher`: 203 lines
  - Other Codex skills: 107-120 lines (avg ~111 lines)
- Files: `codex/skills/grd-codebase-mapper/SKILL.md`, `codex/skills/grd-phase-researcher/SKILL.md`
- Cause: New skills include additional context sections (`upstream_input`, `downstream_consumer`, `when_to_use` with more detail) not present in other skills
- Workaround: Both skills are fully functional despite size difference; potential for boilerplate normalization
- Risk: If new sections become standard, all existing skills need updating via sync script

**Boilerplate Change Not Yet Synchronized:**
- Symptoms: `anti_enterprise` block was added to COMMON_BLOCKS.md but sync check shows "All codex skill files are in sync"
- Files: `codex/skills/_shared/COMMON_BLOCKS.md`, all `codex/skills/grd-*/SKILL.md`
- Cause: Scripts run before changes were staged; or changes were made but sync hasn't been run yet
- Current state: `anti_enterprise` block now appears in all modified skill files (verified present in grd-algo-implementer, grd-build-architect, etc.)
- Resolution: Either sync was already run and files are in sync, or pending commit will bring them into sync

## Dependencies at Risk

**Python Script Maintenance:**
- Risk: `sync_skill_boilerplate.py` is a critical operational script but has no error recovery or logging
- Files: `scripts/sync_skill_boilerplate.py`, uses `load_common_blocks()` with `ValueError` on missing blocks
- Impact: If COMMON_BLOCKS.md structure changes unexpectedly, all skills could fail to sync
- Current mitigation: Script validates against expected tags on startup; `--check` mode allows validation before applying changes
- Migration plan: Add logging output, unit tests for regex patterns, and pre-flight validation for file encoding

**Cross-Repo Installation:**
- Risk: Installation scripts exist but are not tested in CI/CD
- Files: `scripts/install.sh`, `scripts/install.ps1` (referenced in README.md)
- Impact: Shell/PowerShell scripts for copying skills to external repos have unknown compatibility; breaking changes to file paths could break downstream installations
- Current mitigation: Installation documented in README.md; scripts support both Linux/macOS (bash) and Windows (PowerShell)
- Migration plan: Add integration tests for installation to sample projects, document version compatibility

## Scaling Limits

**Boilerplate Sync Linear Growth:**
- Current capacity: 12 Codex skills + potential future skills
- Limit: Synchronization becomes increasingly fragile as skill count grows; regex-based block replacement could fail with edge cases
- Scaling path: Consider template-based skill generation or database-driven boilerplate instead of file scanning and regex substitution

**Directory Naming Convention Inconsistency:**
- Issue: Codex skills use `grd-` prefix (GSD Research Done), but Antigravity skills use `research-` prefix
- Files: `agy/skills/research-*` vs `codex/skills/grd-*`
- Impact: Creates two naming conventions across the codebase; confusing for users deciding where to find skills
- Scaling concern: As more skills are added, naming inconsistency will become more pronounced

## Documentation Gaps

**Missing Installation Verification:**
- Problem: Installation scripts exist but README lacks verification steps to confirm successful installation
- Files: `README.md` documents installation but doesn't provide post-install checks
- Risk: Users may not realize installation failed silently, leading to missing skills

**Missing CI/CD Configuration:**
- Problem: Boilerplate sync script exists but is not integrated into any CI/CD pipeline
- Files: `scripts/sync_skill_boilerplate.py`, `Makefile` with targets but no CI hooks
- Risk: Pull requests can introduce skill file drift without detection

**Incomplete Changelog:**
- Problem: Recent commits show major changes (consolidation, skill additions) but no CHANGELOG.md or release notes
- Risk: Users cannot easily understand what changed between versions or when their installation becomes outdated

## Test Coverage Gaps

**Untested Boilerplate Sync:**
- What's not tested: `sync_skill_boilerplate.py` regex patterns, file I/O, insertion point calculation
- Files: `scripts/sync_skill_boilerplate.py` (no test suite exists)
- Risk: Changes to COMMON_BLOCKS.md block structure could corrupt skill files without detection
- Priority: High - this is a production-critical script

**Untested Installation Scripts:**
- What's not tested: `scripts/install.sh` and `scripts/install.ps1` behavior on various OS/shell combinations
- Risk: Breaking changes to directory structure could silently fail to copy files
- Priority: High - affects all downstream users

**No Integration Tests:**
- What's not tested: End-to-end skill installation and functionality in target repositories
- Risk: Unknown until user runs installation and finds skills missing or misconfigured
- Priority: Medium - could be caught earlier with CI

## Performance Bottlenecks

**Boilerplate Sync Sequential Processing:**
- Problem: `find_skill_files()` reads all skill files and applies all 7 blocks sequentially using regex substitution
- Files: `scripts/sync_skill_boilerplate.py` lines 43-50, 61-78
- Cause: No batching or parallel processing
- Impact: Scales linearly with skill file count; regex operations on large files could become slow
- Improvement path: Batch file operations, use compiled regex patterns, consider incremental updates

**No Caching of Common Blocks:**
- Problem: `load_common_blocks()` re-reads and re-parses COMMON_BLOCKS.md on every sync operation
- Files: `scripts/sync_skill_boilerplate.py` line 32
- Impact: Unnecessary I/O and regex parsing for every skill sync
- Improvement path: Cache blocks in memory during batch operations

## Fragile Areas

**Boilerplate Block Boundary Detection:**
- Files: `scripts/sync_skill_boilerplate.py` lines 35, 54-58
- Why fragile: Uses regex patterns to find insertion point and block boundaries; sensitive to whitespace and tag structure
- Safe modification: Document exact formatting requirements for `<tag>` blocks; add validation; use XML/YAML parsers instead of regex
- Test coverage: No unit tests for regex patterns or insertion logic

**Skill File Structure Assumptions:**
- Files: All `codex/skills/grd-*/SKILL.md` files
- Why fragile: Every skill file must follow exact structure with `<role>`, `<when_to_use>`, `<source_of_truth>` and shared blocks; deviation breaks sync
- Safe modification: Validate skill structure in pre-commit hooks; fail early with clear error messages
- Test coverage: Manual verification only; no schema validation

**Installation Path Hardcoding:**
- Files: `README.md` lines 34-48 show bash/PowerShell commands with hardcoded paths
- Why fragile: Users must manually copy commands and substitute paths; typos in paths lead to incomplete installation
- Safe modification: Create dedicated `install.sh` wrapper that validates target directory, validates all files copied correctly
- Test coverage: Installation not tested; no automated verification

## Security Considerations

**No Access Control on Installation Scripts:**
- Risk: `scripts/install.sh` and `scripts/install.ps1` are executable and can be run without validation
- Files: `scripts/install.sh`, `scripts/install.ps1`
- Current mitigation: Scripts documented in README; users must explicitly copy to target repo
- Recommendations: Add pre-flight checks in installation scripts to validate target directory; document required permissions

**No Integrity Checks:**
- Risk: No checksums or signatures for skill files; no verification that copied files match source
- Files: All `codex/skills/grd-*/SKILL.md` files
- Impact: File corruption during transfer could go undetected
- Recommendations: Add SHA256 checksums to installation scripts; verify after copying

**Installation Script Permissions:**
- Risk: Shell and PowerShell scripts could inadvertently run with elevated privileges
- Current mitigation: Scripts are read-only; installation uses user-level directory paths
- Recommendations: Document that scripts should never be run with `sudo` or elevated PowerShell

## Missing Critical Features

**No Skill Versioning:**
- Problem: Skills are copied directly without version information; no way to determine installed skill version
- Blocks: Cannot support multiple versions of skills simultaneously; breaking changes force all users to update

**No Dependency Management for Skills:**
- Problem: Skills reference each other and external documents but dependencies are not explicitly declared
- Blocks: Cannot auto-validate that all dependencies are present after installation; cross-skill imports could break

**No Skill Metadata Registry:**
- Problem: Skills exist as individual files; no central registry of available skills, versions, or compatibility
- Blocks: Users cannot discover skills programmatically; installation tooling cannot verify completeness

---

*Concerns audit: 2026-02-10*
