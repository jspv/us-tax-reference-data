# Wisconsin 2025 settlement log

Readings: `work/extract/2025/WI.r6.A.json`, `WI.r6.B.json`. Settled 2026-11-07.
Sources: `sources/archive/2025/WI/`: Form 1 Instructions I-111 ("Inst"), Form 1 I-010 ("Form"), Schedule SB and its
Instructions ("SB Inst"), Schedule AD and its Instructions ("AD Inst", fetched after the readers finished),
Publication 126 ("Pub 126"), Publication 106 ("Pub 106") and the retired-persons FAQ page ("FAQ"). Page numbers
are PDF pages. Outputs: `data/states/2025/WI.record.json`, `data/states/2025/WI.projection.json`.

`tools.compare` reported **130 structured differences** and 182 wording differences. All 130 were read against the
sources and settled. **109 were decided by what the sources print; 21 were not**: 12 are `who.basis` on the
uncapped Social Security and railroad entries (rule 5), 9 are B's printed `base` figures on the brackets (schema
use of `base`).

Figures did not differ between the readers anywhere: rates, bracket starts, the four standard deduction maxima and
first falling rows, 700 / 250 exemptions, 24,000 / 48,000 / 5,000, the 15,000 / 30,000 income test, 30% / 60%
gains. Every difference is about the shape of an entry or what it covers.

## Comparison

