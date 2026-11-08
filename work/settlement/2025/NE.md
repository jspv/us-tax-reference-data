# Nebraska 2025 settlement log

Readings: `work/extract/2025/NE.r6.A.json`, `NE.r6.B.json`. Settled 2026-11-07.
Sources: `sources/archive/2025/NE/`: the booklet `f_Individual_Income_Tax_Booklet`, Form 1040N `f_1040N`, and
Schedules I to III `f_1040N_Schs`. Page numbers are PDF pages of the booklet unless a form is named.
Outputs: `data/states/2025/NE.record.json`, `data/states/2025/NE.projection.json`.

`tools.compare` reported **199 structured differences** and 102 wording differences. All 199 were read against
the sources and settled. **173 were decided by what the booklet prints; 26 were not**: 18 are `who.basis` on
reliefs with no age test or cap, settled by extraction brief rule 5; 4 are B's premium relief, dropped because it
covers no kind of income; 4 are the start of the 5.20% band, which the table can't pin down.

## Comparison

| Lines | Field | A | B | Source | Settled | From the booklet? |
|---|---|---|---|---|---|---|
| 149 | `brackets.derivation.table_rows`, compared by position | 20 rows | 52 rows | Pages 46-49. Every row of both readers checked against the parsed table: all printed | Replaced by all 777 rows of all four columns, plus the four worksheet amounts: 3,112 rows | Yes |
| 1 | `brackets.married_joint[1].start` | 8,059 | 8,060 | Pages 46-49 | 8,040, neither reader | Yes |
| 1 | `brackets.married_joint[2].start` | 48,223 | 48,240 | Pages 46-49 | 48,250, neither reader | Yes |
| 1 | `brackets.head_of_household[1].start` | 7,508 | 7,540 | Pages 46-49 | 7,510, neither reader | Yes |
| 1 | `brackets.head_of_household[2].start` | 38,593 | 38,590 | Pages 46-49 | 38,590, B | Yes |
| 1 | `brackets.married_joint[3].start` | 77,550 | 77,760 | Table passes both; page 49 prints 77,760 | 77,760, B, the figure printed most directly. **Not pinned** | No |
| 1 | `brackets.head_of_household[3].start` | 57,520 | 57,630 | Table passes 57,535 to 57,639: A is out, B is in | 57,630, B. **Not pinned** | No |
| 2 | `brackets.single[3].start`, `brackets.married_separate[3].start` | 38,890 | 38,870 | Table passes both | 38,870, B, so all the 5.20% starts come from one reading; 0.04 a year between them. **Not pinned** | No |
| 17 | `base.deductions`: age 65 (7), blind (7), dependent (3) | in notes, or none | entries | Page 13 chart; page 12 lines 2a, 4c; page 14 line 18 | Age and blind kept as B, marked derived. Dependent moved to `reliefs`, see below | Yes |
| 3 | Credit for the elderly or disabled | none | relief, `each_person` | Page 15 line 20 | Kept, with `who.basis: return`: the line takes the return's federal credit | Yes |
| 18 | `who.basis` on military, CSRS and railroad (3 pairs of 3 lines) | `each_person` | `return` | Pages 26, 27, 24. No age test or cap, so the tax is the same either way | `each_person`: each retiree qualifies on their own service. Rule 5; most uncapped military entries in the settled states do the same | No: rule 5 |
| 4 | Retired officers' health premiums | none | relief, `covers: other_income` | Page 27 line 36 | Dropped as a relief, kept in `notes`: it subtracts premiums paid, not a kind of income | No: format |

Total 199: 173 from the booklet, 26 not.

## One-sided entries and changes neither reader made

