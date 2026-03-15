# PRD: Social Media Manager Template MVP

## Dokumentstatus
- Version: `0.2`
- Datum: `2026-03-10`
- Status: `Draft`
- Scope: `MVP`

## 1. Sammanfattning
Vi ska bygga en enkel, billig och automatiserad contentmotor for sociala medier med fokus pa `Instagram` i version 1. Systemet ska lasa in amnen eller ideer fran `Google Sheets`, generera textinnehall via `OpenAI API`, generera bild via Googles officiella `Gemini Image Generation API`, och lagra resultatet for manuell review innan export eller senare publicering.

Produkten ska samtidigt byggas som en `template` som kan ateranvandas och saljas till andra foretag. Ett nytt foretag ska kunna komma igang genom att:

- ange egna API-nycklar
- fylla i foretagsinformation i tydliga configfiler
- lagga in kunskap om foretaget i en separat kunskapsbank
- justera enkla installningar utan att behova ga in och leta i applikationskoden

Plattformsstod for `LinkedIn`, `Facebook`, `X` och `TikTok` ska forberedas som placeholders i datamodell och struktur, men endast `Instagram` ska vara aktivt i forsta versionen.

## 2. Produktteori
Detta ar inte bara ett internt verktyg. Det ar en `ateranvandbar white-label template` som ska kunna sattas upp for flera olika kunder med sa lite specialbygge som mojligt.

Karniden ar:

- en standardiserad contentmotor
- ett enkelt reviewflode
- en tydlig kundspecifik configyta
- en kunskapsbank som styr tonalitet, budskap, erbjudanden och bildsprak

Varje installation av systemet ska i MVP vara `en kund per deployment`. Multi-tenant ar inte ett mal i version 1.

## 3. Bakgrund
Malet ar att minska tiden fran content-ide till fardigt publiceringsbart inlagg. I stallet for att skriva varje post manuellt ska anvandaren kunna lagga in amnen i ett Google Sheet och lata systemet generera ett forsta utkast bestaende av:

- rubrik
- hook
- caption
- bildprompt
- genererad bild

Systemet ska inte ersatta mansklig kvalitetskontroll i MVP:n. Det ska istallet skapa ett snabbt produktionsflode dar AI gor forsta utkastet och anvandaren granskar innan innehallet godkanns.

For att outputen ska bli relevant for olika kunder maste systemet kunna lasa in foretagsspecifik kunskap. Den kunskapen ska inte hardkodas i promptar eller filer som kraver utvecklare att hitta ratt i kodbasen. Den ska ligga i tydliga, separata och kundredigerbara filer.

## 4. Problem Som Ska Losas
- Det tar for lang tid att ga fran ide till fardigt inlagg.
- Contentproduktion blir ofta inkonsekvent nar den goras manuellt.
- Det saknas ett enkelt och billigt arbetsflode for att batcha ideer, generera utkast och hantera review.
- Befintliga verktyg blir snabbt dyra eller for komplexa for ett forsta internt system.
- Kundanpassning blir dyr om varje ny implementation kraver kodandringar pa flera stallen.
- AI-genererad copy och bild blir for generisk om systemet inte har tillgang till foretagets egen kunskap, tonalitet och erbjudanden.

## 5. Mal
- Skapa ett fungerande MVP-flode for `Instagram`.
- Halla systemet sa nara gratis som mojligt i datalager och arbetsyta.
- Bygga repot som en tydlig och saljbar template.
- Skilja kundspecifik information fran applikationslogik.
- Skapa en enkel kunskapsbank som styr copy och bildgenerering.
- Gora review-steget tydligt sa att innehall kan godkannas, regenereras eller justeras.
- Forbereda struktur for fler plattformar utan att bygga dem annu.

## 6. Icke-Mal For MVP
- Automatisk publicering till sociala plattformar i version 1.
- Fullt multi-platform-stod i version 1.
- Multi-tenant SaaS med flera kunder i samma runtime.
- Avancerad kampanjplanering, kalenderfunktion eller analytics-dashboard.
- Samarbetsfunktioner for storre team.
- Komplext roll- och behorighetssystem.
- Automatisk semantisk sokning eller RAG-pipeline med embeddings som krav for v1.

## 7. Malgrupp
Primara malgrupper i MVP:

