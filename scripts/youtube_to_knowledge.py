# -*- coding: utf-8 -*-
import argparse
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import List

BASE_DIR = Path(__file__).resolve().parents[1]
KNOWLEDGE_DIR = BASE_DIR / "knowledge" / "youtube"
INDEX_FILE = BASE_DIR / "knowledge" / "INDEX.md"
INDEX_JSONL_FILE = KNOWLEDGE_DIR / "INDEX.jsonl"

CLASSIFICATION_OPTIONS = [
    "tutorial",
    "tool demo",
    "feature breakdown",
    "strategy",
    "workflow",
    "automation idea",
    "business idea",
    "prompt engineering",
    "technical guide",
]




def split_sentences(text):
    return [s.strip() for s in __import__('re').split(r'(?<=[.!?])\s+', text) if s.strip()]


def heuristic_extract(text, keywords, limit=3):
    sentences = split_sentences(text)
    hits = []
    for sentence in sentences:
        lower = sentence.lower()
        if any(keyword in lower for keyword in keywords):
            hits.append(sentence.strip())
        if len(hits) >= limit:
            break
    return hits


AD_REMOVAL_KEYWORDS = [
    "profit boardroom",
    "profit boarding",
    "ai profit",
    "playbook",
    "kurs",
    "cohort",
    "community",
    "discord",
    "newsletter",
    "patreon",
    "sponsor",
    "sponsored",
    "brought to you by",
    "partner",
    "affiliate",
    "use code",
    "discount",
    "sign up",
    "link in description",
]


def detect_ad_keyword(line: str) -> str | None:
    lower = line.lower()
    for keyword in AD_REMOVAL_KEYWORDS:
        if keyword in lower:
            return keyword
    return None


def remove_ad_segments(lines: List[str]) -> tuple[List[str], List[dict]]:
    kept: List[str] = []
    segments: List[dict] = []
    buffer: List[str] = []
    reason: str | None = None
    for line in lines:
        ad_keyword = detect_ad_keyword(line)
        if ad_keyword:
            buffer.append(line)
            if not reason:
                reason = ad_keyword
            continue
        if buffer:
            segments.append({
                "lines": buffer.copy(),
                "reason": reason or "promo segment",
            })
            buffer.clear()
            reason = None
        kept.append(line)
    if buffer:
        segments.append({
            "lines": buffer.copy(),
            "reason": reason or "promo segment",
        })
    return kept, segments


def simple_classifications(text):
    mapping = {
        'tutorial': ['how to', 'guide', 'tutorial', 's� h�r'],
        'tool demo': ['verktyg', 'demo', 'tool'],
        'feature breakdown': ['feature', 'funktion'],
        'strategy': ['strategi', 'plan'],
        'workflow': ['workflow', 'fl�de', 'process'],
        'automation idea': ['automation', 'automatisera'],
        'business idea': ['aff�rside', 'business'],
        'prompt engineering': ['prompt'],
        'technical guide': ['teknisk', 'setup'],
    }
    lower = text.lower()
    found = []
    for klass, keywords in mapping.items():
        if any(keyword in lower for keyword in keywords):
            found.append(klass)
    return found


SUMMARY_TAGS = {
    'openclaw': 'openclaw',
    'automation': 'automation-workflows',
    'ai profit': 'ai-profit-boardroom',
    'ai': 'ai',
    'agent': 'agent-teams',
    'playbook': 'automation-playbooks',
    'community': 'community',
    'youtube': 'youtube',
    'prompt': 'prompt-engineering',
}


def normalize_sentence(sentence: str) -> str:
    return " ".join(sentence.split())


def generate_summary_tags(cleaned_text: str, info: dict) -> list[str]:
    data = ' '.join([cleaned_text, info.get('title', ''), info.get('description', '')]).lower()
    tags: list[str] = []
    for keyword, tag in SUMMARY_TAGS.items():
        if keyword in data and tag not in tags:
            tags.append(tag)
    if 'youtube' not in tags:
        tags.append('youtube')
    if 'knowledge-bank' not in tags:
        tags.append('knowledge-bank')
    return tags[:6]


CATEGORY_KEYWORDS = {
    "tool": ["tool", "verktyg", "software", "saas", "platform", "app"],
    "workflow": ["workflow", "process", "playbook", "steps", "system"],
    "business_idea": ["business idea", "affärsidé", "offer", "service idea", "startup"],
    "seo_distribution": ["seo", "distribution", "traffic", "ranking", "backlink", "content strategy"],
    "agent_flow": ["agent flow", "multi-agent", "agent", "agents"],
    "automation": ["automation", "automate", "automatis"],
    "app_idea": ["app idea", "micro-saas", "build an app", "app business"],
    "product_opportunity": ["product", "pricing", "package", "product opportunity", "offer"],
    "mcp": ["mcp", "model context protocol"],
    "api": ["api", "sdk", "endpoint", "oauth"],
}

