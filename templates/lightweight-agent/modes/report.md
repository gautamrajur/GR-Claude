# Report Mode

Generate a detailed report for an already-evaluated item, or regenerate an existing report.

## Steps

1. Identify the item (URL or report number from tracker.md)
2. Load config/profile.yml and modes/_profile.md
3. Fetch content if needed
4. Write report to `reports/{###}-{company-slug}-{YYYY-MM-DD}.md`
5. Confirm path to user

## Report sections

```markdown
# Evaluation: {Company} - {Item}

**Date:** YYYY-MM-DD
**Score:** X.X/5
**URL:** {url}

---

## A) Item Summary
Brief description. Domain, type, scope.

## B) Match Analysis
Table: requirement -> CV/profile match -> strength (Strong/Good/Gap)

## C) Gaps
Table: gap -> hard blocker? -> mitigation

## D) Strategy
How to position. Key talking points.

## E) Score Summary
| Dimension | Score | Notes |
|-----------|-------|-------|
| Match | X/5 | |
| North Star | X/5 | |
| Comp | X/5 | |
| Red flags | 0/5 | none / list |
| **Global** | **X.X/5** | |

**Recommendation:** APPLY / REVIEW / SKIP
```
