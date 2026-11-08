# VA 2025 settlement

Readings A and B (round r3), settled 2026-11-07. `tools.compare`: 20 structured differences, 137
wording differences. Record built from reading B (its cites use PDF page numbers), with the changes
below. Sources: 2025 Form 760 instructions (43-page PDF) and the 2025 Form 760.

**Page numbers.** Cites use PDF page numbers (the PDF and the pypdf text). The printed page number
is 6 lower (PDF p41 = printed Page 35). The docling text skips blank pages, so its page markers
run 2 to 3 lower than the PDF from page 13 on. Reading A cited docling pages (its "p.13" for
exemptions is PDF p15, its "p.38" rate schedule is PDF p41), so B's cites were used.

## Structured differences (20)

| # | Field (compare key) | A | B | Settled | Source |
|---|---|---|---|---|---|
| 1 | `muni_interest.treatment` | other_states_taxed_own_exempt | other | **other_states_taxed_own_exempt** | PDF p23 Schedule ADJ Line 1 "Interest on Obligations of Other States ... not included in your Federal Adjusted Gross Income, which is taxable in Virginia" (an addition); PDF p25 code 20 subtracts "interest on Virginia state bonds or municipal obligations and gains from sales of those obligations". B cited only code 10 and missed Line 1. |
| 2-4 | Military basic pay (code 38) `income_test` (effect, measure.base, threshold.all) | dollar_for_dollar, other, 15000 | none (in cap_rule only) | **A's income_test kept** | PDF p26 code 38: "For every $1.00 of income over $15,000, the maximum subtraction is reduced by $1.00. If your basic military pay is $30,000 or more, you are not entitled to a subtraction." Measure is the basic pay itself, so `base: other` with `as_printed`. |
| 5-10 | Death benefit (code 49) `who.basis` (shows as 3 fields on each side because the entries were matched by basis) | return | each_person | **return** | PDF p26-27 code 49: "Allows a beneficiary taxpayer to subtract ..."; no age test, no per-person cap, no each-spouse rule. |
| 11-16 | Combat zone pay (code 30) `who.basis` (3 + 3 fields) | return | each_person | **return** | PDF p26 code 30: no age test, no cap, no each-spouse rule. |
| 17-20 | Retirement income previously taxed by another state (code 31) `who.basis` and `covers_unclear` (B's entry showed 4 one-sided fields because A's code 31 entry was matched against B's unemployment entry) | return, no covers_unclear | each_person, covers_unclear [ira_distribution, employer_plan_distribution, private_pension, public_pension_other_state] | **return; B's covers_unclear kept** | PDF p26 code 31: "retirement income received during the taxable year on which the contributions were taxed in another state"; no person-level test; "retirement income" leaves the kinds open, so `covers: other_income` with B's kinds in `covers_unclear`. VRS does not qualify (kept in not_covered). |

Rule used for 5-20: `who.basis` is `each_person` where the booklet prints an age test, a
per-person cap or an each-spouse rule (codes 38, 39, 60 and Line 5 say "each spouse can qualify";
the age deduction goes by each spouse's birth date), and `return` where it prints none (the
schema: "return when neither"). None of the three has a cap, so the choice changes no amount.

Decided from what the booklet prints: 1-4 (muni; code 38 income test) and the covers_unclear part
of 17-20. The basis items (5-20) were read against the booklet, which is silent on any per-person
rule; the schema's definition settled them.

## One-sided entries

- **Lottery prizes under 600 (code 24), B only: dropped.** Printed (PDF p26) but out of scope:
  not retirement, wage or investment income. Both readers left out the other minor Schedule ADJ
  subtractions (Holocaust assets, WOTC wages, land preservation, historic rehabilitation, eminent
  domain gain, student loan discharge, first-time home buyer accounts).
- A's code 31 and code 37 entries matched B's code 37 and code 24 entries by shape, so their
  wording differences are mismatches, not disagreements. Both readers have codes 31 and 37, and
  both are kept.
- `cap_rule` text present in only one reading (codes 44, 30, Line 5, Line 4 of U.S. obligations):
  kept where the booklet prints it.

## Added at settlement (neither reader)

- `head_of_household` in the standard deduction (8,750) and in the income-based age deduction
  threshold (50,000). PDF p15: "Fill in the Head of Household oval if your filing status is Single
  and you checked the Head of Household box on your federal return", so a head of household files
  Filing Status 1, whose amounts are 8,750 (PDF p17 Line 11) and 50,000 (PDF p16 worksheet line 9A;
  PDF p17).
- B's `indexing.standard_deduction.index` held the scheduled sunset text. Removed, because `index`
  is what a figure is indexed to. The sunset is in the record notes and the standard deduction
  condition, as the dispatch asked. Scheduled changes are tax-reference-data issue #2.

## Facts checked against a second line or document

- **Social Security: exempt.** Form 760 page 1 Line 5 "Social Security and equivalent Tier 1
  Railroad Retirement benefits if taxable on federal return" (a subtraction); PDF p17 Line 5. The
  age worksheet (PDF p16 line 7) and the spouse worksheet (PDF p18 line 15) also take it out.
- **Age deduction.** PDF p15 Line 4: born on or before 1961-01-01 may qualify; barred with the
  disability subtraction, the low-income credit, VEITC and the refundable VEITC; each spouse takes
  the age deduction or the disability subtraction ("whichever gives the greatest tax benefit", so
  `best_of_group`). PDF p17 gives the branches: on or before 1939-01-01, 12,000 each with no income
  test; 1939-01-02 to 1961-01-01, income-based, 12,000 reduced $1 per $1 of AFAGI over 50,000
  (single) or of joint AFAGI over 75,000 (all married, joint or separate). If both spouses claim,
  the joint deduction is computed first and split in half. PDF p16 worksheet lines 1-15 agree,
  including line 12 (number of claimants x 12,000) and line 15 (divide by 2). AFAGI is federal AGI
  adjusted for conformity, less taxable Social Security and Tier 1 (worksheet lines 2-8). PDF p25
  Line 5 confirms the disability/age choice from the other side.
- **Brackets.** PDF p41 schedule: 2% to 3,000; 60 + 3% over 3,000; 120 + 5% over 5,000; 720 +
  5.75% over 17,000. The worked example is 90,000 → 4,918. The printed tax amounts agree with the
  starts (3,000 x 2% = 60; 60 + 2,000 x 3% = 120; 120 + 12,000 x 5% = 720). One schedule for all
  statuses.
- **Standard deduction and exemptions.** PDF p17 Line 11 (8,750 / 17,500 / 8,750) agrees with
  PDF p7 What's New. PDF p15: 930 per You/Spouse/Dependent, 800 per 65-or-older/Blind box. These
  agree with the Form 760 page 1 Exemption Sections A ("X $930") and B ("X $800").
- **Military benefits (code 60).** PDF p28: 40,000 for 2025 and after, each spouse their own
  maximum.

## Projection choices

- Modelled: the rate schedule; the standard deduction, the personal exemption (per person) and the
  age-65 exemption (min_age 65); Social Security exempt; both age-deduction branches; military
  benefits (needs `pension_source`); municipal interest as other-states-taxed, own-exempt.
- Disability is not modelled, so the projection has no `best_of_group` or `cannot_combine_with`
  for the age deduction. The two age branches exclude each other by birth date.
- Not modelled, with warnings: disability, dependents and blind, Medal of Honor, railroad, code 31,
  the military and government wage subtractions, U.S. obligations, Virginia obligations, and the
  minor subtractions.
- Approximations:
  - the joint reduction of the age deduction (a per-person evaluation takes the excess twice:
    overstates tax by up to 690);
  - married-separate joint AFAGI;
  - AFAGI conformity adjustments;
  - the standard deduction held at its 2025 amounts past the scheduled sunset (understates tax
    from 2027);
  - itemizing;
  - the Spouse Tax Adjustment;
  - the filing threshold;
  - Treasury interest;
  - Virginia bond interest;
  - the edge of the age-65 test.

## Unsure

- `who.basis` for codes 30, 31 and 49. The booklet is silent and I applied the schema's "return
  when neither". A reviewer may prefer each_person for personal pay (combat zone). No amount
  changes either way.
- Code 31 `covers_unclear` lists four kinds that "retirement income" may include. The booklet names
  none of them.
- `head_of_household` amounts come from the Filing Status 1 mapping on PDF p15, not from a line
  that prints "head of household" next to a figure.
- How a consumer evaluates the income-based age deduction for a couple who both qualify. The
  approximation assumes a per-person evaluation. If the consumer already reduces the joint
  maximum, that entry does not apply.

## 2026-11-08: marker ids and indexing covers

- Marker ids: all 9 markers have an `id`. Each takes its first from_record id, so warning codes are unchanged.
- Indexing covers: `brackets`, `deductions`, `relief_caps` (reliefs.cap). Split `standard_deduction` (indexed false, not assumed) out of `deductions` for deductions:standard_deduction. Added `relief_income_tests` (indexed false, assumed) for reliefs.income_test (the income-based age deduction).
- Assumed resolved: the standard deduction is indexed false, no longer assumed (new entry `standard_deduction`). Instructions PDF p7 (printed Page 1), What's New, Increase in Standard Deduction: legislation set 8,750 / 17,500 'for Taxable Years 2025 and 2026', and the increase 'is scheduled to sunset after Taxable Year 2026 and revert to the standard deduction amounts that applied prior to Taxable Year 2019: $3,000 ... $6,000'. Amounts set by law for named years are not adjusted for inflation. The record's `indexing.standard_deduction` goes from not_stated to no with that cite, and the Indexing note says so; the projection's record sha256 is updated. This reverses the 2026-11-07 reading that the booklet states nothing; the sunset itself is still not modelled (tax-reference-data issue #2). The other VA entries stay assumed.

## 2026-11-08: indexing settled from statutes

Statute research (work/indexing/findings*.json) settled every projection indexing entry that was `assumed: true`:

- `brackets` (brackets): not indexed, Va. Code 58.1-320
- `personal_exemption` (deductions:personal_exemption): not indexed, Va. Code 58.1-322.03(2)(a)
- `age_65_exemption` (deductions:age_65_exemption): not indexed, Va. Code 58.1-322.03(2)(b)
- `relief_caps` (reliefs.cap): not indexed, Va. Code 58.1-322.03(5); 58.1-322.02(18)
- `relief_income_tests` (reliefs.income_test): not indexed, Va. Code 58.1-322.03(5)(b)
- `standard_deduction` (existing entry, indexed false): note added with the statute's schedule, Va. Code 58.1-322.03(1)(b)
- Record `indexing`: updated brackets -> no; added personal_exemption -> no; added age_65_exemption -> no; added age_deduction_born_by_1939 -> no; added age_deduction_income_based -> no; added military_benefits -> no.
- The record's existing `standard_deduction` entry (no, booklet cite) is kept. The booklet says the 8,750 / 17,500 amounts revert to 3,000 / 6,000 after 2026; the statute read now schedules 9,200 / 18,400 for 2027 and 9,300 / 18,600 for 2028-2029 before 3,000 / 6,000 from 2030 (a later amendment). The projection note gives the statute's schedule; the 2025 figures are unaffected.
