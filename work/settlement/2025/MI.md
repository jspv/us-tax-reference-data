

## Corrections from the hand-worked checks (2026-11-07)

- pre1946_public and pre1946_private removed from the best-of group: Form 4884 Section A gives public benefits in full plus private up to the remaining limit.
- public_pension_other_state added to the private-bucket reliefs (pre1946_private, born_1946_1966, Tier 2/3): Michigan's 'public' is Michigan and federal only, so another state's pension is private.
- Tier 2/3 min_age 67 dropped: the booklet counts 67 the day before the birthday; the birth-date bounds decide.
- Approximation added: the 1946-1966 cap is reduced by 75% of military/railroad retirement on Worksheet 3.3; the projection reduces it in full (overstates tax).
- Record: Worksheet 3.3 cites moved from PDF page 24 to 25.
- senior_investment_deduction: cap_reduced_by gains public_pension_other_state (line 28 subtracts everything claimed on line 27, which includes another state's pension as private).

- Main session, 2026-11-07 (format v1): `social_security_basis: taxable` set on the relief(s) whose cap Social Security reduces, stating what the cases already used.

## 2026-11-08: marker ids and indexing covers

- Marker ids given: first from_record id (warning code unchanged): `mi_ssa_exempt_1959_1964`, `mi_firepolice_public`, `mi_special_exemption`, `mi_active_duty_pay`, `mi_us_obligations_interest`.
- Indexing covers: `brackets` -> `brackets`; `deductions` -> `deductions`; `relief_caps` -> `reliefs.cap`; `private_retirement_maximum` -> `reliefs:pre1946_private.cap`, `reliefs:born_1946_1966.cap`.
- Split `relief_caps`: added `private_retirement_maximum` (indexed true) for the caps of `pre1946_private` and `born_1946_1966`; the Tier 2/3 standard deductions (20,000 / 40,000) and the senior investment deduction cap stay under `relief_caps` (assumed).
- RESOLVED: the private retirement maximum is indexed. Revenue Administrative Bulletin 2026-1, 'Pre-2012 Michigan Tax Treatment of Retirement Distributions': the maximum of MCL 206.30(1)(f)(iv) 'has been indexed for inflation each year since 2008'; 'Post-2011', Tier 1: 'the inflation-indexed private retirement maximum, which for tax year 2025 is $65,897 for a single filer and $131,794 for joint filers'; PA 4, Issue 2: for 2025 the 1946-1966 deduction is '75% of the inflation-adjusted private retirement maximum'. Record: indexing entries added for mi_pre1946_private, mi_ret_1946_1952, mi_ret_1953_1959 and mi_ret_1959_1966 (indexed yes, with that cite); projection record sha256 updated. The book prints the 14,688 senior investment cap and the 5,800 exemption 'for 2025' without saying they are adjusted, and nothing says for brackets, so those stay assumed.
- Warning codes unchanged (every id is the marker's first from_record id).

## 2026-11-08: indexing settled from statutes

- `brackets` (projection `brackets`): not_indexed, MCL 206.51(1)(b): flat 4.25% from 0. Record `brackets` added as no.
- `deductions` (projection `deductions`): indexed, MCL 206.30(7), (12)(c): US CPI on a state fiscal year basis plus 600, nearest 100. Record `mi_personal_exemption` added as yes.
- `relief_caps` (projection `reliefs.cap`): split. Its parts `reliefs:pre1946_private.cap` and `reliefs:born_1946_1966.cap` (indexed, MCL 206.30(1)(f)(iv), (10)) were already covered by the existing `private_retirement_maximum` entry (indexed true), so the entry is replaced by `tier2_standard_deduction_cap` (not_indexed, 206.30(9)(b)), `tier3_standard_deduction_cap` (not_indexed, 206.30(9)(e)) and `senior_investment_deduction_cap` (indexed, 206.30(1)(p)). Record `mi_tier2_std_deduction`, `mi_tier3_std_deduction` added as no, `mi_senior_investment_deduction` as yes; the existing booklet-cited yes entries for `mi_pre1946_private` and the 1946-1966 groups are kept (the finding agrees).
- Unsure: the `born_1946_1966` cap is 75% of the (f)(iv) maximum for 2025 and 100% from 2026 (206.30(10)(d)), a one-time step the `private_retirement_maximum` entry (indexed, CPI) does not show.
