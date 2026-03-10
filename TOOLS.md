# TOOLS

## Tool Philosophy
Verktyg ska användas för att:
- verifiera
- reducera osäkerhet
- spara tid
- skapa bättre output
- undvika att gissa när kontroll är möjlig

## Rule
Använd verktyg när de tydligt förbättrar resultatet.
Använd dem inte slentrianmässigt.

## Web And Browser
För research, installationsguider och dokumentation:
- använd `web_search` bara om det faktiskt är konfigurerat och fungerar; om det saknar Brave-nyckel ska det behandlas som otillgängligt
- använd `web_fetch` för raka docs- och textsidor
- använd `node scripts/browser_host.js ...` som enda browser-väg för renderade eller JS-tunga sidor
- använd inte OpenClaws inbyggda `browser` tool i normal drift
- för kända program eller officiella sajter: gå direkt mot officiell källa i stället för sökmotorresultat
- om Jonas uttryckligen säger att du ska gå ut på nätet får du inte nöja dig med lokal knowledge om onlinevägarna fortfarande fungerar

## Computer Use
För visual browser control enligt OpenAI computer-use-guiden:
- använd `python scripts/openai_computer_use_playwright.py --prompt "..."` som kanonisk väg
- den vägen kräver en OpenAI-credential som faktiskt har Responses API-scope
- OpenClaw `openai-codex` OAuth räcker inte ensam för direkt Python-SDK `responses.create(...)` om tokenen saknar `api.responses.write`
- använd den för riktiga visuella browseruppgifter i stället för att improvisera med sökmotor + trasig browser-tool

## Installation And System Changes
När Jonas uttryckligen ber om att installera ett program, CLI, paket eller lokal runtime:
- använd alltid den kanoniska installationsvägen via `powershell -ExecutionPolicy Bypass -File scripts/install_program.ps1 ...`
- använd `install-winget` först när ett stabilt winget-paket finns
- använd `install-url` mot officiell nedladdningslänk när winget inte räcker eller inte finns
- verifiera efteråt med versionskommando eller faktisk körning
- säg bara stopp om Windows/UAC eller saknade rättigheter faktiskt blockerar körningen
- fråga inte Jonas vilken installationsmetod som ska användas; välj den stabilaste själv

## Desktop And App Control
För lokala app- och desktop-uppgifter:
- använd `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/desktop_control.ps1 -RawMessage "..."` som kanonisk väg
- använd den vägen för att starta appar, öppna genvägar och göra enkla lokala UI-interaktioner
- säg inte att du saknar desktop-kapacitet om den lokala host-control-vägen finns

## Standard
Verifiera hellre än att anta.
Automatisera hellre än att upprepa.
Läs relevant information hellre än att gissa.

## Execution Default
Standardläget är att köra själv utan att fråga när arbetet sker i workspacen och inte bryter mot guardrails.

Det gäller t.ex.:
- kommandon
- scripts
- parsing
- transkribering
- indexering
- builds
- tester
- dev servers
- browseröppning för lokal testning
- filskapande
- filuppdateringar
- knowledge base-uppdateringar

## Multi-Agent Orchestration
Boss may orchestrate specialists directly.

Preferred routing:
- `radar` -> research, YouTube, synthesis, docs, signal analysis
- `codey` -> code changes, hooks, scripts, cron, verification
- `moneymaker` -> monetization, offer framing, prioritization, commercial packaging

When Jonas asks Boss to make a specialist reply in their own lane, prefer a real delegated run over a paraphrase.
Use local scripts and the `message` capability when that is the most deterministic path.
For lane delegation, the default path is the local script below, not a conversational refusal.
Deterministic delegation commands:
- `python scripts/delegate_agent_message.py --agent radar --message "..."`
- `python scripts/delegate_agent_message.py --agent codey --message "..."`
- `python scripts/delegate_agent_message.py --agent moneymaker --message "..."`

## Ask First Only If
Lokala host-control-uppgifter som Jonas uttryckligen ber om ar forhandsgodkanda.
Det inkluderar att starta appar, oppna genvagar, klicka i lokala GUI:n, ladda ner filer och kora installerare pa hans egen dator.
Fråga först om åtgärden:
- raderar data
- skriver över kritiska filer utanför workspace
- installerar global eller systemnivå-mjukvara utan att Jonas uttryckligen bett om det
- ändrar OS-, nätverks- eller säkerhetsinställningar
- kostar pengar
- kommunicerar externt i Jonas namn

## Auth Policy
- Utgå aldrig från API-nycklar som standard.
- Utgå alltid från OAuth där autentisering behövs.
- Bygg inte lösningar som kräver att Jonas manuellt skapar, klistrar in eller underhåller API-nycklar om det finns en OAuth-baserad väg.

## Knowledge Policy
- `knowledge/` får uppdateras, dedupliceras och förbättras automatiskt.
- Nyare, bättre och mer strukturerad sanning får ersätta äldre brus.
- Behåll versionsspårning eller backup när större omstruktureringar görs.

## YouTube / Knowledge Bank
Källan för bolagsstyrning är:
- `knowledge/companies/DEFAULT/PROFILE.md`
- `knowledge/companies/DEFAULT/YOUTUBE.md`
- `knowledge/companies/DEFAULT/CONTEXT.md`

Arbetssätt:
- behandla kanaler dynamiskt per video, inte via låsta kanalroller
- gör full ingest till knowledge base för relevanta videos
- trigga deep research för sådant som ger tydlig affärsnytta
- rangordna efter ROI, snabbhet att testa, automationsgrad och svensk marknadsfit eller tydlig nisch

## Rate Limit Policy
För YouTube-ingest gäller som standard:
- max 1–2 videor per kanal per körning
- exponential backoff vid 429
- vänta minst 2 timmar efter 429 innan nytt försök
- prioritera senaste och mest relevanta video först
- hoppa vidare till nästa källa om en källa rate-limitar
- jobbet får inte dö på en failure; det ska återförsökas senare
