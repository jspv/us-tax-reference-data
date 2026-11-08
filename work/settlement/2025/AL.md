# Settlement: Alabama, tax year 2025 (round r5)

Settled 2026-11-07 from `work/extract/2025/AL.r5.A.json` and `AL.r5.B.json`.
Sources: `sources/archive/2025/AL/25f40bk` (the 2025 Form 40 Instruction Booklet, cited "booklet"), `25f40blk` (Form 40 itself, cited "Form 40"), and the agency page `income-exempt-from-alabama-income-taxation`. Page numbers are PDF pages.

`uv run python -m tools.compare` reported **134 structured differences** (62 wording). 131 were decided by reading the booklet. 3 were one-sided indexing entries, dropped under extraction-brief rule 8.

The two readers agreed on everything that drives the tax. They agreed on the rates and bracket starts, the standard deduction and exemption amounts, Social Security, and which pensions are exempt. Almost all of the 134 come from two places: how a stepped band's `over` is written (84), and which table rows were picked as derivation evidence (35).

## Structured differences

| # | Field(s) | Count | A | B | Settled | Page |
|---|---|---|---|---|---|---|
| 1 | `standard_deduction.phase_out.threshold` (4 statuses) and `steps[].over` (80 steps) | 84 | 26,000 / 13,000, and each step at the bottom of its band (26,000, 26,500 ...) | 25,999 / 12,999, and each step at the top of the band below (25,999, 26,499 ...) | **B**. The chart prints whole-dollar bands ("$0 - $25,999", "$26,000 - $26,499"). The schema keeps a step's amount for income *over* `over`, so "over 25,999" is the band that starts at 26,000. A's 26,000 would leave an AGI of exactly 26,000 at the full amount. This matches the CT settlement (upper end of the band below). The amounts were identical in both readings, and I checked all 84 against the chart. | booklet p.9 Standard Deduction chart; p.7 "Rounding Off to Whole Dollars" |
| 2 | `dependent_exemption.phase_out.threshold` | 1 | 50,000 | 0 | **A**. The amount first falls for AGI over 50,000. Both readers had the same steps. | booklet p.10 chart: "0 - 50,000 1,000 / 50,001 - 100,000 500 / Over 100,000 300" |
| 3 | `brackets.derivation.table_rows` | 35 | 14 rows | 8 rows | **10 rows** across every band of both columns: single 450→9, 1,750→60, 3,050→113, 36,050→1,763, 99,950→4,958; joint 950→19, 2,050→62, 6,050→223, 36,050→1,723, 99,950→4,918. Every row either reader recorded is printed and is reproduced by the agreed schedule, so picking rows decides nothing about the schedule. | booklet pp.25, 27, 30 |
| 4 | IRC 414(j) defined benefit entry: `covers`, `covers_unclear`, `form`, `who.basis` (compare keys it by covers, so the fields show twice) | 8 | covers `private_pension`; unclear `public_pension_other_state` | covers `employer_plan_distribution`; unclear `private_pension`, `public_pension_other_state` | covers **`private_pension`, `public_pension_other_state`**. `employer_plan_distribution` is not covered. Plan qualification goes in `who.other_conditions`. See the pension section below. | booklet p.7 and p.14 |
| 5 | Peace officer retirement as its own entry | 3 | separate fire fighter and peace officer entries | one combined entry | **A**, two entries. They are separate lines with different conditions ("from any Alabama firefighting agency"; "from any Alabama police retirement system"), so brief rule 3 asks for one entry each. | booklet p.7 |
| 6 | `indexing` entries for `standard_deduction`, `personal_exemption`, `dependent_exemption` | 3 | none (brackets, all_other) | each `not_stated` | **Dropped.** Rule 8 asks for entries only for figures the booklet speaks about. The booklet says nothing on indexing, so `all_other: not_stated` covers them. | not found in the booklet |

Total: 84 + 1 + 35 + 8 + 3 = 131 decided from the booklet; 3 dropped under rule 8.

### Not flagged by the compare, but settled

- **`brackets.married_separate` and `head_of_household` removed.** Both readers gave them the single schedule. The record schema says to give these statuses "only when the booklet prints its own schedule for them". The table prints one shared column, "Single ✱ Married filing separately ✱ Head of family" (p.25 header). The p.30 worksheet groups them the same way. Left out, so they default to single.
- **Over-100,000 worksheet and the formula field (as the dispatch asked me to log).** The p.30 worksheet is printed as "Enter taxable income / Less – 100,000.00 / Multiply line 3 by .05 / Plus + 4,958.00" (Single, MFS, HoF), and "+ 4,918.00" for Married filing jointly.
  - **Why it doesn't fit the schema.** That is "(income − 100,000) × .05 + constant". The schema's `derivation.formula` takes "rate × income minus constant".
  - **The equivalent form.** It is 0.05 × income − (5,000 − constant): 0.05 × income − 42 for single and 0.05 × income − 82 for joint. Neither 42 nor 82 is printed.
  - **It also disagrees with the brackets by 2 dollars.** The derived brackets give 0.05 × income − 40 and − 80, which is 4,960 and 4,920 at exactly 100,000. The worksheet's constants are the printed tax of the last table row (99,900–100,000, taxed at its midpoint 99,950). So above 100,000 the brackets give 2 dollars more tax than the worksheet. The validator's formula check uses a 1-dollar tolerance, so a formula object would fail by 2 dollars even if the form fitted.
  - **What I recorded.** No `formula` object; `method` is `tax_table`. The worksheet is recorded in `brackets.cite` and in notes. The 2-dollar gap is a projection approximation.
