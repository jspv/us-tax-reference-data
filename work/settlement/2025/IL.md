# Settlement: Illinois, tax year 2025 (round r6)

Settled 2026-11-07 from `work/extract/2025/IL.r6.A.json` and `IL.r6.B.json`.
Sources: `sources/archive/2025/IL/`: the 2025 IL-1040 Instructions ("Instr"), Form IL-1040 ("Form"), Schedule M and its Instructions ("Sch M Instr"), Publication 120 R-12/25 ("Pub 120") and its HTML copy, whose rule text matches the PDF. Page numbers are PDF pages.

`uv run python -m tools.compare` reported **32 structured differences** (122 wording). They are six disagreements, and **all 32 lines were decided from the booklet**. Every line is about how entries are split or what they cover. No figure differed: rate, exemption amounts, thresholds, Social Security and municipal treatment all agreed.

## Structured differences

| # | Entry | Lines | A | B | Settled | Page |
|---|---|---|---|---|---|---|
| 1 | Indexing entries | 1 | `all_other` only | `all_other` and `personal_exemption`, both not_stated | A. The brief asks for an entry per figure the booklet says something about; it says nothing about adjusting the exemption. | Instr p.1 "The personal exemption amount for tax year 2025 is $2,850." |
| 2 | Government pensions, including `public_pension_other_state` | 10 | Two entries (`public_pension`; `military_pension`); other states in `covers_unclear` | One entry covering `public_pension`, `public_pension_other_state`, `military_pension` | B: one entry, other states in `covers`. See "Another state's pension" below. | Pub 120 p.2, p.3 |
| 3 | Employer plans and IRAs | 9 | One entry | Two entries | B. Separate bullets, and the 10-year averaging refusal reaches only a qualified retirement plan. | Pub 120 p.2, p.3 |
| 4 | Other Line 5 items | 6 | One entry (`capital_gains`, `wages`, `interest`) | Employer securities and retirement bonds each alone; group term life left out | Three entries, one per bullet, each with its own condition. Group term life kept from A: the booklet prints it. | Pub 120 p.2 |
| 5 | Sch M Line 22 `covers` | 3 | `interest` | `interest`, `dividends` | `interest`, with `dividends` in `covers_unclear` and the fund rule in `cap_rule`. The line says "distributions received from mutual funds", never dividends. | Sch M Instr p.3 |
| 6 | Sch M Line 21 military pay | 3 | Notes only | Relief entry | B kept. The booklet prints the subtraction and its exclusions. | Sch M Instr p.3 |

The compare's key for B's retirement bonds entry matched A's Line 22 entry (both `interest`), so that pair showed as wording. They are different rules; both are kept as separate entries.

## One-sided entries

- **Kept, from A:** group term life premiums (`il_group_term_life`).
- **Kept, from B:** `il_nua_employer_securities`, `il_retirement_bonds`, `il_military_pay`, and the `not_covered` wording on Line 21 and Line 22.
- **Added, neither reader as an entry:** `il_governmental_457`. Both held it in the text of the government entry, but Pub 120 p.2 gives it a bullet of its own, reported on "Line 1z or 5b", and its kind is an employer-plan distribution.
- **Added, neither reader:** `annuity` in `covers_unclear` on `il_qualified_plan`. Not named on Line 5, and Pub 120 p.3 refuses "income that is not from a qualified employee benefit plan". Federal Line 5b is "Pensions & annuities" (Instr p.17).
- **Dropped:** A's `not_covered` on the government entry. That text is about non-government plans, so it now sits on `il_governmental_457` and `il_qualified_plan`.
- **Dropped:** B's `personal_exemption` indexing entry (item 1).
- **Notes only:** retired partners' payments, railroad sick pay (Sch M Line 37), college savings subtractions, property tax and K-12 credits (Schedule ICR is not in the sources).

## The five required settlements

**1. Another state's pension, and New York State's: covered, in the same entry as Illinois's own (`public_pension_other_state` in `covers`; no `paying_states`, no `not_covered`).** Decided from Pub 120's wording, as the dispatch asked:

