#!/usr/bin/env python3
"""Enforce references coverage for GRD skills."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--strict-mentions",
        action="store_true",
        help="Also require each SKILL.src.md to mention 'references/'.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    skill_dirs = sorted(repo_root.glob("skills/grd-*"))

    if not skill_dirs:
        print("No skill directories found under skills/grd-*")
        return 1

    errors: list[str] = []

    for skill_dir in skill_dirs:
        rel_dir = skill_dir.relative_to(repo_root)
        src_path = skill_dir / "SKILL.src.md"
        ref_dir = skill_dir / "references"

        if not src_path.exists():
            errors.append(f"missing source file: {rel_dir / 'SKILL.src.md'}")
            continue

        md_refs = sorted(ref_dir.glob("*.md")) if ref_dir.exists() else []
        if not md_refs:
            errors.append(f"missing references markdown files: {rel_dir / 'references'}")

        if args.strict_mentions:
            text = src_path.read_text(encoding="utf-8")
            if "references/" not in text:
                errors.append(
                    f"missing references mention in source: {rel_dir / 'SKILL.src.md'}"
                )

    if errors:
        print("Skill references check violations:")
        for item in errors:
            print(f"- {item}")
        return 1

    mode = " with strict mention enforcement" if args.strict_mentions else ""
    print(
        f"Skill references check passed: {len(skill_dirs)} skills include references/*.md{mode}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