- en soloanvandare eller ett mycket litet team som vill producera Instagram-content snabbare
- en byra, freelancer eller operator som vill salja en fungerande content-template till andra foretag
- ett mindre foretag som vill kunna fylla i sin egen information utan att anpassa kodbasen manuellt

## 8. Produktvision
En lattanvand white-label contentmotor dar ett foretag matar in ideer i ett spreadsheet, tillfor egen kunskap i en tydlig kunskapsbank, och far tillbaka fardiga social media-utkast med text och bild som ar riktade till just deras varumarke.

## 9. Template-Forst Princip
Templatebarhet ar ett forstaklassigt produktkrav, inte bara en implementationdetalj.

MVP:n ska darfor byggas sa att:

- alla kundspecifika nycklar ligger i tydliga miljo- eller configfiler
- all kundspecifik affarsinfo ligger i separata kundfiler, inte utspridd i kodbasen
- det ska vara latt att se "detta ar saker kunden kan andra"
- inga kundspecifika hardkodningar ska behova goras i core-logiken for en vanlig onboarding
- projektet ska kunna dupliceras och sattas upp for en ny kund med begransade justeringar

## 10. Kundspecifik Anpassning
Systemet ska ha en tydlig och begransad yta for det som ar kundspecifikt.

Minimikrav:
- API-nycklar och tekniska IDs i `.env` eller motsvarande
- foretagsprofil i separat configfil
- plattformsinstallningar i separat configfil
- kunskapsbank i separat mapp med redigerbara filer
- tydlig dokumentation om vilka filer kunden eller operatorn ska redigera

Exempel pa kundspecifik information:
- foretagsnamn
- kort beskrivning av bolaget
- malgrupper
- produkter eller tjanster
- erbjudanden
- tonalitet
- no-go-ord eller claims
- visuella riktlinjer
- CTA-preferenser

## 11. Kunskapsbank
Systemet ska innehalla en enkel men tydlig `kunskapsbank` som anvands for att styra bade copy och bildgenerering mot kundens verklighet.

Kunskapsbanken ska i MVP vara `filbaserad`, eftersom det ar enklast att paketera, forsta, redigera och salja vidare i en template.

Kunskapsbanken ska kunna innehalla:
- foretagsbeskrivning
- malgrupper
- produkter eller tjanster
- erbjudanden
- USP och differentiering
- tonalitet och skrivregler
- vanliga fragor
- bevis, case eller kundresultat
- visuella riktlinjer
- exempel pa tidigare bra inlagg
- saker man inte far saga eller lova

Kunskapsbanken ska kunna fyllas pa med mycket information over tid. Systemet behover inte ha avancerad automatisk indexering i MVP, men det maste vara tydligt var denna information laggs in och hur den anvands.

## 12. Karnflode
1. Anvandaren lagger in ett amne eller en ide i `Google Sheets`.
2. Anvandaren triggar systemet manuellt via CLI-kommando eller knapp i review-UI.
3. Systemet hamtar nasta rad med status `new` och satter status till `processing`.
4. Systemet laser in kundens config och kunskapsbank.
5. Systemet skickar amnet, plattformen och relevant foretagskontext till `OpenAI API`.
6. OpenAI returnerar:
   - title
   - hook
   - caption
   - image_prompt
7. Systemet skickar `image_prompt` plus relevant visuell foretagskontext till Googles officiella `Gemini Image Generation API`.
8. Genererad bild sparas lokalt och sokvagen lagras i datamodellen. Status satts till `generated`.
9. Anvandaren granskar resultatet i en enkel lokal webbvy och valjer:
   - approve
   - regenerate copy
   - regenerate image
   - edit manually
10. Nar posten ar godkand markeras den som `approved`.
11. Systemet kan darefter exportera posten som ett fardigt content-paket.

## 13. Plattformsstrategi
### Aktiv plattform i MVP
- `Instagram`

### Placeholder-plattformar
- `LinkedIn`
- `Facebook`
- `X`
- `TikTok`

### Princip
Datamodell, promptstruktur och kodarkitektur ska fran start ha ett falt for `platform`, men bara `Instagram` behover ha faktisk logik i MVP:n.

## 14. Kanalregler For Instagram MVP
MVP:n ska optimera for vanliga Instagram feed-posts.

### Format
- Bildformat default: `4:5`
- Framtida stod: `9:16` for stories/reels

