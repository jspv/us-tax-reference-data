# Settlement: Connecticut (CT), tax year 2025

Date: 2026-11-07. Readings: `work/extract/2025/CT.r3.A.json`, `CT.r3.B.json` (round r3).
Sources: `sources/archive/2025/CT/` (2025 Form CT-1040 Instructions, Rev. 12/25, 28 pages; Form CT-1040).
Outputs: `data/states/2025/CT.record.json`, `data/states/2025/CT.projection.json`.

`uv run python -m tools.compare A B`: **104 structured differences**, 204 wording differences. They fall into
12 items. 81 lines (7 items) were decided by reading the booklet; 23 lines (5 items) were decided by
the brief's or the schema's rules once the booklet showed it had nothing more to say.

Validator, final run:

```
data/states/2025/CT.record.json: ok
data/states/2025/CT.projection.json: ok
```

## Structured differences

| # | Item (compare lines) | A | B | Settled | Source |
|---|---|---|---|---|---|
| 1 | `brackets.married_separate` (14) | copy of the single schedule | left out | Left out | PDF p. 20 prints one "Single or Married Filing Separately" schedule; the schema gives married_separate only when it has its own schedule |
| 2 | CHET deduction / CHET and ABLE reliefs (7 + 9 + 9) | CHET as base deduction `other`, no ABLE | CHET and ABLE as `all_income` subtraction reliefs, cap 5,000 / 10,000 | Both kept as base deductions `other`, amount = the limit, "lesser of contributions" in `condition` | p. 9 Line 48; p. 10 Line 48d. Same limits printed for both; they deduct contributions, they are not relief on a kind of income |
| 3 | `indexing` (2) | `all_other` only | adds `brackets`, `personal_exemption` as not_stated | `all_other` not_stated only | Booklet silent on indexing for every figure; brief rule 8 asks for entries only for figures the booklet speaks of |
| 4 | `ct_eitc` (5 + 7) | wages + self_employment, 0.40, investment-income test 11,950 removes | all_income, 0.40, credit_amount 250, no test | A's entry | p. 3 Line 20a; pp. 16-17 Schedule CT-EITC Line 2 ("cannot claim ... more than $11,950"), Line 9 (40%), Line 15a (250 only with a qualifying child, so not `credit_amount`) |
| 5 | `personal_tax_credit.income_test.effect` (1) | other | removes | `stepped`, 28 steps per status with the Table E decimal as `amount`; `credit_basis: tax` | p. 23 Table E; p. 19 Lines 7-10 |
| 6 | U.S. obligation interest and dividends (3 + 3 + 3) | one entry, interest + dividends | two entries | Two entries (B) | p. 8: Line 39 (interest) and Line 40 (qualifying-fund dividends, 50% asset test) are separate lines with separate conditions |
| 7 | `military_retirement.who.basis` (3 + 3) | return | each_person | return | p. 9 Line 44: no age test, cap or per-person limit; brief rule 5 (basis is whose age counts) |
| 8 | `railroad_retirement.who.basis` (3 + 3) | return | each_person | return | p. 9 Line 43: same reasoning |
| 9 | `teachers_pension_50.who.basis` (3 + 3) | return | each_person | return | p. 9 Line 45: same reasoning |
| 10 | `state_local_tax_refunds`, Line 42 (3) | not recorded | recorded (other_income) | Dropped | Printed (p. 9), but it removes a federal item (taxable state refunds), not relief on income a planner produces; the other such Schedule 1 modifications are also left out |
| 11 | Line 48b pension entry (9 + 10) | covers without public_pension_other_state (unclear), roth_conversion unclear, effect phase_out_rate | covers with public_pension_other_state, effect other | covers incl. public_pension_other_state (B); roth_conversion in covers_unclear (A); effect `stepped` with keep_share steps | p. 24 worksheet Line 2 takes 100% of federal Line 5b less only military, railroad and CT teachers' pay, so another state's pension is taken; p. 10 never mentions conversions; p. 25 Phase-Out Table |
| 12 | `ira_subtraction.income_test.effect` (1) | phase_out_rate | other | `stepped`, same keep_share steps (they multiply worksheet Line 2, 75% of Line 4b) | p. 25 Phase-Out Table; p. 24 Line 2 |

