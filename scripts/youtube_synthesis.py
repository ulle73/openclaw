# -*- coding: utf-8 -*-
import json
import re
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    from project_inventory import (
        PROJECT_INDEX_FILE,
        PROJECT_INVENTORY_FILE,
        build_project_inventory,
        slugify,
        write_project_inventory,
    )
except ModuleNotFoundError:
    from scripts.project_inventory import (
        PROJECT_INDEX_FILE,
        PROJECT_INVENTORY_FILE,
        build_project_inventory,
        slugify,
        write_project_inventory,
    )

BASE = Path(__file__).resolve().parents[1]
TOPICS_FILE = BASE / "knowledge" / "youtube" / "TOPICS.json"
INDEX_JSONL_FILE = BASE / "knowledge" / "youtube" / "INDEX.jsonl"
DIGEST_STATE_FILE = BASE / "knowledge" / "system" / "digest_state.json"
TOPIC_ROOT = BASE / "knowledge" / "topics"
IDEAS_ROOT = BASE / "knowledge" / "ideas"
CONTEXT_FILE = BASE / "knowledge" / "companies" / "DEFAULT" / "CONTEXT.md"
PROFILE_FILE = BASE / "knowledge" / "companies" / "DEFAULT" / "PROFILE.md"

LABEL_SCORE = {"low": 3, "medium": 6, "high": 9}
CATEGORY_WEIGHT = {
    "tool": 2,
    "workflow": 3,
    "automation": 3,
    "agent_flow": 3,
    "business_idea": 3,
    "product_opportunity": 3,
    "app_idea": 3,
    "seo_distribution": 2,
    "api": 2,
    "mcp": 2,
}

ROLE_WEIGHT = {
    "product": 6,
    "offer": 6,
    "venture_platform": 4,
    "repo_only": 1,
    "manual_only": 1,
    "operating_system": -5,
    "reference_library": -10,
}

GENERIC_OVERLAP_SIGNALS = {
    "openclaw",
    "workflow-automation",
    "agent-automation",
    "knowledge-systems",
    "automation",
    "python",
    "node",
    "typescript",
    "node-tooling",
}

HIGH_VALUE_OVERLAP_SIGNALS = {
    "gravityclaw",
    "antigravity",
    "telegram",
    "voice-ai",
    "seo-content",
    "content-repurposing",
    "marketing-explainers",
    "onboarding-training",
    "ai-video-generation",
    "audit-offer",
    "service-offer",
    "web-offer",
    "design-offer",
    "betting-analytics",
    "sports-data",
    "ml-models",
    "golf-tech",
    "venture-studio",
    "product-platform",
}

OFFER_TOPIC_SIGNALS = {
    "seo-content",
    "content-repurposing",
    "marketing-explainers",
    "ai-video-generation",
}

PRODUCT_TOPIC_SIGNALS = {
    "openclaw",
    "antigravity",
    "gravityclaw",
    "telegram",
    "agent-automation",
    "workflow-automation",
    "knowledge-management",
    "proactive-assistant",
}

BETTING_TOPIC_SIGNALS = {
    "betting-analytics",
    "sports-data",
    "ml-models",
}

WEAK_CLUSTER_TERMS = {
    "the",
    "breakdown",
    "guide",
    "tool",
    "tools",
    "model",
    "models",
    "feature",
    "features",
    "process",
    "update",
    "updates",
    "new",
    "free",
    "wild",
    "insane",
    "anything",
    "day",
}


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def utc_now_iso() -> str:
    return utc_now().replace(microsecond=0).isoformat().replace("+00:00", "Z")


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def load_json(path: Path, default):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def write_json(path: Path, data) -> None:
    ensure_dir(path.parent)
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


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def parse_iso(raw_value: str | None) -> datetime | None:
    if not raw_value:
        return None
    candidate = raw_value.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(candidate)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def dedupe_keep_order(items: list[str]) -> list[str]:
    seen = set()
    output = []
    for item in items:
        normalized = item.strip()
        if not normalized:
            continue
        key = normalized.lower()
        if key in seen:
            continue
        seen.add(key)
        output.append(normalized)
    return output


