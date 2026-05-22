#!/usr/bin/env python3
"""
scan.py - Zero-token portal scanner.
Hits Greenhouse, Lever, and Ashby APIs directly. No LLM cost.

Usage:
  python scripts/scan.py                  # scan all enabled companies
  python scripts/scan.py --dry-run        # preview without writing files
  python scripts/scan.py --company Stripe # scan a single company
"""
import subprocess, sys, os

# Venv bootstrap - never install to system Python
if not os.environ.get("VIRTUAL_ENV"):
    venv_path = os.path.abspath(os.path.join(os.getcwd(), ".venv"))
    if not os.path.exists(venv_path):
        subprocess.check_call([sys.executable, "-m", "venv", venv_path])
    python = os.path.join(venv_path, "bin", "python")
    os.execv(python, [python] + sys.argv)

for pkg in [("requests", "requests"), ("yaml", "pyyaml")]:
    import_name, install_name = pkg
    try:
        __import__(import_name)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", install_name])

import re
import csv
import argparse
from datetime import date
from pathlib import Path

import requests
import yaml

# ── Config ──────────────────────────────────────────────────────────────────

PROJECT_ROOT = Path.cwd()
PORTALS_PATH = PROJECT_ROOT / "portals.yml"
SCAN_HISTORY_PATH = PROJECT_ROOT / "data" / "scan-history.tsv"
PIPELINE_PATH = PROJECT_ROOT / "data" / "pipeline.md"
APPLICATIONS_PATH = PROJECT_ROOT / "data" / "tracker.md"

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; career-ops-scanner/1.0)"}
TIMEOUT = 12
CONCURRENCY = 8  # not used in Python sequential mode - kept for parity

# ── Provider implementations ─────────────────────────────────────────────────

def _fetch_json(url):
    resp = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def _greenhouse_api_url(entry):
    if entry.get("api"):
        return entry["api"]
    url = entry.get("careers_url", "")
    m = re.search(r"job-boards(?:\.eu)?\.greenhouse\.io/([^/?#]+)", url)
    if m:
        return f"https://boards-api.greenhouse.io/v1/boards/{m.group(1)}/jobs"
    return None


def fetch_greenhouse(entry):
    api_url = _greenhouse_api_url(entry)
    if not api_url:
        raise ValueError(f"greenhouse: cannot derive API URL for {entry['name']}")
    data = _fetch_json(api_url)
    jobs = data.get("jobs", []) if isinstance(data, dict) else []
    return [
        {"title": j.get("title", ""), "url": j.get("absolute_url", ""),
         "company": entry["name"], "location": (j.get("location") or {}).get("name", "")}
        for j in jobs if j.get("absolute_url")
    ]


def _lever_api_url(entry):
    url = entry.get("careers_url", "")
    m = re.search(r"jobs\.lever\.co/([^/?#]+)", url)
    return f"https://api.lever.co/v0/postings/{m.group(1)}" if m else None


def fetch_lever(entry):
    api_url = _lever_api_url(entry)
    if not api_url:
        raise ValueError(f"lever: cannot derive API URL for {entry['name']}")
    data = _fetch_json(api_url)
    if not isinstance(data, list):
        return []
    return [
        {"title": j.get("text", ""), "url": j.get("hostedUrl", ""),
         "company": entry["name"], "location": (j.get("categories") or {}).get("location", "")}
        for j in data if j.get("hostedUrl")
    ]


def _ashby_api_url(entry):
    url = entry.get("careers_url", "")
    m = re.search(r"jobs\.ashbyhq\.com/([^/?#]+)", url)
    return f"https://api.ashbyhq.com/posting-api/job-board/{m.group(1)}?includeCompensation=true" if m else None


def fetch_ashby(entry):
    api_url = _ashby_api_url(entry)
    if not api_url:
        raise ValueError(f"ashby: cannot derive API URL for {entry['name']}")
    data = _fetch_json(api_url)
    jobs = data.get("jobs", []) if isinstance(data, dict) else []
    return [
        {"title": j.get("title", ""), "url": j.get("jobUrl", ""),
         "company": entry["name"], "location": j.get("location", "")}
        for j in jobs if j.get("jobUrl")
    ]


PROVIDERS = {
    "greenhouse": (fetch_greenhouse, _greenhouse_api_url),
    "lever": (fetch_lever, _lever_api_url),
    "ashby": (fetch_ashby, _ashby_api_url),
}


def detect_provider(entry):
    """Auto-detect which provider handles this entry based on careers_url."""
    explicit = entry.get("provider")
    if explicit:
        return explicit if explicit in PROVIDERS else None
    for name, (_, detect_fn) in PROVIDERS.items():
        try:
            if detect_fn(entry):
                return name
        except Exception:
            pass
    return None

# ── Filters ──────────────────────────────────────────────────────────────────

def build_title_filter(title_filter_cfg):
    positive = [k.lower() for k in (title_filter_cfg or {}).get("positive", [])]
    negative = [k.lower() for k in (title_filter_cfg or {}).get("negative", [])]

    def check(title):
        lower = title.lower()
        has_positive = not positive or any(k in lower for k in positive)
        has_negative = any(k in lower for k in negative)
        return has_positive and not has_negative
    return check


def build_location_filter(location_filter_cfg):
    if not location_filter_cfg:
        return lambda _: True
    allow = [k.lower() for k in location_filter_cfg.get("allow", [])]
    block = [k.lower() for k in location_filter_cfg.get("block", [])]

    def check(location):
        if not location:
            return True
        lower = location.lower()
        if block and any(k in lower for k in block):
            return False
        if not allow:
            return True
        return any(k in lower for k in allow)
    return check

# ── Dedup ────────────────────────────────────────────────────────────────────

