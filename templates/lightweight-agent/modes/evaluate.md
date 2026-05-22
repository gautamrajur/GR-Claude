# Evaluate Mode

Single-item evaluation. No report file, no PDF, no tracker entry.

## Steps

1. Load `config/profile.yml` and `modes/_profile.md`
2. Fetch the item content if URL
3. Score against the dimensions in profile.yml
4. Check deal-breakers
5. Print structured evaluation to chat

## Scoring dimensions (default - customize in _profile.md)

| Dimension | Weight | What to assess |
|-----------|--------|----------------|
| Match | 40% | How well does the candidate profile match? |
| North Star | 25% | Does this align with the target archetype? |
| Comp | 20% | Does comp meet/exceed threshold? |
| Red flags | 15% | Blockers, deal-breakers, risks |

**Global score = weighted average**

## Output format

```
## Evaluation: {Company} - {Item}

**Score:** X.X/5
**Recommendation:** APPLY / REVIEW / SKIP

### Match
[analysis]

### Key gaps
[any gaps and whether hard blockers]

### Comp
[comp analysis vs targets]

### Red flags
[any blockers]
```
