# Splitwise Skill Setup

Configure this file before your first run. Claude will use it every session.

## Your Name (who pays / card holder)
```
payer: Your Name
```

## People You Split With
List everyone you regularly split expenses with:
```
people:
  - Alice
  - Bob
  - Carol
  - Dave
```

## Grouping Patterns
Define your common splitting groups to speed up confirmation.
Claude will pre-suggest these when categorizing expenses.

```
groups:
  - name: "Daily staples duo"
    members: [Your Name, Alice]
    typical_items: "Milk, bread, basic groceries"

  - name: "Cooking group"
    members: [Your Name, Alice, Bob]
    typical_items: "Meat, produce, cooking staples"

  - name: "Full household"
    members: [Your Name, Alice, Bob, Carol, Dave]
    typical_items: "Sugar, shared pantry, household supplies"

  - name: "Solo buyer"
    members: [Bob]
    typical_items: "Bob almost always buys separately"
```

## Personal Expense Categories (never split, never ask)
Add merchant names or keywords that are always personal:
```
always_personal:
  - Claude.AI
  - Anthropic
  - AWS
  - Netflix
  - Spotify
  - Transit (MBTA, Uber, Lyft)
  - Laundry
  - Education fees
```

## Output
Where to save the generated xlsx:
```
output_dir: ~/Downloads
```
