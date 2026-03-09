import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

try:
    import output_bus
    import project_inventory
    import youtube_synthesis
except ModuleNotFoundError:
    from scripts import output_bus
    from scripts import project_inventory, youtube_synthesis


def ensure_utf8_output() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass


ensure_utf8_output()


SIGNAL_LABELS = {
    "agent-automation": "agentflöden",
    "ai-video-generation": "AI-video",
    "audit-offer": "audit-erbjudande",
    "automation": "automation",
    "content-repurposing": "content repurposing",
    "design-offer": "design och paketering",
    "gravityclaw": "Gravity Claw",
    "knowledge-systems": "kunskapssystem",
    "marketing-explainers": "explainers och content",
    "onboarding-training": "onboarding",
    "openclaw": "OpenClaw",
    "seo-content": "SEO och content",
    "service-offer": "tjansteerbjudande",
    "telegram": "Telegram",
    "web-offer": "webberbjudande",
    "workflow-automation": "workflow och automation",
}

ROLE_LABELS = {
    "offer": "erbjudande",
    "operating_system": "system",
    "product": "repo",
    "reference_library": "referensrepo",
    "venture_platform": "paraply",
}

SWEDISH_LABELS = {
    "low": "Låg",
    "medium": "Medel",
    "high": "Hög",
}


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
    timestamp = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    line = f"{timestamp} | manual-youtube | {status} | {url} | {summary}"
    with log_path.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


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
        "processed_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "status": status,
    }
    data.append(entry)
    processed_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def load_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def load_meta(meta_path: Path) -> dict:
    return load_json(meta_path, {})


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def load_summary_sections(summary_path: Path) -> dict[str, list[str]]:
    text = read_text(summary_path)
    sections: dict[str, list[str]] = {}
    current = ""
    for line in text.splitlines():
        if line.startswith("# "):
            current = line[2:].strip().lower()
            sections[current] = []
            continue
        if current:
            sections[current].append(line.rstrip())
    return sections


def extract_bullets(lines: list[str]) -> list[str]:
    bullets: list[str] = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("- "):
            bullets.append(stripped[2:].strip())
    return bullets


def extract_numbered(lines: list[str]) -> list[str]:
    items: list[str] = []
    for line in lines:
        stripped = line.strip()
        match = re.match(r"^\d+\.\s+(.*)$", stripped)
        if match:
            items.append(match.group(1).strip())
    return items


def natural_join(items: list[str]) -> str:
    cleaned = [item for item in items if item]
    if not cleaned:
        return ""
    if len(cleaned) == 1:
        return cleaned[0]
    if len(cleaned) == 2:
        return f"{cleaned[0]} och {cleaned[1]}"
    return ", ".join(cleaned[:-1]) + f" och {cleaned[-1]}"


def dedupe_keep_order(items: list[str]) -> list[str]:
    seen = set()
    output = []
    for item in items:
        key = item.strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        output.append(item)
    return output


def prettify_signal(signal: str) -> str:
    if signal in SIGNAL_LABELS:
        return SIGNAL_LABELS[signal]
    return signal.replace("-", " ")


def role_label(project: dict) -> str:
    if project.get("repoPaths"):
        return "repo"
    return ROLE_LABELS.get(project.get("projectRole", ""), "projekt")


def yes_no(value: bool) -> str:
    return "Ja" if value else "Nej"


def fit_reason(signals: list[str]) -> str:
    cleaned = dedupe_keep_order([prettify_signal(signal) for signal in signals if signal])
    if "workflow och automation" in cleaned and "automation" in cleaned:
        cleaned = [item for item in cleaned if item != "automation"]
    if not cleaned:
        return "allmän strategisk fit"
    if len(cleaned) == 1:
        return cleaned[0]
    if len(cleaned) == 2:
        return f"{cleaned[0]} samt {cleaned[1]}"
    return f"{', '.join(cleaned[:-1])} samt {cleaned[-1]}"


