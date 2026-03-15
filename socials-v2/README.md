# Socials V2

Socials V2 is a white-label social content workflow built for multiple brands.

It includes:

- AI copy generation (OpenAI)
- AI image generation (Gemini)
- Google Sheets pipeline backend
- Instagram publishing integration
- Dashboard with:
- content overview
- pipeline status
- brand switcher
- calendar/planner base
- knowledge bank view

## Why this structure

`ai-social-media-post-automation` (A) had useful component ideas (orchestrator, scheduler, adapters), but the implementation was incomplete and not runnable (`config.py` empty, missing modules, broken imports).

This project therefore uses a robust implementation path based on a stable flow and applies A's component thinking where it adds value:

- queue + scheduling support
- clearer pipeline states
- planner-ready dashboard

## Core Flow

1. New row in Google Sheet with status `new`.
2. Process next post:
- loads active brand profile + knowledge bank
- generates title/hook/caption/image prompt (OpenAI)
- generates image (Gemini)
- updates row to `generated`
3. Review in dashboard:
- notes
- regenerate copy/image
- approve
- schedule or publish
4. Scheduled rows (`status=scheduled`) can be auto-published by queue worker when due.
5. Export approved/published content package.

## Project Structure

- `src/` application code
- `brands/` brand packs (multi-brand support)
- `brands/default/` default active brand
- `brands/template/` starter template for new customer
- `public/` dashboard styles
- `scripts/` local automation helpers
- `docs/` setup notes

## Multi-Brand Model

Each customer is a folder under `brands/<brand-key>/`:

- `brand.yaml` (name + short description)
- `company.yaml` (company profile)
- `platforms.yaml` (platform rules)
- `knowledge/**.md` (tone, audience, offers, no-go, etc)

Switch active brand:

- from dashboard brand selector, or
- with env `ACTIVE_BRAND=<brand-key>`, or
- via CLI flag `--brand <brand-key>`

## Required Environment Variables

Use `.env.local` (already supported):

- `OPENAI_API_KEY`
- `GEMINI_API_KEY`
- `GOOGLE_SHEETS_SPREADSHEET_ID`
- `GOOGLE_SERVICE_ACCOUNT_KEY_PATH`
- `GOOGLE_SHEETS_TAB_NAME`
- `PORT`
- `ACTIVE_BRAND`
- `INSTAGRAM_ACCESS_TOKEN`
- `INSTAGRAM_APP_SCOPED_USER_ID`
- `INSTAGRAM_GRAPH_BASE_URL`
- `INSTAGRAM_GRAPH_API_VERSION`
- `PUBLIC_BASE_URL`
- `INSTAGRAM_AUTO_PUBLISH`
- `AUTO_QUEUE_ENABLED`
- `AUTO_QUEUE_INTERVAL_MS`

Template exists in `.env.example`.

## Google Sheet Columns

The app auto-bootstraps required headers, including:

- `brand_key`
- `topic`
- `status`
- `scheduled_for`
- generation + publish fields

Rows are filtered by active `brand_key` in dashboard and workflow.

## Commands

Install:

```bash
npm install
```

Run dashboard:

```bash
node cli.js serve --brand default
```

Start queue worker:

```bash
node cli.js worker --brand default
```

Process next:

```bash
node cli.js process-next --brand default
```

Schedule post:

```bash
node cli.js schedule <postId> <ISO_DATE> --brand default
```

## Dashboard Statuses

- `new`
- `processing`
- `generated`
- `approved`
- `scheduled`
- `publishing`
- `published`
- `error`
- `exported`

## Onboard New Customer

1. Copy `brands/template` to `brands/<new-brand-key>`.
2. Fill `brand.yaml`, `company.yaml`, `platforms.yaml`, and `knowledge/`.
3. Set `ACTIVE_BRAND=<new-brand-key>` or switch in UI.
4. Add sheet rows with `brand_key=<new-brand-key>` and status `new`.

No core code changes required.
