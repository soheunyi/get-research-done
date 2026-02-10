#!/usr/bin/env python3
"""Sync shared SKILL.md boilerplate blocks across codex skills.

Usage:
  python scripts/sync_skill_boilerplate.py --check
  python scripts/sync_skill_boilerplate.py --fix
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
COMMON_BLOCKS = REPO_ROOT / "codex" / "skills" / "_shared" / "COMMON_BLOCKS.md"
SKILLS_ROOT = REPO_ROOT / "codex" / "skills"
TAGS = ("delivery_rule", "output_format", "action_policy")


def load_common_blocks() -> dict[str, str]:
    text = COMMON_BLOCKS.read_text(encoding="utf-8")
    blocks: dict[str, str] = {}
    for tag in TAGS:
        pattern = re.compile(rf"(?s)<{tag}>\n.*?\n</{tag}>")
        match = pattern.search(text)
        if not match:
            raise ValueError(f"Missing canonical block <{tag}> in {COMMON_BLOCKS}")
        blocks[tag] = match.group(0)
    return blocks


def find_skill_files() -> list[Path]:
    files: list[Path] = []
    for path in SKILLS_ROOT.glob("*/SKILL.md"):
        if "__MACOSX" in path.parts:
            continue
        files.append(path)
    files.sort()
    return files


def replace_or_insert(text: str, tag: str, block: str) -> tuple[str, bool]:
    pattern = re.compile(rf"(?s)<{tag}>\n.*?\n</{tag}>")
    if pattern.search(text):
        updated = pattern.sub(block, text, count=1)
        return updated, updated != text

    insertion = "\n\n" + block
    for anchor in ("clarification_rule", "source_of_truth"):
        anchor_pattern = re.compile(rf"(?s)</{anchor}>")
        m = anchor_pattern.search(text)
        if m:
            idx = m.end()
            return text[:idx] + insertion + text[idx:], True

    return text.rstrip("\n") + "\n\n" + block + "\n", True


def sync_file(path: Path, blocks: dict[str, str]) -> bool:
    original = path.read_text(encoding="utf-8")
    updated = original
    changed = False

    for tag in TAGS:
        updated, block_changed = replace_or_insert(updated, tag, blocks[tag])
        changed = changed or block_changed

    updated = updated.rstrip("\n") + "\n"
    if updated != original:
        path.write_text(updated, encoding="utf-8")
        return True
    return changed and updated != original


def check_file(path: Path, blocks: dict[str, str]) -> bool:
    original = path.read_text(encoding="utf-8")
    candidate = original
    for tag in TAGS:
        candidate, _ = replace_or_insert(candidate, tag, blocks[tag])
    candidate = candidate.rstrip("\n") + "\n"
    return candidate != original


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="Fail if files would change")
    mode.add_argument("--fix", action="store_true", help="Apply changes in place")
    args = parser.parse_args()

    blocks = load_common_blocks()
    skill_files = find_skill_files()

    if args.check:
        out_of_sync = [str(path) for path in skill_files if check_file(path, blocks)]
        if out_of_sync:
            print("Out-of-sync skill files:")
            for item in out_of_sync:
                print(f"- {item}")
            return 1
        print("All codex skill files are in sync.")
        return 0

    changed_files = [str(path) for path in skill_files if sync_file(path, blocks)]
    if changed_files:
        print("Updated skill files:")
        for item in changed_files:
            print(f"- {item}")
    else:
        print("No changes needed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