SWEDISH_LABELS = {
    "low": "låg",
    "medium": "medel",
    "high": "hög",
}

ACTION_BY_CATEGORY = {
    "tool": "Testa verktyget i ett av Jonas aktiva projekt och dokumentera fit/gap.",
    "workflow": "Bryt ner workflowet till en återanvändbar mall eller automation.",
    "business_idea": "Gör en snabb Idea Fit Report för svensk marknad eller tydlig nisch.",
    "seo_distribution": "Formulera ett konkret distributions- eller SEO-experiment som kan testas direkt.",
    "agent_flow": "Avgör om detta ska bli ett agentflöde eller en skill i den befintliga stacken.",
    "automation": "Identifiera vad som kan automatiseras direkt och vad som kräver manuell validering först.",
    "app_idea": "Bedöm om detta passar som app eller micro-SaaS med tydlig monetiseringsväg.",
    "product_opportunity": "Skissa ett säljbart erbjudande med tydlig ROI och nästa teststeg.",
    "mcp": "Utvärdera om MCP-spåret ger bättre hävstång än nuvarande implementation.",
    "api": "Kontrollera integration, auth-modell och om OAuth-vägen är möjlig.",
}

LOW_SIGNAL_PATTERNS = [
    "hey, if we haven't met already",
    "comment below",
    "link is in the description",
    "links are in the comments and description",
    "go grab them",
    "see you inside",
    "come check it out",
    "join the",
    "i'm the digital avatar",
    "reads every comment",
    "quick pause before we go deeper",
    "if you want to learn",
    "start completely free",
]

USE_CASE_GROUPS = {
    "utbildning och onboarding": ["education", "training program", "students", "members", "onboarding"],
    "marketing och explainers": ["marketing", "landing page", "ad", "explainer video", "cold audiences"],
    "repurposing av gammalt content": ["repurposing old content", "blog posts", "webinars", "pdf guides"],
    "snabba veckouppdateringar": ["weekly updates", "ai news", "roundup doc", "visually engaging update"],
}


def write_chunks(target: Path, lines: List[str], chunk_size: int = 10) -> None:
    out = ['# Chunks', '']
    for idx in range(0, len(lines), chunk_size):
        block = lines[idx: idx + chunk_size]
        if not block:
            continue
        out.append(f'## Chunk {idx // chunk_size + 1:02d}')
        out.append('\n'.join(block))
        out.append('')
    target.joinpath('chunks.md').write_text('\n'.join(out).strip() + '\n', encoding='utf-8')


def dedupe_keep_order(items: List[str]) -> List[str]:
    seen = set()
    result = []
    for item in items:
        normalized = item.strip()
        if not normalized:
            continue
        key = normalized.lower()
        if key in seen:
            continue
        seen.add(key)
        result.append(normalized)
    return result


def contains_any(text: str, keywords: List[str]) -> bool:
    lowered = text.lower()
    return any(keyword.lower() in lowered for keyword in keywords)


def natural_join(items: List[str]) -> str:
    cleaned = [item.strip() for item in items if item.strip()]
    if not cleaned:
        return ""
    if len(cleaned) == 1:
        return cleaned[0]
    if len(cleaned) == 2:
        return f"{cleaned[0]} och {cleaned[1]}"
    return ", ".join(cleaned[:-1]) + f" och {cleaned[-1]}"


def is_low_signal_sentence(sentence: str) -> bool:
    normalized = normalize_sentence(sentence)
    lower = normalized.lower()
    if len(normalized.split()) < 5:
        return True
    return any(pattern in lower for pattern in LOW_SIGNAL_PATTERNS)


def clean_title_for_summary(title: str) -> str:
    if not title:
        return ""
    cleaned = re.sub(r"[^\w\s+&/\-]", " ", title)
    cleaned = re.split(r"\bis\b|\bare\b", cleaned, maxsplit=1, flags=re.IGNORECASE)[0]
    cleaned = re.sub(r"\b(new|insane|crazy|must watch|update)\b", " ", cleaned, flags=re.IGNORECASE)
    cleaned = " ".join(cleaned.split()).strip(" -+/")
    return cleaned


