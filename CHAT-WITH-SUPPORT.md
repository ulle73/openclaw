ryd
OP
 — Yesterday at 11:54 PM
jag formulerar om , jag vill att det ska struktureras på ett sådant sätt att vilket företag som helst ska kunna använda denna boten och göra den till sin personliga med sina personliga mål.

Så tex, låt säga att jag har 3 bolag, ett fitness bolag, ett tech bolag och ett naturbolag.

Då alla bolagen kommer följa olika inspo youtube kanaler osv, då ska man ekelt kunna byta det. Man ska enkelt kunna byta mål osv.

Men det stora hela, bygga kunskapsbanken osv ska vara exakt likadant, den ska ta videos från youtube och bryta ner och spara på ett effektivt sätt så man kan ha det som kunskapsbank. Boten ska alltid lära sig själv och komma upp med egna proaktiva ideer, använda en loop och när den får en ide göra deep research och komma med ännu effektivare tankar. Vad behöver du för att bygga dessa template filer? Men tänk på att youtube delen alltid är ett måste att den funkar ihop med kujnskapsbanken
Krill 🦐:lobster:
APP
 — Yesterday at 11:56 PM
Jag fattar – du vill inte “bygga ryds bot”, du vill bygga en återanvändbar produkt‑mall:

Core‑engine (YouTube → transcript → rensa reklam → chunks → summary → index → knowledge bank) = alltid samma
Company profile (mål, marknad, kanaler, output‑format, delivery targets) = lätt att byta per bolag
Proaktiv loop (cron/heartbeat) = samma motor, men kör mot vald profil och gör deep research när det finns en idé

Det här är 100% görbart – och OpenClaw har redan en superbra primitiv för just detta: multi‑agent.

Rekommenderad design (enkel + robust): 1 agent per bolag
För fitness/tech/natur gör du tre agenter:
fitness
tech
nature

Varje agent får:
samma gemensamma skills (ligger delat i ~/.openclaw/skills)
samma gemensamma hooks (delat i ~/.openclaw/hooks om du vill)
men egen workspace/knowledge/memory → ingen data blandas, allt blir rent och “switch” = byt agent/binding.

Det är mycket enklare än “en agent med tre profiler” (som kräver mer custom routing/state).

Docs: https://docs.openclaw.ai/concepts/multi-agent.md

---

Hur templaten ser ut (filstruktur)
Delat (samma för alla bolag)
~/.openclaw/skills/youtube-skill/… (din ingestion-skill)
ev. ~/.openclaw/hooks/ytb-checker/… (kolla senaste videos)

Per bolag (i respektive workspace)
knowledge/business/CONTEXT.md (bolagets mål/marknad)
knowledge/youtube/CHANNELS.json (kanaler + roll: idea/tool/workflow)
knowledge/youtube/INDEX.jsonl (autogenererat)
knowledge/youtube/<videoId>/… (autogenererat)
knowledge/tools/REGISTRY.md (autogenererat)
knowledge/flows/… (autogenererat)
HEARTBEAT.md (liten checklista) eller cron‑jobs (rekommenderat)

---

Vad jag behöver av dig för att skriva “template-filerna”
Vi kan börja med en bolagsprofil (t.ex. “tech bolaget”), och när den är bra kopierar vi till de andra.

1) Vill du köra “1 agent per bolag” (rekommenderat) eller “1 agent med flera profiler”?
Svar: A eller B

2) Globalt (gäller alla bolag)
Språk på output: svenska / engelska?
Hur ofta ska den vara proaktiv? (t.ex. var 3:e timme / dagligen)
Rate limit policy för yt-dlp: max X videos per run + backoff vid 429 (förslag: 1 video/run, backoff 2h)
3) Per bolag (för varje profil)
För varje bolag behöver jag:
companyId: (fitness / tech / nature)
1 mening: vad bolaget gör
marknad/geografi
1–3 mål (leads/SEO/automation/revenue)
Telegram target (DM/grupp + chat id)
lista på YouTube-kanaler (URL) + roll per kanal: idea | tool | workflow

