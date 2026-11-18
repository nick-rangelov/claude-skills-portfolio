---
name: payments-reconciliation-checker
description: Reconcile two lists of payment transactions (for example an internal ledger and a processor or bank report) with the bundled script, then explain every difference. Use when the user provides two CSV files of transactions and asks what matches, what is missing or what differs.
---

# Payments Reconciliation Checker

## When to use
The user has two transaction lists (CSV) and wants to know which items match, which exist on only one side, and which differ in amount or currency.

## Inputs
Two CSV files with columns `id`, `amount`, `currency` (extra columns are ignored). Ask the user which file is the ledger (side A) and which is the processor or bank (side B). If column names differ, map them before running.

## Steps
1. Run the script:
   `python scripts/reconcile.py <ledger.csv> <processor.csv> --tolerance 0.00`
   It prints JSON with `matched`, `missing_in_b`, `missing_in_a`, `amount_mismatches`, `currency_mismatches`, `duplicates_a` and `duplicates_b`.
2. Do not recalculate the numbers yourself. Use the script output as the source of truth.
3. Write a short explanation per category: the count, the total amount involved and the likely reasons to check. Mark likely reasons as **Hypothesis**.
4. Recommend a next step for each exception (investigate, request a refund report, correct the ledger).

## Output format (always use these headings, in this order)
1. `## Summary`  (counts and total value matched vs unmatched)
2. `## Exceptions`  (one subsection per non-empty category)
3. `## Hypotheses`
4. `## Next steps`

## Rules
- Never state that two items match without the script confirming it.
- Amounts are compared as decimals, never floats; respect the tolerance the user gives.
- Do not guess reasons as facts. Say "Hypothesis" and what evidence would confirm it.
- Treat the files as confidential; do not paste full rows into summaries beyond the exception ids.
