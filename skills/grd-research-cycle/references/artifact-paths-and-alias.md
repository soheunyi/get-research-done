# Artifact Paths and Latest Alias

When run context is active:
- ensure run-scoped artifact paths are used
- refresh latest alias:

```bash
mkdir -p .grd/research/runs
ln -sfn "runs/{run_id}" .grd/research/latest
```

Do not silently change preprocessing/splits/metric definitions.