- **Brackets checked against the whole table.** I parsed every printed row with a script in my private folder: 1,006 rows, from 0–50 to 99,900–100,000, both columns. The tax at each row's midpoint, rounded to the dollar, matches all 2,012 printed cells. The only exceptions are the 0–50 and 50–100 rows, where 0.50 is printed as 0 and 1.50 as 1 (a half rounded down, within the validator's 1-dollar tolerance).
- **The misprinted chart row.** Both readers noted a misprint in the Married Filing Joint column, but at the wrong position and partly misdescribed. It is the *third* row (A said "second"), printed "$25,500 – $26,999". B's note said the PDF text layer prints "$26,500"; it does not. Both converted texts (docling and pypdf) print $25,500. The neighbouring rows and the other columns show it is 26,500–26,999. The settled steps follow that, as both readers had.
- **Personal exemption cite.** I moved it to Form 40 page 1. That is the only place printing all four amounts: Head of Family 3,000 is printed only beside box 4. The booklet p.6 gives boxes 1 to 3.
- **Own and federal public pension entry.** I dropped A's `who.other_conditions` (a list of the named systems) and moved the list into notes. The list is the payer, which `covers` already says, not a test the household might fail. It also tripped `tools/report_pensions.py`'s narrow-case filter on the word "Teachers'", which made the report show Alabama and federal pensions as "taxed".

## One-sided entries

- **Kept (A only):** the separate peace officer entry (row 5).
- **Dropped (B only):** the three per-deduction indexing entries (row 6).
- **Notes merged from both.**
  - A had the beneficiary rule (p.15).
  - B had the rollover regulation, the joint-federal / separate-Alabama split of the federal tax deduction, and the web page check.
  - Notes that misdescribed the misprint were corrected.

## The five facts, each with its quote

1. **Another state's government pension, and a New York State pension.**
   - **Result:** `covers`, as `public_pension_other_state`, in the IRC 414(j) entry, on condition that the paying plan qualifies.
   - **The governing line.** No line names New York or any other state's system. The line that governs is p.7, "Examples of Income You DO NOT Report": "Payments from a 'Defined Benefit Retirement Plan' in accordance with IRC 414(j). Contact your retirement plan administrator to determine if your plan qualifies." p.14 repeats it: "Any 'defined benefit' retirement plan in accordance with IRC 414(j)".
   - **Why other states are covered.** The line names a kind of plan, not a payer. Unlike the fire fighter and peace officer lines beside it, it carries no "Alabama" limit.
   - **If the plan does not qualify.** The pension is taxed: "Pensions and annuities other than those listed in 'Examples of Income You DO NOT Report'" must be reported (p.7).
   - **No reciprocity.** No paying-state rule is printed, so there is no `paying_states`.
2. **Own and federal government pensions: exempt in full, no cap or age test.**
   - p.7 lists "United States Retirement System benefits", "State of Alabama Teachers' / Employees' / Judicial Retirement System benefits", "Military retirement pay", "Tennessee Valley Authority Pension System benefits" and "United States Government Retirement Fund benefits".
   - p.14: "Amounts you received from the following retirement systems are not taxable and should not be reported." It adds "Civil Service Retirement System" and "U.S. Foreign Service Retirement and Disability Fund Annuities".
   - Alabama fire fighter and peace officer retirement compensation is exempt (p.7).
   - The web page repeats the list.
3. **Private pensions, IRA and employer-plan distributions, Roth conversions.**
   - **Private pensions.** Exempt in full when paid by a 414(j) defined benefit plan (quote above). Otherwise "unless specifically excluded by law, your pension payments are fully taxable" (p.14).
   - **IRA, SEP, Keogh, 401(k)(2), 403(b), profit-sharing.** Taxable on Schedule RS: "use these lines to report distributions from SEP, Keogh, 401(k)(2), 403(b), and profit sharing plans" (p.14).
   - **Roth conversions.** Taxable: "the taxable portion of the distribution ... is the amount that you would have to include in income if you had taken a distribution and not converted" (p.14).
4. **Social Security: exempt.**
   - p.7 "Examples of Income You DO NOT Report": "Federal Social Security benefits".
   - Second line: p.14 "not taxable and should not be reported: ... Retirement Systems created by the Federal Social Security Acts".
   - Third: the web page.
   - Form 40 has no subtraction line; the benefits are simply never reported.
