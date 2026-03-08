from pathlib import Path
path = Path('scripts/youtube_to_knowledge.py')
text = path.read_text()
insert_point = text.index('HEURISTIC_KEYWORDS')
if 'def split_sentences' not in text:
    snippet = """\n\ndef split_sentences(text):\n    return [s.strip() for s in __import__('re').split(r'(?<=[.!?])\\s+', text) if s.strip()]\n\n\ndef heuristic_extract(text, keywords, limit=3):\n    sentences = split_sentences(text)\n    hits = []\n    for sentence in sentences:\n        lower = sentence.lower()\n        if any(keyword in lower for keyword in keywords):\n            hits.append(sentence.strip())\n        if len(hits) >= limit:\n            break\n    return hits\n\n\ndef simple_classifications(text):\n    mapping = {\n        'tutorial': ['how to', 'guide', 'tutorial', 'så här'],\n        'tool demo': ['verktyg', 'demo', 'tool'],\n        'feature breakdown': ['feature', 'funktion'],\n        'strategy': ['strategi', 'plan'],\n        'workflow': ['workflow', 'flöde', 'process'],\n        'automation idea': ['automation', 'automatisera'],\n        'business idea': ['affärside', 'business'],\n        'prompt engineering': ['prompt'],\n        'technical guide': ['teknisk', 'setup'],\n    }\n    lower = text.lower()\n    found = []\n    for klass, keywords in mapping.items():\n        if any(keyword in lower for keyword in keywords):\n            found.append(klass)\n    return found\n"""
    text = text[:insert_point] + snippet + text[insert_point:]
    path.write_text(text)
    print('added heuristic functions')
else:
    print('heuristic functions already present')
