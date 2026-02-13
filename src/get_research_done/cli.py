from __future__ import annotations

import argparse
import sys
import os

from .installer import SKILL_TARGET_DIRS, VALID_TARGETS, install_targets
from .state import ResearchState


def _parse_targets(raw_targets: list[str]) -> list[str]:
    if not raw_targets:
        return ["core"]

    parsed: list[str] = []
    for value in raw_targets:
        parsed.extend(item.strip() for item in value.split(",") if item.strip())
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="grd",
        description="Get Research Done (GRD) utility suite.",
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Install command
    install_parser = subparsers.add_parser("install", help="Install GRD into a target repository.")
    install_parser.add_argument(
        "dest",
        nargs="?",
        default=".",
        help="Destination repo/directory (default: current directory).",
    )
    install_parser.add_argument(
        "--target",
        action="append",
        metavar="TARGET",
        help=(
            "Install target(s): runtime, codex, claude, opencode, gemini, core, all. "
            "Repeat or use comma-separated values."
        ),
    )
    install_parser.add_argument(
        "--list-targets",
        action="store_true",
        help="Print valid targets and exit.",
    )

    # Info/State command
    info_parser = subparsers.add_parser("info", help="Show current research state.")
    info_parser.add_argument(
        "--include-state",
        action="store_true",
        help="Print full prompt-friendly state injection string.",
    )

    return parser


def format_state_for_prompt(state: dict) -> str:
    """Formats the state dictionary into a prompt-friendly string."""
    lines = ["<grd_context>", "## Current Research State"]
    for key, value in state.items():
        lines.append(f"- **{key}:** {value}")
    lines.append("</grd_context>")
    return "\n".join(lines)


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "install":
        if args.list_targets:
            print("Valid targets:")
            for target in VALID_TARGETS:
                print(f"- {target}")
            return 0

        targets = _parse_targets(args.target or [])

        try:
            result = install_targets(args.dest, targets)
        except ValueError as exc:
            parser.error(str(exc))
            return 2

        print(f"Installed get-research-done into {result.dest}")
        print("Installed targets:")
        for target in result.installed_targets:
            if target == "runtime":
                print("- runtime -> .grd/templates, .grd/workflows")
                continue
            if target in SKILL_TARGET_DIRS:
                print(f"- {target} -> {SKILL_TARGET_DIRS[target]}")
        return 0

    elif args.command == "info":
        rs = ResearchState()
        state = rs.load()
        if not state:
            print("No .grd/ state found. Run 'grd install' to initialize.")
            return 1
        
        if args.include_state:
            print(format_state_for_prompt(state))
        else:
            print("Current Research State:")
            for key, value in state.items():
                print(f"  {key}: {value}")
        return 0

    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
