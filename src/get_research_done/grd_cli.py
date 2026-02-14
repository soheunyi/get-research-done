from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

from .state import MODES, ResearchState, StateContractError, load_context


def _find_bootstrap_script(repo_root: Path) -> Path | None:
    candidates = (
        repo_root / "skills" / "grd-state-keeper" / "scripts" / "bootstrap_state.py",
        Path(__file__).resolve().parents[2] / "skills" / "grd-state-keeper" / "scripts" / "bootstrap_state.py",
        Path(__file__).resolve().parent / "assets" / "skills" / "grd-state-keeper" / "scripts" / "bootstrap_state.py",
    )
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def _bootstrap_if_missing(repo_root: Path) -> None:
    state_paths = [repo_root / ".grd" / "STATE.md", repo_root / ".grd" / "state.md"]
    roadmap_paths = [repo_root / ".grd" / "ROADMAP.md", repo_root / ".grd" / "roadmap.md"]
    if any(path.exists() for path in state_paths) and any(path.exists() for path in roadmap_paths):
        return
    script = _find_bootstrap_script(repo_root)
    if script is None:
        raise FileNotFoundError(
            "State files are missing and bootstrap script was not found. "
            "Run `grd-state-keeper mode=kickoff` to initialize `.grd/`."
        )
    subprocess.run(
        [sys.executable, str(script), "--repo-root", str(repo_root), "--init-templates", "--init-workflows"],
        check=True,
        capture_output=True,
        text=True,
    )


