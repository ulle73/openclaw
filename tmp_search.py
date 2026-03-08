import pathlib
import sys
for path in pathlib.Path('.').rglob('*.ts'):
    try:
        text = path.read_text(encoding='utf-8')
    except Exception:
        continue
    for i, line in enumerate(text.splitlines(), 1):
        if 'openclaw/hooks' in line:
            print(f"{path}:{i}:{line.strip()}")
