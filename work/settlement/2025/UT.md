# Utah 2025 settlement (round r6, 2026-11-07)

Readings: `work/extract/2025/UT.r6.A.json`, `UT.r6.B.json`. Sources: TC-40 Instructions, TC-40, TC-40A, the TC-40A web page and the credits page.
Comparison: 68 structured differences, 141 wording differences. No dollar figure or rate differs. Every field comes from nine questions: one rule written two ways, or one reader leaving an entry out.

## Structured differences (68 fields, 9 questions)

| Fields | Question | A | B | Settlement | Page |
|---|---|---|---|---|---|
| 28 | Social Security credit `who.basis` and measure (the tool shows two entries because the key differs) | return, base `other` | each_person, base `state_taxable_income` | Return, base `other` | PDF p23 |
| 11 | Qualified Exempt Taxpayer | relief | note only: "cannot express" | Relief kept | PDF p10-11 |
| 6 | Railroad (78) `who.basis` | return | each_person | Return | PDF p20 |
| 6 | Previously-taxed retirement (90) `who.basis` | return | each_person | Return | PDF p20 |
| 6 | Nonresident military pay (82) and spouse income (88) | reliefs | note only | Dropped | PDF p20 |
| 5 | Military Survivor Benefits Credit (AA) | relief | note only | Kept | PDF p28 |
| 3 | US obligations (71) | separate entry, interest and dividends | merged with Utah bonds, interest | A | PDF p19 |
| 2 | `all_income_scope` on the taxpayer credit and 18 | return | absent | Return, the default | schema |
| 1 | Taxpayer credit measure | `other` | `state_taxable_income` | B | PDF p10 |

**Social Security credit basis.** PDF p23 worksheet line 1: "For yourself (and/or your spouse), enter the amount from federal form 1040 or 1040-SR, line 6b". One amount, one threshold on line 10, one credit on line 13. No age test. So `return`. AJ differs: "Complete one worksheet for each person taking this credit" (PDF p24), so `each_person`.

**Its measure.** Lines 5 to 9: line 9, minus code 57, plus 1040 line 2a. Line 9 already holds code 57, so `state_taxable_income` with `plus_tax_exempt_interest` would count that interest twice. No schema base can say "minus code 57". `other`, with the definition in `as_printed`. The retirement credit is the same shape from line 6; both readers had `other`.

**Qualified Exempt Taxpayer.** PDF p10: "If your federal adjusted gross income is less than or equal to your federal standard deduction, you are exempt from Utah income tax." B's note says no income test can hold this. `effect: removes` with the default `over` does: at the threshold the relief stays, above it the relief goes. PDF p4 says "less than"; Line 21 and the worksheet say at or below, and those govern. Both readers cited the worksheet on PDF p10; the pypdf marker puts it on p11, corrected.

**82 and 88.** "Nonresident service members do not pay Utah income tax on active duty military pay" (PDF p20). Neither applies to a resident or to retirement income. A's own note says so.

**AA.** PDF p28: "you may claim a credit for 4.5 percent of the survivor benefits you received during the year." It sits beside AJ for a survivor, so it is in scope. `not_modelled`.

**Taxpayer credit measure.** PDF p10 Line 18: "Subtract line 17 from line 9." Second document, TC-40 page 1 line 18: "subtract line 17 from line 9". `state_taxable_income`.

## One-sided and wording items

- `best_of_group` (a free-text field, not counted): B grouped 18, AH and AJ. Removed; see the next section.
- B's `credit_basis` silence on the taxpayer credit: both left it out, and rightly. 6% is a share of line 15, neither income nor tax.
- B's notes on nonrefundability and on indexing: kept as notes.
- Not recorded, by both readers: code 77, 69, 79, 85, 89, trust items, MSA and my529 addbacks, code 51, credit 17, and credits unrelated to retirement income. All in one note. `docs/design.md` scope.
- Added by the settler: quotes in the notes for every fact below; the phase-out wording in `as_printed` for the taxpayer, AH and 18 tests.

## Points flagged by the readers

**No deduction from income.** Lines 5 to 9 reach Utah taxable income with no deduction, and line 10 taxes it. Line 11: "The Utah personal exemption is $2,111 per dependent." The filer and spouse get none: "You may not claim yourself or your spouse as other dependents" (PDF p9). The record's `base.deductions` hold the printed amounts, each with a condition saying they only feed the credit. The projection's `base.deductions` is empty, on purpose.

