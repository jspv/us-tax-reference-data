# Missouri 2025 settlement log

Readings: `work/extract/2025/MO.r6.A.json`, `MO.r6.B.json`. Settled 2026-11-07.
Sources: `sources/archive/2025/MO/`. Page numbers are PDF pages; the 4711 Reference Guide's printed page
is 3 lower than its PDF page (printed 6 is PDF 9).

`tools.compare` reported 40 structured differences and 114 wording differences. No two readers printed
different figures for the same thing: all 40 are one reader having an entry or field the other lacks, or the
same amounts shaped differently. All 40 were read against the booklet. 37 were decided by what it prints; the
other 3 (the capital gain relief) were dropped as a double count of an entry both readers had.

## The five required questions

### 1. A government pension paid by another state, and New York State in particular

In `covers` as `public_pension_other_state`, in the same entry as Missouri's own public pensions. **This is a
reading, not a printed rule.**

> "Public pensions are pensions received from any federal, state, or local government." (instructions p17;
> Reference Guide p9; Form MO-A p3 Section A has the same words)

The word "state" is not limited to Missouri and "any" points the other way, but no sentence names another
state's pension. No reciprocity rule or paying-state list was found, so there is no `paying_states`, and New
York is treated like any other state. Both readers read it this way. The projection carries an
`understates_tax` approximation for the reading.

**Rule:** a Missouri resident with a New York State pension subtracts the lesser of the taxable pension or
47,633, minus that person's own exempted Social Security, not below 0. No age test, no income test.

### 2. Its own and federal government pensions

Same entry, same rule. Federal, state and local are named together in the quote above. Cap: "In the 2025 tax
year this amount is $47,633 per taxpayer" (Reference Guide p9); Form MO-A p3 Line 2 "$47,633 (maximum social
security benefit)". Income test: none for 2025; the FAQ's 85,000 / 100,000 / 85,000 limits sit under "Tax
years 2023 and prior", and "Tax years beginning on or after January 1, 2024" has none. Age or contributory
test: none printed. Military: subtracted in full on MO-A Part 1 Line 10, "enter your total military
retirement benefits" (instructions p14). The Survivor Benefit Plan annuity "does qualify for the public
pension exemption" and not the military subtraction (FAQ).

**The reduction falls on the exemption, not the cap.** The dispatch and B's note speak of the cap being
reduced; both readers' `cap_rule` text and A's note have it right, and the lines say:

> Line 2: "Amount from Line 1 or $47,633 (maximum social security benefit), whichever is less"
> Line 4: "Subtract Line 3 from Line 2. If Line 3 is greater than Line 2, enter $0"
> FAQ: "If you also claim the social security or social security disability deduction, your public pension
> exemption will be reduced by that amount."

So the exemption is `max(0, min(pension, 47,633) - Social Security exemption)`. `cap_reduced_by` would give
`min(pension, 47,633 - Social Security exemption)`, which is a different number:

| Pension | Exempt SS | Form Line 4 | Pension + SS exempt | `cap_reduced_by` gives | Tax understated |
|---|---|---|---|---|---|
| 30,000 | 20,000 | 10,000 | 30,000 | 27,633 | 828.75 |
| 23,816 | 23,816 | 0 | 23,816 | 23,816 | 1,119.35 (the worst case) |
| 60,000 | 20,000 | 27,633 | 47,633 | 27,633 | 0 |

The two exemptions together equal `max(SS exemption, min(pension, 47,633))`, per person. The projection
therefore puts `public_pension_subtraction` (cap 47,633) and `social_security_retirement_subtraction` in one
`best_of_group`, `mo_social_security_or_public_pension`, with no `cap_reduced_by`. This follows the South
Carolina projection, which uses a group for the same kind of arithmetic. The record stays faithful: no group,
the rule is in `cap_rule`. It depends on the group being evaluated per person. See "Unsure".

### 3. Private pensions, IRA and employer-plan distributions, Roth conversions

One entry: "Annuities, pensions, IRAs, and 401(k) plans funded by a private source" (MO-A p3 Section B). Line
6 takes federal Lines 4b and 5b. 6,000 per taxpayer (Reference Guide p9; Line 7). Limits 25,000 / 32,000 /
16,000 on Missouri AGI less taxable Social Security, reduced "by one dollar for every dollar" (Reference Guide
p9; Lines 1-5, 9). The excess comes once off the spouses' total (Lines 8-9), which the per-person evaluation
cannot do: `overstates_tax` approximation, at most 282 a year.

Roth conversions: `covers_unclear`. A search of all five documents finds no "Roth"; every "conversion" hit is
involuntary conversion of property. Left out of the projection's `covers`, with an approximation.

### 4. Social Security

