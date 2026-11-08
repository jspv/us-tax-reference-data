# Settlement: Idaho, tax year 2025

- Readings: `work/extract/2025/ID.r6.A.json`, `work/extract/2025/ID.r6.B.json` (round r6)
- Sources: `sources/archive/2025/ID/` (2025 Individual Income Tax Instructions EIN00046, which holds Forms 40, 43,
  39R and 39NR as well; web pages "Idaho Retirement Benefits Deduction" and "Income Tax for Seniors and Retirees")
- Outputs: `data/states/2025/ID.record.json`, `data/states/2025/ID.projection.json`
- Settled: 2026-11-07

## Comparison

`uv run python -m tools.compare` reported **50 structured differences** (112 wording differences). They are four
disagreements:

| # | Lines | Field | A | B | Source | Settled |
|---|---|---|---|---|---|---|
| 1 | 42 (3 relief keys on each side x 7 fields) | Civil service, firefighter and police entries, `who.min_age` | 62, with 65 in other_conditions | 65, with 62 in other_conditions | PDF p.45 Part One: "The recipients must be at least age 65 or be classified as disabled and be at least age 62." | Two branches, as rule 3 asks: min_age 65 in each plan's entry, plus one `ret_disabled_62_to_64` entry (min 62, max 64, classified as disabled, the same plan list). Neither reader's shape: each hid a real branch in other_conditions |
| 2 | 2 | Age 65 and blind `qualifying_surviving_spouse` | missing | 1600 | PDF p.11 worksheet line 5: "$1,600 ($2,000 if single or head of household)" | 1600: every status other than single and head of household |
| 3 | 3 | U.S. government interest relief | recorded | notes only | PDF p.43 Line 3: "Idaho doesn't tax interest income you received from U.S. government obligations." | Kept |
| 4 | 3 | `indexing` entries | five entries | two entries | Web page: "Each year the state recalculates the maximum allowed" | See below: kept per figure, and the retirement maximum changed to `yes` |

