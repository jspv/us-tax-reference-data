# Settlement: Ohio, tax year 2025

- Readings: `work/extract/2025/OH.r6.A.json`, `work/extract/2025/OH.r6.B.json` (round r6)
- Sources: `sources/archive/2025/OH/`: booklet `it1040-booklet`, return bundle `1040-bundle-original-fi`, and two Department pages that arrived after the readers finished: `oh-senior-citizens-income-tax` and `oh-faq-retirement-income` (both saved by the maintainer from a browser). Both readers wrote that the pages could not be fetched; those notes are dropped.
- Outputs: `data/states/2025/OH.record.json`, `data/states/2025/OH.projection.json`
- Settled: 2026-11-07

## The five questions

**1. A pension from another state's government, and a New York State pension.** Taxed in full; the retirement income credit is the only relief. In `covers` of `retirement_income_credit` as `public_pension_other_state`, no `paying_states`. No source names New York or another state's government pension, so this rests on the Department's general rule:

> A state can only tax the retirement income of a resident taxpayer. Thus, if an Ohio resident earns or receives retirement income, it is subject to tax in Ohio even if the taxpayer previously lived or worked in another state. This includes any amount included in the taxpayer's federal adjusted gross income. (FAQ 5)

> Generally, retirement income included in federal adjusted gross income is subject to Ohio income tax. Ohio then provides a credit based on the taxpayer's retirement income. (FAQ 1)

FAQ 3 lists the only deductible kinds: Social Security and tier I railroad, certain other railroad, and retired military pay. The credit's words reach any payer: "You received income from a pension, profit-sharing, or retirement plan (such as traditional IRAs or 401(k) plans)" (booklet PDF p.28); "retirement benefits, annuities, or distributions that are: Paid from a pension, retirement, or profit-sharing plan" (FAQ 2).

**2. Ohio's own and federal government pensions.** The same. No deduction is printed.

> Other retirement income included in your Ohio adjusted gross income is usually taxed by Ohio, but you may qualify for credits like Ohio's retirement income credit or the lump sum retirement credit. (Senior Citizens page, "Retirement Income")

One exception: "If you served in the military and receive a federal civil service retirement pension, you are eligible for a limited deduction based on the amount of your federal retirement pay that is attributable to your years of military service." (PDF p.24, line 34). Own entry `federal_civil_service_military_share`; `not_modelled` in the projection, since service years are not a yearly fact.

**3. Private pensions, IRA and employer-plan distributions, Roth conversions.** Pensions and distributions: taxed, FAQ 1 above, retirement income credit only. Roth conversions are taxed:

> if your rollover results in recognizing income that is included in your federal adjusted gross income (e.g. converting to a Roth IRA), it will be taxable to Ohio. (FAQ 8)

Whether a conversion counts toward the credit is not settled: it needs income "received on account of retirement", and "Early withdraws and distributions do not qualify for this credit" (FAQ 7). So `covers_unclear`, and an approximation.

**4. Social Security.** Exempt. "Ohio does not tax Social Security benefits." (Senior Citizens page). "Deduct the amount on your federal 1040 or 1040-SR, line 6b." (PDF p.20, line 16; line 16 is also on bundle PDF p.3).

**5. Brackets, standard deduction, exemptions.** One table for every status (PDF p.18), below. No standard deduction is printed. Exemption by MAGI (PDF p.17): 2,400 at 40,000 or less, 2,150 to 80,000, 1,900 to 749,999, 0 at 750,000 or greater; the example on that page, three exemptions at 75,000 = 6,450, agrees. No age or blindness amount is printed.

## Bracket schedule

Printed (PDF p.18, columns "More than" and "Up to"):

| Taxable nonbusiness income | Tax |
|---|---|
| 0 to 26,050 | 0.000% |
| 26,050 to 100,000 | $342.00 plus 2.750% of the amount in excess of $26,050 |
| 100,000 and over | $2,394.32 plus 3.125% of the amount in excess of $100,000 |

The column heads settle both boundaries: tax is 0 at exactly 26,050, and 2,375.63 at exactly 100,000. A plain rate list is 342.00 too low from 26,050 and 360.695 too low from 100,000.