| Entry | Reader | Kept? | Why |
|---|---|---|---|
| `derivation.method` | both `tax_table` | Changed to `tax_table_and_formula` | Page 49 prints a worksheet above the table. Not a compared difference |
| `derivation.formula` | neither | Left out | See the derivation below |
| Personal exemption in `base.deductions` | both | **Moved to `reliefs`** as a credit: `credit_amount` 171, `credit_basis` tax, `covers` all_income, `each_person`, as California, Delaware, Iowa and Arkansas are recorded | Page 14 line 18: "Residents may claim a $171 credit for each Nebraska personal exemption reported on line 4, Form 1040N." An entry under deductions reads as an amount off income. A consumer that applied 171 as a deduction would give about 9 instead of 171 |
| Dependent exemption | B | Kept, moved to `reliefs` as a credit | Line 4 adds 4a, 4b and 4c, and line 18 multiplies by 171 |
| One credit on a separate return | neither | Added: `cap_rule` in the record; `cap` per status in the projection | Page 12: "If your status is married, filing jointly enter 1 in line 4b for your spouse". See "After the check writer's review" |
| Federal Tax Liability Worksheet | neither | Added, with `not_modelled` and an approximation | Page 17. See "After the check writer's review" |
| Nebraska earned income credit | neither | Added, with `not_modelled` | Page 18 line 44; projection guide. See "After the check writer's review" |
| Nonrefundable | neither | Added to `cap_rule` | Form 1040N page 2, line 34 "Total nonrefundable credits (add lines 18 through 33)", line 35 "if line 34 is more than line 17, enter -0-" |
| `paying_states: ["federal"]` on CSRS | neither | Added, as Indiana does | Without it, `public_pension` would also read as a Nebraska state pension, which line 38 does not take |
| "Contributory plan" on CSRS | B | Dropped | Page 27 prints no such test |
| FERS and "only the portion paid from CSRS" | both, in part | `not_covered`, in the booklet's words | Page 27 |
| Other tax, 29.6% | both, in notes | Notes; projection marker | No field. Page 14 line 16; Form 1040N line 16 |
| National Guard | both | Kept; `not_modelled` | Page 28 line 41 |
| Bullion gain | both | Kept; `not_modelled` | `applies_to: other` has no projection value |
| Special capital gains deduction | both, in notes | Notes only | Terms are in Form 4797N, which is not in the sources |

`form` on the Social Security, military, CSRS, railroad and National Guard entries is written `exempt_in_full`. The
readers wrote `subtraction`; `tools.compare` treats an uncapped subtraction as the same thing, and it is the form
most uncapped entries in the settled states use.

## The five required questions

### 1. A government pension paid by another state, and New York State in particular

**Not found in the booklet.** Not in `covers`, not in `not_covered`, no `paying_states`. "New York" does not
appear in the booklet or forms. Schedule I Part B and its instructions (pages 24-28) print no line for it. The
only line for a non-military government pension is limited to federal employment:

> "The decreasing adjustment is limited to annuities received under the Civil Service Retirement System (CSRS)
> that were earned from employment with the federal government to the extent included in the federal AGI."
> (page 27, line 38)

**Rule:** a Nebraska resident with a New York State pension gets no subtraction found in the booklet; the pension
stays in federal AGI, where Form 1040N line 5 starts, and is taxed at the ordinary rates. This is what the booklet
fails to print, not a sentence saying such pensions are taxed. Schedule II gives a credit for income tax paid to
another state (pages 14, 29), which exempts nothing.

### 2. Its own and federal government pensions

- **Nebraska state and local:** not found in the booklet. Same reasoning as question 1.
- **Federal CSRS:** subtracted in full. Quote above; Schedule I form line 38, "Civil Service Retirement annuities
  received for being employed by federal gov't".
- **Federal FERS:** expressly out. "Note: The exclusion does not apply to annuities received under the Federal
  Employees Retirement System (FERS). Do not include income from FERS annuities." (page 27). "Only the portion
  paid from CSRS qualifies for this deduction."
- **Military:** "All military retirees are allowed to exclude 100% of the military retirement benefits from the
  income subject to Nebraska income tax to the extent included in federal AGI." (page 26, line 32); Schedule I
  form line 32.

The projection puts CSRS in `not_modelled` with `warn_when: has_pension`, not in `reliefs`. The guide's rule to
model pension kinds covers public, private and military. Here the test is CSRS against FERS inside federal
pensions, and modelling it would exempt every FERS pension in full. Oklahoma and Idaho treat CSRS tests the same
way. The cost is a tax overstated for a true CSRS annuitant, with a warning.

### 3. Private pensions, IRA and employer-plan distributions, Roth conversions