def natural_join(items: list[str]) -> str:
    cleaned = [item for item in items if item]
    if not cleaned:
        return ""
    if len(cleaned) == 1:
        return cleaned[0]
    if len(cleaned) == 2:
        return f"{cleaned[0]} och {cleaned[1]}"
    return ", ".join(cleaned[:-1]) + f" och {cleaned[-1]}"


def cluster_label(cluster_key: str, entity_tags: list[str], topic_tags: list[str]) -> str:
    base = entity_tags[:2] or topic_tags[:2] or cluster_key.split("__")
    return natural_join([item.replace("-", " ") for item in base])


def load_video_meta(video_id: str) -> dict:
    return load_json(BASE / "knowledge" / "youtube" / video_id / "meta.json", {})


def load_summary_sections(video_id: str) -> dict:
    summary_path = BASE / "knowledge" / "youtube" / video_id / "summary.md"
    text = read_text(summary_path)
    lines = text.splitlines()
    sections: dict[str, list[str]] = defaultdict(list)
    current = ""
    for line in lines:
        if line.startswith("# "):
            current = line[2:].strip().lower()
            continue
        if not current:
            continue
        sections[current].append(line.rstrip())
    return sections


def fallback_tldr_from_transcript(video_id: str) -> list[str]:
    text = read_text(BASE / "knowledge" / "youtube" / video_id / "transcript_clean.md")
    if not text:
        text = read_text(BASE / "knowledge" / "youtube" / video_id / "transcript_clean.txt")
    if not text:
        return []
    text = re.sub(r"^# .*\n+", "", text, count=1).strip()
    sentences = [
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+", text)
        if len(sentence.strip().split()) >= 8
    ]
    return sentences[:2]


def extract_tldr(video_id: str) -> list[str]:
    lines = load_summary_sections(video_id).get("tl;dr", [])
    output: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped or not stripped.startswith("- "):
            continue
        output.append(stripped[2:].strip())
    return output[:3] or fallback_tldr_from_transcript(video_id)


def collect_cluster_categories(video_ids: list[str]) -> list[str]:
    categories: list[str] = []
    for video_id in video_ids:
        meta = load_video_meta(video_id)
        categories.extend(meta.get("classifications", []))
    return dedupe_keep_order(categories)


def label_average(video_ids: list[str], key: str) -> float:
    scores = []
    for video_id in video_ids:
        meta = load_video_meta(video_id)
        label = meta.get(key)
        if label in LABEL_SCORE:
            scores.append(LABEL_SCORE[label])
    if not scores:
        return 0.0
    return sum(scores) / len(scores)


def expand_cluster_tokens(cluster: dict, categories: list[str]) -> set[str]:
    category_set = set(categories)
    topic_tags = set(cluster.get("topic_tags", []))
    tokens = set(cluster.get("entity_tags", []) + cluster.get("topic_tags", []) + categories)

    if "seo_distribution" in category_set or OFFER_TOPIC_SIGNALS & topic_tags:
        tokens.add("seo-content")
    if {"automation", "workflow", "agent_flow", "api", "mcp"} & category_set:
        tokens.update({"workflow-automation", "agent-automation", "knowledge-systems"})
    return tokens


def overlap_signal_score(signal: str) -> int:
    if signal in HIGH_VALUE_OVERLAP_SIGNALS:
        return 4
    if signal in GENERIC_OVERLAP_SIGNALS:
        return 1
    return 2


def is_noise_topic(payload: dict) -> bool:
    cluster_parts = [part for part in payload.get("clusterKey", "").split("__") if part]
    if cluster_parts and all(part in WEAK_CLUSTER_TERMS or len(part) < 4 for part in cluster_parts):
        return True
    tokens = set(payload.get("entity_tags", []) + payload.get("topic_tags", []))
    if not tokens:
        return True
    informative = [token for token in tokens if token not in WEAK_CLUSTER_TERMS and len(token) >= 4]
    return not informative


