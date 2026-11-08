"""Validate the hand-worked federal checks and their coverage of the federal file.

    uv run python -m tools.federal_checks --year 2025 [--require-verified]

Every file in checks/<year>/US/ matches schema/federal-check.schema.json; ages follow the tax rule;
every path in `tests` names a group in data/federal/<year>/US.federal.json; and coverage holds:
each group in COVERED that the file has needs a case, and each group in THRESHOLD needs a `below`
and an `at_or_above` case. Lookup-only figures (contribution limits, the SALT cap, the Single Life
Table) are proved by the citation check in tools/validate.py instead. Exit 1 on any problem.
"""

from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = json.loads((ROOT / "schema" / "federal-check.schema.json").read_text())
COVERED = (
    "income_tax.brackets", "income_tax.standard_deduction", "income_tax.additional_standard_deduction",
    "income_tax.capital_gains", "medicare.part_b", "payroll.medicare", "rmd.uniform_lifetime_table",
)
THRESHOLD = (
    "income_tax.senior_deduction", "income_tax.net_investment_income_tax", "income_tax.additional_medicare_tax",
    "income_tax.social_security_benefits", "medicare.irmaa", "payroll.social_security", "rmd.start_age",
)


def group(data: dict, path: str):
    node = data
    for part in path.split("."):
        if not isinstance(node, dict) or part not in node:
            return None
        node = node[part]
    return node


def problems_for(year: int, require_verified: bool) -> tuple[int, list[str]]:
    federal_path = ROOT / "data" / "federal" / str(year) / "US.federal.json"
    if not federal_path.exists():
        return 0, [f"no {federal_path.relative_to(ROOT)}"]
    data = json.loads(federal_path.read_text())
    directory = ROOT / "checks" / str(year) / "US"
    cases, problems = [], []
    for path in sorted(directory.glob("*.json")) if directory.exists() else []:
        case = json.loads(path.read_text())
        errors = [f"{path.name}: {'.'.join(map(str, e.absolute_path)) or '<root>'}: {e.message}"
                  for e in jsonschema.Draft202012Validator(SCHEMA).iter_errors(case)]
        problems += errors
        if errors:
            continue
        if case["tax_year"] != year or path.stem != case["id"]:
            problems.append(f"{path.name}: year or id doesn't match the file")
        if require_verified and "verified" not in case:
            problems.append(f"{path.name}: not verified by a second working")
        for index, person in enumerate(case["inputs"].get("persons", [])):
            born = date.fromisoformat(person["born"])
            tax_age = year - born.year + (1 if (born.month, born.day) == (1, 1) else 0)
            if person["age"] != tax_age:
                problems.append(f"{path.name}: person {index} born {person['born']} has age {person['age']}; by the tax rule it is {tax_age}")
        for ref in case["tests"]:
            if group(data, ref) is None:
                problems.append(f"{path.name}: tests '{ref}', which is not a group in the federal file")
        cases.append(case)
    for ref in COVERED + THRESHOLD:
        if group(data, ref) is None:
            continue
        hits = [c for c in cases if ref in c["tests"]]
        if ref in THRESHOLD:
            for side in ("below", "at_or_above"):
                if not any(c["boundary"] == side for c in hits):
                    problems.append(f"'{ref}' has no '{side}' case")
        elif not hits:
            problems.append(f"'{ref}' has no case")
    return len(cases), problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--require-verified", action="store_true")
    args = parser.parse_args(argv)
    count, problems = problems_for(args.year, args.require_verified)
    print(f"US {args.year}: {count} case(s), {'ok' if not problems else str(len(problems)) + ' problem(s)'}")
    for problem in problems:
        print("  ", problem)
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
