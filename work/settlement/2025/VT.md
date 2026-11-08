# VT 2025 settlement log

Readings: `work/extract/2025/VT.r6.A.json`, `VT.r6.B.json`. Settled 2026-11-07. Page numbers are PDF pages.
"Booklet" is Income-Booklet-2025.pdf. "Worksheet" is the Retirement Income Exemption Worksheet, booklet p.16,
which matches IN-112-Instr-2025 p.2 word for word (checked by script).

`tools.compare` gave 85 structured differences and 97 wording differences. All 85 are settled, all from the
booklet. 20 of them are the same value filed under two keys, because the readers' `covers` lists differed.

Sources read: Income Booklet, Form IN-111, Schedule IN-112, IN-112 Instructions, Schedule IN-153, Schedule IN-119,
Seniors and Retirees web page. IN-153 and IN-119 were fetched after the readers finished; both are now used. The
separate IN-111 instructions page returned HTTP 403; the booklet's line instructions cover the same lines.

## Structured differences

| # | Field | A | B | Settled | Page and reason |
|---|---|---|---|---|---|
| 1-42 | `brackets.*` (rows 1 to 4, all four statuses: 10 lines each, 12 for joint) | rows at 75,000 merged, no base | printed rows with base | B | Booklet p.46 prints every row, and its example (85,000 joint: 2,764 + 165 = 2,929) uses the base. A gives 2,928.75. The projection merges them, see below. |
| 43-45 | `vt_dependent_exemption` (`amount.all`, `per`, `what`) | folded into the personal exemption | own entry, 5,300, per dependent | B | Booklet p.11 Line 5c counts dependents apart; the schema has the kind. |
| 46 | `recapture[0].full_rate` | 0.03 | missing | 0.03 | Booklet p.11 Line 8: "a minimum Vermont tax of 3% of federal AGI". |
| 47-49 | `vt_authority_bond_interest` (`covers`, `form`, `who.basis`) | present | notes only | kept | IN-112 Instr p.4 Line 15. See one-sided entries. |
| 50-76 | other-systems exemption, 27 lines under two keys | covers annuity, public_pension; public_pension_other_state unclear | covers public_pension, public_pension_other_state | B's covers | Worksheet question 1. Seven lines are real (`covers` twice, `covers_unclear`, `effect` twice, `rate`, `applies_when`). The other 20 (cap, cap_per, form, measure, the five thresholds, basis) have the same value on both sides. See "A state government" and "The phase-out". |
| 77-79 | military `income_test` (`applies_when`, `effect`, `rate`) | over, phase_out_rate, 0.00002 | missing, other, missing | over, other, no rate | Booklet p.17 and p.33. See "The phase-out". |
| 80-82 | CSRS `income_test` (same three) | over, phase_out_rate, 0.0001 | missing, other, missing | over, other, no rate | Worksheet Lines 4-12. |
| 83-85 | Social Security `income_test` (same three) | over, phase_out_rate, 0.0001 | missing, other, missing | over, other, no rate | Worksheet Lines 4-10. |

## The questions settled, with quotes

**1. Another state's government pension, New York State in particular.** `public_pension_other_state` is in `covers`
of `vt_other_retirement_exemption`. New York is named nowhere, and no reciprocity rule is printed, so no
`paying_states`. Worksheet question 1: "You can choose to exempt your taxable social security income OR the income you
received from a contributory annuity, pension, endowment, or retirement system of the U.S. government or a state
government, including the Civil Service Retirement System. Note that the second exemption only applies to benefits
that are based on earnings not covered by the Social Security Act (i.e., earnings that were not subject to the Social
Security tax withholding)."

**"A state government": covers, not covers_unclear.** The Seniors and Retirees page repeats the words. The phrase takes
an indefinite article and has no limit to Vermont, and these documents write Vermont when they mean it: IN-112 Instr
p.1, "Interest and dividend income from non-Vermont state and local obligations ... A Vermont obligation is one from
the state of Vermont or a Vermont municipality." A New York State
pension is a pension of a state government, so rule 15a puts it in `covers`. This is a reading of the words, not a line
that names other states: flagged below.

Rule for a resident with a New York State pension: it is in federal AGI and taxed, unless the plan is contributory and
the benefits rest on earnings not covered by Social Security; then up to 10,000 comes off, under the AGI limits, in
place of the Social Security exemption.

