# Settlement: Arizona, tax year 2025

- Readings: `work/extract/2025/AZ.r5.A.json`, `work/extract/2025/AZ.r5.B.json` (round r5)
- Sources: `sources/archive/2025/AZ/` (2025 Arizona Form 140 Resident Personal Income Tax Booklet, with the
  Form 140 itself on PDF pages 39-44; agency web page "Identifying Other Taxable Income")
- Outputs: `data/states/2025/AZ.record.json`, `data/states/2025/AZ.projection.json`
- Settled: 2026-11-07

## Comparison

`uv run python -m tools.compare` reported **11 structured differences** (66 wording differences). They are
three disagreements:

| # | Lines | Field | A | B | Source | Settled |
|---|---|---|---|---|---|---|
| 1 | 4 | `brackets.married_separate`, `brackets.head_of_household` | each 2.5% from 0 | not given | PDF page 5: "2025 New Tax Rate of 2.5% for All Income Levels and Filing Status"; PDF page 26 Line 46 and form line 46 (PDF page 40): "Multiply line 45 by 2.5% (.025)". One rate, no schedule printed for either status. | B: single and married_joint only (the schema gives the other lists only when the booklet prints their own schedule; same as NC) |
| 2 | 6 (2 relief keys x covers, form, who.basis) | Line 30 Social Security / railroad relief `who.basis` | `each_person` | `return` | PDF page 20 Line 30: "If you included such social security or railroad retirement benefits as income on your federal return, use line 30 to subtract this income. ... Enter only the taxable amount (the amount that was subject to federal income tax)." No test on either spouse. | `return` (schema: `return` when neither spouse is tested; same as the NC Line 18 settlement) |
| 3 | 1 | `indexing` third entry | `brackets: not_stated` (plus standard_deduction, all_other) | only standard_deduction and all_other | The booklet says nothing on adjusting the rate; not_stated either way. | A's `brackets` entry kept so the rate has an explicit answer. Not a booklet decision. |

Decided from the booklet: 10 of 11 lines (#1 and #2). #3 is a format choice; the answer (not_stated) is the
same in both readings.

## One-sided entries and field choices

- Line 29b military `cap_rule` (B only): kept ("100% ... no cap printed; each spouse ..."), with the surviving
  spouse sentence moved there from A's `other_conditions` (it widens who qualifies; it is not a test a planner
  may not know).
- Line 29a qualifying-source list: kept in `who.other_conditions` (both had it); "only the amount reported as
  income on the federal return" moved to `cap_rule` (a measure, not a test).
- Line 28 and Line 30 descriptive `other_conditions` (A): moved to `cap_rule` and notes, as in NC.
- Indexing cites: kept only on `standard_deduction` (the "Adjusted" heading is the evidence); dropped on the
  others.
- A's Dependent Tax Credit figures (100 / 25, AGI 200,000 / 400,000, Table V steps): B said the amounts were
  not found; they are printed on PDF pages 26-27. Kept in `notes` only (no record field holds a dependent
  credit); in the projection as an approximation.
- American Indian wages (line 31), lump-sum averaging addition (other addition C, PDF page 14), family income
  credit (line 50): notes only, not retirement reliefs.
- Standard deduction: added the booklet's rule that a federal qualifying widow(er) files as head of household
  (PDF page 10, Box 5), in the condition and notes; neither reader had it.
- IDs normalised: `az_gov_pension_exclusion`, `az_military_retirement_exclusion`,
  `az_social_security_railroad_subtraction`, `az_us_obligations_interest_subtraction`,
  `az_armed_forces_pay_subtraction`, `other_exemption`, `qualifying_parent_grandparent_exemption`,
  `az_ltcg_post_2011_subtraction`.

## The five facts, each with a quote

1. **Another state's government pension, a New York State pension included: taxed in full (as federally).**
   PDF page 20, Line 29a: "NOTE: Public retirement pensions from states other than Arizona do not qualify for
   this subtraction." Second source, the web page: "Arizona law states that residents are taxed on the same
   income they report for federal purposes, including income earned and retirement from other states." In
   `not_covered` of `az_gov_pension_exclusion`; no entry covers `public_pension_other_state`. New York is not
   named; the rule covers every state other than Arizona (no reciprocity, so no `paying_states`).
2. **Own and federal government pensions: up to 2,500 per person subtracted.** PDF page 19, Line 29a: "If you
   received pension income from any of the sources listed below, subtract the amount you received or $2,500,
   whichever is less. ... If both you and your spouse receive such pension income, each spouse may subtract the
   amount received or $2,500, whichever is less." Form line 29a (PDF page 39): "Exclusion for federal, Arizona
   state or local government pensions (up to $2,500 per taxpayer)". No age, income or contributory test.
   Military retired pay: 100% (Line 29b, PDF page 20; form line 29b).
3. **Private pensions, IRA and employer-plan distributions, Roth conversions: no relief; taxed as federally.**
   Not found in the booklet as covered by any subtraction. Web page: "as a general rule, the same portion of an
   individual's pension is taxable for Arizona purposes as it is for federal." Roth conversions are not
   mentioned (not found in the booklet). The only related lines: Line 28 does not let pension or IRA amounts
   from funds holding U.S. obligations count as interest (PDF page 19).