def build_topic_context(workspace: Path, video_meta: dict, project_payload: dict | None = None) -> tuple[dict | None, dict]:
    if project_payload is None:
        project_payload = project_inventory.build_project_inventory()
        project_inventory.write_project_inventory(project_payload)

    cluster_key = video_meta.get("topic_cluster_key")
    if not cluster_key:
        return None, project_payload

    topics_payload = youtube_synthesis.load_json(youtube_synthesis.TOPICS_FILE, {"clusters": {}})
    cluster = topics_payload.get("clusters", {}).get(cluster_key)
    if not cluster:
        return None, project_payload

    topic_payload = youtube_synthesis.build_topic_payload(cluster_key, cluster, project_payload.get("projects", []))
    topic_payload["is_noise"] = youtube_synthesis.is_noise_topic(topic_payload)
    youtube_synthesis.write_topic_files(topic_payload)
    return topic_payload, project_payload


def load_video_context(
    workspace: Path,
    video_id: str,
    project_payload: dict | None = None,
) -> tuple[dict, dict[str, list[str]], dict | None, dict]:
    video_root = workspace / "knowledge" / "youtube" / video_id
    video_meta = load_meta(video_root / "meta.json") or {"id": video_id, "title": ""}
    summary_sections = load_summary_sections(video_root / "summary.md")
    topic_payload, project_payload = build_topic_context(workspace, video_meta, project_payload=project_payload)
    return video_meta, summary_sections, topic_payload, project_payload


def polish_text(text: str) -> str:
    replacements = {
        "bor omsattas dar.": "bör omsättas där.",
        "bor bli": "bör bli",
        "for ": "för ",
        " for": " för",
        "amnes": "ämnes",
        "arbetsflode": "arbetsflöde",
        "omsattas": "omsättas",
        "dar": "där",
    }
    result = text or ""
    for source, target in replacements.items():
        result = result.replace(source, target)
    return result


def build_message(video_meta: dict, summary_sections: dict[str, list[str]], topic_payload: dict | None, project_payload: dict) -> str:
    title = (video_meta.get("title") or "Ny video").strip()
    channel = (video_meta.get("channel") or "").strip()
    tldr = extract_bullets(summary_sections.get("tl;dr", []))
    takeaways = extract_numbered(summary_sections.get("5 viktigaste takeaways", []))
    next_actions = extract_numbered(summary_sections.get("next actions (max 3)", []))
    project_index = {project["projectId"]: project for project in project_payload.get("projects", [])}
    should = video_meta.get("should", {})

    lines = [
        "🎥 Ny YouTube-video analyserad",
        "",
        title,
    ]
    if channel:
        lines.append(f"Från: {channel}")

    lines.extend([
        "",
        "🧠 Vad den egentligen handlar om",
        " ".join(tldr[:2]) if tldr else "Videon är analyserad och sparad i kunskapsflödet.",
        "",
        "🔥 Viktigaste insikter",
    ])
    for item in (takeaways[:5] or tldr[:5] or ["Inga tydliga takeaways kunde lyftas fram automatiskt."]):
        lines.append(f"• {item}")

    if topic_payload and topic_payload.get("project_matches"):
        lines.extend(["", "🛠 Bäst att implementera i"])
        for match in topic_payload.get("project_matches", [])[:3]:
            project = project_index.get(match["projectId"], {})
            reason = fit_reason(match.get("shared_signals", [])[:4])
            lines.append(
                f"• {match['projectName']} ({role_label(project)}): starkast fit via {reason}."
            )

    lines.extend(["", "💡 Idéer att testa"])
    idea_lines = []
    if topic_payload and topic_payload.get("ideas"):
        for idea in topic_payload["ideas"][:3]:
            idea_lines.append(idea.get("title", "").strip())
    if not idea_lines:
        idea_lines = next_actions[:3]
    for index, item in enumerate(idea_lines[:3], start=1):
        lines.append(f"{index}. {polish_text(item)}")

    if topic_payload:
        count = int(topic_payload.get("count", 0))
        decision_summary = topic_payload.get("decision", {}).get("summary", "")
        lines.extend(["", "🔁 Kontext i biblioteket"])
        if count > 1:
            lines.append(
                f"Det finns redan {count} videor i samma ämneskluster. {polish_text(decision_summary) or 'Bygg vidare på samma spår i stället för att skapa dubletter.'}"
            )
        elif decision_summary:
            lines.append(polish_text(decision_summary))

    lines.extend(["", "📊 Bedömning"])
    lines.append(f"• ROI: {SWEDISH_LABELS.get(video_meta.get('roi_label', 'low'), 'Lag')}")
    lines.append(f"• Relevans: {SWEDISH_LABELS.get(video_meta.get('relevance_label', 'low'), 'Lag')}")
    lines.append(f"• Automation: {yes_no(bool(should.get('automation')))}")
    lines.append(f"• Skill: {yes_no(bool(should.get('skill')))}")
    lines.append(f"• Produkt/erbjudande: {yes_no(bool(should.get('product')) or bool(should.get('idea_bank')))}")
    return "\n".join(lines).strip()