**2. Vermont's own and federal pensions.** No general relief. Vermont's is "a state government", federal "the U.S.
government", CSRS named. Same tests. Local government plans are not named: not found in the booklet.

**3. Private pensions, IRA and employer-plan distributions, Roth conversions.** No relief. Schedule IN-112 Lines 7-16
(booklet p.23) have no line for them, and they stay in Form IN-111 Line 1, "Federal Adjusted Gross Income". The word
Roth appears only at booklet p.43, in household income for the property tax credit: "Distributions from the
contributions to a ROTH IRA (distributions from the earnings of the ROTH IRA are to be reported in household income)".
Conversions: not found. No sentence says these are taxed; the record says so in a note and lists them in no `covers`.
One thing does touch them: IN-119 Line 1, 4 and 5 add 24% of federal tax on "Qualified Plans including IRA, HSA, and
MSA", which is in the record notes and `not_modelled` for ages under 60.

**4. Social Security.** `relief`. Worksheet question 1, as quoted, and question 3: "If you elected the exemption for
social security, please enter the full amount from federal Form 1040, Line 6b, on Schedule IN-112, Part I, Line 12."
Second check: Schedule IN-112 Line 12, and the page, "Recipients of Social Security benefits may be exempt from Vermont
tax on part or all of their benefits", and "if part or all of your benefits are taxable in Vermont". The structure on
the page agrees; only its limits differ (below).

**5. Brackets, standard deduction, exemptions.** Booklet p.46 schedules X, Y-1 (joint, Qualifying Widow(er), civil union
joint), Y-2, Z. Second check: all 750 rows of the tax tables, pp.47-51, four columns, computed at their midpoint from
the schedule rates. The largest error is 0.80, except the first row (0 to 100, printed 0). Every printed base agrees
with the merged schedule within a dollar. Standard deduction 7,650 / 15,300 / 7,650 / 11,450, Qualifying Widow(er)
15,300: booklet p.11 chart and Form IN-111 filing status boxes agree. Personal exemption 5,300: booklet p.11 Line 5e and
Form IN-111 Line 5e agree. Age or blind 1,250 per box: booklet p.10 Line 4, and the p.11 chart totals are each the
standard amount plus 1,250 per box.

**Per person or per return.** Per return, for the cap and for the election. Worksheet question 3: "enter your eligible
retirement system income or $10,000, whichever is less". Line 11: "Enter the lesser of the retirement income you
earned from that source or $10,000." Section II: "You may only elect one exclusion per taxable year." One amount for
every filing status, though the AGI test does split joint from others; one worksheet; one Line 12; no per-spouse
wording. The contributory and Social Security tests fall on the income ("benefits that are based on earnings not
covered"), not on a person, and there is no age test, so `who.basis` is `return`. On a joint return one spouse's
qualifying pension is enough. Reader A doubted the cap; the sources do not state it outright: flagged below.

**One election, and military.** Social Security, CSRS and other systems: one `best_of_group`, each `cannot_combine_with`
the other two. Military is outside: booklet p.33 and IN-112 Instr p.4, Line 13: "Taxpayers electing to utilize the
Military Retirement Income Exemption may claim one additional exclusion, if eligible, enumerated by 32 V.S.A. § 5830e."
So military plus one of the three. Railroad Retirement, Line 14, is separate and exempt in full.

**3% minimum tax.** Booklet p.11 Line 8: "Taxpayers who have a federal Adjusted Gross Income (AGI) greater than $150,000
must pay a minimum Vermont tax of 3% of federal AGI. If your federal AGI, Line 1, is greater than $150,000, enter the
amount that is higher: 1) 3% of your federal AGI less interest from U.S. obligations, or 2) tax calculated on Vermont
Taxable Income, Line 7, using the applicable tax rate schedule." The p.46 note agrees. In `recapture` with effect `other`,
`full_rate` 0.03, `starts_over` 150,000. The test is on AGI; the 3% base takes off the interest. It is a floor, not a
take-back of lower brackets, and no effect value says that, so `other` and an approximation spell it out.

