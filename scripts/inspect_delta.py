import json
from pathlib import Path

data = json.loads(Path('tmp/youtube_meta_delta.json').read_text(encoding='utf-16'))
for key in ['knowledge/youtube/INDEX.jsonl', 'knowledge/youtube/TOPICS.json']:
    info = data['results'].get(key)
    if not info:
        continue
    print(f"--- {key} ---")
    print(info['new_text'])
