# Settlement: South Carolina, tax year 2025 (round r3)

Settled 2026-11-07 from `work/extract/2025/SC.r3.A.json` and `SC.r3.B.json`.
Sources: `sources/archive/2025/SC/SC1040Instr_2025` (Instructions, cited "Instr") and `IITPacket_2025` (the full packet with the SC1040 form and the tax tables, cited "Packet"). Page numbers are PDF pages.

`uv run python -m tools.compare` reported **70 structured differences** (171 wording). All are in `reliefs`, and all come from the readers splitting or keying entries differently. 48 were decided by reading the booklet. 22 were one-sided B entries that the booklet does print, dropped because they fall outside the record's scope.

## Structured differences

| # | Entry (compare key) | Fields | A | B | Settled | Page |
|---|---|---|---|---|---|---|
| 1 | Retirement deduction, under 65 (p-1/p-2) | 13 (A 7, B 6: the entries didn't match because of `max_age`) | `max_age` 65 | no age, words only | `max_age` 64 ("under age 65" means the oldest age reached is 64), and the words kept in `other_conditions`. `covers` is the same as both readers had, plus `public_pension_other_state` (see 2). `roth_conversion` stays in `covers_unclear`. | Instr p.10 "An individual who is under age 65 may claim a retirement deduction up to $3,000" |
| 2 | Retirement deduction, 65 or older | 1 (`covers_unclear`) | `[roth_conversion]` | `[public_pension_other_state, roth_conversion]` | `public_pension_other_state` moved into `covers` (and the same for the under-65 and surviving spouse entries). `roth_conversion` stays unclear. | Instr p.11: "all public employee retirement plans of the federal, state, and local governments". "All" state plans are named, with no limit to South Carolina. Conversions are not mentioned. |
| 3 | Surviving spouse retirement deduction, p-3 (two entries) | 26 (A 14, B 12) | `min_age`/`max_age` 65 set on the deceased spouse's age; `covers` includes `military_pension` | no ages; no `military_pension` | No `min_age`/`max_age`, because the age tested is the deceased spouse's would-be age, not the filer's; the test is in `other_conditions` (B). `military_pension` kept in `covers` (A). Caps 3,000 / 10,000 per deceased spouse. | Instr p.10 "based on the age of the deceased spouse if they were alive"; p.11: the definition includes "military retirement", and the p-3 deduction is not reduced by the p-6 military deduction |
| 4 | Surviving spouse military retirement deduction, p-6 (A only) | 3 | own entry (return) | folded into one p-4 to p-6 entry | A's separate entry kept: it is a different branch with its own rules (it is added on top of the survivor's own deductions and does not reduce line q) | Instr p.12 Line p-6 |
| 5 | Two Wage Earner Credit (B only) | 5 | — | credit, cap 350, no rate | Kept. Added `credit_rate` 0.007 and `credit_basis` covered_income. The cap 350 is under `married_joint` (only joint filers may claim it). The lower-earner rule and the 50,000 limit are in `cap_rule`. | Instr p.17 ".007 of the lesser of $50,000 or the ... qualified earned income of the spouse with the lower ..."; p.18 worksheet lines 6-7 "Cannot be greater than $350" |
| 6 | Child and Dependent Care Credit (B only) | 6 | — | credit 7%, cap 210 | Dropped: it is a credit other than retirement or Social Security relief (a design.md non-goal) and turns on dependents. B's single cap of 210 also misses the 420 for two or more children. Listed in notes. | Instr p.17 Line 11 |
| 7 | Volunteer deduction (B only) | 5 | — | 6,000 per person | Dropped, out of scope (not retirement relief). In notes. | Instr p.9 Line j |
| 8 | College savings, line k (B only) | 3 | — | all_income | Dropped, out of scope. In notes. | Instr p.9 Line k |
| 9 | Subsistence allowance, line s (B only) | 3 | — | wages | Dropped, out of scope. In notes. | Instr p.13 Line s |
| 10 | Special needs adoption, line v (B only) | 5 | — | 2,000 | Dropped, out of scope and per child. In notes. | Instr p.15 Line v |