Decided from the booklet: **47 of 50 lines** (#1, #2, #3). #4 (3 lines) was settled from the agency web page plus
PDF p.45, as the wording is only on the web page.

The compare tool keys entries on covers and age, so the 42 lines of #1 are one disagreement; the plan, cap and
cap_per of each entry agreed.

## One-sided entries and field choices

- `best_of_group` (A only): dropped. Line 8e is one total of qualifying benefits against one maximum; a filer with
  two qualifying plans adds them. It is not a choice. The sharing is in `cap_rule`.
- Retired service members: both wrote one entry. PDF p.45 lists three alternatives, so I split it: age 62 or older
  (`ret_service_member_62_plus`) and under 62 (`ret_service_member_under_62`, disabled or employed with enough
  income to file).
- Line 8 citation: A cited PDF p.34; Form 39R Part B line 8 is on p.33. Corrected.
- `age_65_addition` / `blind_addition` per `exemption_claimed`: both readers agreed. Kept.
- Dependent filer deduction: both recorded 1,350 as `other`. Kept. B's wording is the worksheet's: "Is your earned
  income more than $900? ... No. Enter $1,350"; A's "larger of" is equivalent.
- B's note "a 100-per-member credit in Form 39R Part F": dropped, it misreads the form. The 100 is Part E line 4,
  for a family member age 65 or older or with a developmental disability; Part F lists dependents.
- A's "Part One bar on married filing separately" for all entries of the plans: kept. For service members the booklet
  states no filing-status test (B said so, A's note agrees): recorded as printed.
- Railroad benefits: both had them with Social Security on line 7. Kept one entry, `exempt_in_full` (PDF p.44:
  "Exempt payments from the Railroad Retirement Board include ...").

**Added, neither reader recorded them** (rule 0: read the form as well as the instructions):

- `qbi_and_schedule_1a_deduction`: Form 40's line 18 is labelled only "Qualified business income deduction" (p.30),
  but the instruction (p.11) is headed "Qualified Business Income and Federal Schedule 1-A Deductions" and says "Add
  lines 13a and 13b from federal Form 1040 or 1040-SR and enter the total on this line." A noted line 18 as QBI only.
  The booklet does not say what Schedule 1-A holds; DC's booklet, in this repository's sources, names no tax on tips,
  overtime, car loan interest and the Enhanced Deduction for Seniors. That is a pointer for the reviewer, no figure
  from it is used.
- `health_insurance_premiums`: Form 39R Part B line 18 (p.48-49): "You can deduct the premiums for Medicare B, D, or
  both if you voluntarily enrolled." A said this line was not relevant to a retirement projection; for a retiree it is.
- `food_tax_credit`: 155 per person (p.4, p.13-14), the per-person amount Idaho has in place of an exemption. Same
  form as Delaware's and Arkansas's personal credits.
- `idaho_child_tax_credit`: 205 per child (p.12), recorded so the marker has an id.

Not recorded, in notes only: line 19 long-term care premiums, line 15 home for the aged (1,000 each, at most three),
the credit for tax paid to other states, and the 10 Permanent Building Fund tax (no field holds it; it is an
approximation in the projection).

## Facts checked

**(1) Another state's government pension, and New York State's.** Not found. Neither the booklet nor either web page
mentions a pension from another state's government, and "New York" is printed nowhere in the Idaho sources.
The list of qualifying benefits is closed: PDF p.45 "their qualified retirement benefits must be one of the
following", and it names only federal CSRS/FSRDS and Idaho funds. So `public_pension_other_state` is in no `covers`
and in no `not_covered` (the booklet doesn't say it in words), and the record's note says "not found in the booklet".
The general rule is the web page's: "By federal law, Idaho taxes your pension if you're an Idaho resident or part-year
resident." **A New York State pension is taxed in full by an Idaho resident at 5.3%.**

**(2) Idaho and federal government pensions.** Taxed, except the named plans. Web page: "Only a very few Idaho pensions
qualify for the deduction from Idaho income tax." Federal: "Retirement annuities paid to a retired federal employee
under the Federal Employees Retirement System (FERS) don't qualify for the deduction." (p.45). Idaho: "Benefits paid
out of the PERSI Base Plan don't qualify for the deduction." (p.46, under both the firefighter and police items).
Named plans: CSRS and FSRDS with "eligibility before 1984", PERSI Firefighters Retirement Fund, closed Idaho city
police funds. Military: its own test on line 8e.

**(3) Private pensions, IRA and employer-plan distributions, Roth conversions.** No relief. PDF p.6 lists "Pensions
and annuities" in gross income; the web page sentence above covers pensions. IRA and 401(k) money: no Idaho
subtraction names it; it arrives through federal AGI on Form 40 line 7. "Roth" is not printed in any Idaho source.

**(4) Social Security.** Exempt, on three documents: Form 39R Part B line 7 (p.33, p.44) "Deduct the portion of your
Social Security benefits ... that's taxable on your federal return"; Form 39NR Line 5 (p.56) "Idaho doesn't tax Social
Security or Social Security equivalent benefits"; seniors web page "While potentially taxable on your federal return,
these aren't taxable in Idaho." Gross benefits still reduce the retirement maximum (p.45 line 8c, Box 5).

**(5) Schedule, standard deduction, exemptions.** One rate, 5.3% (p.4). Worksheet (p.11 Line 20, the same for Form 43):
taxable income less 4,811 (single, married filing separately) or 9,622 (joint, head of household, qualifying surviving
spouse), times 5.3%. Recorded as a 0% band then 5.3%, as both readers did. No `brackets.derivation`: no tax table is
printed, 4,811 and 9,622 are printed themselves, and the formula field holds one constant while Idaho has two, neither
printed as a dollar constant. Standard deduction 15,750 / 31,500 / 23,625 on p.10 and on Form 40 p.30. Age 65 and
blind 1,600 (2,000 single or head of household) per box, p.11. No personal or dependent exemption found in the booklet
(Form 40 lines 11-19).

## Retirement deduction: what the projection does

The projection's pension inputs say a pension's source (public, private, military), its paying government (a state code
or `federal`) and whether it is contributory. None says which plan.

| Plan | Modelled? | Why |
|---|---|---|
| Military, age 62 or older | Modelled: `ret_service_member`, `needs_input: ["pension_source"]`, min_age 62, cap with `cap_reduced_by` Social Security and railroad | `pension_source: military` identifies it and age is known |
| Military, under 62 | `not_modelled`, `has_military_pension` | Disability and "sufficient income to file" are not known |
| CSRS, FSRDS | `not_modelled`, `has_pension` | The inputs show `public`, `federal`; a FERS annuity shows the same and does not qualify |
| Firefighters Retirement Fund, city police funds | `not_modelled`, `has_pension` | The inputs show `public`, `ID`; a PERSI Base Plan pension shows the same and does not qualify |
| Disabled, 62 to 64 | `not_modelled`, in both `has_pension` markers | Same plan facts, and disability |

Modelling `public_pension` would give every FERS and PERSI Base Plan retiree a deduction they can't take, up to 3,833
a year understated. These are the ordinary cases, and a pre-1984 CSRS retiree is the rare one, so the projection taxes
the named plans in full, warns any household with a pension, and says so in `approximations`, direction overstates_tax.

**How the three asked-about pensions run:**

- **PERSI Base Plan pension:** taxed in full. No relief applies. "Benefits paid out of the PERSI Base Plan don't
  qualify for the deduction." (p.46). The `has_pension` warning shows, and doesn't apply to them.
- **FERS annuity:** taxed in full. No relief applies. "Retirement annuities paid to a retired federal employee under
  the Federal Employees Retirement System (FERS) don't qualify for the deduction." (p.45). A mixed annuity (CSA-1099
  first digit 8) has a CSRS portion that may qualify; that portion is within the CSRS marker.
- **New York State pension:** taxed in full. No relief applies, and no marker is needed for it beyond the same warning.
  Not named anywhere; outside the closed list (p.45).

## Other projection choices

- `income_test.applies_when`: not used, because Idaho has no income test on a relief here. The retirement maximum
  falls by benefits received, which is `cap_reduced_by`, not a test. `all_income_scope: return` is set on the two
  all-income subtractions in the record; the projection models neither.
- Food Tax Credit modelled for filer and spouse, like Delaware's personal credit; dependents are `not_modelled`.
- Blind and dependent-filer amounts: `not_modelled`, `never`, as in AZ and DE.
- Treasury interest, Idaho bond interest, the 60% gain deduction: approximations and markers, as in AZ, GA and CO.
- Schedule 1-A marker is `always` because it can hit anyone: Form 40 takes the federal figure directly.
- Indexing: `relief_caps` true, not assumed; the other families false, assumed.

## Unsure

1. Indexing: both readers said `not_stated`; I set the retirement maximum to `yes`, because the state says it
   recalculates each year and p.45 prints the amounts "for 2025". The measure isn't stated, and the page doesn't say
   inflation. Reading the statute would settle it. If a reviewer holds to rule 8's wording, it reverts to `not_stated`.
2. Maximum for head of household, qualifying surviving spouse and married filing separately: not printed. Left out of
   both files. A consumer needs a fallback; the approximation says what I assumed (the brackets' fallback). For a
   military pension only.
3. Line 18 (Schedule 1-A) may be large for people 65 or older; the booklet prints no figure, so its size is unknown
   here. The Form 40 line label and the instruction differ; I followed the instruction.
4. Line 8e's disability definition is printed in Part One, under "all other retirees"; I read it as also defining
   "classified as disabled" for service members.
5. New York State pension "taxed in full" rests on a closed list and the general sentence; no source names another
   state's pension.
6. `cap_reduced_by` semantics: the projection field has no way to say "gross benefits received"; the approximation
   states it.

## 2026-11-07: format v1 adoption

- **Food Tax Credit is refundable** (`reliefs[].refundable`). Form 40 enters line 43 under
  "Payments and Other Credits" (PDF p.31; instructions p.13), adds it into line 50 with withholding, and line 55 pays out
  line 50 above line 41, the total tax. A person 65 or older whom Idaho does not require to file claims it on Form 24
  (p.14). A projection computes it from the persons on the return (155 each, filer and spouse), so `food_tax_credit` now
  has `refundable: true` and state tax can go below 0. Record: a notes line and the relief's cite (p.31 lines 43, 50, 55);
  no new figure. Dollar effect: up to 155 a person more for a household whose tax is under the credit (single, 22,000 of
  wages: tax 76.27, the projection now gives -78.73 instead of 0.00, 78.73 better; a single filer with no tax gets 155).
- **Approximation narrowed**: the Food Tax Credit entry keeps the actual-sales-tax choice (up to 95 a person) and the
  food stamp months (up to 155 a person), direction now `either` with a worked example; its "a credit that stops at zero
  tax loses it" sentence is gone because the refund is now exact. No approximation or marker was deleted outright; the
  dependents' credit stays in `not_modelled` (`has_dependents`).
- **Line 18 marker** (`qbi_and_schedule_1a_deduction`) stays `always`. None of the new triggers fits: the line takes the
  federal qualified business income deduction (business owners) and Schedule 1-A (tips, overtime, car loan interest and
  the senior deduction), which reach wage earners and people 65 or older alike, and no trigger names self-employment or
  wages.
- **Checks**: `id_2025_food_credit_below_single` (0.00 to -78.73), `id_2025_food_credit_below_joint` (0.00 to -51.47) and
  `id_2025_std_deduction_exceeds_income` (0.00 to -155.00) reworked: credits are the full worksheet figure, `relief_amounts`
  added, the old Food Tax Credit approximation dropped, `verified` removed for a new second working. Other cases have tax
  above the credit and are unchanged.
- Unsure: rule 5e says `credits` is limited to `state_tax_before_credits`; the check schema says a refundable credit's
  excess makes state income tax negative. I read the second as overriding the first for a refundable credit, so `credits`
  holds the full 155 each.

- Main session, 2026-11-07 (format v1): `social_security_basis: gross` set on the relief(s) whose cap Social Security reduces, stating what the cases already used.

## 2026-11-08: marker ids and indexing covers

- Marker ids given: first from_record id (warning code unchanged): `ret_csrs_fsrds`, `ret_idaho_firefighters`, `ret_service_member_under_62`, `qbi_and_schedule_1a_deduction`, `health_insurance_premiums`, `blind_addition`, `dependent_filer_standard_deduction`, `food_tax_credit`, `us_government_interest_subtraction`, `idaho_property_gain_deduction`.
- Indexing covers: `brackets` -> `brackets`; `deductions` -> `deductions`; `relief_caps` -> `reliefs.cap`; `credits` -> `reliefs.credit_amount`.
- Every `assumed` answer was checked again against the archived sources (searched for indexed, inflation, cost-of-living, adjusted annually, each year, CPI, fixed): none says, so all stay `assumed: true`.
- Warning codes unchanged (every id is the marker's first from_record id).

## 2026-11-08: indexing settled from statutes

- `brackets` (projection `brackets`): indexed, Idaho Code 63-3024(2)-(3): CPI-U over 1998. Record `brackets` (was not_stated with the booklet cite) -> yes with the statute cite.
- `deductions` (projection `deductions`): indexed, Idaho Code 63-3022(j)(1) and 63-3004 (federal standard deduction by reference). Record `standard_deduction` (was not_stated) -> yes; `age_65_addition` added as yes.
- `credits` (projection `reliefs.credit_amount`): not_indexed, Idaho Code 63-3024A(1). Record `food_tax_credit` added as no.
