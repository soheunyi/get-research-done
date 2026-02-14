from __future__ import annotations

import argparse
import sys

from .installer import SKILL_TARGET_DIRS, uninstall_targets

UNINSTALL_TARGETS = ("codex", "claude", "opencode", "gemini", "all", "core")


def _parse_targets(raw_targets: list[str]) -> list[str]:
    if not raw_targets:
        return ["all"]

    parsed: list[str] = []
    for value in raw_targets:
        parsed.extend(item.strip() for item in value.split(",") if item.strip())
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="grd-uninstall",
        description=(
            "Remove get-research-done installed skill files from a target repository. "
            "Runtime .grd artifacts are kept by default."
        ),
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
            "Uninstall target(s): codex, claude, opencode, gemini, core, all. "
            "Repeat or use comma-separated values."
        ),
    )
    parser.add_argument(
        "--include-runtime",
        action="store_true",
        help="Also remove .grd/templates and .grd/workflows files managed by get-research-done.",
    )
    parser.add_argument(
        "--list-targets",
        action="store_true",
        help="Print valid uninstall targets and exit.",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.list_targets:
        print("Valid uninstall targets:")
        for target in UNINSTALL_TARGETS:
            print(f"- {target}")
        print("- runtime (requires --include-runtime)")
        return 0

    targets = _parse_targets(args.target or [])

    try:
        result = uninstall_targets(
            args.dest,
            targets,
            remove_runtime=args.include_runtime,
        )
    except ValueError as exc:
        parser.error(str(exc))
        return 2

    print(f"Uninstalled get-research-done from {result.dest}")
    print("Removed targets:")
    for target in result.removed_targets:
        if target == "runtime":
            print("- runtime -> .grd/templates, .grd/workflows")
            continue
        if target in SKILL_TARGET_DIRS:
            print(f"- {target} -> {SKILL_TARGET_DIRS[target]}")
    if not args.include_runtime:
        print("Runtime artifacts preserved (.grd/templates, .grd/workflows).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
