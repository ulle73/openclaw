# YouTube Knowledge Bank Schemas

Detta dokument definierar JSONL-formaten för index/queue/failures så ingestion + cron + synthesis kan vara 100% deterministiska.

## Conventions
- JSONL = en JSON per rad.
- Alla timestamps = ISO 8601 UTC (t.ex. 2026-03-08T23:34:00Z).
- Paths är workspace-relativa.

---

## 1) INDEX — `knowledge/youtube/INDEX.jsonl`
En rad per ingested video (append-only; ny ingest av samma videoId kan lägga en ny rad eller uppdatera “latest” via dedupe-jobb).

Minimifält:
```json
{
  "videoId": "YnzsnqsrqXs",
  "sourceUrl": "https://www.youtube.com/watch?v=YnzsnqsrqXs",
  "title": "…",
  "channel": "https://www.youtube.com/@thekoerneroffice/videos",
  "published": "2026-03-08",
  "discoveredAt": "2026-03-08T20:10:00Z",
  "ingestedAt": "2026-03-08T20:25:00Z",
  "categories": ["workflow", "tool"],
  "entity_tags": ["notebooklm", "nano-banana-2"],
  "topic_tags": ["notebooklm", "nano-banana-2", "ai-video-generation"],
  "topic_cluster_key": "nano-banana-2__notebooklm",
  "related_video_ids": ["abc123xyz99"],
  "roi_label": "high",
  "relevance_label": "high",
  "paths": {
    "baseDir": "knowledge/youtube/YnzsnqsrqXs",
    "summary": "knowledge/youtube/YnzsnqsrqXs/summary.md",
    "chunks": "knowledge/youtube/YnzsnqsrqXs/chunks.md",
    "transcript": "knowledge/youtube/YnzsnqsrqXs/transcript.md"
  }
}
```

Valfria falt for amnesgruppering:
- `entity_tags`: normaliserade verktygs- och produktnamn.
- `topic_tags`: bredare amnestaggar for sokning, klustring och dedupe.
- `topic_cluster_key`: stabil nyckel for narliggande videos.
- `related_video_ids`: andra videos som overlappar tydligt i samma amne.

---

## 2) QUEUE — `knowledge/youtube/QUEUE.jsonl`
En rad per “work item” (video som ska processas). Ingest-worker plockar nästa item(s).
```json
{
  "videoId": "YnzsnqsrqXs",
  "sourceUrl": "https://www.youtube.com/watch?v=YnzsnqsrqXs",
  "channel": "https://www.youtube.com/@thekoerneroffice/videos",
  "discoveredAt": "2026-03-08T20:10:00Z",
  "priority": 80,
  "reason": "New upload detected",
  "attempts": 0,
  "status": "queued"
}
```
Regler:
- Vid start av processing: sätt status=processing (om du implementerar dedupe/locking).
- Vid success: status=done och/eller ta bort item via kompaktering/dedupe.
- Vid failure: status=retry och bump attempts.

---

## 3) FAILURES — `knowledge/youtube/FAILURES.jsonl`
En rad per failure (append-only). Används för debug + backoff.
```json
{
  "videoId": "YnzsnqsrqXs",
  "stage": "subtitles|download|parse|chunk|summary|deliver",
  "error": "HTTP Error 429: Too Many Requests",
  "at": "2026-03-08T20:12:00Z",
  "attempt": 1,
  "backoffUntil": "2026-03-08T22:12:00Z",
  "source": "yt-dlp"
}
```

---

## 4) Digest state — `knowledge/system/digest_state.json`
```json
{
  "lastDigestAt": "2026-03-08T08:00:00Z",
  "timezone": "Europe/Stockholm"
}
```

---

## 5) TOPICS â€” `knowledge/youtube/TOPICS.json`
Samlad registry for amneskluster och tagg-till-video-kopplingar.

```json
{
  "updatedAt": "2026-03-09T10:00:00Z",
  "clusters": {
    "nano-banana-2__notebooklm": {
      "entity_tags": ["nano-banana-2", "notebooklm"],
      "topic_tags": ["nano-banana-2", "notebooklm", "ai-video-generation"],
      "videoIds": ["obIeqXJH3d4", "abc123xyz99"],
      "videos": [
        {
          "videoId": "obIeqXJH3d4",
          "title": "Nano Banana 2 + NotebookLM ...",
          "channel": "Julian Goldie SEO",
          "summary": "knowledge/youtube/obIeqXJH3d4/summary.md"
        }
      ],
      "count": 2
    }
  },
  "tags": {
    "notebooklm": {
      "videoIds": ["abc123xyz99", "obIeqXJH3d4"],
      "clusters": ["nano-banana-2__notebooklm"],
      "count": 2
    }
  }
}
```