## Changes neither reading made (brief step 4, newer fields)

- `personal_exemption.phase_out.effect`: both said dollar_for_dollar; Table A (p. 19) drops 1,000 at the
  *start* of each 1,000 band (14,000 just over 30,000 single), so `stepped` with the printed amounts.
- `property_tax_credit.income_test.effect`: both said other; p. 27 table, so `stepped`. The printed
  decimal is the share removed (Line 67 = Line 65 x Line 66), so keep_share = 1 minus it
  (.15 -> .85 ... 1.00 -> 0). Arithmetic in the record notes.
- `personal_tax_credit` threshold moved from where the credit ends (64,500 / 100,500 / 52,500 / 78,500, both
  readers) to where the decimal first falls below .75 (18,800 / 30,000 / 15,000 / 24,000), as the other
  stepped tests use the start of the reduction.
- `ss_full_exempt.income_test.effect`: both said other; p. 8 makes the full subtraction apply only below
  the threshold, so `removes`. `ss_partial_exempt` stays `other` (its formula has no structured field).
- Pension and IRA steps: the Phase-Out Table bands are "greater than or equal to" / "less than or equal to"
  whole dollars, so each step's `over` is the printed upper end of the band below (over 74,999 = 75,000 or
  more). The other tables print "More Than" figures, used directly.
- B's `cannot_combine_with` between ss_partial and railroad dropped: Line 43 only excludes benefits "already
  subtracted on Line 41" (kept in railroad's conditions). A's mutual exclusion of the two SS branches kept.

## The teachers' pension conflict (worksheet vs example)

Both readers saw it. p. 10 (Line 48b text) and the p. 24 worksheet subtract "Connecticut teachers'
retirement pay" from Line 5b; Example 1 (p. 10) puts Anna's 30,000 of teachers' pay in her 68,000 Line 48b
subtraction and nothing on Line 45. Settled from the booklet: p. 10 says "Retired teachers may claim either
the teachers' pension subtraction modification or the pension and annuity subtraction modification (if their
federal adjusted gross income is below the applicable threshold) on the income they receive from the
Connecticut Teachers' Retirement System. Connecticut law does not allow a double benefit for the same
income", and worksheet Line 2 subtracts teachers' pay "as applicable". So teachers' pay leaves Line 48b only
when it is claimed on Line 45. Record: `teachers_pension_50` and `pension_annuity_subtraction` share
`best_of_group: ct_teachers_pension_choice` and name each other in `cannot_combine_with`; the 48b entry's
`not_covered` says teachers' pay is excluded only when claimed on Line 45. Example 2 (AGI over 100,000:
20,000 on Line 45, 0 on 48b) confirms the 50% is the one that helps above the phase-out.

## One-sided entries and checks