| Lines | Field | A | B | Source | Settled | From the sources? |
|---|---|---|---|---|---|---|
| 26 | Standard deduction entries | four entries, one per status; measure `state_agi`; no `applies_when` | one entry, four amounts; measure `other`; `at_or_over` | Inst pp.35-37, the table; Form line 7 "This is your Wisconsin income" | One entry (one table with four columns), measure `state_agi`, `at_or_over` (the table's "At least" column), and **effect `stepped` with every printed row** (neither reader: both had `other` with no steps). See "Standard deduction" | Yes |
| 3 | Standard deduction for dependents | `other` entry, 1,350 | note | Inst p.15 worksheet | Kept (A) | Yes |
| 8 | `brackets.head_of_household` | list = single | none | Pub 106 p.6: "Schedule A - For Single Taxpayers or Head of Household" | None (B): no schedule of its own; the projection falls back to single | Yes |
| 9 | `base` on bands 2-4, three statuses | none | 513.80, 2,089.00, 16,547.93; 685.30, 2,784.98, 22,064.26; 342.65, 1,392.49, 11,032.13 | Pub 106 pp.6-7 print them | Left out (A): each is exactly the sum of the lower bands, so it changes nothing; the schema keeps `base` for a table that steps up (Ohio) | No: schema use |
| 6 | U.S. government interest | `covers: interest` | `covers: interest, dividends` | SB Inst p.1 line 2: "interest on U.S. bonds and interest and dividends of certain U.S. government corporations" | Both kinds (B) | Yes |
| 3 | U.S. government interest in IRA and plan distributions | entry | none | Pub 126 p.10 section H and worksheet | Kept (A) | Yes |
| 3 | Active duty pay | none | entry | SB Inst p.8 line 18 | Kept (B) | Yes |
| 11 | Disability income exclusion | entry | note | SB Inst p.9 line 22; Pub 126 p.9 | Kept (A) | Yes |
| 12 | `who.basis` on Social Security and railroad | `each_person` | `return` | No age test, no cap; the tax is the same | `each_person`, as Nebraska and most settled uncapped entries (rule 5: each retiree qualifies on their own) | No: rule 5 |
| 49 | Lines 16 and 17 (retirement subtractions): `covers`, entry split, basis, caps | one line 16 entry `each_person` 67, cap 24,000 / 48,000 joint per return; public pensions in `covers` | two line 16 entries (24,000 `older_spouse` per person; 48,000 per return) in a best-of group; public pensions in `covers_unclear` | SB Inst pp.7-8; Pub 126 pp.8-9, p.11; Pub 106 p.4; FAQ | Public pensions in `covers` (A). Line 16 as two entries (B's split) with `each_person`, min age 67 on both: 24,000 per person; 48,000 per return only when both are 67. Line 17 as both readers had it. See below | Yes |

Total 130: 109 from the sources, 21 not.

## One-sided entries and changes neither reader made

| Entry | Reader | Kept? | Why |
|---|---|---|---|
| `muni_interest` | both `not_stated` | **Changed to `other`** | AD Inst p.1 line 1, fetched after the readers. See question 6 |
| Pre-1965 tax-sheltered annuity subtraction | both, in notes | Added as an entry (`wi_pre1965_tax_sheltered_annuity`) | Pub 126 pp.10-11 section I prints it with an example; a retirement relief |
| `paying_states` on the pre-1964 entries | neither | Added: `WI` on the local and state systems, `federal` on CSRS (as Nebraska and Indiana) | SB Inst lines 13-14 name only Wisconsin systems and the U.S. Civil Service Retirement System |
| Milwaukee supplemental benefits, WRS part | A (first), neither (second) | `not_covered` on the local and state entry | Pub 126 p.6 Example 2; p.7 Example 1 |
| `form` on Social Security, railroad, military, pre-1964 | readers mixed `subtraction` / `exempt_in_full` | `exempt_in_full` | `tools.compare` treats an uncapped subtraction as the same; most settled states write it so. U.S. government interest stays `subtraction`: it reaches only part of `interest` |
| `who.basis` on military retirement | both `return` | Changed to `each_person` | Not a compared difference; the same rule-5 reading as Social Security and railroad, so the uncapped exemptions agree |
| 33% penalty, Form 4972 lump sums, credits | both, in notes | Notes; projection `not_modelled` | No field |
| Annuity "from a qualified plan" | neither said | Kept in `covers`, with the limit in `notes` and a projection approximation | SB Inst p.8 worksheet line 2 |

## The required questions

### 1. A government pension paid by another state, and a New York State pension

**Taxed as on the federal return; no exemption and no reciprocity; it counts toward both general retirement
subtractions.** `public_pension_other_state` is in `covers` of `wi_retirement_67`, `wi_retirement_67_joint` and
`wi_retirement_5000`; no entry has it in `not_covered`; no `paying_states` on those entries, because no source
treats any paying state differently. "New York" does not appear in the sources.

Pub 126 p.4, section 3: "The amount of your retirement benefits that are taxable for federal income tax purposes are
also taxable for Wisconsin. This is true even though the retirement benefit may be due to services performed in
another state." Example 1 there: "Prior to becoming a Wisconsin resident, you lived and worked as a teacher in
Illinois for 30 years. You are receiving a pension based on your teaching services in Illinois. The amount of your
pension that is taxable on your federal income tax return is also taxable on your Wisconsin income tax return."

**Rule for a Wisconsin resident with a New York State pension:** the federally taxable amount is Wisconsin income;
at 67 or older it can be subtracted up to 24,000 (48,000 for a joint couple both 67, at the cost of all Wisconsin
credits), and at 65 or older with federal AGI under 15,000 (30,000 joint) up to 5,000.

Whether lines 16 and 17 reach a government plan's pension is a judgement (see question 3).

### 2. Wisconsin's own and federal government pensions

Taxable as on the federal return, the Wisconsin Retirement System included, except three exemptions in full:
- U.S. military, Coast Guard, NOAA and Public Health Service retirement pay (SB Inst p.6 line 12).
- The seven listed pre-1964 systems: "Milwaukee City Employees, Milwaukee City Police Officers, Milwaukee Fire
  Fighters, Milwaukee Public School Teachers, Milwaukee County Employees, Milwaukee Sheriff, and Wisconsin State
  Teachers retirement systems", if retired before 1964, a member on December 31, 1963 paid from a pre-1964 account,
  or a beneficiary (SB Inst pp.6-7 line 13).
- The federal Civil Service Retirement System on the same pre-1964 terms; "Payments from the federal Thrift Savings
  Plan do not qualify" (SB Inst p.7 line 14).

Pub 106 p.4: "Generally, the amount of your pension and annuity income that is taxable for federal purposes is
taxable for Wisconsin if you are a full-year resident of Wisconsin." Pub 126 p.7 Example 1: an annuity based on both
WSTRS and WRS service: "Only the portion of the annuity attributable to the WSTRS is exempt." No contributory-plan
test is printed. The pre-1964 entries go to `not_modelled` (`has_pension`): the projection can't know the
membership date.

### 3. Private pensions, IRA and employer-plan distributions, Roth conversions

Taxable as federally (Pub 126 p.4, and its Example 2, an IRA opened in Florida). Two general subtractions, both new
or changed for 2025, reach "retirement income from a qualified retirement plan or individual retirement account
(IRA) that is federally taxable and has not been removed from Wisconsin income on lines 12 through 15" (SB Inst
p.7 line 16).

**Covers.** `private_pension`, `ira_distribution`, `employer_plan_distribution`, `annuity`, `public_pension`,
`public_pension_other_state`. Government pensions are in `covers` on this evidence:
- Pub 126 p.11 (section J) lists what a "qualified retirement plan" includes: 401(a) trusts, SEPs, 403(a), 403(b),
  IRAs, "A deferred compensation plan of state and local governments and tax-exempt organizations under sec. 457,
  IRC", "A government plan under sec. 414(d), IRC".
- FAQ: "Wisconsin has two retirement income subtractions that eligible individuals may claim for benefits other
  than those listed in Answer 1" (Answer 1 lists the exempt systems, military and railroad), and "an individual is
  receiving military retirement benefits that are exempt ... The individual may not claim the military retirement
  benefits under either of these subtractions", which assumes government pay would otherwise count.
- Line 16 excludes what lines 13 and 14 already removed, so the taxable part of a mixed WSTRS/WRS or CSRS annuity is
  left for it.

The doubt: section J is written for nonresidents; the subtraction text itself never says "government".
`annuity` is in `covers` because the line 17 worksheet takes "Taxable pension and annuity income from a qualified
retirement plan"; an annuity bought outside a plan is not said to qualify (projection approximation).

**Roth conversions: `covers_unclear`** on all three entries. No source mentions a conversion. The line 17 worksheet
takes "Taxable IRA distributions from line 4b of your federal Form 1040", where a conversion is reported federally,
but the booklet does not name it, so rule 4 keeps it unclear. The projection leaves conversions out of `covers`
and says so in `approximations` (overstates tax for a converter 67 or older by 5.3% of the conversion, up to 1,272
a year, 2,544 joint).

`not_covered`: "any distribution that is excluded from Wisconsin income under another provision of law, such as
military retirement pay" (Pub 126 p.8), and amounts removed on lines 12-15.

### 4. Social Security

**Exempt.** SB Inst p.2 line 4: "Social security benefits are not taxable for Wisconsin. You may subtract any social
security benefits that were taxable on your federal Form 1040 or 1040-SR." Second document: Pub 126 p.5 "Social
security benefits are not taxable by Wisconsin"; Pub 106 p.4 and the FAQ say the same. Schedule SB line 4 is
"Social security adjustment".

### 5. Brackets, standard deduction, exemptions

**Brackets** (Pub 106 pp.6-7), checked against the Inst Tax Table pp.38-43 at all 3,006 row midpoints (none off by
more than 1 dollar) and the p.44 worksheet constants:

| Status | 3.5% from | 4.4% from | 5.3% from | 7.65% from |
|---|---|---|---|---|
| Single and head of household (Schedule A) | 0 | 14,680 | 50,480 | 323,290 |
| Married filing jointly (B) | 0 | 19,580 | 67,300 | 431,060 |
| Married filing separately (C) | 0 | 9,790 | 33,650 | 215,530 |

No `derivation`: the schedules are printed, so the validator's provenance check stays on every bracket figure;
the table check was done outside it (helper `analyse.py`) and is in the record's notes.

**Standard deduction** (Inst pp.35-37). See the next section. **Exemptions** (Inst pp.15-16): 700 per person (you,
spouse; 0 if claimable as a dependent), 700 per dependent, 250 more per person 65 or older allowed the 700. No
blind amount, no income limit. Qualifying surviving spouse: "you may file your Wisconsin return as head of household"
(Inst p.13), recorded in notes; the projection's default for that status is married joint (approximation).

## Standard deduction: steps, and the gap

The table is the only printed form of the rule: rows "At least / But less than" 500 dollars wide by line 7
Wisconsin income, four columns. `table.py` parsed all 286 rows from the pypdf text (contiguous from 0 to 155,169;
three cells there print with a split digit, "15,11 1" and "11 1,000" / "11 1,500", and the docling text prints
them whole: 15,111, 111,000, 111,500) plus the closing "155,169 or more ... 0".

The record and the projection hold the table itself as `effect: stepped`, one step per row where an amount
changes, each `at_or_over` its row's "At least" figure, starting with `over 0` at the maximum: 836 steps (single
228, joint 257, separate 123, head of household 228). Every amount and bound is printed, so the validator checks
each against the text; a script check gave the printed amount at the start, middle and end of every row. A
consumer gets the form's amount exactly.

