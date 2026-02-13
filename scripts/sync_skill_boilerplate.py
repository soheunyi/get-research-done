#!/usr/bin/env python3
"""Generate SKILL.md files from skill-specific sources and shared base blocks.

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
BASE_BLOCKS = REPO_ROOT / "skills" / "_shared" / "BASE.md"
SKILLS_ROOT = REPO_ROOT / "skills"
SOURCE_FILE = "SKILL.src.md"
TARGET_FILE = "SKILL.md"
MARKER = "{{COMMON_BLOCKS}}"
TAGS = (
    "context_budget",
    "template_convention",
    "state_awareness_contract",
    "intent_lock",
    "questioning_loop",
    "precision_contract",
    "anti_enterprise",
    "delivery_rule",
    "output_format",
    "action_policy",
)


def load_common_blocks() -> dict[str, str]:
    text = BASE_BLOCKS.read_text(encoding="utf-8")
    blocks: dict[str, str] = {}
    for tag in TAGS:
        pattern = re.compile(rf"(?s)<{tag}>\n.*?\n</{tag}>")
        match = pattern.search(text)
        if not match:
            raise ValueError(f"Missing canonical block <{tag}> in {BASE_BLOCKS}")
        blocks[tag] = match.group(0)
    return blocks


def find_skill_dirs() -> list[Path]:
    dirs: list[Path] = []
    for path in SKILLS_ROOT.iterdir():
        if not path.is_dir():
            continue
        if path.name.startswith(".") or path.name == "_shared":
            continue
        if "__MACOSX" in path.parts:
            continue
        dirs.append(path)
    dirs.sort()
    return dirs


def _find_insertion_index(text: str) -> int:
    for anchor in ("clarification_rule", "source_of_truth"):
        m = re.search(rf"(?s)</{anchor}>", text)
        if m:
            return m.end()
    return len(text.rstrip("\n"))


def _strip_common_blocks(text: str) -> str:
    updated = text
    for tag in TAGS:
        pattern = re.compile(rf"(?s)<{tag}>\n.*?\n</{tag}>")
        updated = pattern.sub("", updated, count=1)
    return updated


def _normalize_text(text: str) -> str:
    updated = text.replace("\r\n", "\n")
    updated = re.sub(r"\n*\{\{COMMON_BLOCKS\}\}\n*", f"\n\n{MARKER}\n\n", updated)
    updated = re.sub(r"\n{3,}", "\n\n", updated)
    return updated.rstrip("\n") + "\n"


def bootstrap_source_from_target(skill_dir: Path) -> bool:
    source_path = skill_dir / SOURCE_FILE
    target_path = skill_dir / TARGET_FILE
    if source_path.exists():
        return False
    if not target_path.exists():
        raise FileNotFoundError(f"Missing both {source_path} and {target_path}")

    target_text = target_path.read_text(encoding="utf-8")
    source_text = _strip_common_blocks(target_text).rstrip("\n")

    if MARKER not in source_text:
        idx = _find_insertion_index(source_text)
        source_text = source_text[:idx] + f"\n\n{MARKER}" + source_text[idx:]

    source_path.write_text(_normalize_text(source_text), encoding="utf-8")
    return True


def render_skill(source_text: str, blocks: dict[str, str]) -> str:
    if MARKER not in source_text:
        raise ValueError(f"Missing marker {MARKER} in skill source")
    block_payload = "\n\n".join(blocks[tag] for tag in TAGS)
    updated = source_text.replace(MARKER, block_payload)
    return _normalize_text(updated)


def check_skill(skill_dir: Path, blocks: dict[str, str]) -> str | None:
    source_path = skill_dir / SOURCE_FILE
    target_path = skill_dir / TARGET_FILE
    if not source_path.exists():
        return f"missing source: {source_path}"
    if not target_path.exists():
        return f"missing generated skill: {target_path}"

    source_text = source_path.read_text(encoding="utf-8")
    try:
        rendered = render_skill(source_text, blocks)
    except ValueError as exc:
        return f"{target_path}: {exc}"

    current = target_path.read_text(encoding="utf-8")
    if rendered != current:
        return f"out of sync: {target_path}"
    return None


def sync_skill(skill_dir: Path, blocks: dict[str, str]) -> tuple[bool, bool]:
    source_created = bootstrap_source_from_target(skill_dir)
    source_path = skill_dir / SOURCE_FILE
    target_path = skill_dir / TARGET_FILE
    source_text = source_path.read_text(encoding="utf-8")
    normalized_source = _normalize_text(source_text)
    if normalized_source != source_text:
        source_path.write_text(normalized_source, encoding="utf-8")
        source_text = normalized_source

    rendered = render_skill(source_text, blocks)

    changed = False
    if not target_path.exists() or target_path.read_text(encoding="utf-8") != rendered:
        target_path.write_text(rendered, encoding="utf-8")
        changed = True
    return changed, source_created


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="Fail if files would change")
    mode.add_argument("--fix", action="store_true", help="Apply changes in place")
    args = parser.parse_args()

    blocks = load_common_blocks()
    skill_dirs = find_skill_dirs()

    if args.check:
        out_of_sync = []
        for skill_dir in skill_dirs:
            check_error = check_skill(skill_dir, blocks)
            if check_error:
                out_of_sync.append(check_error)
        if out_of_sync:
            print("Out-of-sync skill files:")
            for item in out_of_sync:
                print(f"- {item}")
            return 1
        print("All skill files are in sync.")
        return 0

    changed_files: list[str] = []
    bootstrapped_sources: list[str] = []
    for skill_dir in skill_dirs:
        changed, source_created = sync_skill(skill_dir, blocks)
        if changed:
            changed_files.append(str(skill_dir / TARGET_FILE))
        if source_created:
            bootstrapped_sources.append(str(skill_dir / SOURCE_FILE))

    if bootstrapped_sources:
        print("Bootstrapped skill source files:")
        for item in bootstrapped_sources:
            print(f"- {item}")

    if changed_files:
        print("Updated generated skill files:")
        for item in changed_files:
            print(f"- {item}")
    else:
        print("No changes needed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