- The allowance has no limit to Illinois. Pub 120 p.2: "You may subtract the amount of any federally taxed portion (not the gross amount) included in your Form IL-1040, Line 1 that you received from ... a government retirement and government disability plan, including military plans".
- "Government" there is not Illinois's government, because the same bullet's "military plans" are not Illinois plans.
- The next bullet reads "a state or local governmental deferred compensation plan", not an Illinois one.
- The refusal turns only on government or not. Pub 120 p.3: "from deferred compensation and disability plans that are not government plans."
- Illinois says Illinois when it means it: Sch M Instr p.4 Line 34, "obligations of Illinois state and local governments"; Sch M Instr p.2 Line 13 names Illinois's plans and refuses "any other college savings program".

A is right that no sentence names another state. That silence would make it unclear only if the wording were limited, and it is not. Two passages could be read the other way, and neither changes this:

- Sch M Instr p.1, "May I subtract my out-of-state income? No", answers what Schedule M allows. The same list says "income received from Social Security benefits and retirement plans (including Illinois Teacher's Retirement). Eligible retirement income should be subtracted on Form IL-1040, Line 5." So retirement income is outside that question, and "including" gives an example, not a limit.
- Pub 120's bullet says "reported as wages on ... Line 1z". Form Line 5 says "Generally on fed. Forms 1040/1040-SR, Lines 4b, 5b, and 6b", and Pub 120 p.3 lists "government retirement, including military plans" with a Form 1099-R where Lines 4b, 5b and 6b do not identify the income. The line reference does not narrow the kind.

No reciprocity rule concerns pensions: the agreements cover compensation only (Instr p.3).

**2. Illinois and federal government pensions: subtracted in full.** Same bullet, `public_pension` and `military_pension`. Illinois's is named: "retirement plans (including Illinois Teacher's Retirement)" (Sch M Instr p.1). A federal civilian pension is not named as such; it falls under the same "a government retirement ... plan", and "military plans" shows federal plans are within it. Second document: Instr p.7 Line 5, "government retirement and government disability plans".

**3. Private pensions, IRAs, plans, conversions: subtracted in full, no cap, no age test.**
- Pub 120 p.2: "a qualified employee benefit plan including 401(k) plans".
- Pub 120 p.2: "an Individual Retirement Account (IRA) (including amounts rolled over to a Roth IRA) or a self-employed retirement (SEP) plan".
- Roth conversions are in `covers`, confirmed by a second line. Pub 120 p.3: "converting a traditional IRA to a Roth IRA".
- Pub 120 p.2: "You may include early distributions from qualified plans and IRAs."
- `not_covered`: income not from a qualified plan, third-party sick pay, non-government deferred compensation and disability plans, and income under the 10-year averaging method (Pub 120 p.3).

**4. Social Security: exempt.** Three documents:
- Form Line 5: "Social Security benefits and certain retirement plan income if included in Line 1."
- Instr p.7 Line 5: "federally taxed Social Security and retirement income".
- Pub 120 p.2: "Social Security benefits reported on your U.S. 1040 or 1040-SR, Line 6b."

**5. Rate, standard deduction, exemptions.**
- Flat rate for every status. Instr p.1: "The Illinois income tax rate is 4.95 percent (.0495)". Form Line 12: "Multiply Line 11 by 4.95% (.0495)". No schedule by status is printed.
- No standard deduction line on the Form; federal itemized deductions are refused (Sch M Instr p.1).
- Exemptions: 2,850; 5,700 joint (Instr p.8 chart). The chart's Single row "includes Single, Head of Household, Widowed, and Married filing separately".
- A federal Qualifying Surviving Spouse chooses "Widowed" (Instr p.6), so that status gets 2,850 and the 250,000 test, not the joint figures. The projection writes this status out, because a status left out would fall to the joint amount.
- Age 65 and blind: 1,000 per box (Instr p.8; Form Lines 10b, 10c).
- Allowance removed when federal AGI is "greater than" 250,000 (500,000 joint) (Instr p.8).

## Newer fields

- **`income_test.applies_when`:** `over` on all three phase-outs. The word printed is "greater than", so an AGI of exactly 250,000 keeps the allowance. Thresholds are the printed figures.
- **`all_income_scope`:** does not fit and is not used. Illinois has no `all_income` relief; its exemptions are `base.deductions`.
- **`paying_states`:** not used; the rule does not depend on the payer.
- **`stepped`, `share`, `credit_basis`, `recapture`, `brackets.derivation`:** nothing here fits them. Recapture is an empty list. "Recapture of investment tax credits" (Line 13) is not a bracket recapture.

