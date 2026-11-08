# Settlement: Kentucky, tax year 2025

- Readings: `work/extract/2025/KY.r6.A.json`, `work/extract/2025/KY.r6.B.json` (round r6)
- Sources: `sources/archive/2025/KY/` (2025 Form 740 packet with instructions; 2025 Schedule M; 2025 Schedule P)
- Outputs: `data/states/2025/KY.record.json`, `data/states/2025/KY.projection.json`
- Settled: 2026-11-07
- Page numbers are PDF pages (pypdf markers). The differences chart is PDF page 9, printed page 7.

## Comparison

`uv run python -m tools.compare` reported **28 structured differences** (104 wording differences). The two
readers agreed on every figure; all 28 lines are entries one reader had and the other did not, or one rule
split two ways. Taken together they are five disagreements, and the booklet decided all five:

| # | Lines | Field | A | B | Booklet | Settled |
|---|---|---|---|---|---|---|
| 1 | 6 | `capital_gains` | none | eminent domain and Kentucky Turnpike Bond gains exempt | Packet PDF p.9 chart items 7 and 10, both "Exempt"; Schedule M PDF p.4 Line 14 lists "capital gains on property taken by eminent domain" | B's two entries: treatment differs from ordinary income, so in scope |
| 2 | 4 | Killed in the line of duty | no entry | `exempt_in_full`, `all_income`, scope person | Packet PDF p.6: "applies to all income from all sources of the decedent"; Schedule M PDF p.4 Line 14 | B's entry |
| 3 | 9 | Schedule P Part I: where Tier 2 railroad benefits sit | own entry | merged into the pre-1998 government entry | Schedule P PDF p.1 line 1 and PDF p.2: the service-credit test applies to the government pensions; Tier 2 benefits are taken whole, with no test | A's two entries (one entry per branch) |
| 4 | 3 | Tier 1 railroad benefits | no entry | own entry | Schedule M PDF p.3 Line 10: "Social Security and Social Security equivalent U.S. Railroad Retirement Board benefits" | B's entry |
| 5 | 6 | Social Security subtraction `who.basis` | `each_person` | `return` | Schedule M PDF p.3 Line 10 tests neither spouse and has no cap | `return` (schema: `return` when neither is tested) |

Decided from the booklet: all five (all 28 lines).

## The military pension question

Both readers, not one, listed `military_pension` in the uncapped pre-1998 entry, and both flagged it as a
judgement call, so it never showed as a structured difference. It was sent back to be settled from the form.

What Schedule P says:

- Part I line 1: "federal, Kentucky state and Kentucky local government pension income attributable to service
  credit earned before January 1, 1998".
- PDF p.2: "pension income paid by the federal government, by the Commonwealth of Kentucky, or by any Kentucky
  local government".
- PDF p.1 flowchart: "Are you retired from the federal government, the Commonwealth of Kentucky, or a Kentucky
  local government?"
