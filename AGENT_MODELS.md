# AGENT MODELS

## Purpose
This file is the quick map for per-agent model assignments.

The live config is in:
- `C:\Users\ryd\.openclaw\openclaw.json`

Each agent now has its own explicit `model.primary` entry, so you can change one agent without affecting the others.

## Current State
- `main`: `openai-codex/gpt-5.3-codex`
- `boss`: `openai-codex/gpt-5.3-codex`
- `radar`: `openai-codex/gpt-5.1-codex-mini`
- `codey`: `openai-codex/gpt-5.1-codex-mini`
- `moneymaker`: `openai-codex/gpt-5.1-codex-mini`

## Suggested Future Split
- `boss`: balanced general model
- `radar`: strongest reasoning / research model
- `codey`: strong coding model
- `moneymaker`: strong reasoning or balanced commercial model
- `main`: leave on the current safe default unless you want the default agent to change too

## How To Change Later
Edit only the `primary` value for the agent you want inside `C:\Users\ryd\.openclaw\openclaw.json`.

Example:

```json
{
  "id": "radar",
  "name": "Radar",
  "workspace": "C:\\Users\\ryd\\.openclaw\\workspace-radar",
  "agentDir": "C:\\Users\\ryd\\.openclaw\\agents\\radar\\agent",
  "model": {
    "primary": "openai-codex/gpt-5.4"
  }
}
```

## Practical Rule
- change `radar` first when you want deeper research
- change `codey` first when you want stronger code quality
- change `boss` only if you want the main conversational agent to change behavior
- leave `main` alone unless you intentionally want a new default baseline
