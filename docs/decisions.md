# Decisions

## 2026-11-06: converter, fetch path, archive, repository

**Fetch: headless Chromium only.** Plain HTTP downloads are refused by some agencies
(Massachusetts returned 403 to curl, with or without browser-style headers, and a real browser
loaded the same file). The Michigan 403 seen earlier came from the fetch tool, not the state, so the
refusal pattern is not predictable. One path, `tools/fetch.py`; a download that is not a PDF is a
failure and the jurisdiction goes on the manual list.

**Converter: Docling primary, pypdf second.** Bake-off (`tools/bakeoff.py`, four booklets: GA, UT,
MI, MA; checks are figures confirmed by hand from the booklets, and the Georgia retirement
worksheet with each line number required directly before its own label):

| Converter | Figures present | Georgia worksheet rows | Speed |
|---|---|---|---|
| pypdf | all | 7 of 8 (line 15 label detached from its number) | instant |
| pdfplumber | all | 4 of 8 | instant |
| Docling | all | 8 of 8 | about 12 s a page (CPU, arm64) |

Docling keeps worksheet and table rows together, which is where the calculation lives. Its output
has noise on comb-style form fields (stray commas) and fuses a few adjacent labels, so it is not
read blind. pypdf is kept as a second text from a different method, so a figure that appears in
both is better supported and a figure that appears in only one is looked at. The converter sits
behind `tools/convert.py` so it can be replaced; pdfplumber is dropped (worst on layout). PyMuPDF was
not tried (AGPL).

**Archive: keep every downloaded PDF in the repository for now** (maintainer, 2026-11-06). Revisit if
size becomes a problem; each file's sha256 is recorded in its `fetch.json`.

**Repository:** its own repository, separate from any application that uses the data.

**Open: sources that are not PDFs.** A no-income-tax state has no booklet to read, only an agency
statement on a web page. The fetch tool handles PDFs only; HTML sources are added when the first
such state is done.

## 2026-11-07: fetch falls back to a plain request

The browser-only rule (2026-11-06) assumed agencies block simple clients and serve browsers. The
full 2025 run found the reverse too: Maine, Kentucky and Colorado refused headless Chromium (HTTP 403)
while the source finders opened the same files with plain `curl` or a server-side fetch. So `fetch.py`
tries the browser first and, when it is refused or gets no PDF, one plain HTTP request that names
itself honestly (no browser disguise). Every `fetch.json` record says which `method` got the file.
Anything both refuse goes on the manual list.

## 2026-11-07: maintainer decisions on NC military retirement and 401(k)/IRA coverage in GA, HI, MS

**North Carolina, Uniformed Services retirement deduction (Schedule S Line 21).** The deduction is
for a military retiree with at least 20 years of creditable service or a medical retirement. A
projection knows neither fact. The maintainer decided (2026-11-07) that the projection **assumes every
military pension qualifies** and deducts it in full. This is a deliberate assumption, not something
the booklet says. It understates tax for a retiree who left with less than 20 years and no medical
retirement: by 4.25% of the pension, 1,275 a year on 30,000. The projection lists it as an
approximation and its warning tells the user when a military pension is present. Rejected: taxing
every military pension (overstates tax for most military retirees), or adding a projection input for
years of service and medical retirement (possible later; it is a change for a consumer, not the data).

**Georgia, Hawaii and Mississippi: do 401(k), 403(b), 457 and IRA payouts count?** The booklets did
not say. The maintainer asked for the question to be researched in each state's own law and settled
(2026-11-07). Design rule (design.md): a figure may trace to an agency booklet, a statute or a
regulation; all three are the state's own publications.

- **Georgia: they count.** The retirement income exclusion covers all unearned income in Georgia
  taxable income: the Schedule 1 worksheet takes interest, dividends, alimony, capital gains, other
  income, taxable IRA distributions, taxable pensions and rents (IT-511 page 24), and excludes only
  income not taxable to Georgia and lottery or gambling income. A 401(k), 403(b) or 457 payout is a
  federal "pensions and annuities" item (and would be "other income" otherwise), so it is in the
  exclusion; a Roth conversion is a taxable IRA distribution. Source: the IT-511 booklet already
  archived; Georgia's rule 560-7-4-.02 ("income from pensions and annuities, and other similar income")
  agrees but rules.sos.ga.gov refuses automated download.
