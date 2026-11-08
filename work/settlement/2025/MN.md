# MN 2025 settlement log

Readings: `work/extract/2025/MN.r6.A.json`, `MN.r6.B.json`. Settled 2026-11-07. Page numbers are PDF pages.

`tools.compare` gave 14 structured differences and 78 wording differences. All 14 are settled: 9 from the
booklet and 5 that are the same number written two ways. Three more corrections were made where the
readers agreed or stayed silent; they are listed after the table.

Sources in the archive: Form M1 instructions (m1-inst-25), Form M1, Schedule M1M, Schedule M1QPEN, Schedule M1R
(added after the first settlement, see below), and two Department of Revenue web pages (public pension subtraction,
Social Security benefit subtraction).

## Structured differences

| # | Field | A | B | Settled | Page and reason |
|---|---|---|---|---|---|
| 1-4 | `brackets.*[1].rate` (four statuses) | 0.0680 | 0.068 | 0.068 | Same value; M1 inst p.39 prints 6.80%. Formatting. |
| 5 | `indexing` second entry | brackets, not_stated | none | none | Same answer either way. No document in the archive mentions inflation or indexing, so nothing is said about brackets: `all_other` only. |
| 6-8 | US bond interest relief (`covers`, `form`, `who.basis`) | none | present | kept | M1M p.5 line 14. See one-sided entries. |
| 9-10 | pension `income_test.applies_when` (two entries) | missing | over | over | M1QPEN p.1: "If line 4 is less than or equal to line 5, skip lines 6 through 9". |
| 11 | alternative method `measure.base` | other | federal_agi | other | M1M p.4 steps 9-19 start from Form 1040 line 9 (total income), not AGI, and add 50% of line 6a. |
| 12 | alternative method `minus_taxable_social_security` | missing | true | true | M1M p.4 step 11 subtracts line 6b. A's `other` and B's flag are both right; `plus_tax_exempt_interest` true as both said (step 14). |
| 13 | alternative method `rate` | 0.20 | 0.2 | 0.2 | Same value; M1M p.4 step 22 prints 20%. Formatting. |
| 14 | `social_security.treatment` | relief | exempt | relief | See Social Security below. |

From the booklet: 5, 6-8, 9-10, 11, 12, 14 (9). Formatting only: 1-4, 13 (5).

## Corrections beyond the comparison

- **Pension `who.basis`: each_person (both readers) changed to return.** M1QPEN p.3, Line 1 example scenario 2:
  "The retired corrections officer received $50,000 ... and the firefighter received $30,000 ... They will use
  $80,000 on line 1". Spouses share one line 1 and one cap, and there is no age test.
- **`cannot_combine_with` on the pension entries (A only): removed.** A used it to stop the cap doubling, but
  M1QPEN p.3 says "If you receive multiple qualified public pensions, include all taxable qualified public
  pension payments on line 1", so the plans do combine. The shared cap is in `cap_rule`. A's `cap_rule` on the
  other-state entry also pointed at itself; rewritten.
- **`mn_foreign_service_retirement`: added; neither reader kept an entry.** M1M p.8 line 36 and its worksheet print
  a retirement subtraction. No dollar cap; prorated by foreign service years.

## One-sided entries

- `us_bond_interest_subtraction` (B): kept, as `mn_us_bond_interest`. Printed on M1M p.5 line 14 and in scope;
  written exempt_in_full because no cap or test is printed. Projection: not_modelled, warn never (a projection
  cannot tell it from other interest).
- A's `brackets` indexing entry: dropped (row 5).
- A's `not_covered` on the military pension: kept, the federal-taxable test is printed (M1M p.7).
- B's fuller pension `not_covered` wording (service with Social Security credit "whether or not" benefits are being
  received; lines 20, 21, 22, 25, 36): kept, merged with A's. A had the line list in `other_conditions`; moved.
- Reader ids: A's `mn_` ids used. No figure depends on them.

## The five required facts

**1. Government pension paid by another state, New York State in particular.**
Conditional. Recorded as `mn_qualified_public_pension_other_state`, `covers: ["public_pension_other_state"]`, no
`paying_states`. Neither "New York" nor any other paying state appears in the sources (searched all text files).

- M1QPEN p.2 table: "Plans administered by another state or its political subdivisions or the District of
  Columbia if they allow a similar or reciprocal subtraction or exemption".
- Web page, Pension Plans That Qualify: "A plan created by another state or its political subdivisions, or the
  District of Columbia, if the other state allows a similar subtraction or exemption for the Minnesota pension
  plans listed".
