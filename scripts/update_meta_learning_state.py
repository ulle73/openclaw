import json
from datetime import datetime, timezone
from pathlib import Path

state_path = Path('knowledge/system/youtube_meta_learning_state.json')
state = json.loads(state_path.read_text(encoding='utf-8'))
now = datetime(2026, 3, 15, 12, 20, tzinfo=timezone.utc).isoformat().replace('+00:00', 'Z')
state['lastRun'] = now
state.setdefault('topicSignatures', {})
state['topicSignatures']['automate__browser-agent__openclaw'] = now

flows = state.setdefault('flows', [])

for flow in flows:
    if flow.get('id') == 'openclaw-paperclip-command-center':
        vids = flow.setdefault('videos', [])
        if '58T9kb3OFJs' not in vids:
            vids.append('58T9kb3OFJs')
        flow['description'] = "OpenClaw + PaperClip command center now doubles as a distribution-ready command center, making agent work visible and repurposing content and onboarding dashboards from the new OpenClaw update."
        break
else:
    flows.append({
        'id': 'openclaw-paperclip-command-center',
        'description': "OpenClaw + PaperClip command center now doubles as a distribution-ready command center, making agent work visible and repurposing content and onboarding dashboards from the new OpenClaw update.",
        'videos': ['58T9kb3OFJs'],
        'tags': ['openclaw', 'paperclip', 'agent-flow', 'dashboard', 'automation']
    })

flows.append({
    'id': 'openclaw-browser-agent',
    'description': "OpenClaw's new browser agent attaches to Chrome's real user profile via remote debugging so the agent can run Gmail, LinkedIn, and social posts, making the command center act on real browser data with permission gating.",
    'videos': ['J_RNzdX1yiQ'],
    'tags': ['openclaw', 'browser-agent', 'remote-debugging', 'automation', 'telegram']
})

state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding='utf-8')
