# Incident Logger Script Usage

Prefer script-based logging for deterministic incident capture.

## Script

- `scripts/log_incident_with_context.py`

## Default Behavior

- Reads local Codex session streams from `~/.codex/sessions/`.
- Captures recent chats with mixed user/assistant snippets.
- Appends structured incident entry to `.grd/SKILL_FEEDBACK_LOG.md`.

## Key Flags

- `--repo-root <repo-root>`
- `--skill-name <name>`
- `--priority high|medium|low`
- `--session-id <hash>|@current`
- `--snippets-per-chat <n>`
- `--snippet-max-len <n>`

## Example

```bash
python scripts/log_incident_with_context.py \
  --repo-root <repo-root> \
  --skill-name "grd-skill-reliability-keeper" \
  --priority high \
  --session-id @current \
  --snippets-per-chat 10 \
  --snippet-max-len 400 \
  --user-feedback-summary "Skill should have been called first." \
  --expected "Route immediately to reliability flow before normal orchestration." \
  --observed "Normal orchestration continued before incident handling." \
  --suspected-root-cause "Hard-trigger rule was missed at turn start." \
  --proposed-improvement "Add first-pass reliability gate." \
  --verification-status "Recorded with local chat context."
```

## Required Logged Fields

- date
- skill name
- user feedback summary
- expected behavior vs observed behavior
- suspected root cause
- proposed improvement
- priority
- verification follow-up status
