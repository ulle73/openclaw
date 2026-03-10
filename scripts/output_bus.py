from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path


WORKSPACE = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class DeliveryTarget:
    channel: str
    target: str
    thread_id: int | None = None


LANE_TARGETS: dict[str, list[DeliveryTarget]] = {
    "boss-desk": [
        DeliveryTarget(channel="discord", target="1480594494184488960"),
        DeliveryTarget(channel="telegram", target="-1003542162296", thread_id=1),
    ],
    "boss-briefing": [
        DeliveryTarget(channel="discord", target="1480594557698572461"),
        DeliveryTarget(channel="telegram", target="-1003542162296", thread_id=4),
    ],
    "radar-feed": [
        DeliveryTarget(channel="discord", target="1480594614758146089"),
        DeliveryTarget(channel="telegram", target="-1003542162296", thread_id=6),
    ],
    "codey-shipping": [
        DeliveryTarget(channel="discord", target="1480594661864116294"),
        DeliveryTarget(channel="telegram", target="-1003542162296", thread_id=8),
    ],
    "money-maker": [
        DeliveryTarget(channel="discord", target="1480594693141041193"),
        DeliveryTarget(channel="telegram", target="-1003542162296", thread_id=10),
    ],
    "ops-alerts": [
        DeliveryTarget(channel="discord", target="1480594733624721592"),
        DeliveryTarget(channel="telegram", target="-1003542162296", thread_id=12),
    ],
}

AGENT_LANES: dict[str, str] = {
    "boss": "boss-desk",
    "radar": "radar-feed",
    "codey": "codey-shipping",
    "moneymaker": "money-maker",
}


def _fanout_disabled() -> bool:
    value = os.environ.get("OPENCLAW_DISABLE_OUTPUT_FANOUT", "").strip().lower()
    return value in {"1", "true", "yes", "on"}


def _resolve_openclaw_cli() -> str | None:
    for name in ("openclaw", "openclaw.cmd", "openclaw.exe"):
        resolved = shutil.which(name)
        if resolved:
            return resolved
    return None


def send_text(target: DeliveryTarget, message: str, *, silent: bool = False) -> tuple[bool, str]:
    cli = _resolve_openclaw_cli()
    if not cli:
        return False, "openclaw CLI not found in PATH"

    command = [
        cli,
        "message",
        "send",
        "--channel",
        target.channel,
        "--target",
        target.target,
        "--message",
        message,
    ]

    if target.thread_id is not None:
        command.extend(["--thread-id", str(target.thread_id)])
    if silent and target.channel in {"telegram", "discord"}:
        command.append("--silent")

    process = subprocess.run(
        command,
        capture_output=True,
        text=True,
        cwd=WORKSPACE,
    )
    detail = (process.stdout or "").strip() or (process.stderr or "").strip()
    return process.returncode == 0, detail


def fanout_text(lane: str, message: str, *, silent: bool = False) -> list[dict]:
    if _fanout_disabled():
        return [{"lane": lane, "skipped": True, "detail": "fanout disabled by env"}]

    targets = LANE_TARGETS.get(lane, [])
    if not targets:
        return [{"lane": lane, "skipped": True, "detail": "unknown lane"}]

    results: list[dict] = []
    for target in targets:
        ok, detail = send_text(target, message, silent=silent)
        results.append(
            {
                "lane": lane,
                "channel": target.channel,
                "target": target.target,
                "thread_id": target.thread_id,
                "ok": ok,
                "detail": detail,
            }
        )
    return results


def lane_for_agent(agent_id: str) -> str | None:
    return AGENT_LANES.get((agent_id or "").strip().lower())


def fanout_agent_message(agent_id: str, message: str, *, silent: bool = False) -> list[dict]:
    lane = lane_for_agent(agent_id)
    if not lane:
        return [{"agent": agent_id, "skipped": True, "detail": "unknown agent lane"}]
    return fanout_text(lane, message, silent=silent)


def build_ops_alert(source: str, detail: str) -> str:
    lines = [
        "⚠️ Ops Alert",
        "",
        f"Källa: {source}",
    ]
    cleaned = (detail or "").strip()
    if cleaned:
        lines.extend(["", cleaned])
    return "\n".join(lines).strip()
