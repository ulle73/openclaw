# Coastworks Command Center — V1 Spec (ROI-first)

## TL;DR
Bygg en **CEO-vy** som varje dag prioriterar rätt arbete: 
1) rankade projekt efter affärsvärde, 
2) blockerande beslut, 
3) tydlig "Next Best Action", 
4) experiment-pipeline som visar var execution fastnar.

---

## 1) Mål (för Jonas)

- Öka fart från idé → test → intäkt
- Minska brus och kontextbyten
- Prioritera projekt med högst förväntad ROI
- Synliggöra blockerare tidigt
- Göra agent-output mätbart i affärsnytta

### North Star
**Antal validerade intäktsdrivande experiment per månad** + **tid till första signal**.

---

## 2) Scope V1

### In scope (måste in)
1. **CEO Dashboard (ny tab)**
2. **Project Scoreboard** (ROI × Speed × Confidence)
3. **Decision Queue** (blockerande beslut)
4. **Next Best Action** (dagens huvudsteg + 2 backups)
5. **Pipeline Funnel** (Idea → Validation → Build → Monetize)
6. **Execution Radar** (leveranser + impact-taggar)
7. **Morning Brief-kort** (08:00-fokus)

### Out of scope (V2)
- Full forecast i pengar med avancerad modellering
- Auto-pricing rekommendationer per projekt
- Integrerad extern lead/data ingestion
- Multi-user auth/roles

---

## 3) Informationsarkitektur (UI)

## Ny vänstermeny-knapp
- `CEO-vy`

## CEO-vy layout

### Rad 1: KPI-kort
- Aktiva projekt
- Projekt i "Go Now"
- Pågående experiment
- Öppna blockerare
- 30d vunna experiment / totalt

### Rad 2: Next Best Action + Morning Brief
- **Next Best Action** (1 huvudsteg)
- **Backup Step A/B**
- "Do NOT do today" (1–3 anti-brus punkter)

### Rad 3: Project Scoreboard (tabell)
Kolumner:
- Projekt
- Stage
- Potential (SEK/mån)
- Time to test (dagar)
- Confidence (0–100)
- Strategic fit (0–100)
- Score (0–100)
- Status (Go Now / Validate / Park)

### Rad 4: Decision Queue
Kolumner:
- Beslut
- Projekt
- Impact (L/M/H)
- Reversibility (High/Low)
- Deadline
- Rekommenderat val
- Aging (dagar öppet)

### Rad 5: Pipeline Funnel
- Counts per steg + konvertering mellan steg
- Highlight "läckage" (störst tapp)

### Rad 6: Execution Radar
- Senaste leveranser från agenter
- Impact-tag (Low/Medium/High)
- Reusability-tag (Can become template/skill: yes/no)
- Lead time (från task skapad till leverans)

---

## 4) Datamodell (V1)

Skapa `data/ceo_state.json`:

```json
{
  "projects": [
    {
      "id": "tournado-golf",
      "name": "TourNado Golf",
      "stage": "Validation",
      "potentialSekMonth": 120000,
      "timeToTestDays": 7,
      "confidence": 68,
      "strategicFit": 90,
      "owner": "boss",
      "updatedAt": "2026-03-10T06:00:00.000Z"
    }
  ],
  "decisions": [
    {
      "id": "dec_001",
      "projectId": "tournado-golf",
      "title": "Välj launch-offer (årsplan vs månadsplan)",
      "impact": "H",
      "reversibility": "Low",
      "deadline": "2026-03-15",
      "recommended": "Starta årsplan med early adopter bonus",
      "status": "open",
      "createdAt": "2026-03-10T06:00:00.000Z"
    }
  ],
  "experiments": [
    {
      "id": "exp_001",
      "projectId": "tournado-golf",
      "name": "Landing + waitlist test",
      "stage": "Validation",
      "status": "running",
      "startedAt": "2026-03-10T06:00:00.000Z",
      "endedAt": null,
      "result": "unknown"
    }
  ],
  "nextBestAction": {
    "primary": "Lansera 1-sides waitlist för TourNado med tydlig pricing hypothesis",
    "backup": [
      "Skicka 20 riktade outreach till svenska golfgrupper",
      "Sätt upp enkel KPI-tracking för CTR + signup-rate"
    ],
    "antiNoise": [
      "Starta inga nya sidoprojekt idag",
      "Undvik design-polish före första signal"
    ],
    "generatedAt": "2026-03-10T06:00:00.000Z"
  }
}
```

