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


def write_summary(target: Path, cleaned_text: str, info: dict) -> None:
    normalized_sentences = [normalize_sentence(s) for s in split_sentences(cleaned_text) if normalize_sentence(s)]
    tldr = normalized_sentences[:3] if normalized_sentences else ([normalize_sentence(cleaned_text)] if cleaned_text.strip() else [])
    key = normalized_sentences[3:7] if len(normalized_sentences) > 3 else normalized_sentences[:3]
    tags = generate_summary_tags(cleaned_text, info)
    parts = ['# Summary', '', '## TL;DR']
    parts.extend([f'- {sentence}' for sentence in tldr if sentence])
    if not tldr:
        parts.append('- No transcript content available to summarize.')
    parts.extend(['', '## Key takeaways'])
    if key:
        parts.extend([f'- {sentence}' for sentence in key if sentence])
    else:
        parts.append('- Nothing beyond the TL;DR stood out.')
    parts.extend(['', '## Suggested tags'])
    parts.extend([f'- {tag}' for tag in tags])
    target.joinpath('summary.md').write_text('\n'.join(parts).strip() + '\n', encoding='utf-8')


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
    write_summary(target, cleaned_text, info)
    analysis_input = cleaned_text if cleaned_text.strip() else clean_text
    analysis_raw = local_analysis(analysis_input, info)
    analysis = ensure_analysis(analysis_raw, info)
    (target / "learned.md").write_text(build_learned(info, analysis), encoding="utf-8")
    (target / "skill_candidate.md").write_text(evaluate_skill(analysis), encoding="utf-8")
    classification = analysis.get('classification') or []
    skill_flag = analysis.get('skill_candidate', {}).get('should_create', False)
    update_index(info, f"youtube/{vid}/learned.md", classification, bool(skill_flag))
    meta = {
        "id": info.get('id'),
        "title": info.get('title'),
        "channel": info.get('uploader'),
        "upload_date": info.get('upload_date'),
        "description": info.get('description'),
        "classifications": classification,
        "skill_candidate": bool(skill_flag),
        "updated_at": datetime.now(timezone.utc).isoformat(),
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
