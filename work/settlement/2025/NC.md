# Settlement: North Carolina, tax year 2025

- Readings: `work/extract/2025/NC.r3.A.json`, `work/extract/2025/NC.r3.B.json` (round r3)
- Sources: `sources/archive/2025/NC/` (2025 D-401 Individual Income Tax Instructions; 2025 Form D-400 Schedule S)
- Outputs: `data/states/2025/NC.record.json`, `data/states/2025/NC.projection.json`
- Settled: 2026-11-07

## Comparison

`uv run python -m tools.compare` reported **15 structured differences** (71 wording differences). Taken
together they are two disagreements, and the booklet decided both:

| # | Lines | Field | A | B | Booklet | Settled |
|---|---|---|---|---|---|---|
| 1 | 9 (3 relief keys x covers, form, who.basis) | Bailey exclusion, Schedule S Line 20 | two entries: defined benefit plans (`public_pension`, `military_pension`); the state's 401(k) and 457 plans (`employer_plan_distribution`) | one entry covering all three | PDF page 18, Line 20: defined benefit plans (TSERS, LGERS, CJRS, FERS, CSRS) qualify "if the retiree had five or more years of creditable service as of August 12, 1989"; the state's 401(k) and 457 plans qualify "if the retiree had contributed or contracted to contribute to the plan prior to August 12, 1989". Two branches, two tests. | A's two entries (`bailey_defined_benefit`, `bailey_state_401k_457`), each with its own conditions, as the extraction brief asks (one entry per branch) |
| 2 | 6 (2 relief keys x covers, form, who.basis) | US obligation interest, Schedule S Line 18: `who.basis` | `each_person` | `return` | PDF page 18, Line 18: "Enter the amount of interest received from notes, bonds, and other obligations of the United States ... or United States possessions." No test on either spouse's age or status. | `return` (schema: `return` when neither spouse is tested) |

Decided from the booklet: both (all 15 lines).

## Other decisions

- **Municipal interest** (both readers said `other`): settled to `other_states_taxed_own_exempt` from the
  booklet's lines. The starting point is federal AGI (PDF page 12, Line 6), which leaves out tax-exempt
  interest. Schedule S Part A says "only add items that are not included in federal adjusted gross income"
  (Schedule S page 2), and Line 1 (PDF page 17) adds back interest on obligations "of states and political
  subdivisions other than North Carolina", including exempt-interest fund dividends "to the extent such
  dividends do not represent interest from obligations of North Carolina or its political subdivisions".
  No line adds NC's own obligation interest back, so it stays out of NC income. The booklet does not say
  "NC interest is exempt" in one sentence; this is read from how the lines work.
- **Child deduction** (both readers: `phase_out.effect: other`, the table in `as_printed`): rewritten as
  `effect: stepped` with 35 `steps` (7 bands for each of single, married_separate, head_of_household,
  married_joint, qualifying_surviving_spouse) from the Child Deduction Table, PDF page 13. Threshold kept as
  the AGI up to which the full 3,000 applies (20,000 / 30,000 / 40,000). "Up to $40,000" is read as inclusive,
  so the step "over 40000" starts the 2,500 band.
- **Bailey "may or may not be excluded" sentence**: A had it in `not_covered`; moved to `notes`, because it
  does not say those benefits do not qualify.
- **Other-state government pensions**: the booklet says Bailey "does not apply to retirement benefits paid to
  former teachers and state employees of other states"; kept in `not_covered`, and `public_pension_other_state`
  is not in `covers`.
- **Line 19 `who.basis`**: both readers said `each_person`; left as agreed (benefits belong to a person; no
  cap, so it has no effect).
- **Descriptive `other_conditions` from B** on Lines 18 and 19 (which benefits or obligations count): not
  tests a planner may not know, so moved into the label, cite and notes rather than `other_conditions`.

## One-sided entries

- Indexing cites (B only, three entries): dropped; the entries say `not_stated`, and a cite to the page where
  the figure is printed adds nothing. The answers themselves match.
- Bailey `cannot_combine_with` (B: on its single entry; A: on both entries): kept on both of A's entries.
  PDF page 19: "Retirees of the United States Uniformed Services who deducted retirement income on Line 20
  under Bailey may not deduct the same retirement income on Line 21."
- No other one-sided structured entries.

## Facts checked against a second line or document