def project_fit_score(project: dict, cluster: dict, categories: list[str]) -> tuple[int, list[str]]:
    role = project.get("projectRole", "manual_only")
    priority = int(project.get("projectPriority", 0))
    category_set = set(categories)
    entity_tags = set(cluster.get("entity_tags", []))
    project_tokens = set(project.get("tags", []) + project.get("signals", []) + project.get("stack", []))
    cluster_tokens = expand_cluster_tokens(cluster, categories)
    weighted_overlaps = []
    score = 0

    for token in sorted(project_tokens & cluster_tokens):
        token_score = overlap_signal_score(token)
        weighted_overlaps.append((token, token_score))
        score += token_score

    if role == "product" and PRODUCT_TOPIC_SIGNALS & cluster_tokens and {"gravityclaw", "openclaw", "telegram", "voice-ai"} & project_tokens:
        score += 6
    if "openclaw" in cluster_tokens and {"gravityclaw", "openclaw"} & project_tokens:
        score += 4
    if "openclaw" in entity_tags and role == "product" and {"gravityclaw", "openclaw"} & project_tokens:
        score += 2
    if "antigravity" in cluster_tokens and "gravityclaw" in project_tokens:
        score += 6
    if role == "offer" and {"web-offer", "design-offer", "service-offer", "audit-offer", "seo-content"} & project_tokens:
        if OFFER_TOPIC_SIGNALS & cluster_tokens:
            score += 6
        if {"ai-video-generation", "content-repurposing"} & cluster_tokens:
            score += 4
    if role == "venture_platform" and {"business_idea", "product_opportunity", "app_idea"} & category_set:
        score += 5
    if "betting-analytics" in project_tokens and BETTING_TOPIC_SIGNALS & cluster_tokens:
        score += 6
    if "golf-tech" in project_tokens and {"app_idea", "product_opportunity"} & category_set:
        score += 3

    score += ROLE_WEIGHT.get(role, 0)
    score += max(0, priority - 5)

    if weighted_overlaps and all(token in GENERIC_OVERLAP_SIGNALS for token, _ in weighted_overlaps):
        if role in {"reference_library", "operating_system"}:
            score -= 4

    shared_signals = [
        token
        for token, _ in sorted(weighted_overlaps, key=lambda item: (item[1], item[0]), reverse=True)
    ]
    return score, shared_signals[:6]


def rank_project_matches(projects: list[dict], cluster: dict, categories: list[str]) -> list[dict]:
    matches = []
    for project in projects:
        score, overlaps = project_fit_score(project, cluster, categories)
        if score <= 0:
            continue
        matches.append(
            {
                "projectId": project["projectId"],
                "projectName": project["name"],
                "score": score,
                "shared_signals": overlaps,
                "projectRole": project.get("projectRole", "manual_only"),
                "projectPriority": project.get("projectPriority", 0),
            }
        )
    matches.sort(
        key=lambda item: (item["score"], item.get("projectPriority", 0), item["projectName"]),
        reverse=True,
    )
    return matches[:3]


def strong_project_match(match: dict | None) -> bool:
    if not match:
        return False
    if match.get("projectRole") in {"reference_library", "operating_system"}:
        return False
    return match.get("score", 0) >= 10


def idea_shape(categories: list[str]) -> tuple[str, str]:
    if any(category in categories for category in ["automation", "workflow", "agent_flow", "api", "mcp"]):
        return "automation", "Bygg ett repeterbart arbetsflode eller en skill"
    if any(category in categories for category in ["product_opportunity", "business_idea", "app_idea"]):
        return "offer", "Paketera detta som ett testbart erbjudande eller produktspår"
    if "seo_distribution" in categories:
        return "distribution", "Anvand detta for content, SEO och distributionshastighet"
    return "monitor", "Bevaka temat och samla mer bevis innan du agerar"


def idea_score(cluster: dict, categories: list[str], project_matches: list[dict]) -> int:
    repeat_score = min(6, int(cluster.get("count", 0)) * 2)
    roi_score = round(cluster.get("avg_roi_score", 0) / 2)
    relevance_score = round(cluster.get("avg_relevance_score", 0) / 2)
    category_score = sum(CATEGORY_WEIGHT.get(category, 0) for category in categories[:4])
    project_score = project_matches[0]["score"] if project_matches else 0
    return repeat_score + roi_score + relevance_score + category_score + project_score


def speed_label(categories: list[str]) -> str:
    if any(category in categories for category in ["workflow", "automation", "seo_distribution"]):
        return "snabb"
    if any(category in categories for category in ["tool", "agent_flow", "api"]):
        return "medel"
    return "langsam"


def effort_label(categories: list[str]) -> str:
    if any(category in categories for category in ["api", "mcp", "app_idea"]):
        return "hog"
    if any(category in categories for category in ["workflow", "agent_flow", "automation"]):
        return "medel"
    return "lag"


