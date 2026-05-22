#!/usr/bin/env python3
"""
merge_tracker.py - Merge batch tracker additions into tracker.md
Pure stdlib - no external deps, no venv needed.

Usage:
  python scripts/merge_tracker.py [--dry-run]
"""
import sys, os, re, csv, shutil
from pathlib import Path

PROJECT_ROOT = Path.cwd()
APPS_FILE = PROJECT_ROOT / "data" / "tracker.md"
ADDITIONS_DIR = PROJECT_ROOT / "batch" / "tracker-additions"
MERGED_DIR = ADDITIONS_DIR / "merged"
DRY_RUN = "--dry-run" in sys.argv

CANONICAL_STATES = ["Evaluated", "Applied", "Responded", "Interview", "Offer", "Rejected", "Discarded", "SKIP"]
ALIASES = {
    "evaluada": "Evaluated", "condicional": "Evaluated", "hold": "Evaluated",
    "applied": "Applied", "sent": "Applied", "enviada": "Applied",
    "respondido": "Responded",
    "entrevista": "Interview",
    "oferta": "Offer",
    "rechazado": "Rejected", "rechazada": "Rejected",
    "descartado": "Discarded", "descartada": "Discarded", "cerrada": "Discarded",
    "no aplicar": "SKIP", "skip": "SKIP", "monitor": "SKIP",
}

ROLE_STOPWORDS = {
    "junior", "mid", "senior", "staff", "principal", "lead", "head",
    "remote", "hybrid", "onsite", "contract", "fulltime", "parttime",
    "role", "position", "with", "from", "into", "over", "this", "that",
}
SHORT_SPECIALTY = {"api", "sre", "sdk", "cli", "gpu", "cpu", "ios", "qa", "ux", "ui"}
BASELINE_TOKENS = {
    "software", "engineer", "developer", "manager", "architect",
    "analyst", "designer", "platform", "systems", "backend", "frontend",
}


def validate_status(status):
    clean = re.sub(r"\*\*", "", status).strip()
    clean = re.sub(r"\s+\d{4}-\d{2}-\d{2}.*$", "", clean).strip()
    lower = clean.lower()
    for s in CANONICAL_STATES:
        if s.lower() == lower:
            return s
    if lower in ALIASES:
        return ALIASES[lower]
    if re.match(r"^(duplicado|dup|repost)", lower):
        return "Discarded"
    print(f"WARNING: Non-canonical status '{status}' -> defaulting to Evaluated")
    return "Evaluated"


def normalize_company(name):
    return re.sub(r"[^a-z0-9]", "", name.lower())


def role_tokens(s):
    words = re.sub(r"[^a-z0-9\s]", " ", s.lower()).split()
    return [w for w in words if (len(w) > 3 or w in SHORT_SPECIALTY) and w not in ROLE_STOPWORDS]


def role_fuzzy_match(a, b):
    words_a = role_tokens(a)
    words_b = role_tokens(b)
    if not words_a or not words_b:
        return False
    set_b = set(words_b)
    overlap = [w for w in words_a if w in set_b]
    if len(overlap) < 2:
        return False
    discriminating = [w for w in overlap if w not in BASELINE_TOKENS]
    if not discriminating:
        return False
    min_len = min(len(words_a), len(words_b))
    return len(overlap) / min_len >= 0.6


def extract_report_num(report_str):
    m = re.search(r"\[(\d+)\]", report_str)
    return int(m.group(1)) if m else None


def parse_score(s):
    s = re.sub(r"\*\*", "", s)
    m = re.search(r"([\d.]+)", s)
    return float(m.group(1)) if m else 0.0


def parse_app_line(line):
    parts = [p.strip() for p in line.split("|")]
    if len(parts) < 9:
        return None
    try:
        num = int(parts[1])
    except ValueError:
        return None
    if num == 0:
        return None
    return {
        "num": num, "date": parts[2], "company": parts[3], "role": parts[4],
        "score": parts[5], "status": parts[6], "pdf": parts[7], "report": parts[8],
        "notes": parts[9] if len(parts) > 9 else "", "raw": line,
    }


def parse_tsv_content(content, filename):
    content = content.strip()
    if not content:
        return None

    # Pipe-delimited markdown table row
    if content.startswith("|"):
        parts = [p.strip() for p in content.split("|") if p.strip()]
        if len(parts) < 8:
            print(f"WARNING: Skipping malformed pipe-delimited {filename}: {len(parts)} fields")
            return None
        return {
            "num": int(parts[0]) if parts[0].isdigit() else 0,
            "date": parts[1], "company": parts[2], "role": parts[3],
            "score": parts[4], "status": validate_status(parts[5]),
            "pdf": parts[6], "report": parts[7], "notes": parts[8] if len(parts) > 8 else "",
        }

    # Tab-separated
    parts = content.split("\t")
    if len(parts) < 8:
        print(f"WARNING: Skipping malformed TSV {filename}: {len(parts)} fields")
        return None

    col4, col5 = parts[4].strip(), parts[5].strip()
    score_re = re.compile(r"^\d+\.?\d*/5$")
    status_re = re.compile(
        r"^(evaluated|applied|responded|interview|offer|rejected|discarded|skip|evaluada|aplicado"
        r"|respondido|entrevista|oferta|rechazado|descartado|no aplicar|cerrada|duplicado|repost"
        r"|condicional|hold|monitor)", re.IGNORECASE
    )

    col4_is_score = bool(score_re.match(col4)) or col4 in ("N/A", "DUP")
    col5_is_status = bool(status_re.match(col5))
    col4_is_status = bool(status_re.match(col4))

    if col4_is_score and col5_is_status:
        status_col, score_col = col5, col4
    elif col4_is_status:
        status_col, score_col = col4, col5
    else:
        status_col, score_col = col4, col5  # default

    try:
        num = int(parts[0])
    except (ValueError, IndexError):
        num = 0

    return {
        "num": num, "date": parts[1], "company": parts[2], "role": parts[3],
        "status": validate_status(status_col), "score": score_col,
        "pdf": parts[6] if len(parts) > 6 else "❌",
        "report": parts[7] if len(parts) > 7 else "",
        "notes": parts[8] if len(parts) > 8 else "",
    }


