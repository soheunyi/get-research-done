# Bootstrap, Run Index, and Notes Contract

Use this file for `mode=kickoff` and cold-start situations.

## Cold-Start Rule

If `.grd/STATE.md` or `.grd/ROADMAP.md` is missing/empty, initialize through Stage -1 first.

Bootstrap sequence:
1. Ask one bootstrap question: existing codebase vs greenfield.
2. If existing codebase, route first to `Build Architect` for current/target/gap map.
3. Seed state from:
- `.grd/codebase/CURRENT.md`
- `.grd/codebase/TARGET.md`
- `.grd/codebase/GAPS.md`
4. Initialize `.grd/STATE.md` and `.grd/ROADMAP.md` using deterministic scaffolding.
5. Continue with normal routing only after bootstrap artifacts exist.

## Helper Script Contract

Preferred command:
```bash
python scripts/bootstrap_state.py --repo-root <repo-root> --init-templates --init-workflows [--run-id {run_id}] [--include-notes]
```

Options:
- `--init-templates`: scaffold `.grd/templates/*`
- `--init-workflows`: scaffold `.grd/workflows/research-pipeline.md`
- `--include-notes`: scaffold `.grd/research/RESEARCH_NOTES.md`
- `--force`: overwrite existing artifact files when explicitly intended
- `--template-root`: apply intentional skill-local overrides only

## Active Run Index and Alias

For active run context, ensure `.grd/research/runs/{run_id}/0_INDEX.md` exists and latest alias is updated.

Preferred command:
```bash
python scripts/bootstrap_state.py --repo-root <repo-root> --run-id {run_id}
```

Fallback if helper script is unavailable:
```bash
mkdir -p .grd/research/runs
ln -sfn "runs/{run_id}" .grd/research/latest
```

## Notes Append Requirement

After checkpoint/kickoff updates, append a compact activity entry to `.grd/research/RESEARCH_NOTES.md`.
Use timestamp rules from `references/checkpoint-ops.md` when including time-specific headers.