- "Military" appears only for purchased service credit: PDF p.2 definitions ("i.e., military service or prior
  service with the same or similar system") and worksheet line 2.

So the form names no military pension as a payer, and it excludes none. The form's test is who pays, and the
only word it offers for that is "federal".

What the packet says, PDF p.9 chart item 2: "Retirement Income from: Commonwealth of Kentucky Retirement
Systems / Kentucky Local Government Retirement Systems / Federal and Military Retirement Systems", Kentucky
treatment "Partially exempt if retired after December 31, 1997; exempt if retired before January 1, 1998;
Schedule P may be required". The converted text puts that cell at the end of the page, away from its row, so
I rendered the page: the cell sits inside item 2 against all three lines, not against any other row.

**Settled: `military_pension` stays in `ky_pre1998_government_service`.** The chart is the only printed
statement on military retirement and it points those retirees to Schedule P with this treatment. The form is
silent on the word, and silence is not a contrary rule. Extraction rule 4 lists a kind "when the booklet names
it", and this booklet names it. The settlement brief's rule, the reading "printed most directly", points the
same way. `covers_unclear` was considered and not used: the chart does settle it, and the chart's own caveat
("not intended to be all inclusive") limits what it leaves out, not what it says.

Doubt that remains: the chart calls itself "a quick reference guide", and it is the only place the word
appears. The statute was not read (out of scope). The effect on a run is small: the pre-1998 entry is
`not_modelled`, so a military pension is held to the 31,110 limit either way. Only the wording of the marker
depends on this.

## Family Size Tax Credit and personal tax credits

Neither amount is in the sources, and the reason is a gap in the archive, not a misreading:

- **The packet holds no forms.** Form 740 and Schedule ITC are not in it. PDF pp.4, 10, 19, 20, 30 and 34 say
  "This page has been intentionally left blank", and PDF p.39 is empty (rendered and checked). The registry's
  finder note, "The 2025 Form 740 appears to be inside the packet PDF", does not hold for this file.
- **Personal tax credits.** PDF p.14 Line 17: "Enter amounts from Schedule ITC, Section B. NOTE: Use only if 65
  or over, blind, or in Kentucky National Guard." PDF p.25, the whole of Section B: "Complete this section only
  if you are 65 or over, blind or in the Kentucky National Guard." PDF p.21 lists them as a reason to file
  Schedule ITC. No amount is printed anywhere; a search of both converted texts of all three documents found
  none, and the $20 and $40 hits are the use-tax table on PDF p.15.
- **Family Size Tax Credit.** Printed: the 42,760 modified gross income ceiling (PDF p.14), the thresholds
  15,650, 21,150, 26,650 and 32,150 and "133 percent" (PDF p.3), the modified gross income definition (PDF p.11)
  and worksheet (PDF p.26), and two examples (PDF p.26: family of two at 22,650, 80%; family of four at 33,000,
  90%). The table is "located on the Schedule ITC" (PDF p.26) and is not printed. Two examples do not give band
  edges, so no `steps` are recorded and none are derived from the 133 percent.
- **What the record does.** Both readers kept these in `notes` only. The projection guide says every marker
  names its record ids, so I added `ky_personal_tax_credit_age_65`, `ky_personal_tax_credit_blind_guard` and
  `ky_family_size_tax_credit` as relief entries with no amount, each saying in its cite that the figure is not
  printed. No figure was supplied from memory. `credit_basis` is left out of the family size entry: the booklet
  never says what the decimal multiplies.
- **What is needed.** The 2025 Schedule ITC and Form 740 saved into `sources/archive/2025/KY/` and added to the
  registry. The agency refused automated downloads, so the owner saves them by hand (`fetch.json`). The
  personal credit for age 65 applies to many retired households, so this gap is worth closing.

## Other decisions

- **Roth conversions**: in `covers`, on the words of Schedule M PDF p.3 and packet PDF p.28, both "income
  received from converting a regular IRA to a Roth IRA". Schedule P PDF p.2's shorter list leaves those words
  out and does not say conversions fail.
- **`not_covered` on the pre-1998 entry**: B's "pensions of other states' governments" is not the booklet's
  wording. Replaced with the flowchart's own sentence, "You do not need to file Schedule P. You are limited to
  $31,110 in excludable retirement."
- **`not_covered` on the general exclusion**: B's line about deferred compensation describes Part I, not this
  entry. Moved to the pre-1998 entry.
- **Standard deduction**: `per: return` as both readers had it. Filing Status 2 gives each spouse 3,270 when both
  had income (PDF p.13); the projection has an approximation for it (130.80 a year).
- **`needs_input`**: not set on `ky_pension_exclusion`. Every pension kind gets the same 31,110 there, so the
  relief does not turn on the source. Only Schedule P Part I does, and that is `not_modelled`.
- **Projection, pre-1998 entry**: `not_modelled`, `warn_when: has_pension`. A projection cannot know the
  retirement date or months of service before 1998 (same treatment as North Carolina's Bailey exclusion). Without
  it the projection overstates tax; a worked example of 1,155.60 a year is in `approximations`.
- **Projection, family size credit**: `warn_when: never`, as with other low-income credits, with an approximation
  entry. The schema has no income-based warning.

## One-sided entries

- Kept: the five in the table above, as they are printed and in scope.
- Dropped: B's indexing cites (the answers match A's, and a cite to where the figure is printed adds nothing).
- Added by the settler: the three credit entries above; an indexing entry for the family size figures, recording
  "based on the federal poverty level" while staying `not_stated`.
- Corrected from the readers' notes: "nonrefundable" for the personal and family size credits is not in the
  sources for those credits, so it is not repeated.

## Facts checked against a second line or document

1. **Other states' government pensions, and New York**: `public_pension_other_state` in `covers` of
   `ky_pension_exclusion`; not in `ky_pre1998_government_service`. Not named in the sources, and "New York" appears
   nowhere in them. General words: "All pension and retirement income paid under a written retirement plan
   (qualified or unqualified) is eligible for exclusion" (Schedule M PDF p.3; packet PDF p.28; Schedule P PDF p.2
   has the same sentence without the parenthesis). Limit: "You do not need to file Schedule P. You are limited to
   $31,110 in excludable retirement." (Schedule P PDF p.1). Chart item 4, "Other Pension and Annuity Income",
   "100% excludable up to $31,110 per taxpayer" (PDF p.9), agrees. Reciprocity on PDF p.22 covers wages and
   personal services only, so `paying_states` is not used. Judgement call: the kind comes from the general words.