def main():
    if not APPS_FILE.exists():
        print("No tracker.md found. Nothing to merge into.")
        sys.exit(0)

    app_content = APPS_FILE.read_text()
    app_lines = app_content.split("\n")
    existing = []
    max_num = 0

    for line in app_lines:
        if line.startswith("|") and "---" not in line and "Company" not in line:
            app = parse_app_line(line)
            if app:
                existing.append(app)
                if app["num"] > max_num:
                    max_num = app["num"]

    print(f"Existing: {len(existing)} entries, max #{max_num}")

    ADDITIONS_DIR.mkdir(parents=True, exist_ok=True)
    tsv_files = sorted([f for f in ADDITIONS_DIR.iterdir() if f.suffix == ".tsv" and f.is_file()])

    if not tsv_files:
        print("No pending additions to merge.")
        sys.exit(0)

    print(f"Found {len(tsv_files)} pending additions")

    added = updated = skipped = 0
    new_lines = []

    for tsv_path in tsv_files:
        content = tsv_path.read_text().strip()
        addition = parse_tsv_content(content, tsv_path.name)
        if not addition or addition["num"] == 0:
            skipped += 1
            continue

        report_num = extract_report_num(addition["report"])
        duplicate = None

        # Match by report number
        if report_num:
            duplicate = next((a for a in existing if extract_report_num(a["report"]) == report_num), None)
        # Match by exact entry number
        if not duplicate:
            duplicate = next((a for a in existing if a["num"] == addition["num"]), None)
        # Match by company + role fuzzy
        if not duplicate:
            norm_co = normalize_company(addition["company"])
            duplicate = next(
                (a for a in existing
                 if normalize_company(a["company"]) == norm_co and role_fuzzy_match(addition["role"], a["role"])),
                None
            )

        if duplicate:
            new_score = parse_score(addition["score"])
            old_score = parse_score(duplicate["score"])
            if new_score > old_score:
                print(f"Update: #{duplicate['num']} {addition['company']} - {addition['role']} ({old_score}->{new_score})")
                for i, line in enumerate(app_lines):
                    if line == duplicate["raw"]:
                        app_lines[i] = (
                            f"| {duplicate['num']} | {addition['date']} | {addition['company']} | "
                            f"{addition['role']} | {addition['score']} | {duplicate['status']} | "
                            f"{duplicate['pdf']} | {addition['report']} | "
                            f"Re-eval {addition['date']} ({old_score}->{new_score}). {addition['notes']} |"
                        )
                        updated += 1
                        break
            else:
                print(f"Skip: {addition['company']} - {addition['role']} (existing #{duplicate['num']} {old_score} >= {new_score})")
                skipped += 1
        else:
            entry_num = max(addition["num"], max_num + 1)
            if addition["num"] > max_num:
                max_num = addition["num"]
            else:
                max_num = entry_num
            new_line = (
                f"| {entry_num} | {addition['date']} | {addition['company']} | "
                f"{addition['role']} | {addition['score']} | {addition['status']} | "
                f"{addition['pdf']} | {addition['report']} | {addition['notes']} |"
            )
            new_lines.append(new_line)
            added += 1
            print(f"Add #{entry_num}: {addition['company']} - {addition['role']} ({addition['score']})")

    if new_lines:
        insert_idx = -1
        for i, line in enumerate(app_lines):
            if "|---" in line and line.startswith("|"):
                insert_idx = i + 1
                break
        if insert_idx >= 0:
            for j, nl in enumerate(new_lines):
                app_lines.insert(insert_idx + j, nl)

    if not DRY_RUN:
        APPS_FILE.write_text("\n".join(app_lines))
        MERGED_DIR.mkdir(parents=True, exist_ok=True)
        for tsv_path in tsv_files:
            shutil.move(str(tsv_path), str(MERGED_DIR / tsv_path.name))
        print(f"\nMoved {len(tsv_files)} TSVs to merged/")

    print(f"\nSummary: +{added} added, {updated} updated, {skipped} skipped")
    if DRY_RUN:
        print("(dry-run - no changes written)")


if __name__ == "__main__":
    main()
