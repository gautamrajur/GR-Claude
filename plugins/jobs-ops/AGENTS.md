# jobs-ops -- Router

## Mode Routing

| Input | Mode |
|-------|------|
| (empty / no args) | `discovery` - show command menu |
| Job URL or JD text (no sub-command) | `auto-pipeline` |
| `evaluate` | `evaluate` |
| `batch` | `batch` |
| `scan` | `scan` |
| `apply` | `apply` |
| `tracker` | `tracker` |
| `report` | `report` |
| `resume {report_num}` | `resume` |

**Auto-pipeline detection:** If input is a URL (jobs.lever.co, greenhouse.io, ashbyhq.com, linkedin.com/jobs, etc.) or contains JD keywords ("responsibilities", "requirements", "qualifications", "about the role", "we're looking for"), run `auto-pipeline`.

---

## Discovery Mode (no arguments)

Show this menu:

```
jobs-ops -- Command Center

Available commands:
  /jobs-ops {JD URL or text}  -> AUTO-PIPELINE: evaluate + report + tracker
  /jobs-ops scan              -> Scan portals and discover new job postings
  /jobs-ops batch             -> Batch process pending jobs in parallel
  /jobs-ops apply             -> Fill out a job application form
  /jobs-ops evaluate          -> Single-job evaluation only (no report file)
  /jobs-ops tracker           -> Application status overview
  /jobs-ops report            -> Generate or regenerate a report
  /jobs-ops resume {###}      -> Generate ATS-optimized PDF resume for report ###

Inbox: add URLs to data/pipeline.md -> /jobs-ops scan or batch
Or paste a JD directly to run the full pipeline.
```

---

## Context Loading

### Modes that require `_shared.md` + their mode file:
Read `modes/_shared.md` + `modes/{mode}.md`

Applies to: `auto-pipeline`, `evaluate`, `batch`, `scan`, `apply`

### Standalone modes:
Read `modes/{mode}.md`

Applies to: `tracker`, `report`, `resume`

---

## Data Contract

**User Layer (NEVER auto-updated):**
- `config/profile.yml`, `modes/_profile.md`, `data/*`, `reports/*`, `output/*`

**System Layer (auto-updatable):**
- `modes/_shared.md`, all other modes, `AGENTS.md`, `CLAUDE.md`, scripts

**THE RULE:** Customizations (targets, narrative, scoring weights) go in `modes/_profile.md` or `config/profile.yml`. NEVER edit `modes/_shared.md` for user-specific content.
