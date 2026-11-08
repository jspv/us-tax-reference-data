# Settlement: Kansas, tax year 2025

- Readings: `work/extract/2025/KS.r6.A.json`, `work/extract/2025/KS.r6.B.json` (round r6)
- Sources: `sources/archive/2025/KS/`: 2025 booklet `ip25`, Form `k-4025`, Schedule S `schs25`, and the FAQ page `faqs-taxii`
- Outputs: `data/states/2025/KS.record.json`, `data/states/2025/KS.projection.json`
- Settled: 2026-11-07

## Stale sources: drop from the registry

Neither page below was used for any figure or rule. Both are still read by `tools.validate`, because it
scans every `*.page.txt`, so a stale figure could pass its provenance check until they are dropped.

| Saved page | What is stale | Evidence |
|---|---|---|
| `scheduleS_A.page.txt` (and `.html`) | 2007 text | line numbers from 2007 (retirement on line A12), "during 2007", and an old Social Security test: "If your Federal Adjusted Gross Income is $50,000 or less" |
| `incomebook25.page.txt` (and `.html`) | Part 2024 text | line A10 reads "received in 2024" where the PDF reads "received in 2025", and it has a "2024 TAX COMPUTATION WORKSHEET" heading |

The dispatch described `incomebook25.page.txt` as holding 2024 text. That is true of those two places, but
the page is a mix: its title says 2025 and the standard deduction and exemption amounts I looked at match
the 2025 PDF. I did not compare it line by line. It was treated as stale throughout.

## Comparison

`uv run python -m tools.compare` reported **27 structured differences** (122 wording differences). Taken
together they are three disagreements, and the booklet decided all three:

| # | Lines | Field | A | B | Booklet | Settled |
|---|---|---|---|---|---|---|
| 1 | 6 (2 deduction keys x what, per, amount) | Disabled veteran exemption: `per` | `exemption_claimed` | `person` | PDF page 2: "An additional exemption allowance of $2,320 will be allowed for each qualified disabled veteran." PDF page 6: "Enter the number of disabled veterans, multiply by $2,320" | `person`: the count is of veterans |
| 2 | 15 (5 relief keys x covers, form, who.basis) | How line A14 is split | federal (`public_pension`, `employer_plan_distribution`), military (`military_pension`, `employer_plan_distribution`), Kansas plans, Regents (`annuity`) | Kansas and federal together (`public_pension`, `annuity`), military | PDF page 12, line A14: a list of plans by payer, with "including Thrift Savings Plans" in the federal and Armed Forces bullet | Separate federal, military, Kansas and Regents entries, as A. Thrift Savings Plans get their own entry, which neither reader did (see below) |
| 3 | 6 (2 relief keys x covers, form, who.basis) | U.S. obligation interest: `who.basis` | `each_person` | `return` | PDF pages 11-12, line A12: "Enter interest or dividend income received from obligations or securities of any authority, commission or instrumentality of the United States"; no test on either spouse | `return` (extraction brief rule 5) |

Decided from the booklet: all three (all 27 lines).

**Why Thrift Savings Plans have their own entry.** A listed `employer_plan_distribution` inside the federal
and military entries, B left it out of `covers`. The booklet names them, so they belong in `covers` (rule 4),
but on A's entries that kind would read as if the federal entry covered any employer plan. The report tool
would also have shown a general 401(k) as exempt. On their own entry the "only Thrift Savings Plans" condition
travels with the kind.

## A difference the comparison did not show

The tool matches reliefs by form, covered income and age bounds. A's `kansas_public_pension` and B's
`kpers_lump_sum_subtraction` both read `public_pension` with no age test, so they were paired and only their
text was reported as different. They are different rules, line A14 and line A25. See the first row below.

## One-sided entries

| Entry | Reader | Kept? | Why |
|---|---|---|---|
| KPERS lump sum, line A25 | B (A had it in notes) | Kept as `kpers_lump_sum_subtraction` | PDF page 13 prints it and it is retirement relief. Line A25's opening limit is in its `not_covered` |
| Regents annuity contracts, line A14 | A as its own entry (B merged it) | Kept as `regents_annuity_contracts` | Its own income kind and its own rollover limit in the FAQ: "said distributions are subject to Kansas Income Tax" |
| Age 65 and blind amounts | Both, derived | Kept, plus the printed worksheet totals as four new `standard_deduction_worksheet_*` entries | The projection's `derived_figures` need the printed totals in the record; see below |
| Lump sum tax, KPERS add-back, 529, ABLE, nonresident military pay, recruitment bonus | Notes in one or both | Notes only | No field, or not retirement relief |
| A's note using line A25 as evidence on other-state pensions | A | Dropped as evidence | "You may not subtract the amount of your income reported to another state" limits the line A25 subtractions and says nothing about pensions paid by another state |
| `not_covered` on the Social Security entry | A | Moved to `other_conditions`, as B | It describes benefits that never reach federal AGI, not a kind of income refused relief |

