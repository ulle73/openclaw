from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import output_bus
except ModuleNotFoundError:
    from scripts import output_bus


WORKSPACE = Path(__file__).resolve().parents[1]


def ensure_utf8_output() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass


ensure_utf8_output()


def resolve_openclaw_cli() -> str:
    for name in ("openclaw", "openclaw.cmd", "openclaw.exe"):
        resolved = shutil.which(name)
        if resolved:
            return resolved
    raise RuntimeError("openclaw CLI not found in PATH")


def extract_text(payload: dict) -> str:
    items = payload.get("result", {}).get("payloads", [])
    texts: list[str] = []
    for item in items:
        text = (item or {}).get("text")
        if isinstance(text, str) and text.strip():
            texts.append(text.strip())
    return "\n\n".join(texts).strip()


def run_agent(agent_id: str, message: str, thinking: str | None = None) -> tuple[int, str, str]:
    cli = resolve_openclaw_cli()
    command = [
        cli,
        "agent",
        "--agent",
        agent_id,
        "--message",
        message,
        "--json",
    ]
    if thinking:
        command.extend(["--thinking", thinking])

    process = subprocess.run(
        command,
        capture_output=True,
        text=True,
        cwd=WORKSPACE,
    )
    stdout = (process.stdout or "").strip()
    stderr = (process.stderr or "").strip()
    if process.returncode != 0:
        return process.returncode, "", stderr or stdout

    try:
        payload = json.loads(stdout)
    except json.JSONDecodeError:
        raw_text = stdout.strip()
        if raw_text:
            return 0, raw_text, ""
        return 1, "", f"Invalid JSON from openclaw agent: {stdout[:500]}"

    text = extract_text(payload)
    if not text:
        return 1, "", "Agent returned no text payload"
    return 0, text, ""


def build_failure(agent_id: str, detail: str) -> str:
    return output_bus.build_ops_alert(
        f"Agent delegation: {agent_id}",
        detail,
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run an OpenClaw agent turn and fan out the reply to that agent's lane.",
    )
    parser.add_argument("--agent", required=True, help="Agent id: boss, radar, codey, or moneymaker")
    parser.add_argument("--message", required=True, help="Prompt to send to the target agent")
    parser.add_argument("--thinking", default=None, help="Optional thinking level")
    parser.add_argument("--silent", action="store_true", help="Send quietly where supported")
    args = parser.parse_args()

    returncode, text, error = run_agent(args.agent, args.message, thinking=args.thinking)
    if returncode != 0:
        output_bus.fanout_text("ops-alerts", build_failure(args.agent, error or "Unknown error"))
        print(error or "Delegation failed")
        return returncode

    output_bus.fanout_agent_message(args.agent, text, silent=args.silent)
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
