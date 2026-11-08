# Settlement: Indiana, tax year 2025

- Readings: `work/extract/2025/IN.r6.A.json`, `work/extract/2025/IN.r6.B.json` (round r6)
- Sources: `sources/archive/2025/IN/` (2025 IT-40 booklet; Form IT-40; Schedules 1 and 2; Department web page `deductions.page.txt`)
- Outputs: `data/states/2025/IN.record.json`, `data/states/2025/IN.projection.json`
- Settled: 2026-11-07

## Comparison

`uv run python -m tools.compare` reported **53 structured differences** (133 wording differences). Taken
together they are five disagreements. No figure conflicted: the two readers printed the same amounts and
differed in how they wrote them down. All 53 lines were decided by reading the booklet page.

| # | Lines | Field | A | B | Booklet | Settled |
|---|---|---|---|---|---|---|
| 1 | 20 | Additional 500 exemption, `what` (keyed as two entries, so all 10 fields show twice) | `other` | `age_65_exemption` | PDF page 25, Line 5: "An additional $500 exemption is available for you and/or your spouse (if filing a joint return) if you are age 65 or older and the amount on Form IT-40, line 1, is less than $40,000 (or if you are married filing separately and the amount on Form IT-40, line 1 is less than $20,000)." | `age_65_exemption` (B). Figures were the same in both. `applies_when: at_or_over`, from "less than". |
| 2 | 3 | First-year child exemption of 3,000 | inside the 1,500 entry's condition | own entry | PDF page 26: "an amount of $3,000 instead of $1,500 for one tax year" | own entry (B): the brief wants every amount printed, one entry per branch |
| 3 | 15 | Renter's, homeowner's and private school deductions | notes only | entries | PDF page 16 (rent: "up to $3,000 ($1,500 if married filing separately)"), PDF pages 16-17 (property tax: "up to $2,500 ($1,250 if married filing separately)"), PDF page 18 (private school: "$1,000; multiplied by" the qualified children); Schedule 2 lines 1, 2, 8 | entries (B); Massachusetts' rental deduction is held the same way |
| 4 | 9 | Social Security and railroad | one entry | two entries | PDF page 17 prints one rule under one heading, "Lines 5 and 6 - Taxable Social Security and/or Railroad Retirement Benefits Deduction", with the same terms for both | one entry (A); the rule does not differ between them, so it is not two branches |
| 5 | 6 | U.S. government interest, `who.basis` | `return` | `each_person` | PDF page 17, Line 4: no test on either spouse | `return` (A); schema: `return` when neither spouse is tested |

20 + 3 + 15 + 9 + 6 = 53. Decided from the booklet: 53 of 53.

## The five facts always settled

1. **A government pension paid by another state, and a New York State pension: not found.** Neither
   `public_pension_other_state` in `covers` nor `not_covered`: the booklet says nothing about them.
   The nearest words:
   - PDF page 17, Lines 5 and 6: "Do not enter any other types of pension or retirement income on these lines."
   - PDF page 37, Schedule 6 Line 5: "If you received income from another state while you were an Indiana resident, you must report that income on your Indiana income tax return."
   - PDF page 38, Group B: the reciprocal agreement "only applies to income from wages, salaries, tips and commissions". New York is in Group A, no agreement (PDF page 37).
   - The list of Line 11 deductions, PDF pages 19-24, has no such code.

   Effect: a New York State pension in federal AGI stays in Indiana income and pays 3%. That is read from
   how the lines work; no sentence says it. `tools.report_pensions` gives "taxed (no general relief)".

