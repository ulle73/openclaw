from __future__ import annotations

import argparse
import html
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests


BASE_DIR = Path(__file__).resolve().parents[1]
KNOWLEDGE_DIR = BASE_DIR / "knowledge" / "github-trends"
HISTORY_DIR = KNOWLEDGE_DIR / "history"
REPOS_DIR = KNOWLEDGE_DIR / "repos"
LATEST_FILE = KNOWLEDGE_DIR / "latest.json"
RUN_LOG = BASE_DIR / "memory" / "github_trends_runs.md"
PROJECT_INVENTORY_FILE = BASE_DIR / "knowledge" / "system" / "project_inventory.json"
TRENDING_URL = "https://github.com/trending?since=daily"

REQUEST_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

SIGNAL_KEYWORDS = {
    "agent-automation": ["agent", "agentic", "multi-agent", "autonomous", "assistant"],
    "workflow-automation": ["workflow", "automation", "orchestration", "pipeline"],
    "knowledge-systems": ["knowledge", "memory", "rag", "retrieval", "indexing"],
    "openclaw": ["openclaw"],
    "telegram": ["telegram", "botfather", "grammy"],
    "voice-ai": ["voice", "speech", "audio", "tts", "stt"],
    "seo-content": ["seo", "content", "marketing", "search"],
    "design-offer": ["design", "ui", "ux", "figma"],
    "ml-models": ["ai", "llm", "model", "inference", "embedding"],
    "betting-analytics": ["betting", "odds", "sportsbook"],
    "sports-data": ["sports", "match", "score"],
    "app-product": ["app", "mobile", "product"],
    "service-offer": ["service", "agency", "client"],
    "web-offer": ["website", "web", "frontend", "landing page"],
}

SIGNAL_LABELS = {
    "agent-automation": "agent automation",
    "workflow-automation": "workflow automation",
    "knowledge-systems": "knowledge systems",
    "openclaw": "OpenClaw",
    "telegram": "Telegram",
    "voice-ai": "voice AI",
    "seo-content": "SEO/content",
    "design-offer": "design",
    "ml-models": "AI/models",
    "betting-analytics": "betting analytics",
    "sports-data": "sports data",
    "app-product": "app product",
    "service-offer": "service offer",
    "web-offer": "web offer",
}


def ensure_utf8_output() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8")
        except Exception:
            pass


ensure_utf8_output()


def ensure_dirs() -> None:
    for directory in (KNOWLEDGE_DIR, HISTORY_DIR, REPOS_DIR, RUN_LOG.parent):
        directory.mkdir(parents=True, exist_ok=True)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def local_day_key() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return default


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def append_run_log(status: str, summary: str) -> None:
    line = f"{utc_now_iso()} | github_trends | {status} | {summary.strip()}"
    with RUN_LOG.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")


def request_text(url: str, *, headers: dict[str, str] | None = None) -> str:
    response = requests.get(url, headers=headers or REQUEST_HEADERS, timeout=30)
    response.raise_for_status()
    return response.text


def clean_html(raw: str) -> str:
    text = re.sub(r"<svg.*?</svg>", " ", raw, flags=re.S)
    text = re.sub(r"<.*?>", " ", text, flags=re.S)
    text = html.unescape(text)
    text = text.replace("\xa0", " ")
    return re.sub(r"\s+", " ", text).strip()


def parse_count(text: str) -> int:
    digits = re.sub(r"[^\d]", "", text or "")
    return int(digits) if digits else 0


