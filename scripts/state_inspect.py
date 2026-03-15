import json
from pathlib import Path
state = json.loads(Path('knowledge/system/youtube_meta_read_state.json').read_text(encoding='utf-8'))
print(state['files']['knowledge/ideas\\2026-03-09-digest.md'])