### Innehall
- Copy ska skrivas for Instagram-tonalitet
- Caption ska vara latt att lasa i mobil
- Hook ska fungera for forsta raden
- Bildprompt ska vara tydligt kopplad till captionens budskap
- Copy och bild ska spegla kundens varumarke enligt config och kunskapsbank

## 15. Produktkrav
### 15.1 Input
Systemet maste kunna lasa fran ett `Google Sheet` dar varje rad representerar en postide.

Minimikrav pa inputfalt:
- `id`
- `topic`
- `platform`
- `status`

### 15.2 Templatebarhet
Systemet maste vara strukturerat sa att en ny kund kan onboardas utan att affarskritiska andringar goras direkt i core-koden.

Minimikrav:
- separat kundconfig
- separat kunskapsbank
- separat `.env` for nycklar och IDs
- tydlig README eller setupguide for "andra detta"
- inga krav pa kodandringar for normal kundanpassning

### 15.3 Foretagsprofil
Systemet maste ha en definierad foretagsprofil som anvands i genereringen.

Minimikrav:
- foretagsnamn
- kort beskrivning
- malgrupp
- erbjudande eller tjanstefokus
- tonalitet
- CTA-riktning

### 15.4 Kunskapsbank
Systemet maste kunna lasa kundspecifik kunskap fran separata filer.

Minimikrav:
- enkel mappstruktur
- stod for flera filer
- tydliga kategorier eller filnamn
- kontexten ska kunna injiceras i copygenerering
- kontexten ska kunna injiceras i bildgenerering

### 15.5 Textgenerering
Systemet maste kunna skicka amne, plattform och foretagskontext till `OpenAI API` och fa tillbaka strukturerad output for Instagram.

Minimikrav pa output:
- `title`
- `hook`
- `caption`
- `image_prompt`

### 15.6 Bildgenerering
Systemet maste anvanda Googles officiella `Gemini Image Generation API`.

Minimikrav:
- stod for bildgenerering fran textprompt
- mojlighet att ange `aspectRatio`
- genererad bild sparas som lokal fil under `output/images/`
- relativ sokvag till filen lagras i datamodellen (`image_path`)
- bildprompten ska kunna forstarkas med visuell foretagskontext fran kunskapsbanken

### 15.7 Review
Systemet maste stodja manuell review innan posten anses klar.

Minimikrav:
- markera post som `generated`
- markera post som `approved`
- markera post som `needs_changes` eller motsvarande
- stod for att regenerera copy eller bild separat

### 15.8 Export
Systemet maste kunna exportera ett godkant content-paket.

Minimikrav pa export:
- title
- hook
- caption
- image
- metadata om plattform och status
- tillracklig metadata for att forsta vilken kundprofil och vilket underlag som anvants

## 16. Datamodell For MVP
### 16.1 Google Sheets
Foreslagna kolumner i `Google Sheets`:

- `id`
- `topic`
- `platform`
- `status`
- `title`
- `hook`
- `caption`
- `image_prompt`
- `image_path`
- `review_notes`
- `approved_at`
- `created_at`
- `updated_at`

### Rekommenderade statusvarden
- `new`
- `processing`
- `generated`
- `approved`
- `needs_changes`
- `error`
- `exported`

### 16.2 Kundfiler
Utovet Google Sheets ska projektet ha en tydlig struktur for kundredigerbara filer.

Konceptuella filer eller mappar:
- `config/company.*`
- `config/platforms.*`
- `knowledge/brand/*`
- `knowledge/offers/*`
- `knowledge/audience/*`
- `knowledge/visuals/*`
- `knowledge/rules/*`

Exakta filformat kan beslutas senare, men de ska vara enkla att redigera, till exempel `json`, `yaml` eller `md`.

## 17. Val Av Datakalla
`Google Sheets` ar valt som primar datakalla for contentkon i MVP:n.

### Skal
- gratis och lattillgangligt
- enkelt att forsta och uppdatera manuellt
- passar en radbaserad contentko mycket bra
- lag integrationsfriktion for forsta versionen

### Avgransning
Google Sheets ar valt for `contentkon`, inte som plats for all kundkunskap. Kundspecifik profil och kunskapsbank ska i stallet leva i tydliga templatefiler i projektet.

### Varfor inte Notion i MVP
- battre som adminvy an som forsta karndatalager
- mer komplex behorighets- och API-modell for detta use case
- svagare som gratis bas for denna templateprodukt

