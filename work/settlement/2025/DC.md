# Settlement: District of Columbia, tax year 2025

- Readings: `work/extract/2025/DC.r5.A.json`, `work/extract/2025/DC.r5.B.json` (round r5)
- Sources: `sources/archive/2025/DC/` (2025 D-40 Booklet, Individual Income Tax Forms and Instructions,
  105 PDF pages; 2025 D-40 form)
- Outputs: `data/states/2025/DC.record.json`, `data/states/2025/DC.projection.json`
- Settled: 2026-11-07

## Page numbers

Page numbers below are PDF page numbers (pypdf; pages 4, 13 and 51 also rendered and read as images).
The docling conversion has only 96 page markers for the 105-page PDF, so its markers drift after page 20:
B's cites "page 46" (Calculation G-1), "page 58" (Schedule I) and "page 60" (Calculation B instructions)
are docling markers for PDF pages 51, 64 and 66. The record cites the PDF pages.

## Comparison

`uv run python -m tools.compare` reported **21 structured differences** (60 wording differences). They are
three disagreements:

| # | Lines | Field | A | B | Booklet | Settled |
|---|---|---|---|---|---|---|
| 1 | 16 (8 under A's key, 8 under B's) | Disability exclusion, Schedule I Calculation B Lines 7a/7b: `covers`, `income_test.measure.base` (the rest, cap 10000 per return, effect removes, threshold 100000, each_person, agree but sit under different keys) | `all_income`; `federal_agi` | `other_income`; `household_income` | PDF page 66: "Income not to exceed $10,000 is excludable in computing DC gross income for persons determined by the Social Security Administration to be totally and permanently disabled ... and whose annual household adjusted gross income is less than $100,000. Household income includes income received by all household members in the year, even income excluded from federal adjusted gross income." | `covers: ["all_income"]` (A; income of any kind, brief rule 14); measure `household_income` (B; the test is on the household's income, not the filer's federal AGI) |
| 2 | 3 | Line 10 relief entry (social_security, railroad_retirement) | entry | none | PDF page 20, Line 10 "Taxable amount of social security and tier 1 railroad retirement ... Enter the amount from 1040 or 1040-SR"; D-40 form page 2, Line 10 under "Subtractions from DC Income" | kept (one-sided, printed, in scope; the only line carrying tier 1 railroad retirement) |
| 3 | 2 | Indexing entries for `brackets` and `standard_deduction` (not_stated) | present | absent (only `all_other`) | PDF pages 5, 13 and 20 say nothing about inflation adjustment | dropped (brief rule 8: an entry per figure only when the booklet says something about it); `all_other: not_stated` kept |

Decided from the booklet's text: 19 of 21 lines (#1 and #2). The 2 indexing lines (#3) were decided by the
extraction brief's rule 8 after confirming the booklet is silent.

## Standard deduction (raised by the dispatch)

The dispatch said A found no standard deduction and B found 15,000 / 22,500 / 30,000 plus 65-or-blind
amounts. In the r5 readings both readers recorded the same amounts (A: `standard_deduction`,
`additional_standard_age65`, `additional_standard_blind`; B: `std_deduction`, `age_65_additional_std`,
`blind_additional_std`), so the compare tool shows no structured difference there. Settled anyway from the
booklet, on four pages:

- PDF page 4, "DC Basic Standard Deduction": "For tax year 2025, those amounts are: $15,000 for single
  filers, dependent filers and married/registered domestic partner filers filing separately; $22,500 for head
  of household filers; and $30,000 for married/registered domestic partners filing jointly and qualifying
  widow(er) with dependent child filers." Same page, "Additional Standard Deduction": "If you or your
  spouse/registered domestic partner were born before January 2, 1961, or blind, an additional standard
  deduction of $1,600 ($2000 if single, head of household, or dependent claimed by someone else and are not
  married) is allowed."
- PDF page 13, "Standard Deduction": the same three amounts, plus "married/registered domestic partners
  filing separately on the same return are allowed a standard deduction of $30,000", and "You are not
  entitled to the standard deduction if you itemize on your federal return." (The pypdf text of this page is
  garbled, "$£x,000" and "$22,x00"; the rendered page reads $15,000 and $22,500.)
- PDF page 7, filing requirements chart: 15,000 single, married filing separately and dependent filer;
  30,000 joint, same-return separate and qualifying widow(er); 22,500 head of household.
- PDF page 51, Schedule S Calculation G-1: line a basic amount; lines b-e count age 65 (born before
  January 2, 1961) and blindness for the filer and, for joint or same-return filers, the spouse; line g
  "Multiply $1,600 ($2,000 if your filing status is single, head of household, or dependent claimed by
  someone else and are not married) by the number on Line f."

Recorded: standard deduction per return (15,000 single and married_separate; 22,500 head_of_household;
30,000 married_joint and qualifying_surviving_spouse); age 65 and blind amounts per person (2,000 single
and head_of_household; 1,600 married_joint, married_separate, qualifying_surviving_spouse). No personal or
dependent exemption is printed (G-1 line i counts dependents, no amount).

## The five facts, each with its quote

1. **Another state's government pension, and a New York State pension**: not found in the booklet; taxed
   as part of federal AGI. PDF page 19, Line 4: "Include your taxable portion of pension/annuity in your
   federal adjusted gross income." The only government-pension line, D-40 Line 12, is titled "DC and federal
   government survivor benefits" (PDF page 20) and names no other government. `public_pension_other_state`
   is in no entry's `covers`; the record's notes say "not found in the booklet" (rule 15a).
