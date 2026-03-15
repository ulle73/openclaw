import json
from pathlib import Path

path = Path('tmp/youtube_meta_delta.json')
data = json.loads(path.read_text(encoding='utf-16'))
for path, info in sorted(data['results'].items()):
    if not info['has_new']:
        continue
    snippet = info['new_text'][:200].replace('\n', ' ') + ('...' if len(info['new_text']) > 200 else '')
    print(f"{path}\n  size={info['size']} hash={info['hash']} offset={info['offset']} has_new={info['has_new']}\n  snippet={snippet}\n")
