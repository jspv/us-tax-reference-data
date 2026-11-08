# Settlement: Louisiana, tax year 2025

- Readings: `work/extract/2025/LA.r6.A.json`, `work/extract/2025/LA.r6.B.json` (round r6)
- Sources: `sources/archive/2025/LA/` (2025 IT-540 Instructions, Revised 7-26; 2025 Form IT-540; the LDR FAQ page "Is there a list of retirement system benefits that may be excluded from Louisiana income tax?"; the LDR forms page)
- Outputs: `data/states/2025/LA.record.json`, `data/states/2025/LA.projection.json`
- Settled: 2026-11-07

Page numbers are PDF pages of the instructions unless the Form or the FAQ page is named.

## Comparison

`uv run python -m tools.compare` reported **20 structured differences** (77 wording differences). The readers
disagreed on five things. No two readers recorded different values for the same field: every difference is
one reader having something the other did not, or splitting a rule differently.

| # | Lines | Field | A | B | Source | Settled |
|---|---|---|---|---|---|---|
| 1 | 9 (3 relief keys x covers, form, who.basis) | Railroad Retirement | own entry; 04E covers `public_pension`, `military_pension` | folded into 04E with `railroad_retirement` | FAQ page 1: "Railroad Retirement System Benefits received by federal retirees may be excluded from Louisiana taxable income." Page 7 code 04E does not name railroad benefits. | A's own entry, `la_railroad_retirement`: it has its own condition and its source is the FAQ page, not the 04E text |
| 2 | 4 (cap.all, covers, form, who.basis) | Code 49E disability income | recorded, cap 6,000 | not recorded | Pages 9 and 10: "Persons receiving disability income (La. R.S. 47:44.1(B)) for a permanent, total disability may exclude up to $6,000 of annual disability income from their taxable income." | Kept |
| 3 | 3 (applies_to, treatment, value) | Code 20E capital gain | `other`, `deduction_share`, `1` | note only | Page 8: "provides a deduction for net capital gains ... This deduction is limited to those with installment and perfected sales prior to January 1, 2025." | Kept, because an installment sale can still report gain on a 2025 return. Changed to `exempt`, value 0: the booklet prints no share, the code sits under "EXEMPT INCOME LINES 4A THROUGH 4G", and AL, AR and NJ record full exclusions the same way |
| 4 | 3 (indexing entries) | Indexing | `not_stated` entries for the standard deduction, 06E and brackets, plus `all_other` | `all_other` only | Searched for inflation, consumer price, indexed and adjusted: the only hit is the School Readiness credit (page 1, code 66F), not a recorded figure. Extraction brief rule 8 asks for an entry only for a figure the booklet speaks about. | B: `all_other` only |
| 5 | 1 | Code 10E `cap_per` | left out | `person` | Page 8 tests each resident's own active duty, exempts that person's compensation "up to $50,000", and writes the example to "you". | `person`. Judgement: the booklet never says "per person" outright. No tax effect here, because 10E is `not_modelled` |

Decided from the sources: 17 of the 20 lines (8 from the booklet alone, the 9 railroad lines from code 04E
together with the FAQ page). The other 3 (indexing) were decided by extraction brief rule 8, after a search
confirmed the booklet says nothing.

## The facts every settlement must settle

1. **Another state's government pension, and a New York State pension.** Not found in the sources by name, and
   no reciprocity rule or paying-state list exists, so `paying_states` is not used. Both readers put
   `public_pension_other_state` in code 06E's `covers` as a judgement call. I kept it, from three printed lines:
   - Page 7, 05E is limited to "retirement systems whose benefits are specifically exempted by law from
     Louisiana income tax", and every system on the FAQ list is a Louisiana system.
   - Page 9, 49E: "Do not list income earned in another state. Residents of Louisiana are taxed on all income,
     regardless of where the income was earned."
   - Page 7, 06E: "'Annual retirement income' that is taxable to Louisiana is any distributions from a pension,
     an annuity, or an individual retirement arrangement (IRA) that you receive and report on Federal Form 1040
     or 1040-SR, Lines 4b and 5b. Do not include retirement benefits that are coded as 02E, 03E, 04E, or 05E."

   **Result:** a Louisiana resident with a New York State pension pays Louisiana tax on it, less up to 12,000 a
   person from age 65; under 65 there is no relief.