2. **DC's own and federal government pensions**: no exclusion for a retiree's own pension. Only survivors:
   PDF page 20, Line 12: "If you are an annuitant's survivor and 62 years of age or older as of December 31,
   2025, enter the total survivor benefits (do not include Social Security survivor benefits)." Recorded as
   `government_survivor_benefits` (covers `public_pension`, min_age 62, no cap).
3. **Private pensions, IRA and employer-plan distributions, Roth conversions**: no relief found on D-40
   Lines 8-14, Schedule I Calculation B Lines 1-15 (PDF page 64) or their instructions (PDF pages 20, 66);
   taxed via federal AGI (PDF page 19, Line 4, quoted above). Federal Schedule 1-A deductions, including the
   Enhanced Deduction for Seniors, are not allowed (PDF page 4).
4. **Social Security**: exempt. D-40 form page 2, Line 10 "Taxable amount of social security and tier 1
   railroad retirement" under "Subtractions from DC Income"; PDF page 20, Line 10 "Enter the amount from
   1040 or 1040-SR."
5. **Brackets, standard deduction, exemptions**: one schedule for every filing status, PDF page 20
   Calculation I and PDF page 5 Income Tax Rate Table: 4% to 10,000; 6% from 10,000; 6.5% from 40,000;
   8.5% from 60,000; 9.25% from 250,000; 9.75% from 500,000; 10.75% from 1,000,000. Cumulative amounts
   check (400; 2,200; 3,500; 19,650; 42,775; 91,525). Tax on taxable income of 100,000 or less comes from the
   tax tables; three rows checked against the schedule: 21,650-21,699 = 1,101 (PDF page 96; schedule at the
   midpoint 1,100.50), 50,950-50,999 = 2,913 (PDF page 99; 2,913.38), 82,350-82,399 = 5,401 (PDF page 102;
   5,401.88). `brackets.derivation` not used because the schedule itself is printed. Standard deduction and
   exemptions: above.

## Other decisions

- Line 10, Line 12 and Calculation B Line 1 kept as `form: subtraction` (both readers); the compare tool
  keys an uncapped subtraction as `exempt_in_full`, so this is not a difference.
- Line 12 `other_conditions`: A's and B's wordings merged (survivor of a DC or federal government
  annuitant; age as of December 31, 2025).
- Line 10 `cap_rule` notes that only tier 1 railroad retirement is named; tier 2 is neither covered nor
  excluded in the booklet, so nothing goes in `not_covered`.
- Disability exclusion `as_printed` extended with the page 66 sentence on whose income counts (tenants
  under a written lease excluded). Form D-2440 exclusion (Calculation B Line 2): rules not in the booklet,
  no entry.
- B's notes on unemployment benefits (Line 13), the filing threshold (page 7) and the $3,000 capital loss
  limit (page 19) kept as notes.

## Projection

- Brackets: the one schedule for single and married_joint (other statuses fall back by the schema).
- Base: federal AGI less the DC standard deduction (per return) and the age-65 additional amount (per
  person, `min_age` 65).
- Social Security exempt; railroad retirement `exempt_in_full` from `social_security_tier1_subtraction`
  (Social Security left to the top-level treatment so it is not subtracted twice).
- `not_modelled`: Line 12 survivor benefits (`has_pension`; survivor status not known), the blind amount
  (`never`), the disability exclusion (`never`), US obligation interest (`never`).
- Approximations: pensions and survivor benefits taxed (overstates, only for a survivor 62+); itemizing not
  modelled (either); tier 2 railroad retirement exempted (understates); blind and disability amounts left
  out (overstates); Treasury interest taxed (overstates); DC bonds treated as other-state (overstates);
  same-return separate filing not modelled (either); tax tables vs schedule (either, under 3 dollars);
  QSBS and business additions not modelled (understates).
- Indexing: brackets and deductions `indexed: false, assumed: true`.

## Validator

```
data/states/2025/DC.record.json: ok
data/states/2025/DC.projection.json: ok
```

## Unsure

- New York State pension: the booklet is silent, not explicit. The "taxed" reading rests on Line 4 (all
  of federal AGI) and on no subtraction line naming it; there is no sentence saying other states'
  pensions are taxed.
- Disability exclusion `cap_per: return`: the booklet says "persons ... Income not to exceed $10,000" and
  the form line says "up to $10,000"; per person is also a fair reading.
- Tier 2 railroad retirement: Line 10 names tier 1 only; the projection exempts all railroad retirement
  because it cannot split tiers (understates tax for tier 2 recipients).
- Qualifying widow(er) additional amount 1,600: read from the 2,000 list (single, head of household,
  unmarried dependent) not naming it; not printed for that status directly.

## 2026-11-08: marker ids and indexing covers

- Marker ids given: first from_record id (warning code unchanged): `government_survivor_benefits`, `additional_standard_blind`, `disability_income_exclusion`, `us_obligations_interest`.
- Indexing covers: `brackets` -> `brackets`; `deductions` -> `deductions`.
- Every `assumed` answer was checked again against the archived sources (searched for indexed, inflation, cost-of-living, adjusted annually, each year, CPI, fixed): none says, so all stay `assumed: true`.
- Warning codes unchanged (every id is the marker's first from_record id).