4. **Social Security: exempt.** PDF page 20, Line 30: "Arizona does not tax the following: Social security
   benefits received under Title II of the Social Security Act." Second line: form line 30 (PDF page 39) and the
   filing-requirement list on PDF page 6 ("Income that Arizona law does not tax includes: ... social security
   retirement benefits received under Title II").
5. **Rate, standard deduction, exemptions.** Rate 2.5% for every status (PDF page 5; PDF page 26 Line 46; form
   line 46). Standard deduction 15,750 single and married filing separate, 31,500 married filing joint, 23,625
   head of household (PDF page 26 table; the same in the PDF page 5 changes list and the PDF page 6 filing
   requirement table). Exemptions: age 65 or over 2,100 per person (Line 38, PDF page 25; form line 38), blind
   1,500 (Line 39), other 2,300 (Line 40), qualifying parent or grandparent 10,000 (Line 41, PDF page 26). No
   personal or dependent exemption in dollars (dependents get the Line 49 credit).

## Projection

- Brackets 2.5% from 0 (single, married_joint; the other statuses fall back to these).
- Base: federal AGI less the standard deduction (per return; `qualifying_surviving_spouse` set to the head of
  household amount, 23,625, because the booklet files a federal qualifying widow(er) as head of household) and
  the age 65 exemption (2,100 per person, `min_age` 65).
- Social Security exempt; railroad retirement `exempt_in_full` from the line 30 entry.
- Reliefs: line 29a government pension subtraction (`public_pension` only, 2,500 per person,
  `needs_input: pension_source`); line 29b military retired pay `exempt_in_full` (`needs_input:
  pension_source`). Another state's pension is taxed, which is exact, not an approximation.
- Capital gains: 25% deduction share of long-term gains, with an approximation (understates tax for gains on
  pre-2012 or undated assets).
- `not_modelled`: blind exemption (never), other exemption 2,300 (person 65 or over in the household), parent or
  grandparent exemption (has_dependents), U.S. obligation interest (never), active-duty pay (never).
- Approximations: itemizing and the 34% charitable increase (overstates), the post-2011 gain test
  (understates), Treasury interest taxed (overstates), all municipal interest treated as other-state
  (overstates), Dependent Tax Credit and family income credit left out (overstates).
- Indexing: brackets, deductions and relief caps `indexed: false, assumed: true`.

## Validator

```
data/states/2025/AZ.record.json: ok
data/states/2025/AZ.projection.json: ok
```

## Unsure

- The web page says "In regards to capital gains, Arizona has no special arrangement", against the booklet's
  25% subtraction (Line 24). The booklet is the more direct and current statement and is followed.
- The web page says the government pension subtraction covers "U.S. government service, including the U.S.
  military"; the booklet sends military retired pay to line 29b (100%), not line 29a. Recorded the booklet's way.
- `warn_when` for the 2,300 other exemption is `person_in_age_range` 65-120: it can apply to a filer paying a
  spouse's or parent's care costs, which a projection doesn't know; the parent or grandparent exemption uses
  `has_dependents` as the nearest marker though the person need not be a dependent.
- Applying the 25% gain subtraction to all long-term gains assumes most future sales are of assets bought after
  2011; a household with old holdings or undated fund distributions pays slightly more than projected.

## 2026-11-08: marker ids and indexing covers

- Marker ids given: first from_record id (warning code unchanged): `blind_exemption`, `other_exemption`, `qualifying_parent_grandparent_exemption`, `az_us_obligations_interest_subtraction`, `az_armed_forces_pay_subtraction`.
- Indexing covers: `brackets` -> `brackets`; `deductions` -> `deductions`; `relief_caps` -> `reliefs.cap`.
- Every `assumed` answer was checked again against the archived sources (searched for indexed, inflation, cost-of-living, adjusted annually, each year, CPI, fixed): none says, so all stay `assumed: true`. The booklet's only inflation sentences (PDF page 5) are about the private school tuition organization credits, which are not in the projection.
- Warning codes unchanged (every id is the marker's first from_record id).

## 2026-11-08: indexing settled from statutes

- `brackets` (projection `brackets`): not_indexed, A.R.S. 43-1011(A)(6), (D): one 2.5% band from 0, nothing to grow (43-1011(D) Phoenix CPI indexing is for a graduated schedule). Record `brackets` -> no.
- `deductions` (projection `deductions`): split, replaced by `standard_deduction` (covers `deductions:standard_deduction`, indexed, A.R.S. 43-1041(H), federal IRC 63 method) and `age_65_exemption` (covers `deductions:age_65_exemption`, not_indexed, A.R.S. 43-1023(E), fixed 2,100). Record `standard_deduction` (was not_stated with the booklet cite) -> yes with the statute cite; `age_65_exemption` added as no.
- `relief_caps` (projection `reliefs.cap`): not_indexed, A.R.S. 43-1022(2), fixed 2,500. Record `az_gov_pension_exclusion` added as no.
