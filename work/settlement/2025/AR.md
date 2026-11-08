# Settlement: Arkansas, tax year 2025 (round r5)

Settled 2026-11-07 from `work/extract/2025/AR.r5.A.json` and `AR.r5.B.json`.
Sources: `sources/archive/2025/AR/`: the 2025 AR1000F and AR1000NR Instructions (cited "Instr"), the 2025 AR1000F return ("Form") and Subject 206 Pensions and Annuities, revised 2/24/2023 ("S206"). Page numbers are PDF pages.

`uv run python -m tools.compare` reported **127 structured differences** (150 wording).
- **78 decided from the booklet.**
- **49 dropped on scope.** These are B's Additional Tax Credit for Qualified Individuals (46) and B's Low Income Tax Table entry (3).

## Structured differences

| # | Entry | Fields | A | B | Settled | Page |
|---|---|---|---|---|---|---|
| 1 | Bracket starts and derivation rows | 29 | 2% 5,600; 3% 11,150; 3.4% 16,100; 3.9% 26,400; 8 rows | 5,600; 11,200; 16,000; 26,400; 11 rows | **5,600 / 11,200 / 15,990 / 26,400**, with 16 rows. See "Brackets" below. | Instr pp.30-34 table; p.6 "Marginal Income Tax rates for 2025 are 3.9%" |
| 2 | Recapture | 3 | starts_over 94,001 | starts_over 94,701; full_over 100,000; full_rate 0.039 | starts_over **94,701**. Effect `phase_out_lower_brackets` (both had `other`). full_over and full_rate dropped. See "Recapture" below. | Instr p.34 rows and PLEASE NOTE |
| 3 | Principal residence gain (B only) | 3 | — | capital_gains other / exempt / 0 | Kept. The booklet prints it. | Instr p.13 "The gain on the sale of your personal residence is exempt up to $250,000 per taxpayer" |
| 4 | Indexing entries for the standard deduction and the 6,000 exclusion (B only) | 2 | — | not_stated | Kept. The booklet says nothing about either. | Instr p.14; p.11 |
| 5 | Blind credit, deaf credit (B only) | 8 | — | credit 29 each | Kept | Instr p.12 line 7A: "On December 31, 2025, were you deaf? ... blind?" |
| 6 | Head of household / surviving spouse credit, dependent credit (B only) | 8 | — | credit 29 each | Kept | Instr p.12 line 7A "Is your filing status Head of Household or Surviving Spouse?"; line 7B "Multiply the number by $29" |
| 7 | Age-65 credits | 6 (A's 65 Special matched against B's age-65 credit, plus B's 65 Special) | only 65 Special, with cap_per person | age 65 or over, and 65 Special | Both kept: they are separate boxes. cap_per dropped because the credit has no cap. | Instr p.12 "On January 1, 2026, were you age 65 or over?" and "Any taxpayer age 65 or over not claiming a retirement income exemption on line 18 is eligible for an additional $29 (per taxpayer) tax credit"; the Form prints both boxes for each spouse |
| 8 | Social Security and railroad | 9 | one entry for both | one entry each | One entry: item 8 is one sentence with one rule. B's railroad conditions and not_covered kept. | Instr p.11 item 8 |
| 9 | Active-duty military pay (B only) | 3 | — | exempt_in_full wages | Kept | Instr p.11 item 11 "U.S. active-duty military compensation is exempt from tax" |
| 10 | Employer-plan exclusion covers_unclear | 1 | annuity, public_pension_other_state | the same plus roth_conversion | roth_conversion kept in covers_unclear (the booklet is silent). public_pension_other_state moved into **covers**; see "Pensions" below. | Instr p.13 line 18B |
| 11 | IRA death or disability branch (B only) | 6 | folded into the 59.5 entry's conditions | own entry | B's split kept: one entry per branch | Instr p.11 item 13 "Premature distributions made on account of the participant's death or disability also qualify for the exemption" |
| 12 | Additional Tax Credit for Qualified Individuals (B only) | 46 | — | credit 60, stepped to 0 by 27,600 | Dropped. It is a low-income credit, not retirement or Social Security relief (a design.md non-goal). Kept in notes, and in the projection's approximations. | Instr p.25 |
| 13 | Low Income Tax Table as a relief (B only) | 3 | — | all_income entry | Dropped. It is an alternative tax table, not a subtraction, and its rows are not recorded. Kept in notes. | Instr p.28 |

### Not flagged by the compare, but settled

- **`best_of_group` on the two 6,000 entries (A).** Dropped. The entries share one cap per taxpayer ("Total exemptions from all plans described under 12 and 13 cannot exceed $6,000 per taxpayer", Instr p.11). They are not alternatives, and `cap_rule` says so.
- **`cannot_combine_with` military retirement on the 6,000 entries (B).** Dropped. The military exemption uses up the 6,000 first (see the military conflict below).
- **A's `not_covered` on the employer-plan entry.** Dropped: it quotes the IRA premature-distribution sentence.
- **Ids renamed** with an `ar_` prefix.

## Brackets (decision asked for in the dispatch)

The booklet prints no schedule. It prints the Regular Income Tax Table (Instr pp.30-34: 100-dollar rows, one table for every filing status), the 3.9% top rate (p.6), and the formula for 100,001 and over (p.34).

**How the starts were found**
- **Rows.** I parsed 771 of the 897 rows up to the 94,601-94,701 row from the converted texts. pypdf and Docling agree on every row both have. The 126 rows I could not split from the layout all lie inside bands (22,000-25,900, 42,000-45,900, 62,000-65,900, 74,000-74,900, and three single rows).
- **Fit.** With tax taken at the row midpoint and rounded half up:

| Schedule | Rows reproduced exactly | Rows off | Within 1 dollar |
|---|---|---|---|
| A | 731 of 771 | 40 rows 1 dollar high: the 26,500 row (printed 615) and every 1,000 after | all |
| B | 751 of 771 | 20 rows 1 dollar low: the 75,501-75,601 row (printed 2,527, p.33; both converters) and every 1,000 after | all |
| 5,600 / 11,200 / 15,990 / 26,400 | **all 771** | none | all |

- **Why neither reader's set is exact.** Both fail because of the constant subtracted in the 3.9% band:
  - That constant is 0.02 x s1 + 0.01 x s2 + 0.004 x s3 + 0.005 x s4.
  - The table needs it between 419.96 and 419.98. A gives 419.90 and B gives 420.00.
- **What the table leaves open.** On round tens, 150 combinations reproduce every row. For example, 5,600 / 11,150 / 16,120 / 26,400 also works.
  - 5,600 and 26,400 are common to almost all of them, and both readers had them.
  - I chose the combination closest to round hundreds, which keeps B's 11,200.
- **Evidence recorded.** 16 rows sit on both sides of every start. The validator re-computes them without a problem.
- **No derivation formula.** The p.34 formula is evidence for the recapture, not for the five-band schedule.

## Recapture (decision asked for in the dispatch)

**What the table does.**
- Rows 94,001 to 94,601 (3,248 to 3,271) follow the schedule.
- From the 94,701 row (3,296) to the 97,801 row (3,727), each row adds 13 or 14 dollars: 3.9% plus about 10 cents per dollar.
- From the 97,901 row (3,731), each row adds 3 or 4 again. The rows equal 3.9% of income less about 89.
- The note "For $100,001 and over, your tax is $3,809 + 3.9% of the excess over $100,000" equals 3.9% of income less 91.
- Below 94,601, the tax is 3.9% of income less 419.96.

**Decision.** This is a recapture of the lower brackets, but only part of it: about 330 of the 420 benefit is taken back between about 94,550 and 97,850, and the rest stays. I recorded it as faithfully as the schema allows:
- **`effect`:** `phase_out_lower_brackets`.
- **`starts_over`:** 94,701, the first printed row above the schedule.
- **`as_printed`:** the row pattern and the formula, in full.
- **Left out:** `phase_in_width`, `full_over` and `full_rate`.
  - The benefit is not taken back in full.
  - No width is printed.
  - Above 100,000, the formula does not tax all income at one rate (3.9% of 100,000 is 3,900, not 3,809).
  - B's `full_over` of 100,000 is also past the point where the take-back ends.

**Considered and rejected:** adding a 13.9% band to the schedule. A 13.9% band would make the derivation reproduce the table and formula above 94,600 too. But it cannot fit both the 94,601 row and the 94,701 row: the table jumps 25 dollars there. It would also put the recapture in the brackets and in `recapture` at once, and a consumer would count it twice.

## Pensions and the facts most often missed

**(1) Another state's government pension, New York State included: covered by the 6,000 exclusion.** `public_pension_other_state` is in `covers` of `ar_employer_plan_exclusion`.
- **Quote (Instr p.13, line 18B):** "You might be eligible for the $6,000 exemption for retirement or disability benefits provided the distribution was from public or private employment-related retirement systems, plans, or programs. (The recipient does not have to be retired.) The method of funding is irrelevant."
- **Second document (Instr p.11, item 12):** "If you received income from an employer-sponsored retirement plan ... the first $6,000 is exempt from tax."
- **Why `covers`:** no state is named and no limit to Arkansas plans is printed. The test is the kind of plan, not which government pays.
- **What the readers had:** both put it in `covers_unclear`. I moved it.
- **No paying-state entries:** no state is named.

**(2) Arkansas and federal government pensions.** These take the same 6,000 exclusion ("public or private", p.13).
- No contributory test is printed.
- Cost is recovered first under IRC 72 (p.11, item 12).
- Military retirement is exempt in full (p.10, item 1; p.8; line 17).

**(3) Private pensions, IRAs and employer plans.**
- **Private pensions and employer-plan distributions:** in the same 6,000 entry, at any age.
- **Traditional IRAs:** 6,000 from 59 1/2, or before that on account of death or disability (p.11, item 13; line 18B).
- **Shared cap:** one 6,000 per taxpayer across items 12 and 13 (p.11 NOTE). A spouse has their own (S206). A surviving spouse is limited to a single 6,000 (p.11).
- **Roth conversions:** not mentioned in the booklet, so they stay in `covers_unclear`.
- **65 Special credit:** cannot be combined with the exclusions (p.12; S206).

**Conflict on the under-59.5 test, settled for the dispatch.**
- **S206 says:** "You cannot qualify for the $6,000 exemption if: ... You are under 59 ½." It also opens "If you are retired and receiving retirement benefits from an employer-sponsored pension plan".
- **The 2025 instructions say:** for employer plans, "the first $6,000 is exempt from tax" (p.11, item 12) and "(The recipient does not have to be retired.)" (p.13). They print the 59 1/2 test only in the traditional IRA sentences (p.11, item 13; p.13).
- **Settled on the 2025 instructions:** no age test on the employer-plan entry, and 59.5 on the IRA entry.
  - The instructions are for 2025 and state the rule twice.
  - S206 is dated 2023, and its list follows its IRA sentence.
  - The same S206 list also disagrees with the 2025 instructions on military retirees.
- **Where it is recorded:** S206's condition is in the entry's `other_conditions` as a flagged note, not as a test. The projection carries an approximation (understates tax by up to 234 a person under 59.5).

**Conflict on military retirees and the 6,000.**
- **Pages 8 and 13 (line 18B):** none of the 6,000 if the military exemption exceeds 6,000; the remainder may be taken if it is less.
- **Line 17 (p.13):** "Retirees cannot claim both the military retirement exemption and the $6,000 exemption for traditional IRA distributions (A.C.A 26-51-307(f))".
- **S206:** none if you "take the Military Pension exemption and also have an employer sponsored pension".
- **Settled on pages 8 and 18B:** the wording is printed twice and is the most detailed. In the projection this is `cap_reduced_by: military_pension`, with an approximation for the line 17 reading.

**(4) Social Security: exempt.**
- **Instr p.11, item 8:** "Social Security benefits, VA benefits, Workers' Compensation, Railroad Retirement benefits and related supplemental benefits are exempt from tax."
- **Second check:** the Form's income lines 8-22 have no Social Security line, and gross income excludes "income specifically described as exempt on pages 10 and 11" (p.10).

**(5) Schedule, deduction and exemptions.**
- **Schedule:** one table for every printed status (p.30, "Married couples must use the same filing status and tax table"). Status 4 taxes each spouse separately from the same table (p.11, Method A).
- **Standard deduction (p.14 table):** 2,470 single, head of household, surviving spouse, and each spouse under status 4 or 5; 4,940 married filing jointly.
- **No exemptions:** no personal, dependent, age or blind exemption is printed. Instead there are 29-dollar credits (p.12, lines 7A/7B; Form "X $29 ="), recorded as credit reliefs with `credit_amount` 29:
  - personal (each taxpayer and spouse)
  - head of household or surviving spouse
  - age 65 or over on January 1, 2026
  - 65 Special
  - blind
  - deaf
  - each dependent

## One-sided entries

- **Kept (B only):** rows 3 to 7, 9 and 11 above.
- **Kept (A only):** none. A's extra facts (the line 32 additional 10%, the Low Income Tables) are kept in notes.
- **Dropped (B only):**
  - the Additional Tax Credit (scope)
  - the Low Income Tax Table entry (not a relief)
  - `full_over` and `full_rate` on the recapture (they misdescribe it)
  - `cannot_combine_with` military retirement

## Projection choices (`AR.projection.json`)

**Base.** `state_own` is mapped to `federal_agi`, with an approximation. The standard deduction is applied per return. Social Security is exempt.

**Retirement reliefs.** Three entries share one `best_of_group`, so each person gets the better of them. For a person 59.5 or older, this gives the exact shared 6,000 over pensions plus IRAs. Under 59.5, only employer plans count.
- **59.5 or older:** 6,000 over public pensions (own state and other states), private pensions, employer plans and IRAs.
- **Any age:** 6,000 over the same pensions and employer plans, without IRAs.
- **65 Special:** the 29-dollar credit.

Both 6,000 entries:
- have `cap_reduced_by` military pension
- have `needs_input` pension_source

**Exempt in full:** military and railroad retirement.

**Credits:**
- 29 for each person
- 29 more for each person 65 or older

**Recapture.** Copied from the record, with `starts_over` only. An approximation says it understates tax by up to about 330 a year.

**Not modelled:**
- IRA withdrawals before 59.5 on account of death or disability
- head of household and surviving spouse credit (a relief cannot test filing status)
- blind and deaf credits
- dependent credit (warn when there are dependents)
- active-duty pay
- U.S. and Arkansas obligation interest
- principal residence gain

**Approximations:**
- Starting point.
- Rounding in the table.
- Recapture.
- **Status 4 option (overstates tax).** A couple can choose to file status 4. For similar incomes this lowers the tax by up to about 420.
- Itemizing.
- **The two conflicts.** The S206 age test and line 17 on military retirees.
- Roth conversions and annuities left out of the exclusions.
- Municipal bonds and Treasury interest.
- Low Income Tables and the Additional Tax Credit.
- Form AR1000D gains.
- The line 32 early-distribution tax.
- The best-of choice.

**Indexing.** Brackets indexed (Instr p.30, "Current year indexed tax brackets"). Deductions, relief caps and credits are not indexed (assumed).

## Validator

```
data/states/2025/AR.record.json: ok
data/states/2025/AR.projection.json: ok
```

## Unsure

- **Bracket starts.** 11,200 / 15,990 is one choice from a set of 150 on round tens. Every set in it reproduces the 771 parsed rows; 126 rows inside bands were not parsed. The website's "indexed tax brackets", not in the sources, would settle it.
- **The recapture's mechanics.** The jump between the 94,601 and 94,701 rows, and the leftover benefit of about 89-91, are not explained anywhere in the sources. Recording `starts_over` alone loses the size, which is kept only in `as_printed`.
- **`public_pension_other_state` in `covers`.** This rests on "public or private employment-related retirement systems" with no state named. Neither reader went that far.
- **The S206 under-59.5 test.** Settled against S206 because S206 is older and not year-specific. If DFA applies it to employer plans, people under 59.5 lose the exclusion.
- **Line 17's military/IRA sentence** (A.C.A. 26-51-307(f)) disagrees with pages 8 and 13. I followed the longer text.

## 2026-11-08: marker ids and indexing covers

- Marker ids given: first from_record id (warning code unchanged): `ar_traditional_ira_exclusion_death_disability`, `ar_head_of_household_credit`, `ar_blind_credit`, `ar_dependent_credit`, `ar_active_duty_military_pay_exempt`, `ar_us_and_arkansas_obligation_interest_exempt`, `ar_principal_residence_gain`.
- Indexing covers: `brackets` -> `brackets`; `deductions` -> `deductions`; `relief_caps` -> `reliefs.cap`; `credits` -> `reliefs.credit_amount`; `recapture_threshold` -> `recapture`.
- Added `recapture_threshold` (indexed false, assumed): the 94,701 start of the partial recapture is read from the Regular Income Tax Table, whose page says 'Current year indexed tax brackets are available on our website' (PDF page 30); that sentence speaks of the brackets, not of where the table departs from them, so the threshold is not taken as indexed.
- Every `assumed` answer was checked again against the archived sources (searched for indexed, inflation, cost-of-living, adjusted annually, each year, CPI, fixed): none says, so all stay `assumed: true`.
- Warning codes unchanged (every id is the marker's first from_record id).
