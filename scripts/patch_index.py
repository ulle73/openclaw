from pathlib import Path
path = Path('scripts/youtube_to_knowledge.py')
text = path.read_text()
old = "    table = INDEX_FILE.read_text().strip().splitlines()\n    row = (\n        f\"| {info['id']} | {info.get('title','-')} | {info.get('uploader','-')} | {info.get('upload_date','-')} | \"\n        f\"{', '.join(classification)} | {'Yes' if skill_flag else 'No'} | {learned_path} |\"\n    )\n    if row in table:\n        return\n    table.append(row)\n    INDEX_FILE.write_text(\n        "\n".join(table) + "\n"
    )\n"
new = "    table = INDEX_FILE.read_text(encoding='utf-8').strip().splitlines()\n    row = (\n        f\"| {info['id']} | {info.get('title','-')} | {info.get('uploader','-')} | {info.get('upload_date','-')} | \"\n        f\"{', '.join(classification)} | {'Yes' if skill_flag else 'No'} | {learned_path} |\"\n    )\n    if row in table:\n        return\n    table.append(row)\n    INDEX_FILE.write_text(\n        "\n".join(table) + "\n", encoding='utf-8'\n    )\n"
if old not in text:
    raise SystemExit('pattern not found')
path.write_text(text.replace(old, new, 1))
print('updated index encoding')
