# Testing Patterns

**Analysis Date:** 2025-02-11

## Test Framework

**Runner:**
- **JavaScript (GSD Tools):** `node:test` (built-in Node.js runner)
- **Python:** No automated test runner detected in the current codebase (e.g., `pytest` or `unittest` are not present).

**Assertion Library:**
- **JavaScript:** `node:assert` (built-in Node.js assertion library)

**Run Commands:**
```bash
# JavaScript tests (from within .gemini/get-shit-done/bin/ or root)
node ./.gemini/get-shit-done/bin/gsd-tools.test.js
```

## Test File Organization

**Location:**
- JavaScript: Co-located with the source code in `.gemini/get-shit-done/bin/`.

**Naming:**
- `*.test.js` pattern (e.g., `gsd-tools.test.js`).

## Test Structure

**Suite Organization:**
```javascript
describe('command name', () => {
  let tmpDir;

  beforeEach(() => {
    tmpDir = createTempProject();
  });

  afterEach(() => {
    cleanup(tmpDir);
  });

  test('scenario description', () => {
    // execution and assertions
  });
});
```

**Patterns:**
- **Setup:** Uses `beforeEach` to create fresh temporary environments (e.g., `createTempProject`).
- **Teardown:** Uses `afterEach` to remove temporary files and directories (e.g., `cleanup`).
- **Assertion:** Uses `assert.strictEqual`, `assert.ok`, `assert.deepStrictEqual`.

## Mocking

**Framework:**
- No specialized mocking library used; relies on file system state manipulation.

**Patterns:**
- **System Calls:** Uses `child_process.execSync` to run the CLI tool in a sub-process, effectively performing integration/E2E testing.
- **File System:** Uses `fs.mkdtempSync` and `fs.writeFileSync` to create realistic file structures for the tools to operate on.

## Fixtures and Factories

**Test Data:**
```javascript
function createTempProject() {
  const tmpDir = fs.mkdtempSync(path.join(require('os').tmpdir(), 'gsd-test-'));
  fs.mkdirSync(path.join(tmpDir, '.planning', 'phases'), { recursive: true });
  return tmpDir;
}
```

**Location:**
- Fixture creation logic is typically embedded within the test file as helper functions.

## Coverage

**Requirements:**
- None enforced or detected.

## Test Types

**Integration Tests:**
- Primary test type for the GSD toolset. Tests CLI commands against real (but temporary) file structures.

**Unit Tests:**
- Not explicitly separated from integration tests in the current toolset.

## Common Patterns

**CLI Testing:**
```javascript
function runGsdTools(args, cwd = process.cwd()) {
  try {
    const result = execSync(`node "${TOOLS_PATH}" ${args}`, {
      cwd,
      encoding: 'utf-8',
      stdio: ['pipe', 'pipe', 'pipe'],
    });
    return { success: true, output: result.trim() };
  } catch (err) {
    return {
      success: false,
      output: err.stdout?.toString().trim() || '',
      error: err.stderr?.toString().trim() || err.message,
    };
  }
}
```

**Error Testing:**
- Tests verify that commands fail gracefully when files are missing or malformed (e.g., 'malformed SUMMARY.md skipped gracefully').

---

*Testing analysis: 2025-02-11*
