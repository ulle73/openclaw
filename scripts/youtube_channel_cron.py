import json
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

LEGACY_CHANNELS = [
    "https://youtube.com/@thekoerneroffice/videos",
    "https://youtube.com/@juliangoldieseo/videos",
    "https://youtube.com/@itssssss_jack/videos",
    "https://youtube.com/@gregisenberg/videos",
    "https://youtube.com/@rileybrownai/videos",
]

BASE = Path(__file__).resolve().parents[1]
PROFILE_FILE = BASE / "knowledge" / "companies" / "DEFAULT" / "YOUTUBE.md"
PROCESSED_FILE = BASE / "knowledge" / "processed-videos.json"
CHANNEL_STATE_FILE = BASE / "knowledge" / "channel-state.json"
INDEX_JSONL_FILE = BASE / "knowledge" / "youtube" / "INDEX.jsonl"
QUEUE_FILE = BASE / "knowledge" / "youtube" / "QUEUE.jsonl"
FAILURES_FILE = BASE / "knowledge" / "youtube" / "FAILURES.jsonl"
SCRIPT = BASE / "scripts" / "youtube_to_knowledge.py"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def ensure_json_file(path: Path, default) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        return
    path.write_text(json.dumps(default, ensure_ascii=False, indent=2), encoding="utf-8")


def ensure_jsonl_file(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text("", encoding="utf-8")


def load_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, FileNotFoundError):
        return default


def write_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = "\n".join(json.dumps(row, ensure_ascii=False) for row in rows)
    if content:
        content += "\n"
    path.write_text(content, encoding="utf-8")


def append_jsonl(path: Path, row: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def load_frontmatter_lines(path: Path) -> list[str]:
    if not path.exists():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return []
    frontmatter: list[str] = []
    for line in lines[1:]:
        if line.strip() == "---":
            break
        frontmatter.append(line)
    return frontmatter


def load_profile_settings() -> tuple[list[str], int, int]:
    channels: list[str] = []
    max_per_channel = 1
    backoff_hours = 2
    frontmatter = load_frontmatter_lines(PROFILE_FILE)
    capture_channels = False

    for raw_line in frontmatter:
        stripped = raw_line.strip()

        if stripped == "channels:":
            capture_channels = True
            continue
        if capture_channels:
            if stripped.startswith("- "):
                channels.append(stripped[2:].strip().strip('"'))
                continue
            capture_channels = False

        if stripped.startswith("max_videos_per_channel_per_run:"):
            try:
                max_per_channel = int(stripped.split(":", 1)[1].strip())
            except ValueError:
                pass
        elif stripped.startswith("max_videos_per_run:"):
            try:
                max_per_channel = int(stripped.split(":", 1)[1].strip())
            except ValueError:
                pass
        elif stripped.startswith("backoff_on_429_min_hours:"):
            try:
                backoff_hours = int(stripped.split(":", 1)[1].strip())
            except ValueError:
                pass
        elif stripped.startswith("backoff_on_429_minutes:"):
            try:
                minutes = int(stripped.split(":", 1)[1].strip())
                backoff_hours = max(1, (minutes + 59) // 60)
            except ValueError:
                pass

    return channels or LEGACY_CHANNELS, max_per_channel, backoff_hours


def canonical_channel_key(channel: str) -> str:
    parsed = urlsplit(channel)
    scheme = parsed.scheme or "https"
    netloc = parsed.netloc or "www.youtube.com"
    path = (parsed.path or "").rstrip("/")
    return urlunsplit((scheme, netloc, path, "", ""))


def playlist_url(channel: str) -> str:
    parsed = urlsplit(channel)
    scheme = parsed.scheme or "https"
    netloc = parsed.netloc or "www.youtube.com"
    path = (parsed.path or "").rstrip("/")
    if not path:
        path = "/videos"
    elif not path.endswith("/videos"):
        path = path.rstrip("/") + "/videos"
    return urlunsplit((scheme, netloc, path, "", ""))


def fetch_recent_entries(target_url: str, max_items: int) -> list[dict]:
    playlist_items = ",".join(str(index) for index in range(1, max_items + 1))
    cmd = [
        "yt-dlp",
        "--skip-download",
        "--flat-playlist",
        "-J",
        "--playlist-items",
        playlist_items,
        target_url,
    ]
    proc = subprocess.run(cmd, check=True, capture_output=True, text=True)
    data = json.loads(proc.stdout)
    return data.get("entries") or []


def format_entry(entry: dict, channel: str) -> dict:
    return {
        "id": entry.get("id"),
        "title": entry.get("title"),
        "channel": channel,
        "timestamp": entry.get("timestamp"),
        "upload_date": entry.get("upload_date"),
    }


def load_ingested_video_ids() -> set[str]:
    ids: set[str] = set()
    for row in load_jsonl(INDEX_JSONL_FILE):
        video_id = row.get("videoId")
        if video_id:
            ids.add(video_id)
    for row in load_json(PROCESSED_FILE, []):
        video_id = row.get("id")
        if video_id:
            ids.add(video_id)
    return ids


def append_processed(processed_data: list[dict], video_record: dict) -> None:
    if video_record["id"] in {entry.get("id") for entry in processed_data}:
        return
    record = dict(video_record)
    record["processed_at"] = utc_now_iso()
    processed_data.append(record)


def queue_contains(queue_items: list[dict], video_id: str) -> bool:
    for item in queue_items:
        if item.get("videoId") == video_id and item.get("status") in {"queued", "retry", "processing"}:
            return True
    return False


def detect_429(text: str) -> bool:
    return "429" in (text or "")


def failure_row(video_id: str, stage: str, error: str, attempt: int, backoff_until: str, source: str) -> dict:
    return {
        "videoId": video_id,
        "stage": stage,
        "error": error,
        "at": utc_now_iso(),
        "attempt": attempt,
        "backoffUntil": backoff_until,
        "source": source,
    }


def process_queue_item(item: dict, processed_data: list[dict], backoff_hours: int) -> tuple[bool, str]:
    video_url = item["sourceUrl"]
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), video_url],
        capture_output=True,
        text=True,
    )
    stdout = completed.stdout or ""
    stderr = completed.stderr or ""
    if stdout:
        print(stdout, end="")
    if stderr:
        print(stderr, file=sys.stderr, end="")

    if completed.returncode == 0:
        append_processed(
            processed_data,
            {
                "id": item["videoId"],
                "title": item.get("title"),
                "channel": item.get("channel"),
                "upload_date": item.get("upload_date"),
            },
        )
        item["status"] = "done"
        item["processedAt"] = utc_now_iso()
        return True, f"[cron] Ingested {item['videoId']}"

    error_text = stderr.strip() or stdout.strip() or f"Ingest failed for {video_url}"
    item["attempts"] = int(item.get("attempts", 0)) + 1
    item["status"] = "retry"
    backoff_until = (
        datetime.now(timezone.utc) + timedelta(hours=backoff_hours)
    ).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    item["backoffUntil"] = backoff_until
    stage = "subtitles" if detect_429(error_text) else "deliver"
    source = "yt-dlp" if detect_429(error_text) else "ingest-worker"
    append_jsonl(
        FAILURES_FILE,
        failure_row(item["videoId"], stage, error_text, item["attempts"], backoff_until, source),
    )
    return False, f"[cron] Failed {item['videoId']}: {error_text}"


