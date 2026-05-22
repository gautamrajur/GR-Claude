# {AgentName} -- Router

## Mode Routing

| Input | Mode |
|-------|------|
| (empty / no args) | `discovery` - show command menu |
| Item URL or text (no sub-command) | `auto-pipeline` |
| `evaluate` | `evaluate` |
| `batch` | `batch` |
| `scan` | `scan` |
| `apply` | `apply` |
| `tracker` | `tracker` |
| `report` | `report` |

**Auto-pipeline detection:** If input is a URL or looks like item content (keywords: "about", "requirements", "description", etc.), run `auto-pipeline`.

---

## Discovery Mode (no arguments)

Show this menu:

```
{AgentName} -- Command Center

Available commands:
  /{skill} {URL or content}  -> AUTO-PIPELINE: evaluate + report + tracker
  /{skill} scan              -> Scan sources and discover new items
  /{skill} batch             -> Batch process pending items in parallel
  /{skill} apply             -> Fill out a form or take action on an item
  /{skill} evaluate          -> Single-item evaluation only
  /{skill} tracker           -> Status overview
  /{skill} report            -> Generate a report for an item

Inbox: add URLs to data/pipeline.md -> /{skill} pipeline
Or paste content directly to run the full pipeline.
```

---

## Context Loading

After determining the mode, load the necessary files before executing:

### All modes require `_shared.md` + their mode file:
Read `modes/_shared.md` + `modes/{mode}.md`

Applies to: `auto-pipeline`, `evaluate`, `batch`, `scan`, `apply`

### Standalone modes (only their mode file):
Read `modes/{mode}.md`

Applies to: `tracker`, `report`

Execute the instructions from the loaded mode file.

---

## Data Contract

**User Layer (NEVER auto-updated, customization goes here):**
- `config/profile.yml`, `modes/_profile.md`, `data/*`, `reports/*`, `output/*`

**System Layer (auto-updatable, do NOT put user data here):**
- `modes/_shared.md`, all other modes, `AGENTS.md`, `CLAUDE.md`, scripts

**THE RULE:** When the user asks to customize anything (targets, narrative, scoring, thresholds), ALWAYS write to `modes/_profile.md` or `config/profile.yml`. NEVER edit `modes/_shared.md` for user-specific content.
