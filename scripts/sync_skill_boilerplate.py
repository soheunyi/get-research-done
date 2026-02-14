#!/usr/bin/env python3
"""Generate SKILL.md files from skill-specific sources and shared base blocks.

Usage:
  python scripts/sync_skill_boilerplate.py --check
  python scripts/sync_skill_boilerplate.py --fix
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = REPO_ROOT / "skills"
SHARED_ROOT = SKILLS_ROOT / "_shared"
BASE_BLOCKS = SHARED_ROOT / "BASE.md"
PROFILE_BLOCKS_ROOT = SHARED_ROOT / "profiles"
PROFILE_BASE_NAME = "base"
PROFILE_BASE_BLOCKS = PROFILE_BLOCKS_ROOT / f"{PROFILE_BASE_NAME}.md"
SKILL_PROFILES_FILE = SHARED_ROOT / "skill-profiles.json"
SOURCE_FILE = "SKILL.src.md"
TARGET_FILE = "SKILL.md"
MARKER = "{{COMMON_BLOCKS}}"

GLOBAL_TAGS = (
    "context_policy",
    "template_convention",
    "questioning_loop",
    "precision_contract",
    "anti_enterprise",
    "delivery_rule",
)

PROFILE_TAGS = (
    "intent_lock",
    "output_format",
    "action_policy",
)
PROFILE_DELTA_SUFFIX = "_delta"

RENDER_TAGS = (
    "context_policy",
    "template_convention",
    "intent_lock",
    "questioning_loop",
    "precision_contract",
    "anti_enterprise",
    "delivery_rule",
    "output_format",
    "action_policy",
)


def extract_tag_blocks(text: str, tags: tuple[str, ...], source: Path) -> dict[str, str]:
    blocks: dict[str, str] = {}
    for tag in tags:
        pattern = re.compile(rf"(?s)<{tag}>\n.*?\n</{tag}>")
        match = pattern.search(text)
        if not match:
            raise ValueError(f"Missing canonical block <{tag}> in {source}")
        blocks[tag] = match.group(0)
    return blocks


def extract_optional_tag_block(text: str, tag: str) -> str | None:
    pattern = re.compile(rf"(?s)<{tag}>\n.*?\n</{tag}>")
    match = pattern.search(text)
    if not match:
        return None
    return match.group(0)


def extract_optional_tag_body(text: str, tag: str) -> str | None:
    block = extract_optional_tag_block(text, tag)
    if block is None:
        return None
    pattern = re.compile(rf"(?s)^<{tag}>\n(.*)\n</{tag}>$")
    match = pattern.match(block)
    if not match:
        return None
    return match.group(1)


def merge_delta_block(base_block: str, tag: str, delta_body: str) -> str:
    closing_tag = f"</{tag}>"
    closing_idx = base_block.rfind(closing_tag)
    if closing_idx == -1:
        raise ValueError(f"Invalid base profile block for <{tag}>")

    base_without_close = base_block[:closing_idx].rstrip("\n")
    cleaned_delta = delta_body.strip("\n")
    if not cleaned_delta:
        return base_block
    return f"{base_without_close}\n{cleaned_delta}\n{closing_tag}"


def load_global_blocks() -> dict[str, str]:
    text = BASE_BLOCKS.read_text(encoding="utf-8")
    return extract_tag_blocks(text, GLOBAL_TAGS, BASE_BLOCKS)


def load_profile_base_blocks() -> dict[str, str]:
    if not PROFILE_BASE_BLOCKS.exists():
        raise ValueError(f"Missing profile base blocks file: {PROFILE_BASE_BLOCKS}")
    text = PROFILE_BASE_BLOCKS.read_text(encoding="utf-8")
    return extract_tag_blocks(text, PROFILE_TAGS, PROFILE_BASE_BLOCKS)


def load_skill_profiles() -> dict[str, str]:
    try:
        raw = json.loads(SKILL_PROFILES_FILE.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ValueError(f"Missing skill profile mapping file: {SKILL_PROFILES_FILE}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {SKILL_PROFILES_FILE}: {exc}") from exc

    if not isinstance(raw, dict):
        raise ValueError(f"Skill profile mapping must be an object: {SKILL_PROFILES_FILE}")

    mapping: dict[str, str] = {}
    for skill_name, profile_name in raw.items():
        if not isinstance(skill_name, str) or not isinstance(profile_name, str):
            raise ValueError(
                f"Skill profile mapping must be string:string pairs: {SKILL_PROFILES_FILE}"
            )
        mapping[skill_name] = profile_name
    return mapping


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


def find_available_profiles() -> set[str]:
    profiles: set[str] = set()
    if not PROFILE_BLOCKS_ROOT.exists():
        return profiles
    for path in PROFILE_BLOCKS_ROOT.glob("*.md"):
        if path.stem == PROFILE_BASE_NAME:
            continue
        profiles.add(path.stem)
    return profiles


def validate_skill_profile_map(
    skill_dirs: list[Path],
    skill_profiles: dict[str, str],
    available_profiles: set[str],
) -> None:
    errors: list[str] = []
    known_skill_names = {path.name for path in skill_dirs}

    if not available_profiles:
        errors.append(f"No profile blocks found in {PROFILE_BLOCKS_ROOT}")

    for skill_name in sorted(known_skill_names):
        if skill_name not in skill_profiles:
            errors.append(f"Missing profile mapping for skill: {skill_name}")
            continue
        profile_name = skill_profiles[skill_name]
        if profile_name not in available_profiles:
            errors.append(
                "Unknown profile "
                f"'{profile_name}' for skill '{skill_name}'. "
                f"Available profiles: {sorted(available_profiles)}"
            )

    for mapped_skill in sorted(skill_profiles):
        if mapped_skill not in known_skill_names:
            errors.append(
                f"Profile mapping references unknown skill directory: {mapped_skill}"
            )

    if errors:
        error_lines = "\n".join(f"- {item}" for item in errors)
        raise ValueError(f"Invalid skill profile mapping:\n{error_lines}")


def load_profile_blocks(
    profile_name: str,
    profile_base_blocks: dict[str, str],
    profile_cache: dict[str, dict[str, str]],
) -> dict[str, str]:
    cached = profile_cache.get(profile_name)
    if cached is not None:
        return cached

    profile_path = PROFILE_BLOCKS_ROOT / f"{profile_name}.md"
    if not profile_path.exists():
        raise ValueError(f"Missing profile file: {profile_path}")

    text = profile_path.read_text(encoding="utf-8")
    blocks: dict[str, str] = {}
    has_profile_specific_content = False
    for tag in PROFILE_TAGS:
        explicit_block = extract_optional_tag_block(text, tag)
        if explicit_block is not None:
            blocks[tag] = explicit_block
            has_profile_specific_content = True
            continue

        delta_tag = f"{tag}{PROFILE_DELTA_SUFFIX}"
        delta_body = extract_optional_tag_body(text, delta_tag)
        if delta_body is not None:
            blocks[tag] = merge_delta_block(profile_base_blocks[tag], tag, delta_body)
            has_profile_specific_content = True
            continue

        blocks[tag] = profile_base_blocks[tag]

    if not has_profile_specific_content:
        raise ValueError(
            f"Profile must define at least one explicit or delta block: {profile_path}"
        )

    profile_cache[profile_name] = blocks
    return blocks


def blocks_for_skill(
    skill_name: str,
    global_blocks: dict[str, str],
    skill_profiles: dict[str, str],
    profile_base_blocks: dict[str, str],
    profile_cache: dict[str, dict[str, str]],
) -> dict[str, str]:
    profile_name = skill_profiles[skill_name]
    profile_blocks = load_profile_blocks(profile_name, profile_base_blocks, profile_cache)

    combined = dict(global_blocks)
    combined.update(profile_blocks)
    return {tag: combined[tag] for tag in RENDER_TAGS}


def _find_insertion_index(text: str) -> int:
    for anchor in ("clarification_rule", "source_of_truth"):
        m = re.search(rf"(?s)</{anchor}>", text)
        if m:
            return m.end()
    return len(text.rstrip("\n"))


def _strip_common_blocks(text: str) -> str:
    updated = text
    for tag in RENDER_TAGS:
        pattern = re.compile(rf"(?s)<{tag}>\n.*?\n</{tag}>")
        updated = pattern.sub("", updated, count=1)
    return updated


def _prepare_frontmatter(text: str, *, fix: bool) -> str:
    updated = text.replace("\r\n", "\n")
    if updated.startswith("\ufeff"):
        updated = updated[1:]

    if not fix:
        return updated

    stripped = updated.lstrip("\n")
    if stripped.startswith("---"):
        updated = stripped

    lines = updated.split("\n")
    if not lines:
        return updated

    if lines[0].strip() == "---":
        lines[0] = "---"

    closing_idx: int | None = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            lines[idx] = "---"
            closing_idx = idx
            break

    if closing_idx is not None and lines[0] == "---":
        for idx in range(1, closing_idx):
            if re.match(r"^[A-Za-z0-9_-]+\s*:", lines[idx]) and lines[idx].rstrip().endswith("---"):
                lines[idx] = re.sub(r"\s*---\s*$", "", lines[idx]).rstrip()

    has_closing = closing_idx is not None
    if not has_closing and lines[0] == "---":
        for idx in range(1, min(len(lines), 120)):
            stripped_line = lines[idx].strip()
            if not stripped_line or stripped_line == "---":
                continue
            if stripped_line.endswith("---"):
                lines[idx] = re.sub(r"\s*---\s*$", "", lines[idx]).rstrip()
                lines.insert(idx + 1, "---")
                break

    return "\n".join(lines)


def _validate_frontmatter(text: str) -> str | None:
    lines = text.split("\n")
    if not lines or lines[0] != "---":
        return "frontmatter must start with '---' on line 1"

    closing_idx: int | None = None
    for idx in range(1, len(lines)):
        if lines[idx] == "---":
            closing_idx = idx
            break

    if closing_idx is None:
        return "frontmatter missing closing '---' on its own line"

    for idx in range(1, closing_idx):
        if re.match(r"^[A-Za-z0-9_-]+\s*:", lines[idx]) and lines[idx].rstrip().endswith("---"):
            return "frontmatter contains inline closing marker; closing '---' must be on its own line"

    return None


def _normalize_text(text: str) -> str:
    updated = text.replace("\r\n", "\n")
    updated = re.sub(r"\n*\{\{COMMON_BLOCKS\}\}\n*", f"\n\n{MARKER}\n\n", updated)
    updated = re.sub(r"\n{3,}", "\n\n", updated)
    return updated.rstrip("\n") + "\n"


def _normalize_source(text: str, *, fix: bool) -> tuple[str, str | None]:
    prepared = _prepare_frontmatter(text, fix=fix)
    normalized = _normalize_text(prepared)
    return normalized, _validate_frontmatter(normalized)


def bootstrap_source_from_target(skill_dir: Path) -> bool:
    source_path = skill_dir / SOURCE_FILE
    target_path = skill_dir / TARGET_FILE
    if source_path.exists():
        return False
    if not target_path.exists():
        raise FileNotFoundError(f"Missing both {source_path} and {target_path}")

    target_text, frontmatter_error = _normalize_source(
        target_path.read_text(encoding="utf-8"),
        fix=True,
    )
    if frontmatter_error:
        raise ValueError(f"{target_path}: {frontmatter_error}")

    source_text = _strip_common_blocks(target_text).rstrip("\n")

    if MARKER not in source_text:
        idx = _find_insertion_index(source_text)
        source_text = source_text[:idx] + f"\n\n{MARKER}" + source_text[idx:]

    normalized_source, source_frontmatter_error = _normalize_source(source_text, fix=True)
    if source_frontmatter_error:
        raise ValueError(f"{source_path}: {source_frontmatter_error}")

    source_path.write_text(normalized_source, encoding="utf-8")
    return True


def render_skill(source_text: str, blocks: dict[str, str]) -> str:
    if MARKER not in source_text:
        raise ValueError(f"Missing marker {MARKER} in skill source")
    block_payload = "\n\n".join(blocks[tag] for tag in RENDER_TAGS)
    updated = source_text.replace(MARKER, block_payload)
    return _normalize_text(updated)


def check_skill(
    skill_dir: Path,
    blocks: dict[str, str],
) -> str | None:
    source_path = skill_dir / SOURCE_FILE
    target_path = skill_dir / TARGET_FILE
    if not source_path.exists():
        return f"missing source: {source_path}"
    if not target_path.exists():
        return f"missing generated skill: {target_path}"

    source_raw = source_path.read_text(encoding="utf-8")
    source_text, source_frontmatter_error = _normalize_source(source_raw, fix=False)
    if source_frontmatter_error:
        return f"malformed frontmatter: {source_path} ({source_frontmatter_error})"
    if source_text != source_raw.replace("\r\n", "\n"):
        return f"source needs normalization: {source_path}"

    try:
        rendered = render_skill(source_text, blocks)
    except ValueError as exc:
        return f"{target_path}: {exc}"

    rendered, rendered_frontmatter_error = _normalize_source(rendered, fix=False)
    if rendered_frontmatter_error:
        return f"malformed rendered frontmatter: {target_path} ({rendered_frontmatter_error})"

    current_raw = target_path.read_text(encoding="utf-8")
    current, current_frontmatter_error = _normalize_source(current_raw, fix=False)
    if current_frontmatter_error:
        return f"malformed frontmatter: {target_path} ({current_frontmatter_error})"

    if rendered != current:
        return f"out of sync: {target_path}"
    return None


def sync_skill(skill_dir: Path, blocks: dict[str, str]) -> tuple[bool, bool]:
    source_created = bootstrap_source_from_target(skill_dir)
    source_path = skill_dir / SOURCE_FILE
    target_path = skill_dir / TARGET_FILE

    source_raw = source_path.read_text(encoding="utf-8")
    normalized_source, source_frontmatter_error = _normalize_source(source_raw, fix=True)
    if source_frontmatter_error:
        raise ValueError(f"{source_path}: {source_frontmatter_error}")

    if normalized_source != source_raw:
        source_path.write_text(normalized_source, encoding="utf-8")

    rendered = render_skill(normalized_source, blocks)
    rendered, rendered_frontmatter_error = _normalize_source(rendered, fix=True)
    if rendered_frontmatter_error:
        raise ValueError(f"{target_path}: {rendered_frontmatter_error}")

    changed = False
    if target_path.exists():
        current_raw = target_path.read_text(encoding="utf-8")
        current_normalized, current_frontmatter_error = _normalize_source(
            current_raw,
            fix=True,
        )
        if current_frontmatter_error:
            raise ValueError(f"{target_path}: {current_frontmatter_error}")
        if current_normalized != current_raw:
            target_path.write_text(current_normalized, encoding="utf-8")
            current_raw = current_normalized
        if current_raw == rendered:
            return changed, source_created

    target_path.write_text(rendered, encoding="utf-8")
    changed = True
    return changed, source_created


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="Fail if files would change")
    mode.add_argument("--fix", action="store_true", help="Apply changes in place")
    args = parser.parse_args()

    try:
        global_blocks = load_global_blocks()
        profile_base_blocks = load_profile_base_blocks()
        skill_dirs = find_skill_dirs()
        skill_profiles = load_skill_profiles()
        available_profiles = find_available_profiles()
        validate_skill_profile_map(skill_dirs, skill_profiles, available_profiles)
    except ValueError as exc:
        print(exc)
        return 1

    profile_cache: dict[str, dict[str, str]] = {}

    if args.check:
        out_of_sync = []
        for skill_dir in skill_dirs:
            try:
                blocks = blocks_for_skill(
                    skill_dir.name,
                    global_blocks,
                    skill_profiles,
                    profile_base_blocks,
                    profile_cache,
                )
                check_error = check_skill(skill_dir, blocks)
            except ValueError as exc:
                check_error = str(exc)
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
        try:
            blocks = blocks_for_skill(
                skill_dir.name,
                global_blocks,
                skill_profiles,
                profile_base_blocks,
                profile_cache,
            )
            changed, source_created = sync_skill(skill_dir, blocks)
        except (ValueError, FileNotFoundError) as exc:
            print(exc)
            return 1
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