def parse_trending_page(page_html: str) -> list[dict[str, Any]]:
    articles = re.findall(r"<article class=\"Box-row\".*?</article>", page_html, flags=re.S)
    repos: list[dict[str, Any]] = []
    for rank, article in enumerate(articles, start=1):
        repo_match = re.search(r"<h2[^>]*>\s*<a[^>]*href=\"/([^/\"]+)/([^/\"]+)\"", article, flags=re.S)
        if not repo_match:
            continue
        owner, repo = repo_match.groups()
        repo_name = repo.strip()
        full_name = f"{owner}/{repo_name}"

        desc_match = re.search(
            r"<p class=\"col-9 color-fg-muted my-1 [^\"]*\">\s*(.*?)\s*</p>",
            article,
            flags=re.S,
        )
        description = clean_html(desc_match.group(1)) if desc_match else ""
        language_match = re.search(r"<span[^>]*itemprop=\"programmingLanguage\"[^>]*>(.*?)</span>", article, flags=re.S)
        stars_match = re.search(rf"href=\"/{re.escape(full_name)}/stargazers\"[^>]*>(.*?)</a>", article, flags=re.S)
        forks_match = re.search(rf"href=\"/{re.escape(full_name)}/forks\"[^>]*>(.*?)</a>", article, flags=re.S)
        today_match = re.search(r"([\d,]+)\s+stars today", clean_html(article), flags=re.I)

        repos.append(
            {
                "rank": rank,
                "owner": owner,
                "repo": repo_name,
                "full_name": full_name,
                "url": f"https://github.com/{full_name}",
                "description": description,
                "language": clean_html(language_match.group(1)) if language_match else "",
                "stars": parse_count(clean_html(stars_match.group(1))) if stars_match else 0,
                "forks": parse_count(clean_html(forks_match.group(1))) if forks_match else 0,
                "stars_today": parse_count(today_match.group(1)) if today_match else 0,
            }
        )
    return repos


def load_project_inventory() -> list[dict[str, Any]]:
    payload = load_json(PROJECT_INVENTORY_FILE, {})
    return payload.get("projects", []) if isinstance(payload, dict) else []


def detect_signals(text: str) -> list[str]:
    lowered = (text or "").lower()
    hits: list[str] = []
    for signal, keywords in SIGNAL_KEYWORDS.items():
        if any(keyword in lowered for keyword in keywords):
            hits.append(signal)
    return hits


def summarize_use_case(text: str, language: str) -> str:
    lowered = (text or "").lower()
    if any(token in lowered for token in ("browser", "web page", "scrape", "crawler")):
        return "browser automation or web extraction"
    if any(token in lowered for token in ("agent", "agentic", "assistant")):
        return "agent workflows and AI operators"
    if any(token in lowered for token in ("rag", "retrieval", "knowledge", "memory")):
        return "knowledge retrieval and memory-backed AI"
    if any(token in lowered for token in ("ui", "design", "figma", "frontend")):
        return "frontend or design system work"
    if any(token in lowered for token in ("model", "llm", "inference", "embedding", "ai")):
        return "LLM or AI product development"
    if any(token in lowered for token in ("telegram", "bot")):
        return "bot and messaging automation"
    if language:
        return f"{language} development and prototyping"
    return "general software development"


def first_nonempty_sentence(text: str) -> str:
    cleaned = re.sub(r"`+", "", text or "").strip()
    if not cleaned:
        return ""
    cleaned = re.sub(r"^#+\s*", "", cleaned)
    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", cleaned) if part.strip()]
    for paragraph in paragraphs:
        if paragraph.startswith(("!", "[", "<")):
            continue
        sentence = re.split(r"(?<=[.!?])\s+", paragraph, maxsplit=1)[0].strip()
        sentence = re.sub(r"\s+", " ", sentence)
        if len(sentence) >= 30:
            return sentence[:320].rstrip()
    return cleaned[:320].rstrip()


def fetch_readme_text(full_name: str) -> str:
    url = f"https://api.github.com/repos/{full_name}/readme"
    headers = dict(REQUEST_HEADERS)
    headers["Accept"] = "application/vnd.github.raw+json"
    response = requests.get(url, headers=headers, timeout=30)
    if response.status_code == 404:
        return ""
    response.raise_for_status()
    return response.text