## Municipal interest

Record `other` (both readers). Illinois's own bonds are not exempt as a class: "Interest from state and local government obligations is not exempt from Illinois Income Tax except where legislation has been specifically adopted" (Sch M Instr p.4). Line 2 adds back all federally tax-exempt interest. Only listed obligations come off on Lines 34 and 35.

Projection `all_taxed`, with an overstating approximation. I did not use `other_states_taxed_own_exempt`, the mapping other states took, because a consumer that can tell Illinois bonds apart would then exempt bonds Illinois taxes.

## Projection choices

- **No `needs_input`.** Government, military, qualified private plans, IRAs and railroad all come out the same, so a household need not be asked its pension's source. The guide requires it only for a relief that treats them differently. The cost is one approximation: non-qualified plans are treated as subtractable.
- **Social Security** is `treatment: exempt` with no relief entry, as in the settled states.
- **Not modelled, because the kind would over-reach:** `il_us_obligation_interest` and `il_retirement_bonds` (`interest`), `il_nua_employer_securities` (`capital_gains`), `il_group_term_life` and `il_military_pay` (`wages`). Listing those kinds in a relief would exempt all of that income.
- **Also not modelled:** blind exemption, dependent allowance, dependent-filer chart, retired partners' payments.

## Unsure

- **Other-state pensions rest on wording.** No line names them, and Pub 120 says it does not quote the statutes and does not take their place. The statute was not read.
- **Retired partners' payments:** the documents conflict. Pub 120 p.3 and Instr p.7 send them to Schedule M; Sch M Instr p.2 says "Do include these amounts on Form IL-1040, Line 5." Noted, not modelled.
- **Indexing:** `not_stated`, so `indexed: false, assumed: true`. The exemption sits under "What's New for 2025?" as the amount "for tax year 2025", which hints that it changes by year but does not say so. The statute should be read; if it is indexed, the projection overstates tax in later years.
- **Dependent amount:** Schedule IL-E/EITC is not in the sources, so the figure is missing. Instr p.1 says it "was updated".
- **Line 22 mutual fund distributions:** whether they count as `dividends` is left in `covers_unclear`; it has no effect on the projection.

## 2026-11-08: marker ids and indexing covers

- Marker ids given: first from_record id (warning code unchanged): `il_blind_exemption`, `il_personal_exemption`, `il_us_obligation_interest`, `il_retirement_bonds`, `il_nua_employer_securities`, `il_group_term_life`, `il_military_pay`; descriptive: `il_dependent_allowance` (no from_record id); `il_retired_partner_payments` (no from_record id).
- Indexing covers: `brackets` -> `brackets`; `deductions` -> `deductions`.
- Every `assumed` answer was checked again against the archived sources (searched for indexed, inflation, cost-of-living, adjusted annually, each year, CPI, fixed): none says, so all stay `assumed: true`. The instructions say 'The personal exemption amount for tax year 2025 is $2,850' (PDF page 1); that names the year's amount but does not say it is adjusted, so `deductions` stays assumed.
- `tools.checks --fix-warnings` updated the cases' accepted_warnings where a code changed; nothing else in the cases changed.

## 2026-11-08: indexing settled from statutes

- `brackets` (projection `brackets`): not_indexed, 35 ILCS 5/201(b)(14): flat 4.95% from 0. Record `brackets` added as no.
- `deductions` (projection `deductions`): split, replaced by `il_personal_exemption` (`deductions:il_personal_exemption.amount`, indexed, 35 ILCS 5/204(b)(7), (d-5): CPI-U over 2011, rounded down to 25, written through tax years ending 2028), `il_age_65_exemption` (`deductions:il_age_65_exemption.amount`, not_indexed, 204(d)(1)(A)) and `exemption_phase_outs` (both phase-outs, not_indexed, 204(g)). The figures are named by deduction id so the deductions-answer check holds. Record `il_personal_exemption` added as yes, `il_age_65_exemption` as no. The existing `all_other` entry is left.
- Unsure: the indexed basic amount is defined only for tax years ending on or before December 31, 2028; the statute is silent after that. The projection grows it with no end year.
