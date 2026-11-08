# Settlement: New York, tax year 2025

- Readings: `work/extract/2025/NY.r3.A.json`, `work/extract/2025/NY.r3.B.json` (round r3)
- Sources: `sources/archive/2025/NY/`: Instructions for Form IT-201 (2025) (`it201i`), Form IT-201 (2025)
  (`it201_2025_fill_in`), and the Department's page "Information for retired persons"
  (`information_for_seniors.page.txt`)
- Outputs: `data/states/2025/NY.record.json`, `data/states/2025/NY.projection.json`
- Settled: 2026-11-07

## Comparison

`uv run python -m tools.compare` reported **112 structured differences** (159 wording differences). They
come down to five disagreements:

| # | Lines | Field | A | B | Source | Settled |
|---|---|---|---|---|---|---|
| 1 | 74 (`recapture[0..17]`) | Tax computation worksheets: grouping by filing status, `effect`, qualifying surviving spouse keys | 18 entries: one per status, with married separate entries copying the single worksheets and no qualifying surviving spouse key; worksheets 1, 7, 12 `flat_top_rate_on_all_income`, the tiered worksheets `other`, 6/11/16 one `all` entry | 13 entries: worksheets 7 and 12 grouped, 6/11/16 grouped, qualifying surviving spouse keyed with married joint, married separate with single; every entry `phase_out_lower_brackets` except 6/11/16 | IT-201-I PDF pages 34-39, all 16 worksheets read line by line. Headings: "Married filing jointly and qualifying surviving spouse" (1-6), "Single and married filing separately" (7-11), "Head of household" (12-16). Worksheets 1, 7, 12: line 3 = line 38 x 5.5% or 6%, and that is the tax when NY AGI is $157,650 or more, phased in over $50,000 from $107,650. Worksheets 2-5, 8-10, 13-15: schedule tax + Recapture Base + Incremental Benefit x (lesser of NY AGI over the start or $50,000) / $50,000. Worksheets 6, 11, 16: 10.9% of line 38 when NY AGI is over $25,000,000. | 16 entries, one per worksheet, each keyed by every status its heading names. 1, 7, 12: `flat_top_rate_on_all_income` with `full_over` 157,650 and the printed rate (A). 2-5, 8-10, 13-15: `phase_out_lower_brackets` (B), no `full_over`/`full_rate` because none is printed; Recapture Base, Incremental Benefit and the taxable-income range in `as_printed`. 6, 11, 16: `flat_top_rate_on_all_income`, 10.9%, width 0 (both). |
| 2 | 16 (`base.deductions` standard deduction) | Layout | one entry with an amount per filing status, plus single 3,100 | one entry per status, plus single 3,100 | IT-201-I PDF page 11 table: 3,100 / 8,000 / 16,050 / 8,000 / 11,200 / 16,050. Both readers have these amounts. | A's one entry (`by_status`), plus the 3,100 dependent-filer entry |
| 3 | 12 (beneficiary exclusion, two relief keys) | `who.basis`, `cap_per` of the beneficiary branch of the exclusion | `return`, `return` | `each_person`, `person` | IT-201-I PDF page 10, Beneficiaries; the Department's page, Receiving distributions as a beneficiary (Example 3: John's own 15,000 plus 25,000 inherited, "maximum ... allowed ... is $20,000"; "The maximum exclusion allowable, from the total of all sources ... may not exceed $20,000"). The limit belongs to the beneficiary taxpayer. | B: `each_person`, 20,000 per person; the decedent's shared 20,000 in `cap_rule` |
| 4 | 9 (B only) | NY 529 college savings deduction (line 30) as a relief covering `other_income` | absent | present | IT-201-I PDF page 10, Line 30: a deduction for contributions to a college savings account (5,000, or 10,000 joint). | Dropped: not relief for a kind of retirement income (out of scope for `reliefs`; it would also have misdescribed a contribution deduction as covered income). Named in the record's left-out note. |
| 5 | 1 (B only) | indexing entry `dependent_exemption` | absent | `not_stated` | No inflation or indexing statement in any of the three documents (the only "inflation" text is the inflation refund check, line 25). | Kept as `not_stated` |