- **Mississippi: they count, except early distributions.** DOR regulation Title 35 Part III, Subpart
  02, Chapter 07 (sos.ms.gov ACCode 00000158c, page 18): rule 100 exempts retirement allowances,
  pensions, annuities and optional retirement allowances from any federal, state or private plan;
  rule 101 says optional retirement allowances include all income from Keogh plans, IRAs and other
  similar tax deferred plans; rule 102 adds deferred compensation plans (401(k), 403(b), 457) when the
  recipient qualifies for retirement income by age, service or other criteria; rule 104 leaves early
  distributions taxable.
- **Hawaii: the employee-funded part is taxable.** HAR 18-235-7-03 (amendment effective 1/1/98,
  files.hawaii.gov) excludes a pension only to the extent of employer contributions: the exclusion
  ratio is employer contributions over employer plus pretax employee plus previously taxed
  contributions, and "pretax employee contribution" names 401(k) deferrals, SEP salary reductions,
  457 deferrals and IRAs the employer did not fund. A rollover IRA keeps the character of the money
  rolled in. The Department of Taxation's 2026-07-14 Tax Review Commission presentation says
  traditional IRA and 401(k) withdrawals are fully taxable in Hawaii. A projection does not know the
  employer share, so 401(k) and IRA payouts stay taxed, which overstates tax by the employer-funded
  share (matching and profit-sharing contributions); the warning says so.

## 2026-11-07: format for the first frozen schema

A consumer's state evaluator builds against the first frozen schema tag, so the fields it reads must be
settled first. Validation-only fields (`brackets.derivation`) and the checks format can still change
after the tag.

**Added** (projection schema; the record schema mirrors the income test):
- `income_test.effect: share_phase_out` with `width` and `share_decimals` (ME pension deduction; VT
  exemptions). Exact where eight equal steps or `not_modelled` stood in.
- `measure.minus_reliefs` (MO Line 6).
- `warning_trigger`: `has_retirement_account_distribution` (with `age_range`), `has_long_term_gains`,
  `has_other_state_public_pension`, `income_over` (with `income_over`). A run warns only when the
  household hits the case (MS, HI, KS, WA, MD).
- `reliefs[].assumption` (NC; CA), code `state_assumption:<relief id>`; its text is also an
  approximation.
