import re
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tests"))
import check_output as co  # noqa: E402

SKILLS = sorted(p.parent for p in (ROOT / "skills").glob("*/SKILL.md"))


@pytest.mark.parametrize("skill", SKILLS, ids=lambda p: p.name)
def test_skill_frontmatter(skill):
    text = (skill / "SKILL.md").read_text()
    m = re.match(r"^---\nname: (.+)\ndescription: (.+)\n---\n", text)
    assert m, "frontmatter with name and description required"
    assert m.group(1) == skill.name
    assert len(m.group(2)) <= 1024


@pytest.mark.parametrize("skill", SKILLS, ids=lambda p: p.name)
def test_skill_has_rules_and_output_format(skill):
    text = (skill / "SKILL.md").read_text()
    assert "## Output format" in text and "## Rules" in text


def test_rca_sample_output_passes():
    text = (ROOT / "skills/root-cause-analysis/examples/sample-output-01.md").read_text()
    assert co.check_rca(text) == []


def test_rca_rejects_missing_label():
    text = (ROOT / "skills/root-cause-analysis/examples/sample-output-01.md").read_text()
    bad = text.replace("Evidence: 312 duplicate rows in the file.", "")
    assert "a why has no Evidence or Assumption label" in co.check_rca(bad)


def test_gap_sample_output_passes():
    text = (ROOT / "skills/gap-analysis/examples/sample-output-01.md").read_text()
    assert co.check_gap(text) == []


def test_gap_rejects_wrong_summary_count():
    text = (ROOT / "skills/gap-analysis/examples/sample-output-01.md").read_text()
    bad = text.replace("Major: 2", "Major: 5")
    assert any("Major" in p for p in co.check_gap(bad))