- The rest of the test also applies: service without Social Security credit, AGI under the limit.

Rule for a Minnesota resident with a New York State pension: taxed as part of federal AGI unless New York allows
a similar or reciprocal subtraction for the listed Minnesota plans and the service earned no Social Security
credit; then up to 13,540 (27,080 joint), stepped down by AGI. The sources do not say whether New York passes
that test. Left out of `paying_states` means "no state is named" here, not "every state": this is noted in
the record because the schema reads an absent list as any other state.

Minnesota's reciprocity agreements are a different rule. M1M p.5: "Reciprocity applies only to personal service
income, such as wages, salaries, tips, commissions, fees, and bonuses." Michigan and North Dakota only.

**2. Own and federal government pensions.**
`mn_qualified_public_pension`, `covers: ["public_pension"]`, cap 13,540 (27,080 MFJ/QSS), for one return.

- M1QPEN p.2: "Qualified pension plan: A public pension that is specifically listed in the table below where
  contributions were made by a basic member."
- M1QPEN p.2: "Recipients of the federal Civil Service Retirement System (CSRS) pension are considered basic
  members"; "Recipients of the Federal Employees Retirement System (FERS) pension are considered coordinated
  members"; "Coordinated members are not eligible for the Qualified Public Pension Subtraction unless they were
  converted from a basic member to a coordinated member during their service."
- The test is service without Social Security credit, not a contributory plan, so `pension_contributory` does not apply.
- Second document: the web page gives the same cap and the same limits (103,489; 127,319; 73,159).

**3. Private pensions, IRA and employer-plan distributions, Roth conversions.**
Not found in the booklet as any subtraction or exclusion. They arrive through federal AGI. M1 inst p.11: "Enter the
total taxable IRA distributions, pensions, and annuities you received in 2025"; "Enter your 2025 federal adjusted
gross income from line 11a of Form 1040". The M1M subtraction list (pp.1-2) has no line for them. "Roth" appears
nowhere in the sources. Recorded as not found, not as "the booklet says there is none". The only general relief
these incomes can meet is the Age 65 or Older/Disabled Subtraction, which applies against any income (below).

**4. Social Security.** `treatment: relief`, not exempt.

- M1M p.3: "Enter the full amount from line 6b of Form 1040 or 1040-SR on line 12 of Schedule M1M, if your adjusted
  gross income was below these amounts based on your filing status"; "If your adjusted gross income is greater than
  these amounts, you must determine your subtraction using the Worksheet for Line 12. Your subtraction equals the
  greater of step 28 (Alternative Method) or step 29 (Simplified Method)."
- A second document agrees. Web page: "The subtraction is phased out by 10% for each $4,000 of AGI in excess of the
  income levels mentioned. For Married Filing Separately, the phaseout is 10% for each $2,000 of AGI over $54,160."
- B's `exempt` comes from the schema's "a subtraction line for taxable Social Security counts as exempt". That fits a
  full subtraction. Here a high-income filer loses all of it, so A's `relief` is the printed reading.
- Both entries share `best_of_group: mn_social_security_subtraction`.

**5. Brackets, deductions, exemptions.**

- Four schedules on M1 inst p.39, one per status; both readers agree. Recomputed against p.39's own figures (equal
  or 1 cent off) and all 3,476 table cells (at most 54 cents off at row midpoints). Tax table below 86,800.
- Standard deduction 14,950 / 29,900 / 14,950 / 22,500 on p.4 and p.13. Additions 2,000 / 1,550 per box, p.13 step 4.
- "Your standard deduction is reduced by up to 80%" above 238,950 (119,475 separate): p.4, p.14.
- Dependent exemption 5,200, p.4 and p.14. No personal exemption printed for the filer or spouse.

## Stepped bands

- `steps` is in the record format, but `tools/validate.py` requires every figure in a record to be printed, and the
  band edges are not (86,490, 88,490 and so on). The record has no `derived_figures`. So the pension and simplified
  Social Security tests stay `effect: other` with the printed formula. I did not change the validator.
- The projection holds the Social Security bands exactly: 50 `steps` rows, 34 `derived_figures`. Simulated against
  worksheet steps 2-8 at 28,457 AGI values, all five statuses, with no mismatch.
- Getting there needed two workarounds. `rate: "0.1"` sits on an `effect: other` test so 0.1 is a record figure,
  and the printed 4,000 is written as 2,000 + 2,000 because no record field holds a width.
