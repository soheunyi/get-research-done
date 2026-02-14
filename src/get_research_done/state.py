from __future__ import annotations

import os
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


MODES = ("explore", "plan", "implement", "evaluate", "synthesize", "promote")


class StateContractError(ValueError):
    """Raised when `.grd` state contract is missing or malformed."""


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
    return path.read_text(encoding="utf-8")


def _slugify(text: str) -> str:
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower()).strip("-")
    return normalized or "hypothesis"


@dataclass(frozen=True)
class GrdContext:
    state: dict[str, Any]
    roadmap: str
    repo_root: Path

    def to_markdown(self, max_chars: int = 2400) -> str:
        roadmap_line = ""
        for line in self.roadmap.splitlines():
            if line.strip():
                roadmap_line = line.strip()
                break
        body = [
            "# GRD State Context",
            "",
            "## State",
            yaml.safe_dump(self.state, sort_keys=False).strip() or "{}",
            "",
            "## Roadmap (excerpt)",
            roadmap_line,
            "",
        ]
        output = "\n".join(body)
        if max_chars and len(output) > max_chars:
            return output[: max_chars - 3] + "..."
        return output

    def to_dict(self, include_markdown: bool = False, max_chars: int = 2400) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "state": self.state,
            "repo_root": str(self.repo_root),
        }
        if include_markdown:
            payload["markdown"] = self.to_markdown(max_chars=max_chars)
        return payload