## 18. Tekniska Riktlinjer
### Rekommenderad karna
- `Node.js` / `JavaScript`

### Externa integrationer
- `Google Sheets API`
- `OpenAI API`
- `Gemini Image Generation API` via officiell Google-SDK

### Bildvag
Officiell Google-SDK anvands direkt i applikationskoden. Inga community-MCP-lager eller tredjepartstjanster ska vara grund for produktionsflodet.

### Bildlagring
Genererade bilder sparas lokalt under `output/images/` med filnamn baserat pa post-id. Relativ sokvag lagras i `image_path` i Google Sheets.

### Arkitekturprincip
Core-logik, kundspecifik config och kunskapsbank ska vara separerade.

Det ska vara tydligt i kodbasen:
- vad som ar ramverket
- vad som ar kundspecifik setup
- vad som ar innehallsunderlag

## 19. UX-Niva I MVP
MVP:n ska ha en enkel lokal webbvy som review-interface. Google Sheets anvands som datakalla, inte som review-UI, eftersom bild och text behover visas tillsammans pa ett tydligt satt.

Review-UI ska kunna:
- se genererad text
- se genererad bild
- lamna review notes
- godkanna eller begara andring

MVP:n behover inte ha en avancerad UI for att redigera kunskapsbanken. Det ar tillrackligt att kunskapsbanken ar filbaserad och tydligt dokumenterad.

## 20. Framgangskriterier
MVP:n anses lyckad nar foljande fungerar:

- en ny rad i `Google Sheets` kan bearbetas utan manuell kodkorning per steg
- systemet genererar komplett Instagram-utkast med text och bild
- innehallet speglar kundens tonalitet, erbjudande och visuella riktning battre an ett generiskt AI-utkast
- anvandaren kan avgora om posten ska godkannas eller goras om
- godkant innehall kan exporteras som fardigt paket
- en ny kund kan onboardas genom att andra nycklar, config och kunskapsfiler utan att behova skriva om core-logik

## 21. MVP-Avgransning
Version 1 ska kunna hantera:

- en kund per deployment
- en anvandare eller ett litet team
- en aktiv plattform: `Instagram`
- ett enkelt inflode fran `Google Sheets`
- manuell trigger
- enkel kunskapsbank i filer
- manuell review
- export av godkant material

Version 1 ska inte krava:
- multi-tenant runtime
- full scheduler
- direkt publicering
- avancerat asset management
- avancerad knowledge retrieval med embeddings

## 22. Risker
- Bildkvalitet eller tonalitet kan bli for generisk utan bra promptstyrning.
- Kunskapsbanken kan bli for osorterad om det inte finns tydliga filtyper eller mallar.
- Kundanpassning kan fortfarande bli rorig om config sprids till flera stallen i kodbasen.
- API-kostnader kan vaxa om regenerering anvands mycket, aven om datalagret ar gratis.
- En otydlig statusmodell kan skapa fel i kon.
- For svag kundkunskap ger svag output, aven om flodet fungerar tekniskt.

## 23. Framtida Utbyggnad
Efter MVP kan foljande laggas till:

- stod for `LinkedIn`, `Facebook`, `X` och `TikTok`
- kanalunika promptmallar
- UI for att hantera kunskapsbank
- automatisk import av kundmaterial till kunskapsbanken
- versionshistorik for kunskapsbank och regenereringar
- automatisk publicering
- templatebibliotek for olika contentformat
- analytics och larloop pa vilka poster som fungerar bast

## 24. Oppna Beslut
Foljande behover lasas innan implementation:

- ~~exakt filformat for kundconfig och kunskapsbank~~ → **beslutat: `yaml` for config, `md` for kunskapsbank**
- exportformat: filstruktur, `json` eller enkelt adminuttag
- om Instagram MVP bara ska stodja `4:5`, eller aven `9:16` fran start
- vilken standardniva av kunskapsbank som ska kravas for att en ny kund ska anses onboardad

## 25. Rekommenderad Nasta Fasad
Nasta steg efter denna PRD bor vara att skriva en kort teknisk spec for:

- projektstruktur for template kontra core
- onboardingyta for ny kund
- format for kundconfig
- format for kunskapsbank
- statusflode
- Google Sheet-schema
- promptkontrakt for OpenAI
- bildkontrakt for Gemini image generation
- exportformat
