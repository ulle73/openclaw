from pathlib import Path
import re
text = Path('GravityClaw.en.vtt').read_text(encoding='utf-8')
lines = []
last = ''
for line in text.splitlines():
    line = line.strip()
    if not line:
        continue
    if line.startswith('WEBVTT') or line.startswith('Kind:') or line.startswith('Language:'):
        continue
    if '-->' in line:
        continue
    line = re.sub(r'<.*?>', '', line)
    if not line or line.startswith('['):
        continue
    if line == last:
        continue
    lines.append(line)
    last = line
Path('GravityClaw.en.txt').write_text('\n'.join(lines), encoding='utf-8')
