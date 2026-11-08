# NM 2025 settlement

Readings: `work/extract/2025/NM.r6.A.json`, `NM.r6.B.json`. Sources: `sources/archive/2025/NM/`. Pages are PDF pages. PIT-1 means the 39-page instructions, ADJ the 8-page PIT-ADJ instructions; "Form" means a return form. PIT-1 pp.22, 25, 27, 28, 30, ADJ pp.5, 7, 8 and the rate table's p.7 were rendered and read as images as well as text.

Settled in two passes on 2026-11-07. The second pass added the 2025 Tax Rate Table and the Forms PIT-1, PIT-ADJ, PIT-RC and PIT-B, which the readers did not have.

## Brackets

First pass: both readers left brackets empty, correctly, because the rate tables were not archived. The 2025 Tax Rate Table (`2025trt`, 7 pages) was then added. It prints tax by income row up to 100,000 and a base-plus-rate section over 100,000 (p.7, T-7). It prints no bracket schedule below 100,000.

| Status | 1.5% from | 3.2% from | 4.3% from | 4.7% from | 4.9% from | 5.9% from |
|---|---|---|---|---|---|---|
| Single | 0 | 5,500 | 16,500 | 33,500 | 66,500 | 210,000 |
| Married filing jointly, surviving spouse | 0 | 8,000 | 25,000 | 50,000 | 100,000 | 315,000 |
| Married filing separately | 0 | 4,000 | 12,500 | 25,000 | 50,000 | 157,500 |
| Head of household | 0 | 8,000 | 25,000 | 50,000 | 100,000 | 315,000 |

- **Printed:** 4.9%, 5.9%, the starts 210,000, 315,000, 157,500, and the 100,000 start of the 4.9% band for joint and head of household.
- **Derived:** everything else, from the table's rows. Tested at each row's midpoint, the schedule reproduces all 1,001 rows for all four statuses, largest gap 0.50 (rounding). Moving any one start by 100 or any one rate by 0.1% breaks the fit (smallest worst gap 0.65). The printed example checks: joint at 25,350 is 679.05, printed 679.
- **Validator:** `brackets.derivation` has 24 rows, 6 per status, one in each band below 100,000 plus the last row. Method `tax_table`; no `formula`, because the validator tests one formula on both single and joint, and the printed bases differ by status.
- **Surviving spouse:** "* This column must also be used by surviving spouse."

**The over-100,000 rows are not in `table_rows`, and the validator does not re-check them.** Each printed base is the table's last row (99,900 to 100,000, midpoint 99,950), not the tax at 100,000:

| Status | Schedule at 100,000 | Printed base | Gap | Top base printed | Base + 4.9% of the excess |
|---|---|---|---|---|---|
| Single | 4,358.00 | 4,356 | 2.00 | 9,746 at 210,000 | 9,746.00 |
| Joint, head of household | 4,089.00 | 4,087 | 2.00 | 14,622 at 315,000 | 14,622.00 |
| Separate | 4,494.50 | 4,492 | 2.50 | 7,310 at 157,500 | 7,309.50 |

The validator allows 1 dollar, so a row at 100,000 fails. I did not change the rule, and I did not move a start or add a band to close the gap: either would add a figure the table does not print. The bases are covered indirectly, since the 99,900 row is in `table_rows` for every status and prints the same number. The top bases were checked by hand (last column). The projection carries an `overstates_tax` approximation of 2 (2.50 separate) on every income over 100,000.

The `warn_when: always` marker and the empty-brackets approximation are removed.

## Hidden text in the PDFs

Both PDFs carry editors' working notes in the text layer that are not on the printed page. Both converters pick them up, so the readers saw them as booklet text. Rendered pages do not show:

- ADJ p.5: the "7-2-34 HB 252 Section 8 TY 2025 Change to" box, including "$1,0002,500" and "IMPORTANT: You may not claim the net capital gains deduction in addition to credit provided by the Venture Capital Investments Act", and "UPDATED PER NOTE, 6/17/2025, MJ".
- ADJ p.7: the "HB-0252 Section 32 / Made exemption permanent" box.
- PIT-1 p.22: "Need to determine if this act has been extended or has lapsed."
- PIT-1 p.25: the HB-6(2019) extract.
- PIT-1 p.27 (the first also on p.10): "2024 HB-0252 Section 8 changed to ..." and "Remove A taxpayer may not claim the deduction ...".

