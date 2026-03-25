---
name: splitwise
description: Analyze credit card statements, receipts (PDF, screenshots, photos), and expense data to categorize transactions as personal vs shared, calculate per-person splits, and generate a Splitwise-ready xlsx spreadsheet. Trigger when the user shares bills, credit card statements, or receipts, or asks to split expenses, calculate who owes what, or prepare Splitwise entries. Also trigger on /splitwise.
---

# Splitwise Expense Analyzer

Parse bills and receipts, confirm splits with the user, and generate a Splitwise-ready xlsx.

## First Run Setup

Read [references/setup.md](references/setup.md). If the user hasn't filled it in yet, show them the file and ask them to configure:
- Their name (payer)
- List of people they split with
- Grouping patterns
- Personal expense keywords
- Output directory

Do not proceed until setup is complete.

## Workflow

### 1. Gather Sources
Read all provided sources — PDF statements, app screenshots, receipt photos. Extract every transaction: date, merchant, amount.

### 2. Combine & Deduplicate
Merge across sources. Watch for overlapping date ranges. Flag duplicates for user confirmation.

### 3. Categorize Transactions
Present a full transaction list and sort into:
- **Shared** — groceries, household items, dining out, bulk purchases
- **Personal** — anything matching `always_personal` in setup.md, or clearly solo (subscriptions, transit, laundry, interest charges)
- **Already on Splitwise** — user flags these; skip from new entries
- **TBD** — user will confirm later

Use grouping patterns from setup.md to **pre-suggest** splits. Always confirm before finalizing.

### 4. Item-Level Splits
For shared transactions, break down by item when receipt data is available:
- Different items in the same receipt can have different split groups
- Present as a table: Item | Price | Shared With | Per Person
- Suggest likely group based on setup.md patterns

### 5. Confirm Everything
Before generating xlsx, show:
- Full per-transaction breakdown
- Per-person running total
- Any TBD items still pending

### 6. Generate XLSX
Build a JSON payload and pipe to `scripts/generate_splitwise_xlsx.py`:

```bash
echo '<json>' | python3 scripts/generate_splitwise_xlsx.py
```

**JSON schema:**
```json
{
  "output_path": "~/Downloads/Splitwise_YYYY-MM.xlsx",
  "payer": "Your Name",
  "roommates": ["Your Name", "Alice", "Bob", "Carol", "Dave"],
  "splitwise_entries": [
    {
      "date": "03/17",
      "merchant": "Trader Joe's",
      "item": "Eggs",
      "price": 8.97,
      "split_between": "You, Alice, Bob",
      "per_person": 2.99,
      "owes": { "Alice": 2.99, "Bob": 2.99 },
      "payer_share": 2.99
    }
  ],
  "person_summary": [
    { "name": "Alice", "breakdown": "Eggs $2.99 + ...", "status": "Pending" }
  ],
  "already_on_splitwise": [
    { "date": "02/24", "merchant": "Costco", "amount": 38.34 }
  ],
  "personal_expenses": [
    { "date": "02/10", "merchant": "Netflix", "amount": 15.99, "category": "Subscription" }
  ],
  "tbd": [
    { "date": "02/05", "merchant": "Star Market", "amount": 1.35 }
  ],
  "datewise_transactions": [
    {
      "date": "03/17/2026",
      "merchant": "Trader Joe's",
      "bill_total": 31.23,
      "paid_by": "Your Name",
      "items": [
        { "name": "Eggs", "price": 8.97, "shared_with": "You, Alice, Bob", "per_person": 2.99 }
      ]
    }
  ]
}
```

The xlsx has 6 sheets:
1. **Splitwise Entries** — all line items, per-person owes columns, SUM formulas
2. **Per Person Summary** — who owes how much with breakdown text
3. **Already on Splitwise** — skipped transactions
4. **Personal Expenses** — solo spending
5. **TBD - Pending** — unconfirmed items
6. **Date-wise for Splitwise** — screenshot-friendly mini-table per transaction (self-contained blocks separated by blank rows, ideal for screenshotting into Splitwise)

## Key Behaviors
- Never assume everyone shares every expense — confirm per item
- Use grouping patterns from setup.md to pre-suggest, not decide
- Split at item level when receipt data is available
- Exclude "Already on Splitwise" items from the date-wise sheet
- Show running per-person totals throughout confirmation
