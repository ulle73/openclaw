# YouTube Knowledge Bank

Detta är en lokal-first pipeline som omvandlar YouTube-klipp till sökbar kunskap.

## Struktur
```
knowledge/
  INDEX.md            # Översiktstabell över alla videor
  youtube/
    <video-id>/
      meta.json
      transcript.raw.txt
      transcript.clean.md
      learned.md
      skill_candidate.md
      classification.json
```

## Hur det fungerar
1. Kör `python scripts/youtube_to_knowledge.py <url>`.
2. Systemet hämtar metadata och transcript med `yt-dlp`.
3. Rå transcript sparas (`transcript.raw.txt`), en clean version (`transcript.clean.md`) skapas och analys körs (heuristisk eller via OpenAI).
4. `learned.md` genereras med sektioner för knowledge, actions, relevans och business-insikter.
5. `skill_candidate.md` innehåller bedömning om en video borde bli en skill + fråga “vill du bygga?”.
6. `knowledge/INDEX.md` uppdateras automatiskt med ny rad.
7. Summering och skill-fråga publiceras i chatten direkt efter körningen.
8. Kör `python scripts/knowledge_to_gravity.py` för att göra innehållet sökbart i GravityClaw.

## OpenClaw-integration
- Att koppla denna databank till OpenClaw betyder att `learned.md`-filerna kan läsas in via `gravity-claw` när du söker.
- När OpenAI/OpenRouter-nyckel saknas används nu en lokal heuristisk analys för att ändå skapa features/tools/workflows etc.
- Du kan bygga vidare genom att låta GravityClaw läsa `knowledge_corpus.json` och indexera varje entry i sitt minne vid start.
