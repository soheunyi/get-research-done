#!/usr/bin/env python3
"""Lint adaptive questioning policy contracts for GRD skills."""

from __future__ import annotations

import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
BASE_PATH = REPO_ROOT / "skills" / "_shared" / "BASE.md"
SKILL_SRC_GLOB = "skills/grd-*/SKILL.src.md"

REQUIRED_BASE_PATTERNS = [
    r"Only run this loop when missing information would materially change",
    r"Ask at most 1 high-leverage question per response",
    r"include 2-4 options only when they reduce ambiguity or user effort",
    r"Recap \"Captured so far\" only after multi-turn clarification",
    r"If safe to proceed, continue with explicit assumptions",
]

PROHIBITED_BASE_PATTERNS = [
    r"Include 2-4 concrete options to lower user effort",
    r"After each answer, summarize \"Captured so far\" in bullets",
]

UNCONDITIONAL_SKILL_PATTERNS = [
    re.compile(r"^\s*Start with one .*question", re.IGNORECASE),
    re.compile(r"^\s*Before implementation, ask\b", re.IGNORECASE),
]


def extract_questioning_loop(text: str) -> str | None:
    match = re.search(r"(?s)<questioning_loop>\n.*?\n</questioning_loop>", text)
    if not match:
        return None
    return match.group(0)


def check_shared_loop(errors: list[str]) -> None:
    text = BASE_PATH.read_text(encoding="utf-8")
    block = extract_questioning_loop(text)
    if block is None:
        errors.append(f"missing <questioning_loop> block: {BASE_PATH.relative_to(REPO_ROOT)}")
        return

    for pattern in REQUIRED_BASE_PATTERNS:
        if not re.search(pattern, block, re.IGNORECASE):
            errors.append(
                "missing adaptive questioning invariant "
                f"/{pattern}/ in {BASE_PATH.relative_to(REPO_ROOT)}"
            )

    for pattern in PROHIBITED_BASE_PATTERNS:
        if re.search(pattern, block, re.IGNORECASE):
            errors.append(
                "found prohibited rigid questioning phrase "
                f"/{pattern}/ in {BASE_PATH.relative_to(REPO_ROOT)}"
            )


def check_skill_sources(errors: list[str]) -> None:
    for path in sorted(REPO_ROOT.glob(SKILL_SRC_GLOB)):
        lines = path.read_text(encoding="utf-8").splitlines()
        for idx, line in enumerate(lines, start=1):
            for pattern in UNCONDITIONAL_SKILL_PATTERNS:
                if pattern.search(line):
                    errors.append(
                        "unconditional questioning anti-pattern "
                        f"{pattern.pattern!r} at {path.relative_to(REPO_ROOT)}:{idx}"
                    )


def main() -> int:
    errors: list[str] = []
    check_shared_loop(errors)
    check_skill_sources(errors)

    if errors:
        print("Questioning policy violations:")
        for item in errors:
            print(f"- {item}")
        return 1

    print(
        "Questioning policy check passed: shared adaptive loop invariants present "
        "and no unconditional questioning anti-patterns in skills/grd-*/SKILL.src.md"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
