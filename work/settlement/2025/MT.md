# Montana 2025 settlement (round r6, 2026-11-07)

Readings: `work/extract/2025/MT.r6.A.json`, `MT.r6.B.json`. Sources: Form 2 Instructions, Form 2, and the Tax Simplification Resource Hub page.
Comparison: 16 structured differences, 52 wording differences.

## Structured differences (16 fields, 2 questions)

| Fields | Question | A | B | Settlement |
|---|---|---|---|---|
| 10 | Where the age 65 subtraction sits | `base.deductions`: age_65_exemption, per person, 5660 | relief: all_income, cap 5660 per person, min_age 65; deductions empty | Base deduction, once. |
| 6 | What the U.S. obligation subtraction covers | interest, dividends | interest | A. |

**Age 65.** The readers agree on the facts, which the booklet prints: "Taxpayers 65 and older receive a $5,660 subtraction from federal taxable income. If married filing jointly, and both are 65 and older, the subtraction is equal to $11,320. This amount is adjusted annually for inflation." (Instructions PDF p13, line 6; Form 2 PDF p1, line 6.) So the booklet fixes the figures but not the placement. The placement comes from `docs/projection-guide.md`: "Every record deduction a projection can apply goes in `base.deductions` ... an age-65 amount gets `min_age`". It is a flat amount with no income kind, income test or interaction with another relief, and `age_65_exemption` is the schema's own kind. There is no relief entry, so it cannot be counted twice. Projection: per person, min_age 65.

**U.S. obligations.** PDF p23, line 9: "interest on United States government obligations and mutual fund dividends attributable to that interest". Both kinds are covered.

## One-sided and split entries

- Military line 13: both readers wrote one entry. Split into `working_military_retiree_subtraction` and `military_survivor_benefit_subtraction`, because only retirees have the Montana-source earned income limit (PDF p25). Brief rule 3.
- A's note on the state income tax add-back: kept, and widened to the Worksheet B limit (PDF p13, p22).
- A's note on the 2026 and 2027 tables and B's note on 2026 brackets: kept as one note with the printed figures (PDF p5, p48).
- Exempt tribal income, 529, ABLE, MSA, homebuyer and business subtractions: both left out, kept out, as in other records. A note states that tribal income includes pensions (PDF p24).
- Elderly Homeowner/Renter Credit and earned income credit: both left out, kept out (`docs/design.md`: credits other than relief for retirement income and Social Security are out of scope). Both carry a `not_modelled` marker with an empty `from_record`.
- Added by the settler: the Schedule 2EC mention of Roth conversions (PDF p45), the hub sentence on federally untaxed income, and the Worksheet line 3 limit on gains (Form 2 PDF p2).

## Facts always settled

1. **Another state's government pension, including New York State: not found in the booklet.** It is not in any `covers` and not in `not_covered`. The nearest text is the hub's repeal list ("Several deductions are repealed, including: ... Partial pension, annuity, and IRA deduction") and the Instructions PDF p21 definition: "Montana subtractions are all items of income that are included in federal taxable income and are deducted to determine Montana taxable income". No Schedule I line (Form 2 PDF p3, lines 8-23) or line 21 code (PDF p27-28) names one. The only reciprocity is North Dakota, for wages (PDF p12). Result: taxed as far as it is in federal taxable income.
2. **Montana and federal government pensions: not found in the booklet.** Same text, same result. The hub's list "Which subtractions are still available?" names none. Railroad and military are separate entries.
3. **Private pensions, IRA and employer-plan distributions, Roth conversions.** No subtraction is printed. Hub: "Partial pension, annuity, and IRA deduction" repealed. Instructions PDF p13, line 11b: "If you received pensions, retirement income, or IRA distributions, the Montana tax withheld is reported in Box 14 of your federal Form 1099-R." PDF p33, line 9 treats them as "not Montana source income" for a nonresident and counts them for a part-year resident while resident. Roth conversions are named only in the Schedule 2EC household income definition (PDF p45: "conversions from a traditional IRA to a Roth IRA"). No relief exists to cover them, so `covers_unclear` is not needed. They are taxed through federal taxable income; this is a reading, not a printed sentence.
4. **Social Security: taxed.** Hub, "Montana Taxable Income Calculation": "Taxable Social Security Income and net operating losses are included in Montana taxable income to the extent that they are included in federal taxable income." Second document: Form 2 Schedule I prints no Social Security subtraction; Tier I railroad benefits (line 22) are the only such line. Instructions PDF p34, line 12 counts taxable benefits for residents' periods.
5. **Brackets and deductions.** All four schedules are printed (PDF p18): 4.7% then 5.9% from 21,100 single and separate, 42,200 joint and surviving spouse, 31,700 head of household. Both readers agree. Standard deduction: "Montana no longer has a specific standard deduction." Exemptions: "Montana no longer has dependent or personal exemptions." (Both hub FAQ.)

