import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def extract_video_id(url: str) -> str:
    match = re.search(r"(?:v=|youtu\.be/)([\w-]+)", url)
    if not match:
        raise ValueError("Could not extract a YouTube video id from the URL")
    return match.group(1)


def crunch_summary(stdout: str, stderr: str) -> str:
    for line in reversed(stdout.splitlines()):
        stripped = line.strip()
        if stripped:
            return stripped
    if stderr.strip():
        return stderr.strip()
    return "No output"


def append_log(log_path: Path, status: str, url: str, summary: str) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"
    line = f"{timestamp} | manual-youtube | {status} | {url} | {summary}"
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")
    print(line)


def update_processed(processed_path: Path, video_meta: dict, status: str) -> None:
    processed_path.parent.mkdir(parents=True, exist_ok=True)
    if not processed_path.exists():
        processed_path.write_text("[]", encoding="utf-8")
    data = json.loads(processed_path.read_text(encoding="utf-8"))
    ids = {entry.get("id") for entry in data if entry.get("id")}
    if video_meta.get("id") in ids:
        return
    entry = {
        "id": video_meta.get("id"),
        "channel": video_meta.get("channel"),
        "title": video_meta.get("title"),
        "processed_at": datetime.utcnow().isoformat(),
        "status": status,
    }
    data.append(entry)
    processed_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_meta(meta_path: Path) -> dict:
    if not meta_path.exists():
        return {}
    try:
        return json.loads(meta_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: python scripts/ingest_youtube_url.py <youtube-url>")
        return 1
    url = sys.argv[1]
    workspace = Path(__file__).resolve().parents[1]
    log_path = workspace / "memory" / "youtube_cron_runs.md"
    processed_path = workspace / "knowledge" / "processed-videos.json"
    try:
        video_id = extract_video_id(url)
    except ValueError as exc:
        print(exc)
        append_log(log_path, "FAIL", url, str(exc))
        return 1

    target_meta = workspace / "knowledge" / "youtube" / video_id / "meta.json"
    cmd = [sys.executable, str(workspace / "scripts" / "youtube_to_knowledge.py"), url]
    process = subprocess.run(cmd, capture_output=True, text=True)
    summary = crunch_summary(process.stdout, process.stderr)
    status = "SUCCESS" if process.returncode == 0 else "FAIL"
    append_log(log_path, status, url, summary)

    if process.returncode == 0:
        meta = load_meta(target_meta)
        update_processed(processed_path, meta or {"id": video_id, "title": ""}, "manual")
    else:
        print(process.stderr.strip(), file=sys.stderr)
    return process.returncode


if __name__ == "__main__":
    raise SystemExit(main())
