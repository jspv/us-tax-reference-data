"""Export a consumer bundle of the settled data.

    uv run python -m tools.export --year 2025 --version 2025.0-draft.1 [--out dist] [--tar]

Writes dist/tax-reference-data-<version>/:
  manifest.json            version, tax year, git commit, status, and per state the two files and their sha256
  states/<ST>.projection.json   layer 2: what a planner evaluates (start here)
  states/<ST>.record.json       layer 1: what the booklet says, with a citation on every item
  schema/                  both JSON Schemas
  reports/pensions.md      the cross-state pension report, generated
  README.md                how to read the bundle, and its limits

Refuses to export if any settled file fails `tools.validate`. A consumer pins a version and checks its
copy against the manifest's hashes, so a copied file that differs from the release is caught.
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import shutil
import subprocess
import tarfile
from contextlib import redirect_stdout
from datetime import datetime, timezone
from pathlib import Path

from tools import checks, federal_checks, report_pensions, validate

ROOT = Path(__file__).resolve().parent.parent
NAME = re.search(r'^name = "([^"]+)"', (ROOT / "pyproject.toml").read_text(), re.M).group(1)
ALL = ("AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC "
       "ND OH OK OR PA RI SC SD TN TX UT VT VA WA WV WI WY").split()

README = """# {name} {version}

Cited state income tax data for tax year {year}, for testing retirement-projection software.
Status: **{status}**. {status_note}

**Made by AI, for testing only.** This data was produced and checked by large language models; no
person has checked it line by line, and it will contain errors. Use it for testing software only.
Do not rely on it for any financial, tax, investment or retirement decision, or for preparing a
return. It is not tax, legal, investment or financial advice. Where these files say "hand-worked" or
"second working", the working was done step by step by a language model. It is not connected to or
endorsed by any government agency, it comes with no warranty of any kind, and there is no promise of
updates or support.

## What is here

