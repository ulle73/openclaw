from pathlib import Path
path = Path('scripts/youtube_to_knowledge.py')
text = path.read_text()
needle = 'CLASSIFICATION_OPTIONS = [\n'
if needle not in text:
    raise SystemExit('needle not found')
insert = needle + "    'tutorial',\n"  # placeholder to check

PY