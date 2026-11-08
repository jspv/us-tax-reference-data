# Settlement: Oklahoma, tax year 2025

- Readings: `work/extract/2025/OK.r6.A.json`, `work/extract/2025/OK.r6.B.json` (round r6)
- Sources: `sources/archive/2025/OK/`: the Form 511 packet `511-Pkt` (instructions, tax table, forms) and the Help Center page `income-tax`
- Outputs: `data/states/2025/OK.record.json`, `data/states/2025/OK.projection.json`
- Settled: 2026-11-07

## Comparison

`uv run python -m tools.compare` reported **39 structured differences** (86 wording differences). Taken
together they are five disagreements. The readers agreed on every bracket, on every other deduction and exemption,
and on every relief's cap and `covers` list.

| # | Lines | Field | A | B | Source | Settled |
|---|---|---|---|---|---|---|
| 1 | 1 | `brackets.derivation.method` | `tax_table_and_formula` | `tax_table` | PDF page 27: "If your taxable income is $100,000 or more, use the tax computation on the lower portion of page 38." Page 38 prints the worksheets | `tax_table_and_formula`, as A. No `formula` object: see the derivation below |
| 2 | 30 | `brackets.derivation.table_rows` (14 rows each, compared by position) | rows from 3,025 to 99,975 | rows from 525 to 100,000 | All 28 rows checked against the parsed table: every one is printed. Neither set reaches every band of both columns: A has nothing in single 0-2,500 or 3,750-4,900; B has nothing in single 3,750-4,900 or joint 7,500-14,400 | Replaced by 26 rows, each band edge from both sides, all four status lists |
| 3 | 3 | `base.deductions` `itemized_cap` | left out (in notes) | a deduction `other`, 17,000 per return | PDF page 10: "Oklahoma itemized deductions are limited to, and may not exceed, $17,000." | Left out of `base.deductions`, as A: a limit, not a deduction. An `amount` of 17,000 there reads as a deduction a projection would apply. Kept in `notes` and in the standard deduction's `condition` |
| 4 | 3 | `capital_gains` `exempt_obligation_gains` | recorded | left out | PDF page 16: "The capital gain/loss from the sale of an U.S. Government obligation is exempt." PDF page 20 item 1: "The profit from the sale of such bond, note, or other obligation shall be free from taxation." Schedule 511-A line 11 | Kept, as A: printed and in scope (gains treated differently from ordinary income) |
| 5 | 2 | `indexing` | `all_other` only | adds `brackets` and `standard_deduction` as `not_stated` | The booklet says nothing: "inflation", "indexed", "adjusted annually" and "cost of living" find nothing in the packet or the Help Center page | A's single entry. Extraction brief rule 8 asks for an entry per figure only where the booklet says something, plus `all_other` |

Decided from the booklet: disagreements 1-4 (37 lines). Disagreement 5 (2 lines) is the booklet's silence
plus brief rule 8. Total settled: all 39.

## One-sided entries and wording

| Entry | Reader | Kept? | Why |
|---|---|---|---|
| Rows at 100,000 | B | Kept | Page 38 worksheet line 5 prints "Tax on $100,000" as 4,562 and 4,373; they are how the validator reaches the worksheets |
| `not_covered` CSRS on line 5 | A (B in `cap_rule`) | Kept in `not_covered` | Page 17: "Do not include on this line the CSRS retirement benefits already excluded on Schedule 511-A, line 3." |
| "retirement income in the person's own name (as for line 5)" on line 6 | B; also A's note | Dropped from line 6 | Line 6 prints no such sentence. Only line 5 says "(To be eligible, you must have retirement income in your name.)". Line 6 says "Each individual" |
| A's note that lines 5 and 6 are both closed to code 1 early distributions | A | Corrected | Page 17: only line 5; "This distribution may qualify for the 'Other Retirement Income' exclusion on Schedule 511-A, line 6." |
| B's label and cite "Schedule 511-B" on the military pay exclusion | B | Corrected to Schedule 511-C | Page 22 heading SCHEDULE 511-C; form page 46 Schedule 511-C line 1 |
| A's `base.cite` page 43 for lines 1-13 | A | Corrected to pages 42 and 43 | Lines 1-9 are on page 42, lines 10-13 on page 43 |
| A's note that credits have "no schema field" | A | Reworded | The schema has `form: credit`. Credits are listed in `notes` and in `not_modelled`, as neither reader made entries and none turns on the kind of retirement income |
| `form` on uncapped lines | Both `subtraction` | `exempt_in_full` | The comparison treats them as the same; the record says it outright (Kansas and Mississippi do) |

