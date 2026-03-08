from pathlib import Path
text = Path('scripts/youtube_to_knowledge.py').read_text()
needle = "CLASSIFICATION_OPTIONS = [\n"
start = text.index(needle)
end = text.index(']\n\n', start) + 3
snippet = "\nHEURISTIC_KEYWORDS = {\n    'features': ['feature', 'funktion', 'introduc', 'nyhet'],\n    'tools': ['verktyg', 'app', 'tool', 'plattform'],\n    'workflows': ['workflow', 'flöde', 'process', 'steg'],\n    'guides': ['guide', 'steg', 'tutorial'],\n    'strategic_insights': ['strategi', 'taktik', 'plan'],\n}\n\n"
if 'HEURISTIC_KEYWORDS' not in text:
    text = text[:end] + snippet + text[end:]
    Path('scripts/youtube_to_knowledge.py').write_text(text)
    print('inserted heuristics')
else:
    print('already inserted')