Exempt for age 62 or older and for disability benefits, 100 percent, no income test in 2025.

> "Missouri does not tax 100% of social security benefits for individuals age 62 or older, and 100% of social
> security disability benefits, as long as these benefits are included in federal adjusted gross income under
> IRC §86." (FAQ)
> "The 2025 deduction amount is 100 percent of the taxable amount." (Reference Guide p9)
> "To be eligible for social security deduction you must be 62 years of age by December 31" (MO-A p3 Section C)

Treatment changed from both readers' `exempt` to `relief`: see "Corrections".

### 5. Brackets, standard deduction, exemptions

One chart for every status (instructions p21, checked by recomputing both worked examples). Band arithmetic
at 3,090 gives 37.86 and at 12,000 gives 388.06; the chart gives 37.60 and 388.03, both rounding to the
printed 38 and 388. Standard deduction checked in two documents: Form MO-1040 p2 Line 14 and Reference Guide
p10. Age 65 and blind amounts: instructions p8, and the Reference Guide p10 table agrees (single 1 box 17,750;
married separate 1 box 17,350). No personal or dependent exemption is printed; the only exemption is 1,400 for
head of household and qualifying widow(er) (instructions p8 Line 15).

## Points the dispatch flagged

- **Tax per spouse.** "A separate tax must be computed for you and your spouse" (instructions p21); "Missouri
  law requires a combined return for married couples filing together" (p7). Not an election, unlike Arkansas.
  The format holds one schedule per status, so `married_joint` holds the printed chart, applied once to the
  couple's total: `overstates_tax`, at most about 176 a year (60,000 split evenly: 2,644.06 against 2,468.12).
  A doubled schedule was rejected: it adds figures the booklet doesn't print and understates by the same
  amount for one-income couples.
- **Federal income tax deduction.** The record has it, amount = the cap (5,000; 10,000 combined), the ladder in
  `condition`, and `phase_out` holding the last rung (`removes` over 125,000). `stepped` was rejected: its
  `keep_share` is a share of the relief, and these percentages are of the federal tax, so a consumer would
  compute 25% of 5,000 instead of 25% of the tax. The projection has it in `not_modelled`
  (`warn_when: always`), as Alabama's is, because federal tax is not a yearly fact. Direction `overstates_tax`,
  at most 470 a year on a combined return, 235 otherwise, nothing over 125,000 of Missouri AGI.
- **Citation pages.** Checked with pypdf against the PDFs themselves. Form MO-A has 3 pages: p1 Lines 1-13, p2
  Lines 14-19 and Part 2, p3 Part 3. The docling text fuses p2 into p1, so the pypdf marker governs.
  - B's "MO-A PDF page 1 Part 1 Line 18" is wrong: PDF page 2.
  - A's "PDF page 3, Line 14" on Form MO-1040 is wrong: PDF page 2 (A's notes' "form p23" is the copy inside
    the instructions PDF, which is right for that document).
  - A's "Reference Guide p6" is the printed number: PDF page 9.
  - All other MO-A cites (Part 1 Lines 1, 8, 10, 11 at p1; Part 3 at p3) are right.

## Structured differences

| Field | A | B | Lines | Settlement |
|---|---|---|---|---|
| Age 65 additional | 2 entries, split by amount | 1 entry, 5 statuses | 8 | Instructions p8 prints the amounts both have; one entry with a status map is the format. B's shape |
| Blind additional | 2 entries | 1 entry | 8 | Same |
| Line 15 exemption | `other` | `personal_exemption` | 8 | Instructions p8: "your additional exemption". `personal_exemption`, per return |
| Federal income tax deduction | entry | notes only | 7 | Printed on instructions p8 and form p2. Kept; `phase_out` added |
| Business income deduction | relief | none | 4 | Printed on instructions p16. Kept |
| Capital gain relief | relief as well as `capital_gains` | `capital_gains` only | 3 | One subtraction printed. Relief dropped as a double count |
| `brackets` indexing entry | none | `not_stated` | 1 | Kept; no inflation sentence anywhere |
| Private pension `applies_when` | absent | `over` | 1 | MO-A p3 Line 5: at the limit the excess is 0. `over` |

Total 40. The 114 wording differences were taken from the page: ids and labels use B's names where clearer,
`cap_rule` text was rewritten from the lines.

## One-sided entries

Kept: federal income tax deduction (A), business income deduction (A), `brackets` indexing (B),
`applies_when` (B). A's condition "only when the standard deduction is taken" is kept on the age and blind
entries. B's "for the entire taxable year" on disability is kept (instructions p17). B's explicit nulls for
ages are dropped as empty.

Dropped: A's capital gain relief. A's and B's `married_separate` and `head_of_household` brackets (see below).

