#!/usr/bin/env python3
"""
verify.py - Pipeline integrity checks.
Pure stdlib - no external deps, no venv needed.

Usage:
  python scripts/verify.py
"""
import sys, re
from pathlib import Path

PROJECT_ROOT = Path.cwd()
APPS_FILE = PROJECT_ROOT / "data" / "tracker.md"
ADDITIONS_DIR = PROJECT_ROOT / "batch" / "tracker-additions"
REPORTS_DIR = PROJECT_ROOT / "reports"

CANONICAL_STATUSES = {"evaluated", "applied", "responded", "interview", "offer", "rejected", "discarded", "skip"}
ALIASES = {
    "evaluada", "condicional", "hold", "applied", "sent", "enviada",
    "respondido", "entrevista", "oferta", "rechazado", "rechazada",
    "descartado", "descartada", "cerrada", "no aplicar", "monitor", "geo blocker",
}

errors = 0
warnings = 0


def error(msg):
    global errors
    print(f"X  {msg}")
    errors += 1


def warn(msg):
    global warnings
    print(f"!  {msg}")
    warnings += 1


def ok(msg):
    print(f"OK {msg}")


if not APPS_FILE.exists():
    print("\nNo tracker.md found. Normal for a fresh setup.")
    sys.exit(0)

content = APPS_FILE.read_text()
lines = content.split("\n")

entries = []
for line in lines:
    if not line.startswith("|"):
        continue
    parts = [p.strip() for p in line.split("|")]
    if len(parts) < 9:
        continue
    try:
        num = int(parts[1])
    except ValueError:
        continue
    entries.append({
        "num": num, "date": parts[2], "company": parts[3], "role": parts[4],
        "score": parts[5], "status": parts[6], "pdf": parts[7], "report": parts[8],
        "notes": parts[9] if len(parts) > 9 else "",
    })

print(f"\nChecking {len(entries)} entries in tracker.md\n")

# Check 1: Canonical statuses
bad = 0
for e in entries:
    clean = re.sub(r"\*\*", "", e["status"]).strip()
    clean = re.sub(r"\s+\d{4}-\d{2}-\d{2}.*$", "", clean).strip().lower()
    if clean not in CANONICAL_STATUSES and clean not in ALIASES:
        error(f"#{e['num']}: Non-canonical status \"{e['status']}\"")
        bad += 1
    if "**" in e["status"]:
        error(f"#{e['num']}: Status contains markdown bold: \"{e['status']}\"")
        bad += 1
    if re.search(r"\d{4}-\d{2}-\d{2}", e["status"]):
        error(f"#{e['num']}: Status contains date: \"{e['status']}\"")
        bad += 1
if bad == 0:
    ok("All statuses are canonical")

# Check 2: No exact duplicates
company_role_map = {}
dupes = 0
for e in entries:
    key = re.sub(r"[^a-z0-9]", "", e["company"].lower()) + "::" + re.sub(r"[^a-z0-9 ]", "", e["role"].lower())
    company_role_map.setdefault(key, []).append(e)
for key, group in company_role_map.items():
    if len(group) > 1:
        nums = ", ".join(f"#{e['num']}" for e in group)
        warn(f"Possible duplicates: {nums} ({group[0]['company']} - {group[0]['role']})")
        dupes += 1
if dupes == 0:
    ok("No exact duplicates found")

# Check 3: Report links valid
broken = 0
for e in entries:
    m = re.search(r"\]\(([^)]+)\)", e["report"])
    if not m:
        continue
    report_path = PROJECT_ROOT / m.group(1)
    if not report_path.exists():
        error(f"#{e['num']}: Report not found: {m.group(1)}")
        broken += 1
if broken == 0:
    ok("All report links valid")

# Check 4: Score format
bad_scores = 0
for e in entries:
    s = re.sub(r"\*\*", "", e["score"]).strip()
    if not re.match(r"^\d+\.?\d*/5$", s) and s not in ("N/A", "DUP"):
        error(f"#{e['num']}: Invalid score format: \"{e['score']}\"")
        bad_scores += 1
if bad_scores == 0:
    ok("All scores valid")

# Check 5: Row format
bad_rows = 0
for line in lines:
    if not line.startswith("|"):
        continue
    if "---" in line or "Company" in line:
        continue
    if len(line.split("|")) < 9:
        error(f"Row with <9 columns: {line[:80]}...")
        bad_rows += 1
if bad_rows == 0:
    ok("All rows properly formatted")

# Check 6: No pending TSVs
pending = 0
if ADDITIONS_DIR.exists():
    tsv_files = [f for f in ADDITIONS_DIR.iterdir() if f.suffix == ".tsv" and f.is_file()]
    pending = len(tsv_files)
    if pending > 0:
        warn(f"{pending} pending TSVs in tracker-additions/ (not merged)")
if pending == 0:
    ok("No pending TSVs")

# Check 7: No bold in scores
bold_scores = 0
for e in entries:
    if "**" in e["score"]:
        warn(f"#{e['num']}: Score has markdown bold: \"{e['score']}\"")
        bold_scores += 1
if bold_scores == 0:
    ok("No bold in scores")

# Summary
print("\n" + "=" * 50)
print(f"Pipeline Health: {errors} errors, {warnings} warnings")
if errors == 0 and warnings == 0:
    print("Pipeline is clean!")
elif errors == 0:
    print("Pipeline OK with warnings")
else:
    print("Pipeline has errors - fix before proceeding")

sys.exit(1 if errors > 0 else 0)
