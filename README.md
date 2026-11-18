# Claude Skills Portfolio

![tests](https://github.com/nick-rangelov/claude-skills-portfolio/actions/workflows/ci.yml/badge.svg)

Three reusable Claude skills for common analyst and operations work, each with a defined output format, rules, example inputs and automated checks.

| Skill | What it does |
|---|---|
| `root-cause-analysis` | 5 Whys analysis that separates evidence from assumptions and ends in corrective, preventive and detective actions |
| `gap-analysis` | Compares a current process with a target standard and returns a prioritised gap table with actions |
| `payments-reconciliation-checker` | Reconciles two transaction CSVs with a tested Python script, then explains the differences |

All examples use invented data. No company or customer information is included.

## How the skills are tested
LLM output is not deterministic, so testing has two layers:

1. **Deterministic tests (this repo, run in CI).**
   - `reconcile.py` has unit tests for matches, missing items, amount and currency mismatches, duplicates, tolerance, decimal precision and bad input.
   - Each skill's `SKILL.md` is checked for valid front matter, an output format and rules.
   - `tests/check_output.py` validates the structure of an output: required headings in order, 3 to 5 whys each labelled Evidence or Assumption, action types present, gap table columns, and summary counts that match the table.
2. **Scenario evaluation (manual or with an eval tool).** `evals/cases.json` lists realistic inputs, expected results and acceptance criteria. Run a skill on each input, score the output against the criteria, record failures and group them by cause, then change the instructions and re-run the same cases.

## Run the tests
```
pip install -r requirements.txt
pytest -q
```

## Use a skill
Copy a folder from `skills/` into your Claude skills directory (for example `.claude/skills/` for Claude Code), then ask Claude for the task, for example: "Run a root cause analysis on this incident: ...".

## Known limits
- The rule-based checker tests structure, not the quality of reasoning. Quality is judged against the criteria in `evals/cases.json`.
- Reconciliation matches by `id` only and expects columns `id`, `amount`, `currency`.