- `states/<ST>.projection.json`: **layer 2**, the projection model. Start here. Rules a planner computes
  each year from a household's facts: brackets (surtaxes folded in), starting point and deductions,
  Social Security, retirement reliefs (who, what income, cap, income tests, credits, "take the better
  of" groups), municipal interest, capital gains, indexing, recapture; plus `not_modelled` markers
  (rules a projection can't compute, with when to warn) and `approximations` (each simplification and
  its direction). Format: `schema/projection.schema.json`.
- `states/<ST>.record.json`: **layer 1**, what the state's own booklet says, every item cited to the
  page. Read it to check a projection figure. Format: `schema/record.schema.json`.
- `checks/<ST>/*.json`: hand-worked cases, one household each, worked from the state's own form to the
  cent with the projection's rules and verified by an independent second working. Every relief, credit
  and deduction in a projection has cases (one below and one at or above each cap or income limit).
  Format: `schema/check.schema.json`; conventions (ages, warnings, flooring, expected lines) are in the
  schema descriptions. A consumer converts them to test cases for its own engine.
- `federal/<year>/US.federal.json`: the federal figures for each tax year in the bundle (rate schedules,
  standard and senior deductions, capital gains bands, NIIT, additional Medicare tax, taxable Social
  Security, SALT cap, Medicare Part B and IRMAA, payroll, retirement-account limits, RMD tables). Each group
  is cited and says how it changes in later years (`indexing`) and which figures the statute sets from
  others (`derivations`). Format: `schema/federal.schema.json`. Hand-worked cases: `checks/US/<year>/`,
  format `schema/federal-check.schema.json`.
- `reports/pensions.md`: how each state taxes its own, New York's, New Jersey's and federal government
  pensions, private pensions and IRAs.
- `manifest.json`: the version, the git commit it was built from, and the sha256 of every file.
- `LICENSE` (code, MIT) and `LICENSE-DATA` (data, CC BY 4.0), when built from the public repository.

States in this bundle ({count}): {states}.
Settled but held back until their checks are verified ({held_count}): {held}.
Not yet settled ({missing_count}): {missing}.

## Rules a consumer must know

- Amounts and rates are strings holding decimals (`"0.0425"`, `"65000"`), never floats in the files.
- Only the state of residence may tax a pension (4 U.S.C. 114); the data is per state of residence.
- A relief with `needs_input` needs a household fact the consumer may not have yet (pension source,
  paying government, contributory plan). A consumer needs to ask for it only when the household's state
  has such a relief.
- Indexing entries marked `assumed: true` are held flat because the booklet doesn't say; the statute
  hasn't been read yet.
- Local income taxes (county, city) are out of scope.

## Format version

`manifest.json` gives `format_version`. Within one format version the only changes are added optional
fields, so a reader built for it keeps working and may ignore fields it doesn't know. A renamed or
removed field, or a changed meaning, bumps the version. `unfrozen` means before the first frozen
version: anything may change. Rules the format does not yet hold are listed as approximations in each
state's projection, with their direction and size. Build readers
against `schema/`, not against examples.
"""


def format_version() -> str:
    """The frozen format version (schema/FORMAT_VERSION), or 'unfrozen' before the first tag.

    Within one format version, changes are additions of optional fields only; a consumer built for it
    keeps working. Anything else (a renamed or removed field, a changed meaning) bumps the version."""
    path = ROOT / "schema" / "FORMAT_VERSION"
    return path.read_text().strip() if path.exists() else "unfrozen"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True).stdout.strip()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--version", required=True, help="e.g. 2025.0-draft.1 or 2025.1")
    parser.add_argument("--out", type=Path, default=ROOT / "dist")
    parser.add_argument("--tar", action="store_true", help="also write a .tar.gz of the bundle")
    parser.add_argument("--no-checks", action="store_true",
                        help="export without hand-worked checks (only the early drafts did; a consumer's tests need them)")
    parser.add_argument("--verified-only", action="store_true",
                        help="leave out settled states whose checks are not all verified, and list them as held, instead of refusing")
    args = parser.parse_args(argv)

    data_dir = ROOT / "data" / "states" / str(args.year)
    states = sorted(p.name.split(".")[0] for p in data_dir.glob("*.projection.json"))
    problems = []
    held = []
    if args.verified_only and not args.no_checks:
        held = [st for st in states if checks.state_problems(args.year, st, require_verified=True)]
        states = [st for st in states if st not in held]
    for st in states:
        for kind in ("record", "projection"):
            problems += [f"{st}.{kind}: {p}" for p in validate.validate(data_dir / f"{st}.{kind}.json")]
    if not args.no_checks:
        for st in states:
            problems += [f"{st} checks: {p}" for p in checks.state_problems(args.year, st, require_verified=True)]
    federal_years = sorted(int(p.parent.name) for p in (ROOT / "data" / "federal").glob("*/US.federal.json"))
    for year in federal_years:
        problems += [f"federal {year}: {p}" for p in validate.validate(ROOT / "data" / "federal" / str(year) / "US.federal.json")]
        if not args.no_checks:
            problems += [f"federal {year} checks: {p}" for p in federal_checks.problems_for(year, require_verified=True)[1]]
    if problems:
        print("refusing to export; validation problems:\n  " + "\n  ".join(problems))
        return 1

    draft = "draft" in args.version
    bundle = args.out / f"{NAME}-{args.version}"
    if bundle.exists():
        print(f"{bundle} exists; choose a new version")
        return 1
    (bundle / "states").mkdir(parents=True)
    (bundle / "schema").mkdir()
    (bundle / "reports").mkdir()
    manifest = {"name": NAME, "version": args.version, "tax_year": args.year,
                "status": "draft" if draft else "release",
                "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "git_commit": git("rev-parse", "HEAD"), "git_dirty": bool(git("status", "--porcelain", "data", "schema")),
                "format_version": format_version(), "schemas": {}, "states": {}, "not_yet_settled": [s for s in ALL if s not in states and s not in held],
                "held": held}
    for st in states:
        entry = {}
        for kind in ("projection", "record"):
            target = bundle / "states" / f"{st}.{kind}.json"
            shutil.copyfile(data_dir / f"{st}.{kind}.json", target)
            entry[kind] = f"states/{st}.{kind}.json"
            entry[f"{kind}_sha256"] = sha(target)
        case_dir = ROOT / "checks" / str(args.year) / st
        if not args.no_checks and case_dir.exists():
            (bundle / "checks" / st).mkdir(parents=True, exist_ok=True)
            entry["checks"] = {}
            for case in sorted(case_dir.glob("*.json")):
                shutil.copyfile(case, bundle / "checks" / st / case.name)
                entry["checks"][f"checks/{st}/{case.name}"] = sha(bundle / "checks" / st / case.name)
        manifest["states"][st] = entry
    manifest["federal"] = {}
    for year in federal_years:
        target = bundle / "federal" / str(year) / "US.federal.json"
        target.parent.mkdir(parents=True)
        shutil.copyfile(ROOT / "data" / "federal" / str(year) / "US.federal.json", target)
        entry = {"file": f"federal/{year}/US.federal.json", "sha256": sha(target)}
        case_dir = ROOT / "checks" / str(year) / "US"
        if not args.no_checks and case_dir.exists():
            (bundle / "checks" / "US" / str(year)).mkdir(parents=True)
            entry["checks"] = {}
            for case in sorted(case_dir.glob("*.json")):
                shutil.copyfile(case, bundle / "checks" / "US" / str(year) / case.name)
                entry["checks"][f"checks/US/{year}/{case.name}"] = sha(bundle / "checks" / "US" / str(year) / case.name)
        manifest["federal"][str(year)] = entry
    manifest["checks_included"] = not args.no_checks
    for name in ("projection.schema.json", "record.schema.json", "check.schema.json", "federal.schema.json", "federal-check.schema.json"):
        shutil.copyfile(ROOT / "schema" / name, bundle / "schema" / name)
        manifest["schemas"][name] = sha(bundle / "schema" / name)
    for name in ("LICENSE", "LICENSE-DATA"):  # the public repository's licences travel with its releases
        if (ROOT / name).exists():
            shutil.copyfile(ROOT / name, bundle / name)
            manifest.setdefault("licences", {})[name] = sha(bundle / name)
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        report_pensions.main(["--year", str(args.year)])
    (bundle / "reports" / "pensions.md").write_text(buffer.getvalue())
    (bundle / "README.md").write_text(README.format(
        name=NAME, version=args.version, year=args.year, status=manifest["status"],
        status_note=("Figures are settled from the booklets; see 'Format version' for what may still change."
                     if draft else "Frozen format."),
        count=len(states), states=", ".join(states),
        held_count=len(held), held=", ".join(held) or "none",
        missing_count=len(manifest["not_yet_settled"]), missing=", ".join(manifest["not_yet_settled"]) or "none"))
    (bundle / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    print(f"exported {len(states)} states to {bundle}")
    if args.tar:
        archive = bundle.parent / f"{bundle.name}.tar.gz"
        with tarfile.open(archive, "w:gz") as tar:
            tar.add(bundle, arcname=bundle.name)
        print(f"wrote {archive}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