**The phase-out.** `phase_out_rate` in the schema is a reduction per dollar (Utah, 2.5 cents a dollar). Vermont
multiplies the exemption by a share, "Divide Line 6 by $10,000 ... round to the second decimal place". A's 0.0001 would
read as a hundredth of a cent per dollar. So `effect: other` with the worksheet in `as_printed` (B), and I added `steps`
holding only the two printed ends (1 at the threshold, 0 at 80,000 / 65,000 / 175,000) so the projection can build from
record figures. At AGI of exactly 70,000 or 55,000 the worksheet's fraction is 1, so "less than" and the schema's "over"
agree; military prints "less than or equal to $125,000", the default. The rate is left out; Minnesota's settler kept one
on `other` and noted it had no precedent.

## One-sided entries

- `vt_authority_bond_interest` (A): kept. IN-112 Instr p.4 Line 15 prints it as exempt; B had it in notes.
- `vt_dependent_exemption` (B): kept.
- `annuity` in `covers` (A): dropped. The worksheet names only an annuity "of the U.S. government or a state government", a public pension kind. As `annuity` a private annuity would have matched.
- "contributory plan" in `who.other_conditions` (B, on other systems): kept, added to CSRS too, because the worksheet lists CSRS inside the contributory systems.
- `form` of U.S. obligations interest: A's text said subtraction, B exempt_in_full. Kept exempt_in_full, IN-112 Instr p.1 Line 7, "is exempt from Vermont tax"; compare treats them alike.

## Added by the settler, neither reader

- **Capital gains, IN-153.** Both readers left `capital_gains` empty for want of the schedule. Part I p.1: smaller of Schedule D Line 15 or 16, less Lines 18 and 19, less Form 4952 investment interest; "Enter the smaller of Line 8 or $5,000." Part II p.2: gain on assets held more than three years, less homes, depreciable personal property, and publicly traded stocks, bonds or other financial instruments; "Multiply Line 17 by 40%; enter result or $350,000, whichever is less." Part III: greater of the two, then the smaller of that or 40% of federal taxable income. Recorded the way New Mexico's is: two `capital_gains` entries plus two reliefs that hold the caps.
- **Credit for the Elderly or the Disabled, IN-119.** Part I Lines 8, 11, 12: "MULTIPLY Line 11 by 24% (0.24)", then off Vermont tax. The page says the same, "24% of the federal amount": no conflict. Recorded as a credit with `credit_rate` 0.24. `credit_basis` left out: 24% of a federal credit is neither covered income nor state tax.
- **`not_covered`** on the 10,000 exemptions, in the worksheet's words.

## Seniors and Retirees page against the 2025 booklet

The page is **not dated**: the only date is "Copyright © 2026 State of Vermont" in the footer, and it was retrieved
2026-11-07. The 2025 booklet and worksheets govern each of these. Each is a note in the record.

| Item | Page says | 2025 booklet and worksheet say |
|---|---|---|
| Social Security limits | full to 65,000 joint, 50,000 others; gone at 75,000 / 60,000 | full under 70,000 / 55,000; gone at 80,000 / 65,000 (p.16) |
| CSRS and other systems limits | "earned $75,000 or less" joint, "$60,000 or less" others | under 80,000 / 65,000, phased from 70,000 / 55,000 (p.16) |
| Additional age or blind amount | $1,000 | $1,250 per box checked (p.10) |
| Federal tie of that amount | must have "qualified and received the deduction at the federal level" | each standard deduction box checked on federal Form 1040 (p.10) |
| How many combine | "can only claim one" of Social Security, Military, CSRS, Other | military may add one more (p.33 Line 13) |
| Military amount | "the first $10,000", under the Social Security thresholds (the readers missed this one) | all of it to 125,000, gone at 175,000 (p.17, p.33) |

Its "exclude the first $10,000" for CSRS and other systems agrees with the worksheet. The sentence "The amount will be
adjusted annually for inflation" is kept as the only indexing statement in any source, cited to the page, even though
the page's own amount is stale. Its elderly credit (24%) agrees with IN-119.

## Projection