2. **Own and federal government pensions.**
   - Federal: PDF page 19: "The income on line 1 of Form IT-40 may include federal civil service annuity income. If it does, you may be eligible to take a deduction if you were at least 62 years of age by the end of the tax year and/or a surviving spouse of a civil service annuitant." Limit: "The lesser of the amount of taxable civil service annuity income included in federal adjusted gross income or $16,000, Less all amounts of Social Security income and tier 1 and tier 2 Railroad Retirement income". Second document: the web page gives the same 62 and 16,000.
   - Military: PDF page 22: "For 2022 and later, the deduction is equal to the entire amount of military retirement income and/or survivor's benefits." Second document: the web page, same sentence.
   - Indiana state and local pensions: not found in the booklet. No deduction names them; "PERF" hits are parts of "perform". They are in federal AGI and no line takes them out.

3. **Private pensions, IRA and employer-plan distributions, Roth conversions: not found.** No deduction or
   exclusion. PDF page 17 again: "Do not enter any other types of pension or retirement income on these
   lines." Search ignored the PDF's broken letter spacing: "Roth" appears only inside other words
   ("brother"), "IRA" only in a historic code list (PDF page 49, "IRA charitable distribution - 122** (2010
   through 2012)"), and 401(k), 403(b) and 457 never as plans. No sentence says these are taxed.

4. **Social Security: exempt.** PDF page 17: "Indiana does not tax Social Security income or the railroad
   retirement benefits that are issued by the U.S. Railroad Retirement Board." Schedule 2 line 5, "Taxable
   Social Security benefits", is the subtraction line. PDF page 23 repeats "Indiana does not tax Social
   Security income". The web page agrees.

5. **Brackets, standard deduction, exemptions.**
   - Flat 3% for every status. Form IT-40 line 8: "State adjusted gross income tax: multiply line 7 by 3% (.03)". Second line: Group A Worksheet line B, PDF page 37, "by 3% (.03)", and the examples on PDF page 38. No status has its own schedule, so only `single` and `married_joint` are given.
   - Standard deduction: none printed. "Standard deduction" occurs only in a net operating loss context (PDF pages 19 and 50).
   - Exemptions: 1,000 per filer (PDF page 24: "If you are married filing jointly, enter $2,000 on this line. All other filers* should enter $1,000", agreed by the footnote on PDF page 6); 1,000 per dependent (PDF page 6; the Schedule 3 line 2 text prints the count only); 1,500 or 3,000 additional child (PDF page 26); 1,000 age 65; 1,000 blind (PDF page 25); 500 additional age 65 under 40,000 or 20,000 (PDF page 25). PDF page 53 shows a joint return taking 2,000.

## The conflict named in the dispatch

The Department web page `deductions.page.txt`, marked "Updated for 2023", says of the Military Service
Deduction: "if you are retired from the military or are the surviving spouse of a person who was in the
military, you may be able to take this deduction if: You were at least 60 years of age by the end of the
year". The 2025 booklet has a separate retirement deduction with no age test (PDF page 22). **The 2025
booklet governs.** No age test is recorded on `military_retirement_632`.

Found while checking, same page, same ruling: the web page's civil service limit reads "tier 1 Railroad
Retirement income" and cites Form 1040 line 20a; the booklet says "tier 1 and tier 2" (PDF pages 19-20).

## Decisions not in the structured count

- **`best_of_group` on the civil service entries** (A: `civil_service_annuity`; B: none; reported as a
  wording difference): dropped. PDF page 19: "If you receive a civil service annuity both for yourself and
  as a surviving spouse, the combined deduction cannot exceed $16,000." That is a shared limit, not a
  choice, and a best-of group could drop one spouse's deduction on a joint return.
- **`paying_states: ["federal"]` on both civil service entries**: added by the settler. Without it
  `public_pension` would also reach Indiana state and local pensions, which the booklet does not relieve.
- **Municipal interest** (both readers `other`): kept as `other`, because other states' obligations held
  or acquired before Jan. 1, 2012 are not taxed, so `other_states_taxed_own_exempt` would not be faithful.
  Added the Indiana-only Tax-exempt Bonds Deduction, code 636 (PDF page 21), which neither reader had, to
  the note. The projection, which has no `other`, uses `other_states_taxed_own_exempt` with an approximation.
