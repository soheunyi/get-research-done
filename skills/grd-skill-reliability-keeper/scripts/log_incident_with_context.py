#!/usr/bin/env python3
"""Append a structured skill incident entry with recent local chat context.

This script reads session snapshots/streams under ~/.codex/sessions, captures the most recent
N chats, and appends a structured incident entry to .grd/SKILL_FEEDBACK_LOG.md.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class ChatSnapshot:
    session_id: str
    ts: int
    snippets: list[str]


def _default_codex_home() -> Path:
    return Path.home() / ".codex"


def _to_iso_utc(ts: int) -> str:
    return dt.datetime.fromtimestamp(ts, tz=dt.timezone.utc).isoformat()


def _clean_snippet(text: str, max_len: int = 400) -> str:
    collapsed = " ".join(text.split())
    if len(collapsed) <= max_len:
        return collapsed
    return collapsed[: max_len - 3] + "..."


def _dedupe_preserve_order(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        out.append(item)
    return out


def _is_assistant_snippet(text: str) -> bool:
    return text.startswith("[assistant] ")


def _limit_mixed_snippets(snippets: list[str], max_total: int) -> list[str]:
    if max_total <= 0:
        return []
    assistant_cap = max(1, max_total // 2)
    out: list[str] = []
    assistant_count = 0

    # Pass 1: keep chronological order while respecting assistant cap.
    deferred_assistant: list[str] = []
    for s in snippets:
        if len(out) >= max_total:
            break
        if _is_assistant_snippet(s):
            if assistant_count < assistant_cap:
                out.append(s)
                assistant_count += 1
            else:
                deferred_assistant.append(s)
            continue
        out.append(s)

    # Pass 2: backfill with deferred assistants if there are remaining slots.
    for s in deferred_assistant:
        if len(out) >= max_total:
            break
        out.append(s)
    # Keep chronological readability in the log: oldest -> newest.
    return list(reversed(out))


def _extract_user_texts(content: object) -> list[str]:
    texts: list[str] = []
    if not isinstance(content, list):
        return texts
    for item in content:
        if not isinstance(item, dict):
            continue
        if item.get("type") != "input_text":
            continue
        text = item.get("text")
        if isinstance(text, str) and text.strip():
            texts.append(text)
    return texts


def _extract_assistant_texts(content: object) -> list[str]:
    texts: list[str] = []
    if not isinstance(content, list):
        return texts
    for item in content:
        if not isinstance(item, dict):
            continue
        if item.get("type") != "output_text":
            continue
        text = item.get("text")
        if isinstance(text, str) and text.strip():
            texts.append(text)
    return texts


def _parse_iso_ts(value: object) -> int | None:
    if not isinstance(value, str):
        return None
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return None
    return int(parsed.timestamp())


def _iter_jsonl_rows(path: Path) -> Iterable[dict]:
    try:
        with path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(row, dict):
                    yield row
    except Exception:
        return


def _extract_snapshot_from_json_file(path: Path) -> ChatSnapshot | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    if not isinstance(payload, dict):
        return None

    session = payload.get("session")
    if not isinstance(session, dict):
        return None
    session_id = session.get("id")
    if not isinstance(session_id, str):
        return None

    ts_int = _parse_iso_ts(session.get("timestamp")) or int(path.stat().st_mtime)
    items = payload.get("items")
    texts: list[str] = []
    if isinstance(items, list):
        for item in reversed(items):
            if not isinstance(item, dict):
                continue
            if item.get("type") != "message":
                continue
            role = item.get("role")
            if role == "user":
                texts.extend([f"[user] {t}" for t in _extract_user_texts(item.get("content"))])
            elif role == "assistant":
                texts.extend(
                    [f"[assistant] {t}" for t in _extract_assistant_texts(item.get("content"))]
                )

    if not texts:
        return None
    return ChatSnapshot(session_id=session_id, ts=ts_int, snippets=texts)


def _extract_snapshot_from_jsonl_file(path: Path) -> ChatSnapshot | None:
    session_id: str | None = None
    fallback_ts: int | None = None
    texts: list[str] = []

    for row in _iter_jsonl_rows(path):
        row_type = row.get("type")
        payload = row.get("payload")
        row_ts = _parse_iso_ts(row.get("timestamp"))
        if row_ts is not None:
            fallback_ts = max(fallback_ts or row_ts, row_ts)

        if row_type == "session_meta" and isinstance(payload, dict):
            sid = payload.get("id")
            if isinstance(sid, str):
                session_id = sid
            meta_ts = _parse_iso_ts(payload.get("timestamp"))
            if meta_ts is not None:
                fallback_ts = max(fallback_ts or meta_ts, meta_ts)
            continue

        if not isinstance(payload, dict):
            continue

        # Current Desktop format: user messages are emitted as event_msg/user_message.
        if row_type == "event_msg" and payload.get("type") == "user_message":
            message = payload.get("message")
            if isinstance(message, str) and message.strip():
                texts.append(f"[user] {message}")
            continue

        if row_type == "event_msg" and payload.get("type") == "agent_message":
            message = payload.get("message")
            if isinstance(message, str) and message.strip():
                texts.append(f"[assistant] {message}")
            continue

        # Keep compatibility with response stream messages.
        if (
            row_type == "response_item"
            and payload.get("type") == "message"
            and payload.get("role") == "user"
        ):
            texts.extend([f"[user] {t}" for t in _extract_user_texts(payload.get("content"))])
            continue
        if (
            row_type == "response_item"
            and payload.get("type") == "message"
            and payload.get("role") == "assistant"
        ):
            texts.extend(
                [f"[assistant] {t}" for t in _extract_assistant_texts(payload.get("content"))]
            )

    if session_id is None:
        stem_parts = path.stem.split("-")
        if len(stem_parts) >= 5:
            session_id = "-".join(stem_parts[-5:])
    if not session_id:
        return None
    if not texts:
        return None

    ts_int = fallback_ts or int(path.stat().st_mtime)
    # jsonl stream is oldest -> newest; keep snippets newest first.
    return ChatSnapshot(session_id=session_id, ts=ts_int, snippets=list(reversed(texts)))


def _safe_mtime(path: Path) -> float:
    try:
        return path.stat().st_mtime
    except Exception:
        return 0.0


def _iter_session_candidate_files(
    sessions_dir: Path,
    session_id_filter: str | None = None,
) -> Iterable[Path]:
    seen: set[Path] = set()

    # Fast path when we know the session id: locate likely files first.
    if session_id_filter:
        targeted: list[Path] = []
        for ext in ("jsonl", "json"):
            pattern = f"**/*{session_id_filter}*.{ext}"
            targeted.extend(sessions_dir.glob(pattern))
        for path in sorted(targeted, key=_safe_mtime, reverse=True):
            if path in seen or not path.is_file():
                continue
            seen.add(path)
            yield path

    # Date-partitioned layout: sessions/YYYY/MM/DD/*
    years = sorted(
        [p for p in sessions_dir.iterdir() if p.is_dir() and p.name.isdigit() and len(p.name) == 4],
        key=lambda p: int(p.name),
        reverse=True,
    )
    for year_dir in years:
        months = sorted(
            [p for p in year_dir.iterdir() if p.is_dir() and p.name.isdigit()],
            key=lambda p: int(p.name),
            reverse=True,
        )
        for month_dir in months:
            days = sorted(
                [p for p in month_dir.iterdir() if p.is_dir() and p.name.isdigit()],
                key=lambda p: int(p.name),
                reverse=True,
            )
            for day_dir in days:
                files = sorted(
                    [
                        *day_dir.glob("*.jsonl"),
                        *day_dir.glob("*.json"),
                    ],
                    key=_safe_mtime,
                    reverse=True,
                )
                for path in files:
                    if path in seen or not path.is_file():
                        continue
                    seen.add(path)
                    yield path

    # Minimal fallback for legacy flat layout (top-level files only).
    legacy = sorted(
        [*sessions_dir.glob("*.jsonl"), *sessions_dir.glob("*.json")],
        key=_safe_mtime,
        reverse=True,
    )
    for path in legacy:
        if path in seen or not path.is_file():
            continue
        seen.add(path)
        yield path


def _load_recent_from_sessions(
    sessions_dir: Path,
    chat_count: int,
    snippets_per_chat: int,
    snippet_max_len: int,
    session_id_filter: str | None = None,
) -> list[ChatSnapshot]:
    snapshots: list[ChatSnapshot] = []
    for path in _iter_session_candidate_files(
        sessions_dir=sessions_dir, session_id_filter=session_id_filter
    ):
        if len(snapshots) >= chat_count:
            break
        snap: ChatSnapshot | None
        if path.suffix == ".jsonl":
            snap = _extract_snapshot_from_jsonl_file(path)
        else:
            snap = _extract_snapshot_from_json_file(path)
        if snap is None:
            continue
        session_id = snap.session_id
        if session_id_filter is not None and session_id != session_id_filter:
            continue
        cleaned = [_clean_snippet(t, max_len=snippet_max_len) for t in snap.snippets]
        snippets = _limit_mixed_snippets(
            _dedupe_preserve_order(cleaned),
            snippets_per_chat,
        )
        snapshots.append(ChatSnapshot(session_id=session_id, ts=snap.ts, snippets=snippets))
    snapshots.sort(key=lambda s: s.ts, reverse=True)
    return snapshots[:chat_count]


def _resolve_chat_context(
    codex_home: Path,
    sessions_dir_override: Path | None,
    chat_count: int,
    snippets_per_chat: int,
    snippet_max_len: int,
    session_id: str | None,
) -> tuple[list[ChatSnapshot], str]:
    sessions_dir = sessions_dir_override or (codex_home / "sessions")

    if sessions_dir.exists():
        snapshots = _load_recent_from_sessions(
            sessions_dir,
            chat_count,
            snippets_per_chat,
            snippet_max_len,
            session_id_filter=session_id,
        )
        if snapshots:
            suffix = f"#{session_id}" if session_id else ""
            return snapshots, f"sessions:{sessions_dir}{suffix}"

    if session_id:
        return [], f"none (session_id `{session_id}` not found)"
    return [], "none"


def _resolve_current_session_id(
    codex_home: Path,
) -> str | None:
    # Prefer explicit env signals when available.
    for key in (
        "CODEX_THREAD_ID",
        "CODEX_SESSION_ID",
        "CODEX_CHAT_ID",
        "SESSION_ID",
        "CHAT_SESSION_ID",
    ):
        value = os.environ.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()

    sessions_dir = codex_home / "sessions"
    if sessions_dir.exists():
        snapshots = _load_recent_from_sessions(
            sessions_dir=sessions_dir,
            chat_count=1,
            snippets_per_chat=1,
            snippet_max_len=80,
            session_id_filter=None,
        )
        if snapshots:
            return snapshots[0].session_id
    return None


def _append_entry(
    log_path: Path,
    *,
    date_str: str,
    skill_name: str,
    priority: str,
    user_feedback_summary: list[str],
    expected_behavior: str,
    observed_behavior: str,
    suspected_root_cause: str,
    proposed_improvements: list[str],
    verification_status: str,
    snapshots: list[ChatSnapshot],
    context_source: str,
) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    if not log_path.exists():
        log_path.write_text("", encoding="utf-8")

    lines: list[str] = []
    lines.append("## Entry")
    lines.append(f"- Date: {date_str}")
    lines.append(f"- Skill name: `{skill_name}`")
    lines.append(f"- Priority: {priority}")
    lines.append("- User feedback summary:")
    for item in user_feedback_summary:
        lines.append(f"  - {item}")
    lines.append("- Expected behavior vs observed behavior:")
    lines.append(f"  - Expected: {expected_behavior}")
    lines.append(f"  - Observed: {observed_behavior}")
    lines.append("- Suspected root cause:")
    lines.append(f"  - {suspected_root_cause}")
    lines.append("- Proposed skill improvement:")
    for item in proposed_improvements:
        lines.append(f"  - {item}")
    lines.append("- Local chat context:")
    lines.append(f"  - Source: {context_source}")
    if not snapshots:
        lines.append("  - No local chat snapshots found.")
    else:
        lines.append(f"  - Captured chats: {len(snapshots)}")
        for idx, snap in enumerate(snapshots, start=1):
            lines.append(
                f"  - Chat {idx}: session `{snap.session_id}`, last_ts `{_to_iso_utc(snap.ts)}`"
            )
            for snippet in snap.snippets:
                lines.append(f"    - {snippet}")
    lines.append("- Verification follow-up status:")
    lines.append(f"  - {verification_status}")
    lines.append("")

    existing = log_path.read_text(encoding="utf-8")
    prefix = "" if not existing.strip() else ("\n" if existing.endswith("\n") else "\n\n")
    with log_path.open("a", encoding="utf-8") as f:
        f.write(prefix + "\n".join(lines))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Append skill reliability feedback with local chat context."
    )
    parser.add_argument("--repo-root", default=".", help="Repository root path.")
    parser.add_argument("--log-path", default=".grd/SKILL_FEEDBACK_LOG.md")
    parser.add_argument("--codex-home", default=str(_default_codex_home()))
    parser.add_argument("--sessions-dir", default=None)
    parser.add_argument("--chat-count", type=int, default=5)
    parser.add_argument("--snippets-per-chat", type=int, default=2)
    parser.add_argument(
        "--snippet-max-len",
        type=int,
        default=400,
        help="Maximum characters per captured snippet (minimum 80).",
    )
    parser.add_argument(
        "--session-id",
        default=None,
        help=(
            "Optional target chat/session hash. If provided, only this session is captured. "
            "Use '@current' to auto-resolve the latest/current local session id."
        ),
    )
    parser.add_argument(
        "--print-current-session-id",
        action="store_true",
        help="Print resolved current session id and exit.",
    )

    parser.add_argument("--date", dest="date_str", default=dt.date.today().isoformat())
    parser.add_argument("--skill-name")
    parser.add_argument("--priority", choices=("high", "medium", "low"))
    parser.add_argument(
        "--user-feedback-summary",
        action="append",
        required=False,
        help="Repeat for multiple bullet items.",
    )
    parser.add_argument("--expected")
    parser.add_argument("--observed")
    parser.add_argument("--suspected-root-cause")
    parser.add_argument(
        "--proposed-improvement",
        action="append",
        required=False,
        help="Repeat for multiple bullet items.",
    )
    parser.add_argument("--verification-status")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    log_path = (repo_root / args.log_path).resolve()
    codex_home = Path(args.codex_home).expanduser().resolve()
    sessions_dir = Path(args.sessions_dir).expanduser().resolve() if args.sessions_dir else None
    requested_session_id = args.session_id
    if requested_session_id == "@current":
        requested_session_id = _resolve_current_session_id(
            codex_home=codex_home,
        )

    snippet_max_len = max(80, int(args.snippet_max_len))

    if args.print_current_session_id:
        current = _resolve_current_session_id(
            codex_home=codex_home,
        )
        print(current or "")
        return 0

    missing: list[str] = []
    if not args.skill_name:
        missing.append("--skill-name")
    if not args.priority:
        missing.append("--priority")
    if not args.user_feedback_summary:
        missing.append("--user-feedback-summary")
    if not args.expected:
        missing.append("--expected")
    if not args.observed:
        missing.append("--observed")
    if not args.suspected_root_cause:
        missing.append("--suspected-root-cause")
    if not args.proposed_improvement:
        missing.append("--proposed-improvement")
    if not args.verification_status:
        missing.append("--verification-status")
    if missing:
        print(f"Missing required arguments: {', '.join(missing)}")
        return 2

    snapshots, context_source = _resolve_chat_context(
        codex_home=codex_home,
        sessions_dir_override=sessions_dir,
        chat_count=max(1, args.chat_count),
        snippets_per_chat=max(1, args.snippets_per_chat),
        snippet_max_len=snippet_max_len,
        session_id=requested_session_id,
    )

    _append_entry(
        log_path,
        date_str=args.date_str,
        skill_name=args.skill_name,
        priority=args.priority,
        user_feedback_summary=args.user_feedback_summary,
        expected_behavior=args.expected,
        observed_behavior=args.observed,
        suspected_root_cause=args.suspected_root_cause,
        proposed_improvements=args.proposed_improvement,
        verification_status=args.verification_status,
        snapshots=snapshots,
        context_source=context_source,
    )
    print(f"Appended entry: {log_path}")
    print(f"Chat context source: {context_source}")
    print(f"Chats captured: {len(snapshots)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