- **Brackets:** printed rows merged to four continuous bands, no base. Vermont does not step up at 75,000; the rows restart because the tax table ends there, and consumers read rates as marginal rates. Approximation: about a dollar.
- **CSRS and other systems: `not_modelled`, `warn_when: has_pension`, with an `overstates_tax` approximation.** The guide says two things: model a relief that turns on a contributory plan, and put Social Security-exempt employment in `not_modelled`. Vermont's test has both. `needs_input` has no value for the second fact, and modelling on `pension_contributory` alone would give 10,000 to a New York State member who paid Social Security tax. Minnesota's public pension subtraction is the same case and went the same way. Flagged below.
- **Social Security and military phase-outs: `stepped`, eight equal bands, each keeping the worksheet fraction at its middle.** Exact would be about 100 bands per status, whose edges (70,050 and so on) no record figure can build: the validator's chain needs a printed 50 or 100. Eighths come from halving the printed 10,000 and 50,000. Checked by script against the worksheet at AGI steps of 17 and 29: largest error 0.0625 of the exemption. `derived_figures` holds the 39 figures.
- **Capital gains:** the flat 5,000 as a capped relief, as New Mexico's. The percentage exclusion is `not_modelled`: a projection does not know the asset. `warn_when: never`, as New Mexico's business sale.
- **Elderly credit:** `not_modelled`, `always`, as Nebraska's: a projection does not compute the federal credit.
- **Blind amount, U.S. obligations and authority bond interest:** `not_modelled`, `never`, as other states. Dependents: `has_dependents`.
- **Age amount:** `min_age` 65. Printed test is "born before Jan. 2, 1961"; the page says age 65 or older. A person born on Jan. 1, 1961 is off by one year.
- **Indexing:** age amount true. The rest false, assumed. The blind amount is not a projection deduction.

## Unsure

- "A state government" as covering New York: the plain reading, but no source says so outright, and a Department answer or the statute (32 V.S.A. § 5830e, not in the sources) could narrow it. Little rests on it for a New York State pension, because the Social Security test already rules out a member who paid Social Security tax, and the exemption is not modelled.
- Per return on a joint return where both spouses have qualifying pensions: no printed line says 10,000 each, and none says 10,000 between them. Chosen from one line, one election and one amount for all statuses.
- The military combination: Line 13's "one additional exclusion ... enumerated by 32 V.S.A. § 5830e" does not say which exclusions; I read it as any one of the Line 12 elections.
- The schema has no straight-line share phase-out. If one is added (ends and a rounding), both phase-outs can be exact and the eight bands go away.
- Recapture `effect: other` has no precedent. A consumer must read the approximation to know it is a floor; a consumer needs its own handling for it.
- Whether the percentage exclusion's "40% of federal taxable income" limit (Line 20) also bounds the flat 5,000: Line 21 applies it to both, and the projection leaves it out as an approximation.

- Main session, 2026-11-07 (format for the first frozen schema): the additional-tax marker for early IRA withdrawals warns on an IRA or plan payout by a person under 60, not on any person under 60.

## 2026-11-07: format v1 adoption

