# LinkedIn Post Skill Setup

Configure this file once. Claude will use it every time you run `/linkedin-post`.

## Your Persona
Describe who you are professionally — Claude uses this to write in your voice:
```
persona: |
  [e.g. AI/backend engineer who ships production systems. Confident, direct,
  zero corporate fluff. Speaks like someone who has built things — not someone
  trying to sound impressive.]
```

## Post Structure
Define your preferred post format:
```
structure: |
  [HOOK — ≤ 10 words, punchy. Never start with "I"]

  [BODY — short paragraphs, stacked sentences, specific numbers]
  [Bold key metrics and project names only — not decoration]

  [CLOSING — bold declaration OR forward CTA]

  #Hashtag1 #Hashtag2 #Hashtag3 #Hashtag4
```

## Hook Patterns (use these)
```
hook_patterns:
  - "Contrast triplet: 3 things. 2 outcomes. 1 insight."
  - "Observation + contrast: Most X do Y. We did Z."
  - "Story opener: We built X. Then Y happened."
  - "Direct address: Hello #hiring Managers"
```

## Body Rules
```
body_rules:
  - Short sentences. Fragments are fine. One idea per paragraph.
  - Specific over vague: "2 hours to 5 seconds" not "dramatically faster"
  - Name real people and companies when relevant
  - Show impact, not just the action
```

## Closing Patterns
```
closing_patterns:
  - Bold forward statement
  - Direct CTA with contact info
  - Emotional 1-liner for shoutouts
  - Philosophical close
```

## Banned Phrases (never use these)
```
banned:
  - excited to share
  - thrilled to announce
  - journey
  - passionate about
  - humbled
  - honored
  - synergy
  - leverage
  - utilize
  - game-changer
  - disrupting
  - I'm proud to
```

## Post Types
Define your recurring post formats:
```
post_types:
  job_search: "Direct address hook → bold metrics from past work → availability → CTA with email"
  project: "Story opener → bold product name + value prop → honest reflection → bold forward close"
  thought_leadership: "Observation hook → specific real-world example → distilled insight → optional link"
  shoutout: "Contrast triplet hook → what they did/said → genuine emotional close"
  achievement: "Result first → context → who else was involved → what's next"
```

## Length & Hashtags
```
length:
  target: 120-180 words
  hard_max: 220 words

hashtags:
  count: 4-8
  avoid: ["#innovation", "#future", "#tech", "#inspiration"]
  prefer: specific and domain-relevant tags
```