def collect_step_labels(lower_text: str) -> List[str]:
    steps: List[str] = []
    if contains_any(lower_text, ["upload your sources", "upload a document", "upload them"]):
        steps.append("ladda upp källmaterial")
    if "video overview" in lower_text:
        steps.append("generera en video overview")
    if contains_any(lower_text, ["visual style", "pick your visual style", "style"]):
        steps.append("välja visuell stil")
    if contains_any(lower_text, ["focus prompt", "angle to take", "one prompt changes the entire direction"]):
        steps.append("sätta en tydlig fokusprompt")
    if contains_any(lower_text, ["export and post", "post it straight away", "ready to use"]):
        steps.append("exportera och publicera")
    return dedupe_keep_order(steps)


def collect_use_cases(lower_text: str) -> List[str]:
    found: List[str] = []
    for label, keywords in USE_CASE_GROUPS.items():
        if contains_any(lower_text, keywords):
            found.append(label)
    return found


def yaml_quote(value: str) -> str:
    return str(value or "").replace("\\", "\\\\").replace('"', '\\"')


def to_iso_date(raw_date: str | None) -> str:
    if not raw_date:
        return ""
    if len(raw_date) == 8 and raw_date.isdigit():
        return f"{raw_date[0:4]}-{raw_date[4:6]}-{raw_date[6:8]}"
    return raw_date


def detect_categories(cleaned_text: str, info: dict, analysis: dict) -> List[str]:
    data = " ".join(
        [
            cleaned_text,
            info.get("title", ""),
            info.get("description", ""),
            " ".join(analysis.get("classification", []) or []),
        ]
    ).lower()
    found: List[str] = []
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in data for keyword in keywords):
            found.append(category)
    if "workflow" in (analysis.get("classification") or []) and "workflow" not in found:
        found.append("workflow")
    return dedupe_keep_order(found)


def label_for_score(score: int) -> str:
    if score >= 8:
        return "high"
    if score >= 5:
        return "medium"
    return "low"


def build_summary_metadata(cleaned_text: str, info: dict, analysis: dict) -> dict:
    categories = detect_categories(cleaned_text, info, analysis)
    roi_score = 3
    relevance_score = 4

    if any(category in categories for category in ["business_idea", "product_opportunity", "app_idea"]):
        roi_score += 3
        relevance_score += 2
    if any(category in categories for category in ["tool", "workflow", "automation", "agent_flow", "mcp", "api"]):
        roi_score += 2
        relevance_score += 2
    if "seo_distribution" in categories:
        roi_score += 1
        relevance_score += 1
    if analysis.get("monetization"):
        roi_score += 1
    if analysis.get("automation_opportunities"):
        relevance_score += 1

    roi_score = min(10, roi_score)
    relevance_score = min(10, relevance_score)

    should = {
        "skill": bool(analysis.get("skill_candidate", {}).get("should_create")) or any(
            category in categories for category in ["tool", "workflow", "agent_flow", "mcp", "api"]
        ),
        "automation": any(category in categories for category in ["automation", "workflow", "agent_flow"]),
        "idea_bank": any(category in categories for category in ["business_idea", "app_idea", "product_opportunity"]),
        "system_improvement": any(
            category in categories for category in ["workflow", "automation", "seo_distribution", "tool"]
        ),
        "app": "app_idea" in categories,
        "product": any(category in categories for category in ["product_opportunity", "business_idea"]),
    }

    return {
        "categories": categories,
        "roi_score": roi_score,
        "relevance_score": relevance_score,
        "roi_label": label_for_score(roi_score),
        "relevance_label": label_for_score(relevance_score),
        "should": should,
    }


