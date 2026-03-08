import pathlib
root = pathlib.Path(r"C:\Users\ryd\AppData\Roaming\npm\node_modules\openclaw")
for path in root.rglob('*.d.ts'):
    try:
        text = path.read_text(encoding='utf-8')
    except Exception:
        continue
    for i, line in enumerate(text.splitlines(), 1):
        if 'openclaw/hooks' in line:
            print(f"{path}:{i}:{line.strip()}")
