"""Validate data files of either layer.

    uv run python -m tools.validate FILE.json [...]

Layer 1 (record): the schema, then figure presence: every amount and rate must be printed in that
state's converted source text (any document, either converter). Rates are looked for as
percentages too (0.0519 as 5.19), amounts with and without thousands commas.

Federal (layer "federal", data/federal/<year>/US.federal.json): the schema, then figure presence per
citation: every amount and rate in a group must be printed in the document its cite names (or a
document in cite.also), found through sources/archive/<year>/US/fetch.json.

Layer 2 (projection): the schema; the record it names exists and its sha256 matches (a changed
record makes the projection stale); every from_record id exists in the record; every amount and
rate also appears somewhere in the record, or in derived_figures as a sum or difference of record
figures that the validator re-does (a folded surtax band, an extra gains rate); the state's
deductions have an indexing answer, so a projection knows whether to grow them.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from decimal import Decimal
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parent.parent
SKIP_ZERO_KEYS = {"start", "value"}  # a bracket starting at 0, an exemption share of 0


def schema(layer: str) -> dict:
    return json.loads((ROOT / "schema" / f"{layer}.schema.json").read_text())


def amounts(value, path=""):
    if isinstance(value, dict):
        for key, item in value.items():
            yield from amounts(item, f"{path}.{key}" if path else key)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from amounts(item, f"{path}[{index}]")
    elif isinstance(value, str) and re.fullmatch(r"-?[0-9]+(\.[0-9]+)?", value):
        yield path, value


def leaf(path: str) -> str:
    return path.split(".")[-1].split("[")[0]


def spellings(path: str, text: str) -> set[str]:
    """Ways the sources might print this figure."""
    number = Decimal(text)
    out = {text, f"{number:,}", f"{number:,.2f}"}
    if number == int(number):
        out.add(str(int(number)))
    if leaf(path) == "factor":  # statutes write a factor in words or as a percentage
        out |= {f"{(number * 100).normalize():f} percent", f"{(number * 100).normalize():f}%"}
        out |= {Decimal("2"): {"twice", "2 times"}, Decimal("0.5"): {"one-half", "half"}, Decimal("1.5"): {"150 percent"}}.get(number, set())
    if leaf(path) in {"rate", "credit_rate", "value"} or Decimal(0) < number < 1:
        percent = (number * 100).normalize()
        out |= {f"{percent:f}", f"{percent:f}%", f"{percent:f} percent", str(number)}
        if str(number).startswith("0."):
            out.add(str(number)[1:])  # printed without the leading zero: .007
    return out


def sources_missing(state: str, year: int) -> list[str]:
    """Sources recorded in fetch.json whose converted text is not here (a checkout without pulled sources)."""
    directory = ROOT / "sources" / "archive" / str(year) / state
    fetched = directory / "fetch.json"
    missing = []
    for record in json.loads(fetched.read_text()) if fetched.exists() else []:
        name = record.get("file") or ""
        stem = Path(name).stem
        if record.get("ok") and name.endswith(".pdf") and not any((directory / f"{stem}{suffix}").exists() for suffix in (".docling.md", ".pypdf.txt")):
            missing.append(name)
        elif record.get("ok") and record.get("text_file") and not (directory / record["text_file"]).exists():
            missing.append(name)
    return missing


def not_pulled(state: str, year: int) -> list[str]:
    missing = sources_missing(state, year)
    if not missing:
        return []
    return [f"provenance: {len(missing)} source document(s) for {state} {year} are not pulled; run "
            f"uv run python -m tools.sources pull --year {year} --state {state}"]


def source_text(state: str, year: int) -> str:
    directory = ROOT / "sources" / "archive" / str(year) / state
    files = sorted(directory.glob("*.docling.md")) + sorted(directory.glob("*.pypdf.txt")) + sorted(directory.glob("*.page.txt"))
    return "\n".join(p.read_text(errors="ignore") for p in files)


def schema_problems(data: dict) -> list[str]:
    layer = data.get("layer")
    if layer not in ("record", "projection", "federal"):
        return ["schema: 'layer' must be 'record', 'projection' or 'federal'"]
    return [f"schema: {'.'.join(map(str, e.absolute_path)) or '<root>'}: {e.message}"
            for e in jsonschema.Draft202012Validator(schema(layer)).iter_errors(data)]


def schedule_tax(brackets: list, income: Decimal) -> Decimal:
    tax = Decimal(0)
    for index, band in enumerate(brackets):
        start = Decimal(band["start"])
        end = Decimal(brackets[index + 1]["start"]) if index + 1 < len(brackets) else None
        if income <= start:
            break
        top = income if end is None else min(income, end)
        if "base" in band:
            tax = Decimal(band["base"])  # a printed base replaces the sum of the lower bands
        tax += (top - start) * Decimal(band["rate"])
    return tax


def derivation_problems(data: dict) -> list:
    """A derived schedule must reproduce every printed table row (within 1 dollar; tables round) and the printed formula."""
    derivation = data["brackets"].get("derivation")
    if not derivation:
        return []
    problems = []
    for row in derivation["table_rows"]:
        statuses = ["single", "married_joint"] if row["status"] == "all" else [row["status"]]
        for status in statuses:
            schedule = data["brackets"].get(status) or data["brackets"]["single"]
            got = schedule_tax(schedule, Decimal(row["income"]))
            if abs(got - Decimal(row["tax"])) > 1:
                problems.append(f"derivation: {status} schedule gives {got:.2f} at {row['income']}; the printed table says {row['tax']}")
    formula = derivation.get("formula")
    if formula:
        over = Decimal(formula["over"])
        for status in ("single", "married_joint"):
            for income in (over, over * 2):
                expected = Decimal(formula["rate"]) * income - Decimal(formula["minus"])
                got = schedule_tax(data["brackets"][status], income)
                if abs(got - expected) > 1:
                    problems.append(f"derivation: {status} schedule gives {got:.2f} at {income}; the printed formula gives {expected:.2f}")
    if len(derivation["table_rows"]) < 3:
        problems.append("derivation: at least 3 printed table rows are needed, spread across the bands")
    return problems


def record_problems(data: dict) -> list[str]:
    if not_pulled(data["state"], data["tax_year"]):
        return not_pulled(data["state"], data["tax_year"])
    text = source_text(data["state"], data["tax_year"])
    if not text:
        return [f"provenance: no converted text under sources/archive/{data['tax_year']}/{data['state']}"]
    flat = re.sub(r"\s+", " ", text)
    problems = derivation_problems(data)
    derived = bool(data["brackets"].get("derivation"))
    for where, value in amounts(data):
        if leaf(where) in SKIP_ZERO_KEYS and Decimal(value) == 0:
            continue
        if derived and re.match(r"brackets\.(single|married_joint|married_separate|head_of_household)\[", where):
            continue  # derived bracket figures are checked by derivation_problems instead
        if re.match(r"brackets\.derivation\.table_rows\[\d+\]\.income$", where):
            continue  # a table row's midpoint is computed from its printed bounds, not printed itself
        if not any(s in flat for s in spellings(where, value)):
            problems.append(f"provenance: {where}={value} is not printed in the sources")
    return problems


def document_texts(year: int, jurisdiction: str = "US") -> dict[str, str]:
    """Converted text of each archived source, keyed by the address it was fetched from (asked and final)."""
    directory = ROOT / "sources" / "archive" / str(year) / jurisdiction
    texts = {}
    fetched = directory / "fetch.json"
    for record in json.loads(fetched.read_text()) if fetched.exists() else []:
        if not record.get("ok") or not record.get("file"):
            continue
        stem = Path(record["file"]).stem
        files = [directory / f"{stem}.docling.md", directory / f"{stem}.pypdf.txt", directory / f"{stem}.page.txt"]
        text = re.sub(r"\s+", " ", "\n".join(f.read_text(errors="ignore") for f in files if f.exists()))
        for url in {record.get("url"), record.get("final_url")} - {None}:
            texts[url] = text
    return texts


def cited_groups(value, path=""):
    """Each object that carries a cite, with the amounts that belong to it (not to a nested cited object)."""
    if isinstance(value, dict):
        if "cite" in value:
            own = {k: v for k, v in value.items() if k not in ("cite", "derivations", "indexing") and not (isinstance(v, dict) and "cite" in v)}
            yield path, value["cite"], list(amounts(own, path))
        for key, item in value.items():
            if key != "cite":
                yield from cited_groups(item, f"{path}.{key}" if path else key)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            yield from cited_groups(item, f"{path}[{index}]")


def resolve(node, path: str):
    """The value at a path like 'schedules.single[1].start' inside node, or None."""
    for part in path.split("."):
        name, _, index = part.partition("[")
        if not isinstance(node, dict) or name not in node:
            return None
        node = node[name]
        if index:
            position = int(index.rstrip("]"))
            if not isinstance(node, list) or position >= len(node):
                return None
            node = node[position]
    return node


def derivation_groups(value, path=""):
    if isinstance(value, dict):
        if value.get("derivations"):
            yield path, value
        for key, item in value.items():
            yield from derivation_groups(item, f"{path}.{key}" if path else key)


def federal_derivation_problems(data: dict) -> list[str]:
    """Each derived figure equals its rule exactly, and is set from a figure indexed on its own."""
    problems = []
    for where, group in derivation_groups(data):
        targets = {d["target"] for d in group["derivations"]}
        for rule in group["derivations"]:
            target, source = resolve(group, rule["target"]), resolve(group, rule["from"])
            other = resolve(group, rule["subtract"]) if rule["rule"] == "minus" else None
            if not all(isinstance(v, str) for v in [target, source] + ([other] if rule["rule"] == "minus" else [])):
                problems.append(f"derivation: {where}: {rule['target']} or a figure it uses is not an amount in the group")
                continue
            if rule["from"] in targets or (rule["rule"] == "minus" and rule["subtract"] in targets):
                problems.append(f"derivation: {where}: {rule['target']} is set from a figure that is itself derived")
            if rule["rule"] == "times":
                if "factor" not in rule:
                    problems.append(f"derivation: {where}: {rule['target']} has rule 'times' and no factor")
                    continue
                expected = Decimal(source) * Decimal(rule["factor"])
            else:
                expected = Decimal(source) - Decimal(other)
            if Decimal(target) != expected:
                problems.append(f"derivation: {where}.{rule['target']}={target}; its rule gives {expected.normalize():f}")
    return problems


def federal_problems(data: dict) -> list[str]:
    problems = federal_derivation_problems(data)
    if not_pulled("US", data["tax_year"]):
        return problems + not_pulled("US", data["tax_year"])
    texts = document_texts(data["tax_year"])
    if not texts:
        return problems + [f"provenance: no fetched sources under sources/archive/{data['tax_year']}/US"]
    derived_paths = {f"{where}.{rule['target']}" for where, group in derivation_groups(data) for rule in group["derivations"]}
    for where, cite, figures in cited_groups(data):
        urls = [cite["url"]] + [a["url"] for a in cite.get("also", [])]
        missing = [u for u in urls if u not in texts]
        if missing:
            problems.append(f"provenance: {where} cites {missing[0]}, which is not an archived source")
            continue
        text = " ".join(texts[u] for u in urls)
        for path, value in figures:
            if leaf(path) in SKIP_ZERO_KEYS and Decimal(value) == 0:
                continue
            if path in derived_paths:
                continue  # a derived figure is proved by re-doing its rule (federal_derivation_problems), printed or not
            if not any(s in text for s in spellings(path, value)):
                problems.append(f"provenance: {path}={value} is not printed in the document {where} cites")
    return problems


def record_ids(record: dict) -> set[str]:
    ids = set()
    for section in ("reliefs", "surtaxes", "capital_gains"):
        ids |= {item["id"] for item in record.get(section, [])}
    ids |= {item["id"] for item in record.get("base", {}).get("deductions", [])}
    return ids


def income_tests(data: dict):
    """Every (where, income_test) in a projection: relief tests and deduction phase-outs."""
    for relief in data.get("reliefs", []):
        if "income_test" in relief:
            yield f"reliefs.{relief['id']}", relief["income_test"]
    for deduction in data.get("base", {}).get("deductions", []):
        if "phase_out" in deduction:
            yield f"base.deductions.{deduction['id']}", deduction["phase_out"]


def growable_figures(data: dict) -> list[tuple[str, str | None, str | None]]:
    """(section, id, field) for every amount a projection grows each year."""
    out = []
    if data.get("has_income_tax"):
        bands = max((len(v) for v in data.get("brackets", {}).values() if isinstance(v, list)), default=0)
        out += [("brackets", str(i), None) for i in range(1, bands)] or [("brackets", None, None)]
    if data.get("surtaxes"):
        out.append(("surtaxes", None, None))
    if any("applies_over" in c for c in data.get("capital_gains", [])):
        out.append(("capital_gains", None, None))
    if data.get("recapture"):
        out.append(("recapture", None, None))
    for deduction in data.get("base", {}).get("deductions", []):
        if "amount" in deduction:
            out.append(("deductions", deduction["id"], "amount"))
        if "phase_out" in deduction:
            out.append(("deductions", deduction["id"], "phase_out_thresholds"))
            if any("amount" in step for step in deduction["phase_out"].get("steps", [])):
                out.append(("deductions", deduction["id"], "phase_out_amounts"))
    for relief in data.get("reliefs", []):
        out += [("reliefs", relief["id"], f) for f in ("cap", "income_test", "credit_amount", "applies_over", "earned_income_limit") if f in relief]
    return out


def parse_selector(text: str) -> tuple[str, str | None, str | None]:
    head, _, field = text.partition(".")
    section, _, ident = head.partition(":")
    return section, ident or None, field or None


def indexing_problems(data: dict) -> list[str]:
    """Every growable figure is covered by exactly one indexing entry at its most specific level."""
    entries = data.get("indexing", [])
    if not growable_figures(data) and not entries:
        return []  # nothing to grow (a state with no income tax)
    if not any("covers" in e for e in entries):
        return ["indexing: no entry says which figures it covers (covers)"]
    problems = []
    bands = max((len(v) for v in data.get("brackets", {}).values() if isinstance(v, list)), default=0)
    ids = {"deductions": {d["id"] for d in data.get("base", {}).get("deductions", [])}, "reliefs": {r["id"] for r in data.get("reliefs", [])},
           "brackets": {str(i) for i in range(1, bands)}}
    selectors = []
    for entry in entries:
        if "covers" not in entry:
            problems.append(f"indexing: '{entry['figure']}' has no covers")
            continue
        for text in entry["covers"]:
            section, ident, field = parse_selector(text)
            if ident and ident not in ids.get(section, set()):
                problems.append(f"indexing: '{entry['figure']}' covers {text}, but there is no {section} '{ident}'")
            selectors.append((entry["figure"], section, ident, field))
    for section, ident, field in growable_figures(data):
        def level(s_id, s_field):  # an id beats no id; a longer field ('phase_out_thresholds') beats its prefix ('phase_out')
            return (s_id is not None) * 4 + (len(s_field.split("_")) if s_field else 0)
        matches = [(fig, level(s_id, s_field)) for fig, s, s_id, s_field in selectors
                   if s == section and s_id in (None, ident) and (s_field is None or field == s_field or (field or "").startswith(s_field + "_"))]
        name = section + (f":{ident}" if ident else "") + (f".{field}" if field else "")
        if not matches:
            problems.append(f"indexing: no entry covers {name}")
            continue
        best = max(level for _, level in matches)
        winners = sorted({fig for fig, level in matches if level == best})
        if len(winners) > 1:
            problems.append(f"indexing: {name} is covered by more than one entry at the same level: {', '.join(winners)}")
    return problems


def marker_problems(data: dict) -> list[str]:
    seen, problems = set(), []
    for index, marker in enumerate(data.get("not_modelled", [])):
        if "id" not in marker:
            problems.append(f"not_modelled[{index}]: no id")
        elif marker["id"] in seen:
            problems.append(f"not_modelled[{index}]: id '{marker['id']}' is used twice")
        else:
            seen.add(marker["id"])
    return problems


def projection_shape_problems(data: dict) -> list[str]:
    """Rules the JSON schema can't say: fields that only make sense together."""
    problems = indexing_problems(data) + marker_problems(data)
    investment = {"interest", "dividends", "capital_gains", "rent_and_royalties"}
    if any(r.get("who", {}).get("basis") == "each_person" and investment & set(r.get("covers", [])) for r in data.get("reliefs", [])) \
            and "joint_income" not in data:
        problems.append("joint_income: a per-person relief covers investment income, so say how joint income is divided")
    base = data.get("base", {})
    if base.get("starts_from") == "federal_taxable_income" and "federal_senior_deduction" not in base:
        problems.append("base: a state that starts from federal taxable income needs federal_senior_deduction")
    for index, rule in enumerate(data.get("recapture", [])):
        if (rule["effect"] == "other") != ("other_rule" in rule):
            problems.append(f"recapture[{index}]: other_rule goes with effect other, and only with it")
    relief_ids = {r["id"] for r in data.get("reliefs", [])}
    for where, test in income_tests(data):
        if test["effect"] == "share_phase_out" and "width" not in test:
            problems.append(f"{where}: effect share_phase_out needs a width")
        for ref in test["measure"].get("minus_reliefs", []):
            if ref not in relief_ids:
                problems.append(f"{where}: measure.minus_reliefs names '{ref}', which is not a relief here")
    triggers = [(f"not_modelled[{i}]", m) for i, m in enumerate(data.get("not_modelled", []))]
    for relief in data.get("reliefs", []):
        if relief.get("refundable") and relief["form"] != "credit":
            problems.append(f"reliefs.{relief['id']}: refundable is for credits only")
        for later in ("applies_over", "keeps_taxable", "earned_income_limit"):
            if later in relief and later not in relief.get("requires", []):
                problems.append(f"reliefs.{relief['id']}: {later} must be listed in requires")
        if "social_security" in relief.get("cap_reduced_by", []) and "social_security_basis" not in relief:
            problems.append(f"reliefs.{relief['id']}: cap_reduced_by social_security needs social_security_basis")
        if "cap_reduction" in relief and not relief.get("cap_reduced_by"):
            problems.append(f"reliefs.{relief['id']}: cap_reduction needs cap_reduced_by")
        if "assumption" in relief:
            triggers.append((f"reliefs.{relief['id']}.assumption", relief["assumption"]))
            if relief["assumption"]["what"] not in {a["what"] for a in data.get("approximations", [])}:
                problems.append(f"reliefs.{relief['id']}: the assumption's text must also be an approximations entry")
    for where, rule in triggers:
        if rule["warn_when"] == "income_over" and "income_over" not in rule:
            problems.append(f"{where}: warn_when income_over needs income_over")
        if rule["warn_when"] == "person_in_age_range" and "age_range" not in rule:
            problems.append(f"{where}: warn_when person_in_age_range needs age_range")
    return problems


