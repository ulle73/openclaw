from pathlib import Path
path = Path('scripts/youtube_to_knowledge.py')
text = path.read_text()
start = text.index('HEURISTIC_KEYWORDS')
end = text.index('\n\ndef run_yt_dlp', start)
new = '''HEURISTIC_KEYWORDS = {
    'features': ['feature', 'funktion', 'introduc', 'nyhet'],
    'tools': ['verktyg', 'app', 'tool', 'plattform'],
    'workflows': ['workflow', 'flode', 'process', 'steg'],
    'guides': ['guide', 'steg', 'tutorial'],
    'strategic_insights': ['strategi', 'taktik', 'plan'],
}

'''
text = text[:start] + new + text[end:]
path.write_text(text)
print('keywords rewritten')
