# Settlement: Georgia, tax year 2025 (round r5)

Settled 2026-11-07 from `work/extract/2025/GA.r5.A.json` and `GA.r5.B.json`. The round-1 readings
(`GA.A.json`, `GA.B.json`, older format) were consulted as a third reading.
Sources: `sources/archive/2025/GA/`:
- `2025_IT-511_Booklet_2026.02.16` (the instructions, with the full Form 500 and Schedule 1 bound in at PDF pages 41-49; cited "p.").
- `2025GA500` (the standalone Form 500, the same form; Schedule 1 pages 1-3 at its PDF pages 7-9).
- `retirees-faq.page.txt` (DOR Retirees FAQ).

Page numbers are PDF pages.

`uv run python -m tools.compare` reported **74 structured differences** (88 wording). All 74 were settled against the booklet:
- 68 come from one disagreement over what the retirement income exclusion covers. `covers` is part of the compare key, so each of the three age branches failed to match as a whole: 11 + 12 + 11 fields on each side. The caps, ages, `cap_per` and sub-limits agreed between the readers.
- 6 are A's two one-sided reliefs, which were kept.

Settled record vs A: 68 differences; vs B: 74. Both are explained by the rows below.

## Structured differences

| # | Entry | Fields | A | B | Settled | Page |
|---|---|---|---|---|---|---|
| 1 | Retirement exclusion (62-64, disabled under 62, 65+): `wages`, `self_employment` | part of 68 | in `sub_limits` only, not in `covers` | in `covers`, with the `sub_limits` | **B**. Kept both readers' 5,000 sub-limits. `cap_rule` says it is one combined 5,000 on earned income. | p.48 Schedule 1 page 2 lines 1-5: "Salary and wages", "Other Earned Income", "Maximum Earned Income" 5,000, "The lesser of Line 3 or 4". p.21: "Up to $5,000 of the maximum allowable exclusion may be earned income". Second document: p.31: "only $5,000 of the wages can be included in the RIE". |
| 2 | Retirement exclusion: `employer_plan_distribution` | part of 68 | `covers` | `covers_unclear` | **B** (`covers_unclear`). | p.48 lines 11-12 name only "Taxable IRA Distributions" and "Taxable Pensions". No page names 401(k), 403(b), 457 or employer plans. Additions item 3 (p.20) mentions only Form 4972 lump sums from "employee benefit plans". |
| 3 | Retirement exclusion: `public_pension_other_state` | part of 68 | not listed: no separate rule, so it "falls under the generic taxable pensions line" | `covers_unclear` | **`covers`** (neither reader had it there). It is the same entry as Georgia's own and federal pensions, by rule 15a. | p.48 line 12 "Taxable Pensions": no limit by payer. p.13: "Full-year residents are taxed on all income, except tax-exempt income, regardless of the source or where derived." p.24 leaves out only "Social Security and Railroad Retirement ..., exempt interest, or other income that is not taxable to Georgia". |
| 4 | Social Security and Railroad Retirement subtraction (A only) | 3 | relief, `return` | — | **Kept** as `ga_social_security_railroad`: printed, and it is Social Security relief. | p.22 Subtractions item 5. Form 500 Schedule 1 line 8 (p.47). |
| 5 | U.S. obligations interest (A only) | 3 | relief, `return` | — | **Kept** as `ga_us_obligations_interest`: printed, and kept for SC as well. The FNMA/GNMA/FHLMC/repurchase exclusion is in `not_covered`. | p.22 Subtractions item 4 and Note. Schedule 1 line 10. |

Both readers had `roth_conversion` and `military_pension` in `covers_unclear`. Both stay there (see below).

### Not flagged by the compare, but settled

- **Ids** renamed with a `ga_` prefix. The readers' ids differed (`military_base` and `military_exclusion_base`).
- **Teacher's Retirement System adjustment** (Subtractions item 12, p.22). Neither reader recorded it, and it is not added as a relief:
  - It is the only Georgia-specific government pension rule. It subtracts contributions paid 1987-07-01 to 1989-12-31 that Georgia already taxed. It is not relief on pension income.
  - An uncapped entry covering `public_pension` would read as a full exemption: the compare normalises it to `exempt_in_full`.
  - It is recorded in notes.
- **Military exclusion total.** Schedule 1 page 3 line 7 prints 35,000 as the "Total additional Military Exclusion allowed". This is noted in `cap_rule`. The two-entry split (17,500 + 17,500) that both readers used is kept.
- **Disability branch.** B's form-line detail ("date and type of disability on lines 7c/7f") is kept in `other_conditions`. "each spouse must qualify on a separate basis" is dropped from `other_conditions`, because `basis: each_person` already says it.
- **ABLE note.** B's ABLE line in `not_covered` is dropped. It concerns ABLE contributions, not what the exclusion covers.

