# Maine 2025 settlement log

Readings: `work/extract/2025/ME.r6.A.json`, `ME.r6.B.json`. Settled 2026-11-07.
Sources: `sources/archive/2025/ME/`. Page numbers are PDF pages, by the `*.pypdf.txt` markers.

`tools.compare` reported 23 structured differences and 76 wording differences. No two readers printed
different figures for the same thing. All 23 were read against the booklet: 20 were decided by what it
prints (14 + 6 below); the other 3 (the itemized limit) are printed but out of place as a deduction.

**Gap in the sources.** The Pension Income Deduction Worksheet (lines P1 to P10) and Schedule 1S itself
are not in the folder. The FAQ says the worksheet is on the MRS Forms page. Fetching it would settle the
first two open points below.

## The five required questions

### 1. A government pension paid by another state, and New York State in particular

In `covers` as `public_pension_other_state`, in the same entry as Maine's own public pensions. **This is a
reading, not a printed rule.** Both readers said `covers_unclear`; I moved it.

> "Deductible pension income, other than military retirement pay, includes state and federal pension
> benefits and retirement benefits received from plans established and maintained by an employer for the
> benefit of its employees" (p8, Schedule 1S line 4; FAQ item 14, p9, has the same words)

"State" is not limited to Maine. Where the booklet means Maine alone, the same paragraph says so by name
("the Maine Public Employees Retirement System (MainePERS)"), and p8 and the FAQ also name 457(b) plans of
"state and local government". But no sentence names a pension paid by another state. No reciprocity rule or
paying-state list was found in the booklet, the form, the Schedule 1S worksheet or the FAQ, so there is no
`paying_states` and New York is treated like any other state. Same reading as Missouri's "state". The
projection carries an `understates_tax` approximation for it.

**Rule:** a Maine resident with a New York State pension deducts it on Schedule 1S line 4 like any other
eligible pension: up to 48,216, less all Social Security and railroad benefits received, phased out above
federal AGI of 125,000 / 187,500 / 250,000 at a rate the saved documents do not print. No age test (other
than the under-55 payment rule).

### 2. Its own and federal government pensions

Same entry, same rule, by the quote above. Cap: "you and your spouse (if married) may each deduct up to
$48,216 of other eligible pension income" (p8); FAQ items 14 and 15 repeat it. Age test: none on the person.
Contributory test: none printed. Military is separate and exempt: "The benefits received under a United States
military retirement plan, including survivor benefits, are fully exempt from Maine income tax" (p8; FAQ item
14); no cap and no Social Security reduction.