def projection_problems(data: dict) -> list[str]:
    named = Path(data["record"]["path"])
    record_path = named if named.is_absolute() else ROOT / named
    if not record_path.exists():
        return [f"record: {data['record']['path']} not found"]
    raw = record_path.read_bytes()
    problems = []
    if hashlib.sha256(raw).hexdigest() != data["record"]["sha256"]:
        problems.append("record: sha256 differs, the record changed since this projection was made (stale)")
    record = json.loads(raw)
    known = record_ids(record)
    for section in ("reliefs", "not_modelled"):
        for item in data.get(section, []):
            for ref in item.get("from_record", []):
                if ref not in known:
                    problems.append(f"record: {section} names '{ref}', which is not an id in the record")
    problems += projection_shape_problems(data)
    figures = {entry["figure"] for entry in data.get("indexing", [])}
    deduction_ids = {d["id"] for d in data["base"]["deductions"]}
    if deduction_ids and "deductions" not in figures and not deduction_ids <= figures:
        problems.append("indexing: the deductions need an indexing answer (figure 'deductions' or each deduction id)")
    record_figures = {Decimal(v) for _, v in amounts(record)}
    for item in data.get("derived_figures", []):
        parts = [Decimal(x) for x in item.get("of", [])]
        missing = [str(x) for x in parts if x not in record_figures]
        if missing:
            problems.append(f"figure: derived {item['value']} uses {', '.join(missing)}, which the record doesn't print")
            continue
        result = sum(parts) if item["how"] == "sum" else parts[0] / 2 if item["how"] == "half" else parts[0] - sum(parts[1:])
        if result != Decimal(item["value"]):
            problems.append(f"figure: derived {item['value']} is not the {item['how']} of {', '.join(item.get('of', []))} ({result})")
            continue
        record_figures.add(Decimal(item["value"]))
    for where, value in amounts(data):
        if where.startswith("record.") or where.startswith("derived_figures"):
            continue
        if Decimal(value) not in record_figures and not (leaf(where) in SKIP_ZERO_KEYS and Decimal(value) == 0):
            problems.append(f"figure: {where}={value} is not in the record (a projection adds no figures)")
    return problems


def validate(path: Path) -> list[str]:
    data = json.loads(path.read_text())
    problems = schema_problems(data)
    if problems:
        return problems
    if data["layer"] == "federal":
        return federal_problems(data)
    return record_problems(data) if data["layer"] == "record" else projection_problems(data)


def main(argv: list[str]) -> int:
    bad = 0
    for name in argv:
        problems = validate(Path(name))
        print(f"{name}: {'ok' if not problems else str(len(problems)) + ' problem(s)'}")
        for problem in problems:
            print("  ", problem)
        bad += bool(problems)
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
