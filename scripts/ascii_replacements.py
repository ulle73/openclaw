from pathlib import Path
path = Path('scripts/youtube_to_knowledge.py')
text = path.read_text()
text = text.replace('"business idea": [\'affärside\'', '"business idea": [\'affaride\'')
text = text.replace('\'flöde\'', '\'flode\'')
path.write_text(text)
print('done replacements')
