from __future__ import annotations

import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


class StateContractError(ValueError):
    """Raised when the state payload does not satisfy required fields."""


def _parse_frontmatter(content: str) -> dict[str, Any]:
    if not content.startswith("---"):
        return {}
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}
    parsed = yaml.safe_load(parts[1]) or {}
    return parsed if isinstance(parsed, dict) else {}


def _load_markdown(path: Path) -> str:
    if not path.exists():
        return ""
    with path.open("r", encoding="utf-8") as handle:
        return handle.read()


def _slugify(text: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower()).strip("-")
    return normalized or "hypothesis"


@dataclass(frozen=True)
class GrdContext:
    state: dict[str, Any]
    roadmap: str
    repo_root: Path

    def to_markdown(self, max_chars: int = 2400) -> str:
        roadmap_line = self._first_nonempty_line(self.roadmap)
        parts = [
            "# GRD State Context",
            "",
            "## State",
            yaml.safe_dump(self.state, sort_keys=False).strip() or "{}",
            "",
            "## Roadmap (excerpt)",
            roadmap_line,
        ]
        content = "\n".join(parts).strip() + "\n"
        if max_chars and len(content) > max_chars:
            return content[: max_chars - 3] + "..."
        return content

    def to_dict(
        self,
        include_markdown: bool = False,
        max_chars: int = 2400,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "state": self.state,
            "roadmap_excerpt": self._first_nonempty_line(self.roadmap),
            "repo_root": str(self.repo_root),
        }
        if include_markdown:
            payload["markdown"] = self.to_markdown(max_chars=max_chars)
        return payload

    @staticmethod
    def _first_nonempty_line(text: str) -> str:
        for raw_line in text.splitlines():
            if raw_line.strip():
                return raw_line.strip()
        return ""