2. **Own and federal government pensions.** Exempt in full, no cap, no age test, no income test.
   - Page 7, 02E: "retirement benefits received from the Louisiana State Employees' Retirement System"; 03E the
     same for the Teachers' system.
   - Page 7, 04E: "retirement benefits received from a Federal Retirement System, including benefits received
     from a military survivor benefit plan". The FAQ page adds "federal retirees, both military and nonmilitary",
     which is the source for `military_pension`.
   - Page 7, 05E: the other Louisiana systems. The FAQ page lists them and adds Title 11 Chapter 1 benefits,
     "including disbursements of money from DROP accounts".

3. **Private pensions, IRA and employer-plan distributions, Roth conversions.** No relief under 65. From 65, code
   06E: "Up to $12,000 of your annual retirement income may be exempted from state taxation". The sources name
   "a pension, an annuity, or an individual retirement arrangement (IRA)"; 401(k) plans are not named, and
   `employer_plan_distribution` is listed because the worksheet takes everything on Lines 4b and 5b. Roth
   conversions are not named, so `roth_conversion` stays in `covers_unclear`, as both readers had it.

4. **Social Security.** Exempt. Page 7, 07E: "Social security benefits that are taxed on your federal return are
   exempt from Louisiana tax. Enter the amount shown on your Federal Form 1040 or 1040-SR, Line 6b." Checked
   against Form IT-540 Schedule E ("Taxable Amount of Social Security 07E") and the FAQ page.

5. **Brackets, standard deduction, exemptions.**
   - Flat 3%. Page 1: "changed the income tax rate to a flat tax rate of 3%". Page 3 and Form Line 11: "Multiply
     Line 10 by .03. Round to the nearest dollar." No schedule or tax table is printed for any status, so
     `brackets.derivation` does not apply.
   - Standard deduction. Page 3 and Form Line 8: "If your filing status is 1 or 3, enter $12,500; 2, 4, or 5,
     enter $25,000." Head of household is 25,000, as is qualifying surviving spouse.
   - Exemptions: none. Page 1: Act 11 "repealed the exemption for an additional $1,000 deduction for persons 65
     and older, blind, and dependents. These lines were removed from the tax form."

## Code 06E joint-return wording (settled from the worksheet)

The paragraph says: "If your filing status is married filing jointly, both you and your spouse are age 65 years
or older, and each of you received annual retirement income, up to $12,000 of the annual retirement income that
each taxpayer receives may be exempt". The worksheet says: "5. For each taxpayer 65 or older, enter the amount
from Line 3 or Line 4, whichever is less", and Line 6 adds Lines 5(a) and 5(b) on a joint return.

**Settled:** the test is person by person, `who.basis: each_person`, `min_age: 65`, cap 12,000 per person, on that
person's own income. On a joint return with one spouse 65 or older, that spouse enters up to 12,000 of his or her
own retirement income on Line 5 and the younger spouse enters nothing. The paragraph's "both" describes the case
where two amounts are claimed. Both readers' `other_conditions` line repeating "both spouses" is removed, because
it would have read as a condition on the whole relief.

The FAQ page agrees: "Persons 65 years or older may exclude up to $12,000 of annual retirement income", and "If
only one spouse has retirement income, the exclusion is limited to $12,000." So one spouse cannot use the other's
unused 12,000.

Worked example, joint return: one spouse 67 with a 30,000 private pension, the other 62 with a 10,000 IRA
distribution. Line 5(a) is 12,000, Line 5(b) is empty, and code 06E is 12,000.

## Other decisions

- **`form`**: both readers wrote `subtraction` for the uncapped pensions and the U.S. obligation interest. Written
  as `exempt_in_full`, which is what an uncapped subtraction of the whole amount is (the compare tool already treats
  them as the same).