Total: 13 + 1 + 26 + 3 + 5 = 48 decided from the booklet; 6 + 5 + 3 + 3 + 5 = 22 dropped on scope.

### Not flagged by the compare, but settled

- **Brackets.** Both readers recorded only "6% from 100,000" and described the table in notes. The full schedule is now derived and recorded with `brackets.derivation`: 0% from 0, 3% from 3,560 and 6% from 17,840, the same for every filing status.
  - **How.** I parsed all 1,069 printed table rows (Packet pp.48-51, from 50 to 99,900). Each row's tax at its midpoint, rounded to the dollar, matches the printed tax exactly. The Packet p.51 formula is 6% of income minus 642, and 0.03 x (3,560 + 17,840) = 642, so the derived schedule also matches the formula exactly at 100,000 and above.
  - **What the table leaves open.** On its own, the table fixes the lower threshold only to somewhere in 3,559-3,566 and the upper to somewhere in 17,818-17,857. Taking the printed 642 as exact fixes their sum at 21,400. From the pairs that fit, I chose the one on round tens.
  - **Evidence recorded.** Six rows with status `all` (one table is printed for every status): 3,525→0, 3,625→2, 10,050→195, 17,850→429, 50,050→2,361 and 99,950→5,355, plus the formula. The validator re-computes all of them without a derivation problem.
- **`cannot_combine_with`** between the under-65 and 65-or-older branches: B listed it, A did not. Left out. The age tests already separate the branches for each person, and the list could be read as one spouse's deduction blocking the other's.
- **Cite pages corrected.** A cited the retirement deduction introduction as p.8 (that is the printed page; the PDF page is p.10) and line d as p.4 (it is PDF p.6).

## One-sided entries

- Kept (A only): the p-6 surviving spouse military entry (row 4).
- Kept (B only): the Two Wage Earner Credit (row 5).
- Dropped (B only): rows 6 to 10. The booklet prints each of them, but they are outside the record's scope.
- Both readers had the same set of other reliefs, and all are kept: line g disability, line n Guard and Reserve pay, line v Guard and Reserve retirement, line m US obligations, and line o Social Security and railroad retirement.

## Facts most often missed: second-document checks

- **Social Security: exempt.** Instr p.10 line o subtracts Social Security and railroad retirement taxed on the federal return. Instr p.11 says they "are not taxed by South Carolina". The SC1040 form's line o (Packet p.46) confirms it.
- **Retirement relief.**
  - Caps: 3,000 under 65 and 10,000 at 65 or older (Instr p.10 and the p.11 worksheets line 1).
  - Age 65 deduction: 15,000 against any income (Instr p.12; worksheets for q-1 and q-2 on pp.12-13).
  - How they combine: the age 65 deduction is 15,000 less the person's own p-1/p-2 and p-4/p-5 deductions, so the retirement and age 65 deductions together cannot exceed 15,000 a person. Example 2 (10,000 + 5,000) and Example 3 ("The maximum allowed deduction for 2025 is $15,000") show this.
  - Military retirement is uncapped and can exceed 15,000 (Example 4: 36,000). It reduces both the retirement and the age 65 deductions (Instr p.12).
  - Surviving spouse deductions do not reduce line q.
- **Capital gains.** 44% of net capital gain is deducted. Checked in Instr p.8 line i and on the form line i (Packet p.46).
- **Deductions.** The return starts from federal taxable income (Instr p.5 and form line 1). South Carolina has no standard deduction and no personal exemption of its own. The dependent exemption is 4,930 (Instr p.16 worksheet and Packet p.5), and the under-6 deduction is another 4,930 (Instr p.14 worksheet).
- **Brackets.** All filing statuses use the one table and formula (Packet p.51 "Use this Tax Rate Schedule for any filing status").

