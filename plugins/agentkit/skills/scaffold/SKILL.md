# AgentKit Scaffold

Build a new domain-specific agent from the lightweight-agent template in one shot.

Triggered by: "create me an agent for {domain}" or "scaffold a new agent" or "/agentkit scaffold"

---

## Step 1: Ask 3 questions

Before doing anything, ask:

1. **Domain name** (used as folder and skill name): e.g., "rental", "jobs", "content", "stocks"
2. **Primary data sources**: What URLs/APIs to scan? (Greenhouse/Lever/Ashby auto-detected; for custom sources, list the domain or API endpoint)
3. **Scoring dimensions**: What are the 3-5 dimensions to evaluate items on? (e.g., "match, comp, red flags" or "price, location, condition, seller rating")

Wait for answers before proceeding.

---

## Step 2: Load context

Read these files completely:
- `~/projects/GR-Claude/templates/lightweight-agent/AGENTS.md`
- `~/projects/GR-Claude/templates/lightweight-agent/modes/_shared.md`
- `~/projects/GR-Claude/templates/lightweight-agent/config/profile.yml`
- `~/.claude/knowledge/INDEX.md` (load any files relevant to the domain)

---

## Step 3: Generate the agent

Target directory: `~/projects/{domain}-ops/`

### Files to copy verbatim (no modifications):
- `scripts/merge_tracker.py`
- `scripts/verify.py`
- `scripts/batch_runner.sh`
- `modes/_shared.md` (kimi-webbridge wiring, writing rules, file paths)
- `modes/auto-pipeline.md`
- `modes/evaluate.md`
- `modes/batch.md`
- `modes/scan.md`
- `modes/apply.md`
- `modes/tracker.md`
- `modes/report.md`
- `data/pipeline.md`
- `data/tracker.md`
- `batch/batch-input.tsv`
- `batch/batch-prompt.md`
- `CLAUDE.md`

### Files to customize (replace {placeholders}):

**`AGENTS.md`:**
- Replace `{AgentName}` with `{domain}-ops`
- Replace `{skill}` with the skill name (e.g., `rental-ops`)
- Keep routing table identical

**`config/profile.yml`:**
- Set `agent.name` to `{domain}-ops`
- Set `agent.domain` to a one-line description of the domain
- Set `scoring.apply_threshold`, `review_threshold`, `skip_threshold` based on domain (job search stays 4.0/3.5/2.0; adjust for other domains)
- Leave user fields blank for the user to fill

**`modes/_profile.md`** (create from `_profile.template.md`):
- Replace `{AgentName}` with `{domain}-ops`
- Add the scoring dimensions from the user's answers as the scoring guidance section
- Leave other sections blank for the user to fill

**`scripts/scan.py`:**
- Copy verbatim
- The providers (Greenhouse/Lever/Ashby) are already generic
- If user specified custom API sources, add a note in comments at the top: `# Custom source: {URL} - requires adding a provider function`

Create these directories (empty, gitignored content):
- `reports/`
- `output/`
- `batch/logs/`
- `batch/tracker-additions/`

Create `.gitignore`:
```
output/
batch/logs/
batch/tracker-additions/merged/
.venv/
*.pyc
```

---

## Step 4: Register in marketplace

Edit `~/projects/GR-Claude/.claude-plugin/marketplace.json`:
Add to `plugins[]`:
```json
{
  "name": "{domain}-ops",
  "description": "{domain}-ops: {one-line description from user's domain answer}",
  "source": "./plugins/{domain}-ops",
  "skills": []
}
```

---

## Step 5: Confirm

Print:
```
Agent created at ~/projects/{domain}-ops/

Next steps:
1. Edit config/profile.yml with your targets and thresholds
2. Edit modes/_profile.md with your background and framing
3. Create portals.yml with your data sources (see modes/scan.md for format)
4. Run /{domain}-ops to start

Scoring dimensions configured: {list from user answers}
```

---

## Critical rules

- Copy `_shared.md`, all mode files, and all Python scripts VERBATIM. Do not adapt them for the domain.
- Only customize: `AGENTS.md` labels, `config/profile.yml` schema, `modes/_profile.md` narrative template.
- Do NOT create a new SKILL.md or plugin directory unless the user explicitly asks.
- The new agent is a standalone directory, not a plugin in GR-Claude. The marketplace entry is just for discoverability.