Every amount in the recapture entries (thresholds, rates, the ten Recapture Base and ten Incremental Benefit
amounts) was the same in both readings and matches the worksheets. The threshold differences the comparison
printed came from the grouping, not from different figures.

**Settled: 112. Decided from the booklet: 86** (recapture 74, beneficiary 12). The other 26 were decided by
the extraction brief and schema with the figures checked against the booklet: the standard deduction layout
(16; same amounts, page 11), the 529 entry dropped as out of scope (9), the indexing entry kept (1).

## The recapture (known point 1)

All 16 worksheets were read in `it201i.pypdf.txt` and `it201i.docling.md` (pages 34-39). Recorded per
worksheet (MFJ/QSS = married joint and qualifying surviving spouse; S/MFS = single and married separate):

| WS | Statuses | NY AGI over | Line 38 range | Rule |
|---|---|---|---|---|
| 1 | MFJ/QSS | 107,650 | 161,550 or less | 5.5% of line 38, phased in over 50,000; full at 157,650 |
| 2 | MFJ/QSS | 161,550 | over 161,550 to 323,200 | schedule + 333 + 807 x share |
| 3 | MFJ/QSS | 323,200 | to 2,155,350 | schedule + 1,140 + 2,747 x share |
| 4 | MFJ/QSS | 2,155,350 | to 5,000,000 | schedule + 3,887 + 60,350 x share |
| 5 | MFJ/QSS | 5,000,000 | over 5,000,000 | schedule + 64,237 + 32,500 x share |
| 6 | MFJ/QSS | 25,000,000 | any | 10.9% of line 38 |
| 7 | S/MFS | 107,650 | 215,400 or less | 6% of line 38, phased in; full at 157,650 |
| 8 | S/MFS | 215,400 | to 1,077,550 | schedule + 568 + 1,831 x share |
| 9 | S/MFS | 1,077,550 | to 5,000,000 | schedule + 2,399 + 30,172 x share |
| 10 | S/MFS | 5,000,000 | over 5,000,000 | schedule + 32,571 + 32,500 x share |
| 11 | S/MFS | 25,000,000 | any | 10.9% of line 38 |
| 12 | HOH | 107,650 | 269,300 or less | 6% of line 38, phased in; full at 157,650 |
| 13 | HOH | 269,300 | to 1,616,450 | schedule + 787 + 2,289 x share |
| 14 | HOH | 1,616,450 | to 5,000,000 | schedule + 3,076 + 45,261 x share |
| 15 | HOH | 5,000,000 | over 5,000,000 | schedule + 48,337 + 32,500 x share |
| 16 | HOH | 25,000,000 | any | 10.9% of line 38 |

("share" = lesser of NY AGI over the start or 50,000, divided by 50,000, rounded to four decimals; every
worksheet except 6, 11 and 16 applies only up to NY AGI of 25,000,000.)

- **Schema limit:** the record schema has no field for a worksheet's Recapture Base or Incremental Benefit
  amount, or for its taxable-income range. They are kept in each entry's `as_printed` (said so in the record
  notes too).
- **Arithmetic check** (in the record notes, marked as a check, not a printed statement): in every tiered
  worksheet, Recapture Base + Incremental Benefit = band rate x band start - schedule tax at the start, within
  rounding (for example 333 + 807 = 1,140 = 6% x 161,550 - 8,553; 1,140 + 2,747 = 3,887 against
  6.85% x 323,200 - 18,252 = 3,887.20), and each Recapture Base is the
  previous worksheet's full amount. So once NY AGI is 50,000 over a worksheet's start, the tax equals the
  band's rate on all of line 38. Checked by script for all ten tiered worksheets.
