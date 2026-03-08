# GravityClaw build plan

This file translates the five-step CL.A.W.S. strategy from the transcript into concrete tasks. Each step references the same sections in `transcripts/GravityClaw.en.txt`. Run the helper script after you finish Step 0 to keep your prompts tied to your identity.

## Step 0 – Prep and credentials
1. Install the local prerequisites mentioned at view time (Telegram, Docker, Node.js).
2. Create a Telegram bot via BotFather (bot name `gravity_claw_bot`), copy the bot token, and capture your Telegram user ID via `userinfobot`. Store both in `.env` (see `.env.example`).
3. Sign up for OpenRouter (or your preferred LLM hub) and grab an API key. Use the same account to power the anti-gravity agent (see Connect details below).
4. Reserve accounts / tokens for these services:
   - **OpenRouter / your chosen LLM** for auto-reasoning (connect step).
   - **11 Labs** for TTS output and emotional voice (listen step).
   - **Gro (console.gro.com)** or OpenAI Whisper for voice transcription (listen step).
   - **Pinecone (or another vector store)** for the memory archive (archive step).
   - **Railway** for the heartbeat cron job so the agent can run when your laptop is asleep (sense step).
   - **Zappy/Zapia (or other MCP connectors)** to bridge Gmail, Notion, Supabase, etc. (wire step).
5. Copy `resources/init_prompt_template.md` into `resources/GravityClaw-init-prompt.md` using `scripts/generate_init_prompt.py` once the env file is ready.

## Step 1 – Connect (C)
*Source: `transcripts/GravityClaw.en.txt#L90-L190`.*
- Use the provided initialization prompt (`resources/GravityClaw-init-prompt.md`) so anti-gravity understands the “open core, local-first loop” architecture.
- Set up a new anti-gravity project folder; run planning mode with Opus 4.6 thinking to scaffold the `Grammar` plan.
- Attach Telegram, open the bot chat, and show AntiGravity the API tokens (Telegram bot token + Telegram user ID) so GravityClaw only responds to you.
- Give GravityClaw the OpenRouter (LLM) key so it can reason locally without hitting an unsafe chain. Record those secrets in `.env` with key names from `.env.example`.

## Step 2 – Listen (L)
*Source: `transcripts/GravityClaw.en.txt#L400-L520`.*
- Log into 11 Labs, create an API key, and paste it into the agent (TTS). Choose the Creative voice and low-latency tier described in the transcript.
- Create a Gro (or Whisper) API key for speech-to-text; paste it into the agent so GravityClaw can understand Telegram voice messages.
- Verify voice round-tripping by sending a Telegram voice message and asking the agent to repeat it back (the transcript shows the prompt: “Hey there dude, repeat the message then answer”).
- Add any extra voice controls you need (e.g., ability to send speech responses via 11 Labs) and confirm the agent can speak, listen, and respond.

## Step 3 – Archive (A)
*Source: `transcripts/GravityClaw.en.txt#L530-L640`.*
- Build the three-tier memory: core system prompt + short-term buffer + Pinecone long-term vector store.
- Provide Pinecone API key (and optionally environment/region) via `.env` and allow GravityClaw to store memories in the vector database that can be retrieved semantically.
- Confirm the agent can describe the memory structure (the transcript shows it drawing a diagram and explaining when memories are created).
- Use the memory system to keep “semantic long-term memory” to avoid repeating context in every message.

## Step 4 – Wire (W)
*Source: `transcripts/GravityClaw.en.txt#L737-L880`.*
- Visit the MCP servers dashboard, add connectors such as Notion, Supabase, Vercel, GitHub, Gmail (via Zappy), and any other data sources you need.
- Build a dashboard (Mark-inspired) that lets you drag-and-drop features you want the agent to know (voice, WhatsApp, web hooks, knowledge graphs, etc.).
- Deploy the dashboard (per transcript, it uses Vercel) so GravityClaw can show live logs, connectors, and the generated instructions.
- Validate multi-app workflows — e.g., ask GravityClaw about the last email subject line (via MCP) to ensure connectors are live.

## Step 5 – Sense (S)
*Source: `transcripts/GravityClaw.en.txt#L896-L1120`.*
- Implement a Node cron job (`heartbeat.ts` + `index.ts`) that hits Telegram every morning at 08:00 and asks accountability questions (“Have you logged your weight?”, “What’s one goal for today?”).
- Give the agent the ability to send proactive messages and load context (500 token limit set in the transcript to save credits).
- When you need the agent to run while your laptop is closed, deploy the repo to Railway (or another secure host) as shown in the video — pair your device with the deployment via the Railway CLI and tokens.
- Confirm remote deployment stats (deployments list, logs, etc.) via the Railway dashboard and ensure you only run one instance at a time (no parallel laptop + Railway runs).

## Optional
- Turn the entire Flow into an OpenClaw skill so you can share it with others; AntiGravity can convert the plan into a skill once you mark the workflow as stable.
- Add more automations (e.g., voice playback via 11 Labs, deeper data pulls from Gmail) by instructing AntiGravity with natural language and letting it update the plan.

## Deliverables
- `.env` with real tokens.
- `resources/GravityClaw-init-prompt.md` populated by `scripts/generate_init_prompt.py`.
- Deployed heartbeat on Railway + recorded logs/metrics.
- Documented MCP connectors + dashboards.
- Verified voice, memory, and scheduled sense checks.
