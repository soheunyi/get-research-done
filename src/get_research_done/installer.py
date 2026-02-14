from __future__ import annotations

import shutil
from contextlib import contextmanager
from dataclasses import dataclass
from importlib import resources
from pathlib import Path


SKILL_TARGET_DIRS = {
    "codex": ".agents/skills",
    "claude": ".claude/skills",
    "opencode": ".opencode/skills",
    "gemini": ".gemini/skills",
}
LEGACY_SKILL_BASENAMES = (
    "attribution-and-robustness",
    "codebase-mapper",
    "data-auditor",
    "evaluation-suite",
    "execution-planner",
    "experiment-planner",
    "hypothesis-designer",
    "ideation-and-reasoning",
    "literature-synthesizer",
    "patch-reviewer",
    "phase-researcher",
    "prompt-librarian",
    "reference-checker",
    "result-interpreter",
    "stability-auditor",
)

VALID_TARGETS = ("runtime", "codex", "claude", "opencode", "gemini", "core", "all")
SKILL_TARGET_ORDER = ("codex", "claude", "opencode", "gemini")


@dataclass(frozen=True)
class InstallResult:
    dest: Path
    installed_targets: tuple[str, ...]


@dataclass(frozen=True)
class UninstallResult:
    dest: Path
    removed_targets: tuple[str, ...]


def _copy_tree_contents(source_dir: Path, dest_dir: Path) -> None:
    dest_dir.mkdir(parents=True, exist_ok=True)
    for item in source_dir.iterdir():
        target = dest_dir / item.name
        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True)
        else:
            shutil.copy2(item, target)


def _copy_skill_dirs(source_dir: Path, dest_dir: Path) -> None:
    dest_dir.mkdir(parents=True, exist_ok=True)
    for item in source_dir.iterdir():
        if not item.is_dir():
            continue
        if not item.name.startswith("grd-"):
            continue
        shutil.copytree(item, dest_dir / item.name, dirs_exist_ok=True)


def _remove_path(path: Path) -> None:
    if not (path.exists() or path.is_symlink()):
        return
    if path.is_symlink() or path.is_file():
        path.unlink()
        return
    shutil.rmtree(path)


def _remove_tree_contents(source_dir: Path, dest_dir: Path) -> None:
    for item in source_dir.iterdir():
        _remove_path(dest_dir / item.name)


def _remove_legacy_skill_dirs(dest_dir: Path) -> None:
    _remove_path(dest_dir / "_shared")
    for basename in LEGACY_SKILL_BASENAMES:
        _remove_path(dest_dir / f"grd-{basename}")


def _prune_empty_dirs(start: Path, root: Path) -> None:
    current = start
    while current != root and current != current.parent:
        if current.exists():
            try:
                current.rmdir()
            except OSError:
                break
        current = current.parent


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


def _normalize_uninstall_targets(
    raw_targets: list[str],
    *,
    remove_runtime: bool,
) -> tuple[str, ...]:
    expanded: set[str] = set()
    for target in raw_targets:
        value = target.strip().lower()
        if not value:
            continue
        if value in SKILL_TARGET_ORDER:
            expanded.add(value)
            continue
        if value in ("all", "core"):
            expanded.update(SKILL_TARGET_ORDER)
            continue
        if value == "runtime":
            if not remove_runtime:
                raise ValueError(
                    "Target 'runtime' requires --include-runtime for uninstall."
                )
            expanded.add("runtime")
            continue
        choices = ", ".join((*SKILL_TARGET_ORDER, "all", "core", "runtime"))
        raise ValueError(f"Unknown target '{target}'. Valid uninstall targets: {choices}")

    if not expanded:
        expanded.update(SKILL_TARGET_ORDER)

    if remove_runtime:
        expanded.add("runtime")

    order = ("runtime", *SKILL_TARGET_ORDER)
    return tuple(item for item in order if item in expanded)


def _has_assets(base_dir: Path) -> bool:
    return all((base_dir / name).is_dir() for name in ("skills", "templates", "workflows"))


@contextmanager
def _resolve_assets_dir():
    packaged_assets = resources.files("get_research_done").joinpath("assets")
    try:
        with resources.as_file(packaged_assets) as candidate:
            if _has_assets(candidate):
                yield candidate
                return
    except FileNotFoundError:
        pass

    repo_root = Path(__file__).resolve().parents[2]
    if _has_assets(repo_root):
        yield repo_root
        return

    raise FileNotFoundError(
        "Could not locate packaged assets (skills/templates/workflows)."
    )


def install_targets(dest: str | Path, targets: list[str] | tuple[str, ...]) -> InstallResult:
    resolved_dest = Path(dest).expanduser().resolve()
    resolved_dest.mkdir(parents=True, exist_ok=True)

    selected = _normalize_targets(list(targets))

    with _resolve_assets_dir() as assets_dir:
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
            target_dir = resolved_dest / relative_path
            _remove_legacy_skill_dirs(target_dir)
            _copy_skill_dirs(
                assets_dir / "skills",
                target_dir,
            )

    return InstallResult(dest=resolved_dest, installed_targets=selected)


def uninstall_targets(
    dest: str | Path,
    targets: list[str] | tuple[str, ...],
    *,
    remove_runtime: bool = False,
) -> UninstallResult:
    resolved_dest = Path(dest).expanduser().resolve()
    selected = _normalize_uninstall_targets(
        list(targets),
        remove_runtime=remove_runtime,
    )

    with _resolve_assets_dir() as assets_dir:
        if "runtime" in selected:
            _remove_tree_contents(
                assets_dir / "templates",
                resolved_dest / ".grd" / "templates",
            )
            _remove_tree_contents(
                assets_dir / "workflows",
                resolved_dest / ".grd" / "workflows",
            )
            _prune_empty_dirs(resolved_dest / ".grd" / "templates", resolved_dest)
            _prune_empty_dirs(resolved_dest / ".grd" / "workflows", resolved_dest)
            _prune_empty_dirs(resolved_dest / ".grd", resolved_dest)

        for target, relative_path in SKILL_TARGET_DIRS.items():
            if target not in selected:
                continue
            target_dir = resolved_dest / relative_path
            _remove_tree_contents(
                assets_dir / "skills",
                target_dir,
            )
            _remove_legacy_skill_dirs(target_dir)
            _prune_empty_dirs(target_dir, resolved_dest)

    return UninstallResult(dest=resolved_dest, removed_targets=selected)