None of this is recorded as a rule. It changed three things:
- Both readers wrote the Venture Capital bar into the gains entries; dropped (the same hidden layer on PIT-1 p.27 says "Remove", so it may even be repealed).
- A's armed forces cite to the margin note; dropped. The surviving-spouse wording is in the printed line 24, so the rule stands.
- A's and B's "$1,0002,500" notes; dropped. The printed line 16 says $2,500, and PIT-1 p.27 agrees.

The same scan on the rate table and the four forms found only form-field leftovers ("blah" on Form PIT-ADJ, a repeated line on Form PIT-1), no rule. Other states' PDFs could carry hidden notes; `tools.validate` cannot see them, since it reads the same text layer.

## Structured differences: 261

| Fields | Count | A | B | Settled | Source |
|---|---|---|---|---|---|
| Age 65 and blind `phase_out.steps` | 220 | 8 rows per status, from over 30,000 etc. | 9 rows, with 8,000 from 0 at_or_over | B | ADJ p.5 Table 1 prints nine rows |
| Medical care exemption | 9 | relief, all_income, min_age 65, cap 3,000 (6 fields) | deduction, other, per return (3) | B | ADJ pp.5-6 line 18 |
| U.S. obligations covers | 6 | interest, dividends | interest | A | ADJ p.3: "You may deduct dividends from mutual funds invested in U.S. government obligations" |
| Tribal member income | 7 | all_income, person scope (4) | wages, public and private pension (3) | A, with B's `not_covered` | ADJ p.3: "your income is exempt" |
| 40% business-sale gains `applies_to` | 6 | other | long_term | A | ADJ p.5: "from the sale of a business" |
| New Mexico interest, line 7 | 3 | relief | notes, `muni_interest` | Kept | ADJ p.2 line 7 |
| Personal exemption | 3 | notes | deduction of 0 | A | PIT-1 p.22 prints no amount |
| Organ donation | 3 | notes | deduction 10,000 | B | ADJ p.6 line 19 |
| School supplies | 3 | notes | deduction 1,000 per person | B | ADJ p.8 Table 3 |
| `social_security.treatment` | 1 | relief | exempt | A | ADJ p.7 |

All 261 are settled: 252 from the booklet, 9 (medical care) by which schema slot fits, where the booklet's facts are not in dispute. The 220 step lines are one disagreement: B's extra first row shifted every index.

- **Steps.** Table 1 checks: the printed examples give 6,000 each at joint AGI 35,000 and 8,000 each at 28,000. Bands printed "30,001 to 33,000" are recorded as over 30,000. Both patterns are in settled states (CT without the first row; AL, NC, NJ with it), and B's holds every printed row.
- **Medical care.** It is a flat $3,000 tied to $28,000 of spending. As an `all_income` relief with `min_age` it would appear in the pension report as a general age relief, which it is not. The same fit as ND's expense-based deductions.
- **Tribal income.** "Your income is exempt" is not limited to wages, and ND settled the same rule as `all_income` with person scope. Pension wording is in `other_conditions`, and B's `not_covered` is kept.
- **Social Security.** The schema's `exempt` has no income limit. ADJ p.7 Example 2: "No part of the taxpayer's social security income qualifies" above the limit. So `relief`, with the entry saying how.
- **Personal exemption.** Rule 7 asks for printed amounts; none is printed, and an entry of 0 would be derived. Quote kept in notes.

## One-sided entries

Kept: organ donation, school supplies, line 7 interest, A's `not_covered` for U.S. obligations (both had it), B's Indian `not_covered`, A's Railroad condition.

Dropped: B's personal exemption entry. A's and B's notes on the margin text.

