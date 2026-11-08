# Settlement: New Jersey, tax year 2025 (round r4)

Settled 2026-11-07 from `work/extract/2025/NJ.r4.A.json` and `NJ.r4.B.json`.
Sources (`sources/archive/2025/NJ/`): `1040i` (2025 NJ-1040 Instructions, cited "Instr"), `1040` (the form), `git1_2` (GIT-1 & 2 Retirement Income, January 2026, cited "GIT"), `njit6.page.txt` (Retirement Income web page) and `njit7.page.txt` (Retirement Income Exclusions web page). Page numbers are PDF pages.

`uv run python -m tools.compare` reported **306 structured differences** (119 wording). Almost all come from keying, not from different facts:
- B split the pension exclusion into two entries (age 62; blind/disabled), and A wrote one. A also listed `roth_conversion` and not `public_pension_other_state`, so no pension-exclusion entry matched across the readers. That accounts for 73 + 38 differences, plus most of the 62 on the unclaimed exclusion, which are its 20 steps.
- The rest are `who.basis` keys on the exempt entries and one capital-gains entry.

The facts underneath reduce to the points below.

## Structured differences

| # | Field | A | B | Settled | Source |
|---|---|---|---|---|---|
| 1 | Pension exclusion: other states' government pensions | `public_pension_other_state` in `covers_unclear` | in `covers` | **covers**, no `paying_states`. The same applies to the disability-pension entry. | njit6, Taxable Retirement Income: "Taxable pensions include all state and local government, teachers', and federal pensions ... However, if you ... were 62 or older or disabled, you may be able to use the retirement exclusions to reduce your taxable income." GIT p.4: "State, local government, teachers', and federal pensions are all treated the same as private sector employee pensions and annuities." Instr p.15 lists "Federal, state, and local government, and teachers' pensions" as taxable on line 20a. Instr p.22: "You can exclude all or part of the income reported on line 20a". No source limits "state" to New Jersey, and none prints a reciprocity rule. |
| 2 | New York State pension | not found; treated like row 1 but unclear | not found; within the general rule | Same as row 1: taxable on line 20a, and the line 28a exclusion applies. Recorded in a note. | No source names any other state's pension. New York appears only in the credit for tax paid to other jurisdictions (Instr, "Income From New York", Schedule NJ-COJ) and in a GIT nonresident example (Nyack, NY). "all state ... pensions" (njit6) covers it. |
| 3 | Pension exclusion: Roth conversions | `covers` | `covers_unclear` | **covers** | GIT p.18: "If you convert a traditional IRA to a Roth IRA, any amount from the existing IRA that would be taxable if withdrawn must be included in your income on line 20a". Instr p.16: "If you converted an existing IRA to a rollover Roth IRA during Tax Year 2025, any amount from the existing IRA that would be taxable if withdrawn must be included on line 20a." Instr p.22, Line A of the exclusion: "Amount from line 20a". The worksheet line takes conversions (extraction brief rule 4). No source says in so many words that conversions qualify. |
| 4 | Pension exclusion: age or disability | one entry, min_age 62, disability in `other_conditions` | two entries with `best_of_group` and `cannot_combine_with` | **Two entries** (`nj_pension_exclusion_age62`, `nj_pension_exclusion_disabled`) sharing `best_of_group: nj_pension_exclusion`. `cannot_combine_with` dropped: on a joint return one spouse can qualify by age and the other by disability under the one maximum, and a cannot-combine list would forbid that. | Instr p.22: "You (and/or your spouse if filing jointly) were age 62 or older or blind/disabled as defined by Social Security guidelines on the last day of the tax year". |
| 5 | Pension exclusion: first band of `steps` | `keep_share` 1 | `amount` = the cap | **A** (`keep_share` 1, with the dollar maximum in `cap`). The bands and shares agree in all three sources. | Instr p.22 chart: $0–$100,000: $100,000 / $75,000 / $50,000; $100,001–$125,000: "50% of line 20a" / "37.5%" / "25%"; $125,001–$150,000: "25%" / "18.75%" / "12.5% of line 20a". GIT p.19: "Multiply your taxable pension found on Line 20a ... by the percentage". njit7 says the same. |
| 6 | Line 20a vs line 27 percentages | noted, recorded as printed | noted, recorded as printed | **Each as printed, on its own exclusion:** line 20a shares on the pension exclusion (28a), line 27 shares on the unclaimed exclusion's maximum (Worksheet D/E). These are two rules, not a misprint. | Instr p.22 chart "% of line 20a"; Worksheet D (p.23) and E (p.24) charts: "50% of line 27", "37.5% of line 27", etc. GIT p.25 example (joint, total income $114,000, pension $6,200) uses both: "Maximum Pension Exclusion $3,100" (50% of 6,200) and "Maximum Exclusion $57,000" (50% of 114,000), "Unclaimed Maximum Exclusion $53,900". |
| 7 | Unclaimed exclusion: income test | `stepped` from 100,000 (keep_share of the cap) | `removes` over 150,000, with the percentages in `cap_rule` | **B.** A step's `keep_share` is a share of the relief and can't hold "50% of line 27". | Worksheet D (p.23): "Is income on line 27, NJ-1040 MORE than $150,000? Yes. You are not eligible to use any unclaimed portion of your maximum exclusion." |
| 8 | Military pension `who.basis` | each_person | return | **each_person** | njit6: "Military pensions and survivor's benefit payments, regardless of your age or disability status". Each person's own pension. |
| 9 | Social Security / railroad entry | railroad only | one entry covering social_security and railroad_retirement | **Railroad only.** Social Security is held in `social_security.treatment`. | Instr p.10 "Federal Social Security", "Railroad Retirement (Tier 1 and Tier 2)" |
| 10 | Capital gains on exempt obligations | entry (applies_to other, exempt) | empty | **A's entry kept** | Instr p.10: "Interest and capital gains from (1) obligations of the State of New Jersey or any of its political subdivisions; or (2) direct federal obligations exempt under law" |
| 11 | Disability pension: other states | not in covers | `public_pension_other_state` in covers | **B**, by row 1 | Instr p.15 "Public or private disability pension benefits until the year you turn 65" |