## Projection decisions

- **Long-term gains: represented.** The format allows one `extra_rate`, and a negative value passes the schema. Gains run through the brackets on top of ordinary income, which reproduces the stacking on the bracket top minus ordinary income. The extra rate is -0.018 (4.1% less 5.9%, in `derived_figures`). This is exact above the bracket top and 2.9% against 3% inside it. The alternative, -0.017, would be exact below the top but its error would grow without limit above it. Marked `understates_tax`: at most 21.10, 31.70 or 42.20 a year. Tested against the Form 2 page 2 worksheet at five income and gains pairs; the largest gap was 21.10 for single, and it needs gains limited to taxable income first.
- **Military subtraction: not representable, so marked.** The earned income limit has no field, and the five-year limit and residency dates are not yearly facts. Both entries are in `not_modelled` with `has_military_pension`, plus an approximation marked `overstates_tax`. Modelling a bare 50% was rejected: a retiree with no Montana earned income would wrongly get it every year for life, which is a far larger error than five years of overstatement.
- U.S. obligation interest and active duty pay: `not_modelled`, `never`, as in other projections.
- Railroad: `exempt_in_full` in the projection, as in other states; `subtraction` in the record, as both readers wrote.

## Unsure

- Social Security and the pension treatment rest on the hub, whose text describes the 2024 change and still prints the 5,500 subtraction, not 5,660. The 2025 booklet does not contradict it, and no 2025 sentence repeats it.
- The government pension rule is a reading from silence plus the repeal list. No sentence names government pensions, and the statute was not read.
- One spouse 65 on a joint return and the age test date are not printed. 5,660 per qualifying person is a reading.
- No state before Montana uses a negative `extra_rate`. A consumer must accept it and limit gains to taxable income.
- "Five years after tax year 2024, which is tax year 2028" is copied as printed.
- `brackets: indexed false, assumed` follows the guide, but the booklet prints legislated cuts for 2026 and 2027, so a marker is in `approximations`.

## 2026-11-08: marker ids and indexing covers

- Marker ids: all 6 markers have an `id`. Descriptive ids (no from_record id of their own): `mt_elderly_homeowner_renter_credit`, `mt_earned_income_credit_tribal_income`; the rest take their first from_record id, so their warning codes are unchanged. `tools.checks --fix-warnings` rewrote the cases' accepted_warnings (the old shared code state_rule_not_modelled:unnamed becomes the new ids); nothing else in the cases changed.
- Indexing covers: `brackets` covers brackets; `deductions` covers deductions (the age 65 subtraction, indexed per the record). No split needed.
- Assumed entries: the only indexing statements found are the age 65 subtraction (already indexed in the record) and figures outside the projection (529 subtraction, volunteer firefighter subtraction); HB 337's 2026 bracket change is a law change, not indexing. `brackets` stays assumed.

## 2026-11-08: indexing settled from statutes

Statute research (work/indexing/findings*.json) settled every projection indexing entry that was `assumed: true`:

- `brackets` (brackets): indexed, indexed from 2028, Mont. Code Ann. 15-30-2103(3) (as it stood for tax year 2025, struck by HB 337 Sec. 1 for 2026); 15-30-2101(12) 'inflation factor'; HB 337 (2025), Secs. 1, 2, 4-6
- Record `indexing`: updated brackets -> yes.
- `brackets` is indexed true with indexed_from 2028. HB 337 (2025) sets fixed bands for 2026 (47,500 single / 71,250 head of household / 95,000 joint) and from 2027 (65,000 / 97,500 / 130,000), so the 2026-2027 bands are new fixed amounts, not the 2025 bands held flat; a projection that holds the 2025 bands until 2028 is wrong for those years. The note and the record's index say so.