def impact_label(score: int) -> str:
    if score >= 20:
        return "hog"
    if score >= 12:
        return "medel"
    return "lag"


def build_cluster_ideas(cluster: dict, categories: list[str], project_matches: list[dict]) -> list[dict]:
    label = cluster_label(cluster["cluster_key"], cluster.get("entity_tags", []), cluster.get("topic_tags", []))
    primary_kind, primary_text = idea_shape(categories)
    ideas: list[dict] = []
    base_score = idea_score(cluster, categories, project_matches)

    top_project = project_matches[0] if project_matches else None
    if strong_project_match(top_project):
        top_project = project_matches[0]
        ideas.append(
            {
                "title": f"Applicera {label} i {top_project['projectName']}",
                "kind": "project-fit",
                "impact": impact_label(base_score + top_project["score"]),
                "effort": effort_label(categories),
                "speed": speed_label(categories),
                "why": f"Temat overlappar med {top_project['projectName']} via {natural_join(top_project['shared_signals'])}.",
            }
        )

    if primary_kind == "automation":
        ideas.append(
            {
                "title": f"Bygg en intern skill eller automation runt {label}",
                "kind": "automation",
                "impact": impact_label(base_score),
                "effort": effort_label(categories),
                "speed": "snabb",
                "why": primary_text,
            }
        )
    elif primary_kind == "offer":
        ideas.append(
            {
                "title": f"Testa ett nytt erbjudande runt {label} mot svensk SME",
                "kind": "offer",
                "impact": impact_label(base_score),
                "effort": "medel",
                "speed": speed_label(categories),
                "why": primary_text,
            }
        )
    elif primary_kind == "distribution":
        ideas.append(
            {
                "title": f"Anvand {label} som content- och distributionsmotor",
                "kind": "distribution",
                "impact": impact_label(base_score),
                "effort": "lag",
                "speed": "snabb",
                "why": primary_text,
            }
        )

    ideas.append(
        {
            "title": f"Skapa ett tydligt beslutskort for {label}",
            "kind": "decision",
            "impact": impact_label(base_score - 2),
            "effort": "lag",
            "speed": "snabb",
            "why": "Temat ar tillrackligt relevant for att samla bevis, projektfit och rekommenderade nasta steg i ett stalle.",
        }
    )
    return ideas[:3]


def cluster_decision(categories: list[str], project_matches: list[dict], score: int, count: int) -> dict:
    if project_matches and strong_project_match(project_matches[0]):
        action = "project_upgrade"
        summary = "Passar ett av dina nuvarande projekt starkt och bor omsattas dar."
    elif count >= 2 and any(category in categories for category in ["workflow", "automation", "agent_flow", "api", "mcp"]):
        action = "skill_or_automation"
        summary = "Temat aterkommer och bor bli en gemensam skill eller automation, inte fler separata noteringar."
    elif score >= 16 and any(category in categories for category in ["product_opportunity", "business_idea", "app_idea"]):
        action = "offer_or_product"
        summary = "Temat verkar tillrackligt starkt for att testas som erbjudande, app eller produktspår."
    else:
        action = "monitor"
        summary = "Samla mer bevis innan du prioriterar detta hogt."
    return {"action": action, "summary": summary}


