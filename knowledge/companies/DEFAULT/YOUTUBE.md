---
source: youtube
channels:
  - https://www.youtube.com/@thekoerneroffice/videos
  - https://www.youtube.com/@JulianGoldieSEO/videos
  - https://www.youtube.com/@Itssssss_Jack/videos
  - https://www.youtube.com/@GregIsenberg/videos
  - https://www.youtube.com/@rileybrownai/videos
classification:
  mode: dynamic
rate_limits:
  max_videos_per_channel_per_run: 2
  queue_enabled: true
  backoff_on_429_min_hours: 2
  strategy_on_429:
    - "stop_subtitles_for_that_source"
    - "continue_other_sources_if_possible"
    - "retry_later_with_exponential_backoff"
storage:
  root: "knowledge/youtube"
  index: "knowledge/youtube/INDEX.jsonl"
  ideas_root: "knowledge/ideas"
  tools_registry: "knowledge/tools/REGISTRY.md"
  flows_root: "knowledge/flows"
---

# YouTube Sources — DEFAULT

## Princip
- Klassificera varje video dynamiskt utifrån innehållet (inte per kanal-roll).

## Must-have ingest (alltid)
För varje ny video:
- Hämta transcript (yt-dlp).
- Rensa reklam/sponsor-segment ur chunks + summary (spara borttaget i excluded_ads.md).
- Spara artefakter i knowledge/youtube/<videoId>/.
- Uppdatera INDEX.

## Deep research triggers
Kör deep research om videon innehåller något som kan ge affärsnytta, särskilt:
- nytt verktyg / MCP / agentflöde / API / workflow / SEO/distribution / automation / appidé / produktmöjlighet.