## The pension rules for a New Jersey resident (from rows 1–3)

- **New Jersey state pension, New York State pension, any other state's or local government pension, federal civil service pension, private pension, annuity, IRA, 401(k)/403(b)/457 distribution, and the taxable part of a Roth conversion:**
  - All of these are taxable on line 20a.
  - New Jersey's taxable amount excludes contributions that were taxed when made: the Three-Year Rule, the General Rule, or IRA Worksheet C, reported on line 20b.
  - The line 28a Pension Exclusion applies to the person who is 62 or older, or blind or disabled, on December 31. The maximum is 100,000 joint, 75,000 single, head of household or qualifying widow(er), and 50,000 separate, when line 27 is $100,000 or less. Above that it is a share of the qualifying line 20a income: 50% / 37.5% / 25% for line 27 of $100,001–$125,000, and 25% / 18.75% / 12.5% for $125,001–$150,000. Over $150,000 there is none.
  - The maximum is one per return. On a joint return only the qualifying spouse's income is excluded.
- **Military pension:** exempt at any age. Civil service pensions are taxable "even if based on credit for military service".
- **Disability pension:** exempt until the year the person turns 65.
- **Social Security and Railroad Retirement:** exempt.

## Other retirement income exclusion (line 28b)

- **Unclaimed exclusion** (`nj_unclaimed_pension_exclusion`).
  - Who qualifies: the person must be 62 or older (disability does not count), line 27 must be $150,000 or less, and wages, business, partnership and S-corporation income (lines 15, 18, 21, 22) must total $3,000 or less, combined on a joint return.
  - Amount: the Worksheet D maximum minus line 28a. The maximum is the filing-status amount up to $100,000, then the line 27 shares.
  - What it covers: any income of the qualifying person. GIT p.22: "exclude other types of income (wages, interest, dividends, etc.)". The GIT p.24 and p.26 examples limit it to that person's income.
  - Recorded as `all_income`, as both readers had it.
- **Special exclusion** (`nj_special_exclusion`).
  - Amount: 6,000 for joint, head of household and qualifying widow(er); 3,000 for single and separate. Source: Instr p.22, and GIT p.26 agrees.
  - Who qualifies: you and/or your spouse are 62 or older, and neither spouse can ever receive Social Security or Railroad Retirement benefits.
  - There is no income limit: in the GIT p.27-28 example a return with $154,000 of income still gets 6,000.
  - Both readers had the same amounts. `who.basis` is return.

## Brackets (point 5)

- **Recorded as printed.** The rate schedules (PDF p.65) print the bracket starts and rates directly ("Over / But not over", "Multiply Line 42 by", "Subtract"). Both readers had the same starts and rates.
  - Table A covers single and married/CU partner separate. Table B covers joint, head of household and qualifying widow(er).
  - `married_separate` repeats Table A and `head_of_household` repeats Table B.
