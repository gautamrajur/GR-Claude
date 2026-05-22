# Batch Worker Prompt

You are a batch evaluation worker. Process the following item completely.

## Item Details

- URL: {{URL}}
- Report number: {{REPORT_NUM}}
- Date: {{DATE}}
- Batch ID: {{ID}}

## Instructions

1. Read `config/profile.yml` and `modes/_profile.md` for user context
2. Fetch the item content from the URL (use WebFetch)
3. Evaluate according to `modes/evaluate.md` logic
4. Write a complete report to `reports/{{REPORT_NUM}}-{company-slug}-{{DATE}}.md`
5. Write a TSV line to `batch/tracker-additions/{{REPORT_NUM}}-{company-slug}.tsv`

## TSV format

9 tab-separated columns:
`{{REPORT_NUM}}\t{{DATE}}\t{company}\t{item title}\t{status}\t{score}/5\t❌\t[{{REPORT_NUM}}](reports/{{REPORT_NUM}}-{company-slug}-{{DATE}}.md)\t{one-line note}`

Status: `Evaluated` (or `SKIP` if deal-breaker detected)
Score: use format `X.X/5`

## Output

When done, print a single JSON line:
`{"score": X.X, "report": "{{REPORT_NUM}}", "status": "done"}`