- **Disability retirement cite**: A said PDF page 21, B said PDF page 20; it is printed on PDF page 20.
- **Rate note**: A wrote that the booklet does not restate the rate; it does (PDF pages 37 and 38). B's note kept, page corrected.
- **Military Service Deduction, no cap**: PDF page 18 says "the full amount of military pay"; PDF page 22
  still says "Unlike the Military Service Deduction on line 7, this deduction does not have a dollar limit".
  No limit is printed anywhere, so none is recorded; note added.
- **`qualifying_surviving_spouse`** added to the 40,000, 3,000 and 2,500 figures: the booklet's only split
  is married filing separately against everyone else.

## One-sided entries

- `cannot_combine_with` on `military_service_deduction` (B only): kept. PDF page 22: "You cannot claim both this deduction and the Military Service Deduction (see page 17) based on the same income."
- `not_covered` on the military service, National Guard and U.S. interest entries (B's fuller lists): kept, printed on PDF pages 18, 22 and 17.
- `not_covered` on the Social Security entry (A only): kept, with B's condition on the Railroad Retirement Board.
- `condition` on the dependent exemption (B only): kept.
- Lake County bar on the homeowner's deduction (neither reader): added, PDF page 16.
- Indexing cite (B only): dropped; the entry says `not_stated`, and a cite adds nothing. The answers match.
- Unified Tax Credit for the Elderly (A, notes; "the schema cannot hold"): stays in notes for a different reason. `docs/design.md` puts credits other than retirement relief out of scope, as Arkansas and Georgia settled; a stepped relief could hold it, but it is a low-income credit. The projection carries it as an approximation.
- Adopted-child additional exemption (both, notes): the amount is in no source; stays a note.
- County income taxes: local, out of scope; note only.

## Projection

- Modelled: flat 3%; personal exemption; age 65 exemption; additional age 65 exemption with its income test on federal AGI; Social Security exempt; railroad exempt; civil service annuity (age 62, federal only, 16,000 per person); military retirement in full.
- `not_modelled`: civil service survivor branch, disability retirement, dependents and private school, blindness, renter's and homeowner's deductions, military pay, U.S. government interest.
- Indexing: `not_stated` everywhere, so `indexed: false, assumed: true` for brackets, deductions and relief caps.

## Unsure

1. **Civil service limit order.** The booklet takes Social Security from the lesser of annuity or 16,000; `cap_reduced_by` takes it from the 16,000 first. The projection therefore overstates the deduction when the annuity is below 16,000: the booklet's own example (annuity 6,000, Social Security 1,200) gives 4,800, the projection 6,000. Logged as an approximation (`understates_tax`, at most 240 a year). A check case built from that example will fail until the projection format can express the order.
2. **`paying_states` on `public_pension`.** The schema describes the field for `public_pension_other_state`, but its pattern allows `federal` and `tools/report_pensions.py` honours it. No other settled record uses it this way; a consumer must read it on `public_pension` entries too.
3. **`cap_reduced_by` measure.** The booklet reduces by all Social Security received, not the taxable part. The schema does not say which a consumer uses.
4. **Other-state and private pension treatment is inferred from silence.** The booklet has no sentence saying they are taxed; the "taxed" result comes from federal AGI being the start and no line removing them. Indiana bulletins #6 and #70, named by the booklet, are not in the sources.
5. **Disability cap.** 5,200 is printed only on PDF page 20; the web page gives the tests but no amount, so there is no second document for it.
6. **Schedule 3 and the adopted-child amount.** Schedule 3 is not among the sources, so the exemption amounts come from its line instructions.

## 2026-11-07: format v1 adoption

- **Civil service annuity order (Unsure item 1, now settled).** Projection relief `civil_service_annuity` gets `cap_reduction: from_lesser_of_income_and_cap`: Social Security and railroad retirement come off the lesser of the annuity and 16,000, as PDF page 19 prints it. The approximation "cap_reduced_by takes that income from the 16,000 before comparing with the annuity" is deleted; the deduction is now exact for the age-62 branch.
- **Dollar effect.** Only an annuitant with an annuity under 16,000 who also receives Social Security or railroad retirement is affected; the deduction falls by the smaller of that income and 16,000 less the annuity, and tax rises by 3% of that. The booklet's example (annuity 6,000, Social Security 1,200): deduction 6,000 before, 4,800 now, 36 more tax a year. Largest change, annuity and Social Security both 8,000: 8,000 before, 0 now, 240 a year. No change when the annuity is 16,000 or more.
- **Gross or taxable Social Security (Unsure item 3, now settled).** Gross: PDF page 19 says "Less all amounts of Social Security income and tier 1 and tier 2 Railroad Retirement income ... received by the civil service annuitant", and every booklet example (PDF pages 19-20: 1,200; 17,500 and 6,300; Marie 1,200) subtracts the Social Security received, with no taxable-part step. Stated in the record's `civil_service_annuity_age_62.cap_rule` (and the surviving-spouse entry), with the quote in the cite, and a notes line. Corroboration only: the Department web page (deductions.page.txt, "Updated for 2023", not used as a source) says "received by the qualifying individual (as reported on Form 1040, line 20a, or Form 1040A, line 14a)". The projection schema does not say which amount `cap_reduced_by: social_security` reads; a consumer must use the gross amount received by that person (the checks' `social_security_gross`).
- `record.sha256` updated. Both files validate.
- Checks: `in_2025_civil_service_booklet_gap_example` renamed `in_2025_civil_service_booklet_example` (expected now the booklet's 4,800); `in_2025_civil_service_ss_uses_cap` renamed `in_2025_civil_service_ss_equals_annuity` (deduction 0, was 6,000); `in_2025_civil_service_booklet_matthew_claire` reworked (same figures, approximation removed, worked in the booklet's order); added `in_2025_civil_service_railroad_below_cap` (below: annuity 9,000, railroad 3,000, deduction 6,000) and `in_2025_civil_service_ss_annuity_at_cap` (at_or_above: annuity 16,000, Social Security 5,000 gross, 2,500 taxable, deduction 11,000). The `verified` blocks of the reworked and renamed cases are removed.

