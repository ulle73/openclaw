import json
from pathlib import Path
entry = {
    "timestamp": "2026-03-15T12:20:00Z",
    "ideas": [
        {
            "id": "openclaw-browser-agent",
            "summary": "OpenClaw's new browser agent attaches to Chrome's user profile via remote debugging so the agent can run Gmail, LinkedIn, and social posts with permission gating.",
            "decision": "TEST",
            "scores": {"uniqueness": 8, "roi": 9, "speed": 7, "sweden_fit": 9, "confidence": 7},
            "videos": ["J_RNzdX1yiQ"]
        }
    ],
    "sources": [
        "web_search blocked: missing Brave API key",
        "web_fetch yewtu.be/watch?v=J_RNzdX1yiQ and yewtu.eu/watch?v=J_RNzdX1yiQ returned 403"
    ],
    "notes": "Validation relies on repo summaries; re-run searches once API key is in place."
}
Path('knowledge/ideas/youtube_meta_validation_log.jsonl').write_text(Path('knowledge/ideas/youtube_meta_validation_log.jsonl').read_text() + '\n' + json.dumps(entry, ensure_ascii=False))