def build_topic_payload(cluster_key: str, cluster: dict, projects: list[dict]) -> dict:
    video_ids = cluster.get("videoIds", [])
    categories = collect_cluster_categories(video_ids)
    project_matches = rank_project_matches(projects, cluster, categories)
    avg_roi_score = label_average(video_ids, "roi_label")
    avg_relevance_score = label_average(video_ids, "relevance_label")
    opportunity_score = idea_score(
        {
            "count": cluster.get("count", 0),
            "avg_roi_score": avg_roi_score,
            "avg_relevance_score": avg_relevance_score,
        },
        categories,
        project_matches,
    )
    decision = cluster_decision(categories, project_matches, opportunity_score, cluster.get("count", 0))
    ideas = build_cluster_ideas(
        {
            "cluster_key": cluster_key,
            "entity_tags": cluster.get("entity_tags", []),
            "topic_tags": cluster.get("topic_tags", []),
            "count": cluster.get("count", 0),
            "avg_roi_score": avg_roi_score,
            "avg_relevance_score": avg_relevance_score,
        },
        categories,
        project_matches,
    )

    evidence = []
    for video_id in video_ids:
        meta = load_video_meta(video_id)
        evidence.append(
            {
                "videoId": video_id,
                "title": meta.get("title", ""),
                "channel": meta.get("channel", ""),
                "roi_label": meta.get("roi_label", "low"),
                "relevance_label": meta.get("relevance_label", "low"),
                "tldr": extract_tldr(video_id),
            }
        )

    return {
        "clusterKey": cluster_key,
        "label": cluster_label(cluster_key, cluster.get("entity_tags", []), cluster.get("topic_tags", [])),
        "entity_tags": cluster.get("entity_tags", []),
        "topic_tags": cluster.get("topic_tags", []),
        "categories": categories,
        "videoIds": video_ids,
        "count": cluster.get("count", 0),
        "avg_roi_score": avg_roi_score,
        "avg_relevance_score": avg_relevance_score,
        "opportunity_score": opportunity_score,
        "decision": decision,
        "project_matches": project_matches,
        "ideas": ideas,
        "evidence": evidence,
        "is_noise": False,
        "paths": {
            "overview": f"knowledge/topics/{cluster_key}/overview.md",
            "signals": f"knowledge/topics/{cluster_key}/signals.json",
            "decision": f"knowledge/topics/{cluster_key}/decision.md",
            "opportunity": f"knowledge/topics/{cluster_key}/opportunity.md",
        },
    }


def write_topic_files(payload: dict) -> None:
    target = TOPIC_ROOT / payload["clusterKey"]
    ensure_dir(target)

    signals = dict(payload)
    write_json(target / "signals.json", signals)

    lines = [
        f"# {payload['label']}",
        "",
        f"- Cluster key: {payload['clusterKey']}",
        f"- Opportunity score: {payload['opportunity_score']}",
        f"- Decision: {payload['decision']['action']} - {payload['decision']['summary']}",
        f"- Categories: {', '.join(payload['categories']) or '-'}",
        f"- Entity tags: {', '.join(payload['entity_tags']) or '-'}",
        f"- Topic tags: {', '.join(payload['topic_tags']) or '-'}",
        "",
        "## Why this matters",
        payload["decision"]["summary"],
        "",
        "## Best project matches",
    ]
    if payload["project_matches"]:
        for match in payload["project_matches"]:
            lines.append(
                f"- {match['projectName']} (score {match['score']}): {natural_join(match['shared_signals']) or 'general fit'}"
            )
    else:
        lines.append("- No strong current project match yet.")
    lines.extend(["", "## Best ideas"])
    for index, idea in enumerate(payload["ideas"], start=1):
        lines.append(
            f"{index}. {idea['title']} | impact: {idea['impact']} | effort: {idea['effort']} | speed: {idea['speed']}"
        )
        lines.append(f"   Why: {idea['why']}")
    lines.extend(["", "## Evidence"])
    for evidence in payload["evidence"]:
        lines.append(f"- {evidence['videoId']} | {evidence['title']} | {evidence['channel']}")
        for bullet in evidence.get("tldr", [])[:2]:
            lines.append(f"  - {bullet}")
    (target / "overview.md").write_text("\n".join(lines).strip() + "\n", encoding="utf-8")

    decision_lines = [
        f"# Decision - {payload['label']}",
        "",
        f"- Action: {payload['decision']['action']}",
        f"- Opportunity score: {payload['opportunity_score']}",
        f"- Summary: {payload['decision']['summary']}",
        "",
        "## Recommended next move",
        payload["ideas"][0]["title"] if payload.get("ideas") else "Ingen tydlig åtgärd identifierad än.",
        "",
        "## Best project match",
    ]
    if payload["project_matches"]:
        top_match = payload["project_matches"][0]
        decision_lines.append(
            f"- {top_match['projectName']} (role: {top_match['projectRole']}, score: {top_match['score']})"
        )
        decision_lines.append(
            f"- Shared signals: {natural_join(top_match['shared_signals']) or 'general fit'}"
        )
    else:
        decision_lines.append("- Ingen stark projektmatch ännu.")
    (target / "decision.md").write_text("\n".join(decision_lines).strip() + "\n", encoding="utf-8")

    opportunity_lines = [
        f"# Opportunity - {payload['label']}",
        "",
        "## Best ideas",
    ]
    for index, idea in enumerate(payload["ideas"], start=1):
        opportunity_lines.append(
            f"{index}. {idea['title']} | impact: {idea['impact']} | effort: {idea['effort']} | speed: {idea['speed']}"
        )
        opportunity_lines.append(f"   Why: {idea['why']}")
    (target / "opportunity.md").write_text("\n".join(opportunity_lines).strip() + "\n", encoding="utf-8")


