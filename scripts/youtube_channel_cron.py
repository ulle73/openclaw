import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

CHANNELS = [
    "https://youtube.com/@thekoerneroffice",
    "https://youtube.com/@juliangoldieseo",
    "https://youtube.com/@rileybrownai",
    "https://youtube.com/@itssssss_jack",
]

BASE = Path(__file__).resolve().parents[1]
PROCESSED_FILE = BASE / "knowledge" / "processed-videos.json"
CHANNEL_STATE_FILE = BASE / "knowledge" / "channel-state.json"
SCRIPT = BASE / "scripts" / "youtube_to_knowledge.py"

PROCESSED_FILE.parent.mkdir(parents=True, exist_ok=True)
if not PROCESSED_FILE.exists():
    PROCESSED_FILE.write_text("[]", encoding="utf-8")
if not CHANNEL_STATE_FILE.exists():
    CHANNEL_STATE_FILE.write_text("{}", encoding="utf-8")


def load_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


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


def fetch_latest_entry(target_url: str):
    cmd = [
        "yt-dlp",
        "--skip-download",
        "--flat-playlist",
        "-J",
        "--playlist-items",
        "1",
        target_url,
    ]
    proc = subprocess.run(cmd, check=True, capture_output=True, text=True)
    data = json.loads(proc.stdout)
    entries = data.get("entries") or []
    return entries[0] if entries else None


def format_entry(entry: dict) -> dict:
    return {
        "id": entry.get("id"),
        "title": entry.get("title"),
        "channel": entry.get("uploader") or entry.get("channel"),
        "timestamp": entry.get("timestamp"),
        "upload_date": entry.get("upload_date"),
    }


def main() -> int:
    processed_data = load_json(PROCESSED_FILE, [])
    channel_state = load_json(CHANNEL_STATE_FILE, {})
    state_dirty = False
    processed_dirty = False
    results = []
    errors = []

    for channel in CHANNELS:
        channel_key = canonical_channel_key(channel)
        last_video_id = channel_state.get(channel_key, {}).get("last_video_id")
        playlist = playlist_url(channel)
        try:
            entry = fetch_latest_entry(playlist)
        except subprocess.CalledProcessError as exc:
            msg = f"[cron] yt-dlp failed for {channel}: {exc.stderr or exc}"
            print(msg)
            errors.append(msg)
            continue
        except json.JSONDecodeError:
            msg = f"[cron] Invalid JSON from yt-dlp for {channel}"
            print(msg)
            errors.append(msg)
            continue

        if not entry:
            msg = f"[cron] No entries for {channel}"
            print(msg)
            errors.append(msg)
            continue

        url_candidate = entry.get("webpage_url") or entry.get("url") or ""
        if "/shorts/" in url_candidate:
            msg = f"[cron] Skipping latest entry because it looks like a Shorts video ({channel})"
            print(msg)
            errors.append(msg)
            continue

        video_id = entry.get("id")
        if not video_id:
            msg = f"[cron] Entry missing video id for {channel}"
            print(msg)
            errors.append(msg)
            continue

        if video_id == last_video_id:
            print(f"[cron] No new non-short videos processed for {channel}")
            continue

        video_url = f"https://www.youtube.com/watch?v={video_id}"
        print(f"[cron] Processing new video {video_id} ({entry.get('title')}) from {channel}")
        try:
            completed = subprocess.run(
                [sys.executable, str(SCRIPT), video_url],
                check=True,
                capture_output=True,
                text=True,
            )
            if completed.stdout:
                print(completed.stdout, end="")
            if completed.stderr:
                print(completed.stderr, file=sys.stderr, end="")
        except subprocess.CalledProcessError as exc:
            stdout = exc.stdout or ""
            stderr = exc.stderr or ""
            if stdout:
                print(stdout, end="")
            if stderr:
                print(stderr, file=sys.stderr, end="")
            msg = f"[cron] analysis failed for {video_url}: {exc}"
            print(msg)
            errors.append(msg)
            continue

        video_record = format_entry(entry)
        video_record["processed_at"] = datetime.now(timezone.utc).isoformat()
        processed_data.append(video_record)
        processed_dirty = True
        results.append(video_record)
        channel_state[channel_key] = {
            "last_video_id": video_id,
            "last_title": entry.get("title"),
            "last_checked": datetime.now(timezone.utc).isoformat(),
        }
        state_dirty = True

    if processed_dirty:
        PROCESSED_FILE.write_text(json.dumps(processed_data, ensure_ascii=False, indent=2), encoding="utf-8")
    if state_dirty:
        CHANNEL_STATE_FILE.write_text(json.dumps(channel_state, ensure_ascii=False, indent=2), encoding="utf-8")

    if results:
        print(f"[cron] Processed {len(results)} new videos")
    else:
        print("[cron] No new videos to process")
    if errors:
        print("\nProblem:")
        for problem in errors:
            print(f"  • {problem}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