- Kept: ABLE (B; printed p. 10 Line 48d, same form as CHET). EITC investment-income test (A; p. 16).
- Dropped: Line 42 refunds (B), see item 10. `credit_amount: 250` on the EITC (B), conditional on a child.
- Checked against a second line or document: Social Security (p. 8 Line 41, p. 24 worksheet, form Line 41);
  pension/IRA thresholds (p. 10 text "less than $100,000 / $150,000" agrees with the p. 25 table's zero rows;
  p. 24 Line 1 test 75,000 / 100,000); military and railroad "fully exempt" (p. 10 against pp. 9 Lines 43-44);
  brackets for all three printed schedules against the worked examples on p. 20 (13,000 -> 335; 525,000 ->
  32,998; MFJ 22,500 -> 513 (512.50 before the booklet's rounding), 1,100,000 -> 69,490; HOH 20,000 -> 500, 825,000 -> 51,748); Table A, C, D, E and
  the property table re-read row by row from the pypdf text (the generated steps were printed and compared).
- No standard deduction, dependent exemption or age-65/blind amount is printed; only Table A.
- Other states' government pensions (brief rule 15a, added to the brief during this settlement): not named
  in the booklet; the 48b worksheet takes all of Line 5b, so they are in the same entry; no reciprocity rule
  printed. Record note added.

## Projection

Modelled: brackets (single, MFJ, HOH); Table A exemption with stepped phase-out; SS full exemption below the
threshold; Line 48b pension subtraction (stepped, `needs_input: pension_source`); IRA subtraction (stepped);
military and railroad exempt in full; Table E credit (`credit_basis: tax`, stepped); muni treatment; Tables C
and D as recapture start points. Not modelled (with warnings): SS partial rule (always), teachers' 50%
(has_pension), property tax credit (always), U.S. obligation interest/dividends, EITC, CHET/ABLE (never).
Approximations, with direction and size: C and D amounts (understates), IRA 75% share (understates),
SS above threshold (overstates), teachers (overstates), Roth conversions (overstates), Treasury interest
(overstates), property tax credit (overstates), QSS pension column (either).

## Unsure / for the owner

1. **Format gaps that make the projection knowingly wrong.** (a) No field for "a share of the covered income"
   on a subtraction: the IRA 75% and the teachers' 50% live only in text; the projection subtracts 100% of IRA
   income times the decimal (understates tax by about a quarter of the IRA subtraction at the marginal rate).
   (b) No way to express CT's partial SS rule (taxable benefits less 25% of the lesser of worksheet A and B);
   the projection taxes the full federal amount above 75,000 / 100,000 (about 2,000 a year too much for a
   couple with 60,000 of benefits). (c) Recapture has no step amounts; Tables C and D (up to 3,650 single,
   7,300 MFJ) are only in `as_printed`. Each needs a schema decision.
2. Table E steps use `amount` for the decimal (the credit rate in that band), not dollars; the schema's step
   `amount` is described as "the relief's amount there". A consumer must read it as a rate for a
   `credit_basis: tax` credit. keep_share (decimal / .75) would not be printed figures.
3. "Below the applicable threshold" for the teachers' choice: Example 1 uses under 75,000; I read it as the
   48b test itself (so the stepped phase-out applies to teachers' pay claimed on 48b). The booklet does not say
   whether a teacher can split the pension between Lines 45 and 48b.
4. Qualifying surviving spouse is not named in the pension worksheet or table; no QSS threshold or steps given.
5. The asterisk after "Connecticut AGI" on Tables C and D has no footnote in either converted text; the PDF
   page was not checked visually.
6. Table C/D effect kept as `phase_out_lower_brackets` (both readers); at the top of Table D the tax is close to,
   but not exactly, 6.99% of all income (my arithmetic: 50 short single, 100 MFJ, 200 HOH), so
   `flat_top_rate_on_all_income` and `full_over` were not used.


## 2026-11-07: thresholds that cut in at the figure

ss_full_exempt and the pension/IRA phase-out now carry applies_when at_or_over with the table's own figures (75,000, 77,500, ...), replacing step edges shifted down a dollar.

## 2026-11-07: format v1 adoption

Format: docs/decisions.md "2026-11-07: format for the first frozen schema". No figure changed; the dollar
effect on every modelled tax is 0 (all 22 earlier checks keep their expected figures and `verified`).

- **Table E (`personal_tax_credit`)**: each step's decimal moved from `steps[].amount` to `steps[].rate`
  (140 steps, record and projection; PDF page 23). A consumer can no longer read .75 as 75 cents. Record
  `cap_rule` and `as_printed` now say "rate"; unsure item 2 above is closed.
- **Shares (a format addition)**: `ira_subtraction` already had `share` 0.75 in both files (stale "no
  field" sentence removed from its `cap_rule`). `teachers_pension_50` gains `share` 0.5 in the record (PDF
  page 9, Line 45: "Subtract 50% of the income received from the Connecticut Teachers' Retirement System");
  record note 9 rewritten. The pension/annuity entry subtracts all of Line 5b (worksheet Line 2, PDF page 24),
  so it has no share. The teachers' relief stays a `not_modelled` marker in the projection: the inputs cannot
  tell a Teachers' Retirement System pension from another public pension (`needs_input` offers only source and
  contributory), so its approximation stays; `has_pension` is still the narrowest trigger.
- **Social Security partial rule (`ss_partial_exempt`)**: `warn_when` always -> `income_over`, federal AGI,
  75,000 single and MFS, 100,000 MFJ, QSS and HOH (the record's own figures). The rule applies at "$75,000 or
  more" / "$100,000 or more" (PDF page 24), but `income_over` is strictly over and has no `applies_when`, and
  the projection cannot add 74,999. So a household with federal AGI exactly 75,000 or 100,000 and Social
  Security gets no warning while the projection still taxes the full federal amount (the 1-dollar edge;
  `ct_2025_ss_full_exempt_at_threshold` sits on it and now carries no ss_partial warning). The marker's text
  says so. The tax approximation itself stays (deferred in decisions.md).
- **Approximations**: none removed (no new field makes one exact) and none added. Dollar examples added to the
  four sizes that had none: teachers' (Example 2, 1,150 a year), Roth conversions (1,052.50), Treasury interest
  (495), the qualifying surviving spouse column (2,468 apart).
- **Checks**: `--fix-warnings` dropped `state_rule_not_modelled:ss_partial_exempt` from 18 cases whose federal AGI is not over
  the figure (warnings only; inputs, expected, worked and source unchanged, so `verified`
  kept). Added `ct_2025_ss_partial_warning_over_threshold_mfj` (federal AGI 103,500, the warning fires; military
  pension keeps Connecticut AGI under Table C) and `ct_2025_personal_credit_mid_band_hoh` (Table E rate .60, the
  first head-of-household credit case). No case renamed or removed.

```
data/states/2025/CT.record.json: ok
data/states/2025/CT.projection.json: ok
CT: 24 case(s), ok
```

- Main session, 2026-11-07: the Social Security warning's `income_over` now has `applies_when: at_or_over` (new schema option), so a household exactly at 75,000 / 100,000 is warned, matching the booklet's 'or more'.

## 2026-11-07: partial Social Security (fields added within format 1)

Second pass, for the fields added within format 1 (docs/decisions.md "2026-11-07: `requires` for fields added
within format 1"): Connecticut's partial Social Security subtraction is now modelled.

- **Record**: `ss_partial_exempt.cap_rule` rewritten to quote the worksheet (PDF page 24, Lines A-F): Line A =
  federal worksheet Line 1 (gross benefits); Line B = federal worksheet Line 9 (Line 7 for married filing
  separately living with the spouse); Line C the lesser; Line D = Line C x 25% (.25), stated as share 0.25;
  Line E = federal worksheet Line 18; Line F = E - D, 0 if D >= E. One note added. The record schema has no
  field for the 25% share, so 0.25 sits in the entry's text with its cite; the validator finds the figure 0.25
  elsewhere in the record (the Phase-Out Table's keep_share), so the projection still adds no figure.
- **Projection**: new relief `ss_partial_exempt` (form subtraction, covers social_security, basis return),
  `applies_over` federal AGI at or over 75,000 (single, MFS) / 100,000 (MFJ, QSS, HOH), `keeps_taxable`
  {share 0.25, of_lesser_of [social_security_gross, federal_ss_worksheet_line_9]}, `requires` both.
  `ss_full_exempt` unchanged (removes at or over the same figures, so the two never overlap).
- **Removed**: the `not_modelled` marker for ss_partial_exempt (and its income_over warning) and the
  approximation "Social Security above the AGI threshold is taxed on the full federally taxable amount ...".
  No approximation added: the worksheet is computed exactly from the household's facts.
- **Dollar effect**: at or over the limits, Connecticut income falls by Line F. MFJ, federal AGI 100,000, 40,000
  of benefits (34,000 taxable): subtraction 24,000, tax 3,920.00 -> 2,628.00 (1,292.00 less). MFJ, federal AGI
  103,500 with a 30,000 military pension and 30,000 of benefits: subtraction 18,000, tax 2,526.75 -> 1,149.75
  (1,377.00 less; Table A exemption 16,000 returns at Connecticut AGI 55,500). Below the limits nothing changes.
- **A zero subtraction cannot occur** with a consistent federal worksheet: Line E (taxable benefits) is always at
  least half the lesser of Lines A and B (each branch of federal Lines 11-18 gives at least 0.5 x min(Line 1,
  Line 9)), so Line D (a quarter of it) is at most half of Line E and Line F is at least half of Line E. No case
  for "25% of the lesser at least the taxable amount" was written; the floor at 0 only guards bad inputs.
- **Checks**: reworked `ct_2025_ss_full_exempt_at_threshold` (now also tests ss_partial_exempt; Line A lesser;
  `verified` deleted). Renamed `ct_2025_ss_partial_warning_over_threshold_mfj` to
  `ct_2025_ss_partial_over_threshold_mfj` (no warning any more; reworked, Line A lesser, `verified` deleted; old
  file deleted). Added `ct_2025_ss_partial_line_b_lesser_single` (Line B 46,000 < Line A 50,000, with 2,000 of
  Connecticut municipal interest that enters only through Line B) and `ct_2025_ss_partial_below_threshold_single`
  (federal AGI 73,075: full exemption, partial 0). `--fix-warnings` dropped `state_rule_not_modelled:ss_partial_exempt`
  from five cases without Social Security over the limits (ira_phased_mfj, military_retirement,
  pension_at_threshold_single, pension_phased_mfj, personal_credit_last_band_mfj): warnings only, `verified` kept.
- **Unsure**: a married-separate filer who lived apart all year uses Line 9 (base 25,000), not Line 7; the
  inputs do not say whether the spouses lived together, so a consumer has to assume (no MFS case written).

- Main session, 2026-11-07: approximation added for married separate filers (taken to have lived with the spouse, Line 7 with no base).
- Main session, 2026-11-07: the record schema now mirrors `keeps_taxable` and `applies_over`; `ss_partial_exempt` holds them in the record, so the 0.25 is recorded with its own cite instead of passing on a coincidence.

## 2026-11-08: marker ids and indexing covers

- Marker ids given: first from_record id (warning code unchanged): `teachers_pension_50`, `property_tax_credit`, `us_government_interest`, `ct_eitc`, `chet_contributions`.
- Indexing covers: `brackets` -> `brackets`; `deductions` -> `deductions`; `relief_thresholds` -> `reliefs.income_test`, `reliefs.applies_over`; `recapture` -> `recapture`.
- `relief_thresholds` covers the income tests and the partial Social Security subtraction's `applies_over`.
- Every `assumed` answer was checked again against the archived sources (searched for indexed, inflation, cost-of-living, adjusted annually, each year, CPI, fixed): none says, so all stay `assumed: true`.
- Warning codes unchanged (every id is the marker's first from_record id).

## 2026-11-08: indexing settled from statutes

- `brackets` (projection `brackets`): not_indexed, Conn. Gen. Stat. 12-700(a)(10). Record `brackets` added as no.
- `deductions` (projection `deductions`): not_indexed, Conn. Gen. Stat. 12-702(a)(2)(I) and parallels. Record `personal_exemption` added as no.
- `relief_thresholds` (projection `reliefs.income_test`, `reliefs.applies_over`): not_indexed, Conn. Gen. Stat. 12-701(a)(20)(B)(iii) and the parallel pension/annuity and IRA subtractions; 12-703(a)(2)(I). Record `ss_full_exempt`, `ss_partial_exempt`, `pension_annuity_subtraction`, `ira_subtraction`, `personal_tax_credit` added as no.
- `recapture` (projection `recapture`): not_indexed, Conn. Gen. Stat. 12-700(a)(10)(A)(ii)-(v) and (B)-(E). Record entry added with figure `recapture` (the record recapture rules have no id).
- The researcher searched all of chapter 229 for inflation, consumer price index, cost of living and indexed: none.
