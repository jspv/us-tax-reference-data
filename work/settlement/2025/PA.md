# Settlement: Pennsylvania, tax year 2025

- Readings: `work/extract/2025/PA.r6.A.json`, `work/extract/2025/PA.r6.B.json` (round r6)
- Sources: `sources/archive/2025/PA/`: `2025_pa-40in` (booklet, cited "p."), `2025_pa-40` (the form), `gross-compensation.page.txt` (PA Personal Income Tax Guide, cited "Guide")
- Outputs: `data/states/2025/PA.record.json`, `data/states/2025/PA.projection.json`
- Settled: 2026-11-07

## Comparison

`uv run python -m tools.compare` reported **26 structured differences** (91 wording). All 26 were read against the booklet and settled from it. The readers agreed on the rate, the base, Social Security, the IRA age, the Roth entry, municipal interest and indexing. The 26 reduce to seven points. One of them (row 3) is a reading of general wording, not a sentence that names the case.

| # | Lines | Field | A | B | Settled | Source |
|---|---|---|---|---|---|---|
| 1 | 3 | `base.deductions` student loan interest | 2,500, per return | not recorded | **Kept.** `per` stays return, unsure (below) | p.20: "Student Loan Interest, up to $2,500, may be claimed as a deduction"; p.1 repeats it |
| 2 | 3 | `base.deductions` Section 529 | 19,000, per person | not recorded | **Kept** | p.20: "a maximum deduction of $19,000 per beneficiary, per taxpayer" |
| 3 | 1 | Employer-plan entry, `public_pension_other_state` | left out, "not found" | `covers_unclear` | **`covers`, as a reading**, with the same plan and retirement conditions as a private plan | p.11, p.8, p.13 Tip 2 and the Guide; quotes below |
| 4 | 1 | Named-systems entry, `public_pension_other_state` | left out | `covers_unclear` | **Dropped.** The entry is a closed list | p.12 item 5 names four systems |
| 5 | 9 | Social Security and Railroad Retirement entries | two entries, basis return | one entry, basis each_person | **Railroad only**, `each_person`. Social Security stays in `social_security.treatment` | p.8 bullet "Social Security benefits and/or Railroad Retirement benefits" |
| 6 | 3 | IRA paid on death | own entry | inside the 59½ entry's conditions | **Own entry** (no age test) | p.12 Withdrawals item 2 |
| 7 | 6 | Interest on U.S. and Pennsylvania obligations | two entries | none | **U.S. kept; Pennsylvania dropped**, as `muni_interest` already holds it | p.31 list; p.32 Schedule A Line 7 |

## The pension rules for a Pennsylvania resident

- **Pennsylvania state, school and municipal systems, U.S. Civil Service plan, Civil Service Annuity:** exempt at any age. p.12 item 5: "All distributions (regardless of the distribution code reported in Box 7 of the 1099-R)". p.13 Tip 3 and the Guide repeat it; p.8 lists "Civil Service Annuity".
- **Military:** exempt. p.12 item 6, p.8 "Military pension benefits".
- **Other Pennsylvania local plans:** not named, so the plan test applies; `public_pension` is therefore in the employer-plan entry too.
- **Private pensions and employer plans (401(k), thrift, deferred compensation, profit sharing):** exempt only from an eligible plan, and only after retiring having met the plan's age or service conditions. p.12 item 1: "Payments you receive after you qualify for retirement and retire." p.12-13 Code 1 & 2: "you retired after meeting the age conditions of the plan or years of service conditions of the plan". The booklet prints no age of its own. Otherwise the distribution is taxable above contributions by cost recovery (p.9, p.13).
- **IRA, RMDs included:** exempt "on or after reaching the age of 59 1/2" (p.12), or on death. Before 59½, cost recovery, even after retiring: p.14 "If you retired, but did not reach age 59 1/2, you must report your distributions on a cost recovery basis until you reach age 59 1/2."
- **Roth conversion:** exempt only if the entire withdrawal is rolled over: trustee to trustee, or "within 60 days invested the entire (100 percent) amount you received into a Roth IRA" (p.12), with federal tax withheld put back (p.12 CAUTION, p.13 Tip 4).
  - "Entire" is the whole withdrawal, not the whole IRA.
  - The test only bites before 59½. From then on the part kept is an exempt IRA distribution.
  - The rollover text covers traditional IRA to Roth only. From an employer plan, p.12 item 2 exempts a rollover "only when the transferred amounts are not taxable income for federal purposes", so a Roth rollover rests on item 1 (qualified and retired). In `not_covered`.
- **Social Security:** exempt. p.8 "INCOME NOT TAXABLE FOR PA PIT PURPOSES"; second source, the Guide's never-taxable list: "Social Security payments; railroad retirement benefits". The form has no Social Security line.
- **Commercial annuity:** interest income to the extent federally taxable (p.13, p.15). An annuity from an eligible employer plan after retirement is exempt (p.13 Box 8).

## Another state's government pension, New York State's in particular

