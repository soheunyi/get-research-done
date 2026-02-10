# Testing Patterns

**Analysis Date:** 2026-02-10

## Project Context

This project does not have automated testing infrastructure. It is a documentation and workflow framework for AI-assisted research, not a traditional application. Testing occurs through manual verification, skill execution walkthroughs, and boilerplate synchronization checks.

## Manual Testing & Validation Approach

**Validation Mechanisms:**

The project uses manual verification patterns rather than automated test suites:

1. **Boilerplate Sync Validation** (`sync_skill_boilerplate.py --check`)
   - Verifies all skill files match canonical `COMMON_BLOCKS.md` definitions
   - Non-destructive: reports out-of-sync files without modifying them
   - Used in CI to enforce boilerplate consistency

2. **Makefile Targets:**
   - `make check-skills`: Validates without changes (CI/pre-commit safe)
   - `make sync-skills`: Applies synchronization fixes locally
   - Provides fast feedback loop for boilerplate correctness

## Verification Protocol

**Skill Execution Validation:**

Each skill defines explicit success criteria in its `<execution_contract>` and `<quality_bar>` sections. These are validated through:

1. **Intent Confirmation** (`<intent_lock>`)
   - User confirms intent before high-complexity actions
   - Prevents silent misunderstandings

2. **Verification Steps** (in `<output_format>`)
   - Every skill output includes "how to check it worked"
   - Verification is prescriptive, not optional
   - User-executable without special tools

3. **Risk Tiering** (`<action_policy>`)
   - LOW: summarize, plan, draft (no execution)
   - MED: code modification, test execution (user approval required)
   - HIGH: destructive operations (explicit approval + rollback plan)

4. **Quality Bar** (domain-specific)
   - Example from `grd-phase-researcher`: "Every major recommendation cites at least one high-confidence source"
   - Example from `grd-codebase-mapper`: "Every major claim cites concrete evidence (file path, command output, config)"

## Test File Organization

**Documentation Tests:**

Boilerplate sync is the only automated validation. Test patterns:

```bash
# Check mode (non-destructive, used in CI)
python3 scripts/sync_skill_boilerplate.py --check

# Fix mode (applies changes locally)
python3 scripts/sync_skill_boilerplate.py --fix

# Makefile shorthand
make check-skills
make sync-skills
```

**Expected Behaviors:**

Check passes when:
- All skill files contain `<context_budget>`, `<intent_lock>`, `<precision_contract>`, etc.
- Block content matches canonical definitions in `COMMON_BLOCKS.md`
- No out-of-sync differences detected

Check fails when:
- Missing blocks detected in any skill
- Block content differs from canonical version
- Regex pattern fails to find block boundaries

## Code Validation (Python)

**Validation Approach:**

The single Python utility (`sync_skill_boilerplate.py`) uses:

1. **Type Checking** (not automated, but present in code)
   - Modern Python 3.10+ type hints throughout
   - Example: `def load_common_blocks() -> dict[str, str]:`
   - Can be validated with tools like `mypy` but not automated in repo

2. **Early Validation**
   - `ValueError` raised immediately if blocks missing
   - File existence checked at module load (`COMMON_BLOCKS = REPO_ROOT / ...`)
   - Regex patterns validated during block loading

3. **Path Safety**
   - Uses `pathlib.Path` for cross-platform compatibility
   - Prevents path traversal with `SKILLS_ROOT.glob("*/SKILL.md")`
   - Filters out system artifacts (`if "__MACOSX" in path.parts`)

## No Test Framework

**Why:**

- Project is documentation-focused, not application code
- Skills are prompts/guidance for AI assistants, not executable code
- Validation occurs through:
  - Manual skill execution and user feedback
  - Boilerplate synchronization checks (automated)
  - Document structure validation (regex pattern matching)

## Boilerplate Sync Verification Details

**Sync Algorithm** (from `sync_skill_boilerplate.py`):

```python
def check_file(path: Path, blocks: dict[str, str]) -> bool:
    """Check if file would be modified by sync."""
    original = path.read_text(encoding="utf-8")
    candidate = apply_blocks(original, blocks)
    return candidate != original

def apply_blocks(text: str, blocks: dict[str, str]) -> str:
    """Apply blocks: replace existing or insert missing."""
    updated = text
    missing: list[str] = []

    for tag in TAGS:
        pattern = re.compile(rf"(?s)<{tag}>\n.*?\n</{tag}>")
        match = pattern.search(updated)
        if match:
            # Replace existing block
            updated = pattern.sub(blocks[tag], updated, count=1)
        else:
            # Mark for insertion
            missing.append(tag)

    if missing:
        # Insert after clarification_rule or source_of_truth anchor
        idx = _find_insertion_index(updated)
        payload = "\n\n" + "\n\n".join(blocks[tag] for tag in missing)
        updated = updated[:idx] + payload + updated[idx:]

    return updated.rstrip("\n") + "\n"
```

