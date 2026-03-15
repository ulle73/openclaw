import json
from pathlib import Path
state = json.loads(Path('tmp/youtube_meta_delta.json').read_text(encoding='utf-16'))
print(list(state['results'].keys())[:10])
for key, info in state['results'].items():
    if 'knowledge/ideas' in key:
        print(key, info.get('offset'))
        break
