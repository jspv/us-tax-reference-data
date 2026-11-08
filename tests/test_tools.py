import copy
import hashlib
import json

import pytest

from tools import compare, validate

_CITE = {"publication": "Test booklet", "section": "p.1, line 2", "url": "https://example.gov/b.pdf", "accessed": "2026-11-06"}


def cite():
    return dict(_CITE)


def record(**over):
    data = {
        "layer": "record", "state": "ZZ", "tax_year": 2025, "has_income_tax": True,
        "brackets": {"single": [{"rate": "0.0519", "start": "0"}], "married_joint": [{"rate": "0.0519", "start": "0"}], "cite": cite()},
        "surtaxes": [],
        "base": {"starts_from": "federal_agi", "cite": cite(),
                 "deductions": [{"id": "std", "what": "standard_deduction", "amount": {"single": "12000"}, "per": "return", "cite": cite()}]},
        "social_security": {"treatment": "exempt", "cite": cite()},
        "reliefs": [{"id": "ret_65", "label": "Retirement exclusion", "form": "subtraction",
                     "covers": ["private_pension", "ira_distribution"], "who": {"basis": "each_person", "min_age": 65},
                     "cap": {"all": "65000"}, "cap_per": "person", "cite": cite()}],
        "muni_interest": {"treatment": "other_states_taxed_own_exempt", "cite": cite()},
        "capital_gains": [],
        "indexing": [{"figure": "all_other", "indexed": "not_stated"}],
        "recapture": [],
    }
    data.update(over)
    return data


SOURCE = "rate is 5.19% and the cap is $65,000; standard deduction 12,000"


@pytest.fixture
def root(tmp_path, monkeypatch):
    monkeypatch.setattr(validate, "ROOT", tmp_path)
    (tmp_path / "schema").mkdir()
    for layer in ("record", "projection"):
        (tmp_path / "schema" / f"{layer}.schema.json").write_text(
            (validate.Path(__file__).resolve().parent.parent / "schema" / f"{layer}.schema.json").read_text())
    (tmp_path / "sources" / "archive" / "2025" / "ZZ").mkdir(parents=True)
    (tmp_path / "sources" / "archive" / "2025" / "ZZ" / "b.pypdf.txt").write_text(SOURCE)
    return tmp_path


def write(root, name, data):
    path = root / name
    path.write_text(json.dumps(data))
    return path


# Layer 1

def test_valid_record_passes(root):
    assert validate.validate(write(root, "ZZ.json", record())) == []


def test_number_instead_of_string_is_rejected(root):
    data = record()
    data["reliefs"][0]["cap"]["all"] = 65000
    assert any("schema" in p for p in validate.validate(write(root, "ZZ.json", data)))


def test_cite_without_section_is_rejected(root):
    data = record()
    del data["base"]["cite"]["section"]
    assert any("schema" in p for p in validate.validate(write(root, "ZZ.json", data)))


def test_figure_the_sources_never_print_is_flagged(root):
    data = record()
    data["reliefs"][0]["cap"]["all"] = "66000"
    assert any("66000" in p and "provenance" in p for p in validate.validate(write(root, "ZZ.json", data)))


def test_rate_is_found_as_a_percentage(root):
    (root / "sources" / "archive" / "2025" / "ZZ" / "b.pypdf.txt").write_text("rate 5.19 percent; cap 65000; 12000")
    assert validate.validate(write(root, "ZZ.json", record())) == []


def test_unknown_income_type_is_rejected(root):
    data = record()
    data["reliefs"][0]["covers"] = ["pensions"]
    assert any("schema" in p for p in validate.validate(write(root, "ZZ.json", data)))


# Layer 2

