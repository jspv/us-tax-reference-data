# Settlement: Massachusetts, tax year 2025 (re-settlement: other states' government pensions)

- Earlier settlement: `work/extract/2025/MA.r2.A.json` / `MA.r2.B.json`, logged in `docs/pilot-2025-ledger.md`
  (Round 2). That settlement is kept; this round changes only what the new sources settle.
- New sources read in full (`sources/archive/2025/MA/`):
  - TIR 95-9, "Income Taxation of Contributory Public Employee Pensions of Other States", 01/10/1996
    (`tir-95-9-*.page.txt`)
  - DOR page "Tax Treatment of Government Pensions", updated April 3, 2026 (registry title "Tax Treatment of
    Out-of-State Government Pensions for MA Residents"; `tax-treatment-of-out-of-state-*.page.txt`)
  - Letter Ruling 81-91, "New York State Contributory Pension", 10/07/1981 (`letter-ruling-81-91-*.page.txt`)
  - 2025 Form 1 return (`2025-form-1-massachusetts-resident-income-tax-return.*`)
  - Also re-read: 2025 Form 1 instructions PDF p10-11 (Line 4, "What pensions are exempt?") and PDF p22
    (Schedule Y line 13); the "Differences between MA and federal tax law" page's pension paragraph.
- Outputs: `data/states/2025/MA.record.json`, `data/states/2025/MA.projection.json`
- Settled: 2026-11-07

## What each new source says

### TIR 95-9 (01/10/1996)

The statute (M.G.L. c. 62, § 3(B)(a)(4)) allows a deduction of "any income from a contributory annuity,
pension, endowment or retirement fund of any other state or any political subdivision thereof, provided that
income from any such similar fund established under the laws of the commonwealth is not subject to taxation
in such other state or political subdivision."

Before Pariser the Department required a "blanket exemption for all Massachusetts contributory public
employee pension income". The Appellate Tax Board in Pariser (a Massachusetts resident over 59½ with
$11,322 from a New York State contributory pension) held that "the focus was on whether the taxpayer would
have been taxed in the payor state if he were a resident of that state and the income had been paid by a
Massachusetts pension."

The rule after Pariser, quoted:

> A Massachusetts resident will be allowed a deduction for income received from a contributory annuity,
> pension, endowment or retirement fund of another state or its political subdivisions if:
> (1) that other state has a specific income exclusion for pension income which applies to Massachusetts
> state or local contributory public employee pension plans; or
> (2) that other state has a specific deduction or exemption for pension income which applies to
> Massachusetts state or local contributory public employee pension plans; or
> (3) that other state has no income tax.

> The amount of the deduction ... will equal the amount of the specific pension exclusion, deduction, or
> exemption that could be claimed by the taxpayer under the laws of the other state if the taxpayer were a
> resident of the other state and received the income from a Massachusetts state or local contributory
> pension. In the case of a state that has no income tax, all income from qualifying pensions of the other
> state or its subdivisions may be deducted.

New York, as the TIR quotes its law ("Section 617(c)(3-a)"): "Pensions and annuities received by an
individual who has attained the age of fifty-nine and one-half, . . . to the extent includable in gross
income for federal income tax purposes, but not in excess of twenty thousand dollars."

> Example 1: A Massachusetts resident who is 62 years old receives $25,000 of pension income from a New
> York state contributory public employee pension fund. ... New York allows a deduction for pension income
> provided the recipient is 59½ years old or older and the deduction is not in excess of $20,000. The
> Massachusetts resident is allowed a deduction in the amount of $20,000 for the New York pension income.

> Example 2: A Massachusetts resident who is 55 years old receives $25,000 of pension income from a New
> York state contributory public employee pension fund. The taxpayer, who is not 59½ years old or older, is
> not allowed a deduction for any of the New York pension income.

> Example 3: State A has a personal income tax with a standard personal exemption of $10,000 applicable to
> any type of income, but no specific exclusion, deduction or exemption related to pension income. ... No
> part of the $15,000 of pension income is deductible ... because the $10,000 personal exemption in State A
> is not specifically related to pension income.

"This TIR revokes Letter Rulings 81-91 and 85-12 and Technical Information Releases 80-4 and 89-10."

### Tax Treatment of Government Pensions (DOR page, updated April 3, 2026)

