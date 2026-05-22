# Tracker Mode

Show the current application/evaluation status overview.

## Steps

1. Read `data/tracker.md`
2. Parse the table
3. Group by status
4. Print summary

## Output format

```
## Status Overview ({date})

Applied: {n}
Evaluated (pending decision): {n}
In Progress (Interview/Responded): {n}
Completed (Offer/Rejected/Discarded): {n}
Skipped: {n}

## Recommended Next Actions
- [n] high-scoring items (>= 4.0) in Evaluated - consider applying
- [n] items with no follow-up in 7+ days

## Recent Activity (last 7 days)
[list recent additions/status changes]
```

## Health check

Also run: `python scripts/verify.py` to check pipeline integrity.