def build_takeaways(
    normalized_sentences: List[str],
    cleaned_text: str,
    info: dict,
    analysis: dict,
    summary_meta: dict,
) -> List[str]:
    lower_text = cleaned_text.lower()
    filtered_sentences = [sentence for sentence in normalized_sentences if not is_low_signal_sentence(sentence)]
    topic = clean_title_for_summary(info.get("title", "")) or analysis.get("core_topic") or "verktygskombinationen"
    takeaways: List[str] = []

    if contains_any(lower_text, ["upload a document", "upload your sources", "full narrated video", "video overviews"]):
        takeaways.append(
            f"Videon visar hur {topic} kan förvandla dokument och annat källmaterial till färdiga videor med AI-visuals och voiceover utan traditionell produktion."
        )

    if contains_any(lower_text, ["brain", "art department", "powers the visuals", "research tool"]):
        takeaways.append(
            "Rollfördelningen är tydlig: Notebook LM står för research och struktur, medan Nano Banana 2 driver bildgenereringen och den visuella stilen."
        )

    step_labels = collect_step_labels(lower_text)
    if step_labels:
        takeaways.append(f"Workflowet är tydligt: {natural_join(step_labels)}.")

    use_cases = collect_use_cases(lower_text)
    if use_cases:
        takeaways.append(
            f"De starkaste use casen är {natural_join(use_cases)}, vilket gör att samma upplägg kan användas både internt och externt."
        )

    if contains_any(
        lower_text,
        [
            "depends almost entirely on the prompts and sources",
            "bad input equals generic output",
            "great input equals content",
            "focus prompt changes the entire direction",
        ],
    ):
        takeaways.append(
            "Den avgörande faktorn är inputen: bättre källor och skarpare prompts ger fokuserad output, medan svag input ger generiskt material."
        )

    if contains_any(
        lower_text,
        [
            "ahead of everyone",
            "ahead of your competitors",
            "grow faster with less effort",
            "save time",
            "content machine",
        ],
    ):
        takeaways.append(
            "Affärsvärdet ligger i fart och edge: du kan skapa mer content snabbare, återanvända gammalt material och få en tidig distributionsfördel."
        )

    categories = summary_meta.get("categories", [])
    if "workflow" in categories:
        takeaways.append("Det här bör ses som ett repeterbart content-workflow, inte bara som en enskild feature-demo.")
    if "automation" in categories or "agent_flow" in categories:
        takeaways.append("Potentialen ligger i att systematisera och automatisera produktionen snarare än att skapa varje video manuellt.")
    if "product_opportunity" in categories or "business_idea" in categories:
        takeaways.append("Samma upplägg kan paketeras som intern process, tjänst till kund eller ett produktiserat erbjudande.")
    if "seo_distribution" in categories:
        takeaways.append("Det här är lika mycket ett distributionsverktyg som ett produktionsverktyg, eftersom samma material kan återanvändas i flera format och kanaler.")

    if len(takeaways) < 5:
        for sentence in filtered_sentences:
            if len(sentence.split()) < 8:
                continue
            takeaways.append(sentence)
            if len(dedupe_keep_order(takeaways)) >= 5:
                break

    fallback = dedupe_keep_order(takeaways)
    if not fallback:
        fallback = filtered_sentences[:5] or ["Inget tydligt stack ut utöver grundbeskrivningen av videon."]
    return fallback[:5]


def build_usage_for_jonas(summary_meta: dict, takeaways: List[str]) -> List[str]:
    ideas: List[str] = []
    categories = summary_meta.get("categories", [])
    if any(category in categories for category in ["tool", "automation", "workflow", "agent_flow"]):
        ideas.append("Detta kan omsättas till ett återanvändbart system, skill eller intern automation för Jonas egna projekt eller kundcase.")
    if any(category in categories for category in ["business_idea", "product_opportunity", "app_idea"]):
        ideas.append("Detta kan testas som ett tjänstepaket, en produktiserad process eller ett eget intäktsdrivet spår för svenska SME-bolag.")
    if "seo_distribution" in categories:
        ideas.append("Detta kan användas för onboarding-videor, explainers och distributionsklipp från redan befintligt material.")
    if not ideas and takeaways:
        ideas.append("Spara detta i kunskapsbanken och bevaka om samma tema återkommer i fler videos, då det ofta signalerar ett systematiserbart spår.")
    return dedupe_keep_order([idea for idea in ideas if idea])[:3] or [
        "Spara detta i kunskapsbanken och bevaka om temat återkommer i fler relevanta videos."
    ]


def build_next_actions(summary_meta: dict) -> List[str]:
    actions: List[str] = []
    for category in summary_meta.get("categories", []):
        action = ACTION_BY_CATEGORY.get(category)
        if action:
            actions.append(action)
    if not actions:
        actions.append("Spara videon i kunskapsbanken och återkom om temat dyker upp igen.")
    return dedupe_keep_order(actions)[:3]