def load_seen_urls():
    seen = set()
    if SCAN_HISTORY_PATH.exists():
        with open(SCAN_HISTORY_PATH) as f:
            reader = csv.reader(f, delimiter="\t")
            next(reader, None)  # skip header
            for row in reader:
                if row:
                    seen.add(row[0])
    if PIPELINE_PATH.exists():
        text = PIPELINE_PATH.read_text()
        for m in re.finditer(r"- \[[ x]\] (https?://\S+)", text):
            seen.add(m.group(1))
    if APPLICATIONS_PATH.exists():
        text = APPLICATIONS_PATH.read_text()
        for m in re.finditer(r"https?://[^\s|)]+", text):
            seen.add(m.group(0))
    return seen


def load_seen_company_roles():
    seen = set()
    if APPLICATIONS_PATH.exists():
        text = APPLICATIONS_PATH.read_text()
        for m in re.finditer(r"\|[^|]+\|[^|]+\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|", text):
            company = m.group(1).strip().lower()
            role = m.group(2).strip().lower()
            if company and role and company != "company":
                seen.add(f"{company}::{role}")
    return seen

# ── Writers ──────────────────────────────────────────────────────────────────

def append_to_pipeline(offers):
    if not offers:
        return
    PIPELINE_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not PIPELINE_PATH.exists():
        PIPELINE_PATH.write_text("# Pipeline\n\n## Pending\n\n")
    text = PIPELINE_PATH.read_text()
    marker = "## Pending"
    idx = text.find(marker)
    block = "\n".join(f"- [ ] {o['url']} | {o['company']} | {o['title']}" for o in offers)
    if idx == -1:
        text = text + f"\n{marker}\n\n{block}\n"
    else:
        after = idx + len(marker)
        next_sec = text.find("\n## ", after)
        insert_at = len(text) if next_sec == -1 else next_sec
        text = text[:insert_at] + "\n" + block + "\n" + text[insert_at:]
    PIPELINE_PATH.write_text(text)


def append_to_scan_history(offers, today, status="added"):
    SCAN_HISTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    if not SCAN_HISTORY_PATH.exists():
        SCAN_HISTORY_PATH.write_text("url\tfirst_seen\tportal\ttitle\tcompany\tstatus\tlocation\n")
    with open(SCAN_HISTORY_PATH, "a") as f:
        for o in offers:
            f.write(f"{o['url']}\t{today}\t{o.get('source','')}\t{o['title']}\t{o['company']}\t{status}\t{o.get('location','')}\n")

# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Portal scanner")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--company", type=str, default=None)
    args = parser.parse_args()

    if not PORTALS_PATH.exists():
        print("Error: portals.yml not found. Run onboarding first.")
        sys.exit(1)

    config = yaml.safe_load(PORTALS_PATH.read_text())
    companies = config.get("tracked_companies", [])
    title_filter = build_title_filter(config.get("title_filter"))
    location_filter = build_location_filter(config.get("location_filter"))

    seen_urls = load_seen_urls()
    seen_company_roles = load_seen_company_roles()
    today = date.today().isoformat()

    targets = []
    skipped = 0
    for company in companies:
        if company.get("enabled") is False:
            continue
        if not isinstance(company.get("name"), str):
            continue
        if args.company and args.company.lower() not in company["name"].lower():
            continue
        provider = detect_provider(company)
        if provider:
            targets.append({**company, "_provider": provider})
        else:
            skipped += 1

    print(f"Scanning {len(targets)} companies ({skipped} skipped - no provider matched)")
    if args.dry_run:
        print("(dry run - no files will be written)\n")

    total_found = total_title_filtered = total_location_filtered = total_dupes = 0
    new_offers = []
    errors = []

    for company in targets:
        provider_name = company["_provider"]
        fetch_fn = PROVIDERS[provider_name][0]
        try:
            jobs = fetch_fn(company)
            total_found += len(jobs)
            for job in jobs:
                if not title_filter(job["title"]):
                    total_title_filtered += 1
                    continue
                if not location_filter(job.get("location", "")):
                    total_location_filtered += 1
                    continue
                if job["url"] in seen_urls:
                    total_dupes += 1
                    continue
                key = f"{job['company'].lower()}::{job['title'].lower()}"
                if key in seen_company_roles:
                    total_dupes += 1
                    continue
                seen_urls.add(job["url"])
                seen_company_roles.add(key)
                new_offers.append({**job, "source": f"{provider_name}-api"})
        except Exception as e:
            errors.append({"company": company["name"], "error": str(e)})

    if not args.dry_run and new_offers:
        append_to_pipeline(new_offers)
        append_to_scan_history(new_offers, today)

    # Summary
    print(f"\n{'━' * 45}")
    print(f"Portal Scan - {today}")
    print(f"{'━' * 45}")
    print(f"Companies scanned:    {len(targets)}")
    print(f"Total jobs found:     {total_found}")
    print(f"Filtered by title:    {total_title_filtered} removed")
    print(f"Filtered by location: {total_location_filtered} removed")
    print(f"Duplicates:           {total_dupes} skipped")
    print(f"New offers added:     {len(new_offers)}")

    if errors:
        print(f"\nErrors ({len(errors)}):")
        for e in errors:
            print(f"  x {e['company']}: {e['error']}")

    if new_offers:
        print("\nNew offers:")
        for o in new_offers:
            print(f"  + {o['company']} | {o['title']} | {o.get('location', 'N/A')}")
        if args.dry_run:
            print("\n(dry run - run without --dry-run to save results)")
        else:
            print(f"\nResults saved to {PIPELINE_PATH} and {SCAN_HISTORY_PATH}")

    print("\n-> Run the pipeline mode to evaluate new offers.")


if __name__ == "__main__":
    main()
