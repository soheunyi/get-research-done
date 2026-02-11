#!/usr/bin/env python3
"""Generate AGY wrappers from core skills/workflows.

Source of truth:
- skills/*
- workflows/research-pipeline.md

Generated output:
- agy/skills/*
- agy/workflows/research-pipeline.md
"""

from __future__ import annotations

import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SOURCE_SKILLS = ROOT / "skills"
SOURCE_WORKFLOW = ROOT / "workflows" / "research-pipeline.md"
AGY_SKILLS = ROOT / "agy" / "skills"
AGY_WORKFLOWS = ROOT / "agy" / "workflows"
AGY_WORKFLOW = AGY_WORKFLOWS / "research-pipeline.md"

GENERATED_BANNER = (
    "<!-- GENERATED FILE. Do not edit directly.\n"
    "Source of truth: skills/*, workflows/*\n"
    "Regenerate: python3 scripts/sync_agy_wrappers.py\n"
    "-->\n\n"
)


def transform_markdown(content: str) -> str:
    out = content

    # Workflow references resolve to installed runtime path.
    out = re.sub(
        r"(?<!\.grd/)(?:@GRD_ROOT@get-research-done/|get-research-done/|agy/)?workflows/research-pipeline\.md",
        ".grd/workflows/research-pipeline.md",
        out,
    )

    # Template references resolve to installed runtime path.
    out = re.sub(
        r"(?<!\.grd/)(?:@GRD_ROOT@get-research-done/|get-research-done/)?templates/",
        ".grd/templates/",
        out,
    )

    # Heading polish for generated AGY files
    out = out.replace("# Codex GRD Skill:", "# AGY GRD Skill:")

    return f"{GENERATED_BANNER}{out}"


def copy_source_skills_to_agy() -> None:
    if AGY_SKILLS.exists():
        shutil.rmtree(AGY_SKILLS)
    AGY_SKILLS.mkdir(parents=True, exist_ok=True)

    for source_dir in sorted(SOURCE_SKILLS.iterdir()):
        if not source_dir.is_dir():
            continue
        if source_dir.name.startswith("."):
            continue

        target_dir = AGY_SKILLS / source_dir.name
        shutil.copytree(source_dir, target_dir)

        for md_file in target_dir.rglob("*.md"):
            text = md_file.read_text(encoding="utf-8")
            md_file.write_text(transform_markdown(text), encoding="utf-8")


def copy_source_workflow_to_agy() -> None:
    AGY_WORKFLOWS.mkdir(parents=True, exist_ok=True)
    text = SOURCE_WORKFLOW.read_text(encoding="utf-8")
    AGY_WORKFLOW.write_text(transform_markdown(text), encoding="utf-8")


def main() -> None:
    copy_source_skills_to_agy()
    copy_source_workflow_to_agy()
    print("Generated AGY wrappers from core sources.")
    print(f"Skills: {AGY_SKILLS}")
    print(f"Workflow: {AGY_WORKFLOW}")


if __name__ == "__main__":
    main()
