# Settlement: Mississippi, tax year 2025 (round r6)

Settled 2026-11-07 from `work/extract/2025/MS.r6.A.json` and `MS.r6.B.json`.
Sources: `sources/archive/2025/MS/`: the 2025 Form 80-100 Instructions ("Instr"), the 2025 Form 80-105 resident return ("Form") and the Department's Individual Income Tax FAQ page ("FAQ"). Page numbers are PDF pages; in this booklet they match the printed numbers.

`uv run python -m tools.compare` reported **20 structured differences** (67 wording).
- **20 settled from the sources, 0 dropped.**
- 17 rest on the booklet and form, with the FAQ deciding annuities. The other 3 (capital gains) rest on the FAQ, with Instr p.11 Line 40 for the loss rule.

## Structured differences

| # | Entry | Fields | A | B | Settled | Page |
|---|---|---|---|---|---|---|
| 1 | Retirement income, one entry or two | 12 (A's 4 against B's 8: the compare keys entries by `covers`, so the fields show for each side) | one entry: `public_pension`, `private_pension`, `annuity` | two entries: government; private | **One entry**, `ms_retirement_income_exempt`. Line 46 is one sentence with no difference in cap or condition, so there is no branch to split. | Instr p.11 Line 46 |
| 1a | `annuity` (inside 1) | | `covers` | `covers_unclear` | **`covers`**. The FAQ names it, under the same condition. | FAQ "Is retirement income taxable?"; Instr p.11 |
| 1b | `public_pension_other_state` (inside 1) | | `covers_unclear` | `covers_unclear` | **`covers`** (neither reader had it there). See "Pensions" (1). | Instr p.11 Line 46, against Line 43 |
| 1c | `military_pension`, `ira_distribution`, `employer_plan_distribution`, `roth_conversion` (inside 1) | | `covers_unclear` | `covers_unclear` | **`covers_unclear`**. No source names them. See "Pensions" (3). | Instr p.11; Form p.2; FAQ |
| 2 | National Guard and Reserve pay (A only; B in notes) | 5 | subtraction of wages, cap 15,000 a person | notes only | **Kept as a relief.** See below. | Instr p.12 Line 55; Form p.2 line 55; FAQ |
| 3 | Capital gains exemption (A only) | 3 | `long_term`, exempt, 0 | none | **Kept, with `applies_to` changed to `other`.** See below. | FAQ "What is the Mississippi tax treatment of long-term capital gains?" |

### One-sided entries and points the compare did not flag

- **National Guard and Reserve pay: kept.**
  - Instr p.12 Line 55: "Enter the lesser of the National Guard or Reserve pay or the $15,000 statutory exclusion per taxpayer."
  - Form line 55: "National Guard or Reserve pay (enter the lesser of amount or $15,000)."
  - FAQ: "The first $15,000 of salary received by those serving in the National Guard or reserve forces is excluded from income."
  - B's reason for leaving it out ("not a retirement relief") is not a scope limit: design.md excludes credits, not subtractions, and AZ, HI, SC and VA keep the same relief. It goes to `not_modelled` in the projection, as in those states.
- **Combat-zone hazardous duty pay: added** (A in notes, B silent). The FAQ prints it ("exempt from Mississippi Income Tax"). It is in scope on the same footing as Guard pay and AR's active-duty pay.
- **Capital gains `applies_to`: changed from `long_term` to `other`.** A's field said `long_term` and A's own note said `other`. The FAQ opens "Long-term capital gains are considered taxable income", so a `long_term`/`exempt` entry would misread as all long-term gains being exempt. AR's principal-residence entry has the same shape. The FAQ's sentence is garbled ("domestic corporations or partnership interests in domestic corporations or partnership interests in"); the condition keeps what it says and does not define "domestic".
- **Social Security relief entry: kept in the record** (both readers had it) and left out of the projection, where `social_security.treatment: exempt` holds it. This matches nearly every settled state.
- **`who.other_conditions`:** I dropped "(retirement age and/or service requirements)" from the FAQ's condition. Line 46 uses those words only for deferred compensation. The FAQ sentence "Early distributions are not considered retirement income and may be subject to tax" was added to `not_covered`.
- **`base.cite`:** B's form cite kept (it shows lines 13 to 16). A's and B's ids replaced with the `ms_` prefix.
- **A's note that the schedule applies the band "to the total of Column A and Column B":** not carried over. The schedule enters the first 10,000 per column; only the multiplication by 0% is on the total.

