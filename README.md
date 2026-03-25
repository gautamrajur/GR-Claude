# GR-Claude

A personal Claude Code marketplace by Gautam Raju.

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

## Usage

```bash
# Finance
/splitwise        # share a bill or receipt to get started

# Content
/linkedin-post    # provide a topic or context to write a post
```

## First Run
Both skills require a one-time setup — fill in `references/setup.md` with your personal config (people/groups for splitwise, voice/style for linkedin-post).