**Coverage:**

Tags validated across all skills:
- `context_budget`
- `intent_lock`
- `precision_contract`
- `anti_enterprise`
- `delivery_rule`
- `output_format`
- `action_policy`

## Verification Checklist for New Skills

When adding a new skill to `codex/skills/{skill-name}/SKILL.md`:

1. **Structure**
   - Include YAML frontmatter (name, description)
   - Define `<role>` and `<philosophy>` sections
   - Include `<source_of_truth>` with output artifact paths

2. **Boilerplate Blocks** (will be synced automatically)
   - `<context_budget>` - exploration limits
   - `<intent_lock>` - user confirmation gates
   - `<precision_contract>` - paths and verification criteria
   - `<anti_enterprise>` - process exclusions
   - `<delivery_rule>` - when to write vs propose
   - `<output_format>` - 5-part response structure
   - `<action_policy>` - risk tier classification

3. **Validation**
   ```bash
   # Run check to ensure sync compliance
   python3 scripts/sync_skill_boilerplate.py --check

   # If out of sync, apply fix
   python3 scripts/sync_skill_boilerplate.py --fix
   ```

## Continuous Verification

**Pre-commit Hooks (Recommended):**

Not currently implemented, but alignment with this pattern:
```bash
# Check boilerplate before commit
make check-skills
```

**CI Pipeline (Recommended):**

Not currently implemented, but would use:
```bash
python3 scripts/sync_skill_boilerplate.py --check
```

Exit code 1 if out of sync, preventing merge of misaligned skills.

## Documentation Validation

**Quality Checks** (manual, per skill):

From `<quality_bar>` sections in skills:

1. **grd-phase-researcher**:
   - "Every major recommendation cites at least one high-confidence source"
   - "Ensure every major recommendation cites at least one high-confidence source"

2. **grd-codebase-mapper**:
   - "Every major claim cites concrete evidence (file path, command output, or config)"
   - "Separate 'Observed' from 'Inferred' from 'Proposed'"

3. **grd-algo-implementer**:
   - "Algorithm claims require executable tests or measurable checks"
   - "Correctness before optimization"

## Common Error Patterns & Detection

**Boilerplate Sync Issues:**

```
Error: Missing canonical block <context_budget> in COMMON_BLOCKS.md
→ Indicates COMMON_BLOCKS.md was corrupted or deleted

Error: Out-of-sync skill files
→ Indicates a skill was manually edited and diverged from canonical blocks
→ Run: python3 scripts/sync_skill_boilerplate.py --fix
```

**Regex Pattern Matching:**

Blocks must follow exact format:
```
<tag_name>
content here (multiline OK)
</tag_name>
```

Pattern: `(?s)<{tag}>\n.*?\n</{tag}>` (multiline, non-greedy)

Failure cases:
- Missing closing tag → block not found
- Extra whitespace before opening tag → pattern mismatch
- Tag name typo → skipped during sync

## Testing for Research Workflow Execution

**Pre-execution Checklist** (per `<output_format>`):

1. **Assumptions** - Have all unknowns been identified?
2. **Plan** - Are steps numbered and smallest-first?
3. **Proposed Changes** - Are artifacts named per `<source_of_truth>`?
4. **Verification Steps** - Can user execute without special tools?
5. **Risks** - Are failure modes and rollback plans documented?

**Skill-specific Success Criteria:**

Each skill's `<execution_contract>` defines what "done" means:

- `grd-hypothesis-designer`: "Write one falsifiable hypothesis with baseline, metric, effect size"
- `grd-experiment-planner`: "Define controls, seeds, dataset versions, split strategy"
- `grd-algo-implementer`: "Implement smallest-testable path first, then edge cases"

## Coverage Gaps

**Not Tested:**
- Actual skill execution (AI-driven, user feedback validates)
- Research outcome quality (domain expert review)
- Experiment reproducibility (user-verified in `.grd/research/` artifacts)
- End-to-end workflows (cross-skill integration)

**Why:**
- Skills are AI guidance documents, not executable code
- Research quality depends on user expertise and domain knowledge
- Workflow integration is user-driven, not automated

---

*Testing analysis: 2026-02-10*