## The five facts asked for

### Pensions

**(1) Another state's government pension, New York State included: exempt in full. In `covers` as `public_pension_other_state`, in the same entry as Mississippi's and federal pensions. No `paying_states`.**

- Line 46 (Instr p.11): "Social Security benefits, Railroad Retirement benefits, and retirement income from federal, state, and private retirement systems are exempt in total."
- FAQ: "Generally, retirement income, pensions and annuities are not subject to Mississippi Income tax if the recipient has met the retirement plan requirements."
- **Why `covers` and not `covers_unclear`.** The source is not silent here: it names state retirement systems, and a New York State pension is paid by one.
  - "state" carries no limit to Mississippi, and sits between "federal" and "private", neither of which is limited to Mississippi.
  - The FAQ names no payer.
  - Two lines up the same page, where the booklet means Mississippi only, it says so: Line 43 exempts "the State of Mississippi and subdivisions thereof" and taxes obligations of "states ... outside of Mississippi".
  - This is the same call as SC ("federal, state, and local governments"), and AR, GA and AL on weaker wording.
- **What it rests on.** No sentence names New York or another state, and no reciprocity rule is printed. Both readers stopped at `covers_unclear`. The projection carries this as an `understates_tax` approximation so the reading stays visible.

**(2) Own and federal government pensions: exempt in full,** in `covers` as `public_pension`, on the same two quotes. "federal" and "state" are the booklet's own words.

**(3) Private pensions, IRA and employer-plan distributions, Roth conversions, military retirement.**

| Kind | Settled | Words that decide it |
|---|---|---|
| Private pension | `covers` | "private retirement systems"; FAQ "pensions" |
| Annuity | `covers`, under the plan condition | FAQ "retirement income, pensions and annuities"; Line 46 "Pensions and annuities that are taxable as early or excess distributions ... do not qualify for exemption" |
| IRA distribution | `covers_unclear` | Not named. IRAs appear only as payments in (Instr p.12 Line 50), and the booklet mentions Form 1099-R only for withholding |
| Employer plan (401(k), 403(b)) | `covers_unclear` | Not named. See below |
| Roth conversion | `covers_unclear` | Not named |
| Military retirement | `covers_unclear` | Not named. See below |

- **Employer plans.** The nearest words are "Deferred compensation plan distributions received prior to attainment of retirement age and/or service requirements are taxable". That says what happens before, not after. Reading the exemption out of it would be an inference, so the sentence goes in `not_covered` and the kind stays unclear.
- **Military.** "federal ... retirement systems" might take it in, but it is not named. The FAQ's "I serve in the United States military" and "Does Mississippi exempt any portion of military pay?" both speak of pay only.
- **Conditions.** No age, cap or income test is printed. `not_covered` holds the booklet's exclusions: early or excess distributions (Form 5329), separation pay, deferred compensation before retirement age or service requirements.

### (4) Social Security: exempt

Line 46 as quoted above, and "Do not report Social Security benefits ... on this line". Second document, the FAQ: "Mississippi does not tax benefits received from U.S. Social Security ... Any portion of such income, which may be taxed under federal law, is not subject to Mississippi's income tax." Form 80-105 lines 38 to 49 print no Social Security line, which fits: the benefit is simply not reported.

### (5) Brackets, standard deduction, exemptions

