---
name: gap-analysis
description: Compare a current process, capability or control set against a target standard and produce a prioritised gap analysis with recommended actions. Use when the user asks for a gap analysis, a process review against a policy or standard, or a list of improvements needed to reach a target state.
---

# Gap Analysis

## When to use
The user supplies (or can describe) a current state and a target state: a policy, regulation, internal standard, best-practice checklist or a desired outcome.

## Inputs to collect first
Current state (how it works today), target state (the standard or goal) and scope. If the target is vague, propose a short list of criteria and ask the user to confirm before analysing.

## Method
1. Break the target into discrete, checkable requirements.
2. For each requirement record the current state with evidence, or write "No evidence provided".
3. Rate the gap: **None**, **Minor**, **Major** or **Unknown** (when evidence is missing).
4. Rate priority from impact (risk, cost, customer effect) and effort: **High**, **Medium**, **Low**.
5. Propose one concrete action per Major or Minor gap, with an owner role.
6. Summarise: counts of each gap level and the top three actions.

## Output format (always use these headings, in this order)
1. `## Scope and target`
2. `## Gap table`  (columns: Requirement | Current state | Gap | Priority | Action)
3. `## Summary`  (counts per gap level, top three actions)
4. `## Assumptions and open questions`

## Rules
- Never mark a requirement as met without evidence; use Unknown instead.
- One action per row, starting with a verb, small enough to assign to one owner.
- Do not invent regulations or standards. Use only the target the user supplies, or clearly label suggested criteria as suggested.
