# C.L.A.W.S. cheat sheet
Derived directly from `transcripts/GravityClaw.en.txt` so you can trace every instruction back to the video.

| Step | Description | Key tooling | Transcript reference |
| --- | --- | --- | --- |
| **Connect** | Bootstrap the project (download resource, copy the initialization prompt, create a folder, set up Telegram + Docker + Node.js, supply OpenRouter token). | Telegram bot (BotFather), OpenRouter key, Docker, Node.js, anti-gravity planning mode. | lines 90‑190 |
| **Listen** | Enable two-way voice: 11 Labs for emotional TTS, Gro/Whisper for STT, and add prompts that ask the agent to repeat what you just said before replying. | 11 Labs API, Gro (or Whisper), Telegram voice messages. | lines 400‑520 |
| **Archive** | Build a semantic memory stack (system prompt, conversation buffer, Pinecone long-term store). The agent should articulate how memories are stored and which entity owns which tier. | Pinecone vector database; optional Supabase/SQLite for metadata. | lines 530‑620 |
| **Wire** | Connect MCP services (Zappy/Zapia for Gmail, GitHub, Notion, Supabase, Vercel) and surface the connection dashboard so the agent can route commands through any linked app. | MCP dashboard, Zappy, Notion, Supabase, Vercel, GitHub, Zappy connectors. | lines 737‑880, 1045‑1080 |
| **Sense** | Install the heartbeat (node cron job) so GravityClaw messages you every day; standardize the message (“Have you logged your steps?”), host on Railway for 24/7 uptime, and read logs from the Railway dashboard. | `heartbeat.ts`, Railway deployment, Telegram, node-cron. | lines 896‑1120 |

Use these bullet points to keep each iteration aligned with the video. When adding new integrations (for example, a new voice provider or a CRM), slot them beneath the appropriate step.