def _count_entries(path: Path) -> int:
    if not path.exists():
        return 0
    text = path.read_text(encoding="utf-8")
    return sum(1 for line in text.splitlines() if line.startswith("## "))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="grd", description="GRD runtime CLI.")
    parser.add_argument("--repo-root", default=".", help="Repository root containing `.grd/`.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    info = subparsers.add_parser("info", help="Render current GRD state digest.")
    info.add_argument("--json", action="store_true", help="Emit JSON payload.")
    info.add_argument("--max-chars", type=int, default=2400, help="Maximum markdown digest size.")

    run = subparsers.add_parser("run", help="Prepare a state-enriched payload for a skill.")
    run.add_argument("--skill", required=True, help="Skill identifier for payload metadata.")
    run.add_argument("--json", action="store_true", help="Emit JSON payload.")
    run.add_argument("--max-chars", type=int, default=2400, help="Maximum markdown digest size.")

    log = subparsers.add_parser("log", help="Record lightweight exploration findings.")
    log.add_argument("--what", required=True, help="What you tried.")
    log.add_argument("--happened", required=True, help="What happened.")
    log.add_argument("--why", required=True, help="Why this was done.")
    log.add_argument("--outcome", help="Optional experiment outcome.")
    log.add_argument("--artifact", action="append", default=[], help="Optional artifact path (repeatable).")
    log.add_argument("--source", help="Optional source context.")
    log.add_argument("--notes", help="Optional notes.")
    log.add_argument("--json", action="store_true", help="Emit JSON payload.")

    promote = subparsers.add_parser("promote", help="Promote evidence into a formal hypothesis artifact.")
    promote.add_argument("--title", required=True, help="Hypothesis title.")
    promote.add_argument("--what", required=True, help="What was attempted.")
    promote.add_argument("--happened", required=True, help="Observed result.")
    promote.add_argument("--why", required=True, help="Reasoning behind promotion.")
    promote.add_argument("--source-entry", help="Optional source entry id/timestamp.")
    promote.add_argument("--artifact", action="append", default=[], help="Supporting artifact path.")
    promote.add_argument("--notes", help="Optional notes.")
    promote.add_argument("--tag", action="append", default=[], help="Optional tag (repeatable).")
    promote.add_argument("--json", action="store_true", help="Emit JSON payload.")

    nxt = subparsers.add_parser("next", help="Suggest next actions from current state.")
    nxt.add_argument("--mode", choices=MODES, help="Mode hint: explore/plan/implement/evaluate/synthesize/promote.")
    nxt.add_argument("--max-actions", type=int, default=3, help="Maximum actions to suggest.")
    nxt.add_argument("--json", action="store_true", help="Emit JSON payload.")

    return parser


def _emit_info(repo_root: Path, as_json: bool, max_chars: int) -> int:
    _bootstrap_if_missing(repo_root)
    context = load_context(repo_root)
    if as_json:
        print(json.dumps(context.to_dict(include_markdown=True, max_chars=max_chars), indent=2))
    else:
        print(context.to_markdown(max_chars=max_chars), end="")
    return 0


def _emit_run(repo_root: Path, skill: str, as_json: bool, max_chars: int) -> int:
    _bootstrap_if_missing(repo_root)
    context = load_context(repo_root)
    if as_json:
        print(
            json.dumps(
                {
                    "mode": "payload-only",
                    "skill": skill,
                    "context": context.to_dict(include_markdown=True, max_chars=max_chars),
                },
                indent=2,
            )
        )
    else:
        print("# GRD Skill Payload\n")
        print(f"- Skill: {skill}")
        print("- Mode: payload-only\n")
        print(context.to_markdown(max_chars=max_chars), end="")
    return 0


def _emit_log(
    repo_root: Path,
    what: str,
    happened: str,
    why: str,
    outcome: str | None,
    artifacts: list[str],
    source: str | None,
    notes: str | None,
    as_json: bool,
) -> int:
    _bootstrap_if_missing(repo_root)
    rs = ResearchState(root_dir=repo_root)
    journal_entry: dict[str, object] = {"what": what, "happened": happened, "why": why}
    if source:
        journal_entry["source"] = source
    if notes:
        journal_entry["notes"] = notes
    rs.append_journal(journal_entry)

    experiment_payload: dict[str, object] | None = None
    if outcome:
        experiment_payload = dict(journal_entry)
        experiment_payload["outcome"] = outcome
        if artifacts:
            experiment_payload["artifacts"] = artifacts
        rs.append_experiment(experiment_payload)

    if as_json:
        print(
            json.dumps(
                {"status": "ok", "command": "log", "journal": journal_entry, "experiment": experiment_payload},
                indent=2,
            )
        )
    else:
        dest = f"journal: {rs.journal_path}"
        if outcome:
            dest += f", experiments: {rs.experiments_path}"
        print(f"Logged exploration entry -> {dest}")
    return 0


def _emit_promote(
    repo_root: Path,
    title: str,
    what: str,
    happened: str,
    why: str,
    source_entry: str | None,
    artifacts: list[str],
    notes: str | None,
    tags: list[str],
    as_json: bool,
) -> int:
    _bootstrap_if_missing(repo_root)
    rs = ResearchState(root_dir=repo_root)
    payload: dict[str, object] = {"title": title, "what": what, "happened": happened, "why": why}
    if source_entry:
        payload["source_entry"] = source_entry
    if artifacts:
        payload["artifacts"] = artifacts
    if notes:
        payload["notes"] = notes
    if tags:
        payload["tags"] = tags

    record = rs.promote_hypothesis(payload)
    if as_json:
        print(json.dumps({"status": "ok", "command": "promote", "hypothesis": record}, indent=2))
    else:
        print(rs.render_hypothesis_view(record))
    return 0


def _infer_mode(journal_entries: int, experiment_entries: int, hypothesis_entries: int) -> str:
    if journal_entries == 0:
        return "explore"
    if journal_entries > experiment_entries + 1:
        return "evaluate"
    if hypothesis_entries == 0:
        return "promote"
    return "synthesize"


def _mode_actions(mode: str, rs: ResearchState) -> list[str]:
    if mode == "explore":
        return [
            "Capture one fast observation with `grd log --what ... --happened ... --why ...`.",
            "Add outcome evidence with `grd log --outcome ...` if you ran an experiment.",
            "Run `grd next --mode evaluate` once you have 2+ entries.",
        ]
    if mode == "plan":
        return [
            "Pick one concrete experiment objective and convert it to a hypothesis title.",
            "Use `grd promote --title ... --what ... --happened ... --why ...` for the strongest candidate.",
            "Record expected validation criteria in the hypothesis notes.",
        ]
    if mode == "implement":
        return [
            "Execute only the smallest runnable change for the current experiment.",
            "Log observed behavior immediately after the run with `grd log`.",
            "If behavior diverges, switch to `grd next --mode evaluate`.",
        ]
    if mode == "evaluate":
        return [
            "Compare recent journal vs experiment entries to detect evidence gaps.",
            "Promote only entries with clear `what/happened/why` signal.",
            "Use `grd next --mode synthesize` to prepare a short decision summary.",
        ]
    if mode == "synthesize":
        return [
            "Summarize latest promoted hypothesis and decide continue/pivot/stop.",
            "Record one explicit decision note in your next `grd log` entry.",
            "Switch to `grd next --mode plan` for the next focused iteration.",
        ]
    return [
        "Promote your strongest recent insight with `grd promote --title ... --what ... --happened ... --why ...`.",
        "Check artifact consistency in `.grd/hypotheses/` and update tags if needed.",
        "Use `grd next --mode evaluate` after promotion.",
    ]


def _emit_next(repo_root: Path, mode: str | None, max_actions: int, as_json: bool) -> int:
    _bootstrap_if_missing(repo_root)
    rs = ResearchState(root_dir=repo_root)
    journal_entries = _count_entries(rs.journal_path)
    experiment_entries = _count_entries(rs.experiments_path)
    hypothesis_entries = len(list(rs.hypotheses_dir.glob("*.md"))) if rs.hypotheses_dir.exists() else 0

    selected_mode = mode or _infer_mode(journal_entries, experiment_entries, hypothesis_entries)
    actions = _mode_actions(selected_mode, rs)[: max(1, max_actions)]

    payload = {
        "status": "ok",
        "command": "next",
        "mode": selected_mode,
        "metrics": {
            "journal_entries": journal_entries,
            "experiment_entries": experiment_entries,
            "hypothesis_entries": hypothesis_entries,
        },
        "actions": actions,
    }

    if as_json:
        print(json.dumps(payload, indent=2))
    else:
        print(f"Next mode: {selected_mode}")
        for i, action in enumerate(actions, start=1):
            print(f"{i}. {action}")
    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    repo_root = Path(args.repo_root).expanduser().resolve()

    try:
        if args.command == "info":
            return _emit_info(repo_root, args.json, args.max_chars)
        if args.command == "run":
            return _emit_run(repo_root, args.skill, args.json, args.max_chars)
        if args.command == "log":
            return _emit_log(
                repo_root,
                args.what,
                args.happened,
                args.why,
                args.outcome,
                args.artifact,
                args.source,
                args.notes,
                args.json,
            )
        if args.command == "promote":
            return _emit_promote(
                repo_root,
                args.title,
                args.what,
                args.happened,
                args.why,
                args.source_entry,
                args.artifact,
                args.notes,
                args.tag,
                args.json,
            )
        if args.command == "next":
            return _emit_next(repo_root, args.mode, args.max_actions, args.json)
        parser.error(f"Unknown command: {args.command}")
        return 2
    except (FileNotFoundError, StateContractError, subprocess.CalledProcessError) as exc:
        print(str(exc), file=sys.stderr)
        print("If state is missing/corrupt, run `grd-state-keeper mode=kickoff`.", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
