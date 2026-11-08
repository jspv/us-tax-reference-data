# Settlement: Colorado, tax year 2025 (round r5)

Settled 2026-11-07 from `work/extract/2025/CO.r5.A.json` and `CO.r5.B.json`.
Sources: `sources/archive/2025/CO/Book104_2025` (the 2025 DR 0104 booklet; it also holds the DR 0104 form, PDF p.37-44, the DR 0104AD schedule, PDF p.51-53, and the DR 0104PN, PDF p.63-69) and `DR0104AD_2025` (the DR 0104AD schedule on its own). Page numbers are PDF pages.

**Missing source.** The Department page "Income Tax Topics: Social Security, Pensions and Annuities" (`https://tax.colorado.gov/income-tax-topics-social-security-pensions-and-annuities`) could not be fetched (`fetch.json`: ok false, "Page.goto: Timeout 90000ms exceeded"). The booklet sends the reader to it four times. Had it been in the sources, it would have settled:
- **PERA/DPSRS (line 14):** whether, and how much of, a pension may be subtracted for PERA contributions made July 1, 1984 to December 31, 1986, or Denver Public Schools contributions made in 1986. The booklet prints no amount ("see Department publication ... to determine if you can take a subtraction for any of your pension income", p.22), so the record entry has no cap and the projection leaves it in `not_modelled`.
- **Joint returns where both spouses get Social Security** (p.18 Line 3, p.19 Line 5): how the taxable benefit on Form 1040 line 6b is split between the spouses' lines 3 and 5.
- Possibly whether line 4 takes military retirement pay at 55 or older, Roth conversions, and other states' government pensions. The booklet is silent on all three.

`uv run python -m tools.compare` reported **48 structured differences** (114 wording). All of them are in `reliefs` (47) or `muni_interest` (1). All 48 come from three disagreements:
- the pension tiers' `covers` / `covers_unclear`, which made the three tiers of each reader key differently;
- the PERA entry's `who.basis`;
- the municipal interest treatment.

All 48 were decided from the booklet. None was dropped on scope: no entry is truly one-sided, because each "one-sided" difference is one of the two readers' versions of the same rule, keyed apart.

## Structured differences

| # | Entry (compare key) | Fields | A | B | Settled | Page |
|---|---|---|---|---|---|---|
| 1 | Pension and Annuity Subtraction, 65 or older (line 4/6) | 13 (A 6, B 7: unmatched because `covers` differ) | `covers` includes `public_pension_other_state`; no `covers_unclear` | `public_pension_other_state`, `military_pension`, `roth_conversion` in `covers_unclear` | **`public_pension_other_state` in `covers` (A); `military_pension` and `roth_conversion` in `covers_unclear` (B).** Cap 24,000 per person, less the line 3 Social Security subtraction (both). "Do not enter any social security benefits on line 4" moved into `not_covered` (B; A had it in `other_conditions`). SSDI is added to `not_covered` from the form line. | p.18-19 Line 4: "You might be eligible to subtract the income you earned from a pension or annuity ... This subtraction is allowed only for pension or annuity income that is included in your federal taxable income ... Age 65 or older, then you may subtract $24,000 minus any amount entered on line 3". DR 0104AD line 4 (p.51; DR0104AD p.1): "Pension, Annuity, IRA, or Disability Income (not including SSDI)". |
| 2 | Pension and Annuity Subtraction, 55-64 | 15 (A 7, B 8) | as row 1 | as row 1 | As row 1; cap 20,000 less line 3. | p.19 Line 4 second bullet: "At least 55 years old, but not yet 65, then you may subtract $20,000 minus any amount entered on line 3". |
| 3 | Pension and Annuity Subtraction, under 55, secondary beneficiary | 13 (A 6, B 7) | as row 1 | as row 1 | As row 1; cap 20,000 less line 3; the beneficiary test is in `other_conditions`. | p.19 Line 4 third bullet: "Younger than 55 years old and you received pension/annuity income as a secondary beneficiary (widow, dependent child, etc.)". |
| 4 | PERA/DPSRS Subtraction (line 14) | 6 (A 3, B 3: the compare reads an uncapped subtraction as `exempt_in_full` and keyed the entries apart on `who.basis`) | `basis` return | `basis` each_person, plus "contributory plan" | **return (A).** Line 14 is one line per return with no spouse line and no age test, and rule 5 gives `return` when neither spouse's age is tested. B's generic "contributory plan" is not added. The test is contributions made in a fixed window (1984-1986 PERA, 1986 DPS), and that window is written out; the generic phrase would read as any contributory plan. The form stays `subtraction` with no cap: the booklet prints no amount, and B's `cap_rule` wording saying so is kept. | p.22 Line 14: "If you made contributions to PERA between July 1, 1984, and December 31, 1986, or to Denver Public Schools District No. 1 Retirement during 1986 and your 2024 federal taxable income includes pension income, see Department publication ..."; DR 0104AD line 14 (p.52). |
| 5 | `muni_interest.treatment` | 1 | other | other_states_taxed_own_exempt | **other_states_taxed_own_exempt (B)**, with Colorado bonds issued before May 1, 1980 named in `note` as also added back. That is the main rule; the pre-1980 carve-out is an exception to it, not a different scheme. | p.10 Line 9: "Bond interest: Interest earned from bonds issued by any state or political subdivision, but not bonds issued by the State of Colorado or its political subdivisions on or after May 1, 1980." |