- **Social Security**: exempt. Instruction PDF page 18, Line 19 ("Social Security and railroad retirement
  benefits are not subject to state income tax"), and the form line, Schedule S page 3, Line 19, under Part B
  "Deductions ... (Only deduct items that are included in federal adjusted gross income)".
- **Rate**: 4.25% flat on NC taxable income, PDF page 7 ("What is the Tax Rate?") and PDF page 14, Line 15.
  One rate for all statuses; no surtax, no recapture found.
- **Standard deduction**: PDF page 14 chart (12,750 / 25,500 / 12,750 or 0 for married separate / 19,125) and
  the same amounts in the filing requirements chart, PDF page 6. No age 65 or blind amount (page 14 says so).
  No personal or dependent exemption found in the booklet.
- **Retirement reliefs**: Bailey (Line 20) and Uniformed Services (Line 21) have no cap, no age test and no
  income test printed; read on the instruction pages 18-19 and the form lines on Schedule S page 3. No general
  retirement, IRA, private pension or age exclusion found in the booklet or on Schedule S.

## Projection

- Brackets 4.25% from 0; base federal AGI less the NC standard deduction (per return, every status as printed).
- Social Security exempt; railroad retirement modelled as `exempt_in_full` from `ss_rrb_subtraction`
  (Social Security left to the top-level treatment so it is not subtracted twice).
- `not_modelled`: Bailey, both branches (`warn_when: has_pension`; vesting or contributions before
  1989-08-12 are not known to a projection); Uniformed Services Line 21 (`warn_when: has_military_pension`;
  20 years of service or medical retirement is not known); child deduction (`has_dependents`); US obligation
  interest (`never`, with an approximation, as for Michigan).
- Approximations: government and military retirement taxed (overstates), itemizing not modelled (overstates),
  standard deduction applied where the booklet makes it zero (understates), child deduction left out
  (overstates), Treasury interest taxed (overstates), all tax-exempt interest treated as other-state when bonds
  can't be told apart (overstates), federal AGI as of January 1, 2023 (either).
- Indexing: brackets and deductions `indexed: false, assumed: true` (the booklet says nothing).

## Validator

```
data/states/2025/NC.record.json: ok
data/states/2025/NC.projection.json: ok
```

## Unsure

- Municipal interest: settled from how the lines work, not from a sentence that says NC's own interest is
  exempt. A reviewer may prefer `other`.
- Military pension under Bailey: listed in `bailey_defined_benefit` because Line 20 says US government
  retirees "including military", but the plans the booklet lists by name are civilian; whether military
  retired pay counts as a defined benefit plan "such as" those is not spelled out.
- Line 21 Survivor Benefit Plan payments are covered as `military_pension`; a projection may hold them as an
  annuity to the survivor.
- Uniformed Services Line 21 as `not_modelled`: most military retirees likely meet the 20-year or medical test,
  so a projection that leaves it out will overstate tax for many military retirees; modelling it with
  `needs_input: ["pension_source"]` would be the other choice, but the service test is still not a known fact.

## 2026-11-07: maintainer decision

**Decision** (docs/decisions.md, "2026-11-07: maintainer decisions on NC military retirement and 401(k)/IRA
coverage in GA, HI, MS"): the projection assumes every military pension meets the Uniformed Services
retirement deduction's service test and deducts it in full. This is an maintainer assumption, not a booklet rule.

**Sources.** 2025 D-401 instructions, PDF pages 18-19, Schedule S Part B Line 21: a retired member of the
Uniformed Services or an eligible beneficiary may deduct "Uniformed Service retirement payments received by a
retired member who served at least 20 years in the Uniformed Service or who was medically retired" (not
severance under 10 U.S.C. Chapter 61), and Survivor Benefit Plan payments to a beneficiary of such a member;
PDF page 19: retirees who deducted retirement income on Line 20 under Bailey "may not deduct the same
retirement income on Line 21". PDF page 18, Line 20: Bailey covers US government retirees "including
military" with five or more years of creditable service as of August 12, 1989. Form D-400 Schedule S page 3,
Line 21. PDF page 3 ("What You Should Send Us"): DD-214, 1099-R or similar proof of service for a Line 21
claim. Rate 4.25%: PDF page 7 and page 14, Line 15.

**Layer 1 (record): unchanged.** The record already holds Line 21 as the booklet prints it
(`uniformed_services_retirement`: covers `military_pension`, the 20-year-or-medical test, the Survivor Benefit
Plan branch and the Bailey line in `who.other_conditions`, Chapter 61 severance in `not_covered`,
`cannot_combine_with` both Bailey entries, cited PDF pages 18-19 and Schedule S page 3). No figure or text
changes, so the record's sha256 and the projection's `record.sha256` are unchanged.

**Layer 2 (projection): what changed.**
- New relief `uniformed_services_retirement` (from `uniformed_services_retirement`): `exempt_in_full`, covers
  `military_pension`, `needs_input: ["pension_source"]`, `who.basis: each_person`, no cap, no age or income test
  (none printed). Survivor Benefit Plan payments are deducted when the household holds them as a military
  pension. No `cannot_combine_with`: the Bailey entries are not projection reliefs (still `not_modelled`), so
  the same income cannot be deducted twice in the projection.
- Approximation added (understates_tax): "Maintainer assumption (decision 2026-11-07), not a booklet rule: every
  military pension is assumed to meet the Schedule S Line 21 test ... and is deducted in full, per person ...";
  it also says a military retiree vested for Bailey before 1989-08-12 gets the same result either way (the
  pension is deducted once, in full). Size: 4.25% of the pension, 1,275 a year on 30,000, for a retiree with
  under 20 years, no medical retirement and not vested for Bailey; none otherwise.
- Approximation rewritten (overstates_tax): the Bailey one no longer says military retirement is taxed; it now
  says NC state, NC local and US government civilian benefits (and the state's 401(k) and 457 plans) are taxed,
  and that military retired pay is deducted under Line 21. Size unchanged (1,275 a year on a 30,000 pension).
- Warning marker: the `not_modelled` entry for `uniformed_services_retirement` is kept with
  `warn_when: has_military_pension`, its text rewritten to say the relief IS modelled on the maintainer assumption,
  what the booklet's test is, and what a retiree who fails it owes (4.25% of the pension). It fires for any
  household with a military pension (code `state_rule_not_modelled:uniformed_services_retirement`). Same
  pattern as California's Survivor Benefit Plan marker on its modelled military exclusion.
- Bailey `not_modelled` text: one sentence added that military retired pay is not affected (deducted under
  Line 21), with the same result as Bailey for a military retiree vested before 1989-08-12.

**In dollars.** A military pension of 30,000 now lowers NC tax by 1,275 a year (4.25%). The existing check
`nc_2025_military_pension_not_modelled` (joint, military pension 45,000, wages 30,000) goes from NC taxable
income 49,500.00 and tax 2,103.75 to 4,500.00 and 191.25 (the booklet's own result, since that retiree served
22 years). For a retiree with under 20 years and no medical retirement, not vested for Bailey, the projection
now understates tax by 1,275 a year on 30,000 (before, every military retiree's tax was overstated by that
amount).

**Format gaps.**
- A modelled relief cannot carry a warning, and `warn_when` lives only on `not_modelled`. The nearest existing
  marker is a `not_modelled` entry naming the same record id; its warning code reads
  `state_rule_not_modelled:uniformed_services_retirement` although the relief is applied. The format has no
  marker kind for "modelled on an assumption"; the `what` text says so in words.
- No input for "years of service at least 20 or medically retired" (or Survivor Benefit Plan versus retired
  pay); the decision notes such an input would be a change for the consumer, not the data.

**Checks affected** (`checks/2025/NC/`, not edited here):
- `nc_2025_military_pension_not_modelled`: expected figures change (49,500.00 / 2,103.75 become
  4,500.00 / 191.25, relief amount 45,000.00); `tests` should name `uniformed_services_retirement`; its
  `accepted_approximations` quotes the old Bailey text; its warnings are unchanged.
- `nc_2025_bailey_nc_pension_not_modelled`: figures unchanged (an NC public pension, still taxed); its
  `accepted_approximations` quotes the old Bailey text, which no longer exists.
- `uv run python -m tools.checks --year 2025 --state NC` now reports one problem: relief
  `uniformed_services_retirement` has no case.

**Validator**

```
data/states/2025/NC.record.json: ok
data/states/2025/NC.projection.json: ok
```

**Unsure.** Superseded: the earlier "Unsure" item on leaving Line 21 `not_modelled`. Still open: whether a
projection holds Survivor Benefit Plan payments as a military pension or as an annuity (if as an annuity, they
are taxed, overstating tax by 4.25% of them, and the marker does not fire).

- Main session, 2026-11-07 (format v1): the assumption now sits on the relief (`reliefs.uniformed_services_retirement.assumption`, warn_when has_military_pension), so the warning code is `state_assumption:uniformed_services_retirement`. The stand-in not_modelled marker is gone; the approximation text, which the assumption repeats, now states the cost too. Closes the Format gap noted above.

## 2026-11-08: marker ids and indexing covers

- Marker ids: all 3 markers have an `id`. Each takes its first from_record id, so warning codes are unchanged.
- Indexing covers: `brackets` covers brackets; `deductions` covers deductions. No split needed.
- Assumed entries: searched the archived sources (docling, pypdf and page text) for indexed, inflation, cost of living, adjusted annually and consumer price index, and for statements that figures are fixed; nothing says, so every `assumed: true` stays.
