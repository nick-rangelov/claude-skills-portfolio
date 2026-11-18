#!/usr/bin/env python3
"""Reconcile two payment transaction CSV files by id.

Usage: python reconcile.py ledger.csv processor.csv [--tolerance 0.00]
Prints a JSON report. Amounts are compared as Decimal.
"""
import argparse
import csv
import json
import sys
from collections import Counter
from decimal import Decimal, InvalidOperation


def load(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing = {"id", "amount", "currency"} - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"{path}: missing columns {sorted(missing)}")
        for line_no, row in enumerate(reader, start=2):
            try:
                amount = Decimal(row["amount"].strip())
            except (InvalidOperation, AttributeError):
                raise ValueError(f"{path} line {line_no}: invalid amount {row.get('amount')!r}")
            rows.append({"id": row["id"].strip(), "amount": amount,
                         "currency": row["currency"].strip().upper()})
    return rows


def reconcile(a_rows, b_rows, tolerance=Decimal("0")):
    count_a = Counter(r["id"] for r in a_rows)
    count_b = Counter(r["id"] for r in b_rows)
    dup_a = sorted(i for i, c in count_a.items() if c > 1)
    dup_b = sorted(i for i, c in count_b.items() if c > 1)
    a = {r["id"]: r for r in a_rows}
    b = {r["id"]: r for r in b_rows}

    matched, amount_mm, currency_mm = [], [], []
    for i in sorted(set(a) & set(b)):
        ra, rb = a[i], b[i]
        if ra["currency"] != rb["currency"]:
            currency_mm.append({"id": i, "a": ra["currency"], "b": rb["currency"]})
        elif abs(ra["amount"] - rb["amount"]) > tolerance:
            amount_mm.append({"id": i, "a": str(ra["amount"]), "b": str(rb["amount"]),
                              "difference": str(ra["amount"] - rb["amount"])})
        else:
            matched.append(i)

    return {
        "matched": matched,
        "missing_in_b": sorted(set(a) - set(b)),
        "missing_in_a": sorted(set(b) - set(a)),
        "amount_mismatches": amount_mm,
        "currency_mismatches": currency_mm,
        "duplicates_a": dup_a,
        "duplicates_b": dup_b,
    }


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("ledger")
    p.add_argument("processor")
    p.add_argument("--tolerance", default="0.00")
    args = p.parse_args(argv)
    try:
        tol = Decimal(args.tolerance)
        report = reconcile(load(args.ledger), load(args.processor), tol)
    except (ValueError, InvalidOperation, OSError) as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