def projection(record_path, record_bytes, **over):
    data = {
        "layer": "projection", "state": "ZZ", "tax_year": 2025,
        "record": {"path": str(record_path), "sha256": hashlib.sha256(record_bytes).hexdigest()},
        "has_income_tax": True,
        "brackets": {"single": [{"rate": "0.0519", "start": "0"}], "married_joint": [{"rate": "0.0519", "start": "0"}]},
        "base": {"starts_from": "federal_agi", "deductions": []}, "derived_figures": [],
        "social_security": {"treatment": "exempt"},
        "reliefs": [{"id": "ret_65", "from_record": ["ret_65"], "form": "subtraction", "covers": ["private_pension", "ira_distribution"],
                     "who": {"basis": "each_person", "min_age": 65}, "cap": {"all": "65000"}, "cap_per": "person"}],
        "muni_interest": {"treatment": "other_states_taxed_own_exempt"}, "capital_gains": [],
        "indexing": [{"figure": "brackets", "indexed": False, "assumed": True, "covers": ["brackets", "surtaxes", "capital_gains", "recapture"]},
                     {"figure": "other_figures", "indexed": False, "covers": ["deductions", "reliefs.cap", "reliefs.income_test", "reliefs.credit_amount",
                                                                             "reliefs.applies_over", "reliefs.earned_income_limit"]}],
        "not_modelled": [], "approximations": [], "recapture": [],
    }
    data.update(over)
    return data


def test_valid_projection_passes(root):
    rec = write(root, "ZZ.json", record())
    assert validate.validate(write(root, "ZZ.p.json", projection(rec, rec.read_bytes()))) == []


def test_projection_of_a_changed_record_is_stale(root):
    rec = write(root, "ZZ.json", record())
    proj = write(root, "ZZ.p.json", projection(rec, rec.read_bytes()))
    rec.write_text(json.dumps(record(notes=["edited"])))
    assert any("stale" in p for p in validate.validate(proj))


def test_projection_naming_an_unknown_record_entry_is_rejected(root):
    rec = write(root, "ZZ.json", record())
    data = projection(rec, rec.read_bytes())
    data["reliefs"][0]["from_record"] = ["ret_62"]
    assert any("ret_62" in p for p in validate.validate(write(root, "ZZ.p.json", data)))


def test_projection_adding_a_figure_is_rejected(root):
    rec = write(root, "ZZ.json", record())
    data = projection(rec, rec.read_bytes())
    data["reliefs"][0]["cap"] = {"all": "70000"}
    assert any("70000" in p for p in validate.validate(write(root, "ZZ.p.json", data)))


# Comparison

def test_compare_reports_a_value_difference_and_ignores_wording_and_ids():
    a = record()
    b = copy.deepcopy(a)
    b["reliefs"][0]["cap"]["all"] = "35000"
    b["reliefs"][0]["label"] = "Retirement income exclusion"
    b["reliefs"][0]["id"] = "retirement_65_plus"
    structured, _ = compare.compare(a, b)
    assert len(structured) == 1 and "cap" in structured[0]


def test_compare_matches_reliefs_by_meaning_not_order():
    a = record()
    a["reliefs"].append({**copy.deepcopy(a["reliefs"][0]), "id": "ret_62", "who": {"basis": "each_person", "min_age": 62, "max_age": 64},
                         "cap": {"all": "35000"}})
    b = copy.deepcopy(a)
    b["reliefs"].reverse()
    assert compare.compare(a, b)[0] == []


def test_compare_treats_covers_as_a_set():
    a = record()
    b = copy.deepcopy(a)
    b["reliefs"][0]["covers"] = ["ira_distribution", "private_pension"]
    assert compare.compare(a, b)[0] == []


def test_compare_catches_a_missing_branch():
    a = record()
    b = copy.deepcopy(a)
    b["reliefs"].append({**copy.deepcopy(a["reliefs"][0]), "id": "pre1946", "who": {"basis": "older_spouse", "born_on_or_before": "1945-12-31"}})
    structured, _ = compare.compare(a, b)
    assert any("1945-12-31" in line for line in structured)