Total: 13 + 15 + 13 + 6 + 1 = 48, all decided from the booklet.

### Why `public_pension_other_state` is in `covers` (rows 1-3)

- Both readers put `public_pension` and `private_pension` in `covers` on the same generic words, "pension or annuity". Nothing in the booklet limits those words to Colorado's own or to federal government pensions, names another state, or prints a reciprocity rule.
- So a pension paid by another state's government is in the same entries as Colorado's own, by rule 15a's first case. This is the reading taken for Maryland, where the booklet "sets no Maryland-only limit".
- B left it unclear because the booklet does not name other states' pensions. That is true. But the booklet does not name Colorado's own government pensions either, and B still put `public_pension` in `covers`. It cannot be read as covering one and not the other.

### Why `military_pension` stays unclear (rows 1-3)

- The booklet treats military retirement separately. Line 7 is a 15,000 subtraction for people "54 years of age or younger", and DR 0104AD line 7 reads "Military Retirement Benefits (under age 55)".
- The booklet never says whether line 4 takes military retirement at 55 or older. A noted it as not found; B put it in `covers_unclear`. B's way records the gap in a field, so B is kept.
- Roth conversions are not mentioned anywhere (B), so they stay unclear as well.

### Not flagged by the compare, but settled

- **Brackets derivation.** Neither reader recorded one. The tax comes from a printed table (below 50,000) and a worksheet (above), so `brackets.derivation` now holds the evidence. Method `tax_table_and_formula`, four rows with status `all` (the table has no filing-status columns), at the row midpoint:
  - 100-200 → 7 (p.34)
  - 10,000-10,100 → 442 (p.34)
  - 25,000-25,100 → 1,102 (p.34)
  - 49,900-50,000 → 2,198 (p.35)
  - The formula is over 50,000, rate .044, minus 0, from p.35: "Worksheet for taxable incomes over $50,000 ... Multiply by 4.4% ... X .044".
  - 4.4% of each midpoint, rounded, matches the printed tax, and the validator re-computes all four rows and the formula.
