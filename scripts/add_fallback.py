from pathlib import Path
path = Path('scripts/youtube_to_knowledge.py')
text = path.read_text()
if 'def fallback_analysis' in text:
    print('fallback already present')
else:
    insert_after = text.index('HEURISTIC_KEYWORDS')
    snippet = """

def fallback_analysis(clean_text, info):
    return {
        "core_topic": info.get("title", "Video"),
        "core_idea": info.get("description", "").split('\n')[0],
        "features": heuristic_extract(clean_text, HEURISTIC_KEYWORDS['features']),
        "tools": heuristic_extract(clean_text, HEURISTIC_KEYWORDS['tools']),
        "workflows": heuristic_extract(clean_text, HEURISTIC_KEYWORDS['workflows']),
        "guides": heuristic_extract(clean_text, HEURISTIC_KEYWORDS['guides']),
        "strategic_insights": heuristic_extract(clean_text, HEURISTIC_KEYWORDS['strategic_insights']),
        "monetization": heuristic_extract(clean_text, ['pengar', 'intäkt', 'affär']),
        "automation_opportunities": heuristic_extract(clean_text, ['automation', 'automatisera']),
        "relevance_to_me": "Beskriver varför det här kan vara relevant för nuvarande spår.",
        "related_concepts": simple_classifications(clean_text),
        "classification": simple_classifications(clean_text),
        "skill_candidate": {"should_create": False},
    }
"""
    text = text[:insert_after] + snippet + text[insert_after:]
    path.write_text(text)
    print('fallback inserted')
