# CA 2025 settlement

Readings A and B (round r5), settled 2026-11-07. `tools.compare`: 71 structured differences, 96
wording differences. Sources: the 2025 Form 540 Personal Income Tax Booklet (80-page PDF, Form 540
and the Schedule CA (540) instructions inside) and the 2025 Schedule CA (540) form. The booklet's
printed page numbers equal the PDF page numbers, so every cite is a PDF page. The record was built
from both readings, with the changes below. Helper scripts are in the dispatch's private folder.

## Structured differences (71)

| # | Field (compare key) | A | B | Settled | Source |
|---|---|---|---|---|---|
| 1-21 | `phase_out` on the age-65, blind and dependent exemptions (effect, measure.base, 5 thresholds, x3) | AGI limitation on all four exemptions: federal AGI over 252,203 / 504,411 / 378,310, effect other | limitation only on the personal exemption | **A**, now in each credit relief's `income_test` | PDF p14, Line 32 and the AGI Limitation Worksheet: lines f to i reduce lines 7, 8 and 9 (personal, blind, senior) and lines j to m reduce line 10 (dependents). |
| 22-28 | Second standard deduction `standard_deduction_dependent` (what, per, 5 amounts) | none | an entry with the same 5,706 / 11,412 amounts as maximums | **Folded into the condition of `standard_deduction`**, no second entry | PDF p13, California Standard Deduction Worksheet for Dependents: the smaller of (the larger of earned income or 1,350) and 5,706 / 11,412. A second per-return standard deduction would let a consumer subtract two. |
| 29-31 | `indexing` entries for brackets, standard_deduction, personal_exemption_credit | none (all_other only) | each not_stated | **Dropped; all_other not_stated kept** | The booklet says nothing about indexing any figure (searched inflation, indexed, adjusted annually, cost of living). Brief rule 8 wants an entry only for a figure the booklet speaks about. |
| 32-37 | `us_obligations_interest` who.basis (3 + 3 fields, matched by basis) | each_person | return | **return**, form exempt_in_full | PDF p59 Line 2: no age test, per-person cap or each-spouse rule. The schema says "return when neither". |
| 38-49 | Social Security and railroad entries (3 fields each for 4 entries, matched by covers and basis) | `social_security_exclusion` (social_security, each_person); one railroad entry for Tier 1 and RRB-1099-R (each_person) | `social_security_exclusion` covering social_security and railroad_retirement (Tier 1); a separate Tier 2 entry (return) | **One Social Security entry and one railroad entry for both tiers, basis return, form exempt_in_full** | PDF p60 Line 6: "California excludes U.S. social security benefits or equivalent Tier 1 railroad retirement benefits from taxable income". Line 5: RRB-1099-R benefits included in column A are entered in column B. Both tiers are excluded in full with no cap or age test, so one railroad entry holds both. |
| 50-71 | `military_retirement_exclusion` (A 12 fields, B 10, unmatched because covers and basis differ) | covers military_pension; basis return; thresholds for all 5 statuses (125,000 for single, separate, head of household) | covers military_pension and annuity; basis each_person; thresholds for single, joint and QSS only | **covers military_pension and annuity (B), with the annuity limited to the Survivor Benefit Plan in other_conditions; basis return (A); all 5 thresholds (A); cap 20,000 per return, effect removes (both)** | PDF p60 Line 5: "retirement pay from the federal government for service in the uniformed services or annuity payments pursuant to a United States Department of Defense Survivor Benefit Plan ... not to exceed $20,000 for each type of payments ... The qualified taxpayer's federal AGI must not exceed $125,000 (or $250,000 for a surviving spouse or spouses filing a joint return). The exclusion is capped at $20,000 for a surviving spouse, spouses filing a joint return, and any other individual who did not exceed the federal AGI limits." PDF p6 and p55 What's New agree (2025 to 2029). |

