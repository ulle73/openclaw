from pathlib import Path
text = Path('GravityClaw.en.txt').read_text(encoding='utf-8')
for line in text.split('\n'):
    if 'stand' in line.lower():
        print(line)
