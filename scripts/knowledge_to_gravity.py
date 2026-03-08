import json
from pathlib import Path

BASE = Path(__file__).resolve().parents[1]
KNOWLEDGE_DIR = BASE / "knowledge" / "youtube"
GRAVITY_CORPUS = BASE / "gravity-claw" / "knowledge_corpus.json"

def gather():
    entries = []
    for video_dir in sorted(KNOWLEDGE_DIR.iterdir()):
        if not video_dir.is_dir():
            continue
        meta_file = video_dir / "meta.json"
        learned = video_dir / "learned.md"
        if not meta_file.exists() or not learned.exists():
            continue
        meta = json.loads(meta_file.read_text(encoding="utf-8"))
        entries.append({
            "id": meta.get("id"),
            "title": meta.get("title"),
            "channel": meta.get("channel"),
            "summary": learned.read_text(encoding="utf-8"),
            "classifications": meta.get("classifications", []),
            "skill_candidate": meta.get("skill_candidate", False),
            "path": str(video_dir.relative_to(BASE)),
        })
    GRAVITY_CORPUS.write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {len(entries)} knowledge entries to {GRAVITY_CORPUS}")

if __name__ == "__main__":
    gather()