No subtraction found. Page 13, line 5, lists what federal AGI holds: "retirement income (such as 401K
distributions, pensions, etc.)". No Schedule I line takes it out. "Roth" and "required minimum" appear nowhere in
the three documents; "rollover" is about 529 plans; "Conversion Chart" is about another state's return lines. No
relief exists, so no `covers_unclear`.

Second check: the Schedule I form's line list (lines 14 to 43) against the instructions. Nothing retirement-related
is on the form alone.

### 4. Social Security

Exempt.

> "Enter the amount of Social Security income included in federal AGI. The entire social security benefit amount
> included in the federal AGI can be excluded and no longer has a federal AGI threshold." (page 26, line 31)

Second document: Schedule I form line 31, "Social Security included in Federal AGI". The amount cannot exceed
Form 1040 line 6b. Railroad benefits come out on their own line (page 24, line 18), with a ratio for a filer who
has both forms.

### 5. Brackets, standard deduction, exemptions

Brackets: below.

Standard deduction: page 13 chart, 0 boxes: single 8,600; joint 17,200; surviving spouse 17,200; separate 8,600;
head of household 12,600. Form 1040N line 6 says to take it from the instructions.

Age and blind: **the chart prints totals only.** 2,000 (single, head of household) and 1,650 (joint, separate,
surviving spouse) are differences, for example 18,850 - 17,200 and 10,600 - 8,600, and each step within a status
is equal. They are marked "Derived, not printed" in the `condition` and in `notes`. The validator cannot check
them: it finds "1650" only inside a school district code (0165005), and 2,000 elsewhere in the booklet, not in the chart. The
projection needs a figure in the record, so the record holds them, as Kansas does.

Age test: "taxpayers born before January 2, 1961" (page 12, line 2a).

Personal exemption: a credit of 171; see above. Second check: Form 1040N line 18 "($171 times the number on line 4)".

## Bracket derivation

The booklet prints no rate schedule. It prints:

- The Nebraska Tax Table, pages 46-49: 777 rows of 100 dollars, 60 to 77,760, four columns. The table's first row is
  60 to 160, checked on the page image.
- Page 49: "The tax table shown above calculates tax to the midpoint of the bracket. The amounts shown below
  represent tax calculated on $77,760, the endpoint of the bracket." Then (taxable income - $77,760) x .0520 plus
  $3,566 single, $3,088 joint or surviving spouse, $3,566 separate, $3,276 head of household.
- Page 2: "For the 2025 taxable year, the highest rate for Nebraska taxable income is reduced to 5.20%."

**Only 5.20% is printed as a rate.** 2.46%, 3.51%, 5.01% and every start above 0 are fitted.

The booklet names a schedule it doesn't print: "Electronic filers must use the Nebraska Tax Calculation Schedule"
(page 14). That schedule is not in the archive and would settle every open figure here.

**Row parsing.** The pypdf text splits some digits ("1 9660", "$61 3"), so a row was accepted only if its first
number plus 100 equals its second. All 777 parsed with no gaps, and all 777 match the docling text in all four
columns. Separate equals single on every row.

**Test used.** The validator allows 1 dollar. That is loose for a table that rounds, so the fit used a stricter one:
the schedule at the midpoint, rounded half up, must equal the printed figure, exactly, in fractions.

| Status | Rows failing | Largest gap | Start 1 | Start 2 | Start 3 (5.20%) | Range for start 3 |
|---|---|---|---|---|---|---|
| Single, separate | 0 | 0.496 | 4,030 | 24,120 | 38,870 | 38,793 to 38,897 |
| Joint | 0 | 0.499 | 8,040 | 48,250 | 77,760 | 77,501 to 77,760 |
| Head of household | 0 | 0.496 | 7,510 | 38,590 | 57,630 | 57,535 to 57,639 |

- **Pinned:** starts 1 and 2. With the four rates fixed, exactly one whole-dollar value passes in each case.
- **Not pinned:** start 3 in every status, marked in `notes` and in the projection's `approximations`. The rate step is
  only 0.19 of a percentage point, so a range passes. For joint the rows alone would allow values up to at least
  78,399, and the worksheet's "over $77,760" caps it. The choice inside a range moves tax by at most 0.20 a year
  (0.49 for joint).
