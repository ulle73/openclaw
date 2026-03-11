# Coastworks Command Center (local)

## Start
```bash
cd C:\Users\ryd\.openclaw\workspace\coastworks-command-center
npm start
```

Open: http://localhost:4310

## Includes
- Workspace mirror tree
- Agent list + model mapping (from `AGENT_MODELS.md`)
- Token/cost estimate per agent (parsed from `~/.openclaw/agents/*/sessions/*.jsonl`)
- YouTube full ingest trigger (`scripts/ingest_youtube_url.py <url>`)
- Daily history snapshot
- Knowledge index panel
- Kanban board with assign-to-agent flow

## Assign Flow
When you assign a task to `boss|radar|codey|moneymaker`, the server runs:
```bash
python scripts/delegate_agent_message.py --agent <agent> --message "<task prompt>"
```
Task status auto-moves:
- `In Progress` on assign
- `Review` on successful run
- `Blocked` if run fails

## Files
- `server.mjs` API + runner
- `public/` UI
- `data/tasks.json` task state
- `data/state.json` run history