5. **Brackets, standard deduction, exemptions.**
   - **Brackets (derived).**

     | Statuses | 2% from | 4% from | 5% from |
     |---|---|---|---|
     | Single, MFS, HoF | 0 | 500 | 3,000 |
     | Joint | 0 | 1,000 | 6,000 |

   - **Standard deduction (p.9 chart).** It steps down with Alabama AGI. The joint column falls by 175 every 500 dollars.

     | Status | Full amount | Full up to AGI | Floor | Floor from AGI |
     |---|---|---|---|---|
     | Single | 3,000 | 25,999 | 2,500 | 35,500 |
     | Joint | 8,500 | 25,999 | 5,000 | 35,500 |
     | Separate | 4,250 | 12,999 | 2,500 | 17,750 |
     | Head of family | 5,200 | 25,999 | 2,500 | 35,500 |

   - **Personal exemption, per return.** Single 1,500, joint 3,000, separate 1,500, head of family 3,000 (Form 40 boxes 1 to 4; booklet p.6).
   - **Dependent exemption.** 1,000 / 500 / 300 by AGI (p.10).
   - **Not found in the booklet:**
     - no age-65 or blindness amount
     - no indexing
     - no surtax and no recapture
   - **The federal income tax deduction (line 12, worksheet p.31).** It is a real base deduction with no fixed amount, so it is recorded in notes only.

## Projection choices (`AL.projection.json`)

- **Base.**
  - `starts_from` is federal_agi, standing in for the record's state_own (approximation, either direction).
  - The standard deduction carries its stepped `phase_out` on `state_agi`.
  - The personal exemption is per return by status.
  - The dependent exemption is `not_modelled` (warn `has_dependents`).
- **Federal income tax deduction.** `not_modelled`, warn `always`, with `from_record` empty because no record id holds it. Its approximation overstates tax by up to 5% of federal tax: 1,000 a year on 20,000 of federal tax. It is the largest gap for Alabama.
- **Reliefs.** All exempt in full, per person:
  - Public pensions: the named systems plus Alabama fire and police, in one entry.
  - Military.
  - Railroad.
  - Defined benefit (414(j)), covering `private_pension` and `public_pension_other_state`.
- **No `needs_input`.** Every pension kind comes out exempt, so the projection never needs to know the source.
- **No Social Security relief.** Social Security is handled by `treatment: exempt`, as in the NC, VA and SC projections.
- **Approximations.**
  - The 414(j) qualification is assumed for every private and other-state pension. This understates tax by 5% of any pension whose plan does not qualify.
  - The derived brackets: under 1 dollar of rounding below 100,000, and the worksheet's 2 dollars above it (overstates).
  - Itemized deductions are not modelled.
  - Alabama's larger IRA and plan basis (contributions before 1982 and 1985).
  - U.S. obligation interest is taxed.
  - Own-state bonds can't be told from other states' bonds.
- **Not modelled, warn `never`.** U.S. obligation interest, and the bullion gain exemption.

## Validator

```
data/states/2025/AL.record.json: ok
data/states/2025/AL.projection.json: ok
```

## Unsure

- **Other states' pensions in `covers`.** Both readers left `public_pension_other_state` in `covers_unclear`. I moved it into `covers` because the 414(j) line names no payer and, unlike the lines next to it, has no Alabama limit. This is the same call as the MD settlement (the booklet does not limit public plans to the state).
  - **What the booklet does not say.** It never says whether a given state's plan qualifies under 414(j); it leaves that to the plan administrator. A reviewer who reads "Pensions and annuities other than those listed" as excluding unnamed government systems would put it back in `covers_unclear`.
  - **The same doubt applies to private pensions.** I put `private_pension` in `covers` on the same footing.
- **`employer_plan_distribution` left out of the 414(j) entry.** A defined benefit plan's lump sum is not addressed. p.14 says a lump sum "from an Employee Benefit Plan" is included in income in the year received, which points to taxed, but the booklet does not tie that sentence to 414(j) plans.
- **Alabama city and county general-employee plans.** These are neither fire nor police and are not named. They are exempt only if they qualify under 414(j). The record's `public_pension` entry names only the listed systems. The projection exempts every `public_pension`, which is covered by the 414(j) approximation.
- **`tools/report_pensions.py`.** Its NY and NJ rows say "exempt in full" without the plan-qualification condition, because `describe()` does not print `other_conditions`. Its "private pension / 401(k)" row reads exempt, but 401(k) distributions are taxed; the column lumps kinds together. These are report limits, not record content.

## 2026-11-08: marker ids and indexing covers

- Marker ids given: first from_record id (warning code unchanged): `dependent_exemption`, `al_us_obligation_interest_exempt`, `al_precious_metal_bullion_gain`; descriptive: `al_federal_income_tax_deduction` (the marker had no from_record id).
- Indexing covers: `brackets` -> `brackets`; `deductions` -> `deductions`.
- Every `assumed` answer was checked again against the archived sources (searched for indexed, inflation, cost-of-living, adjusted annually, each year, CPI, fixed): none says, so all stay `assumed: true`.
- `tools.checks --fix-warnings` updated the cases' accepted_warnings where a code changed; nothing else in the cases changed.
