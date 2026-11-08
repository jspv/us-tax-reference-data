"""Validate the hand-worked checks and their coverage of a state's projection.

    uv run python -m tools.checks --year 2025 [--state ST ...] [--require-verified]

For each state with a projection: every file in checks/<year>/<ST>/ matches schema/check.schema.json;
every id in `tests` is a projection relief or base deduction; and coverage holds:
  - a state with an income tax has at least one `base` case; one without has a `no_tax` case;
  - each relief or credit with a cap or an income test has a `below` and an `at_or_above` case;
  - every other relief, and every base deduction, has at least one case.
With --require-verified, every case must carry a second independent working (`verified`).
Exit 1 on any problem. tools/export.py runs this before including a state.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import jsonschema
from datetime import date
from decimal import Decimal

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = json.loads((ROOT / "schema" / "check.schema.json").read_text())


def trigger_fires(rule: dict, case: dict) -> bool:
    """Whether a warning trigger (a not_modelled marker or a relief's assumption) fires for this household."""
    inputs = case["inputs"]
    income = inputs.get("income", {})
    pensions = income.get("pensions", [])
    ages = [p["age"] for p in inputs["persons"]]
    low, high = rule.get("age_range", [0, 200])
    when = rule["warn_when"]
    if when == "always":
        return True
    if when == "has_pension":
        return bool(pensions)
    if when == "has_military_pension":
        return any(p.get("source") == "military" for p in pensions)
    if when == "person_in_age_range":
        return any(low <= a <= high for a in ages)
    if when == "has_retirement_account_distribution":
        items = [i for key in ("ira_distribution", "employer_plan_distribution", "roth_conversion") for i in income.get(key, [])]
        return any(Decimal(i["amount"]) > 0 and low <= ages[i["person"]] <= high for i in items)
    if when == "has_long_term_gains":
        return Decimal(income.get("long_term_gains", "0")) > 0
    if when == "has_other_state_public_pension":
        return any(p.get("source") == "public" and p.get("paying_government") not in (None, "federal", case["state"]) for p in pensions)
    if when == "income_over":
        test = rule["income_over"]
        if test["measure"]["base"] != "federal_agi" or len(test["measure"]) > 1:
            raise ValueError("income_over in checks supports a plain federal_agi measure only")
        threshold = test["threshold"]
        status = inputs["filing_status"]
        fallback = "married_joint" if status == "qualifying_surviving_spouse" else "single"
        limit = threshold.get(status) or threshold.get("all") or threshold[fallback]
        agi, limit = Decimal(inputs["federal_agi"]), Decimal(limit)
        return agi >= limit if test.get("applies_when") == "at_or_over" else agi > limit
    return False  # has_dependents (checks hold no dependents) and never


def expected_warnings(projection: dict, case: dict) -> list[str]:
    """The warnings a projection would show for this household (one rule, not a writer's guess).

    not_modelled markers give state_rule_not_modelled:<marker id>; a relief's assumption gives
    state_assumption:<relief id>. Triggers: see trigger_fires and the projection schema's warning_trigger."""
    codes = []
    for marker in projection.get("not_modelled", []):
        if trigger_fires(marker, case):
            codes.append(f"state_rule_not_modelled:{marker.get('id') or (marker.get('from_record') or ['unnamed'])[0]}")
    for relief in projection.get("reliefs", []):
        if "assumption" in relief and trigger_fires(relief["assumption"], case):
            codes.append(f"state_assumption:{relief['id']}")
    return sorted(set(codes))


def state_problems(year: int, state: str, require_verified: bool, fix: bool = False) -> list[str]:
    projection = json.loads((ROOT / "data" / "states" / str(year) / f"{state}.projection.json").read_text())
    projection.setdefault("not_modelled", [])
    directory = ROOT / "checks" / str(year) / state
    cases = []
    problems = []
    for path in sorted(directory.glob("*.json")) if directory.exists() else []:
        case = json.loads(path.read_text())
        errors = [f"{path.name}: {'.'.join(map(str, e.absolute_path)) or '<root>'}: {e.message}"
                  for e in jsonschema.Draft202012Validator(SCHEMA).iter_errors(case)]
        problems += errors
        if not errors:
            if case["state"] != state or case["tax_year"] != year:
                problems.append(f"{path.name}: state or year doesn't match its folder")
            if require_verified and "verified" not in case:
                problems.append(f"{path.name}: not verified by a second working")
            for index, person in enumerate(case["inputs"]["persons"]):
                born = date.fromisoformat(person["born"])
                tax_age = year - born.year + (1 if (born.month, born.day) == (1, 1) else 0)  # 65 the day before the birthday
                if person["age"] != tax_age:
                    problems.append(f"{path.name}: person {index} born {person['born']} has age {person['age']}; by the tax rule it is {tax_age}")
            want = expected_warnings(projection, case)
            if sorted(case.get("accepted_warnings", [])) != want:
                if fix:
                    case["accepted_warnings"] = want
                    path.write_text(json.dumps(case, indent=2, ensure_ascii=False) + "\n")
                else:
                    problems.append(f"{path.name}: accepted_warnings should be {want} (run with --fix-warnings)")
            known = {a["what"] for a in projection.get("approximations", []) + projection["not_modelled"]}
            for text in case.get("accepted_approximations", []):
                if text not in known:
                    problems.append(f"{path.name}: accepted_approximations quotes text that is not in the projection's approximations or not_modelled: {text[:80]!r}")
            if Decimal(case["expected"]["state_taxable_income"]) < 0:
                problems.append(f"{path.name}: state_taxable_income is negative; floor it at 0 and note the form's figure in worked")
            cases.append(case)
    reliefs = {r["id"]: r for r in projection.get("reliefs", [])}
    deductions = {d["id"] for d in projection.get("base", {}).get("deductions", [])}
    for case in cases:
        for ref in case["tests"]:
            if ref not in reliefs and ref not in deductions:
                problems.append(f"{case['id']}: tests '{ref}', which is not a relief or deduction in the projection")
    kinds = {c["kind"] for c in cases}
    if projection["has_income_tax"] and "base" not in kinds:
        problems.append("no base case (a plain wages and pension return)")
    if not projection["has_income_tax"] and "no_tax" not in kinds:
        problems.append("no no_tax case")
    for rid, relief in reliefs.items():
        hits = [c for c in cases if rid in c["tests"]]
        bounded = bool(relief.get("cap") or relief.get("income_test") or relief.get("credit_amount"))
        if bounded:
            for side in ("below", "at_or_above"):
                if not any(c["boundary"] == side for c in hits):
                    problems.append(f"relief '{rid}' has no '{side}' case")
        elif not hits:
            problems.append(f"relief '{rid}' has no case")
    for did in deductions:
        if not any(did in c["tests"] for c in cases):
            problems.append(f"deduction '{did}' has no case")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--state", action="append", default=[])
    parser.add_argument("--require-verified", action="store_true")
    parser.add_argument("--fix-warnings", action="store_true", help="set each case's accepted_warnings to the computed set")
    args = parser.parse_args(argv)
    data_dir = ROOT / "data" / "states" / str(args.year)
    states = [s.upper() for s in args.state] or sorted(p.name.split(".")[0] for p in data_dir.glob("*.projection.json"))
    bad = 0
    for state in states:
        problems = state_problems(args.year, state, args.require_verified, fix=args.fix_warnings)
        count = len(list((ROOT / "checks" / str(args.year) / state).glob("*.json"))) if (ROOT / "checks" / str(args.year) / state).exists() else 0
        print(f"{state}: {count} case(s), {'ok' if not problems else str(len(problems)) + ' problem(s)'}")
        for problem in problems:
            print("  ", problem)
        bad += bool(problems)
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