def test_projection_deductions_need_an_indexing_answer(root):
    rec = write(root, "ZZ.json", record())
    data = projection(rec, rec.read_bytes())
    data["base"]["deductions"] = [{"id": "std", "amount": {"single": "12000"}, "per": "return"}]
    data["indexing"][1]["covers"].remove("deductions")
    assert any("indexing" in p for p in validate.validate(write(root, "ZZ.p.json", data)))
    data["indexing"].append({"figure": "deductions", "indexed": False, "assumed": True, "covers": ["deductions"]})
    assert validate.validate(write(root, "ZZ.p.json", data)) == []


def test_compare_treats_an_uncapped_subtraction_as_exempt_in_full():
    a = record()
    a["reliefs"].append({"id": "gov", "label": "Government pensions", "form": "exempt_in_full", "covers": ["public_pension"],
                         "who": {"basis": "each_person"}, "cite": cite()})
    b = copy.deepcopy(a)
    b["reliefs"][1]["form"] = "subtraction"
    assert compare.compare(a, b)[0] == []


def test_record_accepts_a_fractional_age_and_not_stated_social_security(root):
    data = record()
    data["reliefs"][0]["who"]["min_age"] = 59.5
    data["social_security"]["treatment"] = "not_stated"
    assert validate.validate(write(root, "ZZ.json", data)) == []


def test_projection_derived_figure_is_checked(root):
    rec_data = record(surtaxes=[{"id": "s", "rate": "0.04", "over": {"all": "65000"}, "measure": {"base": "state_taxable_income"}, "cite": cite()}])
    (root / "sources" / "archive" / "2025" / "ZZ" / "b.pypdf.txt").write_text(SOURCE + " surtax 4%")
    rec = write(root, "ZZ.json", rec_data)
    data = projection(rec, rec.read_bytes())
    data["brackets"]["single"].append({"rate": "0.0919", "start": "65000"})
    data["derived_figures"] = [{"value": "0.0919", "how": "sum", "of": ["0.0519", "0.04"]}]
    assert validate.validate(write(root, "ZZ.p.json", data)) == []
    data["derived_figures"][0]["value"] = "0.0920"
    data["brackets"]["single"][1]["rate"] = "0.0920"
    assert any("not the sum" in p for p in validate.validate(write(root, "ZZ.p.json", data)))


def test_derived_brackets_must_reproduce_the_printed_table_and_formula():
    data = record()
    data["brackets"]["single"] = [{"rate": "0", "start": "0"}, {"rate": "0.03", "start": "3560"}, {"rate": "0.06", "start": "17830"}]
    data["brackets"]["married_joint"] = [dict(b) for b in data["brackets"]["single"]]
    data["brackets"]["derivation"] = {"method": "tax_table_and_formula",
        "table_rows": [{"status": "all", "income": "3025", "tax": "0"}, {"status": "all", "income": "10025", "tax": "193"},
                       {"status": "all", "income": "50025", "tax": "2359"}],
        "formula": {"over": "100000", "rate": "0.06", "minus": "642"}}
    assert validate.derivation_problems(data) == []
    data["brackets"]["single"][1]["start"] = "4000"
    assert any("table" in p or "formula" in p for p in validate.derivation_problems(data))


def test_rate_printed_without_leading_zero_is_found():
    assert ".007" in validate.spellings("rate", "0.007")


def test_stepped_income_test_and_credit_on_tax_are_valid(root):
    data = record()
    data["reliefs"][0]["income_test"] = {"measure": {"base": "federal_agi"}, "threshold": {"single": "75000"}, "effect": "stepped",
        "steps": [{"status": "single", "over": "75000", "keep_share": "0.85"}, {"status": "single", "over": "100000", "keep_share": "0"}]}
    data["reliefs"][0]["credit_basis"] = "tax"
    (root / "sources" / "archive" / "2025" / "ZZ" / "b.pypdf.txt").write_text(SOURCE + " 75,000 100,000 .85")
    assert validate.validate(write(root, "ZZ.json", data)) == []


