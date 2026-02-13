from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

from .state import ResearchState, StateContractError, load_context


def _find_bootstrap_script(repo_root: Path) -> Path | None:
    candidates = (
        repo_root / "skills" / "grd-state-keeper" / "scripts" / "bootstrap_state.py",
        Path(__file__).resolve().parents[2]
        / "skills"
        / "grd-state-keeper"
        / "scripts"
        / "bootstrap_state.py",
        Path(__file__).resolve().parent
        / "assets"
        / "skills"
        / "grd-state-keeper"
        / "scripts"
        / "bootstrap_state.py",
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

    command = [
        sys.executable,
        str(script),
        "--repo-root",
        str(repo_root),
        "--init-templates",
        "--init-workflows",
    ]
    subprocess.run(command, check=True, capture_output=True, text=True)


def _count_markdown_sections(path: Path) -> int:
    if not path.exists():
        return 0
    text = path.read_text(encoding="utf-8")
    return sum(1 for line in text.splitlines() if line.startswith("## "))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="grd",
        description="GRD runtime CLI for state-aware context payload generation.",
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root containing `.grd/` (default: current directory).",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    info = subparsers.add_parser(
        "info",
        help="Render current GRD state digest.",
    )
    info.add_argument("--json", action="store_true", help="Emit JSON payload.")
    info.add_argument(
        "--max-chars",
        type=int,
        default=2400,
        help="Maximum markdown digest size (default: 2400).",
    )

    run = subparsers.add_parser(
        "run",
        help="Prepare a state-enriched context payload for a skill.",
    )
    run.add_argument("--skill", required=True, help="Skill identifier for payload metadata.")
    run.add_argument("--json", action="store_true", help="Emit JSON payload.")
    run.add_argument(
        "--max-chars",
        type=int,
        default=2400,
        help="Maximum markdown digest size (default: 2400).",
    )

    log = subparsers.add_parser(
        "log",
        help="Record lightweight exploration findings.",
    )
    log.add_argument("--what", required=True, help="What you tried.")
    log.add_argument("--happened", required=True, help="What happened.")
    log.add_argument("--why", required=True, help="Why this was done.")
    log.add_argument("--outcome", help="Optional experiment outcome.")
    log.add_argument(
        "--artifact",
        action="append",
        default=[],
        help="Optional artifact path to associate with the log (repeatable).",
    )
    log.add_argument("--source", help="Optional source context for this entry.")
    log.add_argument("--notes", help="Optional notes for richer context.")
    log.add_argument("--json", action="store_true", help="Emit JSON payload.")

    promote = subparsers.add_parser(
        "promote",
        help="Promote exploration evidence into a formal hypothesis artifact.",
    )
    promote.add_argument("--title", required=True, help="Hypothesis title.")
    promote.add_argument("--what", required=True, help="What was attempted.")
    promote.add_argument("--happened", required=True, help="Observed result.")
    promote.add_argument("--why", required=True, help="Reasoning behind promotion.")
    promote.add_argument("--source-entry", help="Optional source entry reference (id/timestamp).")
    promote.add_argument("--artifact", action="append", default=[], help="Optional supporting artifact path.")
    promote.add_argument("--notes", help="Optional promotion notes.")
    promote.add_argument("--tag", action="append", default=[], help="Optional tag (repeatable).")
    promote.add_argument("--json", action="store_true", help="Emit JSON payload.")

    nxt = subparsers.add_parser(
        "next",
        help="Suggest next best actions from current GRD state.",
    )
    nxt.add_argument("--max-actions", type=int, default=3, help="Maximum actions to suggest (default: 3).")
    nxt.add_argument("--json", action="store_true", help="Emit JSON payload.")

    return parser


def _emit_info(repo_root: Path, *, as_json: bool, max_chars: int) -> int:
    _bootstrap_if_missing(repo_root)
    context = load_context(repo_root)
    if as_json:
        print(
            json.dumps(
                context.to_dict(include_markdown=True, max_chars=max_chars),
                indent=2,
            )
        )
        return 0
    print(context.to_markdown(max_chars=max_chars), end="")
    return 0


def _emit_run(repo_root: Path, skill: str, *, as_json: bool, max_chars: int) -> int:
    _bootstrap_if_missing(repo_root)
    context = load_context(repo_root)
    markdown = context.to_markdown(max_chars=max_chars)

    if as_json:
        payload = {
            "mode": "payload-only",
            "skill": skill,
            "context": context.to_dict(include_markdown=True, max_chars=max_chars),
        }
        print(json.dumps(payload, indent=2))
        return 0

    print("# GRD Skill Payload")
    print("")
    print(f"- Skill: {skill}")
    print("- Mode: payload-only")
    print("")
    print(markdown, end="")
    return 0