- **Entry ids** take a `co_` prefix (B's style). The 55-64 limited Social Security entry is named `co_ss_55_64_limited` after the booklet's word, "limited to $20,000".
- **Cite pages.** B cited the over-50,000 worksheet as p.34; it is on p.35. A cited the start of Line 4 as p.19; it starts on p.18.

## One-sided entries

None. Both readers recorded the same 12 rules:
- Social Security at 65 or older, at 55-64 (two branches), and under 55;
- pensions at 65 or older, at 55-64, and under 55;
- military retirement under 55;
- PERA/DPSRS;
- railroad;
- U.S. government interest;
- the agricultural land gain.

Both readers also left the same non-retirement DR 0104AD lines out of `reliefs`; they are listed in `notes`.

## The five facts to settle

1. **Another state's government pension, and a New York State pension in particular.** It is in `covers` as `public_pension_other_state`, in the same three pension entries as Colorado's own. There is no `paying_states`: the booklet names no state, so New York is treated like any other state.
   - Quote, p.18 Line 4: "You might be eligible to subtract the income you earned from a pension or annuity ... This subtraction is allowed only for pension or annuity income that is included in your federal taxable income."
   - Rule for a Colorado resident with a New York State pension: the pension and annuity subtraction on DR 0104AD line 4 (line 6 for the spouse). At 65 or older, up to 24,000 less the person's Social Security subtraction. At 55-64, up to 20,000 less that subtraction. Under 55, only as a secondary beneficiary. The rest is taxed at 4.4%.
2. **Colorado's own and federal government pensions.** Same entries, `public_pension`, same caps, on the same words (rule 1).
   - The PERA/DPSRS line 14 subtraction for 1984-1986 contributions is a separate entry with no printed amount (see "Missing source").
   - Military retirement has its own line 7 subtraction, 15,000 per person, only at 54 or younger (p.20; DR 0104AD line 7 "(under age 55)").
   - Railroad retirement included in federal taxable income is subtracted with no printed cap (p.22 Line 15).
3. **Private pensions, IRA and employer-plan distributions, Roth conversions.**
   - Private pensions, annuities, IRA distributions and employer-plan distributions are in `covers`.
   - The form line names IRA income outright: DR 0104AD line 4 "Pension, Annuity, IRA, or Disability Income".
   - Second document: DR 0104PN line 12 (p.65) sums Form 1040 "lines 4b, 5b, and 6b", and its line 31 (p.68) places "The pension/annuity subtraction ... to the extent included on line 13".
   - Employer-plan distributions rest on "pension or annuity" and on the instruction to submit "all 1099R statements". Both readers listed them.
   - Roth conversions: not mentioned, so `covers_unclear`.
4. **Social Security: relief**, by age at December 31, 2025 (p.18 Line 3; p.19 Line 5; DR 0104AD lines 3 and 5 "Social Security Benefits (including SSDI) received that were included in Federal Taxable Income").
   - 65 or older: the entire taxable amount ("you may claim the subtraction for the entire amount").
   - 55-64: the entire amount if single with federal AGI (DR 0104 line 34) not over 75,000, or joint not over 95,000; otherwise "limited to $20,000".
   - Under 55: only benefits received because of a death, up to 20,000.
   - Checked against the second document, DR0104AD p.1 lines 3 and 5.
   - The Social Security subtraction uses up the pension cap (p.19).
5. **Brackets, deductions and exemptions.**
   - Rate: one flat 4.4% for every filing status. p.10 Line 13: "The income tax rate is currently 4.4%". The table title on p.34 reads "with tax rate of 4.4%", and the worksheet on p.35 multiplies by .044. The table has no status columns, so only single and joint are given; the other statuses fall back to single, which here is the same.
   - The return starts from federal taxable income: p.8 Line 1, "Form 1040 ... line 15"; form p.39 line 1.
   - The booklet prints no standard deduction, personal exemption, dependent exemption, or age or blindness amount of its own. A search for "standard deduction" and "exemption" finds only the line 4 federal deduction addback.

## Projection choices (`CO.projection.json`)

- **Base and brackets.**
  - `starts_from` is federal_taxable_income, because Colorado law starts there; there are no state deductions.
  - Brackets: 4.4% from 0 for single and joint.
- **Social Security** (relief):
  - 65 or older: `exempt_in_full`.
  - 55-64: two entries in one best_of_group. The full subtraction is removed above 75,000 (single) or 95,000 (joint) federal AGI; the alternative is limited to 20,000 a person.
  - Under 55 (survivor benefits only): `not_modelled`, warn `person_in_age_range` 0-54.
- **Pension subtraction.**
  - 65 or older: 24,000. 55-64: 20,000. Both per person, and both carry `needs_input: [pension_source]`, because military pensions must be told apart: they are left out of these covers and have their own entry.
  - `cap_reduced_by: [social_security]`. That reproduces "24,000 minus any amount entered on line 3" exactly when the line 3 amount is the full taxable benefit. In the 20,000-limited case the cap is used up either way.
  - The under-55 beneficiary tier is `not_modelled` (warn `has_pension`).
- **Military retirement under 55:** 15,000 a person (`pension_source`). **Railroad benefit:** `exempt_in_full`.
- **`not_modelled`:**
  - PERA/DPSRS (`has_pension`);
  - U.S. government interest (`never`), with an overstating approximation;
  - the agricultural land gain (`never`).
- **Approximations:**
  - the table-midpoint rounding;
  - the line 4 federal deduction addback above 300,000 AGI, and the line 2 and line 3 addbacks (all understate tax);
  - how a joint return's taxable Social Security is split between spouses for the pension cap;
  - Roth conversions and military retirement at 55 or older left out of the pension subtraction (both overstate tax, at most 4.4% x 24,000 = 1,056 a person a year);
  - the missing head of household and separate-filer thresholds;
  - all municipal interest treated as other-state;
  - Treasury interest taxed.
- **Indexing:** brackets and relief caps, `indexed: false, assumed: true`; the booklet is silent.
- `derived_figures` is empty. Every figure in the projection is printed in the record.

Validator: both files `ok`.

## Page numbers

`Book104_2025.docling.md` has only 83 page markers for the 88-page PDF, because Docling skipped some page breaks, so its page numbers drift low after the skipped pages. Every page cited in the record and in this log is taken from `Book104_2025.pypdf.txt`, whose 88 markers match the PDF (checked with pypdf: 88 pages). Each cited page was then re-checked by finding a phrase from it in the pypdf text: 30 phrases across PDF pp.8, 9, 10, 13, 18-20, 22, 34-35, 39-40, 51-52, 65 and 68, all on the page cited.

The readers' own cites agree with the pypdf pages except the two corrected above (B's worksheet p.34 → p.35; A's Line 4 start p.19 → p.18).

## Unsure

- **`public_pension_other_state` in covers** rests on the absence of any payer limit in "pension or annuity", not on words naming other states. The unfetched Department page may say more.
- **Military retirement at 55 or older** is left unclear. If line 4 takes it, the projection overstates tax by up to 1,056 a person a year.
- **Head of household and separate filers aged 55-64:** the booklet prints no Social Security threshold for them. Read literally, they get only the 20,000-limited subtraction. The record holds the two printed thresholds, and the projection logs the gap.
- **Employer-plan distributions** (401(k), 403(b)) are in `covers` on "pension or annuity" and the 1099R instruction, not on words naming them.

- Main session, 2026-11-07 (format v1): `social_security_basis: taxable` set on the relief(s) whose cap Social Security reduces, stating what the cases already used.

## 2026-11-08: marker ids and indexing covers

- Marker ids given: first from_record id (warning code unchanged): `co_ss_under_55_survivor`, `co_pension_under_55_survivor`, `co_pera_dpsrs_1984_1986`, `co_us_government_interest`, `co_ag_land_capital_gain`.
- Indexing covers: `brackets` -> `brackets`; `relief_caps` -> `reliefs.cap`; `relief_income_tests` -> `reliefs.income_test`.
- Added `relief_income_tests` (indexed false, assumed) for the 55-64 Social Security AGI test (75,000 / 95,000).
- Every `assumed` answer was checked again against the archived sources (searched for indexed, inflation, cost-of-living, adjusted annually, each year, CPI, fixed): none says, so all stay `assumed: true`.
- Warning codes unchanged (every id is the marker's first from_record id).