## The required facts

1. **Another state's government pension, New York State included: not found in the booklet.** Line A14
   (PDF page 12) says "Enter total amount of benefits received from the following plans that was included in
   your federal AGI", and its list names federal, railroad and Kansas plans only. Nothing in the booklet or
   FAQ names another state's plan, so no entry has `public_pension_other_state` and `not_covered` has no
   wording for it to quote. The pension stays in Kansas income because it is in federal AGI and no line takes
   it out. This is read from how the lines work, not from a sentence saying it is taxed. The nearest general
   statement is in the FAQ: "You must file as a Kansas resident and report all income to Kansas, regardless of
   where it was earned."
2. **Own and federal government pensions: exempt in full, with no cap, age or income test.** Line A14:
   "Retirement benefits specifically exempt from Kansas Income Tax"; "Federal Civil Service Retirement or
   Disability Fund payments and any other amounts received as retirement benefits from employment by the
   federal government or for service in the United States Armed Forces including Thrift Savings Plans";
   "Kansas Public Employees' Retirement (KPERS) annuities". FAQ, second document: "Are Federal Civil Service
   annuities taxable to Kansas? No." and "Are military pensions taxable to Kansas? No." Only the Kansas plans
   named are covered, and first class city pensions only in part: "Certain pensions received from Kansas first
   class cities that are not covered by KPERS". The form's line A14 agrees (PDF page 21).
3. **Private pensions, IRA and employer-plan distributions, Roth conversions: not found as a subtraction.**
   The exceptions are narrow: Thrift Savings Plans, KPERS rollovers (line A11) and Regents annuities. Roth and
   conversions are not mentioned in the booklet, form or FAQ. PDF page 6 sends only "income that is taxable at
   the federal level but not taxable to Kansas" to Schedule S, so these follow federal AGI. No sentence says
   they are taxed, and no reader or settlement claims one.
4. **Social Security: exempt.** Line A10 (PDF page 11): "the amount of social security benefits received in
   2025 under the Social Security Act (including SSI) to the extent these benefits are included in your federal
   AGI", with no income test. The form's line A10 is on PDF page 21. FAQ, second document: "Effective for all
   taxable years commencing after December 31, 2023, social security benefits that are included in federal
   adjusted gross income are not subject to Kansas income tax."
5. **Brackets, standard deduction, exemptions.**
   - Worksheet, PDF page 34: 5.2% to 23,000 and 5.58% above for "Single, Head of Household, or Married Filing
     Separate"; 5.2% to 46,000 and 5.58% above for Married Filing Joint. Both readers agreed.
   - Second check: a script re-computed all 2,000 printed table rows (PDF pages 27-34) at their midpoints. None
     is more than 0.50 from the schedule in either column.
   - Standard deduction: 3,605 single, 8,240 joint, 6,180 head of household, 4,120 separate (PDF pages 2 and 6).
   - Exemption allowance: 18,320 joint, 9,160 others, plus 2,320 for head of household, each dependent, each
     child born in the year, a stillbirth and each qualified disabled veteran (PDF pages 2 and 6).

## Age 65 and blind amounts (derived)

The booklet prints only totals by boxes checked (PDF page 6), and each step is the same:

| Status | Totals | Step |
|---|---|---|
| Single | 3,605 / 4,455 / 5,305 | 850 |
| Head of household | 6,180 / 7,030 / 7,880 | 850 |
| Married filing joint | 8,240 / 8,940 / 9,640 / 10,340 / 11,040 | 700 |
| Married filing separate | 4,120 / 4,820 / 5,520 / 6,220 / 6,920 | 700 |

- All 12 steps are in the projection's `derived_figures`, and the validator re-does each one.
- The record's `notes` hold the same arithmetic.
- `tools.validate` finds 850 and 700 elsewhere in the booklet by coincidence, so its provenance pass is no
  evidence for them. The worksheet totals are.
- Second document: the filing thresholds on PDF page 3 equal standard deduction plus exemption and rise by the
  same steps (single 12,765 / 13,615 / 14,465; joint 26,560 to 29,360; head of household 17,660 / 18,510 /
  19,360; separate 13,280 / 13,980 / 14,680).