Added by the settler, in neither reading:
- `net_capital_gains_cap`. The `capital_gains` section has no cap field, and both readers held 2,500 only in `condition` text. Taken literally, `deduction_share` of 1 exempts all long-term gains. The relief holds 2,500 as a figure; the `capital_gains` entries stay as the readers had them. Projection `capital_gains` is empty so nothing counts twice.
- `low_middle_income_exemption` split into three entries with `phase_out_rate`. Both readers used `effect: other` with the factors in text, so a projection could not carry them. Booklet treats it as one rule; the schema's single `rate` forces the split. Recomputed: 2,500 reaches 0 at 36,666.67, 55,000, 27,500, matching the printed ceilings.

## Always-settled questions

1. **Another state's government pension, New York in particular:** not found as a rule of its own. Neither `covers` nor `not_covered` holds `public_pension_other_state`. New York appears nowhere in the sources. PIT-1 p.28 line 20 NOTE: "if you receive a pension from your former California employer and you now reside in New Mexico, California may not tax your retirement income. Because you are now a New Mexico resident, your retirement income is taxable in New Mexico." Taxed like other income; the example does not say the employer was a government. **Second pass:** Form PIT-B settles the doubt. Line 3 is "Pensions, annuities, social security, and lump-sum distributions", with no split by payer, and its NOTE says "Resident taxpayers including persons physically present in New Mexico 185 days or more, must allocate all income and deductions on lines 1, 2, 3, and 7 in full to New Mexico." A paying state's pension goes on that line like any other.
2. **Own and federal government pensions:** no relief. ADJ p.1: "If an item is not listed, it is not a valid New Mexico addition, exemption, or deduction for this schedule." Exceptions: armed forces retirement pay, $30,000 each, ADJ p.7 line 24: "Each qualifying armed forces retiree or surviving spouse of an armed forces retiree may claim an exemption in an amount equal to $30,000 of armed forces retirement pay"; second document PIT-1 p.27. Tribal retirement income, ADJ p.3: "Retirement or pension income is exempt when the retirement or pension is the result of employment within the boundaries". Railroad Retirement, ADJ p.3: "These types of income are exempt from state income taxes."
3. **Private pensions, IRA and employer-plan distributions, Roth conversions:** no relief; same ADJ p.1 quote, and they are in the federal AGI on line 9. PIT-1 p.19 lists "an IRA distribution; an annuity; a pension, Railroad Retirement, other retirement pay" as income to gather. ADJ p.2: "You may not deduct interest and dividends from IRAs." Lump sums on Form 4972 may use averaging (PIT-1 p.27 line 19). Form PIT-ADJ confirms it: 28 lines, none for pensions, IRAs or employer plans beyond those named here. **Roth conversions:** not found in the booklet or on any form.
4. **Social Security:** exempt up to an AGI limit, otherwise taxed in full. ADJ p.7 line 25: "If your federal Adjusted Gross Income (AGI) does not exceed the maximum for your filing status, as listed in Table 2 (below), enter the amount of social security income included in your AGI." Table 2: single 100,000; separate 75,000; joint, head of household, surviving spouse 150,000. Second document, the agency web page: "less than $100,000", "under $150,000", "under $75,000". These differ only at the exact limit; the booklet's wording and its Example 1 ("not above $100,000") are used, and the web page is a 2022 statement. Third: PIT-1 p.27. Fourth: Form PIT-ADJ line 25, "Exemption for social security income."
5. **Schedules, deductions, exemptions:** four schedules, see Brackets. Standard deduction: none of New Mexico's own; PIT-1 p.25 line 12 takes "the allowable federal standard deduction from federal Form 1040 or 1040SR, line 12", no figure printed. Personal exemption: PIT-1 p.22 "Deduction amounts for personal exemptions are suspended for tax years 2018 through 2025". Age 65 or blind: up to 8,000 each by Table 1. Low- and middle-income: up to 2,500 per exemption. Dependents: 4,000 each beyond the first, joint or head of household only.

## Projection choices

