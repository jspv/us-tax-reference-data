"""Cross-state pension report, generated from the settled records (layer 1).

    uv run python -m tools.report_pensions --year 2025 [--paying NY --paying NJ] > docs/reports/2025-pensions.md

For each settled state of residence, how it taxes: its own government pensions, a government pension
paid by each --paying state, federal government pensions, private pensions, and IRA distributions.
Every line cites the record entry (publication, page) it comes from. A pension paid by one state to a
resident of another is taxed only by the state of residence (4 U.S.C. 114, in sources/archive/*/US).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def fmt_amount(by_status: dict | None) -> str:
    if not by_status:
        return "no cap"
    if "all" in by_status and len(by_status) == 1:
        return f"{int(float(by_status['all'])):,}"
    parts = [f"{k.replace('married_joint', 'joint').replace('married_separate', 'separate').replace('head_of_household', 'HoH')} {int(float(v)):,}"
             for k, v in by_status.items()]
    return ", ".join(parts)


def modelled_ids(state: str, year: int) -> set[str]:
    """Record ids the state's projection models; a relief it leaves in not_modelled turns on facts a
    planner doesn't hold (an occupation, disability, a vesting date, years of service)."""
    path = ROOT / "data" / "states" / str(year) / f"{state}.projection.json"
    if not path.exists():
        return set()
    projection = json.loads(path.read_text())
    # The first record id behind a projection relief is its main rule; ids folded in after it (Alabama's
    # fire fighter and peace officer entries inside the public pension exemption) are narrower cases.
    return {relief["from_record"][0] for relief in projection.get("reliefs", []) if relief.get("from_record")}


def is_special(relief: dict, modelled: set[str]) -> bool:
    """A narrow case: listed separately, not in the main line. Structured, not by keyword: the projection
    leaves it unmodelled."""
    return relief["id"] not in modelled


def is_general_any_income(relief: dict) -> bool:
    """An all_income entry belongs in a pension report only when it is an age-based deduction."""
    who = relief.get("who", {})
    return relief.get("credit_basis") != "tax" and (who.get("min_age") is not None or who.get("born_on_or_before"))


def describe(relief: dict) -> str:
    who = relief.get("who", {})
    bits = []
    if relief.get("form") == "exempt_in_full":
        bits.append("exempt in full")
    elif relief.get("form") == "credit":
        rate = relief.get("credit_rate")
        bits.append(f"credit {float(rate) * 100:g}%" if rate else f"credit {relief.get('credit_amount', '')}")
    else:
        bits.append("subtraction up to " + fmt_amount(relief.get("cap")) + (f" per {relief['cap_per']}" if relief.get("cap_per") else ""))
    if relief.get("share"):
        bits.append(f"{float(relief['share']) * 100:g}% of it")
    if who.get("min_age") is not None:
        bits.append(f"age {who['min_age']:g}+")
    if who.get("max_age") is not None:
        bits.append(f"up to age {who['max_age']:g}")
    if who.get("born_on_or_after") or who.get("born_on_or_before"):
        bits.append(f"born {who.get('born_on_or_after') or '...'} to {who.get('born_on_or_before') or '...'}")
    if who.get("basis") == "older_spouse":
        bits.append("by the older spouse's birth date")
    test = relief.get("income_test")
    if test:
        threshold = fmt_amount(test.get("threshold"))
        bits.append(f"reduced as income rises from {threshold}" if test.get("effect") != "removes" else f"none above {threshold}")
    conditions = who.get("other_conditions", [])
    if conditions:
        bits.append("if: " + conditions[0][:90] + (" (+ more)" if len(conditions) > 1 else ""))
    return "; ".join(bits)


def cite(relief: dict) -> str:
    section = relief.get("cite", {}).get("section", "?")
    return section.split(";")[0][:70]


def kinds_for(pension: str, residence: str) -> set[str]:
    if pension in (residence, "federal"):
        return {"public_pension"}
    if pension == "private":
        return {"private_pension", "annuity"}
    if pension == "employer_plan":
        return {"employer_plan_distribution"}
    if pension == "ira":
        return {"ira_distribution"}
    return {"public_pension_other_state"}


def applies(relief: dict, pension: str, residence: str) -> bool:
    covers = set(relief.get("covers", []))
    if "all_income" in covers:
        return is_general_any_income(relief)
    if not covers & kinds_for(pension, residence):
        return False
    paying = relief.get("paying_states")
    return not paying or pension in paying


def state_rows(record: dict, payers: list[str]) -> list[tuple[str, str]]:
    st = record["state"]
    modelled = modelled_ids(st, record["tax_year"])
    if not record["has_income_tax"]:
        return [("all pensions", "not taxed: no personal income tax (" + record["brackets"]["cite"]["publication"] + ")")]
    rows = []
    columns = [(st, f"{st} government pension")] + [(p, f"{p} government pension") for p in payers if p != st] + \
              [("federal", "federal government pension"), ("private", "private pension (defined benefit) / annuity"),
               ("employer_plan", "401(k) / 403(b) / 457 withdrawal"), ("ira", "IRA distribution")]
    for key, label in columns:
        matching = [r for r in record.get("reliefs", []) if applies(r, key, st)]
        found = [r for r in matching if not is_special(r, modelled)]
        special = [r for r in matching if is_special(r, modelled)]
        unclear = [r for r in record.get("reliefs", []) if kinds_for(key, st) & set(r.get("covers_unclear", []))]
        if not found:
            text = "**no relief found in the sources**: taxed as ordinary income"
        else:
            text = "<br>".join(f"**{describe(r)}**: {r.get('label', r['id'])[:80]} ({cite(r)})" for r in found)
        if special:
            text += "<br>narrower cases (not modelled on their own): " + "; ".join(r.get("label", r["id"])[:60] for r in special)
        if unclear:
            text += "<br>unclear in the sources: " + ", ".join(r.get("label", r["id"]) for r in unclear)
        rows.append((label, text))
    return rows


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, default=2025)
    parser.add_argument("--paying", action="append", default=[], help="paying states to show (default NY, NJ)")
    args = parser.parse_args(argv)
    payers = args.paying or ["NY", "NJ"]
    records = sorted((ROOT / "data" / "states" / str(args.year)).glob("*.record.json"))
    print(f"# Pension taxation by state of residence, {args.year}\n")
    print("Generated by `tools/report_pensions.py` from the settled records; regenerate after any settlement. "
          "Only the state you live in can tax a pension (4 U.S.C. 114). Relief listed is what the record holds; "
          "an entry with `all_income` (an age deduction) applies to any income, pensions included. "
          f"States settled: {len(records)}.\n")
    for path in records:
        record = json.loads(path.read_text())
        print(f"## {record['state']}\n")
        print("| Pension | Treatment (source) |\n|---|---|")
        for label, text in state_rows(record, payers):
            print(f"| {label} | {text} |")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