---

Viktigt om “bote ska alltid lära sig själv”
Det bästa sättet är att göra det som en kontrollerad loop:
Cron job “synthesis”: läser senaste summaries → föreslår idéer → gör deep research på topp 1–2 → sparar i knowledge/ideas/… → skickar kort rapport.
Den får gärna “komma på egna idéer”, men bara på schema och med tydliga outputkrav.

---
Om du svarar bara detta nu så kan jag börja skriva templaten direkt:
1) A eller B (multi-agent eller multi-profile)?
2) Vilket bolag vill du börja med (fitness/tech/nature)?
3) Kanallistan (URL + roll) för det bolaget?
4) Telegram target (DM/grupp + chat id) för det bolaget?
ryd
OP
 — 12:19 AM
vi börjar med det jag skulle svara på förut, men försök strukturera .md filerna på ett sådant sätt att det är enkelt att kopiera och byta infon för andra typer av bolag.

A) Vad ska “proaktivt” betyda för dig?

1) Hur ofta vill du ha förslag?
Löpande när något viktigt upptäcks.
Daglig sammanfattning varje morgon kl 08:00.
Omedelbar notis när något har hög affärsnytta, tydlig ROI eller borde bli en egen skill, automation, app eller produkt.

2) Var ska den leverera?
Primärt: Telegram DM till mig.
Sekundärt: kunna posta till vald grupp/topic om jag senare anger chat_id/topic_id.
Chat ID: <FYLL I MITT TELEGRAM CHAT ID HÄR>

Definition av “proaktivt”:
Föreslå nästa steg utan att jag ber om det.
Identifiera återkommande mönster som borde bli mall, automation, skill, app, agent eller kunskapsbank.
Lyft bara sådant som ger tydlig hävstång: pengar, fart, bättre system, bättre beslut eller bättre återanvändbarhet.
Prioritera kvalitet över kvantitet. Hellre få, skarpa förslag än många svaga.

B) Kanaler som ska följas

Kanaler:
https://www.youtube.com/@thekoerneroffice/videos
https://www.youtube.com/@JulianGoldieSEO/videos
https://www.youtube.com/@Itssssss_Jack/videos
https://www.youtube.com/@GregIsenberg/videos
https://www.youtube.com/@rileybrownai/videos

Hur dessa ska hanteras:
Behandla alla kanaler dynamiskt utifrån innehållet i varje enskild video, inte utifrån en förbestämd kanal-roll.
För varje ny video ska du själv avgöra om den främst innehåller:
verktyg
workflow
affärsidéer
SEO/distribution
agentflöden
automation
appidéer
produktmöjligheter
Samma kanal kan ge olika typer av output beroende på videon.
Standard output per relevant video:
Kort notis direkt om videon verkar viktig.
Full ingest till knowledge base.
Deep research om videon innehåller nytt verktyg, MCP, agentflöde, API, workflow, SEO-vinkel, distributionsupplägg, appidé eller något som kan ge mig affärsnytta.
Extrahera konkreta steg, prompts, strukturer, verktyg, implementationstankar, affärsidéer och hur detta kan användas i mina egna projekt.
Rangordna det viktigaste efter ROI, snabbhet att testa, automationsgrad och passform för svensk marknad eller tydlig nisch.

C) Min business

1) Nisch/erbjudande:
Jag bygger AI-drivna digitala produkter, appar, automationer, agentflöden och micro-SaaS-lösningar med fokus på verklig affärsnytta och snabb väg till intäkter.

2) Marknad/geografi:
Primärt Sverige.
Särskilt svenska SME-bolag och tydliga nischer där AI, automation, appar och bättre system kan skapa konkurrensfördel.
Sekundärt globalt om något är enkelt att paketera och sälja digitalt.

3) Mål:
Hitta nya lönsamma idéer tidigt.
Bygga snabbare.
Automatisera mer.
Skapa återanvändbara system, skills, appar och kunskapsbanker.
Få bättre beslutsunderlag för vilka projekt jag ska satsa på.
Generera leads, produkter, SEO-vinklar, tjänstepaket, appar och återkommande intäkter.

