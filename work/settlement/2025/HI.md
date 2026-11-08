# Settlement: Hawaii, tax year 2025

- Readings: `work/extract/2025/HI.r5.A.json`, `work/extract/2025/HI.r5.B.json` (round r5)
- Sources: `sources/archive/2025/HI/` (2025 Form N-11 Instructions `n11ins`; 2025 Form N-11 `n11_f`)
- Outputs: `data/states/2025/HI.record.json`, `data/states/2025/HI.projection.json`
- Settled: 2026-11-07. Page numbers are PDF pages of `n11ins.pdf` unless the form is named.

## Comparison

`uv run python -m tools.compare` reported **29 structured differences** (112 wording differences). They
come down to three disagreements. Both readers recorded the same brackets, deductions, Social Security,
municipal interest, capital gains rate, reserve pay and Treasury interest entries.

| # | Lines | Field | A | B | Booklet | Settled | Decided by |
|---|---|---|---|---|---|---|---|
| 1 | 18 (5 relief keys) | Line 13 pensions: how the entries are split, and what each covers | 2 entries. Public: `public_pension`, `public_pension_other_state`, `military_pension`, with `roth_conversion` unclear. Private: `private_pension`, with `employer_plan_distribution`, `ira_distribution`, `roth_conversion` unclear | 3 entries. Public: `public_pension`, `military_pension`, with `public_pension_other_state` unclear. Private: `private_pension`, `employer_plan_distribution`. Rollover IRA: `ira_distribution`, `roth_conversion` | Page 13, Line 13. Item (1): "Pension or annuity distributions from a public (i.e., government) retirement system (e.g., federal civil service annuity, military pension, state or county retirement system), unless voluntary contributions were made by an employee under an elective right." The opening paragraph names "an employer-funded profit sharing, defined contribution, or defined benefit plan". Nontaxable Rollover IRAs example: "the amount rolled over to the Roth IRA is exempt from Hawaii's income tax." | 3 entries, as B split them. Public: `public_pension`, `public_pension_other_state`, `military_pension` (A's covers, see below). Private: `private_pension`, `employer_plan_distribution`. Rollover IRA: `ira_distribution`, `roth_conversion`. No `covers_unclear` anywhere. | booklet |
| 2 | 8 (1 relief) | Individual housing account deduction (line 16) | a subtraction covering `all_income`, capped at 5,000, or 10,000 joint | in notes only | Page 14, Line 16: a deduction for "cash ... paid ... into a trust account which is established for saving for a down payment on your first principal residence" | Dropped from reliefs. It is a deduction for a contribution, not relief for a kind of income (New York's 529 deduction was dropped for the same reason). Kept in a note. | brief (scope) |
| 3 | 3 | Indexing entries | `all_other` only | `brackets`, `standard_deduction`, `personal_exemption` and `all_other`, each `not_stated` | Nothing on indexing of these figures. Page 14 says only that the student loan interest and adoption benefit ranges "will not be adjusted for inflation". | One `all_other: not_stated` entry. Extraction brief rule 8: an entry per figure only where the booklet says something about it. | brief (booklet silent) |

**18 of the 29 lines were decided from the booklet** (row 1). The other 11 were decided by the brief:
8 lines on scope (row 2) and 3 lines where the booklet is silent (row 3).

### Row 1 in detail

- **Another state's government pension: in `covers` (A), not `covers_unclear` (B).** Item (1) on page 13
  tests what kind of payer it is (a public, government retirement system). It does not say which
  government. Its examples are "federal civil service annuity, military pension, state or county
  retirement system", with no "Hawaii" before "state". When the booklet means Hawaii's own plans it names
  them: "section 457 plans like the State of Hawaii Deferred Compensation Plan" (page 13), and "State or
  County employees who are in the contributory or hybrid plan of the Employees Retirement System" (page 11,
  Line 8). The booklet prints no reciprocity rule and names no paying state, so there is no `paying_states`
  list. The Other State and Foreign Tax Credit Worksheet (page 35, line 3) also says "Do not include any
  income that is exempt in Hawaii such as employer-funded pensions" in out-of-state income. That is
  consistent with this reading but does not prove it. I chose the reading printed most directly: B's
  `covers_unclear` would add a limit the sentence doesn't contain.
- **New York State pension.** A Hawaii resident's New York State pension comes from a state retirement
  system. It is exempt in full on line 13, unless it comes from "voluntary contributions ... made by an
  employee under an elective right" or is an early distribution subject to the 10% federal penalty.
- **Hawaii's own and federal government pensions, and military retirement.** All three are exempt in full
  on line 13 under item (1), with the same exceptions. No cap, no age test and no income test are printed.
  They stay in one entry because the booklet gives them one rule.
- **Roth conversions.** A had `roth_conversion` as unclear on both pension entries. The booklet settles
  it with its two rollover examples (page 13). A conversion of a rollover IRA that holds a qualifying
  employer-funded retirement distribution is exempt. A conversion of money from a distribution "upon
  separation from service before retirement" is taxable. So `roth_conversion` is covered by the rollover
  IRA entry only. A conversion of a self-funded IRA gets no subtraction: it is in federal AGI and no line
  removes it.
- **IRA distributions.** IRAs you fund yourself "are considered to be your own investments", and their
  distributions "may be fully or partly taxable, depending on whether your IRAs include deductible or
  nondeductible contributions" (page 13, Annuity Plans). No relief applies to them. Only a rollover IRA
  that continues a qualifying plan is exempt (B's entry, a one-sided entry kept: the booklet prints it and
  it is retirement income).
- **Employer-plan distributions.** These are in the private entry's `covers` (B), because the line 13
  opening names "employer-funded profit sharing, defined contribution" plans. Deferred compensation plans
  (401(k), SARSEP, Thrift Savings Plan, 457) "may be partly or fully taxable", and hybrid plans use
  Schedule J. Both go in `not_covered`, and the employer-funded test goes in `other_conditions`.
- **Private pensions.** Exempt when received upon retirement and the employee did not contribute.
  "Partially taxed by Hawaii if the employee contributed" (Schedule J figures the taxable part, and the
  booklet doesn't print the fraction, so no `share`). RMDs at 73 under the federal payout rule qualify.
- **`form`.** A wrote `subtraction` for every line 13 entry. B wrote `subtraction` for line 13 and
  `exempt_in_full` for line 14. I used `exempt_in_full` for every uncapped full exclusion: lines 13 and 14,
  and the line 18 Treasury interest. The capped reserve pay exclusion stays a `subtraction`.

## Capital gains: the 7.25% alternative tax (both readers: `own_rate`)

Page 21: "If you have a net capital gain, you may be able to reduce your tax using the Tax on Capital Gains
Worksheet ... if your taxable income is over $48,000 ($24,000 for Single, and Married Filing Separately;
or $36,000 for Head of Household)." On the worksheet (page 35):

- line 13 is the greater of (taxable income less the gain) or 24,000 / 36,000 / 48,000;
- line 16 is "Multiply line 14 by 7.25%";
- line 19 is "Enter the smaller of line 17 or line 18", so the tax is the smaller of the worksheet tax and
  the schedule tax.

- **Layer 1:** `treatment: other`, `value: 0.0725`, with the worksheet mechanics in `condition`.
  `own_rate` would tell a consumer the gains pay 7.25%. Below the 7.6% band that would be more than the
  schedule takes, and the booklet never charges more. This follows Maryland's settlement, which also
  rejected `own_rate` for a gain rule that isn't a plain replacement rate. The two readers agreed here, so
  this is a schema judgement, not a disagreement between readings. It is logged in the record notes.
- **Layer 2:** the projection's `capital_gains` field can hold only a fixed `extra_rate`, a
  `deduction_share` or `exempt`. A smaller-of cap can't be written as any of these. A negative extra rate
  would be wrong in the lower bands and needs a figure the record doesn't print. So:
  - `capital_gains` is empty, and gains run through the brackets.
  - A `not_modelled` marker (`warn_when: always`, since the schema has no gains-based warning).
  - An approximation, `overstates_tax`. Example: a single filer with 400,000 of taxable income including
    100,000 of long-term gain. Schedule tax is 34,216; worksheet tax is 23,466 + 7,250 = 30,716. Tax is
    overstated by 3,500. The overstatement is small or nothing when the gain falls in the 7.6% band or
    lower.

## One-sided entries

- Rollover IRA entry (B only): kept (row 1).
- Individual housing account (A only): dropped (row 2).
- Indexing `brackets`, `standard_deduction`, `personal_exemption` (B only): dropped (row 3).
- B's `not_covered` "Tier 2 railroad retirement: not stated": moved to notes. It is "not found", which is
  different from "does not qualify" (extraction brief rule 1).
- A's `covers_unclear: roth_conversion` on the public entry: dropped (row 1).
- A's notes on the line 8 ERS wage addback and the itemized-deduction limit: kept as notes.

## Facts checked against a second line or document

- **Social Security: exempt.** Page 13, Line 14: "Hawaii does not tax Social Security or first tier
  Railroad Retirement Act benefits." Form N-11 page 2, line 14, "Social security benefits taxed on federal
  return", is a subtraction. Tier 2 railroad retirement: not found.
- **Retirement reliefs.** Read on page 13 (every heading of Line 13) and on the form, line 13 "Pensions
  taxed federally but not taxed by Hawaii". No cap, age test or income test is printed for any pension
  branch. There is no age-based retirement deduction; the only age relief is the extra 1,144 exemption at
  65.
- **Brackets: 12 bands for every printed schedule** (page 50): Schedule I single and married filing
  separately, II joint and qualifying surviving spouse, III head of household. Checked against the Tax
  Table example row on page 38. At 23,250 to 23,300 the table prints 813 single, 399 joint and 524 head of
  household, and the schedules give the same at 23,275 (for joint, 269 + 3.2% of 4,075 = 399). No surtax
  and no recapture found.
- **Standard deduction.** 4,400 single and married filing separately, 8,800 joint and qualifying surviving
  spouse, 6,424 head of household. Printed in the page 20 table, and form line 23 prints the same figures
  by filing-status box.
- **Exemptions.** 1,144 per exemption on line 6e (page 20; form line 25, "Multiply $1,144 by the total
  number of exemptions claimed on line 6e"). The age-65 boxes on 6a and 6b each add one exemption (form
  page 1; page 9, "age 65 or over as of January 1, 2026"). The disability exemption is 7,000, in lieu of
  the regular and age-65 exemptions, and its maximum table on page 20 agrees with 1,144 for age 65
  (9,288 - 8,144).
- **Municipal interest.** Other states' bonds are added on line 9; Hawaii, Puerto Rico, U.S. Virgin
  Islands, Guam and American Samoa bonds are not (page 11; form line 9).

## Projection (`HI.projection.json`)

- **Brackets:** all four schedules as printed. **Base:** federal AGI, less the standard deduction (per
  return, every status), the 1,144 personal exemption per person, and 1,144 more per person aged 65 or
  over.
- **Social Security:** exempt. **Reliefs:**
  - public pensions, covering `public_pension`, `public_pension_other_state` and `military_pension`
    (`needs_input: pension_source`);
  - private pensions, covering `private_pension` (`needs_input: pension_source`);
  - railroad retirement, `exempt_in_full` from the line 14 entry. Social Security is left to the
    top-level treatment so it isn't subtracted twice.
- **`not_modelled`:**
  - the capital gains alternative tax (`always`);
  - the employer-funded part of employer-plan distributions (`always`);
  - rollover IRAs, distributions and conversions (`always`);
  - dependent exemptions (`has_dependents`);
  - the disability exemption, reserve and guard pay, and Treasury interest (`never`).
- **Approximations:**
  - gains alternative tax not applied (overstates);
  - employer-plan distributions taxed in full (overstates);
  - rollover IRAs taxed (overstates);
  - contributory private pensions exempt in full (understates). `pension_contributory` is defined for
    public plans only;
  - early-penalty and elective-contribution distributions exempt (understates);
  - Tier 2 railroad exempt (understates);
  - itemizing not modelled (overstates);
  - married filing separately when the spouse itemizes (either);
  - dependents left out (overstates);
  - Treasury interest taxed (overstates);
  - reserve pay taxed (overstates);
  - all exempt bonds treated as other-state (overstates);
  - the January 1 age-65 test (either).
- **Indexing:** brackets and deductions `indexed: false, assumed: true`. **No derived figures.**

## Validator

```
data/states/2025/HI.record.json: ok
data/states/2025/HI.projection.json: ok
```

## Unsure

- **Other states' government pensions as covered.** This rests on the generic words "a public (i.e.,
  government) retirement system" and "state or county retirement system". The administrative rule the
  booklet cites (section 18-235-7-02, HAR) is not in the sources and could narrow it. A reviewer who reads
  "state or county" as Hawaii's would prefer B's `covers_unclear`.
- **Voluntary contributions under an elective right.** The booklet doesn't define them. I read them as
  optional extra contributions, not the mandatory contributions of a contributory plan (Line 8 shows
  Hawaii's contributory ERS plan is taxed up front through wages). If a mandatory contributory plan
  counted, contributory government pensions would be taxable.
- **`employer_plan_distribution` in the private entry's covers.** It is right for employer-funded profit
  sharing and DC plans, but most 401(k) money is deferred compensation, which "may be partly or fully
  taxable". The projection therefore leaves the kind out of the relief. That departs from "covers exactly
  as the record has it" and is recorded as an approximation.
- **Capital gains `treatment: other`.** This changes a value both readers agreed on (`own_rate`). It is a
  schema-semantics call, not a reading of the booklet.
- **Three `warn_when: always` markers** (gains, employer-plan, rollover IRA) are noisy. The schema has no
  gains-based or IRA-origin warning.

## 2026-11-07: maintainer decision

Carries out the maintainer decision in `docs/decisions.md` ("maintainer decisions on NC military retirement and
401(k)/IRA coverage in GA, HI, MS", Hawaii bullet): the employee-funded part of a retirement distribution
is taxable in Hawaii; the employer-funded part is excluded.

### Sources added (`sources/archive/2025/HI/`, PDF page numbers from the `*.pypdf.txt` markers)

- `98ann02a.pdf`: Department of Taxation amendment to HAR 18-235-7-03, Exclusion of pension income,
  adopted 1997-08-12, effective 1998-01-01 (page 5). It amends subsection (c), the definitions:
  - page 2: "by reason of retirement, disability, or death" (excludes separation from service before
    retirement and early distributions under IRC 72(t)); "employer contribution" begins, and "does not
    include any amounts included in pretax employee contribution or previously taxed contribution";
  - page 3: employer contribution excludes amounts contributed "under an elective right"; "'Exclusion
    ratio' means the ratio described in subsection (e)(1)"; a "pension" "(4) Is attributable to employer
    contribution";
  - pages 3 and 4: "pretax employee contribution" is "voluntary contributions made by the employee under
    any elective right", naming IRAs "to which an employer does not contribute (see subsection (d)(2) for
    rollover individual retirement accounts)", IRC 401(k), 408(k)(6) (SEP salary reduction) and 457 plans,
    "even though the IRC may provide that the amounts are considered employer contributions";
  - page 4: "previously taxed contribution" (included in Hawaii gross income, or would not have been
    includable had the employee been a Hawaii resident paid the amount directly).
- `2026-07-14-Karacaovali_Presentation-Pension_Income_Taxation.pdf` (Department of Taxation, Tax Review
  Commission): page 2, exempt if "Funded entirely by the employer"; private defined-benefit pensions
  qualify "provided the employer funded them and the employee made no contributions"; page 3, ERS employee
  contributions are taxed up front; page 4, "Traditional IRA or 401(k) withdrawals, Portions of pensions
  funded through employee contributions, are fully taxable in Hawai'i".

### What changed

**Record (layer 1).** No `covers` changed. The task asked to resolve `covers_unclear` items on the pension
entries; the settled record had none (round r5 settlement moved every one out on booklet page 13), so
there was nothing to move. What the booklet left open was in text: deferred compensation "may be partly or
fully taxable" and contributory private plans "partially taxed" (Schedule J, not printed). Now:
- `hi_private_pension_exclusion`: the contributory-plan and deferred-compensation `not_covered` items cite
  HAR 18-235-7-03 (98ann02a pages 3 and 4: 401(k), 408(k)(6) and 457 contributions are pretax employee
  contribution, so the deferral part is taxable; only the employer-funded part, match or profit sharing, is
  excluded) and the presentation page 4. The `other_conditions` employer-funded test now states the
  exclusion ratio (pages 2 to 4). `employer_plan_distribution` stays in `covers`: the employer-funded part
  of a defined contribution plan is covered, in its ratio.
- `hi_rollover_ira_exclusion`: self-funded IRAs cite 98ann02a pages 3 and 4 and presentation page 4; new
  `other_conditions` line: a rollover IRA keeps the character of the money rolled in (booklet page 13),
  rolled-in 401(k), 457 or SEP deferrals stay taxable (98ann02a page 4).
- `hi_public_pension_exclusion`: 457 deferrals are pretax employee contribution (98ann02a page 4); the
  elective-right condition cites the rule's definitions (pages 3 and 4).
- Notes 8, 9, 10 (private pensions, employer plans, IRAs) extended with the rule's text; a new settlement
  note records the decision and that subsection (e)(1) is not printed in the amendment.

**Projection (layer 2).** No relief, cover, deduction or rate changed; `record.sha256` updated.
- `hi_private_pension` covers `private_pension` only, as before. Consistent with the rule: a private
  defined benefit pension wholly funded by the employer is excluded in full. A contributory one is also
  treated as fully excluded (understates), because `pension_contributory` is defined for public plans only.
- `employer_plan_distribution` and IRA distributions and Roth conversions stay taxed.
- `not_modelled` texts rewritten (same `from_record` first ids and `warn_when: always`, so the warning
  codes in the cases are unchanged): the `hi_private_pension_exclusion` marker now states the exclusion
  ratio of HAR 18-235-7-03, both directions (employer plans overstated, contributory private pensions
  understated); the `hi_rollover_ira_exclusion` marker states the rollover-character rule.
- Approximations rewritten, with dollar examples at Hawaii rates:
  - employer-plan distributions taxed in full, overstates: 401(k) funded by a 6% deferral and a 3% match
    (ratio one third), 30,000 withdrawn by a single filer on top of 60,000 of other taxable income:
    10,000 excludable at 7.6% = **760 a year** (1,100 at 11%);
  - IRA distributions and conversions taxed, overstates: the booklet's 50,000 conversion of a rollover from
    an employer-funded profit-sharing plan, joint filers with 100,000 of other taxable income, 7.6% =
    **3,800**; a rollover of the one-third-match 401(k), about 1,267; nothing for self-funded IRAs;
  - private pension excluded in full, understates: 30,000 private defined benefit pension, employee made
    20% of the contributions (ratio 0.8), about 6,000 taxable, single filer with 50,000 of other taxable
    income, 7.6% = **about 456 a year**.

### What it means in dollars

Nothing changes in any computed figure: the projection taxes and excludes the same income as before. The
change is that the overstatement for 401(k)/457/IRA money is now bounded by the rule (the employer-funded
share only; zero for employee deferrals and self-funded IRAs), and the understatement for contributory
private pensions is stated with a size.

### Checks (`uv run python -m tools.checks --year 2025 --state HI`)

`HI: 11 case(s), ok`. No case's expected figures change: no relief, cover or rate changed, and the
not_modelled markers keep their first `from_record` ids and `warn_when`, so `accepted_warnings` are
unchanged. No coverage problems reported.

### Format gaps

- No `warn_when` for "has an employer-plan distribution" or "has an IRA distribution or Roth conversion",
  so the employer-plan and rollover IRA markers stay `always` (they fire for a wage earner with no
  retirement accounts).
- No household input for a plan's employer-funded share (exclusion ratio) or an IRA's rollover origin; a
  relief `share` is a fixed figure in the record, and the ratio differs by plan.
- `pension_contributory` is defined only for public pensions, so a contributory private
  pension cannot be asked about; it is excluded in full with an approximation.
- One marker per record id is the effective warning code (`state_rule_not_modelled:<first id>`), so the
  private-pension marker carries both the overstating (employer plans) and understating (contributory
  private pension) cases in one text.

### Unsure

- **The ratio's formula.** The archived amendment prints only subsection (c). It names the exclusion ratio
  ("the ratio described in subsection (e)(1)") and defines its three amounts, but (e)(1) itself, and the
  rollover IRA rule in (d)(2), are not in the sources. "Employer contributions over employer plus pretax
  employee plus previously taxed contributions" is the maintainer decision's reading; the presentation (pages 2
  and 4: employee-funded portions "fully taxable") and the booklet ("partially taxed" if the employee
  contributed) agree with a pro rata rule.
- **401(k) employer match.** The presentation calls "401(k) withdrawals" fully taxable without exception,
  while the booklet sends a 401(k) with an employer match to Schedule J and the rule excludes employer
  contributions. The projection taxes 401(k) money in full either way; the approximation says the
  overstatement may be less than the example.
- **Previously taxed contributions** (for example Hawaii ERS contributions taxed up front, presentation
  page 3) sit in the ratio's denominator; how Hawaii treats the part of a payout attributable to them is in
  subsections not archived. Government pensions stay exempt in full on booklet item (1) and presentation
  page 2, so the projection is unaffected.

- Main session, 2026-11-07 (format for the first frozen schema): the capital gains alternative tax marker warns on has_long_term_gains; the exclusion ratio marker warns on has_retirement_account_distribution, with a copy on has_pension for contributory private pensions; the rollover IRA marker warns on has_retirement_account_distribution. All three warned on every run before.

## 2026-11-08: marker ids and indexing covers

- Marker ids given: first from_record id (warning code unchanged): `hi_capital_gains_alternative_tax`, `hi_rollover_ira_exclusion`, `dependent_exemption`, `disability_exemption`, `hi_military_reserve_pay_exclusion`, `hi_federal_obligation_interest`; descriptive: `hi_employer_plan_exclusion_ratio` (the exclusion-ratio marker that warns on account distributions); `hi_private_pension_exclusion_ratio` (the same rule's marker that warns on pensions; both started with hi_private_pension_exclusion, so their codes had collided).
- Indexing covers: `brackets` -> `brackets`; `deductions` -> `deductions`.
- Every `assumed` answer was checked again against the archived sources (searched for indexed, inflation, cost-of-living, adjusted annually, each year, CPI, fixed): none says, so all stay `assumed: true`. The N-11 instructions say only that the student loan interest and adoption benefit ranges are not adjusted for inflation (PDF page 14); those figures are not in the projection.
- `tools.checks --fix-warnings` updated the cases' accepted_warnings where a code changed; nothing else in the cases changed.
