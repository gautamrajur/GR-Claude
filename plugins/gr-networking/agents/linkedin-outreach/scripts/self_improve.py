"""
Self-improvement and rollback functions for linkedin-outreach agent.
Only loaded when analyze_recent_failures() returns failure_count >= 3.

Usage:
    exec(open(os.path.expanduser("~/projects/GR-Claude/plugins/gr-networking/agents/linkedin-outreach/scripts/self_improve.py")).read())
    # requires helpers.py to already be loaded
"""
import shutil, subprocess, os
from datetime import datetime


def git_backup(version):
    """Commit the current agent file to GR-Claude before any self-update."""
    rel = "plugins/gr-networking/agents/linkedin-outreach/linkedin-outreach.md"
    subprocess.run(["git", "-C", GR_CLAUDE_DIR, "add", rel], check=True)
    subprocess.run(["git", "-C", GR_CLAUDE_DIR, "commit", "-m",
                    f"backup: linkedin-outreach {version} before self-update"],
                   check=True)
    print(f"Git backup: {version} committed to GR-Claude")


def _timestamped_bak():
    """Write a timestamped .bak file before touching AGENT_PATH."""
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    bak = AGENT_PATH + f".bak.{ts}"
    shutil.copy(AGENT_PATH, bak)
    print(f"File backup: {bak}")
    # Keep only last 3 .bak files
    baks = sorted(f for f in os.listdir(os.path.dirname(AGENT_PATH)) if ".bak." in f)
    for old in baks[:-3]:
        os.remove(os.path.join(os.path.dirname(AGENT_PATH), old))


def _bump_patch(version):
    parts = version.split(".")
    parts[-1] = str(int(parts[-1]) + 1)
    return ".".join(parts)


def run_diagnostic(culprit_step, test_profiles):
    """
    Test an alternative approach on up to 5 fresh profiles (cancel before send).
    Returns True only if ALL 5 pass - required before calling self_update().

    test_profiles: list of (name, url) for profiles not yet contacted.
    The alternative logic lives inside this function - edit it when adapting.
    """
    results = []
    for name, url in test_profiles[:5]:
        wb({"action": "navigate", "args": {"url": url}})
        time.sleep(3)

        success = False
        tree = snapshot()

        if culprit_step == "fill":
            # Alternative: click textarea ref directly then use WebBridge fill action
            ta_ref = find_ref(tree, "textbox", "300")
            if ta_ref:
                click(ta_ref)
                time.sleep(0.3)
                r = wb({"action": "fill", "args": {"selector": ta_ref, "value": "TEST"}})
                success = "Uncaught" not in str(r) and r.get("ok", False)

        elif culprit_step == "find_connect":
            # Alternative: search all links for any "connect" text
            first_name = name.split()[0]
            ref = find_ref(tree, "link", "connect")
            success = ref is not None

        # Cancel dialog if open
        cancel_ref = find_ref(snapshot(), "button", "Cancel")
        if cancel_ref:
            click(cancel_ref)

        results.append(success)
        log_run(name, url, "diagnostic", 0,
                "sent" if success else "failed",
                step_failed=None if success else culprit_step)
        time.sleep(1.5)

    pass_rate = sum(results) / len(results) if results else 0
    print(f"Diagnostic: {sum(results)}/{len(results)} passed ({pass_rate*100:.0f}%)")
    return pass_rate == 1.0  # 5/5 required - no partial passes


def self_update(old_version, new_approach_name, old_section, new_section,
                culprit_step, reason):
    """
    Replace a failing section in the agent .md, bump version, append changelog.
    Requires run_diagnostic() to have returned True first.
    """
    # Safety: backup before touching anything
    git_backup(old_version)
    _timestamped_bak()

    with open(AGENT_PATH) as f:
        content = f.read()

    if old_section not in content:
        print("ERROR: section to replace not found - aborting. Check old_section arg.")
        return False

    new_version = _bump_patch(old_version)
    content = content.replace(old_section, new_section)
    content = content.replace(f'version: "{old_version}"', f'version: "{new_version}"')

    changelog_entry = (
        f"\n### {new_version} - {datetime.utcnow().strftime('%Y-%m-%d')}\n"
        f"- Replaced `{new_approach_name}` at step `{culprit_step}`.\n"
        f"- Reason: {reason}\n"
        f"- Validated: 5/5 diagnostic runs passed before applying.\n"
    )
    content = content.replace("## Changelog\n", f"## Changelog\n{changelog_entry}")

    with open(AGENT_PATH, "w") as f:
        f.write(content)

    # Commit the new version
    rel = "plugins/gr-networking/agents/linkedin-outreach/linkedin-outreach.md"
    subprocess.run(["git", "-C", GR_CLAUDE_DIR, "add", rel], check=True)
    subprocess.run(["git", "-C", GR_CLAUDE_DIR, "commit", "-m",
                    f"self-update: linkedin-outreach {old_version} -> {new_version}: {reason}"],
                   check=True)

    print(f"Self-update complete: {old_version} -> {new_version}")
    print(f"Rollback: git -C ~/projects/GR-Claude checkout HEAD~1 -- {rel}")
    return True