def build_should_lines(summary_meta: dict) -> List[str]:
    should = summary_meta["should"]
    categories = summary_meta["categories"]
    return [
        f"- Skill: {'ja' if should['skill'] else 'nej'} + {'Passar som återanvändbar komponent eller operativ mall.' if should['skill'] else 'Ingen tydlig återanvändbar skill ännu.'}",
        f"- Automation: {'ja' if should['automation'] else 'nej'} + {'Innehållet pekar på ett flöde som sannolikt går att automatisera.' if should['automation'] else 'Saknar tydligt automationscase just nu.'}",
        f"- Idébank: {'ja' if should['idea_bank'] else 'nej'} + {'Bör sparas som idéspår med affärsvinkel.' if should['idea_bank'] else 'Mer execution-spår än nytt idéspår.'}",
        f"- Systemförbättring: {'ja' if should['system_improvement'] else 'nej'} + {'Kan förbättra befintligt arbetssätt eller knowledge-flöde.' if should['system_improvement'] else 'Ger ingen tydlig systemförbättring nu.'}",
        f"- App: {'ja' if should['app'] else 'nej'} + {'Har tydlig app- eller micro-SaaS-vinkel.' if should['app'] else 'Inte stark nog som appspår ännu.'}",
        f"- Produkt: {'ja' if should['product'] else 'nej'} + {'Kan paketeras som säljbart erbjudande eller produktspår.' if should['product'] else 'Inte tillräckligt tydlig produktmöjlighet ännu.'}",
        f"- Kategorier: {', '.join(categories) if categories else 'inga tydliga kategorier identifierade'}",
    ]


def build_label_reason(label: str, summary_meta: dict, axis: str) -> str:
    categories = summary_meta.get("categories", [])
    if axis == "roi":
        if label == "high":
            return "Flera kategorier pekar på snabb testbarhet, tydlig hävstång eller produktmöjlighet."
        if label == "medium":
            return "Det finns användbarhet här, men affärsnyttan kräver mer validering."
        return "Innehållet verkar mer informativt än direkt intäkts- eller hävstångsdrivande."
    if label == "high":
        return "Det ligger nära Jonas fokus på AI-produkter, automation, agentflöden eller svensk marknadsfit."
    if label == "medium":
        return "Det är delvis relevant, men kopplingen till aktuella spår är inte helt självklar."
    return "Kopplingen till Jonas nuvarande prioriteringar är svag eller indirekt."


def build_tldr(takeaways: List[str], normalized_sentences: List[str]) -> List[str]:
    if takeaways:
        return takeaways[:3]
    return normalized_sentences[:3] if normalized_sentences else []


def write_summary(target: Path, cleaned_text: str, info: dict, analysis: dict) -> dict:
    normalized_sentences = [normalize_sentence(s) for s in split_sentences(cleaned_text) if normalize_sentence(s)]
    summary_meta = build_summary_metadata(cleaned_text, info, analysis)
    takeaways = build_takeaways(normalized_sentences, cleaned_text, info, analysis, summary_meta)
    tldr = build_tldr(takeaways, normalized_sentences) or ([normalize_sentence(cleaned_text)] if cleaned_text.strip() else [])
    usage_for_jonas = build_usage_for_jonas(summary_meta, takeaways)
    next_actions = build_next_actions(summary_meta)
    roi_label = summary_meta["roi_label"]
    relevance_label = summary_meta["relevance_label"]
    should_lines = build_should_lines(summary_meta)

    frontmatter = [
        "---",
        f'videoId: "{yaml_quote(info.get("id", ""))}"',
        f'sourceUrl: "{yaml_quote(f"https://www.youtube.com/watch?v={info.get("id", "")}")}"',
        f'title: "{yaml_quote(info.get("title", ""))}"',
        f'channel: "{yaml_quote(info.get("uploader") or info.get("channel") or "")}"',
        f'published: "{to_iso_date(info.get("upload_date"))}"',
        "categories: [" + ", ".join(f'"{category}"' for category in summary_meta["categories"]) + "]",
        "",
        f'roi_label: "{roi_label}"',
        f'relevance_label: "{relevance_label}"',
        "",
        "should:",
        f"  skill: {'true' if summary_meta['should']['skill'] else 'false'}",
        f"  automation: {'true' if summary_meta['should']['automation'] else 'false'}",
        f"  idea_bank: {'true' if summary_meta['should']['idea_bank'] else 'false'}",
        f"  system_improvement: {'true' if summary_meta['should']['system_improvement'] else 'false'}",
        f"  app: {'true' if summary_meta['should']['app'] else 'false'}",
        f"  product: {'true' if summary_meta['should']['product'] else 'false'}",
        "---",
        "# TL;DR",
    ]

    body = list(frontmatter)
    body.extend([f"- {sentence}" for sentence in tldr if sentence] or ["- Ingen tydlig transcripttext fanns att sammanfatta."])
    body.extend(["", "# 5 viktigaste takeaways"])
    body.extend([f"{index}. {item}" for index, item in enumerate(takeaways or ["Inget tydligt stack ut utöver TL;DR."], start=1)])
    body.extend(["", "# Hur detta kan användas för mig"])
    body.extend([f"- {item}" for item in usage_for_jonas])
    body.extend(["", "# Next actions (max 3)"])
    body.extend([f"{index}. {item}" for index, item in enumerate(next_actions, start=1)])
    body.extend(["", "# Bör detta bli?"])
    body.extend(should_lines[:6])
    body.extend(["", "# ROI / potential"])
    body.append(f"- {SWEDISH_LABELS[roi_label]} — {build_label_reason(roi_label, summary_meta, 'roi')}")
    body.extend(["", "# Relevans för mig"])
    body.append(f"- {SWEDISH_LABELS[relevance_label]} — {build_label_reason(relevance_label, summary_meta, 'relevance')}")
    target.joinpath('summary.md').write_text('\n'.join(body).strip() + '\n', encoding='utf-8')
    return summary_meta


