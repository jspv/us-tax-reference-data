# WA 2025 settlement

Readings: `work/extract/2025/WA.r6.A.json`, `WA.r6.B.json`. Comparison: 5 structured differences, 49 wording differences. Washington has no booklet; the sources are four Department of Revenue web pages in `sources/archive/2025/WA/`: Income tax, Capital gains tax, Do you owe capital gains tax?, and the special notice New tiered rates (June 30, 2025). All 5 structured differences were settled from those pages.

Shape: as AK, NV, TX and WY. `has_income_tax` false, empty brackets, `starts_from` none, no reliefs. Unlike them, Washington's capital gains tax stays in the record with its cites.

## Structured differences

| # | Field | A | B | Settled | Source |
|---|---|---|---|---|---|
| 1 | `base.deductions[other/return].amount.all` | 111000 | 278000 | Both kept, as separate entries. The comparison paired two different deductions: A's `other` is the charitable deduction, B's `other` is the standard deduction. | Capital gains tax page, Deductions, items 1 and 3 |
| 2 | `base.deductions[standard_deduction].what` | standard_deduction | (B has it as `other`) | `standard_deduction`. The page calls it that; the condition says capital gains tax only. | "The standard deduction for 2025 is $278,000."; Do you owe page table heading "Standard Deduction" |
| 3 | `base.deductions[standard_deduction].amount.all` | 278000 | (same figure under `other`) | 278000 | Same; the Do you owe table prints 2025 278,000 |
| 4 | `base.deductions[standard_deduction].per` | return | (return under `other`) | `return`. One amount for an "individual, married couple, or domestic partnership". | Capital gains tax page, Deductions, item 1 |
| 5 | `indexing` second yes entry (charitable deduction) | yes | missing | Kept, yes | "These amounts are adjusted for inflation annually." (Deductions, item 3) |

## Decisions outside the structured count

- **Real estate (wording difference, as dispatched).** A recorded real estate generally with entity interests in one entry. B recorded entity interests only and wrote that direct real estate is not listed by name. B is wrong: the Exemptions list prints "Real estate." as its own first item, and the entity item second: "Interests in a privately-held entity to the extent that the capital gain or loss from such sale or exchange is directly attributable to the real estate owned directly by such entity." Written as two entries in those words: `wa_cg_real_estate_exempt`, `wa_cg_real_estate_entity_exempt`.
- **The rate over $1 million.** A and B both recorded `own_rate` 0.099. The notice prints "Any amount of Washington capital gains exceeding $1 million is subject to a 7% tax, plus an additional 2.9% tax." Per the dispatch the 9.9% is derived: the record holds 0.07 and 0.029 (`treatment: other`, as Maryland's additional capital gains tax), and the projection's `derived_figures` has 0.099 as their sum, re-done by the validator. `surtaxes` with measure `other` was possible; I used `capital_gains` to follow the Maryland precedent and keep the tax's rates in one block.
- **9.9% is also printed.** B's note says the rate table cells are blank in the saved text. They are not: the notice's table reads "Tax rate 9.9%", "On taxable income from... $1,000,001". The derivation and the printed row agree, so nothing changes; the condition and the notes mention the table row.
- **QFOSB.** B's note says the "QFOSB Max Income" values are not in the saved text. They are: 11,095,000 for 2025, Do you owe page, Updated Amounts. Recorded in `notes` only: the deduction has no fixed amount and the sources do not say how the limit is tested.

## One-sided entries

- **Charitable deduction entry (A only): kept**, with a change. A had `per: return`; the page prints it twice as "per year per individual", so `per: person`. Amount 111000 is the maximum; the 278000 threshold is in the condition. Id renamed `wa_cg_charitable_deduction`.
- **Charitable indexing (A only): kept**, see row 5.
- **B's return due date and underpayment note: dropped.** Filing mechanics, not in scope for a record.
- **B's Do you owe test (Schedule D, domicile, 183 days): kept as a note**, which A's nexus note also covers. The page says it is "for informational purposes only and is not binding upon the department".
- **Other exempt assets, credits: kept in notes in the page's words**, as both readers did; the schema has no field. Real estate and retirement accounts are entries because both readers made them entries.
- **Both readers' 2028 tax note: kept as a note only.** The Income tax page says "Beginning Jan. 1, 2028, a new 9.9% income tax will apply to individuals and married couples filing jointly with annual adjusted gross income exceeding $1 million." It does not apply to 2025 and is in no field. Its 9.9% is unrelated to the capital gains 9.9%.

## Facts settled, with quotes

Quote for items 1 to 4, Income tax page: "Washington does not currently have an individual income tax."

1. **Another state's government pension; New York State pension.** Not found in the sources: no page names pensions. `public_pension_other_state` is in no `covers` or `not_covered`. With no individual income tax there is nothing for a rule to apply to, so no relief is written.
2. **Its own and federal government pensions.** Same: not found, no relief.
3. **Private pensions, IRA and employer-plan distributions, Roth conversions.** Same: not found, no relief. The nearest text is "Assets held in certain retirement accounts." That exempts assets from the capital gains tax; it says nothing about distributions.
4. **Social Security.** `not_stated` in the record. The pension items do not apply here, and nothing is inferred from them or from the absence of an income tax. The projection's enum has no `not_stated`, so it shows `exempt` with the same approximation line as AK, NV, TX and WY, which says the record holds `not_stated`.
5. **Schedule, deductions, exemptions.** No income tax brackets printed, for any status. No income-tax standard deduction or exemption printed. The only printed schedule is the capital gains one, with one column and no filing status. Deductions are the capital gains ones above.

Municipal interest: `not_stated`, not found.

## Projection

- **Capital gains tax: `not_modelled`, `warn_when: always`.** A projection could compute much of this tax, but the schema's `capital_gains` block only adds to bracket tax, and Washington has no brackets. The marker is `always` only because the schema had no gains-based trigger yet (later added: `has_long_term_gains`), so a household with no gains will see the warning too. It should move to the new trigger when that exists. The one marker names all seven capital gains ids.
- **`approximations`:** the AK-shaped line, plus one for the left-out tax (`understates_tax`) with a worked example: (500,000 - 278,000) x 7% = 15,540.
- **`capital_gains`, `base.deductions`, `indexing`: empty.** Nothing in them is computed. Indexing for the two deductions stays in the record.

## Unsure

- `what: standard_deduction` on a no-income-tax state's capital gains deduction follows the page's words, but a layer-1 reader taking `base.deductions` at face value could mistake it for an income-tax deduction. The condition says otherwise.
- The sentence giving "per year per individual, married couple, or domestic partnership" is attached in the page to the 2024 amount. I read it as applying to 2025 too; the sources do not say so outright.
- The notice prints one $1 million figure and is silent on married couples. The charitable deduction is "per individual" with no word on a couple's total.
- The Income tax page is undated ("currently") and was retrieved 2026-11-07; recorded as 2025 as dispatched, as for the other no-tax states.
- WA has no `checks/2025/WA` zero case yet; `tools/checks.py` requires one for a no-tax state, and it will need the warning `state_rule_not_modelled:wa_cg_first_million`.

- Main session, 2026-11-07 (format for the first frozen schema): the capital gains excise tax marker warns on has_long_term_gains instead of every run.

## 2026-11-08: marker ids and indexing covers

- Marker ids: the one marker has an `id`; it takes its first from_record id, so warning codes are unchanged.
- Indexing: no income tax and no grown figures, so `indexing` stays empty; the validator still reports 'no entry says which figures it covers', which an empty list cannot satisfy without inventing an entry. Left for the maintainer.
- Assumed entries: none (no indexing entries).
