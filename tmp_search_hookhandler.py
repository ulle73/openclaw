import pathlib
root = pathlib.Path(r"C:\Users\ryd\AppData\Roaming\npm\node_modules\openclaw")
for path in root.rglob('*'):
    if path.is_file() and path.suffix in {'.ts', '.d.ts', '.js', '.mjs'}:
        try:
            text = path.read_text(encoding='utf-8')
        except Exception:
            continue
        for i,line in enumerate(text.splitlines(), 1):
            if 'HookHandler' in line:
                print(f"{path}:{i}:{line.strip()}")
