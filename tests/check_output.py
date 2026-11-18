"""Rule-based checks for skill outputs (the deterministic part of the evals)."""
import re

RCA_HEADINGS = ["Problem statement", "Timeline", "5 Whys", "Root cause", "Actions", "Open questions"]
GAP_HEADINGS = ["Scope and target", "Gap table", "Summary", "Assumptions and open questions"]


def headings(text):
    return [m.group(1).strip() for m in re.finditer(r"^##\s+(.+)$", text, re.M)]


def check_headings(text, required):
    found = headings(text)
    return found == required


def check_rca(text):
    problems = []
    if not check_headings(text, RCA_HEADINGS):
        problems.append("headings missing or out of order")
    whys = re.findall(r"^\d+\.\s+Why", text, re.M)
    if not 3 <= len(whys) <= 5:
        problems.append("need 3 to 5 whys")
    section = text.split("## 5 Whys")[1].split("## Root cause")[0] if "## 5 Whys" in text else ""
    lines = [l for l in section.splitlines() if re.match(r"^\d+\.", l)]
    if any(not re.search(r"Evidence|Assumption", l) for l in lines):
        problems.append("a why has no Evidence or Assumption label")
    for t in ("Corrective", "Preventive", "Detective"):
        if t not in text:
            problems.append(f"no {t} action")
    return problems


def check_gap(text):
    problems = []
    if not check_headings(text, GAP_HEADINGS):
        problems.append("headings missing or out of order")
    header = next((l for l in text.splitlines() if l.startswith("| Requirement")), "")
    for col in ("Requirement", "Current state", "Gap", "Priority", "Action"):
        if col not in header:
            problems.append(f"missing column {col}")
    rows = [l for l in text.splitlines() if l.startswith("|") and not l.startswith("| Requirement") and not l.startswith("|---")]
    gaps = [r.split("|")[3].strip() for r in rows]
    summary = text.split("## Summary")[1].split("##")[0] if "## Summary" in text else ""
    for level in ("Major", "Minor"):
        m = re.search(rf"{level}:\s*(\d+)", summary)
        if not m or int(m.group(1)) != gaps.count(level):
            problems.append(f"summary count for {level} does not match table")
    return problems