MainePERS (Maine's own system) also has Schedule 1S line 7, for those who "retired after 1988". It is not an
exemption of the pension: box 2a minus box 16 on the 1099-R, the pick-up contributions already taxed by Maine.
A projection cannot compute it (`not_modelled`, `has_pension`). Modelling it as an uncapped subtraction of
`public_pension` would have exempted every MainePERS pension in full, so it is not in the projection's reliefs.

### 3. Private pensions, IRA and employer-plan distributions, Roth conversions

Same entry. Named on p8: IRC 401(a), 401(k), 403 employee annuities, 408 IRAs, 408A Roth IRAs, 408(k) SIMPLE,
408(p) SEPs, 457(b). `annuity` is kept from both readers but only "employee annuities" are named; an
approximation covers annuities bought outside an employer plan.

Roth conversions do not qualify, and the booklet says so:

> "Note that a conversion of benefits from one account to another does not qualify for the pension income
> deduction. For example, a deduction may not be taken when a taxpayer converts a traditional IRA to a Roth
> IRA. The taxpayer, in this case, does not receive a retirement or IRA benefit at the time of conversion."
> (p8)

So `roth_conversion` is neither in `covers` nor `covers_unclear`; the words are in `not_covered`.

Also not qualifying (p8): 457(f) plans, refunds of excess contributions, Form 4972 lump sums, disability
reported as wages, MainePERS pick-up amounts on line 7, benefits earned by another person except a surviving
spouse, and distributions before age 55 that are not a series of equal periodic payments (p3 and p8, new for
2025, effective September 24, 2025). The age 55 rule tests the payment, not the person, so it is not `min_age`:
a person of 52 on a lifetime pension qualifies.

### 4. Social Security

`exempt`. "If included in federal adjusted gross income, enter the taxable amount of social security benefits
issued by the U.S. Government and railroad retirement benefits (tier 1 and tier 2)" (p7, Schedule 1S line 3).
Second line: Quick Facts p11 says Schedule 1S reports "income that is taxable by the federal government but not
in Maine". FAQ item 15 shows the other effect: benefits use up the pension cap, "all taxable and nontaxable".

### 5. Brackets, standard deduction, exemptions

**Brackets:** p13 prints three schedules, confirmed by the readers and by me: 5.8%, 6.75%, 7.15%. Single and
married separate from 0 / 26,800 / 63,450, head of household 0 / 40,200 / 95,150, joint and surviving spouses
0 / 53,600 / 126,900. Second check: I recomputed all 521 printed table rows (pp12-13) from these schedules. All
agree within 1 dollar except the two lowest rows (0 to 50 and 50 to 100), which the table rounds down by up to
1.45. No surtax and no recapture printed.

**Standard deduction:** 15,000 / 30,000 / 15,000 / 22,500, in the p5 chart and in Quick Facts p11. The 2,000 and
1,600 additions are the chart's steps, in `notes` with the arithmetic.

**Personal exemption:** 5,150 per exemption, on p5, p6, p11 and form line 18.

**Dependents:** no deduction. A refundable credit of 305, or 610 under six (p3, p10, p11). Both readers left it
in notes. Two relief entries now hold the amounts; the projection has it in `not_modelled` (`has_dependents`).

## Structured differences

| Difference | A | B | Settled | Page |
|---|---|---|---|---|
| Phase-out on the age 65 and blind additions (14 fields) | same as the standard deduction | none | A. Worksheet line 6 enters "your 2025 standard deduction from the chart above", which includes the boxes | p5 |
| Itemized limit 36,300 as a deduction entry (3 fields) | notes | `other` deduction | Notes. It is a limit, not an amount anyone deducts | p11 |
| Schedule 1S line 3 `who.basis` (6 fields) | `return` | `each_person` | `return`. The line has no age or person test (brief rule 5) | p7 |

## Differences the comparison counts as wording, settled anyway

- `public_pension_other_state`: both `covers_unclear`; moved to `covers` (question 1).
- Line 6 form: A subtraction, B exempt_in_full. p8 says "are exempt". `exempt_in_full`.
- Line 6 and the pension deduction: A `cannot_combine_with`, B `not_covered`. p8 says the amount "must exclude any
  amount included in" the deduction: no double count, not a bar on claiming both. `not_covered`.
- Military `not_covered`: B listed the service-branch sentence. It says who qualifies, so `other_conditions`.
- Line 7 "contributory plan": B only, and B's own note says the booklet has no such test. Dropped.
- Worksheet cite: both said p5; the exemption worksheet is on p6.
- A's nulls for `min_age` etc. are dropped.

## One-sided entries

- Kept from B: the form cite for `base`, the indexing cite, "income must be included in federal AGI".
- Kept from A: the additions' phase-outs. A's note on senior volunteer benefits (line 16, up to 1,465) stays in
  notes; too small and narrow for an entry.
- Added by me: indexing entry for the dependent credit thresholds; the dependent credit reliefs.

## Phase-outs: what is exact and what is not

The projection's `effect` has no "share of the amount" form, and it can only hold figures the record prints.

- **Standard deduction:** exact. On the base amount the worksheet is 0.2 per dollar for every status (15,000 /
  75,000 = 22,500 / 112,500 = 30,000 / 150,000). `phase_out_rate` with rate 0.2 in both layers. 0.2 is derived;
  the arithmetic is in the record's notes. The validator finds "20" in the text by chance, so its pass proves
  nothing here.
- **Age 65 additions and the personal exemption:** `other` in the record with the formula. No single rate fits
  (2,000 / 75,000 is not 1,600 / 150,000; 5,150 / 125,000 is not 5,150 / 62,500), and 0.0412 is not printed, so
  the validator would reject it. The projection uses `removes` at the threshold, chosen over leaving the
  phase-out out because it is exact above the band and wrong only inside it, while leaving it out would be
  wrong for every income above the threshold. `overstates_tax`, at most about 143 per box and 368 per exemption.
  (Blindness: `not_modelled`, as Minnesota.)
- **Pension deduction:** the rate and width are not printed. The record keeps `effect: other` with the
  thresholds. The projection applies the deduction in full, with a `not_modelled` warning (`has_pension`) and an
  `understates_tax` approximation, at most about 3,447 a person a year. I did not use `removes`: a cliff would
  be a rule the booklet does not print, on an amount ten times larger than the others.

## Unsure

1. **Pension phaseout rate and width:** not printed. Direction: understates tax above the thresholds. The
   worksheet is the fix.
2. **Pension phaseout measure:** p3 says federal AGI, FAQ item 14 says Maine AGI. The record follows p3, the most
   direct print: it gives the figures with the measure and cites the law; the FAQ has no figures. Not computed
   in the projection, so it costs nothing until the rate is found.
3. **Other-state pensions:** a reading (question 1). Direction: understates tax if wrong.
4. **Whose benefits reduce whose cap:** recorded per person ("may each deduct"), with `cap_reduced_by` taking that
   person's own. Not said in words. Direction: either.
5. **Under-55 rule:** p3 says "an employee retirement plan"; p8 has no such limit and sits under "Pension benefits
   that do not qualify". Whether it reaches IRA withdrawals is not clear. The warning fires for anyone under 55.
6. **Indexing of the cap:** assumed not indexed. The FAQ's "for tax year 2025" and its pointer to each prior
   year's worksheet suggest the 48,216 changes by year, but no rule is stated. The `pension_income_deduction`
   indexing entry is `yes` for the thresholds only, and says so.

## Schedule 1S worksheets (added 2026-11-07)

The 2025 Schedule 1S, archived after settlement, prints the Pension Income Deduction Worksheet (P1 to P10) and the Worksheet for Phaseout of Non-Military Pension Income Deduction. The phaseout is a straight line: the deduction loses (federal AGI - threshold) / 100,000 of itself (50,000 if married filing separately), at most all of it. The measure is federal AGI (line 1, 'Form 1040ME, line 14'), settling page 3 against FAQ item 14. Military retirement pay (P9) is not phased out. The record holds the rule; the projection keeps it not_modelled because the format has no straight-line share reduction (Vermont needs the same; both were later modelled with `share_phase_out`). Done in the main session after the settler stopped at the weekly limit.

## 2026-11-07: format v1 adoption

Adopts `income_test.effect: share_phase_out` (docs/decisions.md, "format for the first frozen schema"). Every
width is a figure the worksheets print on their line 4; each worksheet enters line 5 to four decimals (the
booklet's boxes `_ . _ _ _ _` on pages 5 and 6; Schedule 1S page 2 says "If one or more, enter 1.0000").

**Record.**
- `pension_income_deduction.income_test`: `other` → `share_phase_out`, width 100,000 (50,000 married filing
  separately), `share_decimals` 4, from the Schedule 1S page 2 phaseout worksheet lines 3 to 5 and P6 to P8.
  Cite now names Schedule 1S PDF page 2. The notes that said the worksheets were not saved and the measure was
  unsettled are rewritten: worksheet line 1 is federal AGI (Form 1040ME line 14).
- `standard_deduction.phase_out`: `phase_out_rate` 0.2 → `share_phase_out`, width 75,000 / 112,500 / 150,000
  (single and separate / head of household / joint and surviving spouse), `share_decimals` 4 (booklet page 5
  worksheet lines 4 and 5). The 0.2 was derived, not printed; the share is what the form enters.
- `age_65_additional_standard_deduction` and `blind_additional_standard_deduction`: `other` → the same
  `share_phase_out` as the standard deduction (line 6 is the whole chart amount, boxes included).
- `personal_exemption.phase_out`: `other` → `share_phase_out`, width 125,000 (62,500 separate),
  `share_decimals` 4 (page 6 worksheet lines 4 and 5).
- One new settlement note line says so.

**Projection.**
- Pension income deduction gets the `income_test` (federal AGI, the three thresholds, width, 4 decimals).
- Standard deduction, 65-or-over addition and personal exemption phase-outs use `share_phase_out` with the
  record's widths (were `phase_out_rate` 0.2 and `removes`).
- `not_modelled`: the pension phaseout marker removed. A second marker carried the same text with
  `age_range` 0 to 54: it was the under-55 marker, overwritten by a text replace in commit 1a1f25a. Its text is
  restored ("Distributions received before age 55 ...") and its trigger narrowed from `has_pension` to
  `has_retirement_account_distribution` with `age_range` 0 to 54, as the projection guide now asks.
- Approximations removed (now exact): pension deduction applied in full above the thresholds; 65-or-over
  additions and exemption removed in full at the threshold; standard deduction at 0.2 per dollar. None added.

**Dollar effect** (projection before → after):
- Pension phaseout, single, federal AGI 155,083 with a 40,000 private pension: deduction 40,000 → 27,968 (share
  0.3008); Maine AGI rises 12,032 and the standard deduction shrinks with it; tax 6,494.99 → 7,527.31
  (+1,032.32). At or past the end of the band the deduction is 0: up to 7.15% x 48,216, about 3,447 more a
  person a year.
- 65-or-over addition inside the band, single, Maine AGI 115,075: 2,000 removed → 1,598 kept; tax 6,494.31 →
  6,380.05 (-114.26).
- Exemption inside the band, joint, Maine AGI 450,100: 10,300 removed → 6,180 kept; tax 31,165.35 → 30,723.48
  (-441.87).
- Standard deduction: four-decimal share instead of 0.2 per dollar: at most 0.00005 x the chart amount (1.82 on
  36,400) of deduction, about 13 cents of tax.

**Checks.** Reworked (verified removed): `me_2025_pension_over_phaseout_threshold` (new federal AGI 155,083, so
the share is not a rounding tie; boundary now `at_or_above`), `me_2025_age65_addition_inside_band`,
`me_2025_exemption_inside_band_joint`. Added: `me_2025_pension_phaseout_at_threshold`,
`me_2025_mfs_pension_phaseout_inside_band`, `me_2025_pension_phaseout_past_end` (with military pay, not phased
out), `me_2025_std_deduction_at_threshold`, `me_2025_joint_std_deduction_inside_band`,
`me_2025_exemption_at_threshold`, `me_2025_exemption_inside_band_separate`. Eight other cases changed only in
`accepted_warnings` (the pension phaseout warning is gone; kept their `verified`).

**Unsure.** The worksheets do not say how line 5 is rounded to four decimals (rounding or cutting off). The cases
avoid shares where the two differ; the gap is at most 0.0001 of the amount (about 5 dollars of deduction on
48,216, 35 cents of tax). Rounding the share lost (the form) or the share kept (the schema's wording) differ
only on an exact half, also avoided.

- Main session, 2026-11-07 (format v1): `social_security_basis: gross` on the pension income deduction (the cap is reduced by all benefits received, taxable or not).

## 2026-11-08: marker ids and indexing covers

- Marker ids given: first from_record id (warning code unchanged): `pension_income_deduction`, `mainepers_subtraction`, `dependent_exemption_credit`, `blind_additional_standard_deduction`, `us_obligation_interest_subtraction`; descriptive: `me_property_tax_fairness_credit` (no from_record id); `me_other_credits_and_returns` (no from_record id).
- Indexing covers: `brackets` -> `brackets`; `deductions` -> `deductions`; `relief_caps` -> `reliefs.cap`; `pension_income_deduction_phase_out` -> `reliefs:pension_income_deduction.income_test`.
- Split the pension income deduction's figures: added `pension_income_deduction_phase_out` (indexed true) for its income test, from the record's existing `pension_income_deduction` entry (booklet PDF page 3: 'For tax years beginning after 2025, the phaseout threshold amounts are adjusted for inflation'); the 48,216 cap stays under `relief_caps` (assumed).
- Every `assumed` answer was checked again against the archived sources (searched for indexed, inflation, cost-of-living, adjusted annually, each year, CPI, fixed): none says, so all stay `assumed: true`.
- `tools.checks --fix-warnings` updated the cases' accepted_warnings where a code changed; nothing else in the cases changed.

## 2026-11-08: indexing settled from statutes

- `brackets` (projection `brackets`): indexed, 36 M.R.S. 5403(1): Chained CPI, rounded down to 50, never falls. Record `brackets` added as yes.
- `deductions` (projection `deductions`, amounts and phase-outs): indexed, 36 M.R.S. 5403(2), (4), (7), (8); 5124-C(1-B) to (1-D); 5126-A. The finding lists three parts (standard deduction, age-65 addition, personal exemption), all indexed, so one entry stays. Record `standard_deduction`, `age_65_additional_standard_deduction`, `personal_exemption` added as yes.
- `relief_caps` (projection `reliefs.cap`): indexed, 36 M.R.S. 5122(2)(M-2)(2)(d)(iv): the Social Security maximum benefit at full retirement age. Record `pension_income_deduction` already says yes with the booklet cite and is kept; its index text says the 48,216 cap "is not stated to be indexed" (true of the booklet), while the statute makes the cap the yearly Social Security maximum. Not contradicting the yes, so not changed; reported.