def fetch_repo_api(full_name: str) -> dict[str, Any]:
    headers = dict(REQUEST_HEADERS)
    headers["Accept"] = "application/vnd.github+json"
    response = requests.get(f"https://api.github.com/repos/{full_name}", headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()


def cache_path_for_repo(full_name: str) -> Path:
    safe_name = full_name.replace("/", "__")
    return REPOS_DIR / f"{safe_name}.json"


def top_project_matches(signals: list[str], projects: list[dict[str, Any]]) -> list[dict[str, Any]]:
    scored: list[dict[str, Any]] = []
    signal_set = set(signals)
    for project in projects:
        project_signals = set(project.get("signals", [])) | set(project.get("tags", []))
        shared = sorted(signal_set & project_signals)
        if not shared:
            continue
        score = len(shared) * 10 + int(project.get("projectPriority", 0))
        scored.append(
            {
                "projectId": project.get("projectId"),
                "projectName": project.get("name"),
                "sharedSignals": shared,
                "score": score,
            }
        )
    return sorted(scored, key=lambda item: item["score"], reverse=True)[:3]


def build_relevance_text(matches: list[dict[str, Any]]) -> str:
    if not matches:
        return "relevant as general market signal"
    top = matches[0]
    labels = [SIGNAL_LABELS.get(signal, signal.replace("-", " ")) for signal in top["sharedSignals"][:3]]
    return f"relevant for {top['projectName']} via {', '.join(labels)}"


def build_repo_brief_payload(full_name: str, *, force_refresh: bool = False) -> dict[str, Any]:
    ensure_dirs()
    cache_file = cache_path_for_repo(full_name)
    cached = load_json(cache_file, {})
    if cached and not force_refresh:
        fetched_at = str(cached.get("fetchedAt", ""))
        if fetched_at.startswith(local_day_key()):
            return cached

    repo_api = fetch_repo_api(full_name)
    readme_text = fetch_readme_text(full_name)
    description = (repo_api.get("description") or "").strip()
    purpose = description or first_nonempty_sentence(readme_text) or f"{full_name} is an active GitHub repository."
    combined_text = " ".join(
        [
            full_name,
            description,
            " ".join(repo_api.get("topics") or []),
            first_nonempty_sentence(readme_text),
        ]
    )
    detected_signals = detect_signals(combined_text)
    project_matches = top_project_matches(detected_signals, load_project_inventory())
    use_case = summarize_use_case(combined_text, repo_api.get("language") or "")
    payload = {
        "fullName": full_name,
        "url": repo_api.get("html_url") or f"https://github.com/{full_name}",
        "description": description,
        "purpose": purpose,
        "useCase": use_case,
        "relevance": build_relevance_text(project_matches),
        "language": repo_api.get("language") or "",
        "topics": repo_api.get("topics") or [],
        "stars": repo_api.get("stargazers_count") or 0,
        "forks": repo_api.get("forks_count") or 0,
        "openIssues": repo_api.get("open_issues_count") or 0,
        "detectedSignals": detected_signals,
        "projectMatches": project_matches,
        "fetchedAt": utc_now_iso(),
    }
    write_json(cache_file, payload)
    return payload


def describe_repo_text(full_name: str, *, force_refresh: bool = False) -> str:
    payload = build_repo_brief_payload(full_name, force_refresh=force_refresh)
    lines = [
        f"Repo: {payload['fullName']}",
        f"Purpose: {payload['purpose']}",
        f"Use for: {payload['useCase']}",
        f"Why relevant: {payload['relevance']}",
        f"Stats: {payload['stars']} stars, {payload['forks']} forks",
        f"URL: {payload['url']}",
    ]
    return "\n".join(lines)


def compare_snapshots(current: list[dict[str, Any]], previous: list[dict[str, Any]]) -> dict[str, Any]:
    previous_by_name = {item["full_name"]: item for item in previous}
    current_by_name = {item["full_name"]: item for item in current}

    new_repos: list[dict[str, Any]] = []
    climbed: list[dict[str, Any]] = []
    dropped: list[dict[str, Any]] = []

    for repo in current:
        prior = previous_by_name.get(repo["full_name"])
        if not prior:
            new_repos.append({**repo, "previous_rank": None, "rank_change": None})
            continue
        rank_change = prior["rank"] - repo["rank"]
        repo["previous_rank"] = prior["rank"]
        repo["rank_change"] = rank_change
        if rank_change > 0:
            climbed.append(repo)

    for repo in previous:
        if repo["full_name"] not in current_by_name:
            dropped.append(repo)

    return {
        "new": new_repos,
        "climbed": sorted(climbed, key=lambda item: item["rank_change"], reverse=True),
        "dropped": dropped,
    }


def snapshot_payload(current: list[dict[str, Any]], comparison: dict[str, Any]) -> dict[str, Any]:
    return {
        "generatedAt": utc_now_iso(),
        "sourceUrl": TRENDING_URL,
        "repoCount": len(current),
        "summary": {
            "newCount": len(comparison["new"]),
            "climbedCount": len(comparison["climbed"]),
            "droppedCount": len(comparison["dropped"]),
        },
        "repos": current,
    }


def shortlist_repos(comparison: dict[str, Any], limit: int = 5) -> list[dict[str, Any]]:
    ordered = comparison["new"] + comparison["climbed"]
    unique: list[dict[str, Any]] = []
    seen: set[str] = set()
    for repo in ordered:
        if repo["full_name"] in seen:
            continue
        seen.add(repo["full_name"])
        unique.append(repo)
        if len(unique) >= limit:
            break
    return unique


def build_scan_message(snapshot: dict[str, Any], comparison: dict[str, Any], briefs: list[dict[str, Any]]) -> str:
    lines = [
        "📈 GitHub Trending-koll klar",
        "",
        f"• Nya på listan: {snapshot['summary']['newCount']}",
        f"• Har klättrat: {snapshot['summary']['climbedCount']}",
        f"• Föll av listan: {snapshot['summary']['droppedCount']}",
        f"• Repos på dagens lista: {snapshot['repoCount']}",
    ]

    if not briefs:
        lines.extend(["", "Ingen ny repo eller klättring sedan senaste körningen."])
        return "\n".join(lines).strip()

    lines.extend(["", "🔥 Mest intressanta rörelser"])
    for item in briefs:
        rank_text = f"#{item['rank']}"
        if item.get("movement") == "new":
            movement = "ny"
        else:
            movement = f"upp {item.get('rank_change', 0)}"
        lines.append(
            f"• {item['full_name']} ({rank_text}, {movement}) — {item['purpose_short']} Relevant för {item['relevance_short']}."
        )

    return "\n".join(lines).strip()


def run_scan() -> str:
    ensure_dirs()
    previous_snapshot = load_json(LATEST_FILE, {"repos": []})
    page_html = request_text(TRENDING_URL)
    current_repos = parse_trending_page(page_html)
    if not current_repos:
        raise RuntimeError("GitHub Trending returned no repositories")

    comparison = compare_snapshots(current_repos, previous_snapshot.get("repos", []))
    snapshot = snapshot_payload(current_repos, comparison)

    write_json(LATEST_FILE, snapshot)
    write_json(HISTORY_DIR / f"{local_day_key()}.json", snapshot)

    brief_rows: list[dict[str, Any]] = []
    for repo in shortlist_repos(comparison):
        brief = build_repo_brief_payload(repo["full_name"])
        brief_rows.append(
            {
                **repo,
                "movement": "new" if repo.get("previous_rank") is None else "up",
                "purpose_short": brief["purpose"][:140].rstrip("."),
                "relevance_short": brief["relevance"].replace("relevant for ", "").replace("relevant as ", ""),
            }
        )

    message = build_scan_message(snapshot, comparison, brief_rows)
    append_run_log("SUCCESS", f"new={snapshot['summary']['newCount']} climbed={snapshot['summary']['climbedCount']}")
    return message


def normalize_repo_ref(value: str) -> str:
    cleaned = (value or "").strip()
    cleaned = cleaned.removeprefix("https://github.com/").removeprefix("http://github.com/")
    cleaned = cleaned.strip("/")
    if cleaned.count("/") < 1:
        raise ValueError("Repo must be in owner/repo format or a GitHub repo URL")
    owner, repo = cleaned.split("/", 1)
    repo = repo.split("/")[0]
    return f"{owner}/{repo}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Watch GitHub Trending and build short repo briefs.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("scan", help="Fetch GitHub Trending, diff against the previous run, and save the snapshot.")

    describe_parser = subparsers.add_parser("describe", help="Describe a GitHub repo in short form.")
    describe_parser.add_argument("repo", help="owner/repo or GitHub repo URL")
    describe_parser.add_argument("--refresh", action="store_true", help="Ignore today's cache and refetch repo details")

    args = parser.parse_args()

    try:
        if args.command == "scan":
            print(run_scan())
            return 0

        if args.command == "describe":
            print(describe_repo_text(normalize_repo_ref(args.repo), force_refresh=args.refresh))
            return 0
    except Exception as exc:
        append_run_log("FAIL", str(exc))
        print(f"GitHub Trends watcher failed: {exc}", file=sys.stderr)
        return 1

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