- **Schedule.** Instr p.22: "0% on the first $10,000.00 of taxable income and 4.4% on taxable income in excess of $10,000.00." p.27 prints the same two lines. One schedule covers every status; married separate and head of family use it through Column A (Line 17, p.7), so by the schema only `single` and `married_joint` are given.
- **Amounts.** Both readers agree, and the p.5 table, the form and the p.4 filing thresholds (6,000 + 2,300 = 8,300; 12,000 + 4,600 = 16,600) all agree.

| Status | Exemption | Standard deduction |
|---|---|---|
| Joint or combined; spouse died 2025 | 12,000 | 4,600 |
| Married separate | 6,000 | 2,300 |
| Head of family | 8,000 (plus 1,500 for the required dependent, 9,500 in all) | 3,400 |
| Single | 6,000 | 2,300 |

- **Additional exemptions.** 1,500 each for a dependent, age 65 or over, and blindness (p.6). Line 15 and the form halve the line 12 total for married separate, which is why the form's "($12,000)" box still gives 6,000.
- **Indexing.** Not stated anywhere: `indexed: false, assumed: true`.

## The 0% band on a joint return (decision asked for in the dispatch)

**What the sources say.**
- Schedule line 1 (p.27): "Enter the first $10,000 of taxable income or part ($0 - $10,000) in Column A and Column B if applicable."
- FAQ: "If married filing joint, the first $10,000 of each taxpayer's taxable income is exempt; and each taxpayer's remaining taxable income is taxed at 4.4%."
- p.6: couples with separate incomes "should separate their incomes ... in order to take advantage of the lowest tax rates."
- So both columns positive means 10,000 each, 20,000 in all. A return with all income in Column A has one band, and "If only one spouse has income, this income may not be split" (p.5). A negative column is netted into Column A, so one band (Line 17, p.7).

**Record.** `married_joint` is the schedule as printed (0 from 0, 4.4% from 10,000), with the per-column rule in `notes`. Both readers had this.

**Projection: one 10,000 band on `married_joint`, stated as an approximation, `overstates_tax`, at most 440 a year.** The schema's schedule runs on the return's total and has no per-spouse band.

| Option | One-income couple | Two-income couple, each 10,000+ taxable | Decision |
|---|---|---|---|
| One 10,000 band | exact | 440 too much | **Chosen.** Never understates; adds no figure; same direction as AR's joint-table choice |
| 20,000 band (a `derived_figures` sum) | 440 too little | exact | Rejected: understates for any couple where one spouse has no income Mississippi taxes (only Social Security or an exempt pension, say) |
| Flat 4.4% plus an `all_income` relief of 10,000 per person with `all_income_scope: person` | exact | exact | Rejected for now, see below |

- **Example.** Each spouse with wages 40,000. Projection: 80,000 less 16,600 is 63,400 taxable, tax 4.4% of 53,400 = 2,349.60. Return: 31,700 in each column, tax 4.4% of 43,400 = 1,909.60. Difference 440.
- **The third option.** By my arithmetic it reproduces the law for any split, because the deductions can be divided in any manner. But it replaces a printed schedule with a relief the record does not hold, needs a record entry that is not a real relief, and depends on the consumer's per-person allocation of interest and gains, which the booklet does not define for joint assets. If 440 a year matters, a per-spouse flag on the schedule is the cleaner fix, and that is a schema decision for the owner.

## Projection