2. **Kentucky and federal government pensions**: two layers that add. Part I: "completely excludable above the
   $31,110" for service credit before January 1, 1998. Note on Schedule P PDF p.2: "Subtract the exempt amount from
   the taxable pension amount and include the difference with other retirement income in Part II." Line 4 adds
   lines 1(c) and 3. Chart item 2 agrees.
3. **Private pensions, IRA and employer-plan distributions, Roth conversions**: "This includes pensions, annuities,
   IRA accounts, 401(k) and similar deferred compensation plans, income received from converting a regular IRA to a
   Roth IRA, death benefits, disability retirement benefits and other similar accounts or plans" (Schedule M PDF
   p.3; packet PDF p.28). Cap 31,110 per person: "This exclusion is for each taxpayer and must be computed
   independently of your spouse". 31,110 also on Schedule M p.1 line 9, Schedule P lines 3 and flowchart, and chart
   item 4. No age, birth-year or income test is printed.
4. **Social Security**: exempt. Subtraction line, Schedule M p.1 line 10: "Enter taxable amount of Social Security
   and Railroad Retirement Board benefits from federal Form 1040 or 1040-SR, line 6(b)". Sentence, packet PDF p.3:
   "Social Security income, which was already exempt from Kentucky taxation prior to the federal updates, remains
   exempt under KRS 141.019(1)(e)." Chart item 6: "Exempt".
5. **Brackets and deductions**: one rate for every status, "Multiply line 11 by four percent (.04)" (PDF p.13) and
   "For 2025, the tax rate for individual income tax is 4%" (PDF p.3). Standard deduction: "For 2025, the standard
   deduction is $3,270" (PDF p.3); PDF p.13 Line 10; PDF p.31. No personal or dependent exemption and no age-65 or
   blindness deduction found in the booklet; the credits above stand in their place. 4,270 and 5,270 in Chart B
   (PDF p.11) are filing thresholds. No surtax or recapture found.

## Unsure

- Military pensions rest on one chart line (see above).
- `who.basis: each_person` on the personal tax credits is a judgement call; the text says "if you are 65 or over"
  and does not cover two spouses.
- Relief entries with no amount are a new shape: earlier states kept a credit with no printed amount in `notes`,
  with a `from_record: []` marker (Illinois dependents, Iowa gains). Validator and tools accept it.
- The Schedule ITC and Form 740 are missing, so rule 0 (read the return form) could not be met for Form 740; the
  line numbers here come from the instructions. Any fact printed only on those forms is unseen.

## Schedule ITC and Form 740 (added 2026-11-07)

The 2025 Form 740 and Schedule ITC were archived after settlement. Schedule ITC Section B prints the personal tax credits: 40 for a person 65 on or before 12/31/2025 (lines 1 and 5), 40 if legally blind, 20 for the Kentucky National Guard. Section C prints the Family Size Tax Credit Table (by family size one to four, 100% down to 10%, none above 20,815 / 28,130 / 35,445 / 42,760). Form 740 line 17 takes the personal credits; line 21 multiplies line 19, the tax after them, by the family size percentage.

The projection now models the 40 age credit per person and the family size credit as a share of tax, with family size taken from filing status (one for single, two otherwise; dependents are not modelled) and modified gross income mapped to federal AGI plus tax-exempt interest. Blind and National Guard stay not modelled: a projection has neither fact. Settled in the main session (the settler stopped at the weekly limit); a second look by a fresh settler is still worth doing.

## 2026-11-07: fresh review

A second settler checked the hand edits made after the first settler stopped, against the printed text (pypdf page markers). Helper scripts: `verify_table.py` and `apply_fixes.py` in the dispatch's private folder.

**Checked and found right**

