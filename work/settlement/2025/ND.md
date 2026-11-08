# ND 2025 settlement

Readings: `work/extract/2025/ND.r6.A.json`, `ND.r6.B.json`. Sources: `sources/archive/2025/ND/`. Pages are PDF pages (the booklet's printed page number is 2 lower). PDF pp.16 and 29 were rendered and read as images as well as text.

## Structured differences: 23

| Fields | A | B | Settled | Source |
|---|---|---|---|---|
| brackets rate at 0% and 2.5%, four statuses (8) | 0, 0.025 | 0.0000, 0.0250 | Same numbers; 0, 0.0195, 0.025 | p.29 prints 0.00%, 1.95%, 2.50% |
| College SAVE deduction (4: single, joint, per, what) | 5,000 / 10,000, per return | notes only | Kept; 5,000 also written for separate, head of household, surviving spouse | Booklet p.15 line 12: "up to a maximum of $5,000 ($10,000, if married filing jointly)" |
| Organ donor deduction (3) | 10,000 per return | notes only | Kept | ND-1SA p.2 line 6: "up to $10,000 of qualified expenses" |
| Stillborn child deduction (3) | 5,241 per dependent | notes only | Kept | ND-1SA p.2 line 8: "enter $5,241 on line 8a" |
| Native American exempt income (4) | relief, all_income, person scope | notes only | Kept, A's form | Booklet p.14 line 7; Form ND-1 line 7 |
| Peace officer covers_unclear (1) | employer_plan_distribution, public_pension_other_state | public_pension_other_state | A | Booklet p.14: "Only include benefits issued by your employer's retirement plan" does not say which kinds of plan |

Of the 23: 9 decided from the booklet (4 + 4 + 1), 6 from Schedule ND-1SA, 8 were spellings of the same number, confirmed on p.29. `per` for the organ donor and stillborn deductions is a judgement call: the schedule says neither outright.

## One-sided entries

Kept: the three deductions, the Native American entry and A's `not_covered` for line 5 (both readers had it, worded differently). The cite on B's missing `all_other` indexing entry comes from A.

Dropped: A's `not_covered` on railroad. It says Tier 1 benefits go on line 8, which means they are covered; moved to notes.

Kept in notes, from B: reciprocity (p.8) covers compensation and wages only.

Added by the settler, in neither reading as an entry: `marriage_penalty_credit`.

## Flagged points

**"$ 80.975" (p.29, joint schedule, second row).** The rendered page shows the period, so it is a misprint in the booklet and not a conversion error (A's note said "OCR/typo"). Corrected to 80,975 because:
- the same page prints 80,975 in the Over and But Not Over columns;
- 1.95% x (298,075 - 80,975) = 4,233.45, exactly the printed base of the top row;
- the Tax Table gives joint tax 0 in row 80,950-81,000 and 1 in row 81,000-81,050, and 371 in row 99,950-100,000 (19,000 x 1.95% = 370.50).

The other top-row bases also check: 3,828.83 single, 2,116.73 separate, 4,026.75 head of household. Table rows just past each start and at the 99,950 row agree for every status.

**Marriage penalty credit (Form ND-1 line 22; booklet pp.16-17).** Recorded as a relief with the worksheet in `cap_rule`, and in the projection as `not_modelled` (`warn_when: always`) with an `overstates_tax` approximation.
- A said maximum 312.00. B said 15,750 on line 13 and flagged it as not confidently tied to a line. The rendered p.16 shows 15,750.00 preprinted on line 5 and 312.00 on line 13, so A is right.
- `covers` is `all_income` with `credit_basis: tax`, following Connecticut's personal credit, because the credit is a difference of taxes and not a share of one income kind. Listing pension kinds would have shown it as a pension relief in `tools.report_pensions`.
- `income_test.effect` is `other`: 81,036 is a floor the credit needs, not a phase-out. The second gate, 47,550, is in `other_conditions`.
- Recomputed from the printed figures: line 12 first turns positive at a lower qualified income of 48,250, and reaches 311.51 when all three computations are in the 1.95% band. Examples: 120,000 joint with 60,000 lower income gives 229.13; 200,000 with 100,000 gives 311.51; 500,000 with 100,000 gives 482.01 on line 12, capped at 312.

**No state standard deduction.** Confirmed: the base is federal taxable income and the form has no such line. `base.deductions` is empty in the projection; the three record deductions are `other` and expense-based, so they are `not_modelled`.

## Always-settled questions

1. **Another state's government pension, New York in particular:** not found. Neither `covers` nor `not_covered` holds `public_pension_other_state`; it appears only in `covers_unclear` on the peace officer entry. New York appears nowhere in the sources. No subtraction line exists, so the pension stays in the starting figure. Quotes: p.4, "The starting point for computing North Dakota taxable income perpetually conforms to the computation of federal taxable income."; p.6, a full-year resident must file "even if you ... have income from sources outside North Dakota."
2. **Own and federal government pensions:** no general relief. Same quote from p.4. Exceptions: line 9, "The exclusion is allowable for a retired licensed peace officer with a minimum of 20 years of service or that was retired disabled." Line 14 covers military retirement: "enter on this line the amount of taxable military retirement benefits that you reported on Form 1040 or Form 1040-SR, line 5b."
3. **Private pensions, IRA and employer-plan distributions:** no relief. The booklet treats them as income: p.17, "Taxable portion of IRAs, pensions, annuities, and social security benefits reported on Form 1040 or 1040-SR, lines 4b, 5b, and 6b." Lump-sum distributions on Form 4972 are added back: ND-1SA p.2, "you must enter on this line the amount from Form 4972, line 6 plus line 10." **Roth conversions:** not found in the booklet.
4. **Social Security:** exempt. Booklet p.15, "Enter on this line the taxable portion of your Social Security benefit`s reported on Form 1040 or 1040-SR, line 6b." Second document: Form ND-1 line 15, "Social security benefit exclusion", in the Subtractions block.
5. **Schedules, deductions, exemptions:** four printed schedules on p.29 (surviving spouse uses joint): 0% / 1.95% / 2.5% starting at 48,475 and 244,825 single; 80,975 and 298,075 joint; 40,475 and 149,025 separate; 64,950 and 271,450 head of household. No state standard deduction, exemption, age-65 or blindness amount is printed; "standard deduction" appears only for the federal one (pp.4, 14).

## Projection choices

- Modelled: brackets, Social Security exempt, railroad, military retirement (`needs_input: pension_source`), 40% of dividends, 40% of long-term gains.
- `not_modelled`: marriage credit, peace officer, U.S. obligations, military pay, Native American income, College SAVE, organ donor, stillborn, Form 4972 addition, credit for tax paid to another state. The last two have an empty `from_record` because the record has no entry for them.
- Line 11 stays out of the reliefs: `covers: wages` would exempt all wages.
- `muni_interest` is `all_exempt`, with an `understates_tax` approximation; see below.

## Unsure

- **Municipal interest.** The record is `not_stated`, but the projection schema has no such value. `all_exempt` follows the form: it starts from federal taxable income and no addition names this interest. No statute was read.
- **Peace officer `covers: public_pension`** rests on reading an officer's employer plan as a government plan. Both readers read it so; the booklet does not say it.
- **Dual status military technician** benefits are a federal civil service pension kept in the military entry as a condition, so the report's federal row does not show them.
- **Marriage credit `covers`** is a fit to the schema, not the booklet's words. The qualified-income kinds are in `other_conditions`.
- **Schedules ND-1CR and ND-1TC** are not in the sources, so those credits are unread.

## 2026-11-08: marker ids and indexing covers

- Marker ids: all 9 markers have an `id`. Descriptive ids (no from_record id of their own): `nd_lump_sum_distribution_addback`, `nd_other_state_tax_credit`; the rest take their first from_record id, so their warning codes are unchanged. `tools.checks --fix-warnings` rewrote the cases' accepted_warnings (the old shared code state_rule_not_modelled:unnamed becomes the new ids); nothing else in the cases changed.
- Indexing covers: `brackets` covers brackets (no deductions or relief figures are grown). No split needed.
- Assumed entries: searched the archived sources (docling, pypdf and page text) for indexed, inflation, cost of living, adjusted annually and consumer price index, and for statements that figures are fixed; nothing says, so every `assumed: true` stays.