def main() -> int:
    ensure_json_file(PROCESSED_FILE, [])
    ensure_json_file(CHANNEL_STATE_FILE, {})
    ensure_jsonl_file(QUEUE_FILE)
    ensure_jsonl_file(FAILURES_FILE)
    ensure_jsonl_file(INDEX_JSONL_FILE)

    channels, max_per_channel, backoff_hours = load_profile_settings()
    processed_data = load_json(PROCESSED_FILE, [])
    channel_state = load_json(CHANNEL_STATE_FILE, {})
    queue_items = load_jsonl(QUEUE_FILE)
    ingested_ids = load_ingested_video_ids()
    discovered = 0
    processed = 0
    errors: list[str] = []

    for channel in channels:
        channel_key = canonical_channel_key(channel)
        playlist = playlist_url(channel)
        try:
            entries = fetch_recent_entries(playlist, max_per_channel)
        except subprocess.CalledProcessError as exc:
            error_text = exc.stderr or str(exc)
            errors.append(f"[cron] yt-dlp failed for {channel}: {error_text}")
            scan_backoff = (
                datetime.now(timezone.utc) + timedelta(hours=backoff_hours)
            ).replace(microsecond=0).isoformat().replace("+00:00", "Z")
            append_jsonl(
                FAILURES_FILE,
                failure_row("", "download", error_text, 1, scan_backoff, "yt-dlp"),
            )
            continue
        except json.JSONDecodeError:
            errors.append(f"[cron] Invalid JSON from yt-dlp for {channel}")
            scan_backoff = (
                datetime.now(timezone.utc) + timedelta(hours=backoff_hours)
            ).replace(microsecond=0).isoformat().replace("+00:00", "Z")
            append_jsonl(
                FAILURES_FILE,
                failure_row("", "download", "Invalid JSON from yt-dlp", 1, scan_backoff, "yt-dlp"),
            )
            continue

        if entries:
            latest = entries[0]
            channel_state[channel_key] = {
                "last_video_id": latest.get("id"),
                "last_title": latest.get("title"),
                "last_checked": utc_now_iso(),
            }

        for entry in reversed(entries):
            video_id = entry.get("id")
            if not video_id:
                continue
            url_candidate = entry.get("webpage_url") or entry.get("url") or ""
            if "/shorts/" in url_candidate:
                continue
            if video_id in ingested_ids or queue_contains(queue_items, video_id):
                continue

            queue_items.append(
                {
                    "videoId": video_id,
                    "sourceUrl": f"https://www.youtube.com/watch?v={video_id}",
                    "channel": channel,
                    "title": entry.get("title"),
                    "upload_date": entry.get("upload_date"),
                    "discoveredAt": utc_now_iso(),
                    "priority": 80,
                    "reason": "New upload detected",
                    "attempts": 0,
                    "status": "queued",
                }
            )
            discovered += 1

    processed_per_channel: dict[str, int] = defaultdict(int)
    now = datetime.now(timezone.utc)
    for item in queue_items:
        if item.get("status") not in {"queued", "retry"}:
            continue
        if processed_per_channel[item["channel"]] >= max_per_channel:
            continue
        backoff_until = item.get("backoffUntil")
        if backoff_until:
            try:
                backoff_at = datetime.fromisoformat(backoff_until.replace("Z", "+00:00"))
            except ValueError:
                backoff_at = now
            if backoff_at > now:
                continue

        item["status"] = "processing"
        ok, message = process_queue_item(item, processed_data, backoff_hours)
        print(message)
        if ok:
            processed += 1
            ingested_ids.add(item["videoId"])
            processed_per_channel[item["channel"]] += 1
        else:
            errors.append(message)

    write_json(PROCESSED_FILE, processed_data)
    write_json(CHANNEL_STATE_FILE, channel_state)
    compacted_queue = [item for item in queue_items if item.get("status") != "done"]
    write_jsonl(QUEUE_FILE, compacted_queue)

    print(
        f"[cron] channels={len(channels)} discovered={discovered} processed={processed} queued={len(compacted_queue)}"
    )
    if errors:
        print("\nProblem:")
        for problem in errors:
            print(f"  - {problem}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
