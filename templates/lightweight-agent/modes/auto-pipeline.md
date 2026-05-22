# Auto-Pipeline Mode

Triggered when user pastes a URL or item content directly with no sub-command.

## Steps

1. **Load context**
   - Read `config/profile.yml`
   - Read `modes/_profile.md`
   - If URL: fetch the content (WebFetch or kimi-webbridge snapshot)

2. **Evaluate** (run evaluate.md logic)
   - Score A-F across relevant dimensions from profile.yml
   - Check deal-breakers (auto-skip if any match)
   - Flag visa/authorization issues if any found

3. **Write report**
   - Report number: find max existing in `reports/`, add 1, zero-pad to 3 digits
   - File: `reports/{###}-{company-slug}-{YYYY-MM-DD}.md`
   - Follow report format from _shared.md

4. **Write tracker TSV**
   - File: `batch/tracker-additions/{###}-{company-slug}.tsv`
   - Follow TSV format from _shared.md exactly

5. **Run merge + verify**
   - `python scripts/merge_tracker.py`
   - `python scripts/verify.py`

6. **Summarize**
   Print: score, recommendation (APPLY / REVIEW / SKIP), key gaps, comp check.

## Auto-skip behavior

If a deal-breaker is detected:
- Set status to `SKIP`
- Still write report documenting why
- Do NOT run PDF or extensive analysis
- Print: "SKIP: [reason]"