The format holds a rate and a start per band, and `formula` holds only "rate x income minus constant". So each lump sum goes in a one-cent band whose rate carries it:

| Start | Rate | Tax at the top of the band |
|---|---|---|
| 0 | 0 | 0 |
| 26,050 | 34200.0275 | 342.000275 at 26,050.01 (342.00 + 0.01 x 2.75%) |
| 26,050.01 | 0.0275 | 2,375.625 at 100,000 |
| 100,000 | 1869.53125 | 2,394.3203125 at 100,000.01 (2,394.32 + 0.01 x 3.125%) |
| 100,000.01 | 0.03125 | |

Proof: `check.py` in the private folder compared this list with the printed formulas in exact decimal arithmetic at 4,389 incomes, including every cent from 26,049.00 to 26,051.99 and from 99,999.00 to 100,001.99; the worst gap was 0. The validator re-computes the four `table_rows`: 26,050 gives 0; 26,051 gives 342.03 against the printed 342.00; 68,050 gives 1,497, the printed example; 100,001 gives 2,394.35 against the printed 2,394.32.

`brackets.derivation.method` is `formula`, with no `formula` object: the constants this table implies (374.375, 730.68) are not printed, so provenance would refuse them. The printed formulas are in the record's notes. The validator skips provenance on derived bracket figures, so 34200.0275, 1869.53125, 26050.01 and 100000.01 pass because they are derived, and the proof above is what stands behind them. The projection's approximations list says these two rates are not marginal rates to show anyone.

## Structured differences

`uv run python -m tools.compare` reported **114 structured differences** (173 wording). Taken together they are 14 disagreements. **94 were decided by reading the sources; 20 were not** (rows 9, 12, 13 and 4: 18 where no source tests a person and the choice changes nothing, 2 where the values are the same number).

| # | Lines | Field | A | B | Source | Settled |
|---|---|---|---|---|---|---|
| 1 | 2 | Dependent exemption top step | at_or_over 750000 | over 749999 | PDF p.17 "$750,000 or greater $0" | A, the printed figure unshifted |
| 2 | 11 | Business income | `base.deductions` kind other | capped relief | PDF p.11: first 250,000 of one kind of income | B: a cap on covered income, not a flat amount. Cap all 250000 and married_separate 125000 as printed |
| 3 | 31 | Personal exemption `per` | exemption_claimed | person | PDF p.17 "Multiply your exemptions by the appropriate amount" | A; the key changed with `per`, which made 31 lines. Over-750,000 step as row 1 |
| 4 | 2 | First bracket rate | 0 | 0.0 | Same number | 0 |
| 5 | 8 | Exemption credit | entry | notes only | PDF p.29 line 9 | Kept (one-sided, below) |
| 6 | 21 | Retirement income credit `who.basis`; `credit_amount` | return, no amount | each_person, 200 | PDF p.28 "your and your spouse's (if filing jointly) total eligible retirement income", "maximum credit per return is $200"; Table 2 PDF p.44, FAQ 2 | A: return, and no fixed amount in the record since the table steps. The key changed with basis, which made 21 lines |
| 7 | 1 | Lump sum retirement credit `covers_unclear` | ira_distribution, roth_conversion | none | PDF pp.28, 43: "qualified pension, retirement, or profit-sharing plan", silent on IRAs | Kept |
| 8 | 8 | Lump sum distribution credit | entry | notes only | PDF pp.28, 44 | Kept |
| 9 | 6 | Uniformed services `who.basis` | return | each_person | No person test, no cap | each_person: brief rule 5 and the other settled states; changes nothing |
| 10 | 6 | Disability and survivor benefits | entries | notes only | PDF p.25 lines 42, 43 | Kept |
| 11 | 3 | Federal civil service military share | own entry | condition on the military entry | PDF p.24 gives it its own limit | A, brief rule 3 |
| 12 | 6 | Railroad `who.basis` | return | each_person | As row 9 | each_person |
| 13 | 6 | Social Security `who.basis` | return | each_person | As row 9 | each_person |
| 14 | 3 | Military pay outside Ohio | entry | absent | PDF p.23 line 32 | Kept |