- **Personal exemptions (IN-111 Line 5, booklet PDF page 11):** no income band. The booklet prints 5,300 for each exemption with no phase-out (the only "phaseout" in the booklet text is the military worksheet's Line 5). The phase-out the dispatch means is the retirement income exemption's, below. Unchanged.
- **`vt_social_security_exemption`:** the worksheet prints a formula, not a table: Line 7 = (Line 4 - AGI) / 10,000, "round to the second decimal place (Example: .481 would round to .48)", Line 8 = the lesser of Line 7 or 1 (booklet PDF page 16). Line 4 is the threshold plus 10,000, so this is 1 - (AGI - threshold) / 10,000. Projection: the 45 `stepped` steps become `share_phase_out`, `width` {all: 10000}, `share_decimals` 2, thresholds 70,000 joint and 55,000 others unchanged, `applies_when` over (at exactly 70,000 or 55,000 the share is 1).
- **`vt_military_retirement_exemption`:** also a printed formula: Line 7 = (175,000 - AGI) / 50,000, rounded to two decimals, Line 8 the lesser of Line 7 or 1 (booklet PDF page 17). Projection: the 9 steps become `share_phase_out`, `width` {all: 50000}, `share_decimals` 2, threshold 125,000, `applies_when` over ("less than or equal to $125,000" is full).
- **Record:** the same `income_test` (`effect` share_phase_out, `width`, `share_decimals` 2) on the Social Security, CSRS, other-systems and military exemptions, in place of `effect: other` with the two printed ends in `steps`; `as_printed` keeps the worksheet wording and says why it is the same straight line. 50,000 is now a record figure (printed on page 17 Line 7); 10,000 already was. A notes line records the change.
- **Removed:** the approximation "The retirement and military phase-outs are shown as eight equal bands ..." and all 41 `derived_figures` (band edges, band widths and keep shares); none is used now. No approximation added: with the two-decimal rounding the projection is the worksheet. The CSRS and other-systems exemptions stay `not_modelled` (Social Security-covered earnings test), so their record change has no projection effect.
- **Dollar effect:** inside the phase-out only, the exemption moves from the band's middle share to the worksheet's share; the old error was at most one sixteenth of the exemption. Single, AGI 57,110, taxable Social Security 13,600: exemption 11,050.00 (0.8125) becomes 10,744.00 (0.79), tax 1,067.31 becomes 1,077.56 (+10.25). Joint, AGI 140,020, military pay 60,000: exemption 41,250.00 (0.6875) becomes 42,000.00 (0.70), tax 2,416.02, about 25 less than the old bands gave (750 x 3.35% = 25.125). At and outside the band edges nothing changes.
- **Checks:** reworked `vt_2025_ss_single_partial` and `vt_2025_military_partial_joint` (verified blocks deleted); the military case's wages moved from 80,010 to 80,020 (AGI 140,020) so the tax is not a half cent (3.35% x 72,110 = 2,415.685). Added `vt_2025_military_at_125000` (single, AGI exactly 125,000: full exemption). Coverage of each share_phase_out: Social Security inside (`ss_single_partial`), at the threshold (`ss_joint_at_70000`), at the end (`ss_single_at_65000`); military inside (`military_partial_joint`), at the threshold (`military_at_125000`), at the end (`military_at_175000`).
- **Unsure:** the worksheet's rounding example (.481 to .48) does not say how an exact half rounds (AGI 57,150 single gives 0.785). The schema says only "rounded to share_decimals"; half up is the ordinary reading. No case sits on a half.

## 2026-11-08: marker ids and indexing covers

- Marker ids: all 10 markers have an `id`. Descriptive ids (no from_record id of their own): `vt_early_distribution_additional_tax`, `vt_medical_expenses_deduction`, `vt_record_notes_lines`; the rest take their first from_record id, so their warning codes are unchanged. `tools.checks --fix-warnings` rewrote the cases' accepted_warnings (the old shared code state_rule_not_modelled:unnamed becomes the new ids); nothing else in the cases changed.
- Indexing covers: each existing per-figure entry covers its own id: `vt_standard_deduction`, `vt_personal_exemption`, `vt_age_65_additional` (deductions:<id>); `vt_social_security_exemption`, `vt_military_retirement_exemption`, `vt_capital_gains_flat` (reliefs:<id>); plus `brackets` and `recapture`. No split needed.
- Assumed entries: none resolved; the only indexing statement (vt-seniors-and-retirees page, 'The amount will be adjusted annually for inflation') was already the record's `vt_age_65_additional` yes. Recapture: added `other_rule: minimum_tax_on_measure` after checking booklet PDF page 11 Line 8 and the PDF page 46 note: when federal AGI is over 150,000, Line 8 is the higher of 3% of federal AGI (less interest from U.S. obligations) and the rate-schedule tax. The 'less U.S. obligation interest' detail is the same Treasury-interest simplification as the projection's other U.S. obligation approximation.

## 2026-11-08: indexing settled from statutes

Statute research (work/indexing/findings*.json) settled every projection indexing entry that was `assumed: true`:

- `brackets` (brackets): indexed, 32 V.S.A. 5822(b)(2)
- `vt_standard_deduction` (deductions:vt_standard_deduction): indexed, 32 V.S.A. 5811(21)(D)
- `vt_personal_exemption` (deductions:vt_personal_exemption): indexed, 32 V.S.A. 5811(21)(D); face amount in (21)(C)(i)
- `vt_social_security_exemption` (reliefs:vt_social_security_exemption): not indexed, 32 V.S.A. 5830e(a)
- `vt_military_retirement_exemption` (reliefs:vt_military_retirement_exemption): not indexed, 32 V.S.A. 5830e(d)
- `vt_capital_gains_flat` (reliefs:vt_capital_gains_flat): not indexed, 32 V.S.A. 5811(21)(B)(ii)
- `recapture` (recapture): not indexed, 32 V.S.A. 5822(a)(6); compare (b)(2)
- Record `indexing`: added brackets -> yes; added recapture -> no; added vt_standard_deduction -> yes; added vt_personal_exemption -> yes; added vt_social_security_exemption -> no; added vt_military_retirement_exemption -> no; added vt_capital_gains_flat_cap -> no; added vt_capital_gains_flat_exclusion -> no.
