#!/usr/bin/env python3
"""Enforce length budgets for GRD skill source files.

Checks only skills/grd-*/SKILL.src.md and fails if any file exceeds the cap.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


DEFAULT_CAP = 80


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cap",
        type=int,
        default=DEFAULT_CAP,
        help=f"Maximum allowed line count (default: {DEFAULT_CAP})",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    src_files = sorted(repo_root.glob("skills/grd-*/SKILL.src.md"))

    if not src_files:
        print("No skill source files found under skills/grd-*/SKILL.src.md")
        return 1

    offenders: list[tuple[Path, int]] = []
    for path in src_files:
        line_count = len(path.read_text(encoding="utf-8").splitlines())
        if line_count > args.cap:
            offenders.append((path, line_count))

    if offenders:
        print(f"Skill length budget violations (cap={args.cap}):")
        for path, line_count in offenders:
            rel = path.relative_to(repo_root)
            print(f"- {rel}: {line_count} lines")
        return 1

    print(
        f"Skill length check passed: {len(src_files)} files within {args.cap} lines "
        "for skills/grd-*/SKILL.src.md"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
