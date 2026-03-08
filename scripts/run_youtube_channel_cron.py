import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def main() -> int:
    workspace = Path(__file__).resolve().parents[1]
    target_script = workspace / "scripts" / "youtube_channel_cron.py"
    memory_dir = workspace / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)
    memory_log = memory_dir / "youtube_cron_runs.md"

    process = subprocess.run(
        [sys.executable, str(target_script)],
        capture_output=True,
        text=True,
    )

    stdout = process.stdout.strip()
    stderr = process.stderr.strip()

    summary_line = None
    for line in reversed(stdout.splitlines()):
        stripped = line.strip()
        if stripped:
            summary_line = stripped
            break

    if not summary_line:
        summary_line = stderr or stdout or "No output"

    if process.returncode != 0 and stderr:
        summary_line = f"{summary_line} | stderr: {stderr}"

    status = "SUCCESS" if process.returncode == 0 else "FAIL"
    timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat() + "Z"
    log_line = f"{timestamp} | youtube_channel_cron | {status} | {summary_line}"

    with memory_log.open("a", encoding="utf-8") as fh:
        fh.write(log_line + "\n")

    print(log_line)
    if stdout:
        print(stdout)
    if stderr:
        print(stderr, file=sys.stderr)

    return process.returncode


if __name__ == "__main__":
    raise SystemExit(main())
