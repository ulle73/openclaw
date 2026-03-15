from __future__ import annotations

import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import output_bus
except ModuleNotFoundError:
    from scripts import output_bus


def ensure_utf8_output() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass


ensure_utf8_output()


def append_log(path: Path, status: str, summary: str) -> None:
    timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    line = f"{timestamp} | github_trends_cron | {status} | {summary}"
    with path.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")


def main() -> int:
    workspace = Path(__file__).resolve().parents[1]
    log_file = workspace / "memory" / "github_trends_runs.md"
    log_file.parent.mkdir(parents=True, exist_ok=True)

    process = subprocess.run(
        [sys.executable, str(workspace / "scripts" / "github_trends_watcher.py"), "scan"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )

    stdout = (process.stdout or "").strip()
    stderr = (process.stderr or "").strip()
    summary = stdout.splitlines()[0] if stdout else stderr or "No output"
    status = "SUCCESS" if process.returncode == 0 else "FAIL"
    append_log(log_file, status, summary)

    if process.returncode != 0:
        detail = stderr or stdout or "GitHub Trends cron failed without output."
        output_bus.fanout_text(
            "ops-alerts",
            output_bus.build_ops_alert("GitHub Trends watcher", detail),
        )
        print(detail)
        return process.returncode

    output_bus.fanout_text("radar-feed", stdout)
    print(stdout)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
