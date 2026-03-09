---
source: youtube
channels:
  - "<CHANNEL_URL_1>/videos"
  - "<CHANNEL_URL_2>/videos"
classification:
  mode: dynamic
rate_limits:
  max_videos_per_run: 1
  backoff_on_429_minutes: 120
storage:
  root: "knowledge/youtube"
  index: "knowledge/youtube/INDEX.jsonl"
  ideas_root: "knowledge/ideas"
  topics_root: "knowledge/topics"
  project_inventory: "knowledge/system/project_inventory.json"
  project_index: "knowledge/projects/PROJECT_INDEX.md"
synthesis:
  daily_digest_mode: "since_last_digest"
  max_research_candidates_per_run: 2
---
# YouTube Sources — TEMPLATE

## Princip
- Alla kanaler klassificeras dynamiskt per video (inte förbestämd kanal-roll).

## Ingest-regler (måste alltid funka)
För varje ny video:
- Hämta transcript (yt-dlp).
- Rensa reklam/sponsor-segment ur det som används för chunks/summary.
- Spara:
  - knowledge/youtube/<videoId>/transcript.md
  - knowledge/youtube/<videoId>/chunks.md
  - knowledge/youtube/<videoId>/summary.md
  - knowledge/youtube/<videoId>/excluded_ads.md (om något togs bort)
- Uppdatera global indexfil (append en rad per video).

## Routing per kategori (vad du ska uppdatera)
- tool → uppdatera knowledge/tools/REGISTRY.md
- workflow → uppdatera knowledge/flows/
- business_idea/app_idea/product_opportunity → skapa Idea Fit Report + deep research
- seo_distribution → skapa experiment/checklistor under knowledge/seo/
