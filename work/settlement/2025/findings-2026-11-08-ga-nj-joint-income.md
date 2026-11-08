# Findings 2026-11-08: Georgia and New Jersey, how income from a joint account is divided between spouses

Question: on a joint return, a relief figured per person covers interest, dividends, capital gains or rents. How is
income from a jointly held bank or brokerage account divided between the spouses for that relief?

| State | Answer | Where |
|---|---|---|
| GA | half_each (stated as a rule) | IT-511 PDF p.21 and p.24; Ga. Comp. R. & Regs. 560-7-4-.02(2) |
| NJ | half_each (shown in the Division's worked example; no rule states it) | GIT-1 & 2 (January 2026) p.26; NJ-1040 instructions PDF p.22-24 |

## Georgia: half to each spouse, stated as a rule

- 2025 IT-511 Booklet (sources/archive/2025/GA/2025_IT-511_Booklet_2026.02.16.pdf), PDF p.21 (printed p.21),
  Subtractions, item 1 "Retirement income":
  "The exclusion is available for the taxpayer and their spouse; however, each must qualify on a separate
  basis. If both spouses qualify, each spouse may claim the amounts above. Income from property that is
  jointly owned should be allocated to each taxpayer at 50% of the total value. Up to $5,000 of the maximum
  allowable exclusion may be earned income."
- Same booklet, PDF p.24 (printed p.24), Retirement Income Exclusion notes:
  "Income or losses should be allocated to the person who owns the item. If any item is held jointly, the income
  or loss should be allocated to each taxpayer at 50%."
- Regulation: Ga. Comp. R. & Regs. R. 560-7-4-.02, "Procedures Governing Retirement Income Exclusion",
  paragraph (2) (https://www.law.cornell.edu/regulations/georgia/Ga-Comp-R-Regs-R-560-7-4-.02, fetched
  2026-11-08): "In the case of a married couple filing jointly, each spouse shall if otherwise qualified be
  individually entitled ..."; "Taxpayers must qualify on a separate basis."; "One spouse may not use any income
  attributable to the other spouse in the calculation of his or her retirement exclusion."; "If property is
  jointly owned, income derived is allocated to each taxpayer at 50 percent of the total."
  (The tool returned the rule in excerpts, not the whole paragraph.)
- Citation note: the rule named in the question, 560-7-3-.03, is "Election to Pay Tax at the Pass-Through Entity
  Level" (https://www.law.cornell.edu/regulations/georgia/Ga-Comp-R-Regs-R-560-7-3-.03). It mentions the
  retirement exclusion only to say an electing entity cannot claim it. The joint-property rule is in 560-7-4-.02.
  O.C.G.A. 48-7-27 itself could not be fetched (Justia returned 403). The booklet and the regulation already
  answer the question.
- The couple cannot choose another split. Income in one spouse's name (an IRA, 401(k) or pension, an individual
  account, that spouse's wages) stays with that spouse ("allocated to the person who owns the item").
- Losses split the same way (p.24 "the income or loss"). Schedule 1 page 2 line 15 floors only the total at
  zero, so half of a joint net capital or rental loss reduces each spouse's other retirement income.
  (Side point, not part of the question.)
- Data: GA.record.json `cap_rule` for both retirement entries already says "Income from jointly owned property
  is allocated 50% to each spouse." The projection reliefs are `who.basis: each_person` with `cap_per: person`
  (35,000 for ages 62-64, 65,000 for 65 and older).
- Does it change tax in a projection? Yes. The cap is per person and the spouses' ages and own income
  differ, so the split changes the total exclusion.
  Example: joint return, spouse A 67 with 100,000 of IRA distributions in A's name, spouse B 63 with no income in
  B's name. A joint brokerage account pays 40,000 of interest, dividends and gains. No wages. Federal AGI 140,000.
  Standard deduction 24,000, flat rate 5.19%.
  - Half each (the rule): A 100,000 + 20,000 = 120,000, exclusion 65,000. B 20,000, exclusion 20,000.
    Total 85,000. Georgia AGI 55,000, taxable income 31,000, tax 1,608.90.
  - All to A: exclusion 65,000 + 0 = 65,000. Taxable 51,000, tax 2,646.90 (1,038.00 more).
  - All to B: exclusion 65,000 + 35,000 = 100,000. Taxable 16,000, tax 830.40 (778.50 less).
  Existing GA checks give no return-level interest, dividends or gains to a joint couple, so none tests this.
  The check schema holds interest, dividends and gains as return amounts with no person, so an engine evaluating
  `each_person` reliefs must split them half to each spouse for Georgia.

## New Jersey: one maximum per return, but only a qualifying spouse's income is excluded; joint-account income counts half to each in the Division's example

- Per person or per return? Both. NJ.projection.json `nj_unclaimed_exclusion` (and `nj_pension_exclusion`)
  has `who.basis: each_person`, min_age 62, with `cap_per: return` (100,000 joint). There is one shared maximum,
  but only income of a spouse who is 62 or older can use it:
  - NJ-1040 Instructions (sources/archive/2025/NJ/1040i.pdf), PDF p.22 (printed p.20), Line 28b: "If you
    are filing jointly and only one spouse is 62 or older, only the income of that spouse can be excluded. You
    cannot exclude the income of the spouse who is younger than 62."
  - Same, PDF p.23 Worksheet D and PDF p.24 Worksheet E: "Joint filers: If only one spouse is 62 or older, only
    the income of that spouse can be excluded."
  - GIT-1 & 2 (sources/archive/2025/NJ/git1_2.pdf), p.25, "Only One Spouse Qualifies for Exclusion", condition 3:
    "The exclusion is applied only to the income of the qualified (age 62 or older) spouse."
  So the split does not matter when both spouses are 62 or older: their income is pooled under one 100,000
  maximum. It does matter when one spouse is 62 or older and the other is not.
- How joint-account income is divided: the only source text is a worked example in GIT-1 & 2, p.25-26 (PDF p.26
  for the split itself):
  "A taxpayer (age 58) and their spouse (age 63) file a joint return for the tax year. They have a combined total
  income of $30,000. Spouse #1 receives a taxable pension of $18,000, and spouse #2 receives a taxable pension of
  $6,000. Interest from their joint savings account totals $4,000. Spouse #1 has wages of $500, and spouse #2 has
  wages of $1,500. ... ORIE – Unclaimed Pension Exclusion $ 3,500 ... only $3,500 of their combined total income
  belongs to the spouse who is age 63 ($1,500 wages and $2,000 interest). The balance belongs to spouse #1 ($500
  wages, $2,000 interest, and $18,000 pension)."
  The 4,000 of joint savings interest is divided 2,000 / 2,000. The publication never states this as a rule, and
  it does not say whether ownership or contribution could change it. No other archived NJ source mentions jointly
  held accounts (searched 1040i, GIT-1 & 2, njit6, njit7).
