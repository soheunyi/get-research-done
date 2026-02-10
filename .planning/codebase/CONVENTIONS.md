# Coding Conventions

**Analysis Date:** 2026-02-10

## Project Context

This is a research workflow and skill documentation framework (not a traditional application codebase). Primary artifacts are Markdown documentation files defining research pipeline stages and AI assistant skills. Secondary artifact is a Python utility for synchronizing shared boilerplate across skill files.

## Naming Patterns

**Files:**
- Skill files: `SKILL.md` (singular, uppercase)
- Workflow files: `research-pipeline.md` (lowercase, hyphens)
- Research artifacts: `.grd/` prefix directory (e.g., `.grd/codebase/CURRENT.md`, `.grd/research/HYPOTHESIS.md`)
- Python scripts: lowercase with underscores (e.g., `sync_skill_boilerplate.py`)
- Templates: `research-notes.md`, `wandb-config.md` (lowercase, descriptive names)
- Shared blocks: `COMMON_BLOCKS.md` (uppercase, shared convention marker)

**Directories:**
- Skills: skill-name format using hyphens (e.g., `grd-codebase-mapper`, `grd-research-hypothesis-designer`)
- Skill groups: `codex/` vs `agy/` (Codex for Claude Code, Agy for Antigravity)
- Workflows: organized by platform under `workflows/` subdirectory
- Planning artifacts: `.planning/codebase/` for analysis outputs, `.grd/` for research phase outputs

## Markdown Structure Conventions

**Skill File Format:**
- YAML frontmatter header (name, description)
- `<role>` section defining AI persona and responsibility
- `<philosophy>` section establishing decision principles
- `<when_to_use>` section for context of applicability
- `<source_of_truth>` section identifying reference docs and output artifacts
- `<clarification_rule>` section for user interaction gating
- Standard blocks (via `COMMON_BLOCKS.md`):
  - `<context_budget>` - file reading and exploration limits
  - `<intent_lock>` - user intent confirmation before action
  - `<precision_contract>` - exact paths, steps, and verification criteria
  - `<anti_enterprise>` - exclusions for corporate process patterns
  - `<delivery_rule>` - when to write artifacts vs propose diffs
  - `<output_format>` - 5-part response structure (Assumptions, Plan, Proposed changes, Verification, Risks)
  - `<action_policy>` - risk tier classification (LOW/MED/HIGH) with approval gates
- `<execution_contract>` section with numbered execution steps
- `<quality_bar>` or similar domain-specific success criteria section (optional)

**Research Pipeline Stages:**
- Stage -1: Codebase Mapping (CURRENT.md, TARGET.md, GAPS.md)
- Stage 0: Research Notes (RESEARCH_NOTES.md)
- Stage 0.5: Phase Execution Research (phases/{phase_id}-RESEARCH.md)
- Stage 1: Hypothesis Design (HYPOTHESIS.md)
- Stage 1.5: Analysis Plan (ANALYSIS_PLAN.md)
- Stage 2: Experiment Plan (EXPERIMENT_PLAN.md)
- Stages 3-5: Evaluation, Ablation, Reproducibility artifacts

## Python Code Style

**File Organization:**
- Module docstring at top with usage examples
- Future imports first: `from __future__ import annotations`
- Standard library imports before third-party
- Type hints using modern syntax with `|` unions and forward references

**Naming Conventions:**
- Functions: snake_case (e.g., `load_common_blocks()`, `find_skill_files()`)
- Constants: UPPERCASE (e.g., `REPO_ROOT`, `TAGS`)
- Private functions: prefix with underscore (e.g., `_find_insertion_index()`)
- Type annotations: use modern Python 3.10+ syntax (`dict[str, str]` not `Dict[str, str]`)

**Function Design:**
- Single responsibility per function
- Clear parameter and return type hints
- No default mutable arguments
- Early returns for clarity (e.g., skip nested if-else)

