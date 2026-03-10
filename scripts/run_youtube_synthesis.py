import json
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path

try:
    import ingest_youtube_url as ingest_helper
    import output_bus
    import youtube_synthesis
except ModuleNotFoundError:
    from scripts import ingest_youtube_url as ingest_helper
    from scripts import output_bus
    from scripts import youtube_synthesis


def ensure_utf8_output() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass


ensure_utf8_output()


def load_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def build_digest_message(workspace: Path, result: dict) -> str:
    project_payload = ingest_helper.project_inventory.build_project_inventory()
    ingest_helper.project_inventory.write_project_inventory(project_payload)
    project_index = {project["projectId"]: project for project in project_payload.get("projects", [])}

    topic_payloads = []
    for cluster_key in result.get("topTopics", []):
        signals_path = workspace / "knowledge" / "topics" / cluster_key / "signals.json"
        payload = load_json(signals_path, {})
        if payload:
            topic_payloads.append(payload)

    lines = [
        "🧠 Daglig YouTube-digest",
        "",
        f"• Projekt i inventeringen: {result.get('projectCount', 0)}",
        f"• Starka ämneskluster idag: {len(topic_payloads)}",
        f"• Deep research-spår idag: {len(result.get('researchPaths', []))}",
    ]

    if not topic_payloads:
        lines.extend(
            [
                "",
                "Ingen ny stark signal dök upp sedan senaste digest.",
            ]
        )
        return "\n".join(lines).strip()

    lines.extend(["", "🔥 Viktigaste rörelser"])
    for topic in topic_payloads[:3]:
        lines.append(
            f"• {topic.get('label', 'Okänt ämne')}: {ingest_helper.polish_text(topic.get('decision', {}).get('summary', ''))}"
        )
        if topic.get("project_matches"):
            match = topic["project_matches"][0]
            project = project_index.get(match["projectId"], {})
            lines.append(
                f"  Bäst i: {match['projectName']} ({ingest_helper.role_label(project)}) via {ingest_helper.fit_reason(match.get('shared_signals', [])[:4])}."
            )

    lines.extend(["", "💡 Bästa drag just nu"])
    added = 0
    seen_titles = set()
    for topic in topic_payloads:
        if not topic.get("ideas"):
            continue
        title = ingest_helper.polish_text(topic["ideas"][0].get("title", "").strip())
        if not title or title.lower() in seen_titles:
            continue
        seen_titles.add(title.lower())
        added += 1
        lines.append(f"{added}. {title}")
        if added >= 3:
            break

    lines.extend(["", "🛠 Bäst att rikta mot"])
    for topic in topic_payloads[:3]:
        if not topic.get("project_matches"):
            continue
        match = topic["project_matches"][0]
        project = project_index.get(match["projectId"], {})
        lines.append(
            f"• {topic.get('label', 'Ämne')} -> {match['projectName']} ({ingest_helper.role_label(project)})"
        )

    if result.get("researchPaths"):
        lines.extend(["", "🔬 Deep research idag"])
        for topic in topic_payloads[:2]:
            if not topic.get("ideas"):
                continue
            lines.append(
                f"• {topic.get('label', 'Ämne')}: {ingest_helper.polish_text(topic['ideas'][0].get('title', ''))}"
            )

    return "\n".join(lines).strip()


def main() -> int:
    workspace = Path(__file__).resolve().parents[1]
    memory_dir = workspace / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)
    memory_log = memory_dir / "youtube_synthesis_runs.md"

    try:
        result = youtube_synthesis.run_synthesis()
        status = "SUCCESS"
        summary_line = f"[youtube-synthesis] projects={result['projectCount']} topics={result['topicCount']} digest={result['digestPath']}"
    except Exception as exc:
        result = {}
        status = "FAIL"
        summary_line = f"{type(exc).__name__}: {exc}"
        error_trace = traceback.format_exc()
    else:
        error_trace = ""

    timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    log_line = f"{timestamp} | youtube_synthesis | {status} | {summary_line}"
    with memory_log.open("a", encoding="utf-8") as fh:
        fh.write(log_line + "\n")

    if status != "SUCCESS":
        output_bus.fanout_text(
            "ops-alerts",
            output_bus.build_ops_alert(
                "YouTube synthesis digest",
                "\n\n".join(part for part in [summary_line, error_trace.strip()] if part),
            ),
        )
        print("❌ Daily YouTube-digest misslyckades.\n")
        print(summary_line)
        if error_trace:
            print(error_trace)
        return 1

    message = build_digest_message(workspace, result)
    output_bus.fanout_text("boss-briefing", message)
    print(message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