- **Base.** `federal_agi`, with an approximation (`state_own` maps there by the guide).
- **Deductions.** Standard, personal (both per return), age 65 per person with `min_age` 65.
- **Reliefs.** Railroad retirement, and retirement income with `covers` as in the record. `needs_input: ["pension_source"]` is set because military retirement is outside `covers` and must be told from the rest.
- **`not_modelled`.** Non-qualifying pension income (`has_pension`), dependent exemption (`has_dependents`), and blindness, Guard and combat pay, and the narrow gains exemption (`never`).
- **Approximations.** 14, each with a direction and size. Besides the band and the unclear kinds:
  - the 4.4% rate held against the printed cuts (3% from 2030, overstates; issue #2);
  - a later-year federal surviving spouse on the married_joint amounts (understates, at most 365.20);
  - Treasury and own-state bond interest; itemizing; the `state_own` base.
- Worked figures in the sizes were recomputed by script.

## Unsure

- **IRA and 401(k) distributions are the largest open item.** The projection taxes them, which can reach 1,834.80 a year on 60,000 for a single person. For a retiree this outweighs everything else in the file, and it can change a where-to-live decision. Only the statute or a Department rule can settle it; the sources here cannot.
- **Other-state pensions in `covers`** rest on the word "state" and the contrast with Line 43. No sentence confirms it, and neither reader went that far.
- **Annuities** are in `covers` on the FAQ, whose text the booklet (p.24) calls an informal interpretation for its printed FAQs; the web page is the same kind of source. An annuity bought outside a retirement plan is not addressed.
- **"retirement plan requirements"** is undefined, and no age is printed, so a projection cannot test it. The `has_pension` warning stands in for it.
- **Line 17 refers to "line 5 of the Schedule"; the schedule prints lines 1 to 4.** I read that as line 4. No figure depends on it.

## Changes after check writing

The check writer found that Form 80-105 halves the whole of line 12 on a married separate return, the age exemption included (Line 3, p.5; Line 15, p.7). The projection's flat 1,500 per person was 33.00 too low in tax for a filer 65 or older with a spouse under 65. It now holds 750 per qualifying person for married_separate, counting both spouses, which matches the form on both returns and when both are 65. `derived_figures` gained `how: half`.

## 2026-11-07: maintainer decision

The owner decided (docs/decisions.md, "2026-11-07: maintainer decisions on NC military retirement and 401(k)/IRA
coverage in GA, HI, MS") that Mississippi's retirement income exemption covers IRA and 401(k)/403(b)/457
payouts, except early distributions, on the Department's own regulation. This settles row 1c above for
`ira_distribution`, `employer_plan_distribution` and `roth_conversion`, and closes the first "Unsure" item
(IRA and 401(k) distributions). `military_pension` stays in `covers_unclear`.

New source: `sources/archive/2025/MS/00000158c.pdf` ("Reg"), Mississippi Administrative Code Title 35 Part III
Income and Franchise, the DOR's finalized income tax regulations (https://www.sos.ms.gov/adminsearch/ACCode/00000158c.pdf,
fetched 2026-11-07). Subpart 02 Chapter 07 "Income from Retirement Allowances, Pensions, Annuities or Optional
Retirement Allowances", rules 100-105, is on PDF p.18 (printed "Page 18 of 123").

### What changed

- **Record** (`MS.record.json`), entry `ms_retirement_income_exempt`:
  - `ira_distribution`, `employer_plan_distribution` and `roth_conversion` moved from `covers_unclear` to `covers`.
    `covers_unclear` now holds only `military_pension`.
  - `not_covered` gained rule 104's two exclusions: early distributions from retirement plans; income from
    investments in stocks, bonds, intangible securities, real or tangible property.
  - `who.other_conditions` gained rule 102's condition for deferred compensation (tax deferred federally, and the
    recipient qualifies for other retirement income by minimum age, years of service or other criteria) and rule
    105 (extends to the spouse or other beneficiary on the retiree's death).
  - `cite.section` now names Reg rules 100-105, PDF p.18, with the URL; the full cite is in `notes`.
  - Notes: one quoting rules 100 and 101 with the full cite, one each for rules 102, 103, 104 and 105, one on Roth
    conversions, one on military retirement, and one "Settlement 2026-11-07 (maintainer decision)" line. The earlier
    notes on "the only rule is Line 46", the four unnamed kinds, and the covers_unclear settlement each end with a
    pointer to the regulation notes. Nothing was deleted.
- **Projection** (`MS.projection.json`):
  - `ms_retirement_income_exempt.covers` gained `ira_distribution`, `employer_plan_distribution`, `roth_conversion`.
    `needs_input: ["pension_source"]` stays (military retirement is still outside `covers`).
  - `record.sha256` updated.
  - The `has_pension` marker now says the same non-qualifying exemption holds for IRA, 401(k), 403(b) and 457
    payouts taken early (rules 102 and 104).
  - **New marker**, `warn_when: person_in_age_range`, `age_range: [0, 59]`: IRA, 401(k), 403(b) and 457 payouts
    taken early (before 59 1/2 under federal law, unless a federal exception applies) are taxable in Mississippi but
    exempted here; a deferred compensation payout qualifies only once the person meets the plan's age or service
    test; a Roth conversion before 59 1/2 is exempted too, the sources not saying whether it is "early". It is a
    second marker because `has_pension` does not fire for a household whose only retirement money is an IRA or a
    401(k).
  - Approximations removed (3):
    - "IRA distributions, required minimum distributions included, are taxed ..." (overstates_tax, 1,834.80 on 60,000).
    - "Employer plan distributions (401(k), 403(b) and the like) are taxed ..." (overstates_tax, 1,834.80 on 60,000).
    - "Roth conversions are left out of covers ..." (overstates_tax, 1,394.80 on 50,000).
  - Approximations added (2):
    - "IRA, 401(k), 403(b) and 457 payouts and Roth conversions are exempted at every age ..." (understates_tax):
      single, age 50, only income a 30,000 IRA distribution before 59 1/2: Mississippi taxable 30,000 - 6,000 -
      2,300 = 21,700, tax 4.4% x 11,700 = 514.80; 0 here.
    - "Roth conversions are exempted on the regulation's rule 101 ..." (understates_tax): if the Department reads a
      conversion as not a retirement allowance, 1,394.80 on a 50,000 conversion, single, under 65, no other income.

### Why: the sources, with pages

- **Reg p.18 rule 100:** "Amounts received as retirement allowances, pensions, annuities or optional retirement
  allowances from any Federal, State, and Private retirement system or plan are exempt from State Income Tax."
- **Reg p.18 rule 101:** "Optional retirement allowances include all income from Keogh Plans, Individual Retirement
  Accounts (IRA'S), and other similar tax deferred plans." This settles `ira_distribution` (RMDs included: they are
  income from an IRA).
- **Reg p.18 rule 102:** "Optional retirement allowances also include income from deferred compensation plans to the
  extent these plans are tax deferred under federal income tax law and the recipient is qualified to receive other
  retirement income based on minimum age, years of service, or other criteria at the time of receipt of the deferred
  compensation." This settles `employer_plan_distribution` under that condition. It is the other half of the
  booklet's Line 46 sentence (Instr p.11), which taxes deferred compensation "received prior to attainment of
  retirement age and/or service requirements".
- **Reg p.18 rule 103:** Roth IRA distributions are "treated in the same manner as provided under the Internal
  Revenue Code". This is about payouts from a Roth IRA, not conversions into one.
- **Reg p.18 rule 104:** "Early distributions from retirement plans do not qualify for this exemption. Although these
  amounts are subject to state income tax, there is no early withdrawal penalty for state purposes." It also leaves
  out investment income. The regulation does not define "early"; the booklet ties it to distributions "taxable as
  early or excess distributions under the Federal Internal Revenue Code (see Federal Form 5329)" (Instr p.11). No
  Mississippi source prints an age; "59 1/2" in the new marker is the federal age, named as federal law at the
  owner's direction.
- **Reg p.18 rule 105:** the exemption "extends to the spouse or other beneficiary upon the death of the primary
  retiree". Recorded; nothing to model (an inherited payout is already in the covered kinds).
- **Roth conversion: `covers`, on rule 101.** A conversion takes money out of a traditional IRA, and the taxable
  amount is income from that IRA; rule 101 says optional retirement allowances include "all income from" IRAs, and
  rule 100 exempts them. Nothing in rules 100-105 takes conversions out: rule 103 governs payouts from the Roth, and
  rule 104 excludes early distributions and investment income. The reading is direct but no source names conversions,
  so the projection keeps an understating approximation that says so (as for other-state pensions).
- **Why not an age test.** The format has one (`who.min_age: 59.5`), but it fits worse than the warning:
  - `who.min_age` applies to the whole relief, so it needs a second relief entry for the plan kinds, with an age
    that no Mississippi source prints;
  - rule 102's test for 401(k), 403(b) and 457 money is the plan's own minimum age, years of service or other
    criteria, not 59 1/2; a 57-year-old drawing a 401(k) after retiring under the plan's rules qualifies, and an age
    test would tax that payout;
  - federal exceptions (Form 5329) make many payouts before 59 1/2 not "early", and a Roth conversion before 59 1/2
    (the early retiree's conversion ladder) is not shown to be early at all; an age test would tax all of them;
  - a new relief id would also need its own check case (`tools.checks` asks for one per relief).
  So the projection exempts every payout, lists the understatement, and warns for anyone 59 or younger.
- **Military retirement: unchanged.** Rule 100's "any Federal ... retirement system or plan" might take it in, but it
  is not named; Reg Subpart 03 Chapter 08 "Exclusion Military Pensions and Disability Payments for Certain Injuries
  and Sicknesses" (PDF p.25) says only that the Commissioner follows federal rules on amounts excluded under it. The
  maintainer decision does not cover it. Its overstating approximation stays.

### What it means in dollars (4.4% over the deductions and the 10,000 band)

- **IRA or 401(k) payout, 59 1/2 or older.** Single, age 62, only income a 60,000 IRA distribution (or 401(k) payout
  after meeting the plan's age or service test): Mississippi tax falls from 4.4% x (60,000 - 8,300 - 10,000) =
  1,834.80 to 0.
- **RMDs.** Exempt every year, at any size: no cap, no income test.
- **Roth conversion.** Single, age 62, a 50,000 conversion and no other income: 1,394.80 to 0. A conversion now costs
  nothing in Mississippi tax, so the projection no longer steers a Mississippi household away from converting.
- **Early payout (understated).** Age 50, a 30,000 IRA distribution before 59 1/2: Mississippi taxes 514.80; the
  projection says 0, and warns.
- **Planning effect.** With pensions, IRAs, 401(k)s, conversions and Social Security all exempt, a Mississippi
  retiree past the early age pays state tax only on wages, interest, dividends and gains (and, in the projection,
  military retirement pay, whose treatment is still unclear).

### Checks (`uv run python -m tools.checks --year 2025 --state MS`)

The run printed "MS: 35 case(s), 15 problem(s)". All 15 are `accepted_warnings` mismatches from the new age-range
marker: each case has a person aged 59 or younger and no pension, so it now gets
`state_rule_not_modelled:ms_retirement_income_exempt`:
`band_just_over_10000`, `band_top_exactly_10000`, `base`, `deductions_head_of_family`, `deductions_joint_one_income`,
`deductions_separate`, `deductions_single`, `deductions_surviving_spouse`, `gains_and_dividends_taxed`,
`income_below_deductions`, `joint_two_earners_equal`, `joint_two_earners_uneven`, `muni_interest_other_state_taxed`,
`muni_interest_own_state_exempt`, `treasury_interest_taxed` (all `ms_2025_`). No coverage problem (missing case per
relief or deduction) is reported. Checks were read-only for this change; `--fix-warnings` would set them. If the
owner prefers no warning on every household with someone under 60, drop the second marker: the 15 problems go away,
and an early IRA-only payout goes unwarned.

Cases whose expected figures change (none edited):
- `ms_2025_ira_distribution_taxed`: 60,000 IRA, age 62. Now exempt: state AGI 0, taxable 0, tax 0 (was 1,834.80);
  `tests` should name `ms_retirement_income_exempt` with relief amount 60,000; the id should drop "taxed".
- `ms_2025_employer_plan_distribution_taxed`: 60,000 401(k), age 62. Same: tax 0 (was 1,834.80), on the assumption
  the person meets the plan's age or service test (rule 102).
- `ms_2025_roth_conversion_taxed`: 50,000 conversion, age 62. Now exempt: tax 0 (was 1,394.80).
- No other case has IRA, employer plan or conversion income; their figures do not change.

### Format gaps

- **One publication per `cite`.** The relief's `cite` holds the booklet; the regulation (a second publication with
  its own URL) is named in `cite.section` and quoted with its full cite in `notes`.
- **No condition tied to one covered kind.** Rule 102's age-or-service condition applies only to deferred
  compensation, and rule 104's exclusion to early payouts of every kind; a relief's `who` applies to all of `covers`.
  Both are in `who.other_conditions` / `not_covered` as text, and in the projection as warnings.
- **No warning keyed to an income kind.** `warn_when` has `has_pension` but nothing for "has an IRA or employer-plan
  payout" or "has a Roth conversion", so the early-payout warning keys on age alone and fires for every household
  with someone 59 or younger, whether or not it draws on a plan.

### Still unsure

- **Roth conversions** rest on rule 101's "all income from" IRAs; no source names them. If the Department reads a
  conversion before 59 1/2 as an early distribution, or a conversion as not a retirement allowance, the projection
  understates (approximation and warning in place).
- **Military retirement** stays unclear, as above.

### Validator

```
data/states/2025/MS.record.json: ok
data/states/2025/MS.projection.json: ok
```

- Main session, 2026-11-07: the second marker (`person_in_age_range` 0-59) was removed and its text folded into the `has_pension` marker. It fired for every household with a person under 60, IRA payout or not, against the rule that a run warns only when it hits the case. The format has no trigger for "an IRA or plan payout before 59 1/2"; recorded as a format gap (later met by the `has_retirement_account_distribution` trigger). Until then an early payout from an IRA alone (no pension item) gets no Mississippi warning.

- Main session, 2026-11-07 (format for the first frozen schema): added a second marker for the same rule that warns when an IRA or plan payout or Roth conversion is taken by a person under 60 (has_retirement_account_distribution, ages 0-59), the case the has_pension marker missed.

## 2026-11-08: marker ids and indexing covers

- Marker ids given: first from_record id (warning code unchanged): `ms_dependent_exemption`, `ms_blind_exemption`, `ms_national_guard_reserve_pay`, `ms_ownership_interest_gain_exempt`; descriptive: `ms_nonqualifying_retirement_income` (the marker that warns on pensions); `ms_early_account_distribution` (the marker that warns on early account distributions; both started with ms_retirement_income_exempt, so their codes had collided).
- Indexing covers: `brackets` -> `brackets`; `deductions` -> `deductions`.
- Every `assumed` answer was checked again against the archived sources (searched for indexed, inflation, cost-of-living, adjusted annually, each year, CPI, fixed): none says, so all stay `assumed: true`.
- `tools.checks --fix-warnings` updated the cases' accepted_warnings where a code changed; nothing else in the cases changed.

## 2026-11-08: indexing settled from statutes

Statute research (work/indexing/findings*.json) settled every projection indexing entry that was `assumed: true`:

- `brackets` (brackets): not indexed, Miss. Code 27-7-5(1)(a)-(b) as amended by 2025 HB 1 (as sent to Governor)
- `deductions` (deductions): not indexed, Miss. Code 27-7-17 (standard deduction) and 27-7-21(b)-(d),(f) (personal and age-65 exemptions)
- Record `indexing`: added brackets -> no; added ms_standard_deduction -> no; added ms_personal_exemption -> no; added ms_age_65_exemption -> no.
- Flagged figure: the 2025 Form 80-100 instructions (80100251_202, PDF p.5 filing status table and PDF p.6 Line 4) print the head of family exemption as 8,000, plus 1,500 for the required dependent on line 6, 'which totals $9,500'. The statute's 9,500 is that total. The data's 8,000 matches the booklet (dependents are not modelled); no change.
