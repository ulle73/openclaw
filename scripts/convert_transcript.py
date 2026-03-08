from pathlib import Path
import re
path = Path('qigPUMrOMH0.en.vtt')
if not path.exists():
    raise SystemExit('VTT file not found')
lines = []
for raw in path.read_text(encoding='utf-8').splitlines():
    line = raw.strip()
    if not line or '-->' in line or line.startswith('WEBVTT') or line.startswith('Kind:'):
        continue
    clean = re.sub(r'<[^>]+>', '', line)
    clean = clean.replace('\ufeff', '')
    clean = clean.strip()
    if not clean:
        continue
    if lines and lines[-1] == clean:
        continue
    lines.append(clean)
out = Path('qigPUMrOMH0.en.txt')
out.write_text('\n'.join(lines), encoding='utf-8')
print('wrote', len(lines), 'lines to', out)
