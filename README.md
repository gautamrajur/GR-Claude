# GR-Claude

A personal Claude Code marketplace by Gautam Raju — skills and agents for finance, content, and networking.

## Install the Marketplace

```
/plugin marketplace add gautamrajur/GR-Claude
```

## Plugins

### `gr-finance` — Personal Finance
| Skill | Description |
|-------|-------------|
| `splitwise` | Parse bills & receipts, confirm splits, generate Splitwise-ready xlsx |

```
/plugin install gr-finance@gr-claude
```

### `gr-content` — Content Creation
| Skill | Description |
|-------|-------------|
| `linkedin-post` | Write LinkedIn posts in your personal voice — configure once, use forever |

```
/plugin install gr-content@gr-claude
```

### `gr-networking` — Networking & Outreach
| Agent | Description |
|-------|-------------|
| `linkedin-outreach` | Send personalized LinkedIn connection requests with notes via Kimi WebBridge browser automation |

```
/plugin install gr-networking@gr-claude
```

Requires [Kimi WebBridge](https://www.kimi.com/features/webbridge) running locally (`kimi-webbridge start`).

## Usage

```bash
# Finance
/splitwise           # share a bill or receipt to get started

# Content
/linkedin-post       # provide a topic or context to write a post

# Networking
# "Send connection requests to these 5 profiles: [URLs]"
# — the linkedin-outreach agent handles the rest
```

## First Run
Skills require a one-time setup — fill in `references/setup.md` with your personal config (people/groups for splitwise, voice/style for linkedin-post).

The `linkedin-outreach` agent needs no config file — pass your name, context, and profile URLs directly in your message.
