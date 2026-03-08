# GravityClaw — AntiGravity co-pilot

This project reproduces Jack Roberts’ GravityClaw (Connect · Listen · Archive · Wire · Sense) inside a single TypeScript + Telegram bot stack. Everything runs locally unless you deploy to Railway.

## Quick start
1. Copy `.env.example` → `.env` and fill in your tokens (Telegram bot + user, Pinecone, OpenRouter/OpenAI, 11Labs, Gro/Whisper, Railway, Zappy, etc.).
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run locally:
   ```bash
   npm run dev
   ```
   The bot uses long polling via `grammy`. Messages only respond to your Telegram user ID.
4. For proactive sense/heartbeat run:
   ```bash
   npm run heartbeat
   ```
   This launches a cron job that uses the same bot token to message you each morning at 08:00 by default (change in `.env`).

## Structure
- `src/` — runtime files
  - `config.ts` – central env loader
  - `telegram.ts` – grammy bot + voice flow
  - `agent.ts` – Claude/OpenRouter agent + memory
  - `memory.ts` – SQLite + FTS + Pinecone
  - `voice.ts` – ElevenLabs + Gro/Whisper integration
  - `index.ts` – bootstrap
- `scripts/heartbeat.ts` – cron job for sense messages.
- `resources/*.md` – prompt templates + CL.A.W.S. cheat sheet.
- `transcripts/*` – raw transcripts pulled from the YouTube video.

## Deploying (Railway)
Follow the SOP in `gravityclaw files/gravityclaw update.txt`:
1. Install Railway CLI (`npm install -g @railway/cli`).
2. `railway login`, `railway link` inside this folder.
3. Push env vars via `railway variables set ...` (copy from `.env`).
4. `railway down` locally before `npm run dev`.
5. After testing, `npm run tsc`, then `railway up --detach`.
6. Use `railway logs --lines 60` to confirm `✅ Heartbeat scheduled` and `✅ Connected as @ryd_claw`.

## Voice + Memory
- Voice: Telegram voice → Gro transcription → Claude → ElevenLabs TTS.
- Memory: SQLite + FTS5 for immediate context + Pinecone for long-term retrieval.
- Agent loops keep max 600 tokens and log interactions in the DB.

## Next steps
- Add MCP JSON, React dashboard, or extra connectors if you want to mimic the GravityClaw web UI (references in `gravityclaw files`).
- Automate `scripts/heartbeat.ts` as a Railway cron job using `railway up`.
- Use `resources/init_prompt_template.md` and `scripts/generate_init_prompt.py` to generate the same init prompt GravityClaw uses.