- **Projection:** 11 layer-2 entries, each a `flat_top_rate_on_all_income` phase-in on NY AGI (`state_agi`):
  the 107,650 entries for MFJ/QSS (5.5%) and for S/MFS/HOH (6%); one entry per tiered worksheet with
  `full_rate` = the band's schedule rate and `full_over` = start + 50,000 (eight sums in `derived_figures`);
  worksheets 5, 10 and 15 merged into one `all` entry (same start, width and rate in layer 2); 6, 11 and 16 one
  `all` entry at 10.9%. The approximations entry says how to read them (pick the entry by taxable income, as
  the booklet does, phase by NY AGI) and the error: exact for worksheets 1, 6, 7, 11, 12, 16 and for every
  worksheet once NY AGI is 50,000 over its start; otherwise **understates** by the Recapture Base x
  (1 - share). For a standard-deduction household with no dependents (checked by script against a worksheet
  implementation):

  | NY AGI | Married joint: recapture / error | Single | Head of household |
  |---|---|---|---|
  | 150,000 | 282 / 0 | 481 / 0 | 666 / 0 |
  | 300,000 | 1,140 / 0 | 2,399 / 0 | 2,192 / -304 |
  | 1,000,000 | 3,887 / 0 | 2,399 / 0 | 3,076 / 0 |

  Largest understatement up to 1,000,000: about 770 MFJ, 480 single, 610 HOH; above that about 2,640 MFJ
  near 2.17 million and 43,550 MFJ near 5.02 million.

## Known points 2 to 5