The gap: no formula, rate or threshold is printed. Fitting the row midpoints gives, to the dollar on every row
(derived, not printed; in the record notes only): single 13,560 less 12% over 19,550; joint 25,110 less 19.778%
over 28,210; separate 11,930 less 19.778% over 13,390; head of household 17,520 less 22.515% over 19,550, never
below single (equal from the 57,000 row). These points sit inside rows, so the `threshold` recorded is the first
falling row (19,500 / 28,000 / 13,390 / 19,500), as both readers had it. Growing the table for later years needs
either next year's table or the statute's formula; indexing is not stated (projection: `indexed: false, assumed`).

## The age 67 subtraction (line 16), how it is held

**Record.** Two entries in one `best_of_group`:
- `wi_retirement_67`: each person 67 or older, up to 24,000 of their own qualifying income ("Individuals may
  subtract up to $24,000 of retirement income received").
- `wi_retirement_67_joint`: joint return, both 67 or older, up to 48,000 pooled ("regardless of how much retirement
  income each spouse received"). On such a return it is never smaller than the two individual amounts, so the
  best-of group picks it.

**Joint return with one spouse 67.** Settled as 24,000 of that spouse's own income. The 48,000 is printed only for
"both"; the pooling sentence is said only of the 48,000; Pub 106's "if you (or your spouse if married filing joint
return) were age 67" is the same opening line 17 uses before a worksheet that figures each spouse in a separate
column. A reading that pools 24,000 across both spouses when only one is 67 is possible; the sources don't settle
it, and this is the one printed most directly.

**Credits.** Claiming line 16 gives up every Wisconsin credit for the year (SB Inst p.7 Caution: "you may not claim
any tax credit on Schedule CR and on lines 13 through 20 and 30 through 35 of the Form 1", including carryforwards).
The schema has no field for this; it is in `who.other_conditions` of both entries and in notes, with the list of
lines. It is a real choice: the filer takes the subtraction or keeps the credits.

**Projection.** One relief, `wi_retirement_67` (from both record entries): `each_person`, min age 67, cap 24,000
(48,000 joint) per return. That is exact for single, separate and head of household returns and for a joint return
where both are 67; it is too generous (up to 24,000 x 5.3% = 1,272 a year) only for a joint return with one spouse
67 and that spouse's qualifying income over 24,000. The alternative (24,000 per person only) would be wrong for
every lopsided both-67 couple for every year after, so the joint cap was used, and the approximation is written as
`understates_tax`. The projection format can't test "both spouses 67".

The credit choice: the projection models no Wisconsin credit, so it always takes the subtraction. When the
subtraction is the better choice (the usual case for a retiree with real IRA or pension income) that is exactly the
form: the credits are lost and the projection has none. When the credits are worth more (small qualifying income
against a 300 school property tax credit, for instance) the filer would skip the subtraction and the projection
overstates tax by the difference. Held as a `not_modelled` entry (`person_in_age_range` 67-130) plus an
`overstates_tax` approximation. A separate `not_modelled` entry (`always`) covers the credits for everyone else.

**Stacking with the 5,000 subtraction (line 17).** Both can be claimed: the line 17 worksheet line 4 takes out "the
total amount subtracted on lines 12, 13, 14, 15, and 16", and line 17 has no credit restriction. Line 17 needs age
65 or older and federal AGI under 15,000 (30,000 joint; for separate filers, the two spouses' AGI together). The
projection has no ordering field, so it applies both to the full covered income; at those incomes the standard
deduction and exemptions take almost all that is left, so the effect is at most about 100 a year (worked bound: a
joint couple both 67 under 30,000 owes tax only when its Wisconsin income passes about 27,010, which leaves at most
about 2,990 of retirement income for line 17, 2,990 x 3.5% = 105). Approximation, `understates_tax`.

## 6. Municipal interest (Schedule AD)

AD Inst p.1 line 1: "Fill in the amount of interest you received from state, municipal, and other bonds. This will
generally be the amount shown as tax-exempt interest on line 2a of your federal Form 1040 or Form 1040-SR." The
exception lists 18 kinds "exempt for federal and Wisconsin tax purposes": mostly named Wisconsin authorities and
districts, bonds of Puerto Rico, Guam, the Virgin Islands, the Northern Mariana Islands and American Samoa (after
October 16, 2004), and some pre-1987 out-of-state public housing agency bonds. So Wisconsin taxes its own general
municipal bonds as well as other states'. Record: `other`, with the note. Projection: `all_taxed`, with an
`overstates_tax` approximation for the listed bonds.

## Other projection choices

- Base: federal AGI, the stepped standard deduction on `state_agi` (Form line 7 is after Schedule SB, so after the
  retirement subtractions and the Social Security adjustment), 700 per person, 250 per person 65 or older.
- Reliefs modelled: railroad and military (exempt), line 16, line 17. Social Security through `treatment: exempt`.
- `not_modelled`: line 16 credit choice, credits, pre-1964 systems, disability, U.S. government interest (both
  entries), pre-1965 tax-sheltered annuities, active duty pay, 60% farm gains, dependents, dependent standard
  deduction, the 33% penalty (`person_in_age_range` 0-59), Form 4972 lump sums.
- Approximations: one-spouse-67 joint cap; credit choice; Roth conversions; non-plan annuities; line 17 after line
  16; separate filers' line 17 test; municipal interest; qualifying surviving spouse; itemized deduction credit;
  Schedule I; Schedule WD.
- Indexing: brackets, deductions, relief caps all `indexed: false, assumed: true`.

## Unsure

- Government pensions (own post-1963 and other states') under lines 16 and 17 rest on Pub 126's nonresident-section
  definition of "qualified retirement plan" and the FAQ, not on the line 16/17 text itself.
- A joint return with one spouse 67: 24,000 of that spouse's own income, or 24,000 of either spouse's. Not settled
  by the sources; the projection's 48,000 cap is a deliberate approximation either way.
- Roth conversions: the worksheet's federal line 4b argues they count; unread in words.
- Disability exclusion's limit for a married couple with only one eligible spouse: Schedule 2440W is not in the
  sources.
- The standard deduction formula behind the table: derived only; the statute is not in the sources.

- Main session, 2026-11-07 (format for the first frozen schema): the early-distribution penalty marker warns on an IRA or plan payout by a person under 60, not on any person under 60.

## 2026-11-08: marker ids and indexing covers

- Marker ids: all 12 markers have an `id`. Descriptive ids (no from_record id of their own): `wi_credits`, `wi_early_distribution_penalty`, `wi_lump_sum_distribution`; the rest take their first from_record id, so their warning codes are unchanged. `tools.checks --fix-warnings` rewrote the cases' accepted_warnings (the old shared code state_rule_not_modelled:unnamed becomes the new ids); nothing else in the cases changed.
- Indexing covers: `brackets`, `deductions` (including the standard deduction phase-out), `relief_caps` (reliefs.cap). Added `relief_income_tests` (indexed false, assumed) for reliefs.income_test (the 5,000 subtraction's AGI test).
- Assumed entries: searched the archived sources (docling, pypdf and page text) for indexed, inflation, cost of living, adjusted annually and consumer price index, and for statements that figures are fixed; nothing says, so every `assumed: true` stays.
