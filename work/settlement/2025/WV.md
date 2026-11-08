# West Virginia 2025: settlement log

Settled 2026-11-07 from `work/extract/2025/WV.r6.A.json` and `WV.r6.B.json`. Sources:
`sources/archive/2025/WV/`: the IT-140 booklet (PDF page numbers below), the separate Schedule M, and
the Tax Division's Social Security Modification page.

`tools.compare` reported **63 structured differences** (119 wording differences). All 63 are settled.
**41 were decided by the booklet's text.** In the other 22 (head of household brackets, 10; bracket
`base`, 12) the readers agreed on what the booklet prints, and the format rules decided how to write it.

## Structured differences

| # | Field | Lines | A | B | Settled | Source |
|---|---|---|---|---|---|---|
| 1 | Low-income earned income exclusion `amount` | 5 | single, married_joint, head_of_household, qualifying_surviving_spouse 10,000; married_separate 5,000 | `all` 10,000, married_separate 5,000 | Each status written out (same figures) | PDF p.31 worksheet line C: "Enter $5,000 if your filing status is married filing separately; otherwise enter $10,000" |
| 2 | Same deduction, `phase_out` | 7 | federal_agi, removes, 10,000 / 5,000 | none (limit in `condition`) | A: `phase_out` removes at federal AGI over 10,000 (5,000 MFS) | PDF p.31: "If Line A is greater than $10,000 ($5,000 if married filing separate returns), you are not eligible for the exclusion" |
| 3 | Surviving spouse exemption | 3 | Its own deduction, 2,000 per exemption claimed | Inside the personal exemption's `condition` | A: its own entry | PDF p.3 box (d); PDF p.26 "(d) SURVIVING SPOUSE ... an additional exemption for the two (2) taxable years following the year in which the spouse died"; PDF p.23 |
| 4 | `brackets.head_of_household` | 10 | left out | Schedule I repeated | Left out | PDF p.37 "RATE SCHEDULE I Use this schedule if you checked 1 (Single), 2 (Head of household), 3 (Married filing joint), or 5 (Widow[er] ...)". The schema gives a status only "when the booklet prints its own schedule" (format) |
| 5 | `brackets[].base` | 12 | printed tax at each band start | none | None | PDF p.37 prints "$222.00 plus 2.96% of excess over $10,000" etc. Each amount is exactly the sum of the lower bands, and `base` is for a table that steps up (Ohio) (format) |
| 6 | Line 29 U.S. and WV obligations relief | 3 | kept | not recorded | Kept, as `exempt_in_full` | PDF p.28 LINE 29; it is also line 47's column (d) |
| 7 | Lines 36 and 37 military pay reliefs | 6 | not recorded (note only) | kept | Kept | PDF p.28 LINE 36, p.29 LINE 37, p.22 "Active Duty Military Pay" and "Active Military Separation" |
| 8 | Surviving spouse deduction (line 48), `who.basis` (shows as two one-sided rows) | 12 | each_person | return | each_person | PDF p.6 form: line 48 has a Column A (You) and Column B (Spouse) entry |
| 9 | Line 33 split | 5 | two entries (33a, 33b), each capped 2,000 | one entry capped 2,000 | B: one entry, one 2,000 a person | PDF p.28: "Combined amounts of 33a and 33b must not exceed $2,000."; PDF p.5 form: "Add lines 33 (a) and (b). If that sum is greater than $2,000, enter $2,000" |

Total: 12 + 3 + 10 + 12 + 3 + 6 + 12 + 5 = 63.

Wording-level settlements worth recording (compare counts them as wording):
- Form of lines 30, 31, 32, 40: A said subtraction, B said subtraction except railroad. Settled `exempt_in_full`
  for all four. PDF p.22: "The State of West Virginia does not impose tax on the retirement income received
  from any West Virginia state or local police, deputy sheriffs' or firemen's retirement system, federal law
  enforcement retirement, or military retirement"; PDF p.29 line 40: "West Virginia does not impose tax on
  this income".
- Line 47 senior and disability entries: `best_of_group` kept and `cannot_combine_with` added both ways
  (B had it; A did not). It is one line with one 8,000 for each person.

## One-sided entries

- **Kept:** line 29 (A), because it is printed and feeds line 47. Lines 36 and 37 (B), because they are printed.
  Surviving spouse exemption (A), because it is printed.
