import pathlib
root = pathlib.Path(r"C:\Users\ryd\AppData\Roaming\npm\node_modules\openclaw\dist")
for path in root.rglob('*.js'):
    try:
        text = path.read_text(encoding='utf-8')
    except Exception:
        continue
    if 'command:new' in text:
        for i,line in enumerate(text.splitlines(),1):
            if 'command:new' in line:
                print(f"{path}:{i}:{line.strip()}")