def build_topic_syntheses(projects: list[dict]) -> dict:
    topics = load_json(TOPICS_FILE, {"clusters": {}})
    syntheses: list[dict] = []
    for cluster_key, cluster in sorted(topics.get("clusters", {}).items()):
        payload = build_topic_payload(cluster_key, cluster, projects)
        payload["is_noise"] = is_noise_topic(payload)
        write_topic_files(payload)
        syntheses.append(payload)
    return {
        "generatedAt": utc_now_iso(),
        "count": len(syntheses),
        "topics": syntheses,
    }


def load_digest_state() -> dict:
    return load_json(DIGEST_STATE_FILE, {"lastDigestAt": None, "timezone": "Europe/Stockholm"})


def write_digest_state(state: dict) -> None:
    write_json(DIGEST_STATE_FILE, state)


def digest_window(index_rows: list[dict], state: dict) -> tuple[datetime, datetime]:
    now = utc_now()
    last_digest = parse_iso(state.get("lastDigestAt"))
    if last_digest:
        return last_digest, now
    return now - timedelta(hours=24), now


def row_in_window(row: dict, start: datetime, end: datetime) -> bool:
    candidate = parse_iso(row.get("ingestedAt") or row.get("discoveredAt"))
    if not candidate:
        return False
    return start <= candidate <= end


def touched_cluster_keys(index_rows: list[dict], syntheses: list[dict], start: datetime, end: datetime) -> list[str]:
    video_ids = {row.get("videoId") for row in index_rows if row_in_window(row, start, end)}
    keys = []
    for topic in syntheses:
        if video_ids & set(topic.get("videoIds", [])):
            keys.append(topic["clusterKey"])
    return dedupe_keep_order(keys)


def research_memo_lines(topic: dict) -> list[str]:
    top_idea = topic["ideas"][0] if topic.get("ideas") else {}
    lines = [
        f"# Research Memo - {topic['label']}",
        "",
        f"- Cluster: {topic['clusterKey']}",
        f"- Opportunity score: {topic['opportunity_score']}",
        f"- Decision: {topic['decision']['action']} - {topic['decision']['summary']}",
        "",
        "## Why now",
        topic["decision"]["summary"],
        "",
        "## Best idea to test",
        f"- {top_idea.get('title', 'No idea generated')}",
        f"- Why: {top_idea.get('why', '-')}",
        f"- Impact / effort / speed: {top_idea.get('impact', '-')} / {top_idea.get('effort', '-')} / {top_idea.get('speed', '-')}",
        "",
        "## Best project matches",
    ]
    if topic["project_matches"]:
        for match in topic["project_matches"]:
            lines.append(f"- {match['projectName']} (score {match['score']}): {natural_join(match['shared_signals'])}")
    else:
        lines.append("- No strong project match yet.")
    lines.extend(["", "## Source evidence"])
    for evidence in topic["evidence"]:
        lines.append(f"- {evidence['title']} ({evidence['channel']})")
        for bullet in evidence.get("tldr", [])[:2]:
            lines.append(f"  - {bullet}")
    return lines


def primary_idea(topic: dict) -> dict:
    ideas = topic.get("ideas", [])
    if not ideas:
        return {}
    top_match = topic.get("project_matches", [None])[0] if topic.get("project_matches") else None
    if strong_project_match(top_match):
        return ideas[0]
    for idea in ideas:
        if idea.get("kind") != "project-fit":
            return idea
    return ideas[0]


