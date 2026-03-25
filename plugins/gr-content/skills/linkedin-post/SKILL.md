---
name: linkedin-post
description: Write a LinkedIn post in the user's personal voice. Trigger on /linkedin-post or when the user asks to write, draft, or create a LinkedIn post, announcement, shoutout, job search post, or thought leadership piece.
---

# LinkedIn Post Writer

Write LinkedIn posts in the user's configured voice — direct, data-driven, no corporate fluff.

## First Run Setup

Read [references/setup.md](references/setup.md). If the user hasn't filled it in yet, show them the template and ask them to configure:
- Their persona / professional voice
- Banned phrases
- Post types they use
- Hook and closing patterns

Do not write a post until setup is complete.

## Workflow

### 1. Understand the Request
Accept the post topic/context from `$ARGUMENTS` or from the conversation. Identify the post type from setup.md (job search, project, thought leadership, shoutout, achievement, or other).

### 2. Write the Post
Using the user's configured voice from setup.md:
- Apply the correct hook pattern for the post type
- Follow body rules (short sentences, specific numbers, bold only key phrases)
- Use the appropriate closing pattern
- Stay within target word count
- End with hashtags on their own line

### 3. Self-Check Before Presenting
Run through this checklist silently — only present the post if it passes:
- [ ] Hook ≤ 10 words and doesn't start with "I"?
- [ ] At least one concrete number or specific detail?
- [ ] Bold on 1–3 key phrases max?
- [ ] Zero banned phrases?
- [ ] Closing is a declaration, CTA, or genuine emotion?
- [ ] Correct number of hashtags on their own line?
- [ ] Within word count limits?

### 4. Present & Iterate
- Present the post **ready to copy-paste** with no preamble
- Offer exactly **one round of iteration** — ask if they want any changes
- Apply requested changes and present the final version

## Key Behaviors
- Never use banned phrases from setup.md
- Specific always beats vague — push back if the user's brief is too generic
- If the user gives raw content (article, notes, achievements), extract the sharpest angle and build the hook around it
- Bold is for metrics and key terms only — never decorative
