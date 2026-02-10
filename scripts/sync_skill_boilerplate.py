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
TAGS = (
    "context_budget",
    "intent_lock",
    "questioning_loop",
    "precision_contract",
    "anti_enterprise",
    "delivery_rule",
    "output_format",
    "action_policy",
)


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


def _find_insertion_index(text: str) -> int:
    for anchor in ("clarification_rule", "source_of_truth"):
        m = re.search(rf"(?s)</{anchor}>", text)
        if m:
            return m.end()
    return len(text.rstrip("\n"))


def apply_blocks(text: str, blocks: dict[str, str]) -> str:
    updated = text
    missing: list[str] = []

    for tag in TAGS:
        pattern = re.compile(rf"(?s)<{tag}>\n.*?\n</{tag}>")
        match = pattern.search(updated)
        if match:
            updated = pattern.sub(blocks[tag], updated, count=1)
        else:
            missing.append(tag)

    if missing:
        idx = _find_insertion_index(updated)
        payload = "\n\n" + "\n\n".join(blocks[tag] for tag in missing)
        updated = updated[:idx] + payload + updated[idx:]

    return updated.rstrip("\n") + "\n"


def sync_file(path: Path, blocks: dict[str, str]) -> bool:
    original = path.read_text(encoding="utf-8")
    updated = apply_blocks(original, blocks)
    if updated != original:
        path.write_text(updated, encoding="utf-8")
        return True
    return False


def check_file(path: Path, blocks: dict[str, str]) -> bool:
    original = path.read_text(encoding="utf-8")
    candidate = apply_blocks(original, blocks)
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
