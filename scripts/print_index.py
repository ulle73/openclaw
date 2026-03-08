from pathlib import Path
text = Path('scripts/youtube_to_knowledge.py').read_text()
start = text.index('    table = INDEX_FILE.read_text')
print(text[start:start+300])
