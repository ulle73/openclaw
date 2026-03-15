import json
import os
import glob
import hashlib
import sys

sys.stdout.reconfigure(encoding='utf-8')

state_path = 'knowledge/system/youtube_meta_read_state.json'
with open(state_path, 'r', encoding='utf-8') as f:
    state = json.load(f)
files_state = state.get('files', {})

targets = ['knowledge/youtube/INDEX.jsonl', 'knowledge/youtube/TOPICS.json']
topics = glob.glob('knowledge/topics/*/signals.json')
ideas = glob.glob('knowledge/ideas/*-digest.md')
memory = ['memory/youtube_cron_runs.md', 'memory/youtube_synthesis_runs.md']
all_paths = sorted(set(targets + topics + ideas + memory))

results = {}

for path in all_paths:
    if not os.path.isfile(path):
        continue
    prev = files_state.get(path, {})
    offset = prev.get('offset', prev.get('size', 0))
    current_size = os.path.getsize(path)
    if offset > current_size:
        offset = 0
    new_bytes = bytearray()
    sha = hashlib.sha256()
    bytes_read = 0
    with open(path, 'rb') as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            sha.update(chunk)
            chunk_len = len(chunk)
            if bytes_read + chunk_len > offset:
                start = max(0, offset - bytes_read)
                new_bytes.extend(chunk[start:])
            bytes_read += chunk_len
    new_text = new_bytes.decode('utf-8', errors='ignore')
    has_new = bool(new_text.strip()) if current_size != offset or offset == 0 else False
    results[path] = {
        'new_text': new_text,
        'size': current_size,
        'hash': sha.hexdigest(),
        'modified': os.path.getmtime(path),
        'offset': current_size,
        'has_new': has_new
    }

print(json.dumps({'results': results}, ensure_ascii=False))