- **Line 9D**: both readers recorded the Line 9C figures as an `other` deduction with a condition saying so. Kept;
  no field holds a threshold of this kind. The name on the form is misleading: it uses only the medical deduction,
  not total itemized deductions. Line 9A is entered but not used in the arithmetic.
- **`cap_per` on code 49E**: A left it out. Set to `person` on the same reading as 10E ("Persons receiving disability
  income ... may exclude"). Judgement; no tax effect, because 49E is `not_modelled`.
- **`all_income_scope` and `income_test.applies_when`**: asked for where they fit; neither does. Louisiana has no age
  deduction against all income, and no relief in the record has an income test. The AGI tests in the booklet
  ("$25,000 or less", child care and school readiness) belong to credits outside the record.
- **Conditions moved or dropped**: "month and year retired is entered" and "attach a 1099-R" are filing steps, not
  tests a planner may not know, so they are not in `other_conditions`.

## One-sided entries

- A's `other_conditions` on 02E, 03E and 04E (which system pays): kept in shortened form.
- B's `not_covered` on 01E (unidentified mutual fund amounts): kept; it is printed on page 7.
- A's `la_business_sale_gain`: kept (difference 3).
- Added by me: `not_covered` on 05E, in the booklet's words, so the limit that decides the New York answer is on
  the entry itself.

## Projection

- One `exempt_in_full` relief, `la_government_pension`, draws on the 02E/03E, 05E and 04E record entries and covers
  `public_pension` and `military_pension`, with `needs_input: ["pension_source"]`. Separate reliefs on the same
  income kind would add nothing and could subtract the same income twice.
- `la_retirement_income_exemption_65` is modelled with its record `covers`, `pension_source` needed, cap 12,000 per
  person. The covers exclude Roth conversions (approximation).
- `la_railroad_retirement` is modelled as exempt in full (approximation, because of "received by federal retirees").
- `not_modelled`: code 49E, code 10E, code 01E, Lines 9A to 9D, code 20E.
- Indexing: `not_stated` becomes `indexed: false, assumed: true` for brackets, deductions and relief caps.
- No surtax, no recapture, no derived figures.

## Not recorded

Neither reader recorded these, and I left them out as outside the record's scope: other Schedule E codes (START
contributions, school expense deductions, adoption, volunteer exclusions and similar), the Louisiana Earned Income
Credit (Line 16, 5 percent of the federal credit), child care and school readiness credits, and the credit for
taxes paid to other states (Schedule C Line 1). The projection lists them in one `overstates_tax` approximation.

## Unsure

- **New York and other-state pensions in 06E:** this rests on the word "any" and the worksheet's Lines 4b and 5b, not
  on a sentence naming them. R.S. 47:44.1 and the code section behind 05E were not in the sources.
- **Joint return with one spouse 65:** settled from the worksheet as asked, but read alone the paragraph could deny
  that return any exemption. The projection carries this as an `understates_tax` approximation, at most 360 a year.
- **Railroad Retirement:** "received by federal retirees" is unclear. The booklet's own 04E text does not name
  railroad benefits, so the only source is the FAQ page.
- **Roth conversions:** left in `covers_unclear`, though a taxable conversion reported on Line 4b would seem to fit
  the worksheet.
- **The FAQ page is undated,** but its 12,000 figure matches the 2025 booklet.
- **Age test date:** not printed. The projection applies age in the tax year.

## 2026-11-08: marker ids and indexing covers

- Marker ids given: first from_record id (warning code unchanged): `la_permanent_total_disability_income`, `la_military_pay_exclusion`, `la_us_obligation_interest`, `la_excess_federal_itemized`, `la_business_sale_gain`.
- Indexing covers: `brackets` -> `brackets`; `deductions` -> `deductions`; `relief_caps` -> `reliefs.cap`.
- Every `assumed` answer was checked again against the archived sources (searched for indexed, inflation, cost-of-living, adjusted annually, each year, CPI, fixed): none says, so all stay `assumed: true`. The only inflation sentence (CPI-U, booklet PDF page 1) is about the child care director and staff credits, which are not in the projection.
- Warning codes unchanged (every id is the marker's first from_record id).
