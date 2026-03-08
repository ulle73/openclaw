---
name: youtube-skill
description: Integrerar YouTube-checker-hooken och visar hur transkript sparas.
metadata:
  openclaw:
    emoji: "📺"
---

# YouTube skill (placeholder)

Det här är en minimal placeholder-skill som gör att OpenClaw kan dokumentera Youtube-flödet utan att crasha när commands refererar till `youtube-skill`. Den beskriver hur `/ytb-library`-hooken fungerar.

## Trigger
Hooken triggas genom att köra kommandot `/ytb-library`

## Syfte
- Lagrar en kanallista i `~/.openclaw/hooks/ytb-library/channels.txt`
- Hämtar senaste videon per kanal via `yt-dlp`
- Sparar råa `.vtt`-transcript under `knowledge/ytb-library/<videoId>/transcript_raw.vtt`
- Loggar state i `~/.openclaw/hooks/ytb-library/state.json`
- Ger användaren status och eventuella fel direkt i chatten

Den egentliga logiken ligger i `hooks/ytb-library/ytb_library.py` och det är den filen som körs via hooken.