D) Operativa constraints
1) Ska den få köra exec fritt?
Ja, absolut.
Standardläget är att den kör själv utan att fråga.
Den ska kunna köra kommandon, scripts, parsing, transkribering, indexering, builds, tester, dev servers, appstarter, browseröppning för lokal testning, filskapande, filuppdateringar och knowledge base-uppdateringar utan att fråga först.
Den ska aldrig utgå från API-nycklar som standard.
Den ska alltid utgå från att jag kör OAuth där autentisering behövs.
Den ska aldrig bygga lösningar som kräver att jag manuellt skapar, klistrar in eller underhåller API-nycklar om det finns en OAuth-baserad väg.
Den ska bara fråga först om åtgärden:
raderar data
skriver över kritiska filer utanför workspace
installerar global eller systemnivå-mjukvara
ändrar OS-, nätverks- eller säkerhetsinställningar
kräver credentials, secrets, login eller manuell auth
kostar pengar
kommunicerar externt i mitt namn
påverkar produktion eller live-miljö

2) Får den skriva över filer automatiskt i knowledge/?
Ja.
Den ska uppdatera, deduplicera och förbättra knowledge/ automatiskt.
Viktigt: behåll versionsspårning eller backup när större omstruktureringar görs.
Nyare, bättre och mer strukturerad sanning ska få ersätta äldre brus.

3) Hur ska vi hantera yt-dlp 429?
Kör kö / backoff automatiskt.
Standard:
max 1–2 videor per kanal per körning
exponential backoff vid 429
vänta minst 2 timmar efter 429 innan nytt försök
prioritera senaste och mest relevanta video först
hoppa över till nästa källa om en källa rate-limitar
Misslyckas hämtning ska jobbet inte dö; det ska återförsökas senare.

.
E) Språk/format

1) Ska allt output vara på svenska?
Ja, primärt svenska.
Verktygsnamn, API-namn, kommandon, kod, filnamn och tekniska begrepp kan vara på engelska där det är naturligt.

2) Vill du ha formatet “TL;DR + 3 takeaways + Next actions (max 3)” som standard?
Ja, men utöka standardformatet till detta:

Standard outputformat:
TL;DR
3 viktigaste takeaways
Hur detta kan användas för mig
Next actions (max 3)
Bör detta bli:
egen skill
ny automation
ny idé i idébanken
förbättring av befintligt system
ny app
ny produkt
ROI / potential:
låg / medel / hög
Relevans för mig:
låg / medel / hög

Övriga preferenser:
Var konkret.
Fokusera på verklig användning, inte bara sammanfattning.
Extrahera verktyg, workflows, implementation, affärsnytta och exakt varför det spelar roll för mig.
Om något återkommer flera gånger ska det systematiseras
Krill 🦐:lobster:
APP
 — 12:22 AM
Perfekt – och bra att du tänker “template först”. Det gör att samma bot/engine kan återanvändas för fitness/tech/natur (eller 100 andra) genom att du bara byter profilfilerna.

Nedan är ett upplägg jag rekommenderar: en “Company Profile Pack” du kan kopiera per bolag/agent. Ingestion‑motorn (youtube-skill, index, chunking, ad‑filter, etc) är oförändrad.

---

Föreslagen struktur (copy/paste‑vänlig)
Lägg allt som är bolagsspecifikt här:

knowledge/
  companies/
    DEFAULT/
      PROFILE.md
      YOUTUBE.md
      CONTEXT.md
När du skapar ett nytt bolag kopierar du DEFAULT/ → FITNESS/ (eller TECH/, NATURE/) och ändrar bara de tydligt markerade fälten.

---

1) knowledge/companies/DEFAULT/PROFILE.md (din A-del + proaktiv definition)
Kopiera detta:

---
companyId: DEFAULT
timezone: Europe/Stockholm   # ÄNDRA VID BEHOV
delivery:
  primary: telegram_dm
  telegram_chat_id: "<FYLL I MITT TELEGRAM CHAT ID HÄR>"
  secondary:
    enabled: true
    description: "Kan senare posta till vald grupp/topic om jag anger chat_id/topic_id."
