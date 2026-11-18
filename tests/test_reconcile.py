import json
import subprocess
import sys
from decimal import Decimal
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT_DIR = ROOT / "skills" / "payments-reconciliation-checker"
sys.path.insert(0, str(SCRIPT_DIR / "scripts"))
import reconcile as rc  # noqa: E402


def rows(*items):
    return [{"id": i, "amount": Decimal(a), "currency": c} for i, a, c in items]


def test_exact_match():
    r = rc.reconcile(rows(("1", "10.00", "EUR")), rows(("1", "10.00", "EUR")))
    assert r["matched"] == ["1"] and not r["amount_mismatches"]


def test_missing_on_each_side():
    r = rc.reconcile(rows(("1", "1", "EUR"), ("2", "1", "EUR")), rows(("2", "1", "EUR"), ("3", "1", "EUR")))
    assert r["missing_in_b"] == ["1"] and r["missing_in_a"] == ["3"]


def test_amount_mismatch_and_difference():
    r = rc.reconcile(rows(("1", "10.50", "EUR")), rows(("1", "10.00", "EUR")))
    assert r["amount_mismatches"][0]["difference"] == "0.50"


def test_tolerance_allows_small_difference():
    r = rc.reconcile(rows(("1", "10.01", "EUR")), rows(("1", "10.00", "EUR")), Decimal("0.01"))
    assert r["matched"] == ["1"]


def test_currency_mismatch_not_counted_as_match():
    r = rc.reconcile(rows(("1", "10", "USD")), rows(("1", "10", "EUR")))
    assert r["currency_mismatches"] and not r["matched"]


def test_duplicates_detected():
    r = rc.reconcile(rows(("1", "5", "EUR"), ("1", "5", "EUR")), rows(("1", "5", "EUR")))
    assert r["duplicates_a"] == ["1"]


def test_decimal_precision_no_float_error():
    r = rc.reconcile(rows(("1", "0.1", "EUR")), rows(("1", "0.10", "EUR")))
    assert r["matched"] == ["1"]


def test_invalid_amount_rejected(tmp_path):
    f = tmp_path / "a.csv"
    f.write_text("id,amount,currency\n1,abc,EUR\n")
    with pytest.raises(ValueError):
        rc.load(str(f))


def test_missing_column_rejected(tmp_path):
    f = tmp_path / "a.csv"
    f.write_text("id,amount\n1,5\n")
    with pytest.raises(ValueError):
        rc.load(str(f))


def test_cli_matches_eval_case():
    case = json.loads((ROOT / "evals" / "cases.json").read_text())["payments-reconciliation-checker"][0]
    a, b = [str(ROOT / p) for p in case["inputs"]]
    out = subprocess.run([sys.executable, str(SCRIPT_DIR / "scripts" / "reconcile.py"), a, b],
                         capture_output=True, text=True, check=True).stdout
    report = json.loads(out)
    exp = case["expected"]
    assert report["matched"] == exp["matched"]
    assert report["missing_in_b"] == exp["missing_in_b"]
    assert report["missing_in_a"] == exp["missing_in_a"]
    assert [m["id"] for m in report["amount_mismatches"]] == exp["amount_mismatches"]
    assert [m["id"] for m in report["currency_mismatches"]] == exp["currency_mismatches"]


def test_cli_bad_file_returns_error_code(tmp_path):
    p = subprocess.run([sys.executable, str(SCRIPT_DIR / "scripts" / "reconcile.py"),
                        str(tmp_path / "none.csv"), str(tmp_path / "none2.csv")],
                       capture_output=True, text=True)
    assert p.returncode == 2