- **Pension and annuity income exclusion (line 29)**: age 59.5 ("59½ before January 1, 2025"; turning 59.5
  during 2025 counts only later income), PDF page 9 and the Department's page. Covers `private_pension`,
  `ira_distribution` ("periodic and lump-sum payments from an IRA"), `employer_plan_distribution` (457, 403(b),
  401(k), Keogh, cafeteria plan), `annuity`. **`public_pension_other_state`: covered.** Line 26 (page 9) lists
  only NYS, its localities and the federal government, and says payments "attributable to your employment by an
  employer other than a New York public employer ... may qualify for the pension and annuity income
  exclusion"; line 29 takes pension income "not from a New York State or local government pension plan or
  federal government pension plan", and its first qualifying kind is "periodic payments for services you
  performed as an employee before you retired". Both readers had it in `covers_unclear`; moved to `covers`.
  Each spouse has their own 20,000 (page 10, Married taxpayers, with its example; the Department's page),
  `cap_per: person`, `basis: each_person`. **Roth conversions: `covers_unclear`.** Neither document mentions
  conversions; the SECURE 2.0 sentence is about employer contributions designated Roth. The projection leaves
  conversions out of `covers` and has an approximation (overstates tax, up to 1,200 a year at 6%).
- **Government pensions (line 26)**: NYS, NY localities, federal including military and DC, any age, no cap
  (page 9; the Department's page "regardless of your age or of the form the payment(s) take"). Recorded
  `exempt_in_full` covering `public_pension` and `military_pension` (both readers had `subtraction` with no
  cap; same effect). One entry, because the line treats them alike. The ORP portion, supplemental annuity and
  457 exclusions are in `not_covered`; FERS-only TSP, QDRO and beneficiary rules in `other_conditions`.
- **Social Security**: exempt. Form IT-201 page 2, line 15 "(also enter on line 27)" and line 27 under New York
  subtractions; second document: the Department's page, Subtractions, Social Security ("may be subtracted").
  No income test. The instructions have no separate line 27 text.
- **IRA rollovers from government pensions** (the Department's page, Rollovers): recorded as their own relief,
  `gov_pension_ira_rollover`, `exempt_in_full` for `ira_distribution`, with the printed pro-rata formula
  (rollover contributions / IRA value including the distribution, at the distribution, x amount distributed),
  the word "Generally", the record-keeping sentence, and "interest or gains ... may be eligible for the Pension
  and annuity income exclusion" in `not_covered`. Neither reader had an entry (B a note). Projection:
  `not_modelled` (`warn_when: always`), with FERS TSP distributions, and an approximation (overstates).

## One-sided entries and other changes

- NY 529 deduction (B only): dropped, see table row 4.
- Indexing `dependent_exemption` (B only): kept, `not_stated`. A's indexing cites dropped (a cite to where the
  figure is printed adds nothing to `not_stated`).
- `social_security_subtraction`, `railroad_tier1_subtraction`, `railroad_tier2_subtraction`,
  `us_government_interest_subtraction`: both readers had them as uncapped `subtraction`; recorded as
  `exempt_in_full` (the whole amount in federal AGI is subtracted), as for line 26.
- Beneficiary exclusion: `public_pension_other_state` added to `covers` to match the main branch.
- Notes from both readers merged; left-out items listed in one note (long-term residential care, disability
  exclusion itself, 529, inflation refund check, 414(h) addition, college tuition, household credit); NYC,
  Yonkers and MCTMT out of scope.

## Facts checked against a second line or document

- **Brackets**: three schedules on PDF page 33, read in both converter texts. The pypdf text places the status
  headings after their tables; docling and the worksheet limits fix the assignment. Base taxes check (686,
  340, 512, and 8,553 = 1,202 + 5.5% x 133,650). Married separate = single (heading), qualifying surviving
  spouse = married joint. Same in both readings.
- **Standard deduction**: PDF page 11 table, and form line 34. No personal, age-65 or blind amount found;
  dependent exemption 1,000 (page 11, line 36, and form line 36).
- **Retirement reliefs**: line 26 and line 29 read on instruction pages 9-10, form lines 26 and 29, and the
  Department's page; cap 20,000, age 59.5 and covered kinds as above.
- **Social Security**: form line 27 and the Department's page, as above.

## Projection

- Brackets: the four printed schedules; QSS uses married joint.
- Base: federal AGI less the standard deduction (per return, all five statuses). Dependent exemption and the
  3,100 dependent-filer amount `not_modelled`.
- Reliefs: `gov_pension` (`exempt_in_full`, public and military, `needs_input: pension_source`),
  `pension_annuity_exclusion` (20,000 per person from 59.5, `needs_input: pension_source`), railroad retirement
  `exempt_in_full`. Social Security through `treatment: exempt` only, so it is not subtracted twice.
- `not_modelled`: beneficiary branch (`person_in_age_range` 0-59), government money in IRAs and FERS TSP
  (`always`), disability exclusion sharing the cap (`never`), dependent exemption (`has_dependents`),
  dependent-filer standard deduction (`never`), U.S. government interest (`never`).
- Approximations: recapture (above), Tax Table below 65,000, Roth conversions, the 59.5 year, itemizing,
  government IRA/TSP money, beneficiaries, dependents, dependent filer, Treasury interest, New York bonds.
- Indexing: brackets, deductions, the exclusion and the recapture thresholds `indexed: false, assumed: true`.

## Validator

```
data/states/2025/NY.record.json: ok
data/states/2025/NY.projection.json: ok
```

## Unsure

- **How layer 2's recapture entries are read**: the schema does not say how a consumer picks one of several
  entries. The approximation's text gives the rule (by taxable income, phased by NY AGI); a consumer that picks
  by NY AGI instead gets errors near band edges (script, MFJ standard deduction: about 1,140 understated near
  323,250 and 64,140 near 5,000,050, and up to 16,700 overstated near 2.17 million). Probably the schema needs a taxable-income range field and a
  base-amount field.
- `effect` for the tiered worksheets: `phase_out_lower_brackets` follows the worksheets' own words (Recapture
  Base, Incremental Benefit); `flat_top_rate_on_all_income` would describe their fully phased-in result, which is
  arithmetic, not printed.
- `public_pension_other_state` as covered by line 29 is read from two sentences together (line 26's "may qualify
  for the pension and annuity income exclusion" and line 29's qualifying list); no sentence names other states.
- `gov_pension_ira_rollover` `warn_when: always` is noisy, but no narrower trigger fits (the money sits in an IRA,
  not a pension).
- Railroad Tier 1: the Department's page says it is claimed on line 27 with Social Security; a projection that
  holds Tier 1 as Social Security and Tier 2 as railroad retirement gets both right.

- Main session, 2026-11-07 (format for the first frozen schema): the beneficiary marker warns on an IRA or plan payout by a person under 60 (it warned on any person under 60); the government-plan rollover marker warns on has_retirement_account_distribution (it warned on every run). An inherited pension (not IRA) under 60 now gets no warning; rare.

## 2026-11-08: marker ids and indexing covers

- Marker ids: all 6 markers have an `id`. Each takes its first from_record id, so warning codes are unchanged.
- Indexing covers: `brackets`, `deductions`, `pension_annuity_exclusion` (reliefs:pension_annuity_exclusion), `recapture`. No split needed.
- Assumed entries: searched the archived sources (docling, pypdf and page text) for indexed, inflation, cost of living, adjusted annually and consumer price index, and for statements that figures are fixed; nothing says, so every `assumed: true` stays.