"Out-of-state employee contributory government pension": "you can deduct those amounts from your
Massachusetts gross income if the former state doesn't tax income its residents receive from Massachusetts
contributory public employee retirement plans", then the same three tests as TIR 95-9, word for word.
"First, include the income you received in your Massachusetts gross income as pension income on Form 1,
Line 4. If the amount is deductible from Massachusetts gross income, claim it as a deduction on Schedule Y,
Line 13." Part-year residents: "If a partial exclusion from income applies, reduce the Massachusetts
related exclusion by the amount excluded in the former state during the same tax year." Reporting:
"Depending on the other state's tax treatment of Massachusetts pensions, some or all of the pension you
reported as income can be excluded on Schedule Y (Line 13)." It links a list "Other State's Tax Treatment of
Out-of-State Employee Contributory Government Pensions", which is not in the sources; the page names no
state.

Other sections, checked against the record:
- Federal contributory pensions (incl. U.S. Postal Service) excluded; "Senior U.S. judges' pension
  distributions are subject to Massachusetts income tax ... since they're not contributory." Consistent
  with `us_ma_contributory_pension`; the judges added to its `not_covered`.
- Massachusetts state/local contributory (incl. ORP), police/fire, MBTA: excluded. Consistent.
- TSP: "Distributions made to the retiree from the plan are fully taxable in the year paid." 457:
  "Distributions ... are included in gross income in the year paid." 403(b): excluded only to the extent of
  Massachusetts previously taxed contributions. Consistent with the record (no relief; basis approximation).
- "Tier I or Tier II railroad retirement benefits are exempt from Massachusetts taxation." New to the
  record (see Changes).
- U.S. military pensions excluded. Consistent.
- Veterans under c. 32 §§ 56-60 who began service before July 1, 1939: "After receiving the lump sum, any
  pension amount received is considered non-contributory, and is taxable." Consistent (already in
  `not_covered`).

### Letter Ruling 81-91 (10/07/1981)

Quotes N.Y. Tax Law § 612(c) paragraph 3-a: "Pensions and annuities, not otherwise excluded ... but not in
excess of twenty thousand dollars received by an individual who has attained the age of fifty-nine and
one-half". Held that because Massachusetts pensions "will continue to be taxed to New York residents who
have not attained age 59½, as well as to New York residents of any age to the extent the income exceeds
$20,000, the deduction ... will not apply", so a New York State contributory pension stayed fully taxable.
**Revoked by TIR 95-9**; used for nothing except to confirm the New York text.

### 2025 Form 1 return

Line 4 "Taxable pensions and annuities"; line 15 "Other deductions from Schedule Y, line 19" (Schedule Y
itself is not in the form file; its line 13 is described in the instructions, PDF p22). Lines 11a/b
(2,000 each), 2a (4,400 / 6,800 / 8,800), 2b (1,000), 2d (2,200), line 22 (.05), 23a (.085), 23b (.12),
28b 4% surtax: all match the record. Line 2c: the text layer (pypdf and docling) reads "× $ 1,700 = 2c";
the rendered page 1 (pypdfium2, checked visually) prints "× $  700 = 2c", matching the instructions (PDF p10,
$700). The "1" is a text-layer artifact; 700 kept. Nothing on the form contradicts the record.

### Differences between MA and federal tax law (already in the folder)

"Pensions eligible for the exclusion include those paid by the Commonwealth and its cities and towns,
contributory plans of other states, and contributory plans of the federal government." This omits the
reciprocity test; the instructions and TIR 95-9 state it, and are followed.

## The rule for a Massachusetts resident with a New York State pension

- Contributory New York State public employee pension, recipient 59½ or older: deduct up to 20,000 a
  person on Schedule Y line 13 (TIR 95-9 Example 1: age 62, 25,000 received, 20,000 deducted); the rest is
  taxed at 5%.
- Under 59½: no deduction; all of it is taxed (Example 2).
- The 20,000 and 59½ are New York's figures as TIR 95-9 quotes them; the TIR's amount rule ties the deduction
  to what New York would allow on a Massachusetts pension, so a change in New York law would change it.
