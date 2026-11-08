# Findings 2026-11-08: Delaware joint-account income; the federal senior deduction in states starting from federal taxable income

## Delaware: income from a joint account counts half to each spouse

- 2025 PIT-RES Instructions (sources/archive/2025/DE/PIT-RES_Instructions_2025-01.pdf), PDF p.5, Filing Status 3 or 4:
  "you must each report your own income, personal credits, deductions, and one-half of the income derived from
  securities, bank accounts, real estate, etc., which are titled or registered in joint names."
- Same, PDF p.6, Line 6 example: joint bank and mutual fund accounts earn 5,000 interest, 1,000 dividends,
  3,000 capital gains; "The income from these joint accounts would be split equally between the two taxpayers";
  the combined exclusion is 17,000 (12,500 + 4,500).
- 30 Del. C. 1106(b)(3)f.1.B (https://delcode.delaware.gov/title30/c011/sc02/index.html): "eligible retirement
  income received by spouses as joint tenants with right of survivorship or as tenants by the entirety is deemed
  to have been received 1/2 by each."
- The couple cannot choose another split. Income in one spouse's name (IRA, 401(k), pension, an individual
  account) stays with that spouse.
- Why it matters: the 12,500 cap and the age-60 test are per spouse. Giving all joint income to one spouse gives
  12,500 instead of 17,000 in the booklet's example, and with spouses aged 66 and 57, 4,000 of joint interest gives
  a 2,000 exclusion, not 4,000 or 0.
- The existing checks are right (`de_2025_joint_both_60_shared_income` splits half each).
- Not checked: a 3-year Delaware residence requirement for the exclusion (1106(b)(3)f.4, 83 Del. Laws c. 338);
  the 2025 booklet does not mention it.

## Federal senior deduction (P.L. 119-21 section 70103; Form 1040 line 13b via Schedule 1-A)

| State | Answer | Source |
|---|---|---|
| CO | follows | Book104_2025 PDF p.5, p.8: "Colorado income tax is based on your federal taxable income, which has already considered your deductions"; Line 1 is 1040 line 15; the Line 4 addback uses line 12e only. Colorado State Auditor report (2026), PDF p.42: "the new bonus deduction for seniors will automatically apply to Colorado taxable income." |
| IA | follows | 4435 Expanded Instructions PDF p.3: Line 1f "does not directly affect the calculation of Iowa taxable income as the deduction is already included in your federal taxable income." Added back only inside the low-income exemption, alternate tax, tax reduction and health insurance deduction computations (p.3, p.9). |
| MT | follows | Form 2 Instructions PDF p.13: the Schedule 1-A deductions, including "the enhanced deduction for seniors, are included in the calculation of Montana taxable income." |
| ND | follows | 2025 booklet PDF p.4: North Dakota "perpetually conforms to the computation of federal taxable income ... with an additional $6,000 for some seniors." |
| NM | added_back (in effect) | PIT-1 starts from federal AGI (line 9) and subtracts only the "Federal standard or itemized deduction amount (from federal Form 1040, line 12" (PIT-1 PDF p.1; instructions PDF p.25). Nothing brings in line 13b, so New Mexico income equals federal taxable income plus the line 13 deductions. |
| SC | added_back | SC1040 Instructions PDF p.3: conforms to the IRC "as amended through December 31, 2024"; PDF p.7 Line e: "Add back any federal deductions resulting from IRC sections that South Carolina does not adopt." SCDOR Information Letter #26-4 (Revised), Jan 30 2026, lists "2. Senior Deduction" among the 2025 adjustments (https://dor.sc.gov/sites/dor/files/policies/IL26-4(revised).pdf). From 2026 South Carolina starts from federal AGI (Act 110; Information Letter #26-20). |