- **Family Size Tax Credit Table** (Schedule ITC PDF p.2): all 40 band edges and the percentage column (100 to 10, then 0) parsed from the pypdf text, which agrees row for row with the docling table. The record's `as_printed` holds every edge for sizes one to four in order. The record's structured steps (`single` = size one, `married_joint` = size two) and all five projection step lists (single = size one, the other four = size two) match the table exactly, with "is over / is not over" read as the schema's default `over`.
- **Thresholds and the 133 percent rule**: the first edges are the PDF p.3 thresholds 15,650 / 21,150 / 26,650 / 32,150, and the last edges 20,815 / 28,130 / 35,445 / 42,760 are each 1.33 times the threshold rounded to the dollar. 42,760 is printed on packet PDF p.14 ("If your total MGI is $42,760 or less") and Form 740 PDF p.1 line 5. Both examples (packet PDF p.26, Schedule ITC PDF p.8: size two at 22,650 gives 80%; size four at 33,000 gives 90%) agree with the table.
- **Modified gross income**: the record's wording is packet PDF p.11 word for word. The worksheet (Schedule ITC PDF p.8; packet PDF p.26) matches it and adds the spouse's federal and Kentucky AGI (lines b and g) for a married separate filer living in the same household.
- **Credit order** (Form 740 PDF pp.1-2): line 14 tax, 15 Section A credits, 16, 17 personal credits, 18 = 16 - 17 with "If line 17 is larger than line 16, enter zero", 19 = sum of line 18 Columns A and B, 20 family size, 21 = line 19 x the decimal, 22 = 19 - 21. So the family size credit is a share of the tax after the personal credits; `credit_rate` 1 with `credit_basis` tax is right.
- **Personal credits** (Schedule ITC PDF p.2 Section B): 40 if 65 on or before 12/31/2025 (lines 1 and 5), 40 if legally blind on 12/31/2025 (lines 2 and 6), 20 if in the Kentucky National Guard on 12/31/2025 (lines 3 and 7). The taxpayer's lines are 1-3 and the spouse's 5-7, the spouse's "Complete only if filing joint or married, filing separately on a combined return". Lines 9-12 carry them to Form 740 line 17, not to exceed 100 a person or 200 joint. `each_person` and `min_age` 65 are right; the earlier "judgement call" on `who.basis` is now settled by the separate lines.

**Wrong, and changed**

- Record, `ky_family_size_tax_credit.income_test.threshold` was `all: 42760`. The schema says the test applies above the threshold, so a consumer would give family size one full credit up to 42,760. Changed to `single: 15650, married_joint: 21150`, each structured column's first edge, as Pennsylvania's tax forgiveness does. 42,760 and the 133 percent rule stay in `as_printed`.
- Record notes still said Form 740 and Schedule ITC were missing, that no personal credit amount or family size band was printed, and that `credit_basis` was left out. Those four notes are rewritten from the forms.
- Record cites for the three hand-edited entries had no PDF pages. Pages added (Schedule ITC PDF p.2, p.7, p.8; Form 740 PDF pp.1-2; packet pages). The MGI `as_printed` adds the worksheet's spouse lines; the family size `who` adds the printed size one to four definitions; the blind and Guard condition gives the 12/31/2025 date.
- Projection, family size approximation: said `overstates_tax`. That is not always true. A head of household or qualifying surviving spouse with no qualifying child, or a married separate filer who lived apart all year, is family size one on the form but gets size two here, which understates tax. Direction changed to `either`, with sizes: 1,155.20 too much for a single parent of three at 32,150; 715.20 too little for a family-size-one filer at 21,150.
- Projection, MGI approximation: "one 10% step at most" was not true, because bands are only 469 to 1,286 wide and Kentucky bond interest can move the credit several steps. Re-sized.
- Projection, married separate approximation: said "under 42,760", but size two ends at 28,130. Re-sized (at most 715.20).
- Projection, order approximation: `what` kept word for word (case `ky_2025_family_size_after_age_credit` quotes it). Its size now gives the error if the order is reversed (at most 72).
- Projection `record.sha256` updated; thresholds and steps unchanged.

No case's expected figures change: every case goes through single or married_joint with no dependents, and the projection's computed rules did not change. Validate: both ok. Checks: 16 cases ok.

## 2026-11-08: marker ids and indexing covers

- Marker ids given: first from_record id (warning code unchanged): `ky_pre1998_government_service`, `ky_personal_tax_credit_blind_guard`, `ky_us_government_interest`, `ky_active_duty_military_pay`, `ky_killed_in_line_of_duty`, `ky_eminent_domain_gains`; descriptive: `ky_other_credits_and_averaging` (no from_record id).
- Indexing covers: `brackets` -> `brackets`; `deductions` -> `deductions`; `relief_caps` -> `reliefs.cap`; `credits` -> `reliefs.credit_amount`; `family_size_tax_credit_thresholds` -> `reliefs:ky_family_size_tax_credit.income_test`.
- Added `credits` (indexed false, assumed) for the 40 age-65 personal tax credit, which no entry covered.
- Added `family_size_tax_credit_thresholds` (indexed false, assumed) for the family size tax credit's income test. The packet says the credit is 'based on the federal poverty level' and prints 'The 2025 threshold amount' (PDF page 3), but not that it is adjusted each year; the record keeps not_stated, so this stays assumed.
- Every `assumed` answer was checked again against the archived sources (searched for indexed, inflation, cost-of-living, adjusted annually, each year, CPI, fixed): none says, so all stay `assumed: true`.
- `tools.checks --fix-warnings` updated the cases' accepted_warnings where a code changed; nothing else in the cases changed.