def test_export_verified_only_holds_unverified_states(tmp_path):
    from tools import export
    if any(validate.sources_missing(st, 2025) for st in ("GA", "US")):
        pytest.skip("source documents not pulled (uv run python -m tools.sources pull --year 2025)")
    code = export.main(["--year", "2025", "--version", "test-verified-only", "--out", str(tmp_path), "--verified-only"])
    assert code == 0
    manifest = json.loads((tmp_path / f"{export.NAME}-test-verified-only" / "manifest.json").read_text())
    for st in manifest["held"]:
        assert st not in manifest["states"]
        assert st not in manifest["not_yet_settled"]
    assert set(manifest["states"]) & set(manifest["held"]) == set()


def test_checks_flag_an_approximation_text_the_projection_no_longer_has(tmp_path, monkeypatch):
    import shutil
    from tools import checks
    real = checks.ROOT
    (tmp_path / "data" / "states" / "2025").mkdir(parents=True)
    shutil.copy(real / "data" / "states" / "2025" / "NC.projection.json", tmp_path / "data" / "states" / "2025")
    shutil.copytree(real / "checks" / "2025" / "NC", tmp_path / "checks" / "2025" / "NC")
    monkeypatch.setattr(checks, "ROOT", tmp_path)
    assert checks.state_problems(2025, "NC", require_verified=False) == []
    path = tmp_path / "checks" / "2025" / "NC" / "nc_2025_base.json"
    case = json.loads(path.read_text())
    case["accepted_approximations"] = ["An approximation the projection dropped."]
    path.write_text(json.dumps(case))
    problems = checks.state_problems(2025, "NC", require_verified=False)
    assert any("nc_2025_base.json: accepted_approximations quotes text" in p for p in problems)


def test_format_v1_shape_rules(root):
    rec = write(root, "ZZ.json", record())
    base = projection(rec, rec.read_bytes())
    relief = base["reliefs"][0]
    cases = {
        "needs a width": dict(relief, income_test={"measure": {"base": "federal_agi"}, "threshold": {"all": "65000"}, "effect": "share_phase_out"}),
        "not a relief here": dict(relief, income_test={"measure": {"base": "federal_agi", "minus_reliefs": ["nope"]}, "threshold": {"all": "65000"}, "effect": "removes"}),
        "refundable is for credits only": dict(relief, refundable=True),
        "must also be an approximations entry": dict(relief, assumption={"what": "Assumed to qualify.", "warn_when": "has_pension"}),
    }
    for message, changed in cases.items():
        problems = validate.validate(write(root, "ZZ.p.json", dict(base, reliefs=[changed])))
        assert any(message in p for p in problems), (message, problems)
    good = dict(relief, income_test={"measure": {"base": "federal_agi"}, "threshold": {"all": "65000"}, "effect": "share_phase_out", "width": {"all": "65000"}, "share_decimals": 4},
                assumption={"what": "Assumed to qualify.", "warn_when": "has_pension"})
    approx = [{"what": "Assumed to qualify.", "direction": "understates_tax", "size": "small"}]
    assert validate.validate(write(root, "ZZ.p.json", dict(base, reliefs=[good], approximations=approx))) == []


def test_warning_triggers_for_retirement_accounts_gains_and_income():
    from tools import checks
    case = {"state": "MS", "inputs": {"filing_status": "single", "federal_agi": "400000",
            "persons": [{"age": 50}], "income": {"ira_distribution": [{"amount": "30000", "person": 0}], "long_term_gains": "100"}}}
    assert checks.trigger_fires({"warn_when": "has_retirement_account_distribution", "age_range": [0, 59]}, case)
    assert not checks.trigger_fires({"warn_when": "has_retirement_account_distribution", "age_range": [60, 200]}, case)
    assert checks.trigger_fires({"warn_when": "has_long_term_gains"}, case)
    over = {"warn_when": "income_over", "income_over": {"measure": {"base": "federal_agi"}, "threshold": {"all": "350000"}}}
    assert checks.trigger_fires(over, case)
    case["inputs"]["federal_agi"] = "350000"
    assert not checks.trigger_fires(over, case)
    projection = {"not_modelled": [], "reliefs": [{"id": "usr", "assumption": {"what": "x", "warn_when": "has_retirement_account_distribution"}}]}
    assert checks.expected_warnings(projection, case) == ["state_assumption:usr"]