proactivity:
  daily_digest_time_local: "08:00"
  immediate_alerts: true
---

# Company Profile — DEFAULT

## Proaktivt betyder
- Föreslå nästa steg utan att jag ber om det.
- Identifiera återkommande mönster som borde bli:
  - mall
  - automation
  - skill
  - app
  - agent
  - kunskapsbank
- Lyft bara sådant som ger tydlig hävstång:
  - pengar
  - fart
  - bättre system
  - bättre beslut
  - bättre återanvändbarhet
- Prioritera kvalitet över kvantitet: hellre få, skarpa förslag än många svaga.

## Notifieringsregler
### Omedelbar notis (”hög affärsnytta”)
Skicka direkt när något av detta gäller:
- Tydlig ROI / tydligt “det här borde vi göra”
- Borde bli en egen skill/automation/app/produkt
- Låg effort + hög impact
- Något som ger mig varaktig edge

Format (kort):
- 1 rad: Vad det är
- 1 rad: Varför det är hög ROI
- 1–3 bullets: nästa steg (max 3)

### Daglig sammanfattning 08:00
Varje morgon:
- “Vad kom in senaste 24h?”
- Top 3 insikter
- Top 3 förslag (med impact/effort)
- Vad som är queued för deep research
---

2) knowledge/companies/DEFAULT/YOUTUBE.md (din B-del + dynamisk klassificering)
---
source: youtube
channels:
  - https://www.youtube.com/@thekoerneroffice/videos
  - https://www.youtube.com/@JulianGoldieSEO/videos
  - https://www.youtube.com/@Itssssss_Jack/videos
  - https://www.youtube.com/@GregIsenberg/videos
  - https://www.youtube.com/@rileybrownai/videos
classification:
  mode: dynamic   # dvs inte låst per kanal
---
# YouTube Sources — DEFAULT

## Princip
- Behandla alla kanaler dynamiskt utifrån innehållet i varje enskild video (inte förbestämd kanal-roll).
- För varje ny video ska du avgöra om den främst innehåller (en eller flera):
  - verktyg
  - workflow
  - affärsidéer
  - SEO/distribution
  - agentflöden
  - automation
  - appidéer
  - produktmöjligheter

## Vad du ska göra per typ (routing)
- tool:
  - uppdatera knowledge/tools/REGISTRY.md
- workflow:
  - uppdatera knowledge/flows/ (flow library)
- business_idea / product_opportunity / app_idea:
  - skapa en “Idea Fit Report” + deep research + konkurrent/alternativ-scan
- seo_distribution:
  - skapa konkreta experiment + checklistor (och spara i knowledge/seo/)

## Output-krav
- Spara alltid transcript/chunks/summary under knowledge/youtube/<videoId>/
- Reklam/sponsor-segment ska INTE in i chunks eller summary
- Om något har hög ROI enligt PROFILE.md → skicka omedelbar notis


---
3) Vad jag behöver av dig för att göra detta “klart” (små frågor)
1) Vilken timezone gäller för 08:00? (gissning: Europe/Stockholm – bekräfta)
2) Vill du att “daglig digest” ska summera senaste 24h eller sedan förra digest?
3) Vill du att deep research ska triggas automatiskt för alla videos som klassas som business_idea, eller bara när confidence är hög?

När du svarat på de tre kan jag skriva nästa del också: CONTEXT.md (bolagsspecifik) + en tydlig “engine prompt” till din cron som använder PROFILE/YOUTUBE/CONTEXT på exakt samma sätt oavsett bolag.
Grymt — nu har du gett tillräckligt för att jag ska kunna skriva riktiga, återanvändbara template-filer.

För att göra det kopierbart för “vilket bolag som helst” föreslår jag att du har:

knowledge/companies/TEMPLATE/… = helt generisk mall (copy → nytt bolag)
knowledge/companies/DEFAULT/… = din nuvarande profil (fylld)

Nedan är färdigt innehåll för TEMPLATE (du kan kopiera rakt av).

