from pathlib import Path
text = Path('GravityClaw.en.txt').read_text(encoding='utf-8').lower()
keywords = ['clause','mission','control','listen','connect','voice','telegram','dashboard','mission control','claw','gravity']
for keyword in keywords:
    if keyword in text:
        idx = text.index(keyword)
        snippet = text[max(0, idx-200):idx+200]
        print('\n---{}---\n{}'.format(keyword, snippet[:400]))