def write_transcript_md(target: Path, canonical_url: str, vid: str, info: dict, text: str) -> None:
    parts = [
        '# Transcript',
        '',
        f'- URL: {canonical_url}',
        f'- VideoId: {vid}',
    ]
    if info.get('title'):
        parts.append(f"- Title: {info['title']}")
    parts.extend(['', '## Transcript', text])
    target.joinpath('transcript.md').write_text('\n'.join(parts).strip() + '\n', encoding='utf-8')


def write_transcript_clean(target: Path, cleaned_text: str) -> None:
    target.joinpath('transcript_clean.txt').write_text(cleaned_text, encoding='utf-8')
    target.joinpath('transcript_clean.md').write_text(f'# Clean Transcript\n\n{cleaned_text}\n', encoding='utf-8')


def write_source_url(target: Path, canonical_url: str) -> None:
    target.joinpath('source.url').write_text(canonical_url + '\n', encoding='utf-8')


def write_excluded_ads(target: Path, segments: List[dict]) -> None:
    path = target.joinpath('excluded_ads.md')
    if not segments:
        if path.exists():
            path.unlink()
        return
    parts = ['# Excluded Ads', '']
    for idx, segment in enumerate(segments, start=1):
        reason = segment.get('reason', 'promo segment')
        parts.extend([f'## Segment {idx}', f'Reason: Removed sponsor/promo segment ({reason})', ''])
        parts.extend(segment.get('lines', []))
        parts.append('')
    path.write_text('\n'.join(parts).strip() + '\n', encoding='utf-8')


HEURISTIC_KEYWORDS = {
    'features': ['feature', 'funktion', 'introduc', 'nyhet'],
    'tools': ['verktyg', 'app', 'tool', 'plattform'],
    'workflows': ['workflow', 'flode', 'process', 'steg'],
    'guides': ['guide', 'steg', 'tutorial'],
    'strategic_insights': ['strategi', 'taktik', 'plan'],
}



def run_yt_dlp(url: str, outdir: Path) -> Path:
    cmd = [
        "yt-dlp",
        "--skip-download",
        "--write-info-json",
        "--write-auto-sub",
        "--sub-lang",
        "en",
        "-o",
        str(outdir / "%(id)s.%(ext)s"),
        url,
    ]
    subprocess.run(cmd, check=True)
    info_files = list(outdir.glob("*.info.json"))
    if not info_files:
        raise RuntimeError("Info json missing after yt-dlp")
    return info_files[0]


def clean_vtt(vtt_path: Path) -> str:
    lines = []
    for line in vtt_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("WEBVTT") or re.search("-->", line) or line.startswith("Kind:") or line.startswith("Language:"):
            continue
        line = re.sub(r"<[^>]+>", "", line)
        line = re.sub(r"\[[^\]]+\]", "", line)
        if line:
            lines.append(line)
    deduped = []
    for line in lines:
        if deduped and line.lower() == deduped[-1].lower():
            continue
        deduped.append(line)
    return "\n".join(deduped)