## One-sided entries

- Kept (A only): rows 4 and 5.
- Dropped: none from either reader.
- Not added (neither reader): these are out of scope (credits other than retirement or Social Security relief) and listed in notes:
  - the Low Income Credit (federal AGI under 20,000; p.17, p.35);
  - the Eligible Itemizer Tax Credit (up to 300; p.9);
  - Path2College;
  - the 1981-86 IRA/Keogh/SEP basis subtraction (item 7).

## The five required facts, with quotes

1. **Another state's government pension, and a New York State pension.** In `covers` as `public_pension_other_state`, in the same retirement-exclusion entries as Georgia's own pensions. No rule specific to another state's or New York's pensions is found in the booklet.
   - p.48 line 12: "Taxable Pensions".
   - p.13: "Full-year residents are taxed on all income, except tax-exempt income, regardless of the source or where derived."
   - p.21: "The maximum retirement income exclusion is $35,000 for taxpayers who are: A. 62 - 64 years of age, or B. less than 62 and permanently disabled ... The maximum retirement income exclusion is $65,000 for taxpayers who are 65 years of age or older."
2. **Georgia's own and federal government pensions.** These have no exemption of their own and fall under the same exclusion. The only own-state rule is the TRS 1987-89 contribution adjustment: p.22 item 12, "Adjustment for teachers retired from the Teacher's Retirement System of Georgia for contributions paid between July 1, 1987, and December 31, 1989, that were reported to and taxed by Georgia." No contributory-plan test is printed.
3. **Private pensions, IRAs, employer plans and Roth conversions.**
   - Private pensions and IRA distributions are in `covers`: p.48 line 11 "Taxable IRA Distributions" and line 12 "Taxable Pensions". The FAQ says "Retirement income includes items such as: interest, dividends, net rentals, capital gains, royalties, pensions, annuities".
   - Employer-plan distributions are in `covers_unclear` (row 2).
   - Roth conversions are in `covers_unclear`. p.12 says "The provisions concerning taxability and conversion from a traditional IRA to a Roth IRA are the same for Georgia and the Internal Revenue Service". It does not say whether a conversion counts on line 11.
   - Caps: 35,000 at 62-64 (or under 62 and disabled) and 65,000 at 65 or older, per person. These are printed on p.21 and again in the Schedule 1 page 2 footnote (p.48; GA500 p.8): "*If age 62-64 or less than age 62 and permanently disabled enter $35,000, or if age 65 or older enter $65,000."
   - No income test is printed.
4. **Social Security: exempt.** p.22 item 5: "Social Security or Railroad Retirement (Tier 1 and Tier 2) paid by the Railroad Retirement Board included in Federal adjusted gross income." Checked against two other documents:
   - Schedule 1 line 8 (p.47): "Social Security Benefits (Taxable portion from Federal return)".
   - Retirees FAQ: "No. Taxable Social Security and Railroad Retirement on the Federal return are exempt from Georgia Income Tax."
5. **Rate, deduction and exemptions.**
   - Rate: a flat 5.19% for every status. p.17 Line 16: "Multiply the amount on Line 15c by 5.19%". p.9: "Effective January 1, 2025, the income tax rate is 5.19%". Form 500 line 16 says the same.
   - No schedule, table, surtax or recapture is printed.
   - Standard deduction (p.16 Line 11; repeated in the p.13 filing table): 24,000 married filing jointly. 12,000 for single, married filing separately, head of household and qualifying surviving spouse. It applies only to a filer who does not itemize federally.
   - Dependent exemption: 4,000 per dependent (p.17 Line 14; Form 500 line 14, "Multiply by $4,000").
   - No personal, spouse, age-65 or blind amount is printed.
   - Indexing: not stated.

Earned income: the FAQ says "the first $4000.00 of earned income". The booklet and form print 5,000 (p.21, p.24 example, Schedule 1 line 4), and the booklet is followed. Both readers did the same.

## Projection choices (`GA.projection.json`)

- **Base.** Starts from federal AGI. The Georgia standard deduction is taken per return. The dependent exemption is in `not_modelled` (warn `has_dependents`).
- **Reliefs modelled.**
  - Retirement exclusion at 62-64 (35,000) and at 65 or older (65,000), per person.
    - `covers` is the record's, with `public_pension_other_state` included.
    - The wages and self-employment sub-limits are 5,000 each.
    - `needs_input: pension_source`, because military retirement is treated differently.
  - Base military exclusion: 17,500, for a person aged 61 or younger.
  - Railroad retirement: exempt in full.
  - Social Security: `exempt`.
