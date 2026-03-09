# -*- coding: utf-8 -*-
import json
import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
ACTIVE_PROJECTS_FILE = BASE / "ACTIVE_PROJECTS.md"
PROJECT_INVENTORY_FILE = BASE / "knowledge" / "system" / "project_inventory.json"
PROJECT_INDEX_FILE = BASE / "knowledge" / "projects" / "PROJECT_INDEX.md"

EXCLUDED_ROOTS = {
    ".git",
    ".clawhub",
    ".learnings",
    ".openclaw",
    "knowledge",
    "memory",
    "scripts",
    "__pycache__",
    "node_modules",
}

STACK_HINTS = {
    "next": "nextjs",
    "react": "react",
    "react-dom": "react",
    "tailwindcss": "tailwind",
    "mongodb": "mongodb",
    "supabase": "supabase",
    "expo": "expo",
    "grammy": "telegram-bot",
    "telegram": "telegram",
    "openai": "openai",
    "pinecone": "pinecone",
    "elevenlabs": "voice-ai",
    "typescript": "typescript",
    "python": "python",
    "tsx": "node-tooling",
    "vercel": "vercel",
    "nextjs": "nextjs",
}

TAG_PATTERNS = {
    "betting-analytics": ["betting analytics", "betting", "odds", "edge", "break even", "break-even", "units"],
    "sports-data": ["football", "soccer", "e soccer", "sports data"],
    "ml-models": ["machine learning", "machinelearning", "ml model", "models", "prediction model"],
    "telegram": ["telegram", "telegram bot", "telegram bots"],
    "openclaw": ["openclaw", "open claw"],
    "gravityclaw": ["gravityclaw", "gravity claw"],
    "antigravity": ["antigravity", "anti gravity"],
    "agent-automation": ["ai employee", "agent automation", "agent flow", "assistant", "bot"],
    "workflow-automation": ["automation", "automated", "workflow", "process", "system"],
    "audit-offer": ["audit", "visibility audit", "audit offer"],
    "seo-content": ["seo", "ranking", "content strategy", "content marketing", "visibility"],
    "golf-tech": ["golf", "caddie", "club recommendation", "wind caddie"],
    "web-offer": ["website", "webb", "hemsida", "web offer", "digital tjänst", "digital tjanst"],
    "design-offer": ["design", "branding", "paketering", "premium hemsida"],
    "venture-studio": ["venture studio", "venture", "projektparaply", "experimentlabb"],
    "micro-saas": ["micro saas", "micro-saas"],
    "app-product": ["app product", "mobilapp", "mobile app", "subscription product", "produkt"],
    "voice-ai": ["voice", "voice ai", "elevenlabs"],
    "knowledge-systems": ["memory", "knowledge", "second brain", "knowledge bank"],
    "service-offer": ["offer", "erbjudande", "tjänst", "tjanst", "byrå", "byra"],
    "ai-product": ["ai product", "ai tool", "ai app", "ai service"],
}

GENERIC_README_SNIPPETS = {
    "this is a next.js project bootstrapped",
    "getting started",
    "learn more",
    "deploy on vercel",
    "create-next-app",
    "bootstrapped with",
}

ROOT_PROJECT_HINTS = {
    "workspace": {
        "name": "OpenClaw Workspace",
        "summary": "Jonas lokala OpenClaw workspace med hooks, YouTube knowledge flow, skills och agent-automation.",
        "tags": ["openclaw", "agent-automation", "knowledge-systems", "workflow-automation"],
        "role": "operating_system",
        "priority": 3,
    }
}

REPO_HINTS = {
    "gravity-claw": {
        "summary": "Telegram-nativ AI-copilot med minne, voice, automation och proactive loops.",
        "tags": ["gravityclaw", "openclaw", "telegram", "agent-automation", "knowledge-systems", "voice-ai"],
        "role": "product",
        "priority": 8,
    },
    "awesome-openclaw-skills": {
        "summary": "Referensrepo och inspiration for OpenClaw skills, inte ett primart kund- eller produktprojekt.",
        "tags": ["openclaw", "skill-library", "reference-library"],
        "role": "reference_library",
        "priority": 1,
    },
    "ullebets-vecel": {
        "summary": "Datadriven bettingprodukt med oddsanalys, modeller, dashboards och automation.",
        "tags": ["betting-analytics", "sports-data", "ml-models", "telegram", "app-product"],
        "role": "product",
        "priority": 8,
    },
}