def build_compact_video_card(
    video_meta: dict,
    summary_sections: dict[str, list[str]],
    topic_payload: dict | None,
    project_payload: dict,
) -> str:
    title = (video_meta.get("title") or "Ny video").strip()
    channel = (video_meta.get("channel") or "").strip()
    tldr = extract_bullets(summary_sections.get("tl;dr", []))
    takeaways = extract_numbered(summary_sections.get("5 viktigaste takeaways", []))
    next_actions = extract_numbered(summary_sections.get("next actions (max 3)", []))
    project_index = {project["projectId"]: project for project in project_payload.get("projects", [])}

    lines = [f"🎥 {title}"]
    if channel:
        lines.append(f"Från: {channel}")

    summary_line = tldr[0] if tldr else (takeaways[0] if takeaways else "Videon är analyserad i knowledge-flödet.")
    lines.append(f"🧠 {summary_line}")

    if topic_payload and topic_payload.get("project_matches"):
        top_match = topic_payload["project_matches"][0]
        project = project_index.get(top_match["projectId"], {})
        lines.append(
            f"🛠 Bäst i: {top_match['projectName']} ({role_label(project)}) via {fit_reason(top_match.get('shared_signals', [])[:4])}."
        )

    idea = ""
    if topic_payload and topic_payload.get("ideas"):
        idea = topic_payload["ideas"][0].get("title", "").strip()
    if not idea and next_actions:
        idea = next_actions[0]
    if idea:
        lines.append(f"💡 Testa: {polish_text(idea)}")

    lines.append(
        f"📊 ROI: {SWEDISH_LABELS.get(video_meta.get('roi_label', 'low'), 'Låg')} | Relevans: {SWEDISH_LABELS.get(video_meta.get('relevance_label', 'low'), 'Låg')}"
    )
    return "\n".join(lines).strip()


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
        append_log(log_path, "FAIL", url, str(exc))
        print(f"❌ Kunde inte läsa YouTube-länken.\n\nDetalj: {exc}")
        return 1

    target_meta = workspace / "knowledge" / "youtube" / video_id / "meta.json"
    summary_path = workspace / "knowledge" / "youtube" / video_id / "summary.md"
    cmd = [sys.executable, str(workspace / "scripts" / "youtube_to_knowledge.py"), url]
    process = subprocess.run(cmd, capture_output=True, text=True)
    summary = crunch_summary(process.stdout, process.stderr)
    status = "SUCCESS" if process.returncode == 0 else "FAIL"
    append_log(log_path, status, url, summary)

    if process.returncode != 0:
        error_detail = process.stderr.strip() or summary
        output_bus.fanout_text(
            "ops-alerts",
            output_bus.build_ops_alert(
                "YouTube ingest",
                f"URL: {url}\n\n{error_detail}",
            ),
        )
        print(f"❌ YouTube-ingest misslyckades.\n\n{error_detail}")
        return process.returncode

    video_meta = load_meta(target_meta) or {"id": video_id, "title": ""}
    update_processed(processed_path, video_meta, "manual")
    summary_sections = load_summary_sections(summary_path)
    topic_payload, project_payload = build_topic_context(workspace, video_meta)
    message = build_message(video_meta, summary_sections, topic_payload, project_payload)
    output_bus.fanout_text("radar-feed", message)
    print(message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