## Corrections to what both readers agreed

- `social_security.treatment`: both `exempt`, now `relief`. The exemption needs age 62 or disability benefits,
  so someone younger on survivor benefits is taxed. The projection needs `relief` too: under `exempt` the
  group in question 2 would have nothing to compare.
- `brackets`: both listed four statuses, now `single` and `married_joint`. The schema asks for the other two
  only when a status has its own schedule, and the projection falls back to `single`. Same result.
- `us_obligations_interest`: neither made an entry, both noted it. Added from instructions p13 Line 8, as in
  the other settled states, with `dividends` for the mutual fund sentence. The projection marks it
  `not_modelled` and approximates.
- Indexing of `standard_deduction` and `standard_deduction_age_65`: neither had it. Added as `yes`, tied to the
  federal amount: see "Unsure".

## Projection

Relief `business_income_deduction` covers `self_employment` only: `other_income` in the projection is broader
than Schedule E Part 2, so it stays in the record and the difference is an approximation (`either`).
`needs_input: ["pension_source"]` on the public, private and military reliefs. Disability benefits are
`not_modelled` with a warning for anyone under 62. `relief_caps` (`indexed: false`, assumed) covers the 6,000
and the income limits; the public cap has its own entry, `indexed: true`.

Income test measure: `state_agi` is Form MO-1040 Line 6, after the MO-A Part 1 subtractions (capital gain,
military, railroad, exempt federal interest, business income) and before the Line 8 pension exemptions. A
consumer must compute it that way. Taking federal AGI instead would count gains against the 6,000.

## Unsure

1. `public_pension_other_state` rests on the word "any". Missouri's statute was not read. If Missouri treats
   such a pension as private, tax is understated by up to 1,956.75 a year per person.
2. The `best_of_group` is exact only if the consumer evaluates it per person. The AR and SC checks already need
   that, but the schema doesn't say it outright, and a consumer could read it as "compute each, keep the
   lowest tax" once for the whole return. Chosen once for the whole return, a couple with his Social Security and her pension would lose
   one, up to 2,238.75 a year too much. This needs confirming before a consumer evaluates Missouri.
3. Indexing `yes` on the standard deduction rests on "equals the allowable federal standard deduction"; the
   booklet says nothing about inflation. The figure ties to federal, and the projection marks it not assumed.
   Consumers may also need to read per-deduction indexing figures rather than `deductions`.
4. The FAQ links `dor.mo.gov/pdf/pension.pdf`, an eligibility chart that is not in the sources. It could
   hold a detail these documents do not, though the 2025 form lines leave no gap.
5. A government 457 or an IRA rolled from a public pension: "funded by a private source" and "from any
   federal, state, or local government" don't settle which side it falls on. Left to `pension_source`.

## Pension chart

The chart at dor.mo.gov/pdf/pension.pdf was fetched on 2026-11-07, read, and dropped from the sources: it is a 2015 document (PDF metadata; $36,976 maximum benefit), it prints income limits the FAQ puts under 2023 and prior, and it settles none of the open questions.

## 2026-11-07: format v1 adoption

Record: unchanged (no new figure was needed; its income test already says Missouri AGI, Line 6, as printed).
`record.sha256` in the projection is therefore unchanged.

Projection, private pension income test:

- **Measure.** Form MO-A Part 3 Section B Line 1 is "Missouri adjusted gross income from Form MO-1040, Line 6"
  (MO-A PDF p3); Line 6 is Line 3 (federal AGI plus the MO-A Part 1 Line 7 additions) less the Part 1 Line 19
  subtractions (MO-1040 PDF p2 Lines 1-6; MO-A PDF p1 Lines 1, 7, 8, 10, 11 and PDF p2 Lines 17-19). The old
  measure `state_agi` minus taxable Social Security was wrong for a consumer: the projection's `state_agi` is
  after every relief, so it also took off the public pension, Social Security and private pension exemptions and
  subtracted taxable Social Security twice. It is now `federal_agi`, plus tax-exempt interest, minus Missouri
  bond interest (the Line 1 addition of other states' bonds), minus taxable Social Security (Section B Line 2),
  with `minus_reliefs` = `capital_gain_subtraction`, `military_retirement_subtraction`,
  `railroad_retirement_exempt`, `business_income_deduction` (Part 1 Lines 18, 10, 11, 17). Exact within the
  modelled items. Dollar effect: on `mo_2025_private_test_line6_every_subtraction_over` the old measure, read
  literally, is state_agi 27,000 before the private exemption less taxable Social Security 15,300 = 11,700, under
  the limit, so it kept 6,000 instead of 4,000: taxable income 5,250 instead of 7,250, 98.42 instead of 171.83,
  73.41 too little tax (at most 4.7% x 6,000 = 282 a year per person).
- **Gains as a relief.** `minus_reliefs` can only name reliefs, and the gain subtraction was a `capital_gains`
  entry (`deduction_share` 1). It is now an `exempt_in_full` relief covering `capital_gains`, `who.basis`
  return, from record `capital_gain_subtraction`, and `capital_gains` is empty, as in the New Mexico and Vermont
  projections. No dollar change. Missouri enters a negative Line 7a as 0 (instructions PDF p16 Line 18): the
  relief must floor at 0, and `mo_2025_capital_loss_not_added_back` now pins it (relief amount 0.00).
- **`reduce_each_person: false`.** Section B Line 7 limits each spouse's pension to 6,000, Line 8 adds Lines 7Y
  and 7S, and Line 9 is "Total private pension, subtract Line 5 from Line 8" (MO-A PDF p3): the one excess comes
  off the couple's total once. The field (default false) says exactly that, so the approximation "Private
  pension income test: Missouri takes the return's one excess ... so twice" (at most 282 a year) is deleted.
  Example: joint, Line 6 40,000, both spouses 6,000: excess 8,000, Line 9 4,000; per-person reduction gave 0.
- **Sizes reworded, not new:** the Treasury interest and Missouri bond approximations now say the interest
  also counts in the private pension test (example: single at the limit with 2,000 of it, 4,000 more taxable
  income, at most 188).

No approximation said the measure was mapped elsewhere; the old mapping had none, which was the gap.

Checks: `mo_2025_private_joint_both_spouses_excess_twice` deleted and replaced by
`mo_2025_private_joint_both_spouses_excess_once` (wages 28,000, Line 9 4,000, tax 75.92). Reworked (new
`capital_gain_subtraction` in `tests` and `relief_amounts`, `verified` removed):
`mo_2025_private_test_ignores_gains`, `mo_2025_capital_loss_not_added_back`. Added:
`mo_2025_private_test_line6_every_subtraction_below` / `_at_limit` / `_over` (single, 63: military, railroad,
self-employment, gains, both kinds of bond interest and Social Security; test 24,000 / 25,000 / 27,000; private
exemption 6,000 / 6,000 / 4,000; tax 18.74 / 41.86 / 171.83).

Unsure: a consumer must floor an `exempt_in_full` relief at 0 when gains net to a loss; the schema says this for
`deduction_share` but not for reliefs.

## 2026-11-08: marker ids and indexing covers

- Marker ids given: first from_record id (warning code unchanged): `federal_income_tax_deduction`, `social_security_disability_subtraction`, `standard_deduction_blind`, `standard_deduction_dependent_filer`, `us_obligations_interest`; descriptive: `mo_other_subtractions` (no from_record id); `mo_lump_sum_tax_and_credits` (no from_record id).
- Indexing covers: `brackets` -> `brackets`; `standard_deduction` -> `deductions:standard_deduction`; `standard_deduction_age_65` -> `deductions:standard_deduction_age_65`; `head_of_household_additional_exemption` -> `deductions:head_of_household_additional_exemption`; `public_pension_subtraction` -> `reliefs:public_pension_subtraction`; `relief_caps` -> `reliefs.cap`; `relief_income_tests` -> `reliefs.income_test`.
- Existing per-figure entries now name their figure by id (`deductions:standard_deduction`, `deductions:standard_deduction_age_65`, `deductions:head_of_household_additional_exemption`, `reliefs:public_pension_subtraction`).
- Added `relief_income_tests` (indexed false, assumed) for the private pension subtraction's income test.
- Every `assumed` answer was checked again against the archived sources (searched for indexed, inflation, cost-of-living, adjusted annually, each year, CPI, fixed): none says, so all stay `assumed: true`.
- `tools.checks --fix-warnings` updated the cases' accepted_warnings where a code changed; nothing else in the cases changed.

## 2026-11-08: indexing settled from statutes

Statute research (work/indexing/findings*.json) settled every projection indexing entry that was `assumed: true`:

- `brackets` (brackets): indexed, RSMo 143.011.5 (definitions in 143.011.6)
- `head_of_household_additional_exemption` (deductions:head_of_household_additional_exemption): not indexed, RSMo 143.161.2
- `private_pension_subtraction_cap` (reliefs:private_pension_subtraction.cap): not indexed, RSMo 143.124.3
- `relief_income_tests` (reliefs.income_test): not indexed, RSMo 143.124.3
- Record `indexing`: updated brackets -> yes; added head_of_household_additional_exemption -> no; added private_pension_subtraction -> no.
- The public pension cap (indexed, RSMo 143.124.5) stays with the existing `public_pension_subtraction` entry and its record cite; only the private pension cap got its own entry.