**Taxpayer tax credit: how it is represented.** Lines 13 to 20: 6% of (2,111 per dependent + federal deduction - state income tax itemized), less 1.3% of line 9 over 18,213 / 27,320 / 36,426. The `credit_basis` values cannot reach it: `covered_income` alone means 6% of income, and `tax` means a share of tax.

- The format does reach it another way. `covers: ["all_income"]`, `credit_rate` 0.06, `credit_basis: covered_income`, and `cap` set to the federal standard deduction, per return. That gives 6% of the deduction once income passes the cap. Below the cap the credit is smaller than the form's, but tax is 0 either way, because 6% of income exceeds 4.5% of it. Oregon's retirement credit is the precedent for `cap` limiting income before `credit_rate`.
- `income_test` is `phase_out_rate` 0.013 on `state_taxable_income`, so the projection adds no figure. The cap figures come from the record's `utah_federal_standard_deduction`, which is in `from_record`. The record itself carries no cap, because the booklet prints none.
- Rejected: a bracket schedule (0, 5.8%, 4.5%), which is exact but needs band starts that are products, not record figures, and would hide the credit. Rejected: the deduction in `base.deductions`, which gets the rate wrong (4.5% against 6%) and loses the phase-out.
- Tested: `arith.py` in the private folder compared the projection's arithmetic with lines 10 to 22 at 8 incomes for each of single, head of household and joint. Same tax in every case, for a filer under 65 on the standard deduction with no dependents.

**The gap, with direction and size** (`approximations` and `not_modelled`):

| Gap | Direction | Size |
|---|---|---|
| Age 65 and blindness extras: line 12 takes federal 12e, the cap can't hold them, and the sources print no amount | overstates tax | 6% of the extras: 120 single, 96 a person married, 192 a couple. Hits nearly every retired household until the credit runs out (Utah taxable income about 90,905 / 136,358 / 181,811) |
| Itemizers | either | 6% of the difference: 450 for the example in the file |
| Dependents | overstates tax | 126.66 each (`not_modelled`, `has_dependents`) |
| Federal deduction held flat | overstates tax | 9.45 single, 18.90 joint for each 1% it rises |

The 120 and 96 use the 2025 federal extras in `docs/checks-brief.md`, not Utah's sources. They appear only in the prose size, not in a data field.

**Retirement Credit 18, AH, AJ.** Birth test confirmed in two documents: "born on or before Dec. 31, 1952" (PDF p21; TC-40A web page). 18 cannot go with AH or AJ, and the bar crosses spouses: "You may not claim this credit if you (or your spouse, if filing jointly) claim either the Social Security Benefits Credit (code AH) or the Military Retirement Credit (code AJ)." AH and AJ each repeat it for 18 only (PDF p23).

**AH and AJ can combine.** Each names only code 18 as its bar, and nothing printed bars one with the other. This is a reading from the absence of a bar on two adjacent, otherwise parallel rules, not a printed sentence. No `best_of_group`: it would make AH and AJ alternatives, and a `best_of_group` is chosen per person (the schema says so), while this bar is on the return. `cannot_combine_with` holds the bars; an approximation covers a consumer that compares 18 with each one alone.

**Qualified exempt taxpayer in the projection.** Mostly redundant with the credit, but it matters where line 9 runs above federal AGI: 15,000 of AGI and 50,000 of added-back municipal interest gives Utah tax, but the test is on federal AGI, so the tax is 0. Modelled. The senior add-on (Schedule 1-A line 37) has no printed amount, so it is an approximation.

**Other-state municipal interest.** PDF p18: "Do not enter interest earned on non-Utah municipal bonds if the issuer does not impose an income tax on bonds issued by Utah, or the issuing state does not impose an income tax." And only bonds "acquired after Jan. 1, 2003". Record `other`. Projection `other_states_taxed_own_exempt`, with an `overstates_tax` approximation at 4.5% of the interest.

## Facts always settled