- Statute: N.J.S.A. 54A:6-15 (other retirement income). The text read
  (https://getpocketlaw.com/law/state_new_jersey/section-54a-6-15-other-retirement-income_06848c9636b6, a
  secondary copy; Justia, https://law.justia.com/codes/new-jersey/title-54a/section-54a-6-15/, returned 403)
  excludes income "when received in any tax year by a person aged 62 years or older". The fetch reported no
  wording about joint returns beyond the "married couple filing jointly" amounts, about whose income it is, or
  about jointly held property. The statute is silent on the split. N.J.S.A. 54A:6-10 is the pension, annuity and
  IRA exclusion. That income is always in one person's name, so the joint-account question does not arise
  there; it was not fetched.
- Data: NJ.record.json notes and the projection have nothing on joint-account income. The check schema holds
  interest, dividends and gains as return amounts. nj_2025_unclaimed_joint_earned_combined has both spouses 62
  or older (64 and 63), so the split does not matter there.
- Does it change tax in a projection? Yes, when exactly one spouse is 62 or older (the younger spouse not
  disabled), joint earned income is 3,000 or less, and line 27 is 150,000 or less.
  Example: joint return, spouse A 64, spouse B 60. No pensions, no wages. A joint brokerage account pays 50,000
  of interest and 30,000 of dividends. Line 27 is 80,000, so the maximum is 100,000 and line 28a is 0, leaving
  100,000 unclaimed. Regular exemptions are 2 x 1,000. Tax uses the Table B bands; under 100,000 the Tax Table
  gives these figures within a dollar or so.
  - Half each (the GIT-1 & 2 example): A's 40,000 is excluded. Taxable 80,000 - 40,000 - 2,000 = 38,000,
    tax about 595.
  - All to A: 80,000 excluded, taxable 0, tax 0 (about 595 less).
  - All to B: nothing excluded, taxable 78,000, tax about 1,575 (about 980 more).
  For a couple both 62 or older the same 80,000 is excluded in full under the shared 100,000 maximum, whatever
  the split.

## Answers

- GA: half_each. Stated in IT-511 PDF p.21 and p.24 and in Ga. Comp. R. & Regs. 560-7-4-.02(2). It changes tax
  whenever both spouses have joint-account income and different ages or different own retirement income
  against the per-person caps.
- NJ: half_each, but only from the Division's worked example (GIT-1 & 2 p.26, joint savings interest
  4,000 counted 2,000 to each spouse). No rule states it, and the statute is silent. The maximum is one amount
  per return, so the split changes tax only when exactly one spouse is 62 or older.
