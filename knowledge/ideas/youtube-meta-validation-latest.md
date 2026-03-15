# YouTube Meta Validation – 2026-03-15T19:20Z

## Högsignalidéer

### 1. Claude Skills 2.0 Content & Distribution Lab (GO)
- **Vad som upptäcktes:** Julian Goldie SEO släppte två nya Claude-klipp ("NEW Claude Skills 2.0 Is INSANE!" och "New FREE Claude Update: 2X Extra for 2 Weeks!") som visar hur Skills 2.0 plus "2 Weeks Extra"-träningen använder en skill.md-fil, färdiga script och templates för att bygga återanvändbara flows med marketing explainers, onboarding-träning och SEO-distribution.
- **Varför det spelar roll:** Det är första gången Claude officiellt pushar ett shareable "skill"-flöde och samtidigt visar en distribution/taktik (2 veckor extra) som är byggd för återanvändning över flera kanaler. Det passar direkt in i Coastworks content & automation stack eftersom vi redan paketerar agent-flöden + SEO-distribution och kan nu göra det som en Claude-specifik målsida/produkt.
- **Nästa åtgärder:**
  1. Bygg en Claude Skills 2.0-mall som tar ett befintligt Coastworks-fall (exempelvis AI Visibility Audit) och genererar en "2 Weeks Content Sprint" med prompts, templates, video-inspelningar och publikationsplan.
  2. Kör mallen på ett aktuellt case, dokumentera outputen i OpenClaw (skill.md, referensmaterial, automation scripts) och bedöm hur väl det funkar som produkt/paket för svenska SME-kunder.
  3. Formulera ett Coastworks-erbjudande som säljer Claude Skills 2.0 som "Content Automation Pilot" med tydlig scope, pris (ex. "10 korta explainer-klipp + 2 SEO-artiklar på 2 veckor") och outreach-meddelanden till svenska byråer/kundlistor.

## Validering
- `web_search` blockerades (missing Brave API key) så vi fick förlita oss på fångade data från YouTube-summeringar och web_fetch.
- `web_fetch https://r.jina.ai/https://www.youtube.com/watch?v=JwVJo5kMsUk` och `...watch?v=9rQm8AjcY8I` bekräftar att Julian Goldie SEO publicerade videorna som beskriver skill.md-mallar, "2 Weeks Extra"-kursen och att Claude 2.0-skills sätts ihop med automation/distribution.
- Försökte komma åt X-sökning (`https://x.com/search?q=Claude%20Skills%202.0`) men sidan kräver inloggning; ingen Reddit/X-signal kunde extraheras på grund av det.

## Poäng
| Idé | Unikhet | ROI | Hastighet | Sweden fit | Förtroende | Beslut |
| --- | --- | --- | --- | --- | --- | --- |
| Claude Skills 2.0 Content & Distribution Lab | 8 | 8 | 7 | 9 | 7 | GO |

## Proaktiv brief för Coastworks (på svenska)
1. **Vad vi såg:** Claude Skills 2.0 + "2 Weeks Extra"-uppdateringen introducerar en skill.md-mall + script som gör att samma workflow kan producera onboarding-videor, marketing explainers och SEO-material från ett och samma case.
2. **Varför det spelar roll:** Det gör det enkelt att sälja Claude som ett repeterbart content-automation-erbjudande till svenska SME-kunder: vi kan outsourca hela produktionen till ett Claude-skill, återanvända samma prompts för olika vertikaler och automatisera distributionen via Coastworks befintliga pipelines.
3. **Exakt nästa handling:** Skapa en "Claude Skills 2 Weeks Content Sprint" i OpenClaw, testa den på ett pågående Coastworks-projekt och paketera resultatet som ett pilot-erbjudande med outreach till två svenska kundlistor (exempelvis content-byråer eller marknadschefer som behöver snabb SEO-video- och onboarding-content).