- **`brackets.derivation` added, with method `tax_table`.** A helper (in the private scratch folder) parsed all 2,000 Tax Table rows (PDF p.56-64, 0 to 100,000) for both columns. The recorded schedules reproduce every row at the row midpoint, rounded to the dollar: 0 mismatches. Sixteen rows across every band below 100,000 are recorded, including the booklet's Evans example (39,850–39,900: 713 / 628).
- **Why not `formula`.** The schema has one `formula`, and the validator checks it against both the single and the joint schedule. New Jersey's subtraction constants differ by status above 20,000, so no printed formula could be recorded without failing one status. All 15 printed constants are listed in a record note instead.
  - I checked each constant against the bands. 14 of the 15 match exactly.
  - The exception is Table B 70,000–80,000, ".035 – $1,154.50". The bands give 1,155.00 there, so the printed constant gives 0.50 more tax across that band.
  - The Tax Table follows the bands, not the constant: the 70,100–70,150 row prints 1,299, and the formula would give 1,299.88. Taxable income under 100,000 must use the table, so that constant is never the one applied.
  - Both converters print 1,154.50.
- **No surtax and no recapture.** 10.75% over 1,000,000 is an ordinary bracket.

## One-sided entries

- **Kept:**
  - The A capital-gains entry (row 10).
  - The B disabled pension-exclusion entry (row 4).
  - `public_pension_other_state` on the disability-pension entry (row 11).
- **Dropped:**
  - B's `social_security` in the railroad entry (row 9): redundant with `social_security.treatment`.
  - B's `cannot_combine_with` on the pension-exclusion pair (row 4).
- **Both readers had these, kept:** the seven exemptions (lines 6–12) and the military, railroad and disability-pension exemptions.

## Facts most often missed: second-document checks

- **Social Security: exempt.**
  - Instr p.10 lists "Federal Social Security" among the exempt income examples.
  - Instr p.15 lists "Social Security benefits" under "nontaxable retirement income (do not report on this return)".
  - njit6 says "Social Security and Railroad Retirement benefits" are not taxable.
  - The form has no Social Security line.
- **Retirement reliefs.** The caps, the age test (62 on the last day of the year), the disability alternative, the bands and the covered income were checked in three places that agree: Instr p.22, GIT pp.18-21 and njit7. The other two exclusions were checked in Worksheet D (p.23), GIT pp.22-28 and njit7.
- **Exemptions.** Instr pp.8-9 lines 6-12, checked against form lines 6-13. Amounts: 1,000 regular per filer; 1,000 senior (65+, "born in 1960 or earlier"); 1,000 blind or disabled; 6,000 veteran; 1,500 per dependent; 1,000 per college dependent. There is no standard deduction.
- **Base.** Line 27 is "Add lines 15, 16a, 17 through 20a, and 21 through 26" on the form, and "Add lines 15 through 26 (do not include lines 16b and 20b)" in Instr p.21. It is New Jersey's own income measure, so `starts_from` is state_own.

## Projection choices (`NJ.projection.json`)

- **Base.** `federal_agi`, with an approximation listing the differences. Deductions: the regular exemption (per person) and the senior exemption (per person, min_age 65).
- **Pension exclusion.** Modelled from the age-62 entry:
  - `covers` lists the seven pension kinds, including `public_pension_other_state` and `roth_conversion`.
  - `needs_input` is `pension_source`, because military pensions are exempt separately.
  - The income test is stepped on federal AGI, less taxable Social Security, plus tax-exempt interest.
  - The disabled entry is in `not_modelled`, warned for ages 18–61.
- **Unclaimed exclusion.** Modelled:
  - `covers` is interest, dividends, capital gains, rents and royalties, and other income. Wages and self-employment are left out so that a working person isn't given an exclusion on wages.
  - `cap_reduced_by` is the pension kinds, which makes the maximum minus line 28a exact up to $100,000.
  - The band shares are reused as an approximation.
  - The $3,000 earned-income test can't be expressed, so it is logged as understating tax.