def _emit_log(
    repo_root: Path,
    what: str,
    happened: str,
    why: str,
    *,
    outcome: str | None,
    artifacts: list[str],
    source: str | None,
    notes: str | None,
    as_json: bool,
) -> int:
    _bootstrap_if_missing(repo_root)
    rs = ResearchState(root_dir=repo_root)

    journal_entry: dict[str, object] = {
        "what": what,
        "happened": happened,
        "why": why,
    }
    if source:
        journal_entry["source"] = source
    if notes:
        journal_entry["notes"] = notes
    rs.append_journal(journal_entry)

    experiment_payload: dict[str, object] | None = None
    if outcome is not None:
        experiment_payload = dict(journal_entry)
        experiment_payload["outcome"] = outcome
        if artifacts:
            experiment_payload["artifacts"] = artifacts
        rs.append_experiment(experiment_payload)

    if as_json:
        payload = {
            "status": "ok",
            "command": "log",
            "journal": journal_entry,
            "experiment": experiment_payload,
        }
        print(json.dumps(payload, indent=2))
    else:
        destination = f"journal: {rs.journal_path}"
        if outcome is not None:
            destination += f", experiments: {rs.experiments_path}"
        print(f"Logged exploration entry -> {destination}")

    return 0


def _emit_promote(
    repo_root: Path,
    title: str,
    what: str,
    happened: str,
    why: str,
    *,
    source_entry: str | None,
    artifacts: list[str],
    notes: str | None,
    tags: list[str],
    as_json: bool,
) -> int:
    _bootstrap_if_missing(repo_root)
    rs = ResearchState(root_dir=repo_root)
    payload: dict[str, object] = {
        "title": title,
        "what": what,
        "happened": happened,
        "why": why,
    }
    if source_entry:
        payload["source_entry"] = source_entry
    if artifacts:
        payload["artifacts"] = artifacts
    if notes:
        payload["notes"] = notes
    if tags:
        payload["tags"] = tags

    output_path = rs.promote_hypothesis(payload)

    if as_json:
        print(
            json.dumps(
                {
                    "status": "ok",
                    "command": "promote",
                    "artifact": str(output_path),
                    "input": payload,
                },
                indent=2,
            )
        )
    else:
        print(f"Promoted hypothesis -> {output_path}")
    return 0


def _emit_next(repo_root: Path, *, max_actions: int, as_json: bool) -> int:
    _bootstrap_if_missing(repo_root)
    rs = ResearchState(root_dir=repo_root)

    journal_count = _count_markdown_sections(rs.journal_path)
    experiment_count = _count_markdown_sections(rs.experiments_path)
    hypothesis_count = len(list(rs.hypotheses_dir.glob("*.md"))) if rs.hypotheses_dir.exists() else 0

    actions: list[str] = []
    if journal_count == 0:
        actions.append("Capture one quick exploration note: `grd log --what ... --happened ... --why ...`.")
    if journal_count > 0 and hypothesis_count == 0:
        actions.append("Promote your strongest recent insight: `grd promote --title ... --what ... --happened ... --why ...`.")
    if journal_count > experiment_count:
        actions.append("Add outcome evidence for recent logs using `--outcome` in `grd log`.")
    if hypothesis_count > 0:
        actions.append("Pick the latest hypothesis and run a focused validation experiment.")
    if not actions:
        actions.append("Continue exploration and use `grd next --json` to chain actions programmatically.")

    actions = actions[: max(1, max_actions)]

    if as_json:
        print(
            json.dumps(
                {
                    "status": "ok",
                    "command": "next",
                    "metrics": {
                        "journal_entries": journal_count,
                        "experiment_entries": experiment_count,
                        "hypotheses": hypothesis_count,
                    },
                    "actions": actions,
                },
                indent=2,
            )
        )
    else:
        print("Next best actions:")
        for idx, action in enumerate(actions, start=1):
            print(f"{idx}. {action}")
    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    repo_root = Path(args.repo_root).expanduser().resolve()

    try:
        if args.command == "info":
            return _emit_info(repo_root, as_json=args.json, max_chars=args.max_chars)
        if args.command == "run":
            return _emit_run(
                repo_root,
                args.skill,
                as_json=args.json,
                max_chars=args.max_chars,
            )
        if args.command == "log":
            return _emit_log(
                repo_root,
                what=args.what,
                happened=args.happened,
                why=args.why,
                outcome=args.outcome,
                artifacts=args.artifact,
                source=args.source,
                notes=args.notes,
                as_json=args.json,
            )
        if args.command == "promote":
            return _emit_promote(
                repo_root,
                title=args.title,
                what=args.what,
                happened=args.happened,
                why=args.why,
                source_entry=args.source_entry,
                artifacts=args.artifact,
                notes=args.notes,
                tags=args.tag,
                as_json=args.json,
            )
        if args.command == "next":
            return _emit_next(
                repo_root,
                max_actions=args.max_actions,
                as_json=args.json,
            )
        parser.error(f"Unknown command: {args.command}")
        return 2
    except (FileNotFoundError, StateContractError, subprocess.CalledProcessError) as exc:
        print(str(exc), file=sys.stderr)
        print(
            "If state is missing or corrupt, route through `grd-state-keeper mode=kickoff`.",
            file=sys.stderr,
        )
        return 2


if __name__ == "__main__":
    sys.exit(main())
