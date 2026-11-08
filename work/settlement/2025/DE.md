# Settlement: Delaware, tax year 2025

- Readings: `work/extract/2025/DE.r5.A.json`, `work/extract/2025/DE.r5.B.json` (round r5)
- Sources: `sources/archive/2025/DE/`: 2025 PIT-RES Resident Instructions (instructions PDF), 2025 Form
  PIT-RES, Personal Income Tax FAQs (revenue.delaware.gov), and Delaware Code Title 30 Chapter 11
  Subchapter I (delcode.delaware.gov, `index.page.txt`, fetched 2026-11-07 for §1102)
- Outputs: `data/states/2025/DE.record.json`, `data/states/2025/DE.projection.json`
- Settled: 2026-11-07

## Comparison

`uv run python -m tools.compare` reported **73 structured differences** (127 wording differences). They
come down to nine disagreements:

| # | Lines | Field | A | B | Source | Settled |
|---|---|---|---|---|---|---|
| 1 | 6 | `base.deductions`: 529 contribution exclusion | `other` deduction, 1,000 / 2,000 | notes only | Instr p.7 Line 8b: a subtraction for contributions, capped, with an AGI limit | **dropped** (it isn't a standard deduction, an exemption or retirement relief), kept in notes |
| 2 | 6 | `base.deductions`: ABLE contribution exclusion | `other` deduction, 5,000 / 10,000 | notes only | Instr p.7 Line 8b | **dropped**, same reason |
| 3 | 4 | Personal credits, Line 27a | credit 110, `each_person` | notes only | Instr p.8 Line 27a "a joint couple with no dependents ... enter $220"; Form p.2 "Enter number of exemptions x $110" | **kept** (A) as `de_personal_credit`. Delaware has no exemption deduction and uses this credit instead. |
| 4 | 1 | Higher-education exclusion `covers_unclear` | `[roth_conversion]` | none | Instr p.7: the distribution must be "used in the same tax year to pay for books, tuition or fees" | **dropped**. Converted money goes into a Roth, so it can't be the amount used to pay tuition. |
| 5 | 3 | Interest on U.S. obligations, Line 5 | notes only | `exempt_in_full`, `interest` | Instr p.5 Line 5: "exempt from Delaware tax" | **kept** (B) |
| 6 | 6 | Social Security/RR relief: form and `who.basis` | subtraction, `each_person` | `exempt_in_full`, `return` | Instr p.7 Line 8a subtracts "the total of any taxable payments". It has no cap and tests no person. | **`exempt_in_full`, `each_person`**. Each benefit belongs to one person. Without a cap the basis changes nothing. |
| 7 | 32 | Line 11, persons 60 or over or disabled | two entries: single/separate (2,000, `each_person`, min 60) and joint (4,000, `return`, both spouses) | one entry, `return`, min 60, caps by status | Instr p.7 Line 11 worksheet: two columns with different tests. Single/separate: "Were you at least 60 ... or totally and permanently disabled", earned income "less than $2,500", "Is Line 10 $10,000 or less?" Joint: "Were both spouses at least 60", combined earned income "less than $5,000", "Is Line 10 $20,000 or less?" | **A's two entries** (brief: one entry per branch, each with its own conditions) |
| 8 | 14 | 60-plus pension exclusion: `annuity` | in `covers` | in `covers_unclear` | Instr p.6 names "pension" and lists eligible retirement income (dividends, gains, interest, net rental income, IRC 4974 plans: IRA, 401(k), Keogh, 457). Annuities aren't named. | **`covers_unclear`** (B) |
| 9 | 1 | Under-60 non-military exclusion: `covers_unclear` | without `annuity` | with `annuity` | Instr p.6 doesn't name annuities | **with `annuity`** (B) |

Decided from the booklet: rows 3, 5, 7, 8 and 9, which are **54 of the 73 lines**. Rows 1 and 2 (12 lines)
were decided by the extraction brief's scope, though the booklet prints both. Rows 4 and 6 (7 lines) are
judgement calls that the booklet's wording supports but doesn't state.

## The five facts to settle (with quotes)

1. **Another state's government pension, including a New York State pension.** It goes in `covers`, as
   `public_pension_other_state`, in the same entries as Delaware's own government pensions, federal pensions
   and private pensions. The quote is Instr p.6, Line 6: "Amounts received as pensions from employers
   (including pensions of a deceased taxpayer) may qualify for an exclusion from Delaware taxable income,
   subject to the limitations described below." The FAQ says: "As a resident of Delaware, the amount of
   your pension and 401K income that is taxable for federal purposes is also taxable in Delaware. However,
   persons 60 years of age or older are entitled to a pension exclusion of up to $12,500 ...". No source
   names New York or any other state. The rule is read from the missing Delaware-only limit, the way
   Maryland was settled. Both readers had it in `covers_unclear`.
   **A Delaware resident with a New York State pension** pays Delaware tax on it at Delaware rates, less
   the Line 6 exclusion. At 60 or over the exclusion is the lesser of 12,500 and pension plus eligible
   retirement income. Under 60 it is the lesser of 2,000 and the pension. `paying_states` isn't used,
   because the rule doesn't depend on which state pays.
2. **Delaware's own government pensions and federal pensions.** They get the same Line 6 entries, on the
   same quote. The booklet doesn't separate public from private pensions. The one split by source is the
   United States military pension under 60: "IF YOU WERE UNDER 60 on December 31, 2025 and retired from
   the United States military and received pension income during the year, your exclusion equals $12,500
   or the amount of your pension, whichever is less" (p.6). Form PIT-RES p.1 Line 6 has a box for it
   ("Column B if You had a Military Pension"). At 60 or over, military pensions are in the 60-plus entry's
   `covers`. Both readers had them as unclear. The worksheet's "1. Amount of pension" has no exception,
   and the under-60 text calls military retirement "your pension".
3. **Private pensions, IRA and employer-plan distributions, Roth conversions.**
   - Private pensions are covered in every branch.
   - At 60 or over, IRA, 401(k), Keogh and 457 distributions are covered as "eligible retirement income
     includes dividends, capital gains net of capital losses, interest, net rental income from real
     property and qualified retirement plans (IRC Sec. 4974), such as IRA, 401(k), Keogh plans, and
     government deferred compensation plans (IRC Sec. 457)" (p.6). They share the one 12,500 cap per
     person.
   - Under 60, IRA and 401(k) distributions are unclear, because the text says only "you receive a
     non-military pension, your exclusion equals $2,000 or the amount of your pension".
   - Roth conversions aren't mentioned in any source, so they are in `covers_unclear` everywhere.
   - Early distributions don't qualify: "If the distribution code listed in Box 7 of your 1099 R is a 1
     (one), or if you were assessed an early withdrawal penalty ... that distribution DOES NOT qualify for
     the pension exclusion" (p.6).
4. **Social Security: exempt.** Instr p.7 Line 8a says: "Social Security and Railroad Retirement benefits
   are not taxable in Delaware and, therefore, should not be included in taxable income. Enter on Line 8a
   the total of any taxable payments included on Line 1." Three other places confirm it. The p.3 Persons
   60 or Over Checklist says "Social Security and Railroad retirement benefits are excluded from Delaware
   taxable income". The FAQ says the same. Form PIT-RES p.1 has the Line 8a label "TAXABLE SOCIAL
   SECURITY/RR RETIREMENT BENEFITS".
5. **Brackets, standard deduction, exemptions.**
   - **Brackets.** Neither reader recorded any, because the booklet points to "the tax table" (Line 23
     under $60,000) and "the tax schedule at the end of the tax table" ($60,000 or more), Instr p.8 Line
     24, and neither is in the PDF. They are taken from **30 Del. C. §1102(a)(14)**: "For taxable years
     beginning after December 31, 2013, the amount of tax shall be determined as follows: 2.2% of taxable
     income in excess of $2,000 but not in excess of $5,000; 3.9% ... $5,000 ... $10,000; 4.8% ... $10,000
     ... $20,000; 5.2% ... $20,000 ... $25,000; 5.55% ... $25,000 ... $60,000; and 6.6% of taxable income
     in excess of $60,000."
   - Recorded schedule: 0 from 0, 2.2% from 2,000, 3.9% from 5,000, 4.8% from 10,000, 5.2% from 20,000,
     5.55% from 25,000, 6.6% from 60,000. It is one schedule for every filing status, because the statute
     prints no status split.
   - §1102(d)(1) says the Director's tables "shall be computed on the basis of the rates prescribed by
     subsection (a)".
   - The agency's own figures match. The FAQ says "a graduated tax rate ranging from 2.2% to 5.55% for
     income under $60,000, and 6.60% for income of $60,000 or over", and its Bonds answer says "The maximum
     income tax rate is 6.60% on income of $60,000 or over". Line 24's split at 60,000 also matches.
     Instr p.5 ("separate returns ... will be advantageous if both spouses have Delaware adjusted gross
     income in excess of $9,400") fits a single schedule that joint filers don't get doubled.
   - The intermediate band starts (5,000, 10,000, 20,000, 25,000) are printed only in the statute. The
     booklet prints no tax table rows to check them against.
   - **Standard deduction.** Instr p.8 Line 20a: 3,250 for statuses 1, 3 and 5, and 6,500 for status 2.
     Status 4 gets 3,250 in each column. This was checked against Form PIT-RES p.2 Line 20 ("Filing
     Statuses 1, 3, & 5 enter $3250 ... Filing Status 2 enter $6500").
   - **Additional standard deduction** (Line 21; form p.2): 2,500 per box for 65 or over and for blind,
     "a maximum of $5,000 per individual", allowed only with the standard deduction.
   - **No exemption deduction.** Delaware gives personal credits instead: 110 per exemption (Line 27a)
     and 110 more at 60 or over (Line 27b, also on the p.3 checklist).

## One-sided entries and other changes

- Covered in the table: the personal credit (kept), U.S. obligations interest (kept), 529 and ABLE
  (dropped), and the higher-education `roth_conversion` (dropped).
- **`cannot_combine_with` on the three pension branches** (B only): kept on all three. Instr p.6 says
  "Each taxpayer may receive ONLY ONE pension exclusion, even if he or she is receiving more than one
  pension or other retirement distribution."
- **A's "exclusion available only if the person receives pension income"** (60-plus entry): dropped. The
  booklet's own example contradicts it: "The secondary taxpayer received no pension income ... the
  secondary taxpayer is entitled to a pension exclusion of $4,500" (p.6).
- **The joint-account split** (B's `cap_rule`) is kept. Income from joint accounts "would be split equally
  between the two taxpayers" (p.6 example).
- **`qualifying_surviving_spouse: 3250`** was added to the standard deduction. The form's filing status 1
  is "Single, Divorced, Widow(er)", and Instr p.5 says "If you were single on December 31, 2025 ... use
  Filing Status 1."
- **Line 11 head of household**: neither worksheet column names it, so it is left out and noted.

## Projection choices

- The pension exclusion has three entries, as in the record.
  - The two under-60 entries carry `needs_input: ["pension_source"]`, because military pensions get
    12,500 there and other pensions get 2,000.
  - The 60-plus entry doesn't need it, because every pension kind is treated the same there.
  - The 60-plus entry's `covers` also takes interest, dividends, gains and rental income, which are inside
    the same 12,500.
- Personal credits are modelled as `credit_amount` 110 `each_person`, plus 110 at 60 or over. The
  dependent part is in `not_modelled` (`has_dependents`). No earlier projection uses `credit_amount`, so
  the engine's handling of a fixed per-person credit should be checked.
- Line 11 is in `not_modelled` with `warn_when: never`, because it can't change the tax of a filer who
  qualifies by age. A single filer aged 60 with a Line 10 of 10,000 owes 134.25 before credits, and the
  credits are 220. A joint couple both aged 60 with a Line 10 of 20,000 owes 429, and the credits are 440.
  It can matter only for a disabled filer under 60.
- Approximations, each with its direction:
  - the standard deduction is always taken;
  - Roth conversions and annuities are left out of the 60-plus entry;
  - IRA, 401(k) and annuities are left out under 60;
  - the early-distribution test is not applied;
  - joint-account attribution may differ from the booklet's equal split;
  - own-state municipal bonds are treated as other-state;
  - Treasury interest is taxed;
  - the other-state tax credit is not modelled;
  - the lump-sum separate tax is not used;
  - the statute's schedule is used in place of the table.
- Indexing: brackets, deductions, relief caps and credits are all `indexed: false, assumed: true`. Neither
  the booklet nor §1102 says anything about indexing.

## Unsure

- The statute paragraph as fetched, §1102(a)(14), reads "after December 31, 2013" with no end date. The
  dispatch described it as "before 2026", but no end date appears in the fetched text. It covers 2025
  either way.
- `public_pension_other_state` and the 60-plus `military_pension` are read from general wording ("pensions
  from employers"; "Amount of pension"). No sentence names another state's pension or a military pension
  at 60 or over.
- Under 60, the sentence "an early distribution from an IRA ... does not qualify for the pension
  exclusion" suggests that a non-early IRA distribution (for example at 59½, or under a code 2 exception)
  may qualify. This was left in `covers_unclear`.
- No table rows could be checked against the statute's bands, because the tax table isn't in the
  sources.

## 2026-11-08: marker ids and indexing covers

- Marker ids given: first from_record id (warning code unchanged): `de_line11_single_separate`, `de_higher_education_exclusion`, `de_us_obligations_interest`, `de_additional_standard_blind`, `de_personal_credit`.
- Indexing covers: `brackets` -> `brackets`; `deductions` -> `deductions`; `relief_caps` -> `reliefs.cap`; `credits` -> `reliefs.credit_amount`.
- Every `assumed` answer was checked again against the archived sources (searched for indexed, inflation, cost-of-living, adjusted annually, each year, CPI, fixed): none says, so all stay `assumed: true`.
- Warning codes unchanged (every id is the marker's first from_record id).

## 2026-11-08: indexing settled from statutes

- `brackets` (projection `brackets`): not_indexed, 30 Del. C. 1102(a)(14). Record `brackets` added as no.
- `deductions` (projection `deductions`): not_indexed, 30 Del. C. 1108(a)(3), (b). Record `de_standard_deduction`, `de_additional_standard_65` added as no.
- `relief_caps` (projection `reliefs.cap`): split, replaced by `pension_cap_under60_nonmilitary` (`reliefs:de_pension_excl_under60_nonmilitary.cap`, not_indexed, 1106(b)(3)b.1.A), `pension_cap_under60_military` (`reliefs:de_pension_excl_under60_military.cap`, scheduled 12,500 through 2026, 15,000 2027, 20,000 2028, 25,000 from 2029, 1106(b)(3)b.-e.; indexed false with the schedule in the note) and `pension_cap_60_plus` (`reliefs:de_pension_excl_60_plus.cap`, not_indexed, 1106(b)(3)b.2). Record entries added for all three.
- `credits` (projection `reliefs.credit_amount`): not_indexed, 30 Del. C. 1110(b). Record `de_personal_credit`, `de_additional_personal_credit_60` added as no.
- Unsure: `de_pension_excl_60_plus` covers military pensions too; from 2027 the statute gives a military pension the greater of 12,500 and the military schedule. The projection has one 12,500 cap and grows nothing; the note says so.
