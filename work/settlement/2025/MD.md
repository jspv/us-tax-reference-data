# Settlement: Maryland, tax year 2025

- Readings: `work/extract/2025/MD.r3.A.json`, `work/extract/2025/MD.r3.B.json` (round r3)
- Sources: `sources/archive/2025/MD/` (2025 Resident Booklet; Form 502; Form 502R)
- Outputs: `data/states/2025/MD.record.json`, `data/states/2025/MD.projection.json`
- Settled: 2026-11-07

## Comparison

`uv run python -m tools.compare` reported **37 structured differences** (132 wording differences). Every
one is one-sided at the key level (one reader has the key, the other `<missing>`), because the two readers
keyed the same rule differently. Taken together they are eight disagreements:

| # | Lines | Field | A | B | Source | Settled | Decided by |
|---|---|---|---|---|---|---|---|
| 1 | 7 | `dependent_exemption.phase_out` | none | Chart 10A, effect `other`, thresholds 100,000 / 150,000 | PDF page 12, Chart 10A: "This reduction applies to the additional dependency exemptions as well" | kept, written as `effect: stepped` with the chart's steps (also on `dependent_age_65_exemption`) | booklet |
| 2 | 6 (2 keys x 3) | 2% capital gain tax | `applies_to: other`, `treatment: own_rate` | `applies_to: all_gains`, `treatment: other` | PDF page 21 Line 20a, page 22 Line 21b ("Multiply the amount on Line 20a by .02"), page 53 Lines 3b, 8a-8c (8c = 8a schedule tax + 8b): an additional tax on top of the schedule, on "certain net capital gain income", no short/long split | `all_gains`, `other`, 0.02; AGI over 350,000 and the exclusions in `condition`. Not `own_rate`: the gains still pay the schedule rate | booklet |
| 3 | 1 | `indexing` | `brackets` and `all_other`, both `not_stated` | `all_other` only | booklet searched for inflation, indexed, adjusted annually, cost of living: nothing | one `all_other: not_stated` entry | brief (booklet silent) |
| 4 | 3 | code a, fire/police job-injury pension payments | recorded (`other_income`) | absent | PDF page 16, code a: "Payments from a pension system to fire fighters and policemen for job related injuries or disabilities" | kept (printed, a pension rule); covers changed to `public_pension`, `private_pension` (a pension; the booklet doesn't say whose) | booklet |
| 5 | 2 | `two_income_subtraction.cap` | `married_joint: 1200` | `all: 1200` | PDF page 21 Line 14: "if both spouses have income subject to Maryland tax and you file a joint return" | `married_joint: 1200` | booklet |
| 6 | 6 | pension exclusion, disabled branch | separate entry `pension_exclusion_disabled` | one entry, disability in `other_conditions` | PDF page 15 Line 10a: "You were 65 or over or totally disabled, or your spouse was totally disabled" | A's two entries (one per branch), each `cannot_combine_with` the other and the ranger exclusion (FAQ 1, PDF page 7: one pension exclusion per individual) | brief (one entry per branch) |
| 7 | 1 | pension exclusion `covers_unclear` | `roth_conversion` | none | PDF page 15: IRAs don't qualify; conversions not named | `roth_conversion` in `covers_unclear` | brief (booklet silent) |
| 8 | 11 (2 keys) | military retirement under 55, `who.max_age` | 54 | none (test in `other_conditions`) | PDF page 17, code u: "Individuals under the age of 55 on the last day of the taxable year may subtract up to $12,500" | `max_age: 54` (age reached), condition kept in words | booklet |

Decided from the booklet: 29 of 37 lines (disagreements 1, 2, 4, 5, 8). The other 8 lines (3, 6, 7) are
settled by the extraction brief's rules where the booklet is silent or prints the branches plainly.

## Other decisions (not structured differences)

- **Rate schedules and the printed typo.** Both readers agree. Schedule I and II on PDF page 22 are
  printed again on PDF page 54 with the same figures; the cumulative amounts re-compute from the rates;
  tax table rows 20,000-20,050 = 899, 49,950-50,000 = 2,321 and 99,950-100,000 = 4,696 match the schedule
  at the midpoint. The Schedule I worksheet (17A) on PDF page 41 prints "At least $250,001 but not over
  $1,000,000" with subtraction 500,000.00, x .0625, addition 27,135.00: from its own subtraction and
  addition amounts and the schedule, the row is 500,001 to 1,000,000. Recorded 6.25% from 500,000. Logged in
  the record notes.
- **Personal exemption phase-out**: both readers used `effect: other` with the chart in words; rewritten as
  `effect: stepped`, 15 steps (single and married separate: 1,600 over 100,000, 800 over 125,000, 0 over
  150,000; joint, head of household, qualifying surviving spouse: 1,600 over 150,000, 800 over 175,000, 0 over
  200,000), `amount` per exemption. Chart on PDF page 12, repeated on PDF page 53.
- **Pension exclusion covers** (both readers: `public_pension`, `private_pension`, `annuity`,
  `employer_plan_distribution`): `annuity` removed. Line 10a qualifies only "a pension, annuity, or endowment
  from an employee retirement system" under 401(a), 403 or 457(b), and the Form 502R chart (page 2, row 7)
  marks "other taxable retirement income" as not qualifying, so a commercial annuity is out (added to
  `not_covered`). `public_pension_other_state` added: the booklet sets no Maryland-only limit on the qualified
  plan (unlike code v, which excludes other states' personnel).
- **Ranger exclusion `max_age: 64`** added (neither reader had it): Line 10b, PDF page 16, "You were not 65
  or older".
- **Code aa added** (neither reader): PDF page 19, pension-system payments and death benefits to survivors
  of law enforcement officers and firefighters killed on duty. A pension rule the brief's scope covers.
- **IDs**: A's ids kept throughout (`ss_rr_exempt`, `pension_exclusion_age_65`, `state_pension_pickup`,
  `age_100_income`, `us_obligations_income`, `dependent_age_65_exemption`, `additional_cap_gain_tax`).
- **Notes merged** from both readers, rewritten once; one `Settlement 2026-11-07:` line per decision.
- **Local income tax**: county and Baltimore City taxes (PDF page 25 chart, .0225 to .0330; Anne Arundel and
  Frederick brackets on PDF pages 4-5) are out of scope (tax-reference-data issue #1): a record note only,
  nothing in either file's figures.

## One-sided entries

- Code a (A only): kept, see row 4.
- Pension exclusion, disabled branch (A only): kept, see row 6.
- Indexing `brackets` (A only): dropped, see row 3.
- B's `cg_additional_2pct` / A's `additional_cap_gain_tax`: same rule, see row 2.
- B's `military_retirement_under_55` without `max_age` / A's with it: same rule, see row 8.
- B's phase_out on `dependent_exemption`: kept, see row 1.

## Facts checked against a second line or document

- **Social Security**: exempt. Instruction 13 Line 11, PDF page 16 ("Social Security and railroad retirement
  benefits are exempt from state tax"), and Form 502 page 2 Line 11 (subtracts the taxable SS and RR
  benefits in Line 1).
- **Pension exclusion**: 41,200 per person on Worksheet 13A (PDF page 14, line 2 and specific instructions),
  and again on Worksheet 13E (PDF page 18, "maximum Social Security benefit"). Reduced by that person's gross
  SS and RR (Tier I and II, taxable or not). Age 65 on the last day of the year, or totally disabled (self or
  spouse) (Line 10a, PDF page 15). Qualifying plans: Line 10a text and the Form 502R chart (401(a), 403,
  403(b), 457(b), 401(k), Thrift Savings, SIMPLE 401(k) yes; traditional, SIMPLE, rollover, Roth IRAs, SEP,
  457(f), Keogh, foreign, other no). FAQ 2, PDF page 7: "401(k) and 403(b) plans qualify ... an IRA does not."
- **Military (code u)**: 20,000 at 55+, 12,500 under 55, PDF page 17. **Public safety (code v)**: 15,000 at
  55+, PDF page 17. **Ranger (Line 10b)**: 15,000, 55-64, Worksheet 13E line 6, PDF pages 16 and 18.
- **Brackets**: every printed status (see above), pages 22, 41 and 54 and the tax table.
- **Standard deduction**: 3,350 / 6,700, Instruction 16 (PDF page 21) and the estimated tax instructions
  (PDF page 53, Line 4). No percentage, minimum or maximum printed.
- **Exemptions**: 3,200 (Chart 10A, PDF page 12; PDF page 53 Line 6), 1,000 age 65 and blind (Instruction 10,
  PDF page 13; Form 502 Exemptions Line B "X $1,000").

## Projection

- Brackets: Schedule I for single and married separate, Schedule II for joint and head of household
  (qualifying surviving spouse falls to married_joint by the schema's default). No surtax to fold.
- Base: federal AGI; standard deduction per return; personal exemption 3,200 per person with the stepped
  phase-out; 1,000 per person 65 or older (`min_age: 65`).
- Social Security exempt; `ss_rr_exempt` also exempts railroad retirement.
- Reliefs modelled: pension exclusion 65+ (41,200 per person, `cap_reduced_by` social_security and
  railroad_retirement, `needs_input: pension_source` because military pensions are treated differently);
  military 55+ (20,000) and under 55 (12,500, `max_age: 54`), both `needs_input: pension_source`; centenarian
  subtraction (100,000 per person, all income).
- `not_modelled`: 2% capital gain tax (`always`); pension exclusion for the disabled, ranger and public
  safety, fire/police injury and survivor payments, state pickup (`has_pension`); dependent exemptions
  (`has_dependents`); blind exemption, U.S. obligations, two-income subtraction (`never`).
- 2% capital gain tax: the projection's `capital_gains` can hold `all_gains` / `extra_rate` / 0.02 but has no
  AGI test, so charging it would overstate tax for every household at or below 350,000 of AGI. Left out, with
  an approximation (understates tax; 2% of the gain in a year AGI is over 350,000: 4,000 on a 200,000 gain).
- Approximations: 2% gain tax (understates), Roth conversions not covered (overstates), standard deduction only
  (overstates), dependents' exemptions (overstates, up to 152 per dependent), Treasury interest taxed
  (overstates), two-income subtraction (overstates, at most 57), centenarian income attribution (either),
  457(f) distributions inside `employer_plan_distribution` (understates).
- Indexing: brackets, deductions, relief caps `indexed: false, assumed: true`.
- No derived figures.

## Validator

```
data/states/2025/MD.record.json: ok
data/states/2025/MD.projection.json: ok
```

## Unsure

- Removing `annuity` from the pension exclusion's covers goes against both readers. It rests on "annuity ...
  from an employee retirement system" and the Form 502R row 7; a consumer that files employer-plan annuities
  under `annuity` would see Maryland tax overstated for them.
- `public_pension_other_state` in the pension exclusion is read from the absence of a Maryland-only limit on
  Line 10a, not from a sentence saying other states' pensions qualify.
- Code a covers `public_pension` and `private_pension`: "a pension system" is not said to be public; A had
  `other_income`. Not modelled either way.
- The 2% capital gain tax as `all_gains`: the booklet says "certain net capital gain income" and Form 502CG,
  which says which gains, is not in the sources. Whether short-term gains count is not printed.
- `warn_when: always` for the 2% gain tax is noisy; the schema has no AGI-based warning.
- The dependent 65+ exemption's phase-out rests on reading "the additional dependency exemptions" as including
  it; the booklet's "up to $3,200" supports that reading.

- Main session, 2026-11-07 (format v1): `social_security_basis: gross` set on the relief(s) whose cap Social Security reduces, stating what the cases already used.

## 2026-11-07: format v1 adoption

- **2% capital gain tax modelled.** The projection's `capital_gains` now holds `additional_cap_gain_tax`:
  `all_gains`, `extra_rate` 0.02, `applies_over` {federal_agi, `all` 350000, `over`}. The test is "more than
  $350,000 on Line 1" (booklet PDF page 21 Line 20a, PDF page 22 Line 21b; "in excess of $350,000", PDF page 4),
  so exactly 350,000 pays nothing. The `always` marker and the "not charged" approximation (understates tax)
  are gone.
- **Form 502CG is not in the archive** (`sources/archive/2025/MD/` holds the resident booklet, Form 502 and
  Form 502R only). The rule rests on the booklet's own text (PDF pages 4, 21, 22 and 53, Line 3b: "Net capital
  gain from the sale of certain assets is excluded from the surtax ... see Maryland Technical Bulletin No. 58").
  The booklet names no excluded asset, so the record cannot list the exclusions (a primary residence, for
  example, is not mentioned).
- **Record.** A record `capital_gains` entry has no threshold field and a projection may use only record
  figures, so the 350,000 is recorded as its own entry, `additional_cap_gain_tax_agi_threshold` (applies_to and
  treatment `other`, value 350000, condition saying it is a threshold, not a rate), cited to PDF pages 4, 21 and
  22; one `notes` line says why. The main entry's condition points to it.
- **What stays simplified.** New approximation (overstates tax): the 2% is charged on every gain, short- and
  long-term (Line 1c is federal Form 1040 Line 7a, both kinds), with no exclusion; the booklet doesn't say
  whether short-term gains count. A narrower `not_modelled` marker for the exclusions, `warn_when: income_over`
  federal AGI 350,000 (the schema's own Maryland example), replaces the `always` warning, so only households
  over 350,000 see it.
- **Dollar effect.** At or below 350,000 of federal AGI: none. Above it: tax rises by 2% of the net gain
  (100,000 gain: +2,000; joint return, wages 300,000 + 100,000 long-term gain: 20,437.25 before, 22,437.25 now).
  A gain that Form 502CG excludes is now overstated by 2% (300,000 excluded gain: 6,000), where before every
  gain was understated by 2%.
- **Checks.** Added `md_2025_cap_gain_2pct_agi_at_350000_joint` (below: AGI exactly 350,000, no 2%),
  `md_2025_cap_gain_2pct_agi_over_350000_joint` and `md_2025_cap_gain_2pct_short_and_long_single` (at or above).
  The other 23 cases kept their figures and `verified` blocks; `--fix-warnings` only dropped the old
  `state_rule_not_modelled:additional_cap_gain_tax` warning from them (all have AGI at or under 350,000).

```
data/states/2025/MD.record.json: ok
data/states/2025/MD.projection.json: ok
```

- Main session, 2026-11-07: the record schema now has `capital_gains[].applies_over`, so the 350,000 threshold moved onto `additional_cap_gain_tax` (cite kept) and the stand-in entry `additional_cap_gain_tax_agi_threshold` is gone.

## 2026-11-08: marker ids and indexing covers

- Marker ids given: first from_record id (warning code unchanged): `additional_cap_gain_tax`, `pension_exclusion_disabled`, `ranger_pension_exclusion`, `fire_police_injury_payments`, `state_pension_pickup`, `dependent_exemption`, `blind_exemption`, `us_obligations_income`, `two_income_subtraction`.
- Indexing covers: `brackets` -> `brackets`; `deductions` -> `deductions`; `relief_caps` -> `reliefs.cap`; `capital_gains_threshold` -> `capital_gains`.
- Added `capital_gains_threshold` (indexed false, assumed) for the 350,000 federal AGI over which the 2% capital gains tax applies.
- Every `assumed` answer was checked again against the archived sources (searched for indexed, inflation, cost-of-living, adjusted annually, each year, CPI, fixed): none says, so all stay `assumed: true`. The booklet's 'have been adjusted for taxable year 2025' note is about the refundable child and dependent care credit's FAGI limits, which are not in the projection. The ranger worksheet calls the 41,200 'the maximum Social Security benefit' (the same figure as the pension exclusion's cap), but nothing says the exclusion is adjusted each year, so `relief_caps` stays assumed.
- Warning codes unchanged (every id is the marker's first from_record id).

## 2026-11-08: indexing settled from statutes

- `brackets` (projection `brackets`): not_indexed, Tax-General 10-105(a)(1). Record `brackets` added as no.
- `deductions` (projection `deductions`): split, replaced by `standard_deduction` (`deductions:standard_deduction`, indexed from 2026, Tax-General 10-217(c): IRC 1(f)(3) with 2024 base, rounded down to 50; `indexed_from: 2026`), `personal_exemption` (`deductions:personal_exemption`, not_indexed, 10-211(b)(1), (c)) and `age_65_exemption` (`deductions:age_65_exemption`, not_indexed, 10-211(b)(3)). Record entries added for all three.
- `relief_caps` (projection `reliefs.cap`): split, replaced by `pension_exclusion_cap` (`reliefs:pension_exclusion.cap`, indexed: the Social Security maximum benefit at 65 for the prior year, Tax-General 10-209(b)(2), (c)), `military_retirement_55_plus_cap` (not_indexed, 10-207(q)(2)(ii)), `military_retirement_under_55_cap` (not_indexed, 10-207(q)(2)(i)) and `age_100_income_cap` (not_indexed, 10-207(nn)). Record `pension_exclusion_age_65` and `pension_exclusion_disabled` (same 10-209 cap) added as yes; the three fixed caps added as no.
- `capital_gains_threshold` (projection `capital_gains`): not_indexed, Tax-General 10-105(a)(4), 350,000. Record `additional_cap_gain_tax` added as no.
- The existing `all_other` entry (booklet searched, nothing said) is left.
