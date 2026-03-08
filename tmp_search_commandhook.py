import pathlib
root = pathlib.Path(r"C:\Users\ryd\AppData\Roaming\npm\node_modules\openclaw")
for path in root.rglob('*.d.ts'):
    try:
        text = path.read_text(encoding='utf-8')
    except Exception:
        continue
    if 'Command' in text and 'Hook' in text:
        if 'CommandHook' in text:
            print(path)
