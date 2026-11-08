"""Second working for the hand-worked checks.

    uv run python -m tools.checks_compare prepare --year 2025 --state ST
        writes work/checks-verify/<year>/<ST>/<id>.inputs.json: each case without expected or worked,
        for an independent verifier
    uv run python -m tools.checks_compare compare --year 2025 --state ST
        reads the verifier's <id>.verify.json ({"expected": {...}}), compares every expected line to the
        cent, and on agreement writes the `verified` block into checks/<year>/<ST>/<id>.json.
        Prints each disagreement; exit 1 if any.
"""

from __future__ import annotations

import argparse
import json
from datetime import date
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HIDDEN = ("expected", "worked", "verified", "accepted_approximations", "accepted_warnings")


def paths(year: int, state: str) -> tuple[Path, Path]:
    return ROOT / "checks" / str(year) / state, ROOT / "work" / "checks-verify" / str(year) / state


def prepare(year: int, state: str) -> int:
    cases, out = paths(year, state)
    out.mkdir(parents=True, exist_ok=True)
    count = 0
    for path in sorted(cases.glob("*.json")):
        case = json.loads(path.read_text())
        blind = {k: v for k, v in case.items() if k not in HIDDEN}
        blind["asked"] = sorted(case["expected"].keys()) + [f"relief_amounts.{k}" for k in case["expected"].get("relief_amounts", {})]
        (out / f"{path.stem}.inputs.json").write_text(json.dumps(blind, indent=2) + "\n")
        count += 1
    print(f"{state}: {count} case(s) prepared in {out}")
    return 0


def flat(expected: dict) -> dict:
    out = {k: v for k, v in expected.items() if k != "relief_amounts"}
    out.update({f"relief_amounts.{k}": v for k, v in expected.get("relief_amounts", {}).items()})
    return out


def compare(year: int, state: str) -> int:
    cases, out = paths(year, state)
    disagreements = 0
    for path in sorted(cases.glob("*.json")):
        case = json.loads(path.read_text())
        verify_path = out / f"{path.stem}.verify.json"
        if not verify_path.exists():
            print(f"  {path.stem}: no second working")
            disagreements += 1
            continue
        theirs = flat(json.loads(verify_path.read_text())["expected"])
        ours = flat(case["expected"])
        diffs = [f"{k}: case {ours.get(k)} vs second working {theirs.get(k)}" for k in sorted(set(ours) | set(theirs))
                 if k in ours and (k not in theirs or abs(Decimal(ours[k]) - Decimal(theirs[k])) > Decimal("0.01"))]
        if diffs:
            disagreements += 1
            print(f"  {path.stem}: DISAGREES\n    " + "\n    ".join(diffs))
            continue
        case["verified"] = {"by": "independent second working (tools/checks_compare.py)", "on": date.today().isoformat(), "result": "agrees"}
        path.write_text(json.dumps(case, indent=2, ensure_ascii=False) + "\n")
    print(f"{state}: {disagreements} case(s) without agreement")
    return 1 if disagreements else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("action", choices=("prepare", "compare"))
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--state", required=True)
    args = parser.parse_args(argv)
    return (prepare if args.action == "prepare" else compare)(args.year, args.state.upper())


if __name__ == "__main__":
    raise SystemExit(main())
