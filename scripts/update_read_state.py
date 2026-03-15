import json
from pathlib import Path
state_path = Path('knowledge/system/youtube_meta_read_state.json')
delta_path = Path('tmp/youtube_meta_delta.json')

delta = json.loads(delta_path.read_text(encoding='utf-16'))
state = json.loads(state_path.read_text(encoding='utf-8'))
files = state.get('files', {})
for path, info in delta['results'].items():
    files[path] = {
        'size': info['size'],
        'hash': info['hash'],
        'modified': info['modified'],
        'offset': info['offset']
    }
state['files'] = files
state_path.write_text(json.dumps(state, indent=2), encoding='utf-8')