## Projection choices (`SC.projection.json`)

- **Base.** `starts_from` federal_taxable_income with no state deductions. The dependent amounts are in `not_modelled` (warn `has_dependents`).
- **Retirement and age 65 deductions.** Modelled in four parts:
  - Under 65: 3,000, cap reduced by military retirement.
  - 65 or older: 10,000, cap reduced by military retirement.
  - Age 65: 15,000 against all income, cap reduced by military retirement.
  - Military retirement: uncapped.
  - The 65-or-older retirement entry and the age 65 entry share one `best_of_group`. For a person 65 or older this gives the worksheet result, the larger of 15,000 and the person's military retirement. Using the cap reduction on the age 65 entry instead would lower its cap by retirement *income* rather than by the deduction, which is wrong: a 14,000 IRA would give 11,000 instead of 15,000. This is logged as an approximation (direction either, none in practice).
  - `needs_input: pension_source` is set on these entries because the military/non-military split drives the caps.
- **Not modelled:** the surviving spouse branches (deceased spouse's would-be age), line v Guard and Reserve retirement, line g disability, the Two Wage Earner Credit (it needs the lower earner's income; warn `always`), US obligation interest, and Guard and Reserve pay.
- **Approximations.**
  - Rounding in the derived brackets.
  - The best_of_group equivalence above.
  - Roth conversions left out of the retirement deduction.
  - Penalised early withdrawals and inherited plans, which the projection can't tell apart.
  - Capital-loss netting.
  - Own-state municipal bonds.
  - Treasury interest.
  - The itemizer's state tax addback (line a).

## Validator

`data/states/2025/SC.projection.json: ok`.

`data/states/2025/SC.record.json` has 5 problems, all of the form "provenance: brackets.derivation.table_rows[n].income=… is not printed in the sources" (3,625, 10,050, 17,850, 50,050, 99,950).
- **Why it fails.** The schema defines a row's income as the row midpoint, and the booklet never prints midpoints (only "At least" and "But less than"). A lower or upper bound would not reproduce the tax: the error is 1.50 dollars in the 3% band and 3 dollars in the 6% band, against a 1-dollar tolerance.
- **Not a reading error.** The derivation check itself passes for every row and for the formula. The first row's midpoint (3,525) passes only because 3,525 happens to be printed as a tax amount on another row.
- **Fix needed in `tools/validate.py`.** It should skip `brackets.derivation.table_rows[*].income` from the provenance check, the way it already skips the derived bracket figures. That is outside the files this settlement may change.

## Unsure

- **`max_age` 64 for "under age 65".** The schema doesn't say whether `max_age` is inclusive. I read "age reached" as inclusive, so 64. If consumers treat it as an exclusive limit, it should be 65.
- **`public_pension_other_state` in covers.** This rests on "all public employee retirement plans of the federal, state, and local governments". Neither reader put it in `covers`.
- **Military retirement in the own-plan and p-3 worksheets.** Read literally, the definition counts military retirement as qualified retirement income, and the worksheets' line 4 takes "pensions". A person under 65 with less than 3,000 of military retirement could then deduct some military income twice (on p-4 and on p-1). I kept the literal reading (both readers did).
- **Bracket thresholds.** 3,560 / 17,840 is one choice from a feasible set. Every pair in that set gives the same table to the dollar.

## 2026-11-08: marker ids and indexing covers

- Marker ids: all 8 markers have an `id`. Each takes its first from_record id, so warning codes are unchanged.
- Indexing covers: `brackets`, `relief_caps` (reliefs.cap: both retirement deductions and the age 65 deduction). No split needed.
- Assumed entries: searched the archived sources (docling, pypdf and page text) for indexed, inflation, cost of living, adjusted annually and consumer price index, and for statements that figures are fixed; nothing says, so every `assumed: true` stays.
