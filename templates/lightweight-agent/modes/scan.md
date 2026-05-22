# Scan Mode

Discover new items from configured sources. Zero LLM tokens - pure HTTP.

## Steps

1. Verify `portals.yml` exists
2. Run: `python scripts/scan.py`
3. Review output - new items added to `data/pipeline.md`
4. Suggest: "Run `/{skill} batch` to evaluate the new items"

## Dry run

`python scripts/scan.py --dry-run` previews without writing.

## Single source

`python scripts/scan.py --company CompanyName` scans one company.

## portals.yml setup

Required to scan. If missing, prompt the user to create it:

```yaml
tracked_companies:
  - name: "CompanyName"
    careers_url: "https://jobs.ashbyhq.com/companyname"
    enabled: true
  - name: "AnotherCompany"
    careers_url: "https://job-boards.greenhouse.io/anothercompany"
    enabled: true

title_filter:
  positive: ["engineer", "analyst", "specialist"]
  negative: ["director", "principal", "VP", "head of"]

location_filter:
  allow: ["remote", "United States", "US"]
  block: []
```

Supported providers (auto-detected from careers_url):
- Greenhouse: `job-boards.greenhouse.io/{token}` or `boards.greenhouse.io/{token}`
- Lever: `jobs.lever.co/{company}`
- Ashby: `jobs.ashbyhq.com/{company}`
