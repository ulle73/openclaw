from pathlib import Path
text_path = Path('qigPUMrOMH0.en.txt')
if not text_path.exists():
    raise SystemExit('transcript missing')
text = text_path.read_text(encoding='utf-8').strip()
words = text.split()
max_words = 200
chunks = []
for i in range(0, len(words), max_words):
    chunk = ' '.join(words[i:i+max_words]).strip()
    if chunk:
        chunks.append(chunk)
out_path = Path('C:/Users/ryd/Desktop/test-chunk.txt')
out_path.parent.mkdir(parents=True, exist_ok=True)
with out_path.open('w', encoding='utf-8') as f:
    for idx, chunk in enumerate(chunks, 1):
        f.write(f"== Chunk {idx} ==\n{chunk}\n\n")
print('wrote', len(chunks), 'chunks to', out_path)
