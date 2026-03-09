# Knowledge System

Detta ar nu mer an en YouTube-bank. Det ar ett lokalt kunskapssystem som gor videoingest, topic-syntes, projektmatchning och idegenerering pa samma grunddata.

## Struktur
```text
knowledge/
  INDEX.md
  ideas/
    YYYY-MM-DD-digest.md
    YYYY-MM-DD-01-<topic>.md
  projects/
    PROJECT_INDEX.md
  system/
    digest_state.json
    project_inventory.json
  topics/
    <cluster-key>/
      overview.md
      decision.md
      opportunity.md
      signals.json
  youtube/
    INDEX.jsonl
    TOPICS.json
    <video-id>/
      meta.json
      transcript.raw.txt
      transcript_clean.txt
      transcript_clean.md
      transcript.md
      chunks.md
      summary.md
      learned.md
      skill_candidate.md
      excluded_ads.md
```

## Flode
1. En video kommer in via cron, manuell URL eller chat-hook.
2. `scripts/youtube_to_knowledge.py` gor alltid samma ingest: raw transcript, clean transcript, chunks, summary, tags, metadata och index.
3. Liknande videos grupperas i `knowledge/youtube/TOPICS.json`.
4. `scripts/project_inventory.py` bygger en aktuell projektbild fran `ACTIVE_PROJECTS.md` och dina repos.
5. `scripts/youtube_synthesis.py` skapar topic-kort, projektmatchning, ideer och ett dagligt digestlager i `knowledge/topics/` och `knowledge/ideas/`.

## Viktiga filer
- `knowledge/system/project_inventory.json`: maskinlasbar projektkatalog med roller, prioritet, stack och repo-paths.
- `knowledge/projects/PROJECT_INDEX.md`: lasbar oversikt over aktuella projekt som agenten ska rikta forslag mot.
- `knowledge/topics/<cluster>/decision.md`: kort beslutskort per amneskluster.
- `knowledge/ideas/YYYY-MM-DD-digest.md`: daglig syntes sedan senaste digest.

## Kommandon
- `python scripts/ingest_youtube_url.py "<url>"`: ingest av en video via samma wrapper som hooken anvander.
- `python scripts/youtube_channel_cron.py`: kanalscan enligt `knowledge/companies/DEFAULT/YOUTUBE.md`.
- `python scripts/project_inventory.py`: uppdatera projektinventering och projektindex.
- `python scripts/youtube_synthesis.py`: bygg topics, beslutskort, ideer och digest.
- `python scripts/run_youtube_synthesis.py`: samma synthesis med loggrad till `memory/youtube_synthesis_runs.md`.