---

1) knowledge/companies/TEMPLATE/PROFILE.md
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


---
2) knowledge/companies/TEMPLATE/YOUTUBE.md
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


---

3) knowledge/companies/TEMPLATE/CONTEXT.md
---
companyId: TEMPLATE
market:
  primary: "<LAND/REGION>"
  secondary: "<EVT GLOBALT>"
---

# Business Context — TEMPLATE

## Nisch/erbjudande
- <1–2 meningar>

## Marknad/geografi
- Primärt: <…>
- Sekundärt: <…>
- Svensk marknads-fit: <ja/nej + vilka segment>
## Mål
- <…>

## “Passar mitt företag” betyder
En idé passar om den:
- går att testa snabbt
- går att automatisera
- går att paketera digitalt
- ger tydlig edge/ROI i vald marknad/nisch

## Constraints (fylls i)
- Tid per vecka:
- Budget:
- Team:
- Riskaptit:
- Vad vi INTE gör:


---

Nu: din DEFAULT-profil (fylld med det du skrev)
Du kan skapa knowledge/companies/DEFAULT/ genom att kopiera TEMPLATE och sedan byta:

knowledge/companies/DEFAULT/CONTEXT.md (din text, färdig att klistra in)
---
companyId: DEFAULT
market:
  primary: "Sverige (SME + nischer)"
  secondary: "Globalt om det är lätt att paketera digitalt"
---

# Business Context — DEFAULT

## Nisch/erbjudande
- Jag bygger AI-drivna digitala produkter, appar, automationer, agentflöden och micro-SaaS-lösningar med fokus på verklig affärsnytta och snabb väg till intäkter.

## Marknad/geografi
- Primärt Sverige.
- Särskilt svenska SME-bolag och tydliga nischer där AI, automation, appar och bättre system kan skapa konkurrensfördel.
- Sekundärt globalt om något är enkelt att paketera och sälja digitalt.

## Mål
- Hitta nya lönsamma idéer tidigt.
- Bygga snabbare.
- Automatisera mer.
- Skapa återanvändbara system, skills, appar och kunskapsbanker.
- Få bättre beslutsunderlag för vilka projekt jag ska satsa på.
- Generera leads, produkter, SEO-vinklar, tjänstepaket, appar och återkommande intäkter.


---

Sista biten jag behöver (D: Operativa constraints)
För att jag ska kunna skriva “final version” av DEFAULT/PROFILE.md + DEFAULT/YOUTUBE.md (med rätt throttle/backoff/alert‑trösklar), svara bara på:

1) Timezone för 08:00: Europe/Stockholm ok?
2) Max deep research per dag: 1 / 2 / 3 / obegränsat?
3) Vid 429: backoff 60 / 120 / 240 minuter?
4) Ska den alltid få skriva över filer i knowledge/youtube/<videoId>/ vid re-run (ja/nej)?
När du svarat de fyra ger jag dig också en färdig cron-prompt (check → ingest → deep research + daily 08:00 digest) som använder exakt de här filerna.
Perfekt — nu har vi D (constraints) för att göra “DEFAULT-profilen” komplett. Här är färdiga filer + färdiga cron‑prompter (copy/paste). Jag antar Europe/Stockholm för 08:00 – säg till om du vill ändra.

---

1) knowledge/companies/DEFAULT/PROFILE.md (FÄRDIG)
---
companyId: DEFAULT
timezone: Europe/Stockholm
delivery:
  primary: telegram_dm
  telegram_chat_id: "<FYLL I MITT TELEGRAM CHAT ID HÄR>"
  secondary:
    enabled: true
    description: "Kan senare posta till vald grupp/topic om chat_id/topic_id anges."
proactivity:
  immediate_alerts: true
  daily_digest_time_local: "08:00"
execution_policy:
  exec_default: "run_without_asking"
  never_assume_api_keys: true
  prefer_oauth_over_api_keys: true
  ask_first_if:
    - deletes_data
    - overwrites_critical_files_outside_workspace
    - installs_global_or_system_software
    - changes_os_network_or_security_settings
    - needs_credentials_secrets_login_or_manual_auth
    - costs_money
    - communicates_externally_in_my_name
    - affects_production_or_live_environment
