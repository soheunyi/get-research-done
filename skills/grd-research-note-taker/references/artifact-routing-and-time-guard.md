# Artifact Routing and Timestamp Guard

Default path:
- `.grd/research/<topic_or_run>/NOTES.md`

Resolution:
- if `run_id` exists, use `runs/{run_id}`
- otherwise use `<topic_slug>`

Optional mirror:
- `.grd/research/RESEARCH_NOTES.md`

Timestamp rule for time-specific headers:
- fetch exact local system time immediately before write
- otherwise use date-only `YYYY-MM-DD`
- do not infer time from conversation flow
