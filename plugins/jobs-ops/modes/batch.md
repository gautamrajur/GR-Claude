# Batch Mode

Process multiple items from `batch/batch-input.tsv` in parallel using `claude -p` workers.

## Steps

1. Verify `batch/batch-input.tsv` exists with pending items
2. Verify `batch/batch-prompt.md` exists
3. Run: `bash scripts/batch_runner.sh --parallel 3`
4. After completion: `python scripts/merge_tracker.py && python scripts/verify.py`
5. Report summary

## batch-input.tsv format

```
id	url	source	notes
1	https://example.com/item1	manual	CompanyName | Item Title
2	https://example.com/item2	scan	CompanyName | Item Title
```

## batch-prompt.md

The worker prompt template. Placeholders replaced by batch_runner.sh:
- `{{URL}}` - item URL
- `{{REPORT_NUM}}` - assigned report number
- `{{DATE}}` - YYYY-MM-DD
- `{{ID}}` - batch job ID

Worker must: evaluate, write report to `reports/{{REPORT_NUM}}-{slug}-{{DATE}}.md`, write TSV to `batch/tracker-additions/{{REPORT_NUM}}-{slug}.tsv`.

## Adding items to batch

To add a URL to the batch:
1. Find the max id in batch-input.tsv
2. Append: `{id+1}\t{url}\t{source}\t{notes}`
3. Or append to data/pipeline.md for pipeline mode to pick up

## Parallel limit

3 workers is the safe default. Above 5 risks API rate limits.
