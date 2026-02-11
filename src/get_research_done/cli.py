from __future__ import annotations

import argparse
import sys

from .installer import SKILL_TARGET_DIRS, VALID_TARGETS, install_targets


def _parse_targets(raw_targets: list[str]) -> list[str]:
    if not raw_targets:
        return ["core"]

    parsed: list[str] = []
    for value in raw_targets:
        parsed.extend(item.strip() for item in value.split(",") if item.strip())
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="grd-install",
        description="Install get-research-done skills/workflows into a target repository.",
    )
    parser.add_argument(
        "dest",
        nargs="?",
        default=".",
        help="Destination repo/directory (default: current directory).",
    )
    parser.add_argument(
        "--target",
        action="append",
        metavar="TARGET",
        help=(
            "Install target(s): runtime, codex, claude, opencode, gemini, core, all. "
            "Repeat or use comma-separated values."
        ),
    )
    parser.add_argument(
        "--list-targets",
        action="store_true",
        help="Print valid targets and exit.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

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


if __name__ == "__main__":
    sys.exit(main())