def test_later_fields_must_be_listed_in_requires(root):
    rec = write(root, "ZZ.json", record())
    base = projection(rec, rec.read_bytes())
    relief = dict(base["reliefs"][0], applies_over={"measure": {"base": "federal_agi"}, "threshold": {"all": "65000"}})
    problems = validate.validate(write(root, "ZZ.p.json", dict(base, reliefs=[relief])))
    assert any("applies_over must be listed in requires" in p for p in problems)
    relief["requires"] = ["applies_over"]
    assert validate.validate(write(root, "ZZ.p.json", dict(base, reliefs=[relief]))) == []


def test_federal_figures_must_be_printed_in_the_document_they_cite(root):
    (root / "schema" / "federal.schema.json").write_text((validate.Path(__file__).resolve().parent.parent / "schema" / "federal.schema.json").read_text())
    archive = root / "sources" / "archive" / "2025" / "US"
    archive.mkdir(parents=True)
    (archive / "fetch.json").write_text(json.dumps([
        {"url": "https://www.irs.gov/a.pdf", "final_url": "https://www.irs.gov/a.pdf", "file": "a.pdf", "ok": True},
        {"url": "https://www.irs.gov/b.pdf", "file": "b.pdf", "ok": True}]))
    (archive / "a.docling.md").write_text("standard deduction $15,750 for single; rounded down to a multiple of $50")
    (archive / "b.pypdf.txt").write_text("married filing jointly $31,500")
    a = {"publication": "A", "section": "p.1", "url": "https://www.irs.gov/a.pdf", "accessed": "2026-11-07"}
    item = {"amount": {"single": "15750", "married_joint": "31500"}, "cite": dict(a),
            "indexing": {"method": "inflation", "index": "C-CPI-U", "rounding": {"multiple": "50", "direction": "down"}, "cite": dict(a)}}
    data = {"layer": "federal", "jurisdiction": "US", "tax_year": 2025,
            "income_tax": {"standard_deduction": item}, "medicare": {}, "payroll": {}, "retirement_accounts": {}, "rmd": {}}
    found = validate.federal_problems(data)
    assert found == ["provenance: income_tax.standard_deduction.amount.married_joint=31500 is not printed in the document income_tax.standard_deduction cites"]
    item["cite"]["also"] = [{"url": "https://www.irs.gov/b.pdf", "section": "p.2"}]
    assert validate.federal_problems(data) == []
    item["indexing"]["cite"]["url"] = "https://www.irs.gov/missing.pdf"
    assert validate.federal_problems(data) == ["provenance: income_tax.standard_deduction.indexing cites https://www.irs.gov/missing.pdf, which is not an archived source"]


def test_federal_checks_coverage_and_age_rule(tmp_path, monkeypatch):
    from tools import federal_checks
    monkeypatch.setattr(federal_checks, "ROOT", tmp_path)
    (tmp_path / "data" / "federal" / "2025").mkdir(parents=True)
    (tmp_path / "data" / "federal" / "2025" / "US.federal.json").write_text(json.dumps(
        {"income_tax": {"brackets": {}, "net_investment_income_tax": {}}}))
    cases = tmp_path / "checks" / "2025" / "US"
    cases.mkdir(parents=True)
    case = {"id": "US-2025-base", "jurisdiction": "US", "tax_year": 2025, "kind": "income_tax", "boundary": "below",
            "tests": ["income_tax.brackets", "income_tax.net_investment_income_tax"], "description": "d",
            "inputs": {"filing_status": "single", "persons": [{"born": "1960-01-01", "age": 65}]},
            "expected": {"regular_tax": "100.00"}, "worked": "w"}
    (cases / "US-2025-base.json").write_text(json.dumps(case))
    count, problems = federal_checks.problems_for(2025, require_verified=True)
    assert count == 1
    assert problems == [
        "US-2025-base.json: not verified by a second working",
        "US-2025-base.json: person 0 born 1960-01-01 has age 65; by the tax rule it is 66",
        "'income_tax.net_investment_income_tax' has no 'at_or_above' case",
    ]


