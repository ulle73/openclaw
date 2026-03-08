from pathlib import Path
path = Path('scripts/youtube_to_knowledge.py')
text = path.read_text()
for old, new in [('int�kt','intakt'), ('aff�r','affar'), ('fl�de','flode'), ('varf�r','varfor'), ('h�r','har'), ('sp�r','spar')]:
    text = text.replace(old, new)
path.write_text(text)
print('cleanup2 done')
