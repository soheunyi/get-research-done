from __future__ import annotations

import shutil
from dataclasses import dataclass
from importlib import resources
from pathlib import Path


SKILL_TARGET_DIRS = {
    "codex": ".agents/skills",
    "claude": ".claude/skills",
    "opencode": ".opencode/skills",
    "gemini": ".gemini/skills",
}

VALID_TARGETS = ("runtime", "codex", "claude", "opencode", "gemini", "core", "all")


@dataclass(frozen=True)
class InstallResult:
    dest: Path
    installed_targets: tuple[str, ...]


def _copy_tree_contents(source_dir: Path, dest_dir: Path) -> None:
    dest_dir.mkdir(parents=True, exist_ok=True)
    for item in source_dir.iterdir():
        target = dest_dir / item.name
        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True)
        else:
            shutil.copy2(item, target)


def _normalize_targets(raw_targets: list[str]) -> tuple[str, ...]:
    expanded: set[str] = set()
    for target in raw_targets:
        value = target.strip().lower()
        if not value:
            continue
        if value not in VALID_TARGETS:
            choices = ", ".join(VALID_TARGETS)
            raise ValueError(f"Unknown target '{target}'. Valid targets: {choices}")
        if value in ("core", "all"):
            expanded.update(("runtime", "codex", "claude", "opencode", "gemini"))
        else:
            expanded.add(value)

    if not expanded:
        expanded.update(("runtime", "codex", "claude", "opencode", "gemini"))

    # Ensure per-tool installs include runtime files.
    if expanded.intersection(SKILL_TARGET_DIRS.keys()):
        expanded.add("runtime")

    order = ("runtime", "codex", "claude", "opencode", "gemini")
    return tuple(item for item in order if item in expanded)


def install_targets(dest: str | Path, targets: list[str] | tuple[str, ...]) -> InstallResult:
    resolved_dest = Path(dest).expanduser().resolve()
    resolved_dest.mkdir(parents=True, exist_ok=True)

    selected = _normalize_targets(list(targets))

    assets_root = resources.files("get_research_done").joinpath("assets")
    with resources.as_file(assets_root) as assets_dir:
        if "runtime" in selected:
            _copy_tree_contents(
                assets_dir / "templates",
                resolved_dest / ".grd" / "templates",
            )
            _copy_tree_contents(
                assets_dir / "workflows",
                resolved_dest / ".grd" / "workflows",
            )

        for target, relative_path in SKILL_TARGET_DIRS.items():
            if target not in selected:
                continue
            _copy_tree_contents(
                assets_dir / "skills",
                resolved_dest / relative_path,
            )

    return InstallResult(dest=resolved_dest, installed_targets=selected)