def write_daily_digest(syntheses: list[dict], project_payload: dict) -> dict:
    index_rows = load_jsonl(INDEX_JSONL_FILE)
    state = load_digest_state()
    start, end = digest_window(index_rows, state)
    active_keys = touched_cluster_keys(index_rows, syntheses, start, end)

    ranked_topics = [
        topic
        for topic in syntheses
        if topic["clusterKey"] in active_keys and not topic.get("is_noise")
    ]
    ranked_topics.sort(key=lambda item: item["opportunity_score"], reverse=True)
    top_topics = ranked_topics[:3]
    research_topics = ranked_topics[:2]

    date_stamp = end.astimezone(timezone.utc).date().isoformat()
    ensure_dir(IDEAS_ROOT)
    digest_path = IDEAS_ROOT / f"{date_stamp}-digest.md"

    research_paths = []
    for index, topic in enumerate(research_topics, start=1):
        research_path = IDEAS_ROOT / f"{date_stamp}-{index:02d}-{slugify(topic['label'])}.md"
        research_path.write_text("\n".join(research_memo_lines(topic)).strip() + "\n", encoding="utf-8")
        research_paths.append(research_path)

    lines = [
        f"# Daily YouTube Digest - {date_stamp}",
        "",
        f"- Window: {start.isoformat().replace('+00:00', 'Z')} -> {end.isoformat().replace('+00:00', 'Z')}",
        f"- Videos in window: {len([row for row in index_rows if row_in_window(row, start, end)])}",
        f"- Topic clusters considered: {len(ranked_topics)}",
        f"- Project inventory: {len(project_payload.get('projects', []))} projects",
        "",
        "## Top 3 insights",
    ]
    if top_topics:
        for topic in top_topics:
            lines.append(
                f"- {topic['label']}: {topic['decision']['summary']} (score {topic['opportunity_score']})"
            )
    else:
        lines.append("- No new clusters in the selected window.")
    lines.extend(["", "## Top 3 forslag"])
    proposals = [primary_idea(topic) for topic in top_topics if topic.get("ideas")]
    if proposals:
        for idea in proposals[:3]:
            lines.append(
                f"- {idea['title']} | impact: {idea['impact']} | effort: {idea['effort']} | speed: {idea['speed']}"
            )
    else:
        lines.append("- No proposal candidates this run.")
    lines.extend(["", "## Project-targeted opportunities"])
    project_lines = []
    for topic in top_topics:
        if not topic["project_matches"]:
            continue
        match = topic["project_matches"][0]
        project_lines.append(
            f"- {match['projectName']} <- {topic['label']} ({natural_join(match['shared_signals']) or 'general fit'})"
        )
    lines.extend(project_lines or ["- No strong project-targeted opportunity found this run."])
    lines.extend(["", "## Deep research queue (top 1-2)"])
    if research_topics:
        for topic, path in zip(research_topics, research_paths):
            lines.append(
                f"- {topic['label']} | decision: {topic['decision']['action']} | file: {path.relative_to(BASE).as_posix()}"
            )
    else:
        lines.append("- No research queue this run.")
    lines.extend(["", "## Supporting files"])
    lines.append(f"- Project inventory: {PROJECT_INVENTORY_FILE.relative_to(BASE).as_posix()}")
    lines.append(f"- Project index: {PROJECT_INDEX_FILE.relative_to(BASE).as_posix()}")
    lines.append(f"- Topic root: {TOPIC_ROOT.relative_to(BASE).as_posix()}")
    digest_path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")

    state["lastDigestAt"] = utc_now_iso()
    write_digest_state(state)
    return {
        "digestPath": str(digest_path),
        "researchPaths": [str(path) for path in research_paths],
        "topTopics": [topic["clusterKey"] for topic in top_topics],
        "windowStart": start.isoformat().replace("+00:00", "Z"),
        "windowEnd": end.isoformat().replace("+00:00", "Z"),
    }


def run_synthesis() -> dict:
    project_payload = build_project_inventory()
    write_project_inventory(project_payload)
    topic_payload = build_topic_syntheses(project_payload.get("projects", []))
    digest_payload = write_daily_digest(topic_payload.get("topics", []), project_payload)
    return {
        "generatedAt": utc_now_iso(),
        "projectCount": len(project_payload.get("projects", [])),
        "topicCount": topic_payload.get("count", 0),
        "digestPath": digest_payload["digestPath"],
        "researchPaths": digest_payload["researchPaths"],
        "topTopics": digest_payload["topTopics"],
    }


def main() -> int:
    result = run_synthesis()
    print(
        f"[youtube-synthesis] projects={result['projectCount']} topics={result['topicCount']} digest={result['digestPath']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