- **Rates:** scanned from 2.00% to 5.99% in steps of 0.01 point on rows clear of the band edges. 2.46 and 3.51 are the
  only fits in every column. 5.01 is the only fit in all three columns: 5.00 touches at one exact point for single
  and head of household and fails joint. Joint has no full 5.20% band.

**How the readers fared under the strict test.** A's joint schedule fails 141 rows and its head of household 51. B's
joint fails 102 and its head of household 230. Both pass the validator's 1 dollar test, which is why they looked
settled. Single passes for both.

**The worksheet.** `brackets.derivation.formula` is left out. It holds one "rate x income minus constant" checked
against single and joint, Nebraska prints a constant per status, and as `minus` figures they would not be printed
(per-status formula constants, a format item not yet added; Nebraska is one more case of the item New Jersey raised). The
worksheet amounts are table rows at income 77,760 instead, so the validator reaches them. Above 77,760 the schedule
differs from the worksheet by a constant: -0.448 single and separate, -0.394 joint, +0.318 head of household,
checked at 100,000, 155,520 and 1,000,000.

The record is about 252 KB, larger than any other state, because `table_rows` holds every printed row. Each row is
on one line.

## Projection

`derived_figures` holds one figure: 342 = 171 + 171, the joint limit on the personal credit. Every other figure is in
the record. Modelled: brackets, standard deduction, age 65 addition (`min_age: 65`), the 171 credit per person up to
its limit per status, military and railroad. Social Security is `exempt`.

| Rule | Where | Why |
|---|---|---|
| CSRS | `not_modelled`, `has_pension` | Question 2 |
| Federal Tax Liability Worksheet | `not_modelled`, `always`, plus an `overstates_tax` approximation | No federal tax input, and no trigger for a low federal tax |
| Elderly or disabled credit | `not_modelled`, `always` | The booklet prints no age test to narrow the warning, and I would not take one from outside it |
| Other tax, 29.6% | `not_modelled`, `always`, no record id | No field. `has_pension` would miss an IRA-only household |
| Dependent credit | `not_modelled`, `has_dependents` | Guide |
| Earned income credit | `not_modelled`, `never` | Guide: "low-income and renter credits". `never` as other states' earned income credits |
| Blind addition; dependent-filer deduction; National Guard; bullion; other lines | `not_modelled`, `never` | A projection doesn't know these |
| Fitted brackets; federal tax limit; itemizing; Treasury interest; own-state bonds; age test edge | `approximations` | |

Indexing is `false, assumed` for brackets, deductions and the credit: the words inflation, indexed, adjusted
annually and cost of living are in none of the three documents.

## After the check writer's review (2026-11-07)

The check writer found two gaps. Neither changes the 199 compared lines above: neither reader recorded these.

**1. Federal Tax Liability Worksheet (page 17; Form 1040N line 35).** Missed in the first settlement. Now
`ne_federal_tax_liability_limit` in the record.

> "Do not complete the worksheet below if the result of line 12 minus line 13 is $5,000 or more. Otherwise, if your
> federal tax liability is -0- or is less than your Nebraska tax, complete the Federal Tax Liability Worksheet below.
> On line 35, enter the smaller of the amounts from line 2 or line 3 of the worksheet."

Worksheet line 3 is "Federal tax before credits": Form 1040 line 16 plus Schedule 2 lines 2 and 8. The form's line 35
says the same in short: "If the result is greater than your federal tax liability, see instructions". The 5,000 test is
in `income_test` with `applies_when: at_or_over`, on a measure of `other`, and the form is `credit`, the nearest value
for a limit on the tax. Net adjustments under 5,000 include every negative figure, so the Social Security and military
subtractions leave the worksheet open.

The projection marks it `not_modelled` with `warn_when: always` and an `overstates_tax` approximation. Worked size: a
couple with 60,000 of long-term gains and federal tax 0. Line 14 is 60,000 - 17,200 = 42,800. Tax is 8,040 x 2.46% +
34,760 x 3.51% = 1,417.86, less 342 of credits = 1,075.86 in the projection; the form gives 0.

**2. One personal credit on a separate return.** The record had `each_person`, so a separate return listing both
spouses (checks brief rule 5d) gave 342 where the form gives 171. `credit_amount` has no per-status form, so the
projection keeps `each_person` and adds `cap` per status with `cap_per: return`: 171 for every status, 342 for joint.
342 is in `derived_figures` as 171 + 171, not in the record, because the booklet doesn't print it. Oregon's retirement
credit has the same shape. The record says it in `cap_rule`.