knowledge_policy:
  knowledge_overwrite_ok: true
  keep_backups_on_major_restructure: true
quality:
  prioritize: ["roi", "speed_to_test", "automation_degree", "swedish_market_fit_or_clear_niche"]
  prefer_few_strong_over_many_weak: true
---

# Company Profile — DEFAULT

## Proaktivt betyder
- Föreslå nästa steg utan att jag ber om det.
- Identifiera återkommande mönster som borde bli: mall, automation, skill, app, agent, kunskapsbank.
- Lyft bara sådant som ger tydlig hävstång: pengar, fart, bättre system, bättre beslut, bättre återanvändbarhet.
- Prioritera kvalitet över kvantitet.
## Standard output per relevant video
- Kort notis direkt om videon verkar viktig.
- Full ingest till knowledge base.
- Deep research om videon innehåller nytt verktyg, MCP, agentflöde, API, workflow, SEO-vinkel, distributionsupplägg, appidé eller något som kan ge affärsnytta.
- Extrahera konkreta steg, prompts, strukturer, verktyg, implementationstankar, affärsidéer och hur detta kan användas i mina egna projekt.
- Rangordna efter ROI, snabbhet att testa, automationsgrad och passform för svensk marknad eller tydlig nisch.

## Triage & scoring (för alert + deep research)
För varje ny video, sätt:
- categories: [tool, workflow, business_idea, seo_distribution, agent_flow, automation, app_idea, product_opportunity, mcp, api]
- roi_score: 0–10
- effort_score: 0–10 (lägre är bättre)
- speed_to_test_score: 0–10
- automation_degree_score: 0–10
- swedish_market_fit_score: 0–10 (eller “clear niche fit”)

Regler:
- send_immediate_alert=true om roi_score >= 8 eller om den är “uppenbar edge”.
- run_deep_research=true om video matchar någon av: tool/mcp/agent_flow/api/workflow/seo_distribution/app_idea/product_opportunity
  men prioritera att faktiskt köra deep research på topp-kandidater först (quality > quantity).

## Alert-format (max 10 rader)
- Vad det är (1 rad)
- Varför ROI (1 rad)
- 1–3 nästa steg
- Länk + path till sparad summary


---
2) knowledge/companies/DEFAULT/YOUTUBE.md (FÄRDIG)
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


---
3) Cron-prompter (redo att använda som --message)
Cron A — “Scan → queue” (billigt, ofta)
Kör t.ex. varje 1–3 timmar.
Du kör en YouTube-scan (utan att ladda subtitles):
1) Läs:
   - knowledge/companies/DEFAULT/PROFILE.md
   - knowledge/companies/DEFAULT/YOUTUBE.md
2) För varje kanal i YOUTUBE.md:
   - lista senaste videorna (billigt/flat playlist)
   - jämför mot knowledge/youtube/INDEX.jsonl (vad är nytt?)
3) Lägg nya videoIds i en köfil: knowledge/youtube/QUEUE.jsonl
4) Skicka en kort notis endast om du ser något som sannolikt är high ROI (enligt PROFILE triage), annars NO_REPLY.


Cron B — “Ingest worker” (dyrt, throttlat)
Kör t.ex. varje 1–3 timmar (eller tätare), men processa lite.
Du är en ingestion-worker.
0) Läs PROFILE + YOUTUBE.
1) Ta nästa item(s) från knowledge/youtube/QUEUE.jsonl (max 1–2 videos per kanal per körning).
2) För varje video:
   - kör youtube-ingest (transcript → ad-filter → chunks → summary → index)
   - sätt triage-scores + categories
   - om high ROI: skicka omedelbar alert till Telegram (kort format + paths)
3) Om yt-dlp ger 429:
   - stoppa subtitles för den källan
   - logga status i knowledge/youtube/FAILURES.jsonl
   - backoff minst 2h (exponential)
   - låt jobbet fortsätta med andra källor om möjligt