Lines sum to 114.

## One-sided entries and additions

- Kept from A: `disability_benefits_deduction`, `survivor_benefits_deduction`, `military_pay_outside_ohio`, `lump_sum_distribution_credit`, `exemption_credit`, the `covers_unclear` on the lump sum retirement credit. All printed, all in scope.
- Added, neither reader had an entry: `joint_filing_credit` (PDF p.29). Both held it in notes. It is the largest credit a retired couple can get here, up to 650, and FAQ 6 says undeducted retirement income is qualifying income. `credit_rate` 0.20, `credit_basis` tax, stepped by MAGI less exemptions, in the form Connecticut's Table E uses. The 750,000 limit is written as an at_or_over step on MAGI less exemptions; this is exactly the MAGI test, because exemptions are 0 at that level.
- Added to `not_covered` on the retirement income credit from the Department pages: early withdrawals (FAQ 7), stock options and non-qualified deferred compensation (FAQ 5).
- Stayed in notes: earned income credit, child care credit, resident credit, medical deduction (line 44), Treasury interest (line 26), school district tax.

## Second-document checks

| Fact | First | Second |
|---|---|---|
| Social Security | Booklet p.20 line 16 | Senior Citizens page, bundle p.3 |
| Retirement income credit: cap, table, test, income | Booklet pp.28, 43, 44 | FAQ 2 prints the same table and 100,000 test; bundle p.7 line 2 |
| Senior citizen credit | Booklet p.28 | FAQ 2, bundle p.7 line 4; the wording differs on age, below |
| Lump sum credits | Booklet pp.28, 43, 44 | FAQ 2 |
| Military | Booklet p.24 | FAQ 3, Senior Citizens page |
| Railroad | Booklet p.20 line 17 | FAQ 3, 4 |
| Bracket rates | Booklet p.18 | Letter p.4 and p.5 give 3.125%; the lump sums have no second source |
| Exemptions | Booklet p.17 | The example on the same page; no other document |
| MAGI | Booklet p.8 | Worksheet p.40 |

## Projection choices

- **Credit income tests use `state_taxable_income`.** The record's measure is MAGI less exemptions, which is IT 1040 line 3 plus the business income deduction less line 4. Line 5 is line 3 less line 4, so without business income it is the same figure, not an approximation. No other projection uses this measure yet.
- **Exemption phase-out uses `state_agi`**: MAGI is Ohio AGI when there is no business income deduction (PDF p.8).
- **Retirement income credit is flat 200 in the projection.** Table 2 steps on the covered income itself, and neither layer can hold both that and the 100,000 test: `income_test` is one slot and the projection's measures don't include covered income. I kept the 100,000 test, since most retirees are over 8,000 of retirement income, where the table is flat at 200. The table is in `cap_rule`, and an approximation gives the direction: at most 200 understated. This is a format gap.
- **Senior citizen credit uses `older_spouse`** in the projection, meaning at least one spouse is 65. The record keeps `return`. PDF p.44's "If filing jointly and only one taxpayer qualifies for this credit" shows one-spouse cases exist for its neighbour, but no source says so for this credit.
- **Business income and the 3% tax** are `not_modelled`, warn always, with an approximation. The dispatch asked for them to be marked as outside a retirement projection's core.
- **Survivor benefits** are `not_modelled`, has_pension. Worth a second look: a survivor's pension is deducted in full, which can be far larger than any credit, but a projection can't tell it from other pension income.
- **Exemption credit** is `not_modelled`, never, as a low-income credit under the guide.
- `derived_figures` is empty: the validator's sum, difference and half can't express the band rates, and they are in the record.

## Unsure

