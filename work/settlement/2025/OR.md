# Settlement: Oregon, tax year 2025

- Readings: `work/extract/2025/OR.r6.A.json`, `work/extract/2025/OR.r6.B.json` (round r6)
- Sources: `sources/archive/2025/OR/`: Form OR-40, its instructions (Publication OR-40-FY), Publication OR-17, the Schedule OR-ASC instructions, and the Department's Personal Income Tax page (`pit.page.txt`)
- Outputs: `data/states/2025/OR.record.json`, `data/states/2025/OR.projection.json`
- Settled: 2026-11-07

Page numbers are PDF pages, from the `*.pypdf.txt` markers.

## Comparison

`uv run python -m tools.compare` reported **326 structured differences** (200 wording differences). The readers
agreed on every bracket they both wrote, on the standard deduction, the age and blind amounts, the federal
subtraction table, the medical table, and Social Security. The 326 lines are eleven disagreements, and most lines
are one choice of key repeated: the comparison pairs reliefs by key, so a different age field turned 20 rows of an
identical table into 183 lines.

| # | Lines | Field | A | B | Source | Settled |
|---|---|---|---|---|---|---|
| 1 | 60 | Exemption credits, where they live | `reliefs`, form `credit` | `base.deductions`, marked "a CREDIT" in `condition` | Instructions p17: "Exemption credit"; p18 worksheet line 5 "Line 4 multiplied by $256"; form p4 line 25 | Reliefs, as A and as California, Delaware, Iowa. Four entries, one per branch. Basis `each_person` for filer and spouse (OR-17 p99), not A's `return`; dependents their own entry |
| 2 | 3 | Dependent's standard deduction floor | in `condition` | a deduction of 1,350 per person | Instructions p16: "your standard deduction is limited to the larger of..." | In `condition`, as A. It is a limit for someone claimable as a dependent, not a deduction anyone adds |
| 3 | 1 | Federal subtraction `phase_out.applies_when` | `at_or_over` | left out | Instructions p15 Table 4: "At least— / But less than—" | `at_or_over` |
| 4 | 16 | `brackets.head_of_household`, `married_separate` | listed | left out | OR-17 p143 prints "Single / Married filing separately" and "Married filing jointly / Head of household / Qualifying surviving spouse"; instructions p17 and p32 | Listed. Head of household must be: a missing status defaults to single, and Oregon's goes with joint. B's omission would have been a real error for a consumer |
| 5 | 4 | `indexing` | exemption credit, `all_other` | two exemption entries; brackets, standard deduction, federal subtraction `not_stated` | OR-17 p98: "The exemption amount is indexed for inflation." Nothing else | One line (the dependent's entry) from the sentence. The other three are silence: `all_other` carries them (brief rule 8) |
| 6 | 1 | `muni_interest.treatment` | `other` | `other_states_taxed_own_exempt` | OR-17 p63: "Oregon taxes interest and dividends on bonds and notes of another state or political subdivision of another state that you didn't include on your federal return." p85-86: code 317 subtracts bonds of Oregon and its subdivisions | As B. A did not find code 317 |
| 7 | 37 | `retirement_income_credit` | see below | see below | OR-17 p106-107 | See below |
| 8 | 3 | `us_obligations_interest_subtraction` | relief | only in the muni note | OR-17 p77 code 315; p86 "exempt from state tax" | Kept, `exempt_in_full`, as other states |
| 9 | 6 | Federal pension `covers` | public, military | adds `employer_plan_distribution` | OR-17 p73: "withdrawals from federal TSP accounts are eligible for the subtraction based on dates of service" | As B, the limit in `other_conditions`, `paying_states: ["federal"]` as Indiana so the entry cannot be read as covering Oregon's pensions |
| 10 | 12 | Social Security and railroad `form`, `who.basis` | `subtraction`, `return` | `exempt_in_full`, `each_person` | OR-17 p52: "Oregon doesn't tax any amount of your Social Security, Railroad Retirement Board, or railroad unemployment benefits." | As B, as Oklahoma and Ohio |
| 11 | 183 | `special_oregon_medical_subtraction` | `min_age` 66, scope `person`, cap per status | `born_on_or_before` 1959-12-31, scope `return`, cap `all` | Schedule OR-ASC instructions p2: "turned age 66 by the end of the tax year" | `min_age` 66 as A (rules 5, 15: a birth date is right for 2025 only). Scope `return` as B: it comes off the return's income. Cap `all` as B: one figure. The 20 table rows are the same in both |

**Decided from the booklet: 323 of the 326 lines. The other 3 (in #5) are the booklet's silence plus brief rule 8.**

### Disagreement 7, the retirement income credit

| Field | A | B | Source | Settled |
|---|---|---|---|---|
| Age | `min_age` 62 | `born_on_or_before` 1963-12-31 | p106: "age 62 or older at the end of the year" | `min_age` 62 |
| `public_pension_other_state` | `covers_unclear` | `covers` | p106: "State or local government public pensions. Employee pensions." No limit to Oregon. p52: "Plans for federal, state, or local government employees" | `covers`. Even on A's doubt, a pension from another state is an employee pension |
| Cap | in `cap_rule` only | 7,500 / 15,000 per return | p107 worksheet line 4 | As B |
| `income_test` | `removes` at 22,500 / 45,000, `at_or_over` | `other` at the same figures | p107 lines 7-10 | **Neither.** `dollar_for_dollar` over 15,000 / 30,000. See the working below |
| Measure flags | none | `plus_tax_exempt_interest`, `minus_taxable_social_security` on `household_income` | p107 | Left out of the record: `household_income` already means this, and flags on it would read as a second adjustment. Used in the projection, where the base is federal AGI |

The credit is 9% of the smaller of line 3 (pension) and line 10, and line 10 = max(0, 7,500 - benefits) - max(0,
household income - 15,000). Line 10 reaches 0 exactly when household income plus benefits reaches 22,500. So the
printed qualifying tests are not a cliff on top of the worksheet: the third test is the worksheet's own zero, and
the first two are implied by it. A credit that stopped at 22,500 would have overpaid everyone between 15,000 and
22,500. The printed tests stay in `who.other_conditions` and `as_printed`.

**Other filing statuses.** The dispatch noted figures printed only for single and joint. The booklet does not name
single: it prints "$22,500 ($45,000 if married filing jointly)", "$7,500 ($15,000 if married filing jointly)" and
"$15,000 ($30,000 if married filing a joint return)". The first figure is therefore every return that is not joint.
Separate, head of household and qualifying surviving spouse take it. Both readers did the same, B with a doubt.

## One-sided entries and wording

| Entry | Reader | Kept? | Why |
|---|---|---|---|
| `previously_taxed_retirement_contributions`, `previously_taxed_ira_conversion` | Both | Kept | OR-17 p80-81 |
| `not_covered` of the credit | B | Kept, reworded | p52 "Retirement income doesn't include income received from: Stock options. Restructured stock plans. Severance plans."; p107 lines 2 and 5 |
| `not_covered` of the federal pension | A | Kept, TSP lines split | p73 |
| Standard deduction short-period sentence | B | Kept | OR-17 p95 |
| Statewide transit tax note | B | Kept | OR-17 p31: "It's not reported on your Oregon income tax return." |
| Kicker note | A | Kept, with B's point that it is odd years only | Instructions p18; OR-17 p96 |
| B's `other_conditions` on the conversion | B | Kept | p81 example: "Susan lived in New York" |
| A's note that Oregon's own bonds are not stated | A | Replaced | p85-86 state them |
| A's "not found" for a rule on another state's pension | A | Sharpened | The Department's page says it outright; see fact 1 |

**Added, neither reader:** `us_interest_in_ira_distributions`, code 331 (OR-17 p86-87): the part of an IRA or Keogh
distribution that comes from U.S. government interest is subtracted. It is a relief on IRA income, and p77's "you
may not subtract pension income received from funds invested in U.S. government securities" is not the whole
story without it.

## The required facts

1. **Another state's government pension, New York State included: taxed like any other pension, with no exclusion.**
   - "If you change your permanent residence to Oregon, your pension income, along with all other income regardless of
     source, is taxable in Oregon." (Department's page, "If I become an Oregon resident, is my retirement income
     taxable?"; `pit.page.txt`.) Neither reader cited this. It is the most direct sentence in the sources.
   - "Most retirement income is subject to Oregon tax when received by an Oregon resident. This is true even if you
     were a nonresident when you earned the income." (OR-17 p52.)
   - "if you live in Oregon, other states can't tax your pension income" (OR-17 p100), so no credit for tax paid
     to another state on it.
   - "New York" appears only in the IRA conversion example (p81). No paying state and no reciprocity rule is named, so
     `paying_states` is left out.
   - Relief: in `covers` of the retirement income credit (`public_pension_other_state`), and the code 327
     subtraction if the other state taxed the contributions (p81 Example 2 is Kansas's public employee fund).
2. **Own and federal government pensions.** Oregon's: no subtraction found; taxed, and in the credit ("State or local
   government public pensions", p106). Federal: "You may be able to subtract some or all of your taxable federal
   pension included in federal income" (p73), by the share earned before October 1, 1991; "If you have no months
   of service or points earned before October 1, 1991, you can't subtract any federal pension." Military is in it:
   p74 Example 2 is an Army Reserve retiree, and p106 says "Federal pensions (includes military)". The Department's
   page agrees.
3. **Private pensions, IRAs, employer plans, Roth conversions.** Taxed. "Oregon taxes any taxable IRA distribution
   you received during the year and any amounts reported in federal income that you converted from a traditional IRA
   into a Roth IRA." (p49.) The only relief is the credit. Whether a conversion is retirement income for the credit is
   not stated: household income lists "IRA conversions included in AGI" (p107), retirement income lists "Individual
   retirement plans" (p106) and does not mention conversions. `roth_conversion` stays in `covers_unclear`.
4. **Social Security: exempt.** Form OR-40 p3 line 11 subtracts "Social Security amount on federal Form 1040 or
   1040-SR, line 6b"; OR-17 p83: "Oregon doesn't tax Social Security benefits. Any Social Security benefits included in
   your federal AGI are subtracted on your Oregon return."; OR-17 p52; the Department's page.
5. **Schedule, deduction, exemptions.**
   - Schedule, OR-17 p143: single and separate 4.75% first 4,400, 6.75% to 11,100, 8.75% to 125,000, 9.9% over; joint,
     head of household, surviving spouse 8,800, 22,200, 250,000. Second source: Chart S on instructions p32 gives
     4,065 and 10,627 and table rows match (39,000-39,100: 3,107 and 2,797).
   - Chart J prints 3,756 and 21,256 where the bare schedule gives 3,755 and 21,255. The table's pattern shows why:
     rows fit a base of 1,323 at 22,200 (bare 1,322.50) and 661 at 11,100 (bare 661.25), so the Department rounds at the
     bracket edge. Under a dollar, in `approximations`. B's note that the charts "agree" passes over this.
   - Standard deduction: 2,835, 5,670, 2,835 (or 0), 4,560, 5,670. Agrees on instructions p16, form p3, OR-17 p95, p143.
   - Age 65 and blind: 1,200 single or head of household, 1,000 otherwise, per box. Instructions p16, OR-17 p95.
   - Exemptions: no deduction; a 256 credit each. Form p4, instructions p18, OR-17 p98, p143. Gone over 100,000 single
     or separate, 200,000 otherwise; the two additional credits over 100,000 for every status.

## Points the dispatch flagged

- **Federal income tax subtraction.** The record holds it in `base.deductions` with the maximum and the full Table 4
  ladder as `stepped` with `amount` (the schema fits here, where it did not for Missouri, because Table 4 steps a
  dollar maximum and not a percentage of the tax). The real amount is the smaller of that and the federal tax, and
  federal tax is not a yearly fact (guide, test 1). Two representations are possible:

  | | Left out (chosen) | Applied at the maximum |
  |---|---|---|
  | Error | Tax too high by 8.75% x min(tax, max) | Tax too low by 8.75% x (max - min(tax, max)) |
  | Federal tax 0 | None | 743.75 too low |
  | Federal tax 4,250 | 371.88 too high | 371.88 too low |
  | Federal tax 8,500 or more | 743.75 too high | None |
  | AGI 145,000 / 290,000 or more | None | None |
  | Catches the AGI steps | No | Yes |

  Left out it is: it follows the guide's test and Alabama and Missouri, so the three states stay comparable; its
  error is largest for the households paying the most Oregon tax and vanishes for those paying the least, where the
  other choice would misstate a small tax by a large share; and it errs toward too much tax in a planning figure.
  What it costs: above 4,250 of federal tax the other choice is closer, and the AGI steps do not show as a cost of
  extra income. A single filer going from 120,000 to 150,000 on a Roth conversion loses up to 743.75 that the
  projection does not charge. Both are said in `approximations`.

  **Direction `overstates_tax`, at most 743.75 a year (371.88 separate).** 8.75% is the right rate for the maximum:
  a single filer just under 125,000 of AGI has taxable income under 125,000, and a joint filer under 250,000 likewise;
  at 129,999 single, 6,800 at a part-9.9% rate gives about 620. Example: joint, AGI 120,000, federal tax 6,000: 525.
  If a consumer supplies federal tax as a yearly fact, the record already holds what is needed, and Alabama and
  Missouri would be fixed the same way. That needs a schema change, which is not mine to make.
- **Federal pension subtraction.** Personal share, no input for it: `not_modelled`, `warn_when: has_pension`.
  `needs_input` holds only `pension_source` and `pension_contributory`. `overstates_tax`. It is larger than the
  federal tax gap for those it hits (the booklet's own Jared: 26,585 subtracted, 2,326.19 a year) and nothing for
  anyone with no federal service before October 1991.
- **Retirement income credit.** Modelled: 9% of covered income of each person 62 or older, cap 7,500 / 15,000 per
  return reduced by Social Security and railroad benefits (line 5 is both spouses' total, not the taxable part), and
  the income test dollar for dollar over 15,000 / 30,000.
  - Measure: federal AGI plus tax-exempt interest minus taxable Social Security, the nearest to household income.
    `understates_tax`, up to the whole credit, for a household with items the projection does not hold.
  - Order: the relief applies the income test after the cap, while the worksheet takes the smaller of the pension
    and the limit after both reductions. I searched the grid: the gap is 0 to 337.50 a year (675 joint), always the
    same way, worst at pension 3,750, household income 18,750. `overstates_tax`.
  - It is a small credit: at most 675, 1,350 joint, and only under 22,500 / 45,000.
- **Exemption credits.** 256, `each_person`, indexed, in the projection (`credits` true). Dependents and the
  disability credits `not_modelled`.
- **Farm liquidation rate.** Not in the sources: "a reduced tax rate" (OR-17 p28), "Use Publication OR-FCG" (p29);
  OR-FCG is not in the folder. `capital_gains` is empty and `value` is required, so there is no entry. Noted in `notes`
  and in `not_modelled`. Qualified business income rates are printed (p26) but need business income a projection cannot
  sort; not recorded as gains.

## Other projection decisions

- **Itemizing.** The guide asks for one approximation; here it matters. Oregon's standard deduction is small and a
  filer takes the larger, so this is `overstates_tax` only and can exceed the federal tax gap: 816.38 a year on 15,000
  of itemized deductions, joint. Schedule OR-A is not in the sources, so I cannot say what Oregon allows.
- **Medical subtraction.** `not_modelled`, warn at 66 and over. It is not for itemizers only: instructions p3 lines
  1-5 and OR-17 p85 Example 5. At most 315 a year.
- **Kicker.** `not_modelled`, `warn_when: always`, `from_record: []`. 9.863% of the prior year's tax for 2025 can be
  bigger than anything here in a year it pays, and no long-range run can know it.
- **Indexing.** Brackets, deductions and relief caps `false, assumed`. OR-17 p143 shows the lower bracket starts and
  the standard deduction rising every year and the 125,000 / 250,000 starts not moving, which points to indexing, but no
  sentence says so. Said in `approximations`, about 17 to 33 of tax for each year held flat.

## Unsure

- The retirement income credit's `covers` on another state's pension is my reading of an unqualified list, not a
  sentence naming such pensions. I rate it safe: p106's "Employee pensions" alone would cover it.
- Leaving the federal subtraction out rather than applying the maximum is a judgement; the table above is the whole
  case. A consumer that wants the other side has the ladder in the record.
- The `cap_reduced_by` on all railroad income is wider than the worksheet's Tier 1. Small, in `approximations`.
- `annuity` in the credit's `covers`: the booklet says "Employee annuity plans" (p52, IRC 403). A private commercial
  annuity is not on the list. Both readers listed `annuity`; the kind cannot be split. In `approximations`.
- `tools.report_pensions` lists the medical subtraction on every Oregon pension row, because it is `all_income`
  with a `min_age`, as if it were an age deduction. The record is right; the report's filter reads it wrong.
- Local taxes are out of scope (issue #1). The sources mention only transit taxes on self-employment.

- Main session, 2026-11-07 (format v1): `social_security_basis: gross` set on the relief(s) whose cap Social Security reduces, stating what the cases already used.

## 2026-11-08: marker ids and indexing covers

- Marker ids: all 11 markers have an `id`. Descriptive ids (no from_record id of their own): `or_surplus_kicker_credit`, `or_other_rates_subtractions_credits`; the rest take their first from_record id, so their warning codes are unchanged. `tools.checks --fix-warnings` rewrote the cases' accepted_warnings (the old shared code state_rule_not_modelled:unnamed becomes the new ids); nothing else in the cases changed.
- Indexing covers: `brackets`, `deductions`, `relief_caps` (reliefs.cap). `credits` (indexed, from the record's personal_exemption_credit cite, OR-17 PDF p.98 'The exemption amount is indexed for inflation') now covers only reliefs:personal_exemption_credit.credit_amount, since the cite speaks of the exemption amount, not the 100,000/200,000 AGI limits. Added `relief_income_tests` (indexed false, assumed) for reliefs.income_test: the exemption credit's AGI limits and the retirement income credit's income test.
- Assumed entries: the only indexing statements are the exemption credit (already in the record) and the 529-type subtraction limit (not in the projection); nothing says for brackets, the standard deduction or the retirement income credit, so they stay assumed.

## 2026-11-08: indexing settled from statutes

Statute research (work/indexing/findings*.json) settled every projection indexing entry that was `assumed: true`:

- `brackets` (brackets): split (kept as one entry), ORS 316.037(1)(b)-(e)
- `standard_deduction` (deductions:standard_deduction): indexed, ORS 316.695(1)(c)(B)-(C)
- `age_65_additional` (deductions:age_65_additional): not indexed, ORS 316.695(7)
- `relief_caps` (reliefs.cap): not indexed, ORS 316.157(2)(d)
- `relief_income_tests` (reliefs.income_test): not indexed, ORS 316.157(2)(d); ORS 316.085(5)
- Record `indexing`: added brackets -> yes; added standard_deduction -> yes; added age_65_additional -> no; added retirement_income_credit -> no; kept existing personal_exemption_credit (yes, booklet cite, about another figure of it); the statute says its income_test is not indexed.
- `brackets` is one entry, indexed true: the statute indexes every band limit except the 125,000 (250,000 joint) start of the 9.9% band (ORS 316.037(1)(b)(D)), and a covers selector cannot name one band, so a projection grows that start too (it understates tax above it in later years). Its note says so.
- Later the same day: the format gained `brackets:<n>` selectors, so the top band's start now has its own entry, `brackets_top_band` (covers `brackets:3`, not indexed, ORS 316.037(1)(b)(D)); the projection no longer grows it.
