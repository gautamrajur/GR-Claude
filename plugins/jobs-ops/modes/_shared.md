# Shared Rules - {AgentName}

## Writing rules

- Never use em dashes (—). Use a hyphen (-) or rephrase.
- Keep explanations direct. No filler phrases.
- No markdown bold in status fields.
- Dates go in date columns, not status fields.

## File paths

| File | Purpose |
|------|---------|
| `config/profile.yml` | User targets, thresholds, narrative |
| `modes/_profile.md` | User framing and adaptive narrative |
| `data/pipeline.md` | Pending item inbox (`- [ ] url | source | notes`) |
| `data/tracker.md` | Evaluation tracker table |
| `data/scan-history.tsv` | Scanner dedup history |
| `reports/` | Evaluation reports (`{###}-{slug}-{YYYY-MM-DD}.md`) |
| `output/` | Generated artifacts (gitignored) |
| `batch/tracker-additions/` | Per-job TSV additions (merged after batch) |

## Tracker format

```markdown
# Tracker

| # | Date | Company | Item | Score | Status | PDF | Report | Notes |
|---|------|---------|------|-------|--------|-----|--------|-------|
```

### Canonical statuses

`Evaluated`, `Applied`, `Responded`, `Interview`, `Offer`, `Rejected`, `Discarded`, `SKIP`

No bold, no dates in status. Notes column for extra context.

## Report format

```markdown
# Evaluation: {Company} - {Role}

**Date:** YYYY-MM-DD
**Score:** X.X/5
**URL:** {url}

## A) Item Summary
## B) Match / Analysis
## C) Strategy
## D) Score Summary
```

Report numbering: sequential 3-digit zero-padded. `max_existing + 1`.

## TSV format for tracker additions

Single tab-separated line, 9 columns:
```
{num}\t{date}\t{company}\t{item}\t{status}\t{score}/5\t{pdf_emoji}\t[{num}](reports/{slug}.md)\t{notes}
```

Column order: num, date, company, item, **status**, **score**, pdf, report, notes.

## Batch pipeline rules

- NEVER edit tracker.md to ADD entries. Write TSV to `batch/tracker-additions/` and run merge script.
- YES you can edit tracker.md to UPDATE status/notes of existing entries.
- After batch: run `python scripts/merge_tracker.py` then `python scripts/verify.py`.
- Health check: `python scripts/verify.py`

## Python scripts

- `scripts/scan.py` - portal scanner (Greenhouse/Lever/Ashby APIs)
- `scripts/merge_tracker.py` - merge TSV additions into tracker.md
- `scripts/verify.py` - pipeline integrity checks
- `scripts/batch_runner.sh` - bash + `claude -p` batch orchestrator

## Browser automation (kimi-webbridge)

Read `~/.claude/knowledge/kimi-webbridge.md` before any browser tasks.

Key rules:
- Health check first: `~/.kimi-webbridge/bin/kimi-webbridge status`
- Always `find_tab` before `navigate` (reuse existing tabs)
- Re-snapshot after any dropdown or dynamic DOM change (@e refs shift)
- File uploads: use `#id` selector via `evaluate()`, NOT `@e` ref
- Screenshots: always use `~/.claude/skills/kimi-webbridge/scripts/screenshot.sh`
- Simplify extension auto-fills fields - re-verify everything it touches

## Portals configuration (`portals.yml`)

Defines which sources to scan. Required fields per entry:
```yaml
tracked_companies:
  - name: "CompanyName"
    careers_url: "https://jobs.ashbyhq.com/companyname"  # auto-detects provider
    enabled: true
title_filter:
  positive: ["engineer", "analyst"]
  negative: ["director", "principal"]
location_filter:
  allow: ["remote", "US"]
  block: ["on-site only"]
```