**Added, neither reader:** the resident income sentences from pages 3 and 9, which are the direct evidence that
a pension stays in Oklahoma income unless a Schedule 511-A line takes it out. Both readers searched for
pension wording only.

## The required facts

1. **Another state's government pension, New York State included: not named anywhere; line 5 no, line 6 a
   question of plan type.** "New York" appears in neither the packet nor the Help Center page (grep: 0 hits in
   the pypdf, Docling and page texts).
   - Line 5 is a closed list by payer. Page 17: "The retirement benefits must be received from the following"
     and then the U.S. civil service and named Oklahoma systems. A New York State pension is not on it. The
     booklet has no sentence saying so in words, so it is not in `not_covered`.
   - Line 6 is a list by plan type, with no limit on who pays. Page 17: "The retirement benefits must be
     received from the following and satisfy the requirements of the IRC: An employee pension benefit plan
     under IRC Sec. 401; An eligible deferred compensation plan under IRC Sec. 457; An individual retirement
     account, annuity or trust or simplified employee pension under IRC Sec. 408; An employee annuity under
     IRC Sec. 403 (a) or (b), United States Retirement Bonds under IRC Sec. 86; or Lump-sum distributions from a
     retirement plan under IRC Sec. 402 (e)." So whether a New York pension reaches line 6 depends on whether
     its plan is one of those types, and the booklet does not say what type any other state's plan is.
     `public_pension_other_state` stays in `covers_unclear` on line 6, as both readers had it. I did not settle
     the plan type from outside knowledge (brief rule).
   - If it is not a listed type, it is taxed, and that is a sentence, not silence. Page 3: "An Oklahoma resident
     individual is taxed on all income reported on the federal return, except income from real and tangible
     personal property located in another state, income from business activities in another state, or the
     gains/losses from the sales or exchange of real property in another state." Page 9 on line 4 out-of-state
     income: "It is not non-business interest or dividends, installment sale interest, salary/wages, pensions,
     unemployment compensation, gambling, or income from personal services."
   - Rule for the resident: taxed by Oklahoma, less up to 10,000 a person on line 6 if the plan is a listed IRC
     type. The projection follows the brief's rule for `covers_unclear` and leaves it out of `covers`, taxing it
     in full, with an approximation of at most 475 a person a year.
2. **Own and federal government pensions.** Line 5, page 17: "Each individual may exclude their retirement
   benefits up to $10,000, but not to exceed the amount included in the Federal AGI." The list opens "The Civil
   Service of the United States*". CSRS paid in lieu of Social Security, line 3: "Each individual may exclude
   100% of their retirement benefits received from the Federal Civil Service Retirement System (CSRS), including
   survivor benefits, paid in lieu of Social Security to the extent such benefits are included in the Federal
   AGI." FERS does not qualify for line 3 except a CSRS component and the Annuity Supplement. Military, line 4:
   "Each individual may exclude 100% of retirement benefits from any component of the Armed Forces of the United
   States." Second document: the Help Center answers repeat all three.
3. **Private pensions, IRA and employer-plan distributions, Roth conversions.** Line 6, page 17: "Each individual
   may exclude their retirement benefits up to $10,000, but not to exceed the amount included in the Federal
   AGI." The **shared cap**: "For any individual who claims the exclusions for government retirees on Schedule
   511-A, line 5, the amount of the exclusion on this line cannot exceed $10,000 minus the amounts already claimed
   on Schedule 511-A, line 5 (if less than zero, enter '0'). If the maximum $10,000 is claimed on Schedule 511-A,
   line 5, no additional amount is allowed on Schedule 511-A, line 6." The Help Center repeats the rule. One
   10,000 a person across both lines; no age test on either. Roth conversions, page 20: "Rollovers and IRA
   Conversions are taxed in the same year as on the federal return." That says when, not whether a conversion
   counts as retirement benefits on line 6, so `roth_conversion` stays in `covers_unclear`.