- Noncontributory pensions are outside § 3(B)(a)(4) (it covers only a "contributory annuity, pension,
  endowment or retirement fund"): taxed.

## Changes

| Field | Was | Now | Source |
|---|---|---|---|
| `reliefs.other_state_contributory_pension` | one entry, `covers: [public_pension]`, condition "that state does not tax such income from Massachusetts (see TIR 95-9 for which states)" | `covers: [public_pension_other_state]` (rule 14); tests (1)-(2) and the amount rule in `who`/`cap_rule`; `not_covered`: noncontributory plans, general exemptions (Example 3); for a paying state without its own entry | TIR 95-9; instructions p10, p22; DOR pensions page |
| `reliefs.other_state_contributory_pension_ny` | — | new: `paying_states: [NY]`, `min_age: 59.5`, `cap: 20000` per person | TIR 95-9 (NY law quoted; Examples 1, 2) |
| `reliefs.other_state_contributory_pension_no_income_tax` | — | new: test (3), all of it, no cap; no `paying_states` because the sources name no such state | TIR 95-9 |
| `reliefs.railroad_retirement_exempt` | — (note: "not found in the booklet ... no relief entry written") | new, `exempt_in_full`, `railroad_retirement` | DOR pensions page, "Tier I and II railroad retirement pension" |
| `reliefs.us_ma_contributory_pension.not_covered` | 3 items | + senior U.S. judges' pensions ("not contributory") | DOR pensions page |
| `notes` | pension and railroad notes | rewritten for the new sources; 9 "Settlement 2026-11-07" lines | — |

The three other-state entries name each other in `cannot_combine_with`, so New York pension income is not
also run through the general entry.

Unchanged: brackets, surtax, exemptions and deductions, Social Security (exempt), U.S./MA contributory
and military exemptions, firefighter/police exclusion, municipal interest, capital gains, indexing,
recapture. No new source contradicts them.

## Projection

- `record.sha256` = sha256 of the record as written (961c5a81...).
- New relief `other_state_contributory_pension_ny`: subtraction, `public_pension_other_state`,
  `needs_input: [pension_source, pension_contributory]`, `paying_states: [NY]`, each person, `min_age` 59.5,
  cap 20,000 per person.
- New relief `railroad_retirement`: `exempt_in_full`.
- `not_modelled`: the general and no-income-tax entries (any other state), `warn_when: has_pension`: the
  amount depends on the other state's law and the sources name no other state, so such a pension is taxed in
  full (overstates tax where a state qualifies).
- Approximations added: the 59½ test applied by age in the year (direction either; the turning year only);
  part-year residents moving from New York not reduced by New York's own exclusion (understates tax, move
  year only).

## Validation

```
data/states/2025/MA.record.json: ok
data/states/2025/MA.projection.json: ok
```

## Unsure

- "Credits don't count": no source says anything about credits. The tests name an "exclusion",
  "deduction" or "exemption" for pension income; recorded only that, with a note.
- The New York figures (20,000 at 59½) are New York's law of 1981-1996 as Massachusetts quotes it; the
  Massachusetts sources say nothing about New York's 2025 law. A reviewer may check them against the New York
  record, which this settlement did not use.
- New York localities' pensions (e.g. a city system): the general rule covers "another state or its
  political subdivisions", but the examples name only New York State funds. `paying_states: [NY]` is
  read as covering both; the entry's condition says "New York State contributory public employee pension
  fund", as printed.
- On what date 59½ is measured is not stated in the Massachusetts sources.
- TIR 95-9 cites New York's provision as § 617(c)(3-a); LR 81-91 as § 612(c) paragraph 3-a. Same text.
- The railroad entry is an addition beyond the New York question; it rests on one sentence of the DOR page,
  and the instructions are silent.

## 2026-11-08: marker ids and indexing covers

- Marker ids given: first from_record id (warning code unchanged): `other_state_contributory_pension`, `dependent_exemption`, `retirement_contribution_deduction`, `rental_deduction`, `firefighter_police_incapacity_exclusion`, `collectibles_gains`.
- Indexing covers: `ma_4pct_surtax` -> `brackets`; `deductions` -> `deductions`; `relief_caps` -> `reliefs.cap`.
- `ma_4pct_surtax` (indexed, cite in the record) covers `brackets`: the surtax is folded into the brackets, and the 1,083,150 start of the 9% band is the only band start above 0.
- Added `relief_caps` (indexed false, assumed) for the 20,000 New York contributory pension cap; the letter ruling and TIR 95-9 print New York's 20,000 without saying whether it changes.
- Every `assumed` answer was checked again against the archived sources (searched for indexed, inflation, cost-of-living, adjusted annually, each year, CPI, fixed): none says, so all stay `assumed: true`.
- Warning codes unchanged (every id is the marker's first from_record id).

## 2026-11-08: indexing settled from statutes

- `deductions` (projection `deductions`): not_indexed, M.G.L. c. 62 s. 3(B)(b)(1)(A), (1A), (C): revenue-triggered fixed steps already at their caps; age 65 fixed 700. Record `personal_exemption` and `age_65_exemption` added as no.
- `relief_caps` (projection `reliefs.cap`): not_indexed, N.Y. Tax Law 612(c)(3-a) as applied by M.G.L. c. 62 s. 2(a)(2)(E) and DOR TIR 95-9 (medium confidence: only part of section 612 was read). Record `other_state_contributory_pension_ny` added as no.