MANUAL_PROJECT_HINTS = {
    "tournado-golf": {
        "tags": ["golf-tech", "app-product", "mobile-app", "subscription-product"],
        "role": "product",
        "priority": 2,
    },
    "ullebets": {
        "tags": ["betting-analytics", "sports-data", "ml-models", "telegram", "app-product"],
        "role": "product",
        "priority": 8,
    },
    "westcoastline-labs": {
        "tags": ["venture-studio", "product-platform", "ai-product"],
        "role": "venture_platform",
        "priority": 7,
    },
    "edel-ventures": {
        "tags": ["venture-studio", "brand-platform", "product-platform"],
        "role": "venture_platform",
        "priority": 6,
    },
    "coastworks": {
        "tags": ["web-offer", "design-offer", "seo-content", "automation", "service-offer"],
        "role": "offer",
        "priority": 10,
    },
    "vibecoda": {
        "tags": ["web-offer", "design-offer", "ai-product", "service-offer"],
        "role": "offer",
        "priority": 7,
    },
    "ai-visibility-audit": {
        "tags": ["audit-offer", "seo-content", "automation", "service-offer"],
        "role": "offer",
        "priority": 9,
    },
}


def slugify(value: str) -> str:
    lowered = (value or "").lower().replace("&", " and ")
    lowered = re.sub(r"[^a-z0-9]+", "-", lowered)
    return re.sub(r"-{2,}", "-", lowered).strip("-")


def title_from_slug(value: str) -> str:
    return " ".join(part.capitalize() for part in value.replace("_", "-").split("-") if part)


def normalize_for_matching(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value or "")
    ascii_value = normalized.encode("ascii", "ignore").decode("ascii").lower()
    ascii_value = ascii_value.replace("&", " and ")
    ascii_value = re.sub(r"[^a-z0-9]+", " ", ascii_value)
    collapsed = re.sub(r"\s{2,}", " ", ascii_value).strip()
    return f" {collapsed} " if collapsed else " "


def text_contains_pattern(text: str, pattern: str) -> bool:
    normalized_text = normalize_for_matching(text)
    normalized_pattern = normalize_for_matching(pattern).strip()
    if not normalized_pattern:
        return False
    return f" {normalized_pattern} " in normalized_text


def extract_tags_from_text(text: str) -> list[str]:
    tags: list[str] = []
    for tag, patterns in TAG_PATTERNS.items():
        if any(text_contains_pattern(text, pattern) for pattern in patterns):
            tags.append(tag)
    return tags