4. **Social Security: exempt.** Page 16: "Social Security benefits that are included in the Federal AGI shall be
   subtracted." Page 45, Schedule 511-A line 2: "Social Security benefits taxed on your Federal Form 1040 or
   1040-SR". Help Center: "Social Security benefits that are included in the federal adjusted gross income shall
   be subtracted on your Oklahoma income tax return." Railroad, page 18: "All qualified U.S. Railroad Retirement
   Board benefits that are included in the Federal AGI may be excluded."
5. **Brackets, standard deduction, exemptions.** See the derivation below. Page 10: "single" or "married filing
   separate" 6,350; "head of household" 9,350; "married filing joint" or "qualifying surviving spouse" 12,700;
   the form's line 10 (page 43) and Schedule 511-E (page 25) print the same amounts. "Oklahoma allows $1,000 for
   each exemption claimed on the top of the return"; form line 11 prints "X $1,000". Page 9, age 65: "An
   additional exemption may be claimed for each taxpayer or spouse who meets the qualifications based on filing
   status and Federal AGI limits* below and who is 65 years of age or older at the close of the tax year", with
   15,000, 25,000, 12,500 and 19,000. **The Roth note**: "If your Federal AGI includes income from the conversion
   of a traditional individual retirement account to a Roth individual retirement account, this income shall be
   excluded in determining the Federal AGI limits." The wording is "equal to $15,000 or less", so `removes` with
   the default `applies_when: over` is exact at the limit.

## Bracket derivation

The booklet prints no bracket schedule. Page 27: "Use this table if your taxable income is less than $100,000."
Page 38: worksheets "$4,562 plus 0.0475 over $100,000" (single or married filing separate) and "$4,373 plus
0.0475 over $100,000" (married filing joint, head of household or qualified widow(er)).

Checked by script over every printed row (2,000 rows of 50 dollars, 0 to 100,000, no gaps; pypdf text):

| Check | First column (single, separate) | Second column (joint, head of household) |
|---|---|---|
| Largest gap, schedule at midpoint against printed tax | 0.44 | 0.44 |
| Rows over 1 dollar off | 0 | 0 |
| Rows over 0.50 off | 0 | 0 |
| At 100,000 | 4,561.50 against 4,562 | 4,373.00 against 4,373 |
| At 200,000, against the worksheet | 9,311.50 against 9,312 | 9,123.00 against 9,123 |
| Range for each start alone at 0.50 tolerance | 1,000: 988-1,012; others plus or minus 6 | 2,000: 1,988-2,012; others plus or minus 6 |
| Any rate moved by 0.05 point or 0.10 point | fails | fails |

Every printed row is the schedule's result at the midpoint, rounded to the dollar, so the rates are fixed and the
starts are the round figures inside narrow ranges. Second-column starts are exactly double the first's.

**Why no `formula` object.** The field holds one "rate x income minus constant" and the validator tests it against
both single and joint. Oklahoma's two columns have different constants, and the constants as `minus` figures (188
and 377) are not printed. Kansas set the same precedent. Instead the worksheets' printed "Tax on $100,000" are
`table_rows` at income 100000 for all four status lists, so the validator re-checks them. It re-checks 26 rows; the
slope above 100,000 is not exercised by it, and rests on the top rate being the worksheets' printed 0.0475 and on the
200,000 line above.

**Column mapping.** Column heads "Single or married filing separate" and "Married* filing joint or head of household";
footnote "This column must also be used by a Qualified Surviving Spouse." `head_of_household` must be explicit:
the projection schema defaults a missing head of household to single, which would be the wrong column here.

**Conversion note.** Docling prints the 85,400-85,450 row's joint tax as 3,683; pypdf prints 3,681 and the schedule
gives 3,680.69. pypdf is right. My parse of Docling's tables found only 494 of the 2,000 rows, so the check uses pypdf.

