---
name: root-cause-analysis
description: Run a structured root cause analysis (5 Whys) on an incident, defect or process failure and produce a report with evidence, root cause, corrective and preventive actions. Use when the user describes something that went wrong and asks why it happened or how to stop it recurring.
---

# Root Cause Analysis (5 Whys)

## When to use
The user describes an incident, error, missed target or recurring problem and wants the underlying cause, not just a fix.

## Inputs to collect first
Ask for anything missing before analysing: what happened, when, impact (who or what was affected, how much), what is already known, and any evidence (logs, numbers, timeline). If the user cannot supply evidence, say so in the report instead of inventing it.

## Method
1. State the problem in one factual sentence: what, where, when, impact. No blame, no cause in the statement.
2. Build a short timeline from the facts given.
3. Ask "why" up to five times. Each answer must be supported by evidence or marked **Assumption**. Stop when the answer is a process, control or design gap that the team can change. If there are several branches, follow each separately.
4. Check the root cause with the reverse test: "If this cause had not existed, would the problem have happened?"
5. Separate actions into **Corrective** (fix this occurrence), **Preventive** (stop it recurring) and **Detective** (notice it sooner). Each action has an owner role and a due date or a placeholder.

## Output format (always use these headings, in this order)
1. `## Problem statement`
2. `## Timeline`
3. `## 5 Whys`  (numbered Why 1 to Why 5, each with Evidence or Assumption)
4. `## Root cause`
5. `## Actions`  (table: Type | Action | Owner | Due)
6. `## Open questions`

## Rules
- Never name a person as the root cause. Root causes are about process, controls, tools or information.
- Label every unsupported statement as **Assumption**.
- Do not stop at "human error"; ask why the process allowed it.
- Keep the report to one page unless the user asks for more.
