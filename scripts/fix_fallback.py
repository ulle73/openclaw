from pathlib import Path
path = Path('scripts/youtube_to_knowledge.py')
text = path.read_text()
text = text.replace('"core_idea": info.get("description", "").split('\n')[0],', '"core_idea": info.get("description", "").split("\\n")[0],')
text = text.replace('"monetization": heuristic_extract(clean_text, ['\n', ' '], ? )','')
PY