- Pension: the worksheet reaches zero at AGI over 102,490 (Single/HoH), 126,320 (MFJ/QSS), 72,160 (MFS), before the
  printed limits, so the limits never decide anything.

## Projection decisions

- **Qualified Public Pension Subtraction: not_modelled, warn has_pension, with an approximation (overstates_tax).**
  `docs/projection-guide.md` lists "Social Security-exempt employment" as not_modelled, and MI, KY and NC set the same
  precedent. `needs_input` has no value for it. Modelling on `pension_source` alone would hand the subtraction to
  coordinated members, who do not qualify.
- **Standard deduction reduction:** `phase_out_rate` 0.03 on the base amount; the 10% tier and the 80% limit are an
  approximation (either, mostly understates; about 1,800 of tax at 566,000 of joint AGI).
- **Alternative Social Security method:** the record's measure is outside the projection list, so it maps to federal AGI
  plus tax-exempt interest. That is nearer than also subtracting taxable benefits: AGI runs at most 35% of benefits
  over step 19, while subtracting line 6b runs up to 50% under it. Overstates tax.

## Schedule M1R, added after the first settlement

Both readers and the first settlement had no Schedule M1R, so they recorded no relief. It has since been fetched
(`m1r-25`, 2026-11-07). Entries added from it replace the earlier "not in the archive" note and marker. **No second
reader has read this schedule**; these entries rest on one reading, cross-checked as below.

Worksheet, M1R p.1:

- Line 1: "If you are married and filing a joint federal income tax return, enter $12,000. If you are single, enter
  $9,600. If you are married and filing separately, enter $6,000".
- Line 8: line 3 less line 7 (line 7 adds Schedule R line 13b amounts, nontaxable Social Security and Railroad
  Retirement Board benefits). "If zero or less, STOP HERE."
- Lines 9-13: AGI measure, less the line 10 amount, times 50%, taken off line 8.
- Line 10, p.2: 14,500 single, head of household, qualifying surviving spouse; 18,000 joint, both spouses; 14,500 joint,
  one spouse; 9,000 separate.

Entries, one per branch (the amount and line 10 differ by branch):

| Entry | Who | covers | Cap | Line 10 |
|---|---|---|---|---|
| `mn_age_65_subtraction` | older spouse born before January 2, 1961; on a joint return both qualify | all_income | 9,600 / 12,000 / 6,000 for the return | 14,500 / 18,000 / 9,000 |
| `mn_age_65_subtraction_one_spouse` | joint, one spouse qualifies | all_income | 12,000 | 14,500 |
| `mn_disabled_subtraction` | under 65, permanent and total disability, taxable disability income | other_income | same, limited by line 2 | same; 14,500 joint with one spouse |

Decisions:

- `who.basis: older_spouse`: line 2 asks "If you (or your spouse if filing a joint return) are 65 or older", and one
  amount applies to the return, so one qualifying spouse is enough and two do not double it.
- `covers: all_income` for age: line 3 takes the line 1 amount whatever the income. Line 2 limits only the under-65 branch.
- `effect: phase_out_rate`, `rate: 0.5` is a true per-dollar rate here, so `steps` and off-label use are not needed.
- Disabled entry `other_income`: line 2 takes disability pensions and insurance payments on Form 1040 line 1z, the
  wage line, and no income kind names them. Judgement call.
- Measure `other`: M1R line 9 takes off railroad benefits and adds Form 4972 lump sums, so it is not plain AGI.

Checks:

- Second document: M1 inst p.15 prints the same four pairs of limits as M1R p.2. pypdf and docling agree on every figure.
- Each AGI limit equals line 10 plus twice line 1 (33,700; 42,000; 38,500; 21,000), and the benefit limit equals line 1.
  So the printed table is exactly where the worksheet reaches zero, and it is held in `as_printed`, not as a second test.
- Line 1 says only "single"; the p.2 table groups head of household and qualifying surviving spouse with it at 9,600,
  and line 10 groups them too. Settled at 9,600 for all three.
- Projection relief against the worksheet, 22,145 cases over all five statuses: no mismatch. This tests the formula as
  I read the schema (cap, then `cap_reduced_by`, then income test), not a consumer's code.

Projection:

- `mn_age_65_subtraction` from both age entries: `older_spouse`, `min_age: 65`, `cap_reduced_by: ["social_security",
  "railroad_retirement"]`, `phase_out_rate` 0.5 over line 10.
- Disabled branch: not_modelled, warn never, per the guide.
- Joint one-spouse case uses 18,000: `who` cannot test both spouses, and both-65 is the state a long projection spends
  most years in. Understates tax by at most about 94, only in years one spouse qualifies.
