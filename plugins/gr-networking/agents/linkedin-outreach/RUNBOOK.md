# linkedin-outreach Runbook

Operational reference for manual inspection, rollback, and log analysis.

## Check recent runs

```bash
# Last 20 entries
tail -20 ~/.claude/logs/linkedin-outreach-runs.jsonl | python3 -m json.tool

# Summary by result
python3 -c "
import json, os
path = os.path.expanduser('~/.claude/logs/linkedin-outreach-runs.jsonl')
runs = [json.loads(l) for l in open(path) if l.strip()]
by_result = {}
for r in runs:
    by_result.setdefault(r['result'], []).append(r['profile_name'])
for k, v in by_result.items():
    print(f'{k}: {len(v)} — {v}')
"

# Failures only
python3 -c "
import json, os
path = os.path.expanduser('~/.claude/logs/linkedin-outreach-runs.jsonl')
for l in open(path):
    r = json.loads(l)
    if r['result'] == 'failed':
        print(r['timestamp'], r['profile_name'], r['step_failed'], r['error'])
"
```

## Rollback a self-update

```bash
REL="plugins/gr-networking/agents/linkedin-outreach/linkedin-outreach.md"
REPO=~/projects/GR-Claude

# See all versions
git -C $REPO log --oneline -- $REL

# Restore the version before the last self-update
git -C $REPO checkout HEAD~1 -- $REL

# Restore a specific commit
git -C $REPO checkout <commit_hash> -- $REL

# Push the rollback
git -C $REPO add $REL && git -C $REPO commit -m "rollback: linkedin-outreach to <version>"
git -C $REPO push origin main
```

## Restore from timestamped .bak

```bash
# List available backups
ls ~/projects/GR-Claude/plugins/gr-networking/agents/linkedin-outreach/*.bak.*

# Restore most recent
BAK=$(ls ~/projects/GR-Claude/plugins/gr-networking/agents/linkedin-outreach/*.bak.* | tail -1)
cp "$BAK" ~/projects/GR-Claude/plugins/gr-networking/agents/linkedin-outreach/linkedin-outreach.md
```

## Recreate symlink (new machine setup)

```bash
ln -sf ~/projects/GR-Claude/plugins/gr-networking/agents/linkedin-outreach/linkedin-outreach.md \
       ~/.claude/agents/linkedin-outreach.md
```

## Verify WebBridge manually

```bash
curl -s --max-time 3 http://127.0.0.1:10086/status | python3 -m json.tool
# running: true + extension_connected: true = good to go
```