- Main session, 2026-11-07 (format v1): `social_security_basis: gross` set on the relief(s) whose cap Social Security reduces, stating what the cases already used.

## 2026-11-08: marker ids and indexing covers

- Marker ids given: first from_record id (warning code unchanged): `civil_service_annuity_surviving_spouse`, `disability_retirement_602`, `dependent_exemption`, `blind_exemption`, `renters_deduction`, `military_service_deduction`, `us_government_interest_deduction`.
- Indexing covers: `brackets` -> `brackets`; `deductions` -> `deductions`; `relief_caps` -> `reliefs.cap`.
- Every `assumed` answer was checked again against the archived sources (searched for indexed, inflation, cost-of-living, adjusted annually, each year, CPI, fixed): none says, so all stay `assumed: true`.
- Warning codes unchanged (every id is the marker's first from_record id).

## 2026-11-08: indexing settled from statutes

- `brackets` (projection `brackets`): not_indexed, IC 6-3-2-1: one flat rate from 0 (the section text itself was not read; medium confidence). Record `brackets` added as no.
- `deductions` (projection `deductions`): not_indexed, IC 6-3-1-3.5(a)(3), (a)(4), (a)(5)(C) (enrolled SEA 243 of 2026). Record `personal_exemption`, `age_65_exemption`, `age_65_additional_exemption` added as no.
- `relief_caps` (projection `reliefs.cap`): not_indexed, IC 6-3-2-3.7 as stated in DOR Information Bulletin #6 (statute text not read; medium confidence). Record `civil_service_annuity_age_62` and `civil_service_annuity_surviving_spouse` (same 16,000) added as no.
