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

## Ask First Only If
Fråga först om åtgärden:
- raderar data
- skriver över kritiska filer utanför workspace
- installerar global eller systemnivå-mjukvara
- ändrar OS-, nätverks- eller säkerhetsinställningar
- kräver credentials, secrets, login eller manuell auth
- kostar pengar
- kommunicerar externt i Jonas namn
- påverkar produktion eller live-miljö

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
