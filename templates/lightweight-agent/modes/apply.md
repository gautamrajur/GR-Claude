# Apply Mode

Fill out a form or take action on a specific item. Uses kimi-webbridge.

## Prerequisites

- kimi-webbridge running: `~/.kimi-webbridge/bin/kimi-webbridge status`
- Read `~/.claude/knowledge/kimi-webbridge.md` before starting
- If form is on Ashby: also read `~/.claude/knowledge/ashby-forms.md`

## Steps

1. Health-check kimi-webbridge
2. Load relevant knowledge files
3. Navigate to the item URL
4. Snapshot the page to understand the form structure
5. Fill each field. After every dropdown, re-snapshot before continuing.
6. STOP before any final submit/send/confirm action
7. Take a screenshot showing the filled state
8. Ask user: "All fields are filled. Ready to submit? (you'll click Submit)"

## Critical rules

- NEVER click Submit / Send / Apply / Confirm without explicit user approval
- Tell the user which fields need manual input (file uploads, passwords)
- Verify every field Simplify may have auto-filled - it often gets URLs wrong

## Field filling order

1. Text fields (name, email, phone) - fill first, stable refs
2. Location / city combobox - type, wait 1s, snapshot, click first match
3. URL fields (LinkedIn, GitHub) - fill, then verify Simplify didn't overwrite
4. Yes/No / radio buttons - use CSS class selectors via evaluate(), not @e refs
5. File uploads - identify input[type=file] id via evaluate(), tell user to upload manually
6. Text areas / cover letter - fill last

## Per-site patterns

- **Ashby:** Read `~/.claude/knowledge/ashby-forms.md`
- **Greenhouse:** Standard HTML form, @e refs are stable, no Simplify issues typically
- **Lever:** Standard HTML form, similar to Greenhouse