- **Not modelled.**
  - The disability branch (warn `has_pension`).
  - The additional military 17,500. It turns on the person's own Georgia earned income, and no measure holds that (warn `has_military_pension`).
  - Dependents.
  - U.S. obligations interest (warn `never`, with an approximation).
- **Approximations.**
  - Employer-plan distributions, Roth conversions, and military retirement at 62 or older are left out of the exclusion. These overstate tax.
  - The combined 5,000 earned-income limit is split into one 5,000 for wages and one for self-employment. This understates tax.
  - Joint-property 50% allocation.
  - The standard deduction is always taken.
  - Treasury interest.
  - Own-state bonds.
  - The Form 4972 lump-sum addition.
  - The Low Income Credit.
- **Indexing.** Brackets, deductions and relief caps: `indexed: false, assumed: true`.

## Validator

```
data/states/2025/GA.record.json: ok
data/states/2025/GA.projection.json: ok
```

## Unsure

- **`employer_plan_distribution` in `covers_unclear`.** This is the most consequential call. If "Taxable Pensions" includes 401(k)/403(b)/457 payouts, which the booklet does not say, the projection overstates Georgia tax for those retirees: up to 3,373.50 a year for a person 65 or older. The statute or the DOR should settle it.
- **`public_pension_other_state` in `covers`.** This is read from the lack of any limit by payer on "Taxable Pensions" together with p.13. No sentence names another state's pensions.
- **Military retirement at 62 or older inside the general exclusion.** Not stated either way. Also not stated: whether an under-62 disabled military retiree can take both the military and the disability exclusion.
- **The 5,000 earned-income limit.** It is one combined limit, but the schema holds sub-limits per income kind, so it is written as two 5,000 sub-limits, with `cap_rule` saying so.

## 2026-11-07: maintainer decision

