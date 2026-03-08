from pathlib import Path
path = Path('scripts/youtube_to_knowledge.py')
text = path.read_text()
start = text.index('def fallback_analysis')
end = text.index('\n\ndef run_yt_dlp', start)
new = '''def fallback_analysis(clean_text, info):
    return {
        "core_topic": info.get("title", "Video"),
        "core_idea": info.get("description", "").split("\\n")[0],
        "features": heuristic_extract(clean_text, HEURISTIC_KEYWORDS['features']),
        "tools": heuristic_extract(clean_text, HEURISTIC_KEYWORDS['tools']),
        "workflows": heuristic_extract(clean_text, HEURISTIC_KEYWORDS['workflows']),
        "guides": heuristic_extract(clean_text, HEURISTIC_KEYWORDS['guides']),
        "strategic_insights": heuristic_extract(clean_text, HEURISTIC_KEYWORDS['strategic_insights']),
        "monetization": heuristic_extract(clean_text, ['pengar', 'intakt', 'affar']),
        "automation_opportunities": heuristic_extract(clean_text, ['automation', 'automatisera']),
        "relevance_to_me": "Beskriver varfor det har kan vara relevant for nuvarande spar.",
        "related_concepts": simple_classifications(clean_text),
        "classification": simple_classifications(clean_text),
        "skill_candidate": {"should_create": False},
    }

HEURISTIC_KEYWORDS = {
    'features': ['feature', 'funktion', 'introduc', 'nyhet'],
    'tools': ['verktyg', 'app', 'tool', 'plattform'],
    'workflows': ['workflow', 'flode', 'process', 'steg'],
    'guides': ['guide', 'steg', 'tutorial'],
    'strategic_insights': ['strategi', 'taktik', 'plan'],
}

'''
text = text[:start] + new + text[end:]
path.write_text(text)
print('fallback block reset')