def display_name(raw_name: str) -> str:
    candidate = (raw_name or "").strip()
    if not candidate:
        return ""
    if " " in candidate or any(char.isupper() for char in candidate):
        return candidate
    return title_from_slug(candidate)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def load_package(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def parse_active_projects() -> list[dict]:
    text = read_text(ACTIVE_PROJECTS_FILE)
    lines = text.splitlines()
    projects: list[dict] = []
    current: dict | None = None
    section = ""

    for raw_line in lines:
        line = raw_line.rstrip()
        if line.startswith("## Purpose") or line.startswith("## Rules For This File"):
            if current:
                projects.append(current)
            current = None
            section = ""
            continue
        if line.startswith("## ") and line not in {"## Purpose", "## Rules For This File"}:
            if current:
                projects.append(current)
            name = line[3:].strip()
            current = {
                "projectId": slugify(name),
                "name": name,
                "status": "",
                "type_tags": [],
                "traits": [],
                "why": [],
                "related_memory": [],
                "aliases": [slugify(name)],
            }
            section = ""
            continue
        if not current:
            continue
        if line.strip() == "---":
            continue
        if line.startswith("### "):
            section = line[4:].strip().lower()
            continue
        if line.startswith("- "):
            item = line[2:].strip()
            if section == "type":
                current["type_tags"].append(item)
            elif section == "known traits":
                current["traits"].append(item)
            elif section == "why it matters":
                current["why"].append(item)
            elif section == "related memory":
                current["related_memory"].append(item)
                current["aliases"].append(slugify(item))
            continue
        if section == "status" and line.strip():
            current["status"] = line.strip()

    if current:
        projects.append(current)
    return projects


def discover_repo_roots() -> list[Path]:
    roots = [BASE]
    for child in BASE.iterdir():
        if not child.is_dir():
            continue
        if child.name in EXCLUDED_ROOTS:
            continue
        if (child / ".git").exists() or (child / "package.json").exists() or (child / "README.md").exists():
            roots.append(child)
    return roots


def extract_readme_summary(text: str) -> str:
    if not text:
        return ""
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or line.startswith("```") or line.startswith("<"):
            continue
        lowered = line.lower()
        if any(snippet in lowered for snippet in GENERIC_README_SNIPPETS):
            continue
        if len(line.split()) < 5:
            continue
        return line
    return ""


def collect_repo_file_tokens(root: Path) -> list[str]:
    tokens: list[str] = []
    for child in root.iterdir():
        if child.name.startswith("."):
            continue
        tokens.append(child.name.lower())
    return tokens


def detect_stack(root: Path, package: dict, repo_text: str) -> list[str]:
    stack: list[str] = []
    dependencies = {
        **package.get("dependencies", {}),
        **package.get("devDependencies", {}),
    }
    combined = " ".join([root.name.lower(), " ".join(dependencies.keys()), " ".join(root.parts[-1:])]).lower()
    if (root / "package.json").exists():
        stack.append("node")
    if any(root.glob("*.py")) or (root / "scripts").exists():
        stack.append("python")
    for keyword, label in STACK_HINTS.items():
        if keyword in combined and label not in stack:
            stack.append(label)
    return stack[:10]


def detect_tags(root: Path, repo_text: str) -> list[str]:
    if root == BASE:
        return ROOT_PROJECT_HINTS["workspace"]["tags"][:]
    if root.name in REPO_HINTS:
        return REPO_HINTS[root.name]["tags"][:]
    return extract_tags_from_text(repo_text)[:12]


def infer_repo_summary(root: Path, readme_summary: str, tags: list[str], stack: list[str]) -> str:
    if root == BASE:
        return ROOT_PROJECT_HINTS["workspace"]["summary"]
    if root.name in REPO_HINTS:
        return REPO_HINTS[root.name]["summary"]
    if readme_summary:
        return readme_summary
    if "betting-analytics" in tags:
        return "Datadriven bettingprodukt med oddsanalys, modeller, dashboards och automation."
    if "gravityclaw" in tags or "openclaw" in tags:
        return "Telegram-nativ AI-copilot med minne, voice, automation och proactive loops."
    if "web-offer" in tags:
        return "Webb- eller paketeringsprojekt med tydlig digital erbjudandevinkel."
    return f"Repo i workspace: {root.name}"


def scan_repo(root: Path) -> dict:
    if root == BASE:
        root_hint = ROOT_PROJECT_HINTS["workspace"]
        return {
            "projectId": "workspace",
            "name": root_hint["name"],
            "repoName": root.name,
            "rootPath": str(root),
            "summary": root_hint["summary"],
            "tags": root_hint["tags"][:],
            "stack": ["python"],
            "files": [],
            "signals": sorted(set(root_hint["tags"] + ["python"])),
            "role": root_hint["role"],
        }

    package = load_package(root / "package.json")
    readme = read_text(root / "README.md")
    readme_summary = extract_readme_summary(readme)
    file_tokens = collect_repo_file_tokens(root)
    repo_text = " ".join(
        [
            root.name,
            package.get("name", ""),
            package.get("description", ""),
            readme[:4000],
            " ".join(file_tokens),
        ]
    )
    stack = detect_stack(root, package, repo_text)
    tags = detect_tags(root, repo_text)
    summary = infer_repo_summary(root, readme_summary, tags, stack)
    role = REPO_HINTS.get(root.name, {}).get("role", "repo_only")
    raw_name = package.get("displayName") or package.get("productName") or package.get("name") or root.name
    return {
        "projectId": slugify(package.get("name") or root.name),
        "name": display_name(raw_name),
        "repoName": root.name,
        "rootPath": str(root),
        "summary": summary,
        "tags": tags,
        "stack": stack,
        "files": file_tokens[:20],
        "signals": sorted({tag for tag in tags + stack})[:20],
        "role": role,
        "priority": REPO_HINTS.get(root.name, {}).get("priority", 4 if role == "product" else 3),
    }


def match_manual_project(repo_record: dict, manual_projects: list[dict]) -> dict | None:
    repo_slug = slugify(repo_record["repoName"])
    repo_tags = set(repo_record.get("tags", []))
    best_match = None
    best_score = 0
    for manual in manual_projects:
        aliases = {alias for alias in manual.get("aliases", []) if alias}
        manual_slug = manual["projectId"]
        score = 0
        if repo_slug == manual_slug or repo_slug in aliases or manual_slug in repo_slug:
            score += 6
        manual_tags = {slugify(item) for item in manual.get("type_tags", []) + manual.get("traits", [])}
        score += len(repo_tags & manual_tags) * 2
        if score > best_score:
            best_score = score
            best_match = manual
    return best_match if best_score >= 4 else None


def manual_project_tags(manual_record: dict) -> list[str]:
    tags = MANUAL_PROJECT_HINTS.get(manual_record["projectId"], {}).get("tags", [])[:]
    text = " ".join(
        manual_record.get("type_tags", [])
        + manual_record.get("traits", [])
        + manual_record.get("why", [])
        + manual_record.get("related_memory", [])
    )
    for tag in extract_tags_from_text(text):
        if tag not in tags:
            tags.append(tag)
    return tags[:16]


def merge_project_data(repo_record: dict, manual_record: dict | None) -> dict:
    if not manual_record:
        return {
            "projectId": repo_record["projectId"],
            "name": repo_record["name"],
            "status": "repo-detected",
            "summary": repo_record["summary"],
            "tags": repo_record["tags"],
            "stack": repo_record["stack"],
            "signals": repo_record["signals"],
            "repoPaths": [repo_record["rootPath"]],
            "sourceTypes": ["repo_scan"],
            "whyItMatters": [],
            "projectRole": repo_record.get("role", "repo_only"),
            "projectPriority": repo_record.get("priority", 3),
        }

    tags = manual_project_tags(manual_record)
    for tag in repo_record.get("tags", []):
        if tag not in tags:
            tags.append(tag)
    return {
        "projectId": manual_record["projectId"],
        "name": manual_record["name"],
        "status": manual_record.get("status") or "repo-detected",
        "summary": repo_record["summary"],
        "tags": tags[:16],
        "stack": repo_record.get("stack", []),
        "signals": sorted({*repo_record.get("signals", []), *tags})[:20],
        "repoPaths": [repo_record["rootPath"]],
        "sourceTypes": ["active_projects", "repo_scan"],
        "whyItMatters": manual_record.get("why", []),
        "projectRole": MANUAL_PROJECT_HINTS.get(manual_record["projectId"], {}).get("role", repo_record.get("role", "product")),
        "projectPriority": MANUAL_PROJECT_HINTS.get(manual_record["projectId"], {}).get("priority", repo_record.get("priority", 5)),
    }


def build_project_inventory() -> dict:
    manual_projects = parse_active_projects()
    merged: dict[str, dict] = {}

    for root in discover_repo_roots():
        repo_record = scan_repo(root)
        manual_match = match_manual_project(repo_record, manual_projects)
        project = merge_project_data(repo_record, manual_match)
        existing = merged.get(project["projectId"])
        if existing:
            existing["repoPaths"] = sorted(set(existing["repoPaths"] + project["repoPaths"]))
            existing["sourceTypes"] = sorted(set(existing["sourceTypes"] + project["sourceTypes"]))
            existing["tags"] = sorted(set(existing["tags"] + project["tags"]))
            existing["stack"] = sorted(set(existing["stack"] + project["stack"]))
            existing["signals"] = sorted(set(existing["signals"] + project["signals"]))
            existing["whyItMatters"] = existing["whyItMatters"] or project["whyItMatters"]
            existing["projectPriority"] = max(existing.get("projectPriority", 0), project.get("projectPriority", 0))
        else:
            merged[project["projectId"]] = project

    for manual in manual_projects:
        if manual["projectId"] in merged:
            continue
        tags = manual_project_tags(manual)
        merged[manual["projectId"]] = {
            "projectId": manual["projectId"],
            "name": manual["name"],
            "status": manual.get("status") or "manual-only",
            "summary": " ".join(manual.get("why", [])[:2]) or manual["name"],
            "tags": tags[:16],
            "stack": [],
            "signals": tags[:20],
            "repoPaths": [],
            "sourceTypes": ["active_projects"],
            "whyItMatters": manual.get("why", []),
            "projectRole": MANUAL_PROJECT_HINTS.get(manual["projectId"], {}).get("role", "manual_only"),
            "projectPriority": MANUAL_PROJECT_HINTS.get(manual["projectId"], {}).get("priority", 5),
        }

    projects = sorted(
        merged.values(),
        key=lambda item: (
            "active_projects" not in item.get("sourceTypes", []),
            -item.get("projectPriority", 0),
            item["name"].lower(),
        ),
    )
    payload = {
        "generatedAt": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "projects": projects,
    }
    return payload


def write_project_inventory(payload: dict) -> None:
    PROJECT_INVENTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    PROJECT_INVENTORY_FILE.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    PROJECT_INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Project Index",
        "",
        f"Generated: {payload.get('generatedAt', '')}",
        "",
    ]
    for project in payload.get("projects", []):
        lines.append(f"## {project['name']}")
        lines.append(f"- Priority: {project.get('projectPriority', 0)}")
        lines.append(f"- Role: {project.get('projectRole', 'unknown')}")
        lines.append(f"- Status: {project.get('status', 'unknown')}")
        lines.append(f"- Summary: {project.get('summary', '')}")
        lines.append(f"- Tags: {', '.join(project.get('tags', [])) or '-'}")
        lines.append(f"- Stack: {', '.join(project.get('stack', [])) or '-'}")
        lines.append(f"- Repo paths: {', '.join(project.get('repoPaths', [])) or '-'}")
        if project.get("whyItMatters"):
            lines.append(f"- Why it matters: {' | '.join(project['whyItMatters'])}")
        lines.append("")
    PROJECT_INDEX_FILE.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")


def main() -> int:
    payload = build_project_inventory()
    write_project_inventory(payload)
    print(f"[project-inventory] projects={len(payload.get('projects', []))} output={PROJECT_INVENTORY_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
