# Settlement: Iowa, tax year 2025 (round r6)

Settled 2026-11-07 from `work/extract/2025/IA.r6.A.json` and `IA.r6.B.json`.
Sources: `sources/archive/2025/IA/`: the 2025 Expanded Instructions ("Instr", `4435`), the 2025 IA 1040 return ("Form", `4400`; Schedule 1 is its PDF p.5), the Schedule 1 web page and the Retirement Income Tax Guidance page dated March 13, 2025 ("Guidance"). Page numbers are PDF pages (the pypdf markers).

`uv run python -m tools.compare` reported **51 structured differences** (124 wording). **All 51 were decided from the booklet; none was dropped on scope.** Only 1 is a true two-sided difference (`muni_interest.treatment`). The other 50 are entries one reader wrote and the other did not, in 5 groups.

## Structured differences

| # | Entry | Fields | A | B | Settled | Page |
|---|---|---|---|---|---|---|
| 1 | `muni_interest.treatment` | 1 | other_states_taxed_own_exempt | other | **other (B).** Iowa's main rule is that municipal interest is added; only a printed list of Iowa issues escapes, so "own exempt" is wrong for an Iowa bond not on the list. | Instr p.64 "unless specifically exempt from Iowa tax"; "interest from certain Iowa state and municipal securities is exempt" |
| 2 | Personal, 65, blind and dependent amounts as `base.deductions` | 12 | four deductions | none | **Moved out.** They are credits against tax, so `base.deductions` is empty. | Instr p.8 Step 3; Form p.2 line 8 and line 11, subtracted from tax on line 12 |
| 3 | The same four as credit reliefs | 18 | none | four credits | **Kept (B)**, with `credit_amount`, `credit_basis: tax`, `covers: [all_income]`, `all_income_scope: return`. Changes below. | Instr p.8; Form p.1 "x $40", "x $20" |
| 4 | Protection-occupation survivor | 8 (4 each) | `public_pension` only | every retirement kind | **A.** The plan must be one of the named Iowa Code plans. `covers_unclear` dropped; the limit is in `not_covered`. | Instr p.68 "Pension income must come from a retirement plan provided for under one of the following Iowa Code sections" |
| 5 | Disability income exclusion (A only) | 4 | kept | none | **Kept**, cite moved to the booklet. `subtraction`: it excludes "a portion". | Instr p.75 line 19h |
| 6 | Health insurance deduction (A only) | 8 | kept | none | **Kept.** `income_test` `removes`, `applies_when: at_or_over`, threshold 100,000 (the statute's figure, not shifted). `all_income_scope: return`: it can pay for the spouse's or a dependent's cover (Instr p.74). | Instr p.72-74; worksheet p.73 "If line 3 is less than $100,000 ... If line 3 is $100,000 or more you are NOT eligible" |

Changes inside row 3:
- **B's `born_on_or_before: 1961-01-01` dropped.** The booklet prints an age test ("65 or older on or before January 1, 2026"), not a birth date. It would also be wrong in every later year of a projection. `min_age: 65`, with the words in `other_conditions`.
- **B's single `return` personal credit with the count in `cap_rule` split in two.** The count is 1 for status 1, 3, 5 and 2 for status 2 and 4 (Instr p.8). `ia_personal_credit` is per person, which gives a joint return two; `ia_head_of_household_credit` is the extra credit, the same shape as the Arkansas record.

### Not flagged by the compare, but settled

- **`public_pension_other_state` moved from `covers_unclear` into `covers`** in the 55, disabled and survivor entries. Both readers had it unclear, so the compare is silent. See question 1.
- **`ia_federal_securities_income` added.** Neither reader had an entry; both had it in notes. Printed at Instr p.64-66 (line 1 column B) and p.67 (line 2 column B). It holds the Guam, Puerto Rico and Virgin Islands bonds too (p.65). The p.66 obligations "not considered federal securities" are in `not_covered`.
- **Form:** uncapped exclusions written `exempt_in_full`; the compare treats that as the same as an uncapped `subtraction`.
- **Ids** use an `ia_` prefix.
- **Kept in notes, no entry:** the low-income exemption, alternate tax, tax reduction, lump-sum tax, Guard and reserve withdrawals, farm tenancy exclusion, local surtaxes. The low-income figures are not retirement relief (`docs/design.md` non-goal), the same call as the Arkansas settlement; the schema has no field for the alternate tax.

## The questions the dispatch requires

**1. Another state's government pension, and New York State's in particular.** In `covers` as `public_pension_other_state`, same entries as Iowa's own, no `paying_states`.
- Quote: "If you or your spouse receive federal taxable income from a governmental or other pension or retirement plan you may be eligible to exclude that amount from your Iowa income." (Instr p.67; the same words on the Schedule 1 web page and, for the plans covered, in Guidance "What retirement income qualifies".)
- No source names New York or any other state's plan. The rule is read from the words and the absence of a limit by payer. The one place line 7 does limit to Iowa plans is the protection-occupation branch (p.68), which shows the booklet says so when it means it. The same call was made for GA, CO, MD, AL, SC and AR.
- Reciprocity does not change this: "Iowa's only income tax reciprocal agreement is with Illinois" and it covers wages and salaries (p.87).
- **Rule for a New York State pension:** the recipient excludes all of the federally taxable amount if 55 or older on December 31, disabled, or an eligible survivor; otherwise it is taxed at 3.8%. It does not get the protection-occupation branch, which needs a named Iowa Code plan.

**2. Its own and federal government pensions.** Own: "qualified pension plans ... including IPERS" (Instr p.68), under the same four routes. Federal: no line 7 sentence names them. "Retirement pay resulting from participation in the Civil Service Retirement System (CSRS) or the Federal Employees Retirement System (FERS) does not qualify for the exemption" (p.90) is about the military exemption only. They are read as "governmental" under line 7, so `public_pension` in the 55, disabled and survivor entries.

**3. Private pensions, IRA and employer-plan distributions, Roth conversions.** All excluded in full, no cap, no income test, by the same routes. Named on p.68: IRA, SEP, SIMPLE, Keogh, qualified pension plans, "Roth conversion income", 401(k), 403(b), 457(b), "Annuity distributions pursuant to IRC section 402(a)", ESOP. Not eligible: "Nonqualified deferred compensation plans" and "Nonqualified annuities" (p.68). "the income recipient must meet one of the following conditions" (p.67) makes it per person; Guidance confirms for married couples. No cap appears in any of the three documents. Railroad retirement: any age (p.68). Military: "without regard for age or disability" (p.90).

**4. Social Security.** Exempt. "Iowa does not tax Social Security benefits." (Instr p.67), and a second line: Form p.5 Schedule 1 line 5, in the subtraction column.

**5. Brackets, standard deduction, exemptions.** Flat rate, one schedule: "Multiply line 4 by 3.8%" (Form p.2), "Iowa now has a flat tax rate of 3.8%" (Instr p.3, p.12). No status has its own schedule. No Iowa standard deduction is printed: Iowa starts from federal taxable income (Form p.2 lines 2-4), which already holds the federal deduction. Exemptions are the 40 and 20 credits.

## Projection

- **Starts from** `federal_taxable_income`, `deductions` empty (the guide's exception for a state whose law starts there).
- **Reliefs:** 55 or older (7 kinds, `pension_source`, because military is left out of its covers and has its own entry), military (`pension_source`), railroad, personal credit, age-65 credit.
- **`muni_interest`:** `all_taxed`. The projection has no `other`, and an Iowa bond off the list is taxed, so `other_states_taxed_own_exempt` would be wrong if a consumer ever tells Iowa bonds apart. Approximation: overstates.
- **`not_modelled`:**
  - `has_pension`: the disabled branch; the survivor and protection-occupation branches.
  - `person_in_age_range` 65-120: health insurance deduction.
  - `has_dependents`: dependents credit.
  - `never`: head of household's extra credit, blind credit, disability income, federal securities, capital gain deduction, farm tenancy exclusion.
- **Approximations:** low-income exemption, alternate tax and tax reduction; municipal interest; Treasury interest; nonqualified annuities; negative line 2; the January 1 birthday for the 65 credit; lump-sum tax; local surtaxes.
- **Indexing:** brackets and credits, `indexed: false, assumed: true`; the booklet is silent. `derived_figures` is empty.

Validator: both files `ok`.

## Unsure

- **`public_pension_other_state` in `covers`, and federal civilian pensions in `public_pension`,** both rest on "governmental or other", with no sentence naming them. Both readers stopped at unclear for the first. Guidance points to Iowa Administrative Code rule 701-302.47(1), which is not in the sources.
- **Low-income exemption for a separate filer at 65:** p.5's filing test prints 24,000; p.11's exemption text does not. Noted, not resolved. Nothing in the projection depends on it.
- **Alternate tax worksheet** prints "12/31/2024" (p.12) where other pages print 12/31/25. Recorded as printed, in notes. It looks like a stale date.
- **Capital gain deduction:** form IA 100 is not in the sources, so its terms are unknown and gains are taxed in full. This may be material for a farm or business sale.
- **The low-income exemption and alternate tax left as notes** may understate how much a low-income 65-or-older household saves. The example in the projection is about 200 a year.
- **`muni_interest: all_taxed`** differs from the other states' projections, which use `other_states_taxed_own_exempt`. It computes the same for a consumer that treats all bonds as other-state.

## 2026-11-08: marker ids and indexing covers

- Marker ids given: first from_record id (warning code unchanged): `ia_ret_excl_disabled`, `ia_ret_excl_survivor`, `ia_health_insurance_deduction`, `ia_head_of_household_credit`, `ia_blind_credit`, `ia_dependent_credit`, `ia_disability_income_exclusion`, `ia_federal_securities_income`; descriptive: `ia_capital_gain_deduction` (no from_record id); `ia_retired_farmer_tenancy_exclusion` (no from_record id).
- Indexing covers: `brackets` -> `brackets`; `credits` -> `reliefs.credit_amount`.
- Every `assumed` answer was checked again against the archived sources (searched for indexed, inflation, cost-of-living, adjusted annually, each year, CPI, fixed): none says, so all stay `assumed: true`.
- `tools.checks --fix-warnings` updated the cases' accepted_warnings where a code changed; nothing else in the cases changed.