---

## 5) Scoringmodell (Project Score)

`score = 0.40*ROI + 0.25*Speed + 0.20*Confidence + 0.15*StrategicFit`

### Normalisering
- `ROI` från `potentialSekMonth` (min-max inom aktiv portfölj)
- `Speed` från `timeToTestDays` där lägre dagar = högre score
- `Confidence` direkt 0–100
- `StrategicFit` direkt 0–100

### Statusregler
- `Go Now` om score >= 75
- `Validate` om 50–74
- `Park` om < 50

---

## 6) API-endpoints (server.mjs)

## Read
- `GET /api/ceo/overview`  
  Returnerar KPI-kort, funnel, nextBestAction, top blockers

- `GET /api/ceo/projects`  
  Returnerar projekt med beräknad score + status

- `GET /api/ceo/decisions`  
  Returnerar öppna beslut sorterat på impact + aging

- `GET /api/ceo/experiments`  
  Returnerar experiment + 30d win/loss-rate

- `GET /api/ceo/radar`  
  Returnerar task-leveranser från `tasks.json` med lead time + impact-tag

## Write
- `POST /api/ceo/project`
- `POST /api/ceo/project/:id`
- `POST /api/ceo/decision`
- `POST /api/ceo/decision/:id/close`
- `POST /api/ceo/next-action`

---

## 7) UI-komponenter (public/app.js)

Implementera funktioner:
- `renderCEO()`
- `renderProjectScoreboard()`
- `renderDecisionQueue()`
- `renderPipelineFunnel()`
- `renderExecutionRadar()`

Uppdatera navigation:
- Lägg till `button[data-tab="ceo"]`
- Lägg till `<section id="ceo" class="panel"></section>`

---

## 8) Datakällor & derivat

Primärt:
- `data/ceo_state.json` (ny)
- `data/tasks.json` (befintlig)
- `data/state.json` (befintlig)

Deriverat:
- Lead time från task timestamps
- Funnel counts från `projects[].stage` + `experiments[]`
- Execution radar impact kan initialt sättas manuellt per task (V1), senare auto-tagging

---

## 9) Sprintplan (2 sprintar)

## Sprint 1 (shipbar på 1 dag)
- Skapa `ceo_state.json`
- Lägg till read-endpoints
- Lägg till CEO-tab med:
  - KPI-kort
  - Next Best Action
  - Project Scoreboard
  - Decision Queue

**Definition of done Sprint 1**
- CEO-tab synlig
- Minst 3 projekt visas med score/status
- Minst 2 beslut visas med aging
- Ingen regression i befintliga tabs

## Sprint 2 (0.5–1 dag)
- Funnel visual
- Execution Radar
- Write-endpoints för projekt/beslut/next action
- Enkel inline-edit i UI

**Definition of done Sprint 2**
- Funnel visar conversion mellan steg
- Radar visar senaste leveranser + lead time
- Man kan uppdatera beslut/projekt utan filmanuell edit

---

## 10) Acceptance Criteria (affärsorienterade)

1. Det ska gå att se **exakt vad Jonas bör göra först idag** inom 10 sekunder.
2. Minst ett tydligt blockerande beslut ska synas när sådant finns.
3. Projekt ska auto-rankas utan manuell sortering.
4. Dashboarden ska göra det lätt att säga "nej" till låg-ROI arbete.
5. Samma vy ska ge underlag för morgonbrief och daglig prioritering.

---

## 11) Rekommenderad byggordning för Codey

1) Datafil + scoring helpers  
2) `/api/ceo/projects` + `/api/ceo/overview`  
3) CEO-tab skeleton i UI  
4) Scoreboard + Next Action kort  
5) Decision Queue  
6) Funnel + Radar  
7) Write-endpoints + inline edit

---

## 12) Första seed-data (för snabb start)

Seed direkt med 5 projekt:
- TourNado Golf
- UlleBets
- HantverkarOfferter
- AI Visibility Audit
- VilkenAI.se

Det räcker för att få omedelbar signal om prioritering och flaskhals.
