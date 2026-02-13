#!/usr/bin/env python3
"""Scaffold GRD state artifacts from bundled skill templates."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import sys
import shutil


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scaffold .grd state files and optional run index from templates."
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root where .grd artifacts should be created (default: current directory).",
    )
    parser.add_argument(
        "--template-root",
        default="",
        help=(
            "Optional explicit template directory. "
            "Defaults to shared templates (.grd/templates, then repo templates)."
        ),
    )
    parser.add_argument(
        "--workflow-root",
        default="",
        help=(
            "Optional explicit workflow directory. "
            "Defaults to repo workflows, then bundled skill assets."
        ),
    )
    parser.add_argument(
        "--init-templates",
        action="store_true",
        help="Initialize .grd/templates from shared or bundled templates.",
    )
    parser.add_argument(
        "--init-workflows",
        action="store_true",
        help="Initialize .grd/workflows from shared or bundled workflows.",
    )
    parser.add_argument(
        "--run-id",
        default="",
        help="Optional run id (for example: 260211_adaptive_basis).",
    )
    parser.add_argument(
        "--include-notes",
        action="store_true",
        help="Also scaffold .grd/research/RESEARCH_NOTES.md if missing.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing artifact files.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show planned changes without writing files.",
    )
    return parser.parse_args()


def render_template(content: str, template_name: str, run_id: str) -> str:
    now = datetime.now()
    today = now.strftime("%Y-%m-%d")
    timestamp = now.strftime("%Y-%m-%d %H:%M")

    if template_name == "state.md":
        content = content.replace("[YYYY-MM-DD HH:MM]", timestamp)
        content = content.replace("[0|1|2|3|4|5]", "0")
        content = content.replace("[YYMMDD_slug or empty]", "")
        if run_id:
            content = content.replace("[YYMMDD_slug or empty]", run_id)

    if template_name == "run-index.md":
        if run_id:
            content = content.replace('run_id: "YYMMDD_slug"', f'run_id: "{run_id}"')
        content = content.replace('"YYYY-MM-DD"', f'"{today}"')

    return content


def write_template(
    template_path: Path,
    target_path: Path,
    *,
    run_id: str,
    force: bool,
    dry_run: bool,
) -> None:
    existed_before = target_path.exists()
    if target_path.exists() and not force:
        print(f"skip existing: {target_path}")
        return

    rendered = render_template(
        template_path.read_text(encoding="utf-8"),
        template_path.name,
        run_id,
    )

    if dry_run:
        action = "overwrite" if existed_before else "create"
        print(f"would {action}: {target_path}")
        return

    target_path.parent.mkdir(parents=True, exist_ok=True)
    target_path.write_text(rendered, encoding="utf-8")
    action = "overwrote" if existed_before else "created"
    print(f"{action}: {target_path}")


def copy_file(
    source_path: Path,
    target_path: Path,
    *,
    force: bool,
    dry_run: bool,
) -> None:
    existed_before = target_path.exists()
    if existed_before and not force:
        print(f"skip existing: {target_path}")
        return

    if dry_run:
        action = "overwrite" if existed_before else "create"
        print(f"would {action}: {target_path}")
        return

    target_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_path, target_path)
    action = "overwrote" if existed_before else "created"
    print(f"{action}: {target_path}")


def resolve_template_path(
    template_name: str,
    *,
    repo_root: Path,
    skill_dir: Path,
    explicit_template_root: str,
) -> Path | None:
    if explicit_template_root:
        candidate = Path(explicit_template_root).expanduser().resolve() / template_name
        return candidate if candidate.exists() else None

    repo_templates = repo_root / ".grd" / "templates"
    local_repo_templates = skill_dir.parents[1] / "templates"
    skill_templates = skill_dir / "assets" / "templates"
    candidates = (
        repo_templates / template_name,
        local_repo_templates / template_name,
        skill_templates / template_name,
    )
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def resolve_template_source_dir(
    *,
    repo_root: Path,
    skill_dir: Path,
    explicit_template_root: str,
) -> Path | None:
    if explicit_template_root:
        candidate = Path(explicit_template_root).expanduser().resolve()
        return candidate if candidate.is_dir() else None

    candidates = (
        repo_root / ".grd" / "templates",
        skill_dir.parents[1] / "templates",
        skill_dir / "assets" / "templates",
    )
    for candidate in candidates:
        if candidate.is_dir():
            return candidate
    return None


def resolve_workflow_source_dir(
    *,
    skill_dir: Path,
    explicit_workflow_root: str,
) -> Path | None:
    if explicit_workflow_root:
        candidate = Path(explicit_workflow_root).expanduser().resolve()
        return candidate if candidate.is_dir() else None

    candidates = (
        skill_dir.parents[1] / "workflows",
        skill_dir / "assets" / "workflows",
    )
    for candidate in candidates:
        if candidate.is_dir():
            return candidate
    return None


def init_templates(
    *,
    repo_root: Path,
    skill_dir: Path,
    explicit_template_root: str,
    force: bool,
    dry_run: bool,
) -> bool:
    source_dir = resolve_template_source_dir(
        repo_root=repo_root,
        skill_dir=skill_dir,
        explicit_template_root=explicit_template_root,
    )
    if source_dir is None:
        return False

    target_dir = repo_root / ".grd" / "templates"
    for source_path in sorted(source_dir.iterdir()):
        if not source_path.is_file():
            continue
        copy_file(
            source_path,
            target_dir / source_path.name,
            force=force,
            dry_run=dry_run,
        )
    return True


def init_workflows(
    *,
    repo_root: Path,
    skill_dir: Path,
    explicit_workflow_root: str,
    force: bool,
    dry_run: bool,
) -> bool:
    source_dir = resolve_workflow_source_dir(
        skill_dir=skill_dir,
        explicit_workflow_root=explicit_workflow_root,
    )
    if source_dir is None:
        return False

    target_dir = repo_root / ".grd" / "workflows"
    for source_path in sorted(source_dir.iterdir()):
        if not source_path.is_file():
            continue
        copy_file(
            source_path,
            target_dir / source_path.name,
            force=force,
            dry_run=dry_run,
        )
    return True


def ensure_latest_symlink(
    repo_root: Path,
    run_id: str,
    *,
    dry_run: bool,
) -> None:
    latest_path = repo_root / ".grd" / "research" / "latest"
    link_target = Path("runs") / run_id

    if latest_path.exists() or latest_path.is_symlink():
        if latest_path.is_symlink() or latest_path.is_file():
            if dry_run:
                print(f"would replace link/file: {latest_path}")
            else:
                latest_path.unlink()
        else:
            print(
                f"skip latest alias (path is directory): {latest_path}",
                file=sys.stderr,
            )
            return

    if dry_run:
        print(f"would symlink: {latest_path} -> {link_target}")
        return

    latest_path.parent.mkdir(parents=True, exist_ok=True)
    latest_path.symlink_to(link_target)
    print(f"symlinked: {latest_path} -> {link_target}")


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).expanduser().resolve()
    run_id = args.run_id.strip()

    skill_dir = Path(__file__).resolve().parents[1]

    if args.init_templates:
        initialized = init_templates(
            repo_root=repo_root,
            skill_dir=skill_dir,
            explicit_template_root=args.template_root,
            force=args.force,
            dry_run=args.dry_run,
        )
        if not initialized:
            print(
                "could not initialize templates (searched explicit root, .grd/templates, repo templates, skill assets/templates)",
                file=sys.stderr,
            )
            return 2

    if args.init_workflows:
        initialized = init_workflows(
            repo_root=repo_root,
            skill_dir=skill_dir,
            explicit_workflow_root=args.workflow_root,
            force=args.force,
            dry_run=args.dry_run,
        )
        if not initialized:
            print(
                "could not initialize workflows (searched explicit root, repo workflows, skill assets/workflows)",
                file=sys.stderr,
            )
            return 2

    copy_plan: list[tuple[str, Path]] = [
        ("state.md", repo_root / ".grd" / "STATE.md"),
        ("roadmap.md", repo_root / ".grd" / "ROADMAP.md"),
    ]

    if args.include_notes:
        copy_plan.append(
            ("research-notes.md", repo_root / ".grd" / "research" / "RESEARCH_NOTES.md")
        )

    if run_id:
        copy_plan.append(
            (
                "run-index.md",
                repo_root / ".grd" / "research" / "runs" / run_id / "0_INDEX.md",
            )
        )

    for template_name, target_path in copy_plan:
        template_path = resolve_template_path(
            template_name,
            repo_root=repo_root,
            skill_dir=skill_dir,
            explicit_template_root=args.template_root,
        )
        if template_path is None:
            if args.template_root:
                searched = str(Path(args.template_root).expanduser().resolve())
            else:
                searched = ", ".join(
                    str(path)
                    for path in (
                        repo_root / ".grd" / "templates",
                        skill_dir.parents[1] / "templates",
                        skill_dir / "assets" / "templates",
                    )
                )
            print(
                f"missing template '{template_name}' (searched: {searched})",
                file=sys.stderr,
            )
            return 2
        write_template(
            template_path,
            target_path,
            run_id=run_id,
            force=args.force,
            dry_run=args.dry_run,
        )

    if run_id:
        ensure_latest_symlink(
            repo_root,
            run_id,
            dry_run=args.dry_run,
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