**No source names one. "New York" is printed in none of the three documents.** Settled in `covers` of `employer_plan_after_retirement`, not in `covers_unclear`, with no `paying_states`.

The wording that decides it:

- p.11: "Pennsylvania does not impose income tax on payments you receive that are commonly recognized retirement benefits distributed from eligible employer-sponsored retirement plans."
- p.8, not taxable: "Commonly recognized pension, old age, or retirement benefits paid after becoming eligible to retire, and retiring".
- p.13 Tip 2: "Eligible plans must: be in writing; include provisions for separation of service, old age or infirmity, and long-continued service; provide for payments at regularly recurring intervals after separation from service until death or an option for a lump sum payment; and does not permit the distribution of program benefits to any employee until termination of employment except for incidental disability benefits or the return of the employee's previously taxed contributions ... If these conditions are met, the distribution is not taxable".
- Guide: "A plan is considered an eligible Pennsylvania retirement plan if, at a minimum, the plan has the following four characteristics". None of the four concerns the employer or the place.
- Guide, on taxable distributions: "Residents who contributed to a retirement plan while a nonresident are subject to tax only on the amount received over and above their contributions, regardless of whether tax was paid to another state on the retirement income."

Why `covers`, against B's `covers_unclear`: `covers_unclear` is for a kind the booklet doesn't settle. Here the rule is written by plan, not by payer, so what is open is a fact about the plan, the same fact every private pension must pass, and `private_pension` is in `covers` on that condition. B's own note says the exemption "turns on whether the plan is an eligible employer-sponsored retirement plan, not on which government pays". Maine, Missouri and Mississippi were settled this way from general wording. Oklahoma went the other way because its line is a list of plan types.

"Eligible Pennsylvania retirement plan" in the Guide means eligible for PA tax, not run by Pennsylvania. The same Guide uses "eligible plan for PA PIT purposes", and the booklet says "eligible plan for PA income tax purposes" (p.11).

Reciprocity does not reach it. The six agreements cover compensation (p.11), and "These agreements apply to employee compensation only" (Guide). New York is not one of the six.

The named list on p.12 item 5 does not include it, so it needs the retirement test: exempt only after retiring having met the plan's age or service conditions. The projection marks the reading as `understates_tax`: 1,842 a year on 60,000 if it fails.

## Rate, deductions (point 5)

- **Rate:** flat 3.07% on every status. p.1 and form line 12 agree. Both readers agreed. `brackets.derivation` is not used: a rate is printed, no table.
- **Statuses:** the form prints Single, Joint and Separate. No head of household anywhere. No separate schedule, so `single` and `married_joint` only, as the schema asks.
- **Standard deduction and exemptions:** none, and the booklet says so: "PA law does not allow standard deductions, deductions for personal exemptions, itemized deductions, or deductions for personal expenses" (p.9). No age-65 or blind amount. Only Line 10 deductions exist.
- **Surtax, recapture:** none printed. **Indexing:** nothing said; `not_stated`.

## One-sided entries

Kept: A's student loan, 529, U.S. obligation and IRA death entries; B's Railroad `each_person` basis. Dropped: A's Social Security relief and Pennsylvania obligation relief (each held in its own field); A's `basis: return` on Railroad; B's `covers_unclear` on the named-systems entry; B's "Guide" events inside the 59½ conditions (see unsure, 2).

## Added, neither reader had them

The booklet prints each and the brief puts them in scope:

- `united_mine_workers_pension` (p.8, p.38).
- `employer_plan_death` (p.12 item 4).
- `disability_distribution` (p.13 Code 3 or 4; p.14 Tip 11; the Guide: "3 – Under PA PIT law, a distribution due to disability generally is not taxable").
- `employer_plan_annuity` (p.13 Box 8).
- `capital_gains`: `pre_1994_exempt_obligation_gains` and `principal_residence_gain` (p.18).
- `tax_forgiveness` (p.36-39), below.

## Tax Forgiveness (Schedule SP)

A noted it and left it out; B did not mention it. Recorded as a relief: `form: credit`, `credit_basis: tax`, `credit_rate: 1`, `income_test.effect: stepped`, with one band per column of Tables 1 and 2 (`measure.base: other`, Eligibility Income in `as_printed`). The schema has no field for the dependent columns: each child adds 9,500 to every column, which is in `other_conditions`. Status `single` is Table 1; `married_joint` and `married_separate` are Table 2, because "Married Claimants, even if filing separately".

The projection follows the guide (low-income credits are `not_modelled`), with an `approximations` entry. What it means for low-income retirees:

- **Direction:** `overstates_tax`. The run shows PA tax the household doesn't owe.
- **Size:** at most 199.55 single and 399.10 married a year (3.07% of 6,500 and 13,000). Then 90% down to 10% in 250 steps, to 8,750 or 15,250. None above.
- **Who:** Eligibility Income leaves out "Social Security and Railroad Retirement Benefits", "Retirement benefits from Pennsylvania eligible retirement plans after becoming eligible to retire and retiring", military pensions and Civil Service annuities (p.38-39). So the test falls on taxable income, not cash income: a couple with 90,000 of those and 12,000 of interest and dividends is shown 368.40 and owes 0. It reaches more than the low-income, and it can apply every year.
- **What can remove it:** Eligibility Income also counts things a projection doesn't see: Treasury and Pennsylvania bond interest (p.31), gifts, inheritances, insurance proceeds, survivor annuities (p.38), an excluded home-sale gain.
- **Warning:** `person_in_age_range` 60 to 120, not `never` as other states' low-income credits have, because a Pennsylvania retiree is the normal case here. The rule itself has no age test.

## Projection: mapping and direction

`state_own` maps to `federal_agi`. The mapping runs from federal AGI to Pennsylvania's eight classes: start from AGI, take out what the reliefs exempt. Differences that remain, each an `approximations` entry:

| Difference | Direction | Size |
|---|---|---|
| Employee plan contributions are PA compensation (p.12) | understates | 614 on 20,000 |
| Federal adjustments PA refuses (IRA, half of SE tax) | understates | 214.90 on 7,000 |
| Losses: no offset between classes or spouses, no carryover (p.15, p.20) | understates | 92.10 on 3,000 |
| Unemployment compensation and similar in AGI but not PA (p.8) | overstates | 3.07% of it |
| Treasury interest (p.31) | overstates | 614 on 20,000 |
| Pennsylvania bond interest, treated as other-state | overstates | 3.07% of it |
| Another state's pension exempted (reading) | understates | 1,842 on 60,000, only if the reading fails |
| Plan and retirement test not computable; employer plans exempt at any age | understates | 614 on a 30,000 in-service withdrawal with 10,000 of contributions |
| IRA before 59½ at the federal amount; PA uses cost recovery | overstates | 921 on 30,000 |
| Roth conversion not fully rolled over, before 59½ | understates | 307 on 10,000 kept |
| Employer annuity taxed | overstates | 3.07% of it |
| Tax Forgiveness | overstates | at most 199.55 or 399.10 |
| 529 contributions | overstates | at most 583.30 per taxpayer per beneficiary |

For a working saver the net is too low. For a retiree it is too high.

`needs_input: ["pension_source"]` is on the public, military and employer reliefs. The guide asks for it where kinds are treated differently, and they are in the record (the named systems have no retirement test). In the projection every kind ends up exempt, so today's answer changes no tax.

## Unsure

1. **Another state's pension in `covers`.** A reading, and the one figure here worth more than a few hundred dollars a year. The statute or a department bulletin would settle it. Bulletin 2008-01 (named on p.12) is about IRAs and is not in the sources.
2. **IRA before 59½: booklet against Guide.** The booklet: "PA law does not have any exceptions similar to the federal exceptions for withdrawal before age 59 1/2" (p.12). The Guide: exempt "so long as the taxpayer is not required to pay a penalty for early withdrawal". They conflict for a penalty-free withdrawal before 59½ by someone neither dead nor disabled. I followed the booklet as the year's own, more specific document; B recorded both. Tax Bulletin 2008-01 is the likely tiebreak.
3. **Student loan `per`.** p.20 doesn't say per return or per person; Schedule O is not in the sources. Not modelled, so no effect.
4. **Disability entry.** "Generally not taxable" (p.13) is not an unconditional rule; `covers` names private pensions, employer plans and IRAs because the 1099-R codes apply to all three. It sits oddly beside p.12's "no exceptions" for an IRA, though that sentence's own list has only age and death.
5. **Label on the named-systems entry.** Shortened from the booklet's "Retirement Disability Plan", with the exact wording in `notes`: `tools.report_pensions` treats "disab" in a label as a narrow case and reported PA and federal pensions as taxed. The same word was reworded out of the plan test. A checker on the report should look at this, as the word test may misfile other states.
6. **"Five deductions."** p.20 says five, names four in the sentence and lists six codes. Reported as printed; no figure depends on it.

## 2026-11-08: marker ids and indexing covers

- Marker ids: all 9 markers have an `id`. Descriptive ids (no from_record id of their own): `pa_other_credits`; the rest take their first from_record id, so their warning codes are unchanged. `tools.checks --fix-warnings` rewrote the cases' accepted_warnings (the old shared code state_rule_not_modelled:unnamed becomes the new ids); nothing else in the cases changed.
- Indexing covers: `brackets` covers brackets. No split needed.
- Assumed entries: searched the archived sources (docling, pypdf and page text) for indexed, inflation, cost of living, adjusted annually and consumer price index, and for statements that figures are fixed; nothing says, so every `assumed: true` stays.

## 2026-11-08: indexing settled from statutes

Statute research (work/indexing/findings*.json) settled every projection indexing entry that was `assumed: true`:

- `brackets` (brackets): not indexed, Tax Reform Code of 1971, Art. III, Section 302(a) (72 P.S. 7302)
- Record `indexing`: updated brackets -> no.
