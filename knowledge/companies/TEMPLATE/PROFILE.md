---
companyId: TEMPLATE
timezone: Europe/Stockholm               # ÄNDRA
delivery:
  primary: telegram_dm
  telegram_chat_id: "<TELEGRAM_CHAT_ID>" # ÄNDRA
  secondary:
    enabled: true
    description: "Kan posta till vald grupp/topic om chat_id/topic_id anges."
proactivity:
  immediate_alerts: true
  daily_digest_time_local: "08:00"
quality:
  prioritize: ["roi", "speed_to_test", "automation_degree", "swedish_market_fit_or_clear_niche"]
  prefer_few_strong_over_many_weak: true
---

# Company Profile — TEMPLATE
## Proaktivt betyder
- Föreslå nästa steg utan att användaren ber om det.
- Identifiera återkommande mönster som borde bli: mall, automation, skill, app, agent, kunskapsbank.
- Lyft bara sådant som ger tydlig hävstång: pengar, fart, bättre system, bättre beslut, bättre återanvändbarhet.

## Standard output per relevant video
När en ny video bedöms relevant:
1) Kort notis direkt om den verkar viktig (om immediate_alerts=true).
2) Full ingest till knowledge base.
3) Deep research om den innehåller:
   - nytt verktyg / MCP / agentflöde / API / workflow / SEO-vinkel / distributionsupplägg /
     appidé / produktmöjlighet / automation som ger affärsnytta.
4) Extrahera:
   - konkreta steg
   - prompts
   - strukturer
   - verktyg
   - implementationstankar
   - affärsidéer
   - hur det kan användas i användarens projekt

## “Viktigt”-triage (för alert + deep research)
Varje ny video får:
- categories: [tool, workflow, business_idea, seo_distribution, agent_flow, automation, app_idea, product_opportunity, mcp, api]
- roi_score: 0–10
- effort_score: 0–10 (lägre = enklare)
- speed_to_test_score: 0–10
- swedish_market_fit_score: 0–10 (eller “clear niche fit”)
- decision:
  - send_immediate_alert: true/false
  - run_deep_research: true/false

Regel:
- Skicka alert om roi_score >= 8 eller om något är “uppenbart edge”.
- Kör deep research om run_deep_research=true (baserat på categories + score).

## Output-format (alert)
Max 10 rader:
- Vad det är
- Varför ROI
- 1–3 nästa steg
- Länk till sparad summary/path