Two things to watch. The schema's description says an `all_income` relief has "one cap per qualifying person" when
`who.basis` is `each_person`, and this entry relies on `cap_per: return` taking priority over that sentence; the
evaluator must read it so. And page 13's chart gives the separate-return spouse boxes "only if the primary taxpayer can
claim a personal exemption for his or her spouse", which implies a spouse exemption line 4b does not provide. Line 4b is
the direct instruction for the credit, so it decides here. The chart's sentence stays as the age addition's condition.

**3. Earned income credit.** The projection guide puts low-income credits in `not_modelled`, so it calls for a marker.
Now `ne_earned_income_credit` in the record, `warn_when: never` in the projection. Page 18: "allowed a state credit equal
to 10% of the federal credit". Refundable: Form 1040N line 53, "Total payments and refundable credits (add lines 36
through 52)". `credit_rate` 0.10 is a share of the federal credit, not of the income in `covers`, as `cap_rule` says.

`checks/2025/NE` was not edited. `tools.checks` now reports `accepted_warnings` out of date on the cases, because of the
new `always` marker; `--fix-warnings` is the check writer's step.

## Unsure

1. The start of the 5.20% band is a place inside a range in every status, and the choice among 38,870 and 38,890
   rests on nothing printed. Archiving the Nebraska Tax Calculation Schedule would replace all of the fit.
2. The personal exemption moved out of `base.deductions` against both readers. Rule 7 says exemptions are "always
   recorded"; they are, as reliefs, following the states that print a credit.
3. CSRS in `not_modelled` departs from the guide's "model the relief" for pension kinds, for the reason in question
   2. If `pension_source` gains a CSRS or FERS value, it moves to `reliefs`.
4. Three `always` warnings are noisy for a Nebraska run. A trigger for early distributions would narrow the 29.6% one
   (issue #3, "Narrower warning triggers"), and a federal tax input would remove the worksheet one.
5. Questions 1 to 3 are the booklet's silence. The state's statute or an information guide may say more; neither is
   in the sources.

- Main session, 2026-11-07 (format for the first frozen schema): the other-tax marker (29.6% of the federal early-distribution and lump-sum tax) warns on an IRA or plan payout by a person under 60 instead of every run.

## 2026-11-08: marker ids and indexing covers

- Marker ids: all 11 markers have an `id`. Descriptive ids (no from_record id of their own): `ne_other_tax_lump_sum_early_distribution`, `ne_record_notes_lines`; the rest take their first from_record id, so their warning codes are unchanged. `tools.checks --fix-warnings` rewrote the cases' accepted_warnings (the old shared code state_rule_not_modelled:unnamed becomes the new ids); nothing else in the cases changed.
- Indexing covers: `brackets` covers brackets; `deductions` covers deductions; `ne_personal_exemption_credit` covers reliefs:ne_personal_exemption_credit (its cap and credit amount). No split needed.
- Assumed resolved: `brackets` is now indexed true, no longer assumed. Booklet (8-307-2025) PDF page 5, Employee Nebraska Wage Exclusion: 'For tax years beginning on or after January 1, 2026, the annual wage thresholds will be adjusted each tax year by the same percentage used to adjust the individual income tax brackets.' The record gains `indexing` brackets yes with that cite, and its Indexing note says so; the projection's record sha256 is updated. The sentence is indirect (it is about the wage exclusion), but it says the brackets are adjusted each year. The other NE entries stay assumed: nothing else says.

## 2026-11-08: indexing settled from statutes

Statute research (work/indexing/findings*.json) settled every projection indexing entry that was `assumed: true`:

- `deductions` (deductions): indexed, Neb. Rev. Stat. 77-2716.01(3)(b)
- `ne_personal_exemption_credit` (reliefs:ne_personal_exemption_credit): indexed, Neb. Rev. Stat. 77-2716.01(1)(b)
- Record `indexing`: added ne_standard_deduction -> yes; added ne_age_65_additional -> yes; added ne_personal_exemption_credit -> yes.