65 of the 71 were settled by reading the booklet (rows 1-31 and 38-71; the who.basis part of rows
38-49 used the schema's "return when neither" once the booklet showed no person-level rule). The
other 6 (rows 32-37) were settled by the schema rule alone, because the booklet is silent.

Wording difference with a factual error: A said the Tax Table is on pages 63 to 73, B said 69 to 74.
PDF p13 Line 31 says "the tax table beginning on page 69"; it runs PDF p69 to 73 (p74 is blank).

## Change made by the dispatch: exemption credits are reliefs

Both readers put the personal, blind, senior and dependent exemptions in `base.deductions` and
noted that they are credits. PDF p14: "Exemption credits reduce your tax". Form 540 line 11 goes to
line 32, which is subtracted from the line 31 tax, and line 33 does not go below zero. As the
dispatch asked, they are now credit reliefs: `form: credit`, `credit_amount` 153 (personal, blind,
senior) or 475 (dependent), `covers: ["all_income"]`, `credit_basis: tax`, and an `income_test` for
the AGI limitation. `base.deductions` holds only the standard deduction.

- **`credit_basis: tax`.** The schema defines credit_basis as what a `credit_rate` is a share of.
  These credits are fixed amounts with no credit_rate, so `tax` is used to say they come off the tax
  and not off income. A note in the record says so.
- **The income test is stepped, but recorded as `effect: other`.** Each credit loses 6 for each
  2,500 (1,250 filing separately) of federal AGI over the amount, or part of it. That is a stepped
  phase-down: a 153 credit is gone 62,500 over the threshold, a 475 credit 197,500 over. The step
  amounts (147, 141, ...) and the 0.0024-a-dollar rate are not printed, and the validator rejects
  unprinted figures in a record. The record therefore gives the threshold, `effect: other` and the
  full worksheet in `as_printed`. The projection maps it to `removes`, with an approximation, which
  overstates tax.
- **who.** Personal, blind and senior use `each_person`, with min_age 65 for senior. Dependent uses
  `return`, with "one credit for each dependent" in other_conditions and cap_rule. Form 540 line 7
  gives a qualifying surviving spouse (status 5) 2 personal credits. That is in other_conditions,
  and the projection carries an approximation for it.

## One-sided entries

- B's `standard_deduction_dependent`: its content was kept (rows 22-28) as the condition of the
  main entry.
- B's extra indexing entries were dropped (rows 29-31).
- Condition text that only one reader gave (blind definition, dependent rule, personal box counts,
  MFS both-itemize rule) was kept where the booklet prints it (PDF p12, p13, p39).
- A's `measure.as_printed` for the credit phase-out (RDP pro forma AGI) was kept, from PDF p14.

## Facts checked against a second line or document

- **(1) Other states' government pensions, and a New York State pension: not found in the booklet.**
  The booklet has no subtraction, no reciprocity rule, and no mention of another state's or New
  York's pension. Such a pension falls under the general rule on PDF p60, Line 5a and 5b: "Generally,
  no adjustments are made on this line. However, if you received Tier 2 railroad retirement benefits
  or partially taxable distributions from a pension plan, you may need to make the following
  adjustments." It is therefore taxed as it is included in federal AGI. No
  `public_pension_other_state` entry. I searched: pension, annuity, New York, other state,
  government pension, retirement income. The Schedule CA (540) form's line 5 is only a label.
- **(2) California's own and federal government pensions:** no subtraction. The same line 5
  sentence applies, and the only pension adjustments printed are Tier 2 railroad, the three-year-rule
  annuity (1986-87), and the Military Retirement Exclusion. That exclusion covers federal
  uniformed-services retirement pay only (above). No exclusion is printed for a federal civilian or
  CalPERS-type pension.
- **(3) Private pensions, IRA and employer-plan distributions, Roth conversions:** no relief. PDF
  p59, Line 4a and 4b: "Generally, no adjustments are made on this line. However, there may be
  significant differences in the taxable amount of a distribution (including a distribution from
  conversion of a traditional IRA to a Roth IRA), depending on when you made your contributions to
  the IRA." These are differences in California basis, not exclusions. PDF p60 line 5 says the same
  for pensions. No age deduction or retirement-income relief exists anywhere in the booklet.
- **(4) Social Security: exempt.** PDF p60 line 6 (quoted above). Also PDF p67, claim of right:
  "Social security benefits are not taxable by California". Also PDF p13 Line 14: "differences
  between your federal and California income, e.g., social security benefits".
- **(5) Brackets.** PDF p75 prints Schedules X (single or married/RDP filing separately), Y (joint or
  qualifying surviving spouse) and Z (head of household), each with nine rates from 1% to 12.3%. Both
  readers agree on all 36 starts. The printed tax at each band start agrees with the rates (helper
  `check_brackets.py`): X 110.79 ... 72,219.84 (one-cent rounding in the booklet), Y 144,439.65, Z
  97,472.91. Tax Table rows (PDF p69 to 73) agree with the schedules at the row midpoint to the
  dollar: 30,051-30,150 is 568 / 380 / 380; 60,051-60,150 is 2,192 / 1,132 / 1,132; 99,951-100,000
  is 5,736 / 3,068 / 3,708. `brackets.derivation` is not used because the schedules are printed and
  start at 0.
- **Standard deduction and exemptions.** PDF p13 chart: 5,706 / 11,412 / 5,706 / 11,412 / 11,412.
  The same figures are on Form 540 line 18 (PDF p40) and Schedule CA Part II line 30 (PDF p52). The
  exemption credits on Form 540 PDF p39 ("X $153" lines 7 to 9, "X $475" line 10) agree with PDF p12
  lines 7 to 10 and the PDF p14 worksheet.
- **Surtax.** PDF p16 Line 62 worksheet: taxable income less 1,000,000, times .01. One threshold
  for every status. PDF p5 What's New covers the rename from the Mental Health Services Tax.
- **Muni interest.** PDF p59 line 2 lists non-California state and municipal bonds as a column C
  addition, with no California entry, plus the 50% fund rule. Line 3: "California taxes dividends
  derived from other states and their municipal obligations". Both readers say
  other_states_taxed_own_exempt.
- **Capital gains.** PDF p60 line 7a: "California taxes long and short term capital gains as regular
  income. No special rate for long term capital gains exists."

## Projection choices

- **Brackets with the Behavioral Health Services Tax folded in.** The tax is 1% of taxable income
  over 1,000,000 for every status:
  - Single and married filing separately: 13.3% from 1,000,000.
  - Joint: 12.3% from 1,000,000 (11.3% + 1%), then 13.3% from 1,485,906.
  - Head of household: 12.3% from 1,000,000, then 13.3% from 1,010,417.
  - Both rates are in `derived_figures`, as sums.
- **Modelled:**
  - the standard deduction;
  - Social Security exempt;
  - railroad retirement exempt in full;
  - the Military Retirement Exclusion: military_pension only, `needs_input: pension_source`, 20,000
    per return, removed above federal AGI of 125,000 / 250,000;
  - the personal and senior exemption credits (153 per person, senior at min_age 65), removed above
    the AGI threshold;
  - muni interest as other-states-taxed, own-exempt.
- **Not modelled, with warnings:**
  - the Survivor Benefit Plan annuity part of the military exclusion (has_military_pension);
  - the blind credit (never);
  - the dependent credit (has_dependents);
  - U.S. obligations interest (never).
- **Approximations:**
  - the credit phase-down mapped to removes (overstates tax);
  - the qualifying surviving spouse's second personal credit (overstates tax);
  - the military exclusion's end after tax year 2029 (understates tax from 2030);
  - the surtax folded ahead of credits (understates tax; nil for the exemption credits);
  - itemizing (either);
  - California IRA basis differences, including on Roth conversions (either);
  - Treasury interest (overstates tax);
  - California bond interest (overstates tax);
  - the Tax Table rounding (either, under 5 dollars);
  - the January 1 birthday rule for the senior credit (overstates tax).
- **Indexing:** brackets, the surtax, deductions, exemption credits and relief caps are all
  `indexed: false, assumed: true`, because the booklet does not say.

## Unsure

- `credit_basis: tax` on fixed-amount credits stretches the schema's definition, which is about
  credit_rate. A consumer should use credit_amount and ignore credit_basis when there is no
  credit_rate.
- The phase-down is recorded as `effect: other` because the stepped amounts aren't printed. A
  reviewer may want `stepped` with computed steps, if the validator is changed to accept derived
  step figures in a record.
- I read "Surviving spouse" in the military exclusion's 250,000 limit as the qualifying surviving
  spouse status. I read "must not exceed" as no exclusion above the limit. Both are judgement calls.
  So is the 125,000 limit for married filing separately and head of household, which is read from
  "(or $250,000 for ...)".
- The overall military cap: I read "not to exceed $20,000 for each type of payments" together with
  "capped at $20,000 for ... spouses filing a joint return" as one 20,000 cap per return. The first
  sentence alone could allow 20,000 for retirement pay plus 20,000 for an SBP annuity.
- That a New York (or any other state's) public pension is taxed is read from the general "Generally,
  no adjustments are made" sentence. The booklet never names such pensions.

## 2026-11-08: marker ids and indexing covers

- Marker ids given: first from_record id (warning code unchanged): `military_retirement_exclusion`, `blind_exemption_credit`, `dependent_exemption_credit`, `us_obligations_interest`.
- Indexing covers: `brackets` -> `brackets`; `behavioral_health_services_tax` -> `surtaxes`; `deductions` -> `deductions`; `exemption_credits` -> `reliefs:personal_exemption_credit`, `reliefs:senior_exemption_credit`; `relief_caps` -> `reliefs.cap`; `relief_income_tests` -> `reliefs.income_test`.
- `behavioral_health_services_tax` covers `surtaxes`, which the projection leaves empty: the 1% surtax over 1,000,000 is folded into the brackets as a band, so its threshold is grown (or not) with `brackets`.
- Added `relief_income_tests` (indexed false, assumed) for the military retirement exclusion's AGI test; `exemption_credits` names the two exemption credits by id, so their AGI thresholds stay with it.
- Every `assumed` answer was checked again against the archived sources (searched for indexed, inflation, cost-of-living, adjusted annually, each year, CPI, fixed): none says, so all stay `assumed: true`.
- Warning codes unchanged (every id is the marker's first from_record id).