def test_federal_derivations_are_redone_exactly():
    c = {"publication": "A", "section": "p.1", "url": "https://www.irs.gov/a.pdf", "accessed": "2026-11-08"}
    group = {"amount": {"single": "15750", "married_joint": "31500", "married_separate": "15750"},
             "derivations": [
                 {"target": "amount.married_joint", "rule": "times", "from": "amount.single", "factor": "2", "cite": c},
                 {"target": "amount.married_separate", "rule": "times", "from": "amount.married_joint", "factor": "0.5", "cite": c}]}
    data = {"income_tax": {"standard_deduction": group}}
    assert validate.federal_derivation_problems(data) == [
        "derivation: income_tax.standard_deduction: amount.married_separate is set from a figure that is itself derived"]
    group["derivations"][1]["from"] = "amount.single"
    group["derivations"][1]["factor"] = "1"
    group["amount"]["married_joint"] = "31000"
    assert validate.federal_derivation_problems(data) == [
        "derivation: income_tax.standard_deduction.amount.married_joint=31000; its rule gives 31500"]
    tiers = {"tiers": [{"over": {"single": "106000", "married_separate": "106000"}}, {"over": {"single": "500000", "married_separate": "394000"}}],
             "derivations": [{"target": "tiers[1].over.married_separate", "rule": "minus", "from": "tiers[1].over.single", "subtract": "tiers[0].over.single", "cite": c}]}
    assert validate.federal_derivation_problems({"medicare": {"irmaa": tiers}}) == []


def test_indexing_covers_markers_ids_senior_deduction_and_other_rule(root):
    rec = write(root, "ZZ.json", record())
    data = projection(rec, rec.read_bytes())
    data["indexing"] = [{"figure": "brackets", "indexed": True, "covers": ["brackets"]},
                        {"figure": "caps", "indexed": False, "covers": ["reliefs.cap"]},
                        {"figure": "ret_cap", "indexed": True, "covers": ["reliefs:ret_65.cap", "reliefs:nope"]}]
    data["reliefs"][0]["income_test"] = {"measure": {"base": "federal_agi"}, "threshold": {"all": "100000"}, "effect": "lose_all"}
    data["not_modelled"] = [{"id": "a", "from_record": [], "what": "x", "warn_when": "never"}, {"from_record": [], "what": "y", "warn_when": "never"},
                            {"id": "a", "from_record": [], "what": "z", "warn_when": "never"}]
    data["base"]["starts_from"] = "federal_taxable_income"
    data["recapture"] = [{"measure": {"base": "federal_agi"}, "starts_over": {"all": "150000"}, "full_rate": "0.03", "effect": "other"}]
    found = validate.projection_shape_problems(data)
    for message in ("indexing: 'ret_cap' covers reliefs:nope, but there is no reliefs 'nope'",
                    "indexing: no entry covers reliefs:ret_65.income_test",
                    "indexing: no entry covers recapture",
                    "not_modelled[1]: no id", "not_modelled[2]: id 'a' is used twice",
                    "base: a state that starts from federal taxable income needs federal_senior_deduction",
                    "recapture[0]: other_rule goes with effect other, and only with it"):
        assert message in found, (message, found)
    assert not any("reliefs:ret_65.cap" in p for p in found)  # the specific entry wins over the general one
    data["indexing"].append({"figure": "caps2", "indexed": False, "covers": ["reliefs.cap"]})
    data["indexing"][2]["covers"] = ["reliefs:ret_65.income_test"]
    assert "indexing: reliefs:ret_65.cap is covered by more than one entry at the same level: caps, caps2" in validate.projection_shape_problems(data)
