---
name: video-to-10k-webflow
description: Extraherar och operationaliserar starka, säljbara webbflöden från videos (t.ex. Nano Banana + scroll-animation + snabb deploy + SEO-audit) till ett repeterbart leveranssystem.
metadata:
  openclaw:
    emoji: "💸"
---

# Video → 10k Webflow Skill

## Syfte
Förvandla video-insikter till **färdiga leveransflöden** (inte bara sammanfattningar):
- steg-för-steg SOP
- promptpaket
- asset-spec
- deploy/checklist
- paketering till säljbart erbjudande

## När skillen ska användas
Använd när användaren vill:
- extrahera "hur de gör" från en video
- få exakta steg + trix
- bygga en repeterbar tjänst/automation av videoflöde
- få ett 10k-webflow för agency/produktiserad leverans

## Standard-output
Leverera alltid:
1. **Flow map (A→Ö)**
2. **SOP med exakta steg**
3. **Prompt pack** (image + transition + site generation)
4. **Teknisk pipeline** (tools + handoffs)
5. **QA + SEO checklista**
6. **Offer packaging** (engång + recurring)
7. **Automation opportunities** (vad som bör bli skill/script)

## Canonical 10k Website Flow (från video-mönstret)
1. Välj nisch/kundcase + baseline-site
2. Extrahera brand (färg, ton, visuella regler)
3. Generera hero assets (assembled + exploded)
4. Bygg transition-prompt
5. Skapa 5–8s video-animation från start/slut-frame
6. Integrera i hero + scroll-beteende
7. Klona informationsarkitektur + ersätt copy/visuals
8. Generera sidor (About, Testimonials, Team, Contact)
9. Deploy snabbt (preview/live)
10. Kör SEO/metadata/schema + prestandapass
11. Leverera demo + audit + retainer-förslag

## Scroll Animation SOP (detalj)
1. Ta fram två stillbilder:
   - Start = assembled
   - End = exploded
2. Håll samma bildförhållande och motivankare
3. Ladda båda i videoverktyg (image-to-video)
4. Ange transition-prompt (kamera + objekt-rörelse + easing)
5. Rendera 5–8 sek (16:9 för hero-video)
6. Välj bästa variant utifrån: tydlighet, premiumkänsla, läsbarhet
7. Exportera webb-optimerad video
8. Integrera med scroll-trigger + fallback (poster)
9. Finjustera timing/easing så text och CTA förblir läsbara

## Prompt Pack (starter)
### 1) Asset prompt (assembled)
"Create a premium, photoreal hero scene for [BRAND] in [NICHE]. Clean composition, strong center subject, ample negative space for headline/CTA, cinematic lighting, brand color accents [COLORS]. 16:9, high detail, no text overlays."

### 2) Asset prompt (exploded)
"Using the same scene and subject, generate an exploded-view variant where key components separate outward with realistic spacing and depth. Keep lighting and perspective consistent with source image. Preserve brand fidelity and cleanliness. 16:9, high detail, no text overlays."

### 3) Transition prompt
"Animate a smooth premium transition from assembled scene to exploded scene. Camera does subtle push-in, elements separate with physically plausible motion and slight stagger, soft ease-in-out, no jitter, no morph artifacts, maintain subject legibility in center. Duration 6–7s."

### 4) Site generation prompt
"Build a responsive premium landing page for [BRAND], using provided hero video and brand system. Sections: Hero, Social Proof, Services, Process, Testimonials, FAQ, CTA. Keep strong contrast, conversion-focused hierarchy, mobile-first spacing, fast-loading assets."

## QA / SEO gates (måste passera innan leverans)
- LCP/CLS/INP inom acceptabla nivåer
- Hero-video med fallback-image + lazy/loading-strategi
- Metadata: title/description/OG/Twitter
- Schema: Organization + WebSite + Service (vid behov)
- CTA-spårning och kontaktflöde testat
- Mobil test: iOS + Android viewport

## Monetisering (10k-trixen)
- **Gratis premium mockup** som dörröppnare
- **Snabb demo inom 24–72h** för hög close-rate
- **Website som entry-offer**, recurring på SEO/CRO/content/maintenance
- **Produktiserad leverans** (fasta steg + tidsbox + tydlig scope)

## Rekommenderad systematisering
Om mönstret återkommer, bygg dessa komponenter:
1. `video_flow_extractor.py` (tar transcript → SOP JSON)
2. `prompt_pack_builder.py` (brand inputs → promptpaket)
3. `site_scaffold_generator.py` (sections + copy skeleton)
4. `delivery_checklist.md` (standardiserad QA/SEO gate)

## Candidate skills/MCP att koppla på
### Redan hittade relevanta skills
- `kingbootoshi/nano-banana-2-skill@nano-banana`
- `alb-o/pw-rs@pw-higgsfield`
- `firecrawl/cli@firecrawl`
- `vercel-labs/vercel-plugin@vercel-cli`
- `vercel-labs/vercel-plugin@vercel-api`

### För vad de används
- Nano Banana-skill: bildgenerering (assembled/exploded)
- Higgsfield-skill: image-to-video transition
- Firecrawl: snabb brand/content-extraktion
- Vercel: preview/live deploy och iteration

## Install commands (valfritt)
```bash
npx skills add kingbootoshi/nano-banana-2-skill@nano-banana -g -y
npx skills add alb-o/pw-rs@pw-higgsfield -g -y
npx skills add firecrawl/cli@firecrawl -g -y
npx skills add vercel-labs/vercel-plugin@vercel-cli -g -y
```

## Output format till Jonas (kort)
- TL;DR
- 5 takeaways
- Exakta steg (A→Ö)
- Vad som är nytt/speciellt
- Vad som bör automatiseras till skill/script
- Nästa konkreta action inom 24h