class ResearchState:
    """Persistent state + artifact helpers for `.grd/`."""

    def __init__(self, root_dir: str | Path | None = None):
        self.root_dir = Path(root_dir or os.getcwd()).expanduser().resolve()
        self.research_dir = self.root_dir / ".grd"
        self.state_path = self._resolve_path("state.md", "STATE.md")
        self.roadmap_path = self._resolve_path("roadmap.md", "ROADMAP.md")
        self.journal_path = self.research_dir / "journal.md"
        self.experiments_path = self.research_dir / "experiments.md"
        self.hypotheses_dir = self.research_dir / "hypotheses"

    def _resolve_path(self, lower: str, upper: str) -> Path:
        lower_path = self.research_dir / lower
        upper_path = self.research_dir / upper
        if lower_path.exists():
            return lower_path
        if upper_path.exists():
            return upper_path
        return lower_path

    def _timestamp(self) -> str:
        return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    def load(self) -> dict[str, Any]:
        content = _load_markdown(self.state_path)
        parsed = _parse_frontmatter(content)
        if parsed:
            return parsed
        if content.strip():
            return {
                "state_format": "markdown",
                "state_path": str(self.state_path),
            }
        return {}

    def update(self, patches: dict[str, Any]) -> dict[str, Any]:
        state = dict(self.load())
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

        self.research_dir.mkdir(parents=True, exist_ok=True)
        with self.state_path.open("w", encoding="utf-8") as handle:
            handle.write("---\n")
            handle.write(yaml.safe_dump(state, sort_keys=False, default_flow_style=False))
            handle.write("---\n")
            handle.write(body)
        return state

    def append_journal(self, entry: str | dict[str, Any]) -> None:
        normalized = self._normalize_entry(entry, required=("what", "happened", "why"))
        self._append_markdown_entry(self.journal_path, normalized)

    def append_experiment(self, entry: str | dict[str, Any]) -> None:
        normalized = self._normalize_entry(entry, required=("what", "happened", "why"))
        self._append_markdown_entry(self.experiments_path, normalized)

    def _append_markdown_entry(self, path: Path, entry: dict[str, Any]) -> None:
        self.research_dir.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_text("", encoding="utf-8")
        lines = [f"## {self._timestamp()}", ""]
        for key, value in entry.items():
            if key == "artifacts":
                lines.append("- artifacts:")
                for item in value:
                    lines.append(f"  - {item}")
                continue
            lines.append(f"- {key}: {value if value is not None else ''}")
        block = "\n".join(lines).rstrip() + "\n"
        with path.open("a", encoding="utf-8") as handle:
            if path.stat().st_size > 0:
                handle.write("\n")
            handle.write(block)

    def _normalize_entry(self, entry: str | dict[str, Any], required: tuple[str, ...]) -> dict[str, Any]:
        if isinstance(entry, str):
            payload = {"what": entry.strip() or "(empty)", "happened": "(legacy)", "why": "(legacy)"}
        elif isinstance(entry, dict):
            payload = dict(entry)
        else:
            raise StateContractError("Entry must be a string or dictionary.")

        missing = [k for k in required if not str(payload.get(k, "")).strip()]
        if missing:
            raise StateContractError("Missing required fields: " + ", ".join(missing))

        normalized: dict[str, Any] = {k: str(payload[k]).strip() for k in required}
        for key in ("notes", "source", "outcome"):
            if str(payload.get(key, "")).strip():
                normalized[key] = str(payload[key]).strip()
        artifacts = payload.get("artifacts")
        if artifacts:
            if isinstance(artifacts, list):
                normalized["artifacts"] = [str(a).strip() for a in artifacts if str(a).strip()]
            else:
                normalized["artifacts"] = [str(artifacts).strip()]
        return normalized

    def promote_hypothesis(self, entry: dict[str, Any]) -> dict[str, Any]:
        normalized = self._normalize_hypothesis(entry)
        created = self._timestamp()
        stamp = created.replace("-", "").replace(":", "").replace("T", "-").replace("Z", "")
        slug = _slugify(normalized["title"])

        self.hypotheses_dir.mkdir(parents=True, exist_ok=True)
        artifact_path = self.hypotheses_dir / f"{stamp}-{slug}.md"

        state = self.load()
        phase_hint = str(state.get("current_phase", "unknown")) if isinstance(state, dict) else "unknown"
        record = {
            "title": normalized["title"],
            "created": created,
            "phase_hint": phase_hint,
            "source_entry": normalized.get("source_entry"),
            "tags": normalized.get("tags", []),
            "artifacts": normalized.get("artifacts", []),
            "what": normalized["what"],
            "happened": normalized["happened"],
            "why": normalized["why"],
            "notes": normalized.get("notes", ""),
            "path": str(artifact_path),
        }

        artifact_path.write_text(self.render_hypothesis_markdown(record), encoding="utf-8")
        return record

    def _normalize_hypothesis(self, entry: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(entry, dict):
            raise StateContractError("Hypothesis payload must be a dictionary.")
        required = ("title", "what", "happened", "why")
        missing = [k for k in required if not str(entry.get(k, "")).strip()]
        if missing:
            raise StateContractError("Missing required hypothesis fields: " + ", ".join(missing))

        tags_raw = entry.get("tags", [])
        if isinstance(tags_raw, list):
            tags = [str(t).strip() for t in tags_raw if str(t).strip()]
        elif str(tags_raw).strip():
            tags = [s.strip() for s in str(tags_raw).split(",") if s.strip()]
        else:
            tags = []

        artifacts_raw = entry.get("artifacts", [])
        if isinstance(artifacts_raw, list):
            artifacts = [str(a).strip() for a in artifacts_raw if str(a).strip()]
        elif str(artifacts_raw).strip():
            artifacts = [str(artifacts_raw).strip()]
        else:
            artifacts = []

        return {
            "title": str(entry["title"]).strip(),
            "what": str(entry["what"]).strip(),
            "happened": str(entry["happened"]).strip(),
            "why": str(entry["why"]).strip(),
            "source_entry": str(entry.get("source_entry", "")).strip() or None,
            "notes": str(entry.get("notes", "")).strip(),
            "tags": tags,
            "artifacts": artifacts,
        }

    def render_hypothesis_markdown(self, record: dict[str, Any]) -> str:
        frontmatter = {
            "title": record["title"],
            "created": record["created"],
            "phase_hint": record.get("phase_hint", "unknown"),
            "source_entry": record.get("source_entry"),
            "tags": record.get("tags", []),
            "artifacts": record.get("artifacts", []),
        }
        lines = [
            "---",
            yaml.safe_dump(frontmatter, sort_keys=False, default_flow_style=False).rstrip(),
            "---",
            "",
            f"# {record['title']}",
            "",
            "## Hypothesis Statement",
            f"- what: {record['what']}",
            f"- happened: {record['happened']}",
            f"- why: {record['why']}",
            "",
            "## Supporting Exploration Evidence",
            f"- source_entry: {record.get('source_entry') or 'manual'}",
            f"- notes: {record.get('notes', '')}",
            "- artifacts:",
        ]
        artifacts = record.get("artifacts", [])
        if artifacts:
            for artifact in artifacts:
                lines.append(f"  - {artifact}")
        else:
            lines.append("  - (none)")
        lines.extend(
            [
                "",
                "## Expected Validation Path",
                "- [ ] Define success metric",
                "- [ ] Run focused validation experiment",
                "- [ ] Record pass/fail decision",
                "",
            ]
        )
        return "\n".join(lines)

    def render_hypothesis_view(self, record: dict[str, Any]) -> str:
        return "\n".join(
            [
                "Unified Hypothesis Format",
                f"- title: {record['title']}",
                f"- created: {record['created']}",
                f"- source_entry: {record.get('source_entry') or 'manual'}",
                f"- what: {record['what']}",
                f"- happened: {record['happened']}",
                f"- why: {record['why']}",
                f"- artifacts: {', '.join(record.get('artifacts', [])) if record.get('artifacts') else '(none)'}",
                f"- path: {record['path']}",
            ]
        )


def load_context(root_dir: str | Path) -> GrdContext:
    repo_root = Path(root_dir).expanduser().resolve()
    rs = ResearchState(root_dir=repo_root)
    state = rs.load()
    if not state:
        raise StateContractError("Missing or unreadable `.grd/state.md` or `.grd/STATE.md`.")
    roadmap = _load_markdown(rs.roadmap_path)
    if not roadmap:
        raise StateContractError("Missing `.grd/roadmap.md` or `.grd/ROADMAP.md`.")
    return GrdContext(state=state, roadmap=roadmap, repo_root=repo_root)
