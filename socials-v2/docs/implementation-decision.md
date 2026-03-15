# Implementation Decision (A vs B)

## Inputs Compared

1. `social-media-manager` (stable Node flow)
2. `socials-v2/ai-social-media-post-automation` (A)
3. `socials-v2/github-skills.md` (B pointers)

## Findings

### social-media-manager

Strengths:

- End-to-end working flow (Sheets -> AI copy -> AI image -> review -> publish/export)
- Clear service boundaries
- Real dashboard and CLI
- Practical `.env.local` integration

Weaknesses:

- Single-brand oriented
- No planner/calendar view
- Limited brand switching ergonomics

### socials-v2 (before implementation)

Strengths:

- Existing A/B options and env setup

Weaknesses:

- Root had no complete runnable product flow

### A: ai-social-media-post-automation

Strengths:

- Good conceptual architecture in README
- Useful component model: orchestrator, scheduler, adapters, analytics

Weaknesses:

- Not production runnable in current state
- Missing modules and broken imports
- `config.py` empty
- Would require major rebuild before use

### B: github-skills.md

Strengths:

- Good idea source (content research, sheets automation, instagram automation)
- Flexible for rebuilding a productized template

Weaknesses:

- Not a runnable codebase by itself
- Requires implementation work to become product

## Decision

Chosen path: **B-style rebuild in `socials-v2`**, using stable implementation patterns from `social-media-manager` and A's architectural ideas.

Reason:

- A was too incomplete to finish with only minor adjustments.
- Fastest route to robust, sellable, maintainable solution was to port stable core and add missing product capabilities:
- multi-brand support
- brand knowledge bank structure
- planner/calendar base
- brand switch in dashboard

## Result

`socials-v2` now contains a complete, runnable flow with multi-brand-ready structure and dashboard planner foundations.
