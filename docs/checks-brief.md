# Checks brief: hand-worked cases for one state

Each case is one household, worked from the state's own 2025 form or worksheet, that a consumer
(a projection engine that evaluates the data) converts to a test case of its own. Format:
`schema/check.schema.json`. Coverage the release gate enforces (`tools/checks.py`):

- one `base` case: a plain return (wages and/or a pension, standard deduction), no special relief;
  a state with no income tax gets one `no_tax` case instead (state_income_tax "0");
- for each relief or credit in the projection with a cap, an income test or a fixed credit amount: one case
  `boundary: "below"` (income under the cap or limit) and one `"at_or_above"` (at or over it);
- for every other relief, and every `base.deductions` entry, at least one case;
- `edge` cases where the state has them: whose age counts (older spouse, each person), a pension paid by
  another state's government (always include a New York State pension case where the state treats other
  states' pensions differently), can't-combine or take-the-better-of choices, joint returns with one
  qualifying spouse.

One case may test several ids (list them all in `tests`), but each relief needs its own below and
at-or-above cases.

## How to write a case

1. **Pick inputs that make the rule bite**, in round numbers. Income items are per person (`person` 0 or 1);
   pensions say `source`, `paying_government`, `contributory` where the rule turns on them.
2. **Federal figures are given, not tested.** Set `federal_agi` to the sum the federal return would show
   (wages, pensions, IRA and plan distributions, taxable Social Security, interest including Treasury,
   dividends, gains; not municipal interest). Set `federal_taxable_income` to `federal_agi` minus the 2025
   federal standard deduction: 15,750 single or married separate, 31,500 joint or qualifying surviving
   spouse, 23,625 head of household, plus 2,000 per person 65 or older (single, head of household) or 1,600
   (married); ignore the federal senior deduction and say so in `worked`. A case tests only the state part.
3. **Work the state's own form**, line by line, and write each line in `worked`: start (federal AGI or
   federal taxable income, as the projection's `base.starts_from`), additions, subtractions (each relief),
   deductions, taxable income, tax, credits.
4. **Compute to the cent with the projection's own rules**: the bracket schedule as numbers (never the printed
   tax table), no whole-dollar rounding. Where the form rounds or uses a table, put the formula result in
   `expected` and note the form's own figure in `worked` ("the table gives 1,234").
5. **Where the projection simplifies** (an `approximations` entry) or leaves a rule `not_modelled`, compute
   what the projection does and list the approximation text in `accepted_approximations`. Don't choose
   `accepted_warnings` yourself: `uv run python -m tools.checks --year 2025 --state <ST> --fix-warnings` sets
   them from the projection's markers and the inputs (has_pension fires for any pension item, any source or kind).
5b. **Ages follow the tax rule**: a person reaches an age the day before the birthday, so `age` is the age at December 31 counting that rule: only a January 1 birthday moves up (born 1961-01-01 is 65 for 2025; born 1961-01-02 is 64). The coverage check enforces it.
5c. **Municipal interest**: the inputs separate own-state from other-state interest, so a case follows `muni_interest.treatment`, not the approximation for a projection that can't tell them apart. List that approximation only if a case truly depends on it.
5d. **Married separate returns**: `persons` may list both spouses where the rule depends on the spouse (Mississippi, Kansas). A per-person deduction then counts both, and the projection's amount is set so that gives the form's result; all income belongs to person 0 unless a person says otherwise.
5e. **Credit relief amounts**: `relief_amounts` gives each credit's worksheet figure before the limit to the tax; `credits` is the total of the nonrefundable credits limited to `state_tax_before_credits`, plus refundable credits in full, so `state_income_tax` goes below 0 when a refundable credit is larger than the tax that is left.
5f. **Warnings** come only from `tools.checks --fix-warnings`: `state_rule_not_modelled:<id>` for a not_modelled marker whose trigger fires, `state_assumption:<relief id>` for a relief applied on an assumption.
5a. **Taxable income is floored at 0** in `expected`; if the form allows a negative figure, note it in `worked`.
6. **Cite** `source.section` with the form lines or worksheet lines the case follows, and the record's cite
   for the rule.
7. `id`: `<st>_2025_<short_name>`, lower case. One file per case in `checks/2025/<ST>/<id>.json`.

## Verification (second working)

A second worker gets each case's `inputs`, `tests`, `kind`, `boundary` and `source` (not `expected` or
`worked`), works it independently from the same sources, and writes its own expected lines.
`tools/checks_compare.py` compares to the cent: agreement adds the `verified` block; a disagreement is
settled against the booklet and the case corrected (`verified.result: "corrected"`).

## Rules

- Figures come from the state's sources and the settled record/projection only; no other dataset.
- Write helper scripts only in the private folder your dispatch names.
- Never run a recursive delete built from a variable; delete nothing except files you wrote in your folder.