class ResearchState:
    """Persistent state and logging helpers for .grd artifacts."""

    def __init__(self, root_dir=None):
        self.root_dir = Path(root_dir or os.getcwd()).expanduser().resolve()
        self.grd_dir = self.root_dir / ".grd"
        self.state_path = self._resolve_path("state.md", "STATE.md")
        self.journal_path = self.grd_dir / "journal.md"
        self.experiments_path = self.grd_dir / "experiments.md"
        self.hypotheses_dir = self.grd_dir / "hypotheses"

    def _resolve_path(self, *candidates: str) -> Path:
        for name in candidates:
            path = self.grd_dir / name
            if path.exists():
                return path
        return self.grd_dir / candidates[0]

    def load(self):
        """Loads frontmatter from state.md / STATE.md."""
        content = _load_markdown(self.state_path)
        return _parse_frontmatter(content)

    def update(self, patches):
        """Updates fields in state frontmatter."""
        state = dict(self.load())
        if not isinstance(state, dict):
            state = {}
        state.update(patches)
        state["last_update"] = datetime.now(timezone.utc).date().isoformat()

        content = _load_markdown(self.state_path)
        body = ""
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                body = parts[2]
        else:
            body = content

        self.grd_dir.mkdir(parents=True, exist_ok=True)
        if not self.state_path.exists():
            body = content

        with self.state_path.open("w", encoding="utf-8") as handle:
            handle.write("---\n")
            handle.write(yaml.safe_dump(state, sort_keys=False, default_flow_style=False))
            handle.write("---\n")
            handle.write(body)
        return state

    def append_journal(self, entry: str | dict[str, Any]):
        """Append a structured exploration entry to journal.md."""
        normalized = self._normalize_entry(entry, required=("what", "happened", "why"))
        self._append_markdown_entry(self.journal_path, normalized)

    def append_experiment(self, entry: str | dict[str, Any]):
        """Append an outcome-focused experiment entry to experiments.md."""
        normalized = self._normalize_entry(
            entry,
            required=("what", "happened", "why"),
        )
        self._append_markdown_entry(self.experiments_path, normalized)

    def promote_hypothesis(self, entry: dict[str, Any]) -> Path:
        """Promote exploration evidence into a formal hypothesis artifact."""
        normalized = self._normalize_promotion_entry(entry)
        created = self._timestamp()
        stamp = created.replace("-", "").replace(":", "").replace("T", "-").replace("Z", "")
        slug = _slugify(normalized["title"])

        self.hypotheses_dir.mkdir(parents=True, exist_ok=True)
        artifact_path = self.hypotheses_dir / f"{stamp}-{slug}.md"

        state = self.load()
        phase_hint = str(state.get("current_phase", "unknown")) if isinstance(state, dict) else "unknown"

        frontmatter = {
            "title": normalized["title"],
            "created": created,
            "phase_hint": phase_hint,
            "source_entry": normalized.get("source_entry"),
            "tags": normalized.get("tags", []),
            "artifacts": normalized.get("artifacts", []),
        }

        body = [
            f"# {normalized['title']}",
            "",
            "## Hypothesis Statement",
            f"- what: {normalized['what']}",
            f"- happened: {normalized['happened']}",
            f"- why: {normalized['why']}",
            "",
            "## Supporting Exploration Evidence",
            f"- source_entry: {normalized.get('source_entry', 'manual')}",
            f"- notes: {normalized.get('notes', '')}",
            "- artifacts:",
        ]

        artifacts = normalized.get("artifacts", [])
        if artifacts:
            for artifact in artifacts:
                body.append(f"  - {artifact}")
        else:
            body.append("  - (none)")

        body.extend(
            [
                "",
                "## Expected Validation Path",
                "- [ ] Define success metric",
                "- [ ] Run targeted experiment",
                "- [ ] Record pass/fail decision",
                "",
            ]
        )

        with artifact_path.open("w", encoding="utf-8") as handle:
            handle.write("---\n")
            handle.write(yaml.safe_dump(frontmatter, sort_keys=False, default_flow_style=False))
            handle.write("---\n\n")
            handle.write("\n".join(body))

        return artifact_path

    def _normalize_promotion_entry(self, entry: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(entry, dict):
            raise StateContractError("Promotion payload must be a dictionary.")

        required = ("title", "what", "happened", "why")
        missing = [key for key in required if not str(entry.get(key, "")).strip()]
        if missing:
            raise StateContractError(
                "Missing required promotion fields: " + ", ".join(missing)
            )

        normalized: dict[str, Any] = {
            "title": str(entry["title"]).strip(),
            "what": str(entry["what"]).strip(),
            "happened": str(entry["happened"]).strip(),
            "why": str(entry["why"]).strip(),
            "source_entry": str(entry.get("source_entry", "")).strip() or None,
            "notes": str(entry.get("notes", "")).strip() or "",
        }

        tags = entry.get("tags", [])
        if isinstance(tags, list):
            normalized["tags"] = [str(tag).strip() for tag in tags if str(tag).strip()]
        elif str(tags).strip():
            normalized["tags"] = [tag.strip() for tag in str(tags).split(",") if tag.strip()]
        else:
            normalized["tags"] = []

        artifacts = entry.get("artifacts", [])
        if isinstance(artifacts, list):
            normalized["artifacts"] = [str(item).strip() for item in artifacts if str(item).strip()]
        elif str(artifacts).strip():
            normalized["artifacts"] = [str(artifacts).strip()]
        else:
            normalized["artifacts"] = []

        return normalized

    def _append_markdown_entry(self, path: Path, entry: dict[str, Any]) -> None:
        self.grd_dir.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_text("", encoding="utf-8")

        block = self._render_entry_block(entry)
        with path.open("a", encoding="utf-8") as handle:
            if path.stat().st_size > 0:
                handle.write("\n")
            handle.write(block)

    def _render_entry_block(self, entry: dict[str, Any]) -> str:
        lines: list[str] = [f"## {self._timestamp()}", ""]
        ordered = list(entry.items())
        for key, value in ordered:
            if key == "artifacts":
                lines.append(f"- {key}:")
                values = value if isinstance(value, list) else [value]
                for item in values:
                    if item is None:
                        continue
                    lines.append(f"  - {item}")
                continue
            lines.append(f"- {key}: {value if value is not None else ''}")
        return "\n".join(lines).rstrip() + "\n"

    def _timestamp(self) -> str:
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
            "+00:00",
            "Z",
        )

    def _normalize_entry(
        self,
        entry: str | dict[str, Any],
        required: tuple[str, ...],
    ) -> dict[str, Any]:
        if isinstance(entry, str):
            payload = {
                "what": entry.strip() or "(empty)",
                "happened": "(legacy entry text)",
                "why": "(legacy entry text)",
            }
        elif isinstance(entry, dict):
            payload = dict(entry)
        else:
            raise StateContractError(
                "Entry payload must be a string or dictionary with what/happened/why."
            )

        missing = [key for key in required if not str(payload.get(key, "")).strip()]
        if missing:
            raise StateContractError(
                "Missing required logging fields: " + ", ".join(missing)
            )

        normalized: dict[str, Any] = {}
        allowed = {
            "what",
            "happened",
            "why",
            "notes",
            "artifact",
            "source",
            "tags",
            "outcome",
            "artifacts",
        }
        for key in required:
            normalized[key] = str(payload[key]).strip()

        for key in ("notes", "artifact", "source", "outcome"):
            if key in payload and str(payload[key]).strip():
                normalized[key] = str(payload[key]).strip()

        if "tags" in payload and payload["tags"]:
            tags = payload["tags"]
            normalized["tags"] = (
                tags
                if isinstance(tags, list)
                else [tag.strip() for tag in str(tags).split(",") if tag.strip()]
            )

        if "artifacts" in payload and payload["artifacts"]:
            artifacts = payload["artifacts"]
            if isinstance(artifacts, list):
                normalized["artifacts"] = artifacts
            else:
                normalized["artifacts"] = [str(artifacts)]

        normalized.setdefault("notes", None)
        for key, value in payload.items():
            if key in allowed and key not in normalized:
                normalized[key] = value

        return normalized


def _read_roadmap(path: Path) -> str:
    if path.exists():
        return _load_markdown(path)
    return ""


def load_context(root_dir: str | Path) -> GrdContext:
    repo_root = Path(root_dir).expanduser().resolve()
    state = ResearchState(root_dir=repo_root).load()
    if not state:
        raise StateContractError(
            "State contract invalid: missing or unreadable `.grd/state.md` / `.grd/STATE.md`."
        )

    roadmap_candidates = [repo_root / ".grd" / "ROADMAP.md", repo_root / ".grd" / "roadmap.md"]
    roadmap = ""
    for roadmap_path in roadmap_candidates:
        roadmap = _read_roadmap(roadmap_path)
        if roadmap:
            break

    if not roadmap:
        raise StateContractError(
            "State contract invalid: missing `.grd/ROADMAP.md` / `.grd/roadmap.md`."
        )
    return GrdContext(state=state, roadmap=roadmap, repo_root=repo_root)