- **Added (neither reader):** the Family Tax Credit (Schedule FTC-1, PDF p.13; tables PDF p.14). It is a
  credit against income tax printed in the booklet, and it was in scope. Recorded as `credit`,
  `credit_basis: tax`, with the income test `other` and the full tables in `as_printed`. The threshold is
  the top of each table (56,850; MFS 28,425), above which no family size has a credit. It is not modelled
  in the projection.
- **Dropped:** none. Property tax credits (both readers left them out) stay out, because they are credits for
  property tax paid.

## The five required facts

1. **Another state's government pension (New York State in particular): not found in the booklet.**
   The word "New York" does not appear in the booklet. No line names another state's pension: line 31
   names "any West Virginia state or local police, deputy sheriffs' or firemen's retirement system",
   line 33(a) "The West Virginia Teachers' Retirement System and/or The West Virginia Public Employees'
   Retirement System", and line 33(b) "Federal Retirement" (PDF p.28). So no relief lists
   `public_pension_other_state`. A New York State pension stays in federal AGI ("The starting point for
   the West Virginia income tax return is your federal adjusted gross income", PDF p.26) and is taxed.
   Only the line 47 age 65 or disability deduction can reach it, because that takes "all income ... not
   reported on lines 35 through 48" (PDF p.29).
2. **Own and federal government pensions.** WV police, deputy sheriffs' and firemen's systems (line 31)
   and federal law enforcement retirement (line 30) are not taxed: "The State of West Virginia does not
   impose tax on the retirement income received from any West Virginia state or local police, deputy
   sheriffs' or firemen's retirement system, federal law enforcement retirement, or military retirement"
   (PDF p.22). WV Teachers', WV PERS and other federal retirement get 2,000 a person between them: "The
   modification for pensions and annuities received from the West Virginia Public Employees' Retirement
   System, the West Virginia Teachers' Retirement System, and Federal Retirement is limited to a maximum
   of $2,000" (PDF p.22), and "Combined amounts of 33a and 33b must not exceed $2,000." (PDF p.28).
   Military retirement (line 32) is not taxed and has no cap.
3. **Private pensions, IRA and employer-plan distributions, Roth conversions:** no subtraction found.
   The PDF p.30 example puts "IRA Distributions 4,000 1,000" in total income and subtracts them nowhere
   but through line 47. The only private-pension line is the PBGC Modification (line 45). The word "Roth"
   does not appear in the booklet.
4. **Social Security: relief.** PDF p.28 line 34: "100 percent (100%) of the amount of social security
   benefits received and included in federal adjusted gross income ... The deduction may be claimed only
   when the federal adjusted gross income of a married couple filing a joint return does not exceed
   $100,000, or $50,000 in the case of a single, head of household, widow(er), or a married individual
   filing a separate return. Additionally, for taxable year 2025, 65% of social security benefits ... when
   the federal adjusted gross income ... exceeds". Checked against the form (PDF p.5: "Multiply 34(c) by
   0.65 if your Federal AGI exceeds $ 50,000 for SINGLE or MARRIED SEPARATE filers $100,000 for MARRIED
   JOINT filers") and PDF p.17. Recorded as `stepped`, keep 1 then 0.65, `applies_when` over ("does not
   exceed"). **2026:** the Tax Division page says "In Tax Year 2026, it will become a 100% decreasing
   modification". This is a note in the record, and in the projection an `overstates_tax` approximation
   noting the scheduled change.
5. **Brackets, standard deduction, exemptions.** Rate Schedule I (single, head of household, married
   joint, widow[er]) runs 2.22% from 0, 2.96% from 10,000, 3.33% from 25,000, 4.44% from 40,000 and
   4.82% from 60,000. Rate Schedule II (married separate) has half the thresholds: 5,000, 12,500, 20,000
   and 30,000 (PDF p.37). As a second check, every one of the 1,702 Tax Table rows (PDF p.38 onward,
   under 100,000) equals Schedule I at the row midpoint, rounded. **No standard deduction:** the phrase
   does not appear, and "the only itemized deductions allowed to be claimed from the federal income tax
   return are gambling losses" (PDF p.21). Exemptions are 2,000 each: "You can deduct $2,000 for every
   exemption claimed" (PDF p.26). That covers you, your spouse on a joint return, each dependent, and the
   surviving spouse box (d). It is 500 if zero exemptions are claimed. No phase-out is printed.

## Line 47 (the readers' flagged point), and how it is represented

The form (PDF p.6) and the instructions (PDF p.29) say: column (c) is "Income not included in lines 35 to
46 (NOT TO EXCEED $ 8000)"; column (d) is "Add lines 29 through 34"; then "Subtract line 47 column (d)
from (c) (If less than zero, enter zero)". Column (c) includes the income that lines 29 to 34 subtract.
In the PDF p.30 example, Mr Doe has 13,000 of income, 7,500 of it on lines 29 and 31. He enters 8,000 in
(c) and 7,500 in (d), and takes 500. So for each person, lines 29 to 34 plus line 47 come to
**max(sum of lines 29 to 34, min(8,000, column c))**. That matches the Tax Division page: "You receive
the higher of the $8,000 modification or the sum of various itemized decreasing modifications".

The format can't say this exactly. `cap_reduced_by` takes off income received, and line 34 takes off only
taxable benefits at 65% or 100%. So in the projection:
- The Social Security subtraction and the age 65 deduction share `best_of_group: wv_line_47`, evaluated
  for each person. The age 65 cap of 8,000 is reduced by military retirement (`cap_reduced_by:
  ["military_pension"]`), which is on line 32 and taken in full outside the group. Line 32 plus the
  group then gives mil + max(SS, 8,000 - mil) = max(mil + SS, 8,000), which is exact for these lines.
- Line 33 stays outside the group. A person under 65 keeps it alongside Social Security, and the 8,000
  can't be reduced by the whole public pension when only 2,000 of it is on line 33. The error is an
  `understates_tax` approximation: a person 65 or older with a line 33 pension whose Social Security and
  military lines add to under 8,000 gets up to the line 33 amount too much. That is at most 2,000 x 4.82%
  = 96 a year a person.

The surviving spouse deduction (line 48) shares the same 8,000 (its `cap_rule`). It is not modelled.

## Other decisions

- **Line numbers in the instructions:** from line 47 on, the instructions keep older numbers, two higher
  than the 2025 form. Box (c) reads "lines 35 through 48" where the form says 35 to 46, the example table
  is numbered 49, and line 48 says "lines 29 through 34 and line 49" and "Line 49 and 50". The record
  uses the form's numbers and says so in `notes` and in line 48's `cap_rule`.
- **Disability:** PDF p.29 says "taxpayers under age 65", PDF p.23 says "regardless of age". No `max_age`
  is set: a person 65 or older qualifies as a senior anyway. Not modelled (disability).
- **Social Security AGI test:** on the return's federal AGI (a joint couple against 100,000). Head of
  household and widow(er) use 50,000 (PDF p.17 and p.28), though the form's box names only single,
  married separate and married joint.
- **Projection base:** only the personal exemption (2,000 `per: person`). Dependent, surviving spouse and
  zero-exemption amounts and the low-income exclusion are in `not_modelled`, with approximations.
- **Line 33 in the projection** covers every `public_pension`, needing `pension_source`. That
  understates tax for another West Virginia public pension; the projection can't tell systems apart.
  Lines 30 and 31 can't be told from it, so they are `not_modelled` (`has_pension`) with an
  `overstates_tax` approximation.
- **Indexing:** no inflation adjustment language found in the booklet. So it is `not_stated`, and the
  projection marks brackets, deductions and relief caps as not indexed (assumed).

## Unsure

- Line 47 column (c) leaves out lines 35 to 46 (railroad retirement, for example). The projection offsets
  the person's own income without that test, which slightly understates tax. That is an approximation.
- Whether the "regardless of age" federal and WV pensions on line 33 count in line 47 column (d) before
  the cap or after: the form says "Add lines 29 through 34", so after the 2,000 cap. That is what the
  approximation assumes.
- The Family Tax Credit's income test is written as `other` with the table in text. A `stepped` form
  would need a family-size dimension the schema doesn't have.

## 2026-11-08: marker ids and indexing covers

- Marker ids: all 12 markers have an `id`. Each takes its first from_record id, so warning codes are unchanged.
- Indexing covers: `brackets`, `deductions`, `relief_caps` (reliefs.cap). Added `relief_income_tests` (indexed false, assumed) for reliefs.income_test (the Social Security modification's AGI limit).
- Assumed entries: searched the archived sources (docling, pypdf and page text) for indexed, inflation, cost of living, adjusted annually and consumer price index, and for statements that figures are fixed; nothing says, so every `assumed: true` stays.
