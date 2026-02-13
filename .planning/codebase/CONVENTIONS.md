# Coding Conventions

**Analysis Date:** 2025-02-11

## Naming Patterns

**Files:**
- `snake_case.py` for Python source files (e.g., `src/get_research_done/installer.py`)
- `kebab-case.js` for JavaScript files in the GSD toolset (e.g., `.gemini/get-shit-done/bin/gsd-tools.js`)
- `*.test.js` for JavaScript test files (e.g., `.gemini/get-shit-done/bin/gsd-tools.test.js`)

**Functions:**
- `snake_case` for Python functions (e.g., `install_targets`)
- `camelCase` for JavaScript functions
- `_prefix` for private or internal helper functions in Python (e.g., `_copy_tree_contents`)

**Variables:**
- `snake_case` for Python variables
- `camelCase` for JavaScript variables
- `UPPER_SNAKE_CASE` for global constants (e.g., `SKILL_TARGET_DIRS`)

**Types:**
- `PascalCase` for Python classes and dataclasses (e.g., `InstallResult`)
- Type hints are used consistently in Python (e.g., `dest: str | Path`)

## Code Style

**Formatting:**
- Python: Follows PEP 8. Consistently formatted with balanced whitespace, likely using `black`.
- JavaScript: Consistent use of 2-space indentation and single quotes.

**Linting:**
- Not explicitly configured in `pyproject.toml`, but code maintains high consistency.

## Import Organization

**Order (Python):**
1. Future imports (`from __future__ import annotations`)
2. Standard library imports (e.g., `import shutil`, `from pathlib import Path`)
3. Third-party/Local imports (e.g., `from .installer import ...`)

**Grouping:**
- Blank lines between groups of imports.
- Alphabetical sorting within groups.

## Error Handling

**Patterns:**
- Python: Use `try...except` at entry points to catch and report user-facing errors.
- Input validation: Throw `ValueError` for invalid targets or configuration (e.g., in `_normalize_targets`).
- JavaScript: Use `try...catch` for system operations like `execSync`.

## Logging

**Framework:**
- Python: `print()` used for CLI output (standard and error messages).
- JavaScript: `console.log` for tool output.

## Comments

**When to Comment:**
- Use comments for high-level module descriptions (e.g., `/** GSD Tools Tests */` in JS).
- Python code is largely self-documenting with descriptive names and type hints.

**JSDoc/TSDoc:**
- Minimal use of JSDoc in JavaScript toolset.

## Function Design

**Size:**
- Python functions are modular and focused, generally under 50 lines.

**Parameters:**
- Use of type hints for all parameters and return values.
- Dataclasses used for complex return structures (e.g., `InstallResult`).

**Return Values:**
- Explicit return types in Python (`-> None`, `-> int`, etc.).
- Use of `sys.exit(main())` pattern for CLI entry points.

## Module Design

**Exports:**
- Python: Functions intended for external use are imported in `__init__.py` or kept public.
- Helper functions are kept private with `_` prefix.

---

*Convention analysis: 2025-02-11*