4) Jobbet får inte dö på en failure — allt ska återförsökas senare.
Cron C — “Daily 08:00 digest + synthesis”
Daglig briefing 08:00 lokal tid.
1) Läs PROFILE + CONTEXT + INDEX.
2) Sammanfatta senaste 24h:
   - Top 3 insikter
   - Top 3 förslag (impact/effort/speed)
   - Vad som borde bli skill/automation/app
3) Välj 1–2 bästa idéer och gör deep research (web_search/web_fetch) med källor.
4) Spara till knowledge/ideas/YYYY-MM-DD-digest.md
5) Skicka en kort version till Telegram + länk/paths till filerna.


---

Två snabba “sista” inputs jag behöver från dig
1) Din Telegram DM chat id (siffror) så jag kan skriva in det utan placeholder.
2) Vill du att daily digest ska vara “senaste 24h” (som ovan) eller “sedan senaste digest” (state-baserat)?

När du svarat kan jag skriva en sista fil också: knowledge/youtube/SCHEMA.md (exakta JSONL-format för INDEX/QUEUE/FAILURES) så allt blir 100% konsekvent och lätt att återanvända för andra bolag.
Toppen — det där är ett riktigt bra standardformat (det gör synthesis mycket lättare).

Här är exakt hur jag skulle “bädda in” dina E‑preferenser i systemet:

---

1) Uppdatera knowledge/companies/DEFAULT/PROFILE.md
Lägg till (eller ersätt) en sektion i slutet av filen:

## Språk
- Primärt svenska.
- Verktygsnamn, API-namn, kommandon, kod, filnamn och tekniska termer får vara på engelska när det är naturligt.

## Standard outputformat (per relevant video)
All output ska följa detta:
1) TL;DR
2) 3 viktigaste takeaways
3) Hur detta kan användas för mig (kopplat till min business context)
4) Next actions (max 3, konkreta)
5) Bör detta bli:
   - egen skill
   - ny automation
   - ny idé i idébanken
   - förbättring av befintligt system
   - ny app
   - ny produkt
6) ROI / potential: låg / medel / hög
7) Relevans för mig: låg / medel / hög
## Systematisering
- Om något återkommer flera gånger: föreslå hur det ska systematiseras (mall/skill/automation/registry) och uppdatera kunskapsbanken därefter.


---

2) Gör summary.md maskinläsbar (rekommenderat)
Skapa en gemensam template som din ingest alltid följer:

knowledge/templates/VIDEO_SUMMARY_TEMPLATE.md
---
videoId: "<id>"
sourceUrl: "<url>"
title: "<title>"
channel: "<channel>"
published: "<YYYY-MM-DD>"
categories: ["tool", "workflow", "business_idea", "seo_distribution", "agent_flow", "automation", "app_idea", "product_opportunity", "mcp", "api"]

roi_label: "low|medium|high"
relevance_label: "low|medium|high"

should:
  skill: false
  automation: false
  idea_bank: false
  system_improvement: false
  app: false
  product: false
---
# TL;DR
- ...

# 3 viktigaste takeaways
1. ...
2. ...
3. ...

# Hur detta kan användas för mig
- ...

# Next actions (max 3)
1. ...
2. ...
3. ...

# Bör detta bli?
- Skill: <ja/nej + 1 rad varför>
- Automation: <ja/nej + 1 rad varför>
- Idébank: <ja/nej + 1 rad varför>
- Systemförbättring: <ja/nej + 1 rad varför>
- App: <ja/nej + 1 rad varför>
- Produkt: <ja/nej + 1 rad varför>

# ROI / potential
- <låg|medel|hög> — <1–2 meningar motivering>

# Relevans för mig
- <låg|medel|hög> — <1–2 meningar motivering>
Det här gör att din daily digest kan läsa frontmatter och snabbt ranka utan att “tolka” löptext.

---

3) Små justeringar i cron-prompterna
I “ingest worker” och “daily digest”: lägg till kravet:
“Skriv summary.md enligt VIDEO_SUMMARY_TEMPLATE.md (inkl YAML frontmatter).”