1. **Another state's government pension, including New York State: not found in the booklet.** Not in any `covers` or `not_covered`; no reciprocity. Nearest text: "Utah residents who earn income in other states must pay Utah tax on that income" (PDF p7). Line 8's nine subtractions (PDF p10, p19; TC-40A web page) name no government pension. Result: stays in federal AGI on line 4, taxed at 4.5%. Only 18 by birth date can offset it, or code 90 in its rare case. This is a reading from a closed list, not a printed sentence.
2. **Utah and federal government pensions: not found as a separate rule.** PDF p23: military retirement pay "does not include Social Security income, 401(k) or IRA distributions, or other sources of income, such as non-military federal retirement". Same result as item 1. Military has AJ; railroad has 78.
3. **Private pensions, IRA and employer-plan distributions, Roth conversions.** No subtraction. Code 90: "This subtraction is for very rare cases where Utah taxes retirement income derived from contributions to a retirement plan that were previously taxed by another state" (PDF p20). Roth conversions are named nowhere in the sources; they are taxed through federal AGI, and no relief exists to cover them.
4. **Social Security: relief.** No subtraction code (PDF p19; TC-40A web page). AH, PDF p23: "You may only claim this credit for Social Security benefits included in adjusted gross income on this return." 4.5% of line 6b, less 2.5% of modified income over 54,000 / 90,000 / 45,000 / 90,000. Second document: TC-40A web page, same text and figures.
5. **Brackets and deductions.** One rate for all: "Multiply line 9 by 4.5 percent (.045)" (PDF p10); TC-40 line 10, "multiply line 9 by 4.5% (.045)". No other status has a schedule. No Utah standard deduction; exemption 2,111 per dependent; no age or blindness amount.

## Projection decisions

- Six reliefs: taxpayer credit, qualified exempt taxpayer, 18, AH, AJ (`needs_input: pension_source`), railroad (`exempt_in_full`, as in other states).
- **AH's measure is `federal_agi` with `plus_tax_exempt_interest`.** That equals the worksheet less lines 7 and 8. `state_taxable_income` with the flag double-counts added-back municipal interest; `state_taxable_income` alone misses Utah bond interest. The chosen one leaves Treasury and railroad subtractions in: `overstates_tax`, 2.5% of them, inside the phase-out only.
- **18's measure is `federal_agi` with `plus_tax_exempt_interest`.** Exact, apart from additions other than code 57.
- Treasury interest, Utah Build America interest, 04, 26: `not_modelled`, `never`, as in other projections. Code 90: `has_pension`, since a retiree who moved from a state that taxed contributions could qualify.
- Indexing `not_stated`: flat, assumed, with an approximation.
- `derived_figures` is empty: nothing is computed.

## Unsure

- **Phase-out order on a rate credit.** Utah's reductions come off the credit, after the rate (lines 16 to 20; AH lines 4, 12, 13). Oregon's projection takes its income test before the rate. Nothing in the format says which, so a consumer must apply Utah's after the rate or AH and the taxpayer credit come out far too large. Stated in the first approximation; a check should pin it.
- **`cap` on an `all_income` credit** is a new use: Oregon uses cap with a rate, but on named income. A consumer must read `all_income` with `cap` as min(income, cap) x rate.
- **18's single reduction.** `each_person` with a per-person cap could reduce each 450 by the whole reduction; the worksheet reduces the total once. A check on a couple both born by 1952 should pin it.
- **AH and AJ combining** is a reading from silence; the statute was not read.
- **`social_security` in AH's `covers`** means the taxable part (line 6b), not gross benefits.
- The size figures for the age extras and the senior deduction use amounts from outside Utah's sources, marked as such.

## 2026-11-08: marker ids and indexing covers

- Marker ids: all 9 markers have an `id`. Descriptive ids (no from_record id of their own): `ut_dependent_credits`, `ut_other_credits`, `ut_part_year_nonresident`; the rest take their first from_record id, so their warning codes are unchanged. `tools.checks --fix-warnings` rewrote the cases' accepted_warnings (the old shared code state_rule_not_modelled:unnamed becomes the new ids); nothing else in the cases changed.
- Indexing covers: `brackets`; `deductions` (Utah has no base deduction) now covers the two relief figures that are the federal standard deduction: reliefs:taxpayer_tax_credit.cap and reliefs:qualified_exempt_taxpayer.income_test; `relief_caps` covers reliefs.cap. Added `relief_income_tests` (reliefs.income_test) and `relief_credit_amounts` (reliefs.credit_amount), indexed false, assumed, which no entry covered.
- Assumed entries: searched the archived sources (docling, pypdf and page text) for indexed, inflation, cost of living, adjusted annually and consumer price index, and for statements that figures are fixed; nothing says, so every `assumed: true` stays.