- Separate filers: the lived-apart test is not applied. Understates tax by at most about 321.
- Measure maps to federal AGI, direction either. Line 4 (Schedule R) is not taken off.

Example, joint, both 65, AGI 30,000, nontaxable Social Security 5,000: 12,000 - 5,000 = 7,000, less 50% of 12,000 =
1,000. With nontaxable Social Security of 14,000 the worksheet stops at line 8 and the subtraction is 0.

## Missing from the sources

- **Schedule M1C** (joint-filer credit on earned, pension or Social Security income, and others), **Schedule NIIT**
  (rate), **Schedule M1MT**, **Schedule M1LS**, **Schedule M1NC**, **Schedule M1SA**, **Fact Sheet 6, Seniors**.
- Any list of which states meet the "similar or reciprocal" test.

## Unsure

- `cap_reduced_by: social_security`: M1R takes off nontaxable benefits only, and the schema does not say whether the
  list means benefits received or the taxable part. Benefits received is the right reading here and overstates tax; a
  consumer that uses the taxable part would hand out the subtraction to households that get nothing. Needs confirming.
- Pension in not_modelled: this follows the guide's explicit list, but the guide also says to model reliefs that treat
  pension kinds differently. If it should be computed, a consumer needs a new input (service without Social Security
  credit) and a schema change; the record already holds the rule.
- `rate` on `effect: other` (simplified Social Security, standard deduction) has no precedent in another state and is
  off-label against the schema's description. Explained in each `as_printed`.
- `phase_out_rate` on a deduction has no precedent in another projection; other states use stepped or removes there.
  A consumer should confirm it applies the rate to the excess AGI for `base.deductions`.
- The public pension web page's example says "in 2024" where M1QPEN says 2025. Its figures match the 2025 schedule.
- M1M p.3 says "below" and "greater than", leaving AGI exactly at the amount to the worksheet, which gives the full
  subtraction. Recorded as `over`.

- Main session, 2026-11-07 (format v1): `social_security_basis: nontaxable` set on the relief(s) whose cap Social Security reduces, stating what the cases already used.

## 2026-11-08: marker ids and indexing covers

- Marker ids given: first from_record id (warning code unchanged): `mn_qualified_public_pension`, `mn_foreign_service_retirement`, `mn_dependent_exemption`, `mn_blind_standard_addition`, `mn_us_bond_interest`, `mn_disabled_subtraction`; descriptive: `mn_marriage_credit` (the joint filers' credit on Schedule M1C; no from_record id); `mn_niit_amt_lump_sum` (no from_record id); `mn_other_credits_and_subtractions` (no from_record id).
- Indexing covers: `brackets` -> `brackets`; `deductions` -> `deductions`; `relief_caps` -> `reliefs.cap`; `relief_income_tests` -> `reliefs.income_test`.
- Added `relief_income_tests` (indexed false, assumed) for the age 65 subtraction and both Social Security subtraction income tests.
- Every `assumed` answer was checked again against the archived sources (searched for indexed, inflation, cost-of-living, adjusted annually, each year, CPI, fixed): none says, so all stay `assumed: true`.
- `tools.checks --fix-warnings` updated the cases' accepted_warnings where a code changed; nothing else in the cases changed.

## 2026-11-08: indexing settled from statutes

Statute research (work/indexing/findings*.json) settled every projection indexing entry that was `assumed: true`:

- `brackets` (brackets): indexed, Minn. Stat. 290.06, subd. 2d; 270C.22, subd. 1
- `deductions` (deductions): indexed, Minn. Stat. 290.0123, subd. 6
- `relief_caps` (reliefs.cap): not indexed, Minn. Stat. 290.0802 subd. 2; 290.0132 subd. 26(f),(g),(j)
- `mn_age_65_subtraction_income_test` (reliefs:mn_age_65_subtraction.income_test): not indexed, Minn. Stat. 290.0802, subd. 2(b)(2)
- `mn_social_security_simplified_income_test` (reliefs:mn_social_security_simplified.income_test): indexed, Minn. Stat. 290.0132, subd. 26(c), (j)
- `mn_social_security_alternative_income_test` (reliefs:mn_social_security_alternative.income_test): not indexed, Minn. Stat. 290.0132, subd. 26(f), (g)
- Record `indexing`: added brackets -> yes; added mn_standard_deduction -> yes; added mn_age_65_standard_addition -> yes; added mn_age_65_subtraction -> no; added mn_social_security_simplified -> yes; added mn_social_security_alternative -> no.
