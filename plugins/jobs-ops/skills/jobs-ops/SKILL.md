---
name: jobs-ops
description: Job search pipeline -- evaluate offers, scan portals, track applications, fill forms
arguments: mode
user-invocable: true
argument-hint: "[scan | batch | apply | evaluate | tracker | report | resume {###}]"
---

# jobs-ops -- Router

All data lives at `~/projects/jobs-ops/`. Always read files from that absolute path.

## Mode Routing

Determine mode from `$mode`:

| Input | Mode |
|-------|------|
| (empty / no args) | `discovery` |
| URL or JD text (no sub-command) | `auto-pipeline` |
| `scan` | `scan` |
| `batch` | `batch` |
| `apply` | `apply` |
| `evaluate` | `evaluate` |
| `tracker` | `tracker` |
| `report` | `report` |
| `resume {###}` | `resume` |

**Auto-pipeline detection:** If `$mode` contains a URL (greenhouse.io, lever.co, ashbyhq.com, linkedin.com/jobs, etc.) or JD keywords ("responsibilities", "requirements", "qualifications", "about the role"), run `auto-pipeline`.

## Discovery Mode

Show this menu:

```
jobs-ops -- Command Center

  /jobs-ops {URL or JD}  -> evaluate + report + tracker entry
  /jobs-ops scan         -> scan portals, find new postings
  /jobs-ops batch        -> batch process pending jobs in parallel
  /jobs-ops apply        -> fill out a job application form
  /jobs-ops evaluate     -> single-job evaluation (no report file)
  /jobs-ops tracker      -> application status overview
  /jobs-ops report       -> generate or regenerate a report
  /jobs-ops resume {###} -> generate ATS-optimized PDF resume for report ###
```

## Context Loading

After routing, load these files in order:

1. `~/projects/jobs-ops/modes/_shared.md`
2. `~/projects/jobs-ops/modes/{mode}.md`
3. `~/projects/jobs-ops/config/profile.yml`
4. `~/projects/jobs-ops/modes/_profile.md`

For `tracker`, `report`, and `resume` modes, skip `_shared.md` - load only the mode file + profile.

Then execute the instructions in the mode file. All script paths are relative to `~/projects/jobs-ops/`:
- Scan: `python3 ~/projects/jobs-ops/scripts/scan.py`
- Merge: `python3 ~/projects/jobs-ops/scripts/merge_tracker.py`
- Verify: `python3 ~/projects/jobs-ops/scripts/verify.py`
- Batch: `bash ~/projects/jobs-ops/scripts/batch_runner.sh`

All scripts must be run with `~/projects/jobs-ops/` as the working directory.