## Projection decisions

- **Shared cap:** two reliefs, one per record line, with `cap_reduced_by: ["public_pension"]` on line 6 (Michigan's
  form). A person with an 8,000 Oklahoma pension and a 5,000 IRA distribution: line 5 takes 8,000, line 6's cap is
  2,000, total 10,000, as the booklet does it. Each line keeps its own check cases.
- **`needs_input: ["pension_source"]`** on military, line 5 and line 6.
- **CSRS on line 3:** `not_modelled` (`has_pension`). The guide puts Social Security-exempt employment there, and
  public pension source alone cannot separate CSRS from FERS.
- **Age 65 test:** measure `federal_agi`, as the projection schema has no way to subtract conversions. Approximation
  of 47.50 a person in a conversion year.
- **Social Security** is `treatment: exempt` with no relief entry, as Kansas and Mississippi do.
- **Treasury interest, capital gain deduction, exempt obligation gains, military pay, blind and dependent exemptions:**
  `not_modelled`, with approximations.
- **Itemized deductions:** the standard amount and an approximation of direction `either`, because Oklahoma itemizing
  is not a choice: a federal itemizer must use it even if it is smaller.
- **Indexing:** `brackets`, `deductions`, `relief_caps` false, assumed.

## Unsure

- **New York plan type.** The honest answer from these sources stops at "depends on the plan type". If the statute or
  a Commission ruling settles other-state government plans, line 6's `covers_unclear` can become `covers` and the 475
  approximation goes away. The projection's taxed-in-full treatment is the guide's rule for `covers_unclear`, written
  for Roth conversions and applied here by analogy; the words of line 6 lean toward a listed-type plan qualifying.
- **Age 65 exemption for a qualifying surviving spouse.** The four listed returns leave that status out, and the
  booklet does not say whether it is barred or simply unlisted. The threshold has no entry for it. A consumer that
  falls back to joint uses 25,000; 47.50 a year at most either way.
- **Roth conversions on line 6.** A conversion is paid out of an IRC 408 account, which is on the list, but the booklet
  never says a conversion is "retirement benefits".
- **Capital gain deduction `value: 1`.** No percentage is printed; "You can deduct qualifying gains" is read as all
  of them, as both readers did.
- **Credits** are in `notes` and `not_modelled` only. Sales Tax Relief reaches gross household income of 50,000 at 65
  or older, so an Oklahoma retiree might qualify; the figure itself is on Form 538-S and was not recorded.

## 2026-11-08: marker ids and indexing covers

- Marker ids: all 9 markers have an `id`. Descriptive ids (no from_record id of their own): `ok_out_of_state_income_proration`, `ok_credits`; the rest take their first from_record id, so their warning codes are unchanged. `tools.checks --fix-warnings` rewrote the cases' accepted_warnings (the old shared code state_rule_not_modelled:unnamed becomes the new ids); nothing else in the cases changed.
- Indexing covers: `brackets`, `deductions` (including the age 65 exemption's phase-out), `relief_caps` (reliefs.cap). No split needed.
- Assumed entries: searched the archived sources (docling, pypdf and page text) for indexed, inflation, cost of living, adjusted annually and consumer price index, and for statements that figures are fixed; nothing says, so every `assumed: true` stays.

## 2026-11-08: indexing settled from statutes

Statute research (work/indexing/findings*.json) settled every projection indexing entry that was `assumed: true`:

- `brackets` (brackets): not indexed, 68 O.S. 2355(C)
- `deductions` (deductions): not indexed, 68 O.S. 2358(E)(1)-(2)
- `relief_caps` (reliefs.cap): not indexed, 68 O.S. 2358(A)(8) and the 'other retirement' exemption in the same section (limit 'Ten Thousand Dollars ($10,000.00) for the tax year 2006 and for all subsequent tax years')
- Record `indexing`: added brackets -> no; added standard_deduction -> no; added personal_exemption -> no; added age_65_exemption -> no; added ok_government_retirement -> no; added other_retirement_income -> no.