The owner decided (docs/decisions.md, "2026-11-07: maintainer decisions on NC military retirement and 401(k)/IRA
coverage in GA, HI, MS") that Georgia's retirement income exclusion covers 401(k), 403(b) and 457 payouts and
Roth conversions. This settles row 2 above and the Roth conversion item, both left in `covers_unclear` at
settlement. The "Unsure" item on `employer_plan_distribution` is closed.

### What changed

- **Record** (`GA.record.json`), all three exclusion entries (`ga_retirement_exclusion_62_64`,
  `ga_retirement_exclusion_disabled`, `ga_retirement_exclusion_65_plus`):
  - `employer_plan_distribution` and `roth_conversion` moved from `covers_unclear` to `covers`.
    `covers_unclear` now holds only `military_pension`.
  - The `cite.section` now names the p.24 worksheet lines and exclusions, p.12 and p.16 Line 8.
  - Notes:
    - The settlement note on `employer_plan_distribution` now ends by pointing to the maintainer decision.
    - A new "Maintainer decision 2026-11-07" note quotes the sources listed below.
    - The Roth conversion note now says conversions are in `covers`.
- **Projection** (`GA.projection.json`):
  - `employer_plan_distribution` and `roth_conversion` added to `covers` on `ga_retirement_exclusion_62_64` and
    `ga_retirement_exclusion_65_plus`.
  - `record.sha256` updated.
  - Two approximations removed:
    - "Distributions from employer plans (401(k), 403(b), 457) are left out of the retirement exclusion ..."
      (overstates_tax, up to 3,373.50 a year).
    - "Roth conversions are left out of the retirement exclusion ..." (overstates_tax).
  - No approximation or warning is added: the projection now does what the sources say. The disabled branch
    stays in `not_modelled` (warn `has_pension`). Its text says "the same retirement income as the 62-64
    branch", so it now includes these kinds without a change.

### Why: the sources, with pages

All from the 2025 IT-511 booklet (`2025_IT-511_Booklet_2026.02.16`), unless another file is named.

- **The worksheet takes every kind of unearned income.** Schedule 1 page 2 lines 6-13 (p.48; `2025GA500` p.8),
  repeated in the p.24 part-year example (lines 6-13): "Interest Income", "Dividend Income", "Alimony",
  "Capital Gains (Losses)", "Other Income (Losses)", "Taxable IRA Distributions", "Taxable Pensions",
  "Rental, Royalty, Partnership, S Corp, etc.".
- **Only income not taxable to Georgia is left out.** p.24: "Social Security and Railroad Retirement paid by
  the Railroad Retirement Board, exempt interest, or other income that is not taxable to Georgia should not be
  included in the retirement income exclusion calculation." p.24 also leaves out income "from lotteries,
  gambling, illegal sources, or similar income".
- **A 401(k), 403(b) or 457 payout is Georgia income.** Georgia starts from federal AGI (p.16 Line 8), so a
  taxable 401(k), 403(b) or 457 payout is taxable to Georgia. It goes on "Taxable Pensions" (or "Other
  Income"), and it is not among the kinds left out.
- **A Roth conversion is a taxable IRA distribution (line 11).** p.12: "The provisions concerning taxability
  and conversion from a traditional IRA to a Roth IRA are the same for Georgia and the Internal Revenue
  Service."
- **DOR Retirees FAQ** (`retirees-faq.page.txt`): "Retirement income includes items such as: interest,
  dividends, net rentals, capital gains, royalties, pensions, annuities, and the first $4000.00 of earned
  income."
- **Georgia rule 560-7-4-.02** says "income from pensions and annuities, and other similar income" and agrees.
  It is **not archived**, because rules.sos.ga.gov refuses automated download. The record names it in a note
  but does not cite it as a source.

### What it means in dollars (5.19% flat rate)

- **65 or older, 401(k) payout.** A single person aged 70 with a 40,000 401(k) payout and no other covered
  income now excludes 40,000. Georgia tax falls by 5.19% x 40,000 = 2,076.00.
- **The most a person can save.** 3,373.50 a year at 65 or older (65,000 of room). 1,816.50 at 62-64 (35,000
  of room).
- **62-64, Roth conversion.** A person aged 63 with a 10,000 pension and a 50,000 Roth conversion has
  35,000 - 10,000 = 25,000 of room left. Georgia tax falls by 5.19% x 25,000 = 1,297.50.
- **The cap still binds.** Above the cap nothing changes. Someone aged 65 or older whose IRA payouts, pensions
  and investment income already reach 65,000 gets no further relief from a 401(k) payout or a conversion.
- **Planning effect.** Before, the projection steered a 62-plus Georgia household away from converting, or
  toward IRA rather than 401(k) withdrawals, because only the IRA money was excluded. Both now share the same
  per-person room.

### Checks (`uv run python -m tools.checks --year 2025 --state GA`)

- The run printed "GA: 15 case(s), ok" and reported no coverage problems. Warnings are unchanged because
  `not_modelled` did not change.
- No case's expected figures change. None of the 15 cases in `checks/2025/GA/` has `employer_plan_distribution`
  or `roth_conversion` income, and every other covered kind is unchanged.
- The new coverage is not tested by any case. `tools.checks` asks for cases per relief, not per income kind,
  so it does not flag this. A case with a 401(k) payout and one with a Roth conversion, both under the cap,
  should be written (checks were read-only for this change).

### Format gaps

- **One publication per `cite`.** A relief's `cite` holds one publication. The Retirees FAQ, a second source
  for this coverage, is quoted in `notes` only.
- **Rule 560-7-4-.02.** There is no field for a source that agrees but is not archived. It is in a note.

### Still unsure

- `military_pension` at 62 or older stays in `covers_unclear`, and its overstating approximation stays. The
  same "every kind of unearned income" reading would put it on "Taxable Pensions". But the maintainer decision does
  not cover it, and no page names military retirement inside the general exclusion.

### Validator

```
data/states/2025/GA.record.json: ok
data/states/2025/GA.projection.json: ok
```

## 2026-11-08: marker ids and indexing covers

- Marker ids given: first from_record id (warning code unchanged): `ga_retirement_exclusion_disabled`, `ga_military_exclusion_additional`, `ga_dependent_exemption`, `ga_us_obligations_interest`.
- Indexing covers: `brackets` -> `brackets`; `deductions` -> `deductions`; `relief_caps` -> `reliefs.cap`.
- Every `assumed` answer was checked again against the archived sources (searched for indexed, inflation, cost-of-living, adjusted annually, each year, CPI, fixed): none says, so all stay `assumed: true`.
- Warning codes unchanged (every id is the marker's first from_record id).

## 2026-11-08: indexing settled from statutes

- `brackets` (projection `brackets`): not_indexed, O.C.G.A. 48-7-20(a.1): one flat-rate band from 0. Record `brackets` added as no.
- `deductions` (projection `deductions`): not_indexed, O.C.G.A. 48-7-27(a)(1)(B). Record `ga_standard_deduction` added as no. HB 463 of 2026 (scheduled increases from 2026) not confirmed enacted.
- `relief_caps` (projection `reliefs.cap`): not_indexed, O.C.G.A. 48-7-27(a)(5)(A)(xiii) and (a)(5.1)(A). Record `ga_retirement_exclusion_62_64`, `ga_retirement_exclusion_65_plus`, `ga_military_exclusion_base` added as no.
- Code text read in bill text on legis.ga.gov (HB 463 of 2026 quoting existing law) and the 2022 signed HB 1064; the O.C.G.A. itself is on a Lexis site that could not be read. The existing `all_other` entry is left.