## Other decisions

- **Qualifying surviving spouse: neither reader caught this.** PDF page 6: "If your federal filing status is
  Qualifying Widow(er) with Dependent Child, check the Head of Household box." The head of household amounts
  are recorded under `qualifying_surviving_spouse`, including the 2,320. The schema has no bracket list for
  this status and falls back to the joint schedule, which is wrong for Kansas. It is listed as an approximation
  (understates tax by at most 87.40 a year).
- **Head of household exemption in the projection.** Folded into one return-level amount, 9,160 + 2,320 = 11,480
  (in `derived_figures`). No settled state has a deduction that applies to only some statuses, so I did not
  introduce that shape; the projection cannot write a 0 the record doesn't print. PDF page 3 confirms the
  total: 17,660 = 6,180 + 11,480.
- **`brackets.derivation`.** Added with 12 printed table rows across both bands and all four statuses. The
  `formula` field is left out: it holds one formula, the validator tests it against both single and joint, and
  Kansas prints two (less 87, less 175). Both are in `notes`.
- **`married_separate` and `head_of_household` brackets** are kept although they equal `single`. The worksheet
  names those statuses in its heading, and both readers agreed.
- **`form`.** Written `exempt_in_full` for these uncapped entries. The comparison treats it the same as
  `subtraction`, and the pension report prints "exempt in full" only for this value.
- **Fields not used.** `all_income_scope` and `income_test.applies_when` do not apply: Kansas has no age
  deduction against any income, and no income test on any retirement relief. The $75,000 Social Security test
  in the FAQ is for years before 2024. `paying_states`, `share`, `credit_basis`, `recapture` and stepped
  `steps` have nothing to hold either.
- **Wording chosen for the report tool.** `tools/report_pensions.py` treats an entry as a special case when its
  label or conditions contain words such as "police", "teacher", "disab" or "fire", and reports the main line
  as taxed if no other entry is left. Line A14's plain plan list contains those words. So the full list is in
  `notes`, and the conditions refer to it. With this wording the report shows Kansas and federal pensions as
  exempt in full. Nothing is lost, but the matcher could misreport other states.
- **Projection, not modelled.** Blind amount, dependent, child-born and stillbirth exemptions, disabled veteran
  exemption, Thrift Savings Plans, KPERS rollover and lump sum, Regents annuities, U.S. obligation interest.
- **Social Security in the projection.** `treatment: exempt` carries it; the record's relief entry is not
  repeated there.
- **Indexing.** Not stated anywhere; the projection assumes no growth for brackets and deductions.

## Unsure

- **Other-state pensions and private retirement income** are read from silence, not a sentence. The projection
  says so in `approximations`. The cross-state report prints "**taxed**" for New York and New Jersey pensions
  in Kansas, which is firmer than the booklet's own words. The statute was not read.
- **`public_pension` is broader than the list.** The projection exempts every `public_pension`, but a Kansas
  local plan not on line A14 is taxable. `pension_source` cannot tell them apart, so this is an approximation
  that understates tax.
- **Thrift Savings Plan warning.** `warn_when: has_pension` will miss a household with a Thrift Savings Plan and
  no pension. `always` would warn every Kansas household, so I took the narrower one.
- **Separate returns.** The worksheet allows four boxes on a separate return, spouse's included. The projection
  counts age-65 amounts per person, which matches only if it treats the couple's persons as one return.
- **`checks/2025/KS`** does not exist yet. `tools.export` runs the checks before including a state, so Kansas
  needs hand-worked checks before export. Writing them was outside this settlement.

- Main session, 2026-11-07 (format for the first frozen schema): the Thrift Savings Plan and KPERS rollover markers now warn on has_retirement_account_distribution instead of has_pension, which missed a household with plan or IRA withdrawals and no pension.

## 2026-11-08: marker ids and indexing covers

- Marker ids given: first from_record id (warning code unchanged): `blind_additional_standard_deduction`, `dependent_exemption`, `disabled_veteran_exemption`, `thrift_savings_plans`, `kpers_rollover_withdrawals`, `regents_annuity_contracts`, `kpers_lump_sum_subtraction`, `us_government_interest_subtraction`.
- Indexing covers: `brackets` -> `brackets`; `deductions` -> `deductions`.
- Every `assumed` answer was checked again against the archived sources (searched for indexed, inflation, cost-of-living, adjusted annually, each year, CPI, fixed): none says, so all stay `assumed: true`.
- Warning codes unchanged (every id is the marker's first from_record id).