- `reliefs[].refundable` (ID).
- `reliefs[].cap_reduction` (IN).
- `capital_gains[].applies_over` (MD's 2% above 350,000 federal AGI).
- `income_test.steps[].rate` (CT Table E).
- Stated in the schema: best_of_group is chosen per person; negative `extra_rate` and limiting gains to
  taxable income first; `deduction_share` on a net gain only; source outranks kind; `['federal']` alone
  in `paying_states`; the recapture measure picks the worksheet; a rule with no printed amount is a
  `not_modelled` marker; Social Security and municipal treatment are ignored without an income tax.
- U.S. obligation interest gets no field: every state must exempt it (31 U.S.C. 3124), so the answer
  never differs; a consumer that separates Treasury interest exempts it itself.

**Deferred past the first tag**, each with its approximation and size already in the projections:
recapture worksheet structures (NY, off by at most 304 at one sample point; CT tables), Connecticut's
partial Social Security formula (about 2,000 a year too much above the limits), per-spouse brackets (MS at most
440 a year; MO), New Jersey's earned-income test inside a relief, and per-status formula constants
(validation only). Each is an added optional field when it comes, so a consumer can ignore it until
it reads it.

Added while the states adopted the fields (same day, before the tag): `income_test.reduce_each_person`
(default one reduction on the return's total, as VA, UT and MO do), `reliefs[].social_security_basis`
(gross, taxable or nontaxable Social Security uses up a cap; the states differ: gross ID IN ME MD OR,
taxable CO MI, nontaxable MN), `income_over.applies_when` (CT's "75,000 or more"), record
`capital_gains[].applies_over` (MD), share rounding half up, refundable credits counted in full in
`credits`, and covered income net and floored at 0. The qualifying surviving spouse key is stated as
absent (married_joint everywhere so far). Format version 1 is tagged `format-1` once every state is
re-verified; `schema/FORMAT_VERSION` holds `1` and every export's manifest carries it.

## 2026-11-07: `requires` for fields added within format 1

Within format 1, new fields are optional. A field that changes what a relief means (it applies only
above an income level, or it keeps part of the income taxed) would be misapplied by a reader that
ignores it. So such a relief lists the field in `requires`, and a reader that does not implement every
listed field skips the relief and warns, as for a not_modelled rule. This makes later additions safe
for a reader built at the tag. First uses: `applies_over` and `keeps_taxable` (Connecticut's partial
Social Security subtraction). It was added before the first consumer built its evaluator, so every reader built at format 1 knows to skip such a relief.

2026-11-07, later: Connecticut's partial Social Security formula and New Jersey's earned-income test
are no longer deferred: both are modelled within format 1 with fields listed in `requires`
(`applies_over`, `keeps_taxable`, `earned_income_limit`). Still deferred: recapture worksheet
structures (NY, CT), per-spouse bands (MS at most 440 a year, MO at most about 176).

## 2026-11-07: maintainer decisions on refundable credits and the remaining small format items

**Refundable credits (Idaho's Food Tax Credit).** The maintainer decided the data stays unchanged,
because the data records what the law says: Idaho's projection still marks the credit
`refundable: true` and its checks still show the form's figures, including a negative
`state_income_tax`. A consumer that keeps state income tax non-negative can floor it at zero
when it reads the data. Effect of flooring: for a very low-income Idaho household the credit is
understated by at most 155 a person a year; no other state has a refundable credit in the data.

**Remaining small format items.** The maintainer decided not to pursue them: recapture worksheet structures
(NY, CT) and per-spouse bands (MS at most 440 a year, MO at most about 176). Each stays a documented
approximation in its state's projection. They can be reopened later as optional fields listed in
`requires`.

## 2026-11-07: source documents pulled on demand

The 2026-11-06 decision kept every downloaded PDF in the repository. For a public dataset that makes
every clone carry about 200 MB of documents most users never open, and it would re-publish state
documents whose reuse terms vary. So the PDFs leave the repository. `fetch.json` keeps each source's
address, the sha256 of the exact file read, and `archived_url`: an Internet Archive capture whose
content digest equals that file, so the copy is the same bytes. `uv run python -m tools.sources pull`
downloads from the archived copy (or the agency) and keeps a file only if its sha256 matches, then
converts it. Web pages are kept as their converted `.page.txt` text, because a rendered page has no
stable hash. Figure presence (`tools.validate`) needs the sources pulled first.

## 2026-11-08: four additions within format 1 (raised by a consumer building an evaluator)

All are optional fields, so a reader built at format 1 still reads every file.

- **Marker ids** (`not_modelled[].id`). 43 markers in 19 states had no from_record id, and in Hawaii and
  Mississippi two markers started with the same one, so their warning codes collided. Every marker now
  has an id, unique in its projection, and the warning code is `state_rule_not_modelled:<id>`. Where a
  marker had a unique first from_record id, the id is that, so its code did not change.
- **What each indexing answer covers** (`indexing[].covers`). The indexing list named figure families in
  free text. Each entry now lists selectors (`brackets`, `deductions:<id>`, `reliefs.cap`,
  `reliefs:<id>.income_test`, ...), and the validator requires every amount a projection grows to be
  covered by exactly one entry at its most specific level. While adding them, every `assumed` answer
  was checked again against the sources.
- **Vermont's minimum tax** (`recapture[].other_rule: minimum_tax_on_measure`). `effect: other` had no
  defined meaning. The new field says: when the measure is over the threshold, the tax before credits is
  the greater of the schedule tax and the rate times the measure. A reader that does not know
  `other_rule` skips the rule and warns.
- **The federal senior deduction in states that start from federal taxable income**
  (`base.federal_senior_deduction`: follows, added_back or not_stated; the record holds the cite). P.L.
  119-21 added a 6,000 deduction per person 65 or older for 2025-2028, taken in computing federal
  taxable income. Each of the six such states (CO, IA, MT, ND, NM, SC) says whether it keeps it.

## 2026-11-08: jointly held income in states with per-person reliefs

Delaware, Georgia and New Jersey have reliefs figured per spouse that cover interest, dividends or gains.
All three count income from a jointly held account half to each spouse (Delaware and Georgia by rule, New
Jersey by its worked example). A new optional field, `joint_income` (half_each, by_ownership, not_stated),
says so in the projection; the record carries the cite. It changes tax: in Georgia, a couple aged 67 and 63
with 40,000 of joint interest owes 1,608.90 with the split, 2,646.90 if all is given to the older spouse.
The validator requires the field wherever a per-person relief covers investment income. Findings:
`work/settlement/2025/findings-2026-11-08-*.md`.

## 2026-11-08: two checks corrected; income test width; joint income on separate returns

A consumer's evaluator, built from the schema, matched 1,411 of the 1,413 checks. Both misses were errors in
the checks: they had been worked before the schema added the rule that settles them, and kept the old
approximation.

- `va_2025_age_income_joint_both_reduced`: the excess of income over 75,000 comes off the couple's combined
  24,000 once (`reduce_each_person` defaults to false), giving an age deduction of 14,000, the form's
  figure. The check had taken it off each spouse's 12,000 (4,000). Tax 2,619.80, was 3,194.80.
- `mn_2025_age_sub_taxable_ss_differs`: the age-65 cap is reduced by nontaxable benefits only
  (`social_security_basis: nontaxable`), 3,000 rather than the 4,000 received, leaving a subtraction of 850,
  the form's figure. Tax 385.20, was 430.68.

Both were worked again blind before they shipped.

Two questions from the same consumer are answered in the schema:

- When an income test is indexed, its threshold grows and a `share_phase_out` width does not. Maine is
  the only indexed test with a width, and its statute indexes the applicable amounts but not the 100,000 /
  50,000 denominators (36 M.R.S. 5122(2)(M-3)).
- `joint_income` speaks only to rules figured per person. Which return carries joint income when spouses
  file separately is outside it. Delaware's booklet says each separate return carries half. Georgia's and
  New Jersey's sources do not say.

## 2026-11-08: railroad Tier 1, Virginia's railroad exemption, Ohio's band base

**Railroad Tier 1.** The format did not say where Tier 1 benefits go. Federally, the social security
equivalent part of Tier 1 (Form RRB-1099) goes on the Social Security Benefits Worksheet, so Form 1040 line
6b is one taxable amount for both. 45 U.S.C. 231m bars state tax on every Railroad Retirement Act benefit.
The schema now says:
- For a state, Tier 1 is `railroad_retirement` income, never `social_security`.
- When a return has both, the federal taxable amount is split in proportion to the benefits received. No
  booklet prints a split: Colorado points to IRS Publication 915, which has none. The split matters only
  where a state taxes part of Social Security (CO for ages 55-64, CT, MN, MT, NM, RI, UT, VT, WV).
- `measure.minus_taxable_social_security` takes off all of line 6b. Virginia's AFAGI says "taxable Social
  Security and Tier 1 Railroad Benefits", and Oregon and New Jersey group Tier 1 with Social Security in
  their income tests. A relief in `minus_reliefs` that covers railroad income (Missouri) then counts only
  the railroad income outside line 6b, so Tier 1 comes off once.

Checks gain an optional input `railroad_tier1_sseb`. Two new cases combine Tier 1 with Social Security:
- Virginia: Tier 1, Tier 2 and Social Security on a joint return.
- Colorado, age 63: there the split decides the answer, because Tier 1's part is exempt in full while
  Social Security's part is held to 20,000.

**Virginia** had no railroad exemption in its projection, only a warning. It now exempts railroad
benefits in full, as every other state does (Schedule ADJ code 22 and Line 5).

**Ohio's band base.** When Ohio resumes indexing in 2027, the printed base of the 2.75% band is recomputed
as 1.27448% times the indexed start (R.C. 5747.02(A)(5) and (A)(2)). That is 332.00 at 26,050, so the base
grows in proportion to the start. This is in the indexing note and in the schema's description of `base`.
Ohio's 2026 schedule (332.00 base, no 3.125% band) had not been recorded as a later-year change. It is now
an approximation.