def local_analysis(clean_text: str, info: dict) -> dict:
    base_text = clean_text.strip() or info.get("description", "")
    sentences = split_sentences(base_text)
    lower = base_text.lower()
    core_topic = info.get("title") or sentences[0] if sentences else "Video"
    core_idea = sentences[0] if sentences else info.get("description", "")
    skill_keywords = ["automation", "workflow", "playbook", "agent", "dashboard", "course", "training", "system", "tool"]
    skill_hit = next((keyword for keyword in skill_keywords if keyword in lower), None)
    skill_candidate = {
        "should_create": bool(skill_hit),
        "reason": f"Mentions {skill_hit} which could justify a reusable automation skill" if skill_hit else "",
        "skill_description": (
            "Package the mentioned automation/playbook into a reusable agent or prompt" if skill_hit else ""
        ),
        "draft_outline": (
            "1. Define the task and desired ROI\n2. Collect prompts/data references\n3. Build a repeatable assistant flow" if skill_hit else ""
        ),
    }
    return {
        "core_topic": core_topic,
        "core_idea": core_idea,
        "features": heuristic_extract(base_text, HEURISTIC_KEYWORDS["features"]),
        "tools": heuristic_extract(base_text, HEURISTIC_KEYWORDS["tools"]),
        "workflows": heuristic_extract(base_text, HEURISTIC_KEYWORDS["workflows"]),
        "guides": heuristic_extract(base_text, HEURISTIC_KEYWORDS["guides"]),
        "strategic_insights": heuristic_extract(base_text, HEURISTIC_KEYWORDS["strategic_insights"]),
        "monetization": heuristic_extract(base_text, ["pengar", "intakt", "affar", "revenue", "subscription"]),
        "automation_opportunities": heuristic_extract(base_text, ["automation", "automatisera", "automate"]),
        "relevance_to_me": sentences[1] if len(sentences) > 1 else "Visar hur detta kopplar till återkommande intäkt eller scaling.",
        "related_concepts": simple_classifications(base_text),
        "classification": simple_classifications(base_text),
        "skill_candidate": skill_candidate,
    }


def ensure_analysis(analysis: dict, info: dict) -> dict:
    base = {
        "core_topic": info.get("title", "Unknown topic"),
        "core_idea": info.get("description", ""),
        "features": [],
        "tools": [],
        "workflows": [],
        "guides": [],
        "strategic_insights": [],
        "monetization": [],
        "automation_opportunities": [],
        "relevance_to_me": "Säger något om varför detta relaterar till dina projekt.",
        "related_concepts": [],
        "classification": [],
        "skill_candidate": {"should_create": False},
    }
    base.update({k: v for k, v in analysis.items() if v})
    return base


def build_learned(info: dict, analysis: dict) -> str:
    sections = [f"# {info.get('title', 'Video')}\n"]
    sections.append(f"## Core Topic\n{analysis.get('core_topic')}\n")
    sections.append(f"## Core Idea\n{analysis.get('core_idea')}\n")
    for label, key in [
        ("Features & Highlights", "features"),
        ("Tools Mentioned", "tools"),
        ("Workflows", "workflows"),
        ("Step-by-step Guides", "guides"),
        ("Strategic Insights", "strategic_insights"),
        ("Monetization", "monetization"),
        ("Automation Opportunities", "automation_opportunities"),
    ]:
        items = analysis.get(key, [])
        if items:
            sections.append(f"## {label}\n" + "\n".join(f"- {item}" for item in items) + "\n")
    sections.append(f"## Relevance for Jonas\n{analysis.get('relevance_to_me')}\n")
    related = analysis.get('related_concepts', [])
    if related:
        sections.append("## Related Concepts / Videos\n" + "\n".join(f"- {concept}" for concept in related) + "\n")
    classifications = analysis.get('classification') or []
    if classifications:
        sections.append("## Classification\n" + ", ".join(classifications) + "\n")
    return "\n".join(sections)


def evaluate_skill(analysis: dict) -> str:
    candidate = analysis.get('skill_candidate', {})
    lines = ["# Skill Candidate"]
    should = candidate.get('should_create')
    lines.append(f"- Should create: {'Yes' if should else 'No'}")
    if reason := candidate.get('reason'):
        lines.append(f"- Reason: {reason}")
    if desc := candidate.get('skill_description'):
        lines.append(f"- Description: {desc}")
    if draft := candidate.get('draft_outline'):
        lines.append("- Draft:\n" + draft)
    lines.append("- Question:\n  Vill du att denna skill byggs nu?\n")
    return "\n".join(lines)


def ensure_index_header():
    if not INDEX_FILE.exists():
        INDEX_FILE.write_text("# YouTube Knowledge Index\n\n| Video ID | Title | Channel | Date | Classification | Skill Candidate | Learned |\n|---|---|---|---|---|---|---|\n")


def update_index(info: dict, learned_path: str, classification: list, skill_flag: bool):
    ensure_index_header()
    table = INDEX_FILE.read_text(encoding='utf-8').strip().splitlines()
    row = (
        f"| {info['id']} | {info.get('title','-')} | {info.get('uploader','-')} | {info.get('upload_date','-')} | "
        f"{', '.join(classification)} | {'Yes' if skill_flag else 'No'} | {learned_path} |"
    )
    if row in table:
        return
    table.append(row)
    INDEX_FILE.write_text("\n".join(table) + "\n", encoding='utf-8')


def load_index_video_ids() -> set[str]:
    if not INDEX_JSONL_FILE.exists():
        return set()
    ids: set[str] = set()
    for line in INDEX_JSONL_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        video_id = row.get("videoId")
        if video_id:
            ids.add(video_id)
    return ids


