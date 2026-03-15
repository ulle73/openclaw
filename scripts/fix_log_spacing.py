from pathlib import Path
path = Path('knowledge/ideas/youtube_meta_validation_log.jsonl')
data = path.read_text()
data = data.replace('}\n\n{"timestamp": "2026-03-15T12:20:00Z"', '}\n{"timestamp": "2026-03-15T12:20:00Z"')
path.write_text(data)