- **Exempt in full:** military pensions and railroad retirement.
- **Not modelled:**
  - the disability-route exclusion;
  - disability pensions before 65;
  - the special exclusion (Social Security eligibility isn't a projection fact);
  - the blind/disabled and veteran exemptions;
  - the dependent exemptions;
  - gains on exempt obligations.
- **Approximations, each with its direction and a worked size:**
  - the base;
  - New Jersey basis in contributions;
  - the upper-band share applied to the capped amount;
  - the earned-income test;
  - the unclaimed exclusion's covered income and upper bands;
  - the line 27 mapping;
  - municipal and Treasury interest;
  - Tax Table rounding;
  - a joint return where one spouse qualifies only by disability.
- **Indexing.** `false`, `assumed`, for brackets, deductions and both exclusions.

## Unsure

- **Row 1 (other states' pensions).** This rests on general wording ("all state ... pensions"; the exclusion takes "income reported on line 20a"), not on a sentence naming other states. Nothing printed points the other way. The statute was not read.
- **Row 3 (Roth conversions).** This rests on the line 20a link. Nothing says a conversion is excluded from the exclusion, and GIT says conversions go on line 20a.
- **Special exclusion `who.basis`.** I recorded `return`. The age test is "you and/or your spouse", which is the same as `older_spouse` in effect. Both readers chose `return`.
- **Projection measure.** Line 27 can differ from federal AGI by Treasury interest, New Jersey bonds, plan contributions and category losses. Near the 100,000, 125,000 and 150,000 band edges that changes the exclusion by thousands.

## Validator

```
data/states/2025/NJ.record.json: ok
data/states/2025/NJ.projection.json: ok
```

## 2026-11-07: format v1 adoption

- **Record.** `nj_unclaimed_pension_exclusion` gets `earned_income_limit` `{amount: {all: 3000}, per: return}`. Instr PDF p.23, Worksheet D lines 4-8: add NJ-1040 lines 15, 18, 21 and 22 (wages, net profits from business, partnership share, S corporation share), then "Is the amount on line 8 MORE than $3,000? Yes. You are not eligible to use the unclaimed portion". GIT-1 & 2 p.23 condition 3 says "combined if filing jointly", and p.25 works a joint example the same way. The cite's section now names these, and a `notes` line records the adoption. The test was already in `who.other_conditions` and `not_covered`, so nothing else in the record changed.
- **Projection.** `nj_unclaimed_exclusion` gets the same `earned_income_limit` and `requires: ["earned_income_limit"]`. A reader built at the tag skips the relief and warns, rather than give it to a worker. `record.sha256` is updated.
- **Approximation removed:** "Unclaimed exclusion (line 28b) ... the projection does not apply that test" (understated tax). For a person 62 or older who still works, the projection used to exclude their interest, dividends, gains, rents and other income up to the unused maximum. Its own example: joint, both 63, wages 80,000 and interest 15,000. The projection used to exclude 15,000, about 790 less tax than the booklet. It now excludes nothing, as the booklet does.
- **Approximation added** (understates tax): partnership and S corporation income (lines 21, 22) are not projection inputs, so the projection's earned income is wages plus self-employment only. The booklet also counts a business loss as nothing (Instr PDF p.13 line 18, PDF p.18 lines 21 and 22), while a reader that nets a self-employment loss against wages would get a lower total. Example: single, 64, pension 20,000, partnership income 10,000, interest 15,000. The booklet gives tax 350.00. The projection excludes the 15,000 interest and gives tax 126.00, which is 224.00 less.
- **Dollar effect in the checks.** No existing case changes: no settled case has a person 62 or older with wages and income the exclusion covers that is under 150,000. Three cases were added:
  - `nj_2025_unclaimed_earned_at_limit`: wages exactly 3,000.00, exclusion 55,000.00, tax 238.00.
  - `nj_2025_unclaimed_earned_over_limit`: wages 3,000.01, exclusion 0.00, tax 2,485.50. One cent costs 2,247.50.
  - `nj_2025_unclaimed_joint_earned_combined`: 2,000 + 2,000 of wages, exclusion 0.00, tax 315.00. A per-person test would give 28.00.

```
data/states/2025/NJ.record.json: ok
data/states/2025/NJ.projection.json: ok
```

## 2026-11-08: marker ids and indexing covers

- Marker ids: all 7 markers have an `id`. Each takes its first from_record id, so warning codes are unchanged.
- Indexing covers: `brackets`, `deductions`; `nj_pension_exclusion` and `nj_unclaimed_exclusion` cover their own reliefs (cap, income test, and the unclaimed exclusion's earned income limit). No split needed.
- Assumed entries: searched the archived sources (docling, pypdf and page text) for indexed, inflation, cost of living, adjusted annually and consumer price index, and for statements that figures are fixed; nothing says, so every `assumed: true` stays.
