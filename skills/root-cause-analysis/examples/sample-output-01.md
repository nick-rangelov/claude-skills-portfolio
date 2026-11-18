## Problem statement
The weekly customer export on Friday contained 312 duplicate rows, and three customers received two invoices.

## Timeline
- Wednesday: export script changed to add a new column.
- Friday: export ran and sent with duplicates.
- Friday: a customer reported the duplicate invoice.

## 5 Whys
1. Why were invoices duplicated? The export contained duplicate rows. Evidence: 312 duplicate rows in the file.
2. Why were there duplicate rows? The new column caused a join to return several rows per customer. Assumption: needs checking in the script.
3. Why was the join change not caught? The change was not tested against real data volumes. Assumption.
4. Why was it not tested? There is no test or row-count check for the export. Evidence: stated by the team.
5. Why is there no check? Export changes follow no review or release checklist. Assumption.

## Root cause
The export process has no automated validation or change checklist, so a join change could release duplicates unnoticed.

## Actions
| Type | Action | Owner | Due |
|---|---|---|---|
| Corrective | Send corrected invoices and credit duplicates | Finance operations | TBD |
| Preventive | Add a uniqueness check on customer ID before sending | Data owner | TBD |
| Preventive | Add a pre-release checklist for export script changes | Team lead | TBD |
| Detective | Alert when row count differs from the previous run by more than 5% | Data owner | TBD |

## Open questions
- Which exact join produced the duplicates?
- Were other exports changed on Wednesday?