- **`starts_from: federal_taxable_income`, although the record says `federal_agi`.** This is my call and neither reader's. PIT-1 line 17 subtracts the federal deduction, and no source prints a figure, so `federal_agi` with no deduction would overstate tax by the whole federal deduction. Re-checked on Form PIT-1: line 9 is federal AGI, line 12 is "Federal standard or itemized deduction amount (from federal Form 1040, line 12", and no line takes anything the federal return subtracts after line 12. So the record is right to say `federal_agi`, the projection's mapping stands, and the approximation's direction is confirmed. The guide allows federal deductions when the state's law starts there; Montana is the nearest settled case. Record stays `federal_agi` because the booklet's first line and its headings say so. Approximation `understates_tax`: New Mexico subtracts line 12 only, so what the federal return subtracts after line 12 stays taxable.
- Modelled: Social Security (income test `removes`), armed forces retirement (`needs_input: pension_source`), Railroad, age 100, the 2,500 gains cap (1,250 separate, `derived_figures`, half), age 65 exemption, low- and middle-income exemption per person.
- `not_modelled`: blind, dependents, medical care exemption, PIT-RC 65+ credit and rebate, U.S. interest, line 7, 40% gains, tribal income, active duty, organ donation and teacher supplies, other PIT-ADJ lines, lump sums, credit for tax paid elsewhere, part-year, low-income credits. No entry uses `warn_when: always` now. The PIT-RC figures come from the Form: property tax rebate at modified gross income of 16,000 or less, at most 250 (125 separate); low income rebate at 36,000 or less.
- Indexing: all `indexed: false, assumed: true`; no statement in either booklet.

## Unsure

Closed in the second pass:
- **Brackets:** filled in, see Brackets.
- **Base mapping:** confirmed by Form PIT-1, though a reviewer may still prefer a schema value for "federal AGI less the federal deduction".
- **California example:** Form PIT-B line 3 and its NOTE settle general pension treatment.
- **Forms, rule 0:** PIT-1, PIT-ADJ, PIT-RC and PIT-B read. Nothing in the record's rules changed as a result; the forms added the base cite, the PIT-B quote and the PIT-RC figures.

Still open:
- **Over-100,000 rows** are outside the validator's check, see Brackets. A consumer needing the printed section to the dollar has a 2.00 to 2.50 gap.
- **Derived starts** are fixed to the nearest 100 by the table. A start between grid points would fit too; round figures are the plain reading.
- **Hidden text.** The Venture Capital bar might be current law; the booklet as printed does not state it, and Forms PIT-1 and PIT-ADJ are silent. PIT-CR is not in the sources. A scan of all 47 booklet pages for text placed outside the printed area found notes only on PIT-1 pp.10, 22, 27 and ADJ pp.5, 7 (p.10 repeats the HB 252 note and carries no rule used here). The scan is not complete: it did not flag the HB-6 extract on PIT-1 p.25, which rendering showed is not printed. ADJ pp.1-4 and 6 were read as text only, where no out-of-flow block appears.
- **`tools.report_pensions`** shows NM's rows as "exempt in full; age 100+", because every `all_income` entry with an age appears there. It is correct but reads oddly at a glance; the real answer for almost everyone is "taxed". The tool is not one of my outputs.
- **PIT-RC instructions** are not in the sources, so the refundable medical care credit's terms are unread. Also absent: PIT-CR, PIT-S, PIT-B instructions.
- **Married centenarian** rule (half of community income) maps to `all_income_scope: person` with an `either` approximation.

## 2026-11-08: marker ids and indexing covers

- Marker ids: all 14 markers have an `id`. Descriptive ids (no from_record id of their own): `nm_medical_care_credit_property_tax_rebate`, `nm_other_pit_adj_lines`, `nm_lump_sum_averaging`, `nm_other_state_credit_part_year`, `nm_rebates_and_credits`; the rest take their first from_record id, so their warning codes are unchanged. `tools.checks --fix-warnings` rewrote the cases' accepted_warnings (the old shared code state_rule_not_modelled:unnamed becomes the new ids); nothing else in the cases changed.
- Indexing covers: `brackets`, `deductions` (amounts and phase-outs); `relief_caps` covers reliefs.cap (armed forces retirement pay, net capital gains cap). Added `relief_income_tests` (indexed false, assumed) for reliefs.income_test (the Social Security exemption's income limit), which no entry covered.
- Assumed entries: searched the archived sources (docling, pypdf and page text) for indexed, inflation, cost of living, adjusted annually and consumer price index, and for statements that figures are fixed; nothing says, so every `assumed: true` stays.