1. **The 2,394.32 base.** It is 18.70 above what the second band gives at 100,000, so the printed table steps up there. It may be a printing error or intended; no second source is archived (the Department's `tax.ohio.gov/taxcalculator` is not). Recorded as printed. It changes every return over 100,000 by 18.70.
2. **Rates above 1 in a bracket list.** No other state has them. A consumer that uses ordinary bracket arithmetic handles them, but anything showing a top or marginal rate from the list would show 34200.0275. A base-amount field per band would be cleaner: a format gap. If a band start is ever indexed and rounded, a one-cent band would break; Ohio's indexing is `assumed: false`.
3. **New York pension rule** rests on general sentences, not a sentence naming another state's government pension. The direction is not in doubt; I found nothing that treats it differently.
4. **Senior citizen credit age**: "at the end of the tax year" (booklet) against "during the tax year" (FAQ 2). The booklet's wording is in the record; a person turning 65 in the year passes both. The joint test is above.
5. **`covers` of `business_income_deduction`** follows B's reading of the p.11 examples. Only `self_employment` matters to a projection, and it is `not_modelled`.

## Change after settlement: printed base on a band

The one-cent bands (rates 34200.0275 and 1869.53125) gave exact tax but are not rates anyone pays, and anything reading marginal rates, such as a Roth conversion optimiser filling a bracket, would misread them. The bracket format gained an optional `base`, the printed tax at the band's start, which replaces the sum of the lower bands. Ohio's list is now three bands with bases 342 and 2,394.32. Sections above that describe the one-cent bands are superseded.

## 2026-11-08: marker ids and indexing covers

- Marker ids: all 10 markers have an `id`. Descriptive ids (no from_record id of their own): `oh_unreimbursed_medical_deduction`, `oh_other_credits`; the rest take their first from_record id, so their warning codes are unchanged. `tools.checks --fix-warnings` rewrote the cases' accepted_warnings (the old shared code state_rule_not_modelled:unnamed becomes the new ids); nothing else in the cases changed.
- Indexing covers: `brackets`, `deductions` (personal exemption amount and MAGI bands); `relief_caps` covers reliefs.cap. Added `relief_income_tests` (reliefs.income_test) and `relief_credit_amounts` (reliefs.credit_amount), both indexed false, assumed, for the retirement income and senior citizen credits' income limits and credit amounts, which no entry covered.
- Assumed entries: searched the archived sources (docling, pypdf and page text) for indexed, inflation, cost of living, adjusted annually and consumer price index, and for statements that figures are fixed; nothing says, so every `assumed: true` stays.

## 2026-11-08: indexing settled from statutes

Statute research (work/indexing/findings*.json) settled every projection indexing entry that was `assumed: true`:

- `brackets` (brackets): indexed, indexed from 2027, Ohio R.C. 5747.02(A)(5)
- `deductions` (deductions): indexed, indexed from 2027, Ohio R.C. 5747.025(B)-(C)
- `relief_caps` (reliefs.cap): not indexed, Ohio R.C. 5747.055(B), (F)
- `relief_income_tests` (reliefs.income_test): not indexed, Ohio R.C. 5747.055(B) and (F)
- `relief_credit_amounts` (reliefs.credit_amount): not indexed, Ohio R.C. 5747.055(B), (F)
- Record `indexing`: added brackets -> yes; added personal_exemption -> yes; added retirement_income_credit -> no; added senior_citizen_credit -> no.
- Both `brackets` and `deductions` are indexed from 2027: HB 96 Section 757.120(A) suspends the adjustments for 2025 and 2026. The 40,000 / 80,000 / 750,000 exemption tiers are fixed by statute, but they sit in the same deduction's phase_out as the indexed step amounts, so the `deductions` entry grows them too; the note says so.
- Flagged figure: the statute prints the top exemption tier as 2,350; the 2025 IT 1040 booklet (it1040-booklet PDF p.17) prints 2,400 / 2,150 / 1,900 for MAGI of 40,000 or less / 40,001-80,000 / 80,001-749,999. The data (2,400 / 2,150 / 1,900) matches the booklet; no change.
- Later the same day: the format gained '.phase_out_thresholds' / '.phase_out_amounts' selectors, so the fixed income tiers (40,000 / 80,000 / 750,000) have their own not-indexed entry, `personal_exemption_income_tiers`; only the exemption amounts grow.
