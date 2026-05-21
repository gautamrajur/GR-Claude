"""
WebBridge helpers for linkedin-outreach agent.
Load at the top of every bash block:
    exec(open(os.path.expanduser("~/projects/GR-Claude/plugins/gr-networking/agents/linkedin-outreach/scripts/helpers.py")).read())
"""
import subprocess, json, base64, time, os
from datetime import datetime

SESSION       = "linkedin-outreach"
AGENT_VERSION = "1.0.0"
LOG_PATH      = os.path.expanduser("~/.claude/logs/linkedin-outreach-runs.jsonl")
AGENT_PATH    = os.path.expanduser("~/projects/GR-Claude/plugins/gr-networking/agents/linkedin-outreach/linkedin-outreach.md")
GR_CLAUDE_DIR = os.path.expanduser("~/projects/GR-Claude")
SCRIPTS_DIR   = os.path.dirname(os.path.abspath(__file__))

os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)


def wb(payload):
    payload["session"] = SESSION
    r = subprocess.run(
        ["curl", "-s", "-X", "POST", "http://127.0.0.1:10086/command",
         "-H", "Content-Type: application/json",
         "--data-binary", json.dumps(payload)],
        capture_output=True, text=True)
    return json.loads(r.stdout)


def screenshot(label):
    r = wb({"action": "screenshot"})
    path = f"/tmp/lo_{label}.png"
    with open(path, "wb") as f:
        f.write(base64.b64decode(r["data"]["data"]))
    return path  # Read this path after every call to visually confirm


def snapshot():
    return wb({"action": "snapshot"})["data"]["tree"]


def find_ref(node, role_frag="", name_frag=""):
    """Recursively search accessibility tree for the first ref matching role + name."""
    if isinstance(node, dict):
        role = node.get("role", "")
        name = node.get("name", "")
        ref  = node.get("ref", "")
        if ref:
            role_ok = (not role_frag) or (role_frag.lower() in role.lower())
            name_ok = (not name_frag) or (name_frag.lower() in name.lower())
            if role_ok and name_ok:
                return ref
        for c in node.get("children", []):
            found = find_ref(c, role_frag, name_frag)
            if found:
                return found
    elif isinstance(node, list):
        for item in node:
            found = find_ref(item, role_frag, name_frag)
            if found:
                return found
    return None


def click(ref):
    return wb({"action": "click", "args": {"selector": ref}})


def evaluate(code):
    return wb({"action": "evaluate", "args": {"code": code}})


def fill_shadow_textarea(msg):
    """
    LinkedIn's note textarea lives inside a shadow DOM - querySelector misses it.
    composed:true on InputEvent is required to cross the shadow boundary.
    Returns 'filled:NNN' on success or 'not found' on failure.
    """
    js = f"""
(function() {{
  for (var el of document.querySelectorAll('*')) {{
    if (el.shadowRoot) {{
      var ta = el.shadowRoot.querySelector('textarea');
      if (ta) {{
        ta.focus();
        Object.getOwnPropertyDescriptor(
          window.HTMLTextAreaElement.prototype, 'value').set.call(ta, {json.dumps(msg)});
        ta.dispatchEvent(new InputEvent('input', {{
          bubbles: true, composed: true,
          data: {json.dumps(msg)}, inputType: 'insertText'
        }}));
        ta.dispatchEvent(new Event('change', {{bubbles: true, composed: true}}));
        return 'filled:' + ta.value.length;
      }}
    }}
  }}
  return 'not found';
}})()
"""
    return evaluate(js).get("data", {}).get("value", "err")


def log_run(profile_name, profile_url, technique, chars, result,
            error=None, step_failed=None):
    """Append one JSONL entry after every profile attempt (success or failure)."""
    entry = {
        "timestamp":     datetime.utcnow().isoformat() + "Z",
        "agent_version": AGENT_VERSION,
        "profile_name":  profile_name,
        "profile_url":   profile_url,
        "technique":     technique,    # "invite_link" | "connect_button" | "more_menu"
        "fill_method":   "shadow_dom",
        "chars_written": chars,
        "result":        result,       # "sent" | "failed" | "skipped" | "pending"
        "error":         error,
        "step_failed":   step_failed,  # "navigate" | "find_connect" | "dialog" | "fill" | "send"
    }
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(entry) + "\n")


def analyze_recent_failures(window=10, threshold=3):
    """
    Returns (failure_count, culprit_step) if failures >= threshold, else (0, None).
    Caller uses this to decide whether to trigger self-improvement.
    """
    if not os.path.exists(LOG_PATH):
        return 0, None
    with open(LOG_PATH) as f:
        lines = [l.strip() for l in f if l.strip()]
    recent = [json.loads(l) for l in lines[-window:]]
    fails  = [r for r in recent if r["result"] == "failed"]
    if len(fails) < threshold:
        return 0, None
    steps   = [r["step_failed"] for r in fails if r.get("step_failed")]
    culprit = max(set(steps), key=steps.count) if steps else "unknown"
    return len(fails), culprit