---

Två sista saker jag fortfarande behöver från dig
1) Telegram chat id (siffror) så jag kan ersätta placeholdern i PROFILE.md.
2) Daily digest: vill du ha “senaste 24h” (enklast) eller “sedan senaste digest” (mer exakt, kräver state-fil)?

När du svarat kan jag skriva färdigt en knowledge/youtube/SCHEMA.md (INDEX/QUEUE/FAILURES-format) så allt blir helt konsekvent.
ryd
OP
 — 12:34 AM
1, sätt placeholder så länge, skriv "---ERSÄTT MED TELEGRAM CHAT ID---"
2, sedan senaste digest
Krill 🦐:lobster:
APP
 — 12:35 AM
Perfekt. Då gör vi så här:

Telegram placeholder: ---ERSÄTT MED TELEGRAM CHAT ID---
Daily digest: sedan senaste digest (state-baserat)

Nedan är färdiga “copy/paste”-bitar du kan lägga in.

---

1) Uppdatera knowledge/companies/DEFAULT/PROFILE.md (placeholder)
Sätt:

telegram_chat_id: "---ERSÄTT MED TELEGRAM CHAT ID---"


---
2) Daily digest (sedan senaste digest): state-fil + prompt
Skapa en statefil:

knowledge/system/digest_state.json
{
  "lastDigestAt": null,
  "timezone": "Europe/Stockholm"
}


Och använd denna cron‑prompt för daily digest:

Daglig briefing 08:00 lokal tid (Europe/Stockholm), “sedan senaste digest”.
1) Läs:
   - knowledge/companies/DEFAULT/PROFILE.md
   - knowledge/companies/DEFAULT/CONTEXT.md
   - knowledge/youtube/INDEX.jsonl
   - knowledge/system/digest_state.json

2) Bestäm tidsfönster:
   - Om lastDigestAt finns: använd (lastDigestAt → nu).
   - Om lastDigestAt saknas: använd senaste 24h som första körning.

3) Välj videos i INDEX inom tidsfönstret och läs deras summary.md.
   - Rangordna enligt ROI/speed/automation + svensk marknadsfit/nisch.

4) Skapa digest:
   - Top 3 insikter
   - Top 3 förslag (impact/effort/speed)
   - 1–2 deep research (web_search/web_fetch) med källor
   - Spara: knowledge/ideas/YYYY-MM-DD-digest.md
   - Skicka kort version till Telegram (PROFILE standardformat).

5) Uppdatera digest state:
   - Sätt lastDigestAt = nu (ISO timestamp) i knowledge/system/digest_state.json


---

3) knowledge/youtube/SCHEMA.md (INDEX/QUEUE/FAILURES – standard för alla bolag)
Kopiera detta:

md
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
md
json
{
  "videoId": "YnzsnqsrqXs",
  "sourceUrl": "https://www.youtube.com/watch?v=YnzsnqsrqXs",
  "title": "…",
  "channel": "https://www.youtube.com/@thekoerneroffice/videos",
  "published": "2026-03-08",
  "discoveredAt": "2026-03-08T20:10:00Z",
  "ingestedAt": "2026-03-08T20:25:00Z",
  "categories": ["workflow", "tool"],
  "roi_label": "high",
  "relevance_label": "high",
  "paths": {
    "baseDir": "knowledge/youtube/YnzsnqsrqXs",
    "summary": "knowledge/youtube/YnzsnqsrqXs/summary.md",
"chunks": "knowledge/youtube/YnzsnqsrqXs/chunks.md",
    "transcript": "knowledge/youtube/YnzsnqsrqXs/transcript.md"
  }
}
---

## 2) QUEUE — `knowledge/youtube/QUEUE.jsonl`
En rad per “work item” (video som ska processas). Ingest-worker plockar nästa item(s).
json
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


---
```
## 4) Digest state — `knowledge/system/digest_state.json`
json
{
  "lastDigestAt": "2026-03-08T08:00:00Z",
  "timezone": "Europe/Stockholm"
}