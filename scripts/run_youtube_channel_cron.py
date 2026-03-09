import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import ingest_youtube_url as ingest_helper
except ModuleNotFoundError:
    from scripts import ingest_youtube_url as ingest_helper


def ensure_utf8_output() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass


ensure_utf8_output()


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


def latest_nonempty_line(text: str) -> str:
    for line in reversed((text or "").splitlines()):
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def new_video_ids(before_rows: list[dict], after_rows: list[dict]) -> list[str]:
    before_ids = {row.get("videoId") for row in before_rows if row.get("videoId")}
    new_rows = [row for row in after_rows if row.get("videoId") and row.get("videoId") not in before_ids]
    new_rows.sort(key=lambda row: row.get("ingestedAt", ""), reverse=True)
    return [row["videoId"] for row in new_rows]


def queued_count(path: Path) -> int:
    return len(load_jsonl(path))


def extract_problems(stdout: str, stderr: str) -> list[str]:
    problems: list[str] = []
    capture = False
    for raw_line in (stdout or "").splitlines():
        stripped = raw_line.strip()
        if stripped == "Problem:":
            capture = True
            continue
        if capture and stripped.startswith("- "):
            problems.append(stripped[2:].strip())
    if stderr.strip():
        problems.append(stderr.strip())
    return problems[:3]


def build_scan_message(workspace: Path, video_ids: list[str], queue_size: int, problems: list[str]) -> str:
    project_payload = ingest_helper.project_inventory.build_project_inventory()
    ingest_helper.project_inventory.write_project_inventory(project_payload)

    lines = [
        "📺 YouTube-kanalscan klar",
        "",
        f"• Nya analyserade videor: {len(video_ids)}",
        f"• Kvar i kö: {queue_size}",
    ]

    if not video_ids:
        lines.extend(
            [
                "",
                "Ingen ny video behövde analyseras i den här körningen.",
            ]
        )
    else:
        lines.extend(["", "🔥 Höjdpunkter"])
        for video_id in video_ids[:3]:
            video_meta, summary_sections, topic_payload, _ = ingest_helper.load_video_context(
                workspace,
                video_id,
                project_payload=project_payload,
            )
            lines.append(ingest_helper.build_compact_video_card(video_meta, summary_sections, topic_payload, project_payload))
            lines.append("")
        if len(video_ids) > 3:
            lines.append(f"… plus {len(video_ids) - 3} fler videor analyserade i samma körning.")

    if problems:
        lines.extend(["", "⚠️ Att hålla koll på"])
        for problem in problems:
            lines.append(f"• {problem}")

    return "\n".join(lines).strip()


def main() -> int:
    workspace = Path(__file__).resolve().parents[1]
    target_script = workspace / "scripts" / "youtube_channel_cron.py"
    memory_dir = workspace / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)
    memory_log = memory_dir / "youtube_cron_runs.md"
    index_file = workspace / "knowledge" / "youtube" / "INDEX.jsonl"
    queue_file = workspace / "knowledge" / "youtube" / "QUEUE.jsonl"

    before_rows = load_jsonl(index_file)
    process = subprocess.run(
        [sys.executable, str(target_script)],
        capture_output=True,
        text=True,
    )

    stdout = process.stdout.strip()
    stderr = process.stderr.strip()
    after_rows = load_jsonl(index_file)
    processed_video_ids = new_video_ids(before_rows, after_rows)

    summary_line = latest_nonempty_line(stdout) or stderr or "No output"
    if process.returncode != 0 and stderr:
        summary_line = f"{summary_line} | stderr: {stderr}"

    status = "SUCCESS" if process.returncode == 0 else "FAIL"
    timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    log_line = f"{timestamp} | youtube_channel_cron | {status} | {summary_line}"
    with memory_log.open("a", encoding="utf-8") as fh:
        fh.write(log_line + "\n")

    queue_size = queued_count(queue_file)
    problems = extract_problems(stdout, stderr)

    if process.returncode != 0:
        print(
            "\n".join(
                [
                    "❌ YouTube-kanalscan misslyckades.",
                    "",
                    f"Detalj: {summary_line}",
                ]
            )
        )
        return process.returncode

    print(build_scan_message(workspace, processed_video_ids, queue_size, problems))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