def append_index_jsonl(info: dict, summary_meta: dict, discovered_at: str, ingested_at: str) -> None:
    INDEX_JSONL_FILE.parent.mkdir(parents=True, exist_ok=True)
    video_id = info.get("id")
    if not video_id:
        return
    if video_id in load_index_video_ids():
        return
    row = {
        "videoId": video_id,
        "sourceUrl": f"https://www.youtube.com/watch?v={video_id}",
        "title": info.get("title", ""),
        "channel": info.get("uploader") or info.get("channel") or "",
        "published": to_iso_date(info.get("upload_date")),
        "discoveredAt": discovered_at,
        "ingestedAt": ingested_at,
        "categories": summary_meta.get("categories", []),
        "roi_label": summary_meta.get("roi_label", "low"),
        "relevance_label": summary_meta.get("relevance_label", "low"),
        "paths": {
            "baseDir": f"knowledge/youtube/{video_id}",
            "summary": f"knowledge/youtube/{video_id}/summary.md",
            "chunks": f"knowledge/youtube/{video_id}/chunks.md",
            "transcript": f"knowledge/youtube/{video_id}/transcript.md",
        },
    }
    with INDEX_JSONL_FILE.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def ingest(url: str):
    if not KNOWLEDGE_DIR.exists():
        KNOWLEDGE_DIR.mkdir(parents=True)
    match = re.search(r"(?:v=|youtu\.be/)([\w-]+)", url)
    if not match:
        raise ValueError("Could not extract video id")
    vid = match.group(1)
    target = KNOWLEDGE_DIR / vid
    target.mkdir(parents=True, exist_ok=True)
    info_json = run_yt_dlp(url, target)
    info = json.loads(info_json.read_text(encoding="utf-8"))
    canonical_url = f"https://www.youtube.com/watch?v={vid}"
    raw_vtt = target / f"{vid}.en.vtt"
    raw_txt = target / "transcript.raw.txt"
    clean_md = target / "transcript.clean.md"
    if raw_vtt.exists():
        clean_text = clean_vtt(raw_vtt)
        raw_txt.write_text(raw_vtt.read_text(encoding="utf-8"), encoding="utf-8")
        clean_md.write_text(clean_text, encoding="utf-8")
    else:
        clean_text = info.get('description', '')
        raw_txt.write_text(clean_text, encoding="utf-8")
        clean_md.write_text(clean_text, encoding="utf-8")
    target.joinpath('transcript.txt').write_text(clean_text, encoding='utf-8')
    raw_lines = clean_text.splitlines()
    cleaned_lines, excluded_segments = remove_ad_segments(raw_lines)
    cleaned_text = "\n".join(cleaned_lines)
    write_transcript_md(target, canonical_url, vid, info, clean_text)
    write_transcript_clean(target, cleaned_text)
    write_source_url(target, canonical_url)
    write_excluded_ads(target, excluded_segments)
    write_chunks(target, cleaned_lines)
    analysis_input = cleaned_text if cleaned_text.strip() else clean_text
    analysis_raw = local_analysis(analysis_input, info)
    analysis = ensure_analysis(analysis_raw, info)
    summary_meta = write_summary(target, cleaned_text, info, analysis)
    (target / "learned.md").write_text(build_learned(info, analysis), encoding="utf-8")
    (target / "skill_candidate.md").write_text(evaluate_skill(analysis), encoding="utf-8")
    classification = summary_meta.get("categories") or analysis.get('classification') or []
    skill_flag = analysis.get('skill_candidate', {}).get('should_create', False)
    update_index(info, f"youtube/{vid}/learned.md", classification, bool(skill_flag))
    now_iso = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    append_index_jsonl(info, summary_meta, now_iso, now_iso)
    meta = {
        "id": info.get('id'),
        "title": info.get('title'),
        "channel": info.get('uploader'),
        "upload_date": info.get('upload_date'),
        "description": info.get('description'),
        "classifications": classification,
        "roi_label": summary_meta.get("roi_label"),
        "relevance_label": summary_meta.get("relevance_label"),
        "should": summary_meta.get("should"),
        "skill_candidate": bool(skill_flag),
        "updated_at": now_iso,
    }
    (target / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Ingested {vid}")


def main():
    parser = argparse.ArgumentParser(description="Ingest a YouTube video into the knowledge bank")
    parser.add_argument("url", help="YouTube video URL")
    args = parser.parse_args()
    ingest(args.url)


if __name__ == "__main__":
    main()