**Example from `sync_skill_boilerplate.py`:**
```python
def load_common_blocks() -> dict[str, str]:
    """Load all common block definitions."""
    text = COMMON_BLOCKS.read_text(encoding="utf-8")
    blocks: dict[str, str] = {}
    for tag in TAGS:
        pattern = re.compile(rf"(?s)<{tag}>\n.*?\n</{tag}>")
        match = pattern.search(text)
        if not match:
            raise ValueError(f"Missing canonical block <{tag}> in {COMMON_BLOCKS}")
        blocks[tag] = match.group(0)
    return blocks
```

Key patterns:
- Explicit type annotations on return and local variables
- Early error detection with descriptive ValueError messages
- Use of `pathlib.Path` for filesystem operations
- `encoding="utf-8"` explicit on all file I/O

## Error Handling

**Patterns:**
- Raise `ValueError` with descriptive message for validation failures
- Use early returns to avoid nested conditionals
- Validate input before processing (e.g., check for missing blocks)
- Print status messages to stdout for CLI operations
- Return exit codes (0 for success, 1 for failure) from main functions

**Example:**
```python
if updated != original:
    path.write_text(updated, encoding="utf-8")
    return True
return False
```

## Logging & Output

**Approach:**
- No formal logging framework; use `print()` for stdout messages
- Status messages follow pattern: action summary then details
- List items prefixed with `-` for clarity

**Examples:**
```python
print("Out-of-sync skill files:")
for item in out_of_sync:
    print(f"- {item}")
print("All codex skill files are in sync.")
```

## Comments & Documentation

**When to Comment:**
- Docstrings required for all public functions and modules
- Use `"""` style docstrings with brief one-line summary
- Regex patterns benefit from inline explanation (see usage in `apply_blocks()`)
- Complex logic sections explained before code block
- No comments stating the obvious ("# increment counter")

**Format:**
```python
def apply_blocks(text: str, blocks: dict[str, str]) -> str:
    """Apply canonical blocks to skill file, replacing old or adding new."""
    updated = text
    missing: list[str] = []
```

## Imports Organization

**Order (as seen in `sync_skill_boilerplate.py`):**
1. Future imports: `from __future__ import annotations`
2. Standard library: `argparse`, `re`, `sys`, `pathlib`
3. No third-party dependencies (intentionally minimalist)

## Build & Automation

**Makefile Conventions:**
- `.PHONY` declarations for all non-file targets
- Variable placeholder: `PYTHON ?= python3` (allow override)
- Commands use `$(PYTHON)` for portability
- Targets follow action-noun format: `check-skills`, `sync-skills`

**Boilerplate Sync Pattern:**
- Single source of truth: `COMMON_BLOCKS.md`
- Run `sync_skill_boilerplate.py --fix` to update all skills
- Run `sync_skill_boilerplate.py --check` to validate without changes
- Makefile shortcuts: `make sync-skills`, `make check-skills`

## Markdown Link Conventions

**Reference Patterns:**
- Workflow references: `@GSD_ROOT@get-research-done/codex/workflows/research-pipeline.md`
- Skill references within skills use relative paths when possible
- Repository root anchor `@GSD_ROOT@` for absolute path stability

## Documentation Standards

**Quality Bar:**
- Every major skill section must state its purpose and when to use it
- Execution contracts should be numbered and ordered smallest-first
- Risk tiers (LOW/MED/HIGH) explicitly labeled for all actions
- Assumptions and unknowns stated before plans
- Verification steps defined before execution
- No vague directives; all guidance is prescriptive

**Skill Metadata:**
- Frontmatter: `name` (human-readable), `description` (one-liner)
- Role section: clarifies AI persona and responsibility scope
- Philosophy section: underlying principles and decision frameworks
- Source of truth: explicit output artifact paths

## Output Structure Pattern

All skills follow standardized 5-part response format:
1. Assumptions (bullet list; call out unknowns)
2. Plan (numbered; smallest-first)
3. Proposed changes / artifacts (write files only if explicitly requested)
4. Verification steps (how to check it worked)
5. Risks and failure modes (brief)

This format is shared via `COMMON_BLOCKS.md` and synchronized across all codex skills.

---

*Convention analysis: 2026-02-10*
