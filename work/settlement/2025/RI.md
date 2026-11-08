# Settlement: Rhode Island (RI), tax year 2025

Date: 2026-11-07. Readings: `work/extract/2025/RI.r6.A.json`, `RI.r6.B.json` (round r6).
Sources: `sources/archive/2025/RI/`: 2025 RI-1040 instructions (13 PDF pages, I-1 to I-13, Revised 11/2025);
Retirement Income Tax Guide, Publication 2026-01 (issued February 2026, tax year 2025); and three files the
readers did not have: resident 2025 RI Schedule M, the Taxable Social Security Income Worksheet (booklet
page 18), ADV 2025-20 (H.R. 1 decoupling). Added after the first settlement, same date: 2025 Tax Rate Schedule and
Worksheets (one page, marked DRAFT). The file named `2025 1041 Schedule M` is the fiduciary version and
was used for nothing. Outputs: `data/states/2025/RI.record.json`, `data/states/2025/RI.projection.json`.

`uv run python -m tools.compare A B`: **18 structured differences**, 72 wording differences. They fall into 4
items. 6 lines (3 items) were decided by reading the booklet; 12 lines (1 item) by the schema's rule once the
booklet showed one schedule for every status.

Validator, final run:

```
data/states/2025/RI.record.json: ok
data/states/2025/RI.projection.json: ok
```

## Structured differences

| # | Item (compare lines) | A | B | Settled | Source |
|---|---|---|---|---|---|
| 1 | Pension limit, joint and qualifying widow(er) (2) | 133500 | 133750 | 133750 | Instructions PDF p.10 line 1t; worksheet line 6; below |
| 2 | `social_security.treatment` (1) | exempt | relief | relief | The schema's `exempt` is for a subtraction line with no conditions that matter; worksheet lines 5 and 7 end "Otherwise, STOP, you are not eligible for this modification" |
| 3 | `phase_out.measure.base` on the three deductions (3) | state_agi | other | state_agi | PDF p.4: line 3, "Modified Federal Adjusted Gross Income", is line 1 combined with RI modifications |
| 4 | `brackets.married_separate`, `head_of_household` (12) | copies of the schedule | left out | Left out | PDF p.13 worksheet: "Use for all filing status types"; the schema gives them only when they have their own schedule |

## The points flagged for this state

**Joint limit, 133,750 or 133,500: settled 133,750 for both tests.**
- Pension, instructions PDF p.10 line 1t: "Is your Federal AGI less than or equal to the amount listed below for
  your filing status? Single $107,000 / Married Joint $133,750 / Qualifying Widow(er) $133,750 / Married Separate
  $107,000 / Head of Household $107,000".
- Social Security, worksheet line 6: "Single or head of household - $107,000 / Married filing separately - $107,000 /
  Married filing jointly or qualifying widow(er) - $133,750".
- Guide PDF p.14: "married filing jointly, or qualifying widow, or qualifying widower  $133,500 or less"; PDF p.16:
  "married filing jointly or qualifying widow - $133,500" (also pp.18-25).
- The form and the worksheet agree with each other; only the Guide differs. The Guide defers to them, PDF p.14: "when you
  file your return, check the most current version of the Rhode Island Form RI-1040 and instructions to make sure
  you are using the correct income limits". The statute it prints, PDF p.28 (c)(9)(vi), makes the pension limits equal
  the Social Security limits, which the form does. Corroboration only: the law's starting figures are 80,000 and
  100,000 (PDF p.29), and 107,000 x 100,000 / 80,000 = 133,750 exactly. Both readers took 133,500 for Social
  Security, without the worksheet; that was not a compare difference but it is changed.

**Boundary, settled per test.** Social Security: worksheet line 7 "less than the filing status amount", Guide
"below" (PDF p.16), statute "less than" (PDF p.29): `applies_when: at_or_over`. Pension: line 1t "less than or
equal to", Guide table "or less" (PDF p.14), against Guide "below" (PDF p.4) and statute "less than" (PDF p.27):
from the form's own question, the default `over`. The difference is exactly one income figure; an approximation says so.
Both limits are cliffs (`removes`): one dollar over loses the whole relief.

**Age test: one test, stated two ways.** Line 1t: "Were you or your spouse (if applicable) born on or before March 1,
1959?"; worksheet line 5: "Were either you or your spouse born on or before 03/01/1959?"; both instruction lines
open "For those taxpayers who have reached full retirement age"; Guide PDF p.12 prints the table (1959: 66 and ten
months; 1960 or later: 67). By arithmetic, which no source prints: 66 and ten months from March 1, 1959 is January 1,
2026, and a person reaches an age the day before the birthday (the Guide's January 1 note reflects this), so that
person reaches it on December 31, 2025; a person born March 2, 1959 reaches it in 2026. So the printed date is the
full-retirement-age test applied to tax year 2025, and it will not be the same date next year. The statute says
"attained the age used for calculating full or unreduced Social Security retirement benefits" (PDF pp.27, 29). The
record keeps the printed date in `born_on_or_before`, on both reliefs, with the table in `other_conditions`.
B's note that no March 1, 1959 test exists for Social Security is out of date: the worksheet prints it.

**IRAs: not covered, by name.** Guide PDF p.5: "No income from a traditional IRA, Roth IRA, SEP-IRA, or any other type
of IRA qualifies"; instructions PDF p.10: "should NOT include any amounts for IRAs listed on line 4b". Not in `covers`
of any relief, and in `not_covered`. Guide example 3 (PDF p.10): plan money moved into an IRA gets nothing when
drawn from the IRA, so an IRA rollover can lose the relief for good.

**Standard deduction and exemption worksheets: from a page marked DRAFT.** Instructions PDF pp.4, 5: "However, if line 3 is more
than $254,250 see the Exemption Worksheet on the inside of the back cover to compute your exemption amount." The
archived instructions are the 13 instruction pages only. The worksheets are in `2025 Tax Rate and Worksheets_d.pdf`
(address folder 2025-10), fetched after the first settlement. Both worksheets, same steps:
- Line 3 "Is the amount on line 2 more than $254,250?" No: the full amount.
- Line 5 "Subtract line 4 from line 2. If the result is more than $29,000, STOP HERE." The amount is zero.
- Line 6 "Divide line 5 by $7,250. If the result is not a whole number, increase it to the next higher whole number".
- Line 7: 1, 0.8000; 2, 0.6000; 3, 0.4000; 4, 0.2000. Line 8 multiplies line 1 by line 7.

So over 254,250 keep 80%; over 261,500, 60%; over 268,750, 40%; over 276,000, 20%; over 283,250, nothing. Exactly at an
edge stays in the band below (7,250 exactly gives 1), which `over` gives.

*Is DRAFT printed?* Yes. "DRAFT" and "10/01/2025" run across the page as a large diagonal watermark. I rendered the page
and looked at it. It is a PDF watermark layer with view and print both on, so it shows on screen and on paper, over the
Standard Deduction Worksheet and into the Exemption Worksheet. The file's own dates are 2025-10-01 and the address folder
is 2025-10, while the final instructions are Revised 11/2025, so the instructions came later.

*Figures both print, all equal:* standard deduction "$10,900 / $21,800 / $21,800 / $10,900 / $16,350"; "Multiply $5,100 by the
total number of exemptions"; "$254,250"; schedule 79,900, 181,650, 3.75%, 4.75%, 5.99%.
*Printed only in the draft:* 7,250, 29,000, 0.8000 to 0.2000. They agree with each other (4 x 7,250 = 29,000), and no
final document confirms them. The instructions call both worksheets "the Exemption Worksheet on the inside of the back
cover", while the draft has a separate Standard Deduction Worksheet; a final back cover would settle both.

*How it is held.* Projection: `stepped` with `keep_share` on both deductions, on `state_agi`, exact: simulated against the
worksheet at 216,248 incomes, cents included, both deductions, no mismatch. The `warn_when: always` marker is gone. An
approximation says the bands rest on the draft (either way, at most 958.40 single, 1,916.80 couple), and another that a
consumer growing the steps grows the 7,250 too, which no source says is adjusted.
Record: `effect` stays `other` with the worksheet in `as_printed`, because the band edges are computed and the validator allows
only printed figures in a record (Minnesota's stepped bands had the same limit). Two workarounds follow those
settlements, since the projection's `derived_figures` need their parts in the record: `rate: "0.2"` on an `other` test
(Minnesota), which is the share each band removes, and `ri_phaseout_worksheet_step_width`, a `what: other` entry holding the
printed 7,250 and labelled not a deduction (Kansas), because no record field holds a width. The projection does not list
that entry. `derived_figures` has 7 lines: four edges, three percentages.

**Tax rate schedule: confirmed, unchanged.** Draft: "2025 Tax Rate Schedule - FOR ALL FILING STATUS TYPES": 0 to 79,900 at
3.75%; 79,900 to 181,650, 2,996.25 + 4.75%; over 181,650, 7,829.38 + 5.99%. Final (instructions PDF p.13): the same bands and
rates with subtraction amounts 799.00 and 3,051.46; 3.75% x 79,900 = 2,996.25, and 4.75% x 181,650 - 799.00 = 7,829.375, the
draft's 7,829.38 rounded. The final document remains the cite.

**ADV 2025-20: what the decoupling means for a state that starts from federal AGI.** The advisory: "the following items
are now allowed federally that are not allowed under Rhode Island law". It splits them:
- *Above the line* (they lower federal AGI, so they must be added back): business interest expense, section 174A
  research expensing, depreciation of business assets, qualified sound recording. RI Schedule HR1 - Individual, then
  Schedule M line 2k (instructions PDF pp.3, 12; the schedule's image, advisory p.2). So for these, RI income
  is **higher** than federal AGI. All four are business items, for sole proprietors and pass-through members.
- *Below the line* (tips, overtime, car loan interest): "these tax provisions are below the line, meaning they are not
  reflected in federal adjusted gross income, which is the starting point of the RI-1040 and RI-1040NR returns. Rhode
  Island is decoupled from this tax treatment and will not allow for these exclusions". Nothing is added back: they
  never reach the RI return. The SALT cap increase is the same; Rhode Island allows no federal itemized deductions.
- For a projection: start from federal AGI and use Rhode Island's own deduction, and the below-the-line items are already
  excluded; no action. A retired household with no business deductions needs nothing. The business add-backs are
  `not_modelled` with an approximation. The advisory does not mention the federal senior deduction; it too would be
  below the line, but that is my reading, so the record does not say it. The advisory covers 2025 only ("for tax years
  beyond 2025" a working group was to report), so a later year needs checking.

## The required facts

| Question | Settled | Quote |
|---|---|---|
| Another state's government pension | `public_pension_other_state` in `covers`, same entry as Rhode Island's own | Guide PDF p.11: "State government pension plans (State of Rhode Island or another state)"; "Local government pension plans (from within Rhode Island or elsewhere)" |
| New York State pension | Same: up to 50,000 if the age and income tests pass. New York is not named; no rule depends on the paying state, so no `paying_states` | As above |
| Own and federal government pensions | `public_pension`, same entry, same cap | Guide PDF p.11: "Civil Service Retirement System (CSRS)", "Federal Employees Retirement System (FERS)", "Federal Thrift Savings Plan (TSP)"; example 1 PDF p.9 |
| Private pensions, plans | `private_pension`, `employer_plan_distribution`, `annuity`, same entry | Guide PDF p.7: "distributions from pensions, annuities, 401(k) plans, 403(b) plans, and governmental 457(b) plans, qualify"; instructions PDF p.10 table lines 2-4 |
| IRA | Not covered | Above |
| Roth conversions | `covers_unclear`; not named anywhere | Both readers agreed. The Guide does not say where a conversion falls; a conversion from an employer plan might reach line 5b, one from an IRA reaches line 4b. Left out of the projection's `covers` by the guide's rule, with an approximation |
| Social Security | `relief`: subtraction of taxable benefits, cap none, 107,000 / 133,750, age test, each person | Worksheet lines 5-13; Guide PDF p.19: "Her taxable social security benefits will not be subject to Rhode Island tax due to the Social Security Modification"; one spouse: line 9 / line 8, Guide PDF p.25 |
| Brackets | One schedule for every status: 3.75% to 79,900; 4.75% to 181,650; 5.99% over | PDF p.13 "Use for all filing status types"; 4.75% x 79,900 - 799.00 = 2,996.25 = 3.75% x 79,900; 5.99% x 181,650 - 3,051.46 = 7,829.375 = 4.75% x 181,650 - 799.00 |
| Standard deduction | 10,900 single, separate; 21,800 joint, widow(er); 16,350 head of household | PDF p.4 line 4; "Rhode Island does not allow the use of federal itemized deductions" |
| Exemption | 5,100 each | PDF p.5 line 6: "Multiply the number of exemptions in the box by $5,100" |

## Changes neither reading made

- Social Security limit 133,750 (above); `applies_when: at_or_over`; `born_on_or_before` on Social Security.
- `cap_rule` of the pension modification. Both readers wrote "less any amount claimed under the Military Service
  Pension Modification" from Guide PDF p.9. The form's table keeps military pay out of line 2 and takes the lesser of
  line 2 or 50,000, so 40,000 military and 30,000 of pension gives 40,000 + 30,000. The other reading, a cap
  reduced to 10,000, gives 50,000 in all. The form is the more direct text, and statute (11)(iii) (PDF p.28) only
  stops the same military income being taken twice. So no `cap_reduced_by` in the projection.
- `ri_us_obligation_interest` added as a relief; instructions PDF p.9 line 1a prints it and both readers held it in notes.
  In the projection: `not_modelled`, as in the other states.
- Military and railroad: `exempt_in_full`, `who.basis: return` (no age test; brief rule 5). Both readers said
  subtraction, each_person. No effect on a result.
- `indexing` on the pension entry says the limits only; the 50,000 cap falls in `all_other`, not stated.

## One-sided entries

- A's note that the Guide's chart (PDF p.24) marks military pay "No" while PDF p.7 says it "qualifies": kept as a note.
  The income is fully exempt either way.
- B's `not_covered` lines on wages and Social Security: dropped, they are not what the booklet lists as not qualifying.
- B's note on foreign pension plans: kept; the schema has no kind for them.
- Other Schedule M lines, credits (other-state, Schedule I, EIC, RI-1040H): notes in the record, `not_modelled` with
  `warn_when: never`.

## Projection decisions

- **Two branches for each age-tested relief; this needs a look.** A fixed `born_on_or_before: 1959-03-01` would cut off
  everyone born later for every future year, which is wrong under the statute and would matter for any planner
  who is under 67 now. So the projection has the printed branch and a `_later_births` branch: born on or after
  1959-03-02, `min_age: 67`. Tax year 2025 is unchanged (nobody in the second branch is 67 at the end of 2025). Each
  person matches one branch only. The date 1959-03-02 is the day after the printed date and 67 is from the Guide's table, so
  no new amount is added, but it is a modelling choice. Each branch will need its own below and at-or-above checks.
- Income tests use federal AGI (RI-1040 line 1), not line 3.
- `relief_caps` indexed false, assumed: the record says not stated. `brackets`, `deductions`, `relief_thresholds` true
  (instructions PDF p.1).
- Social Security on a joint return with one qualifying person needs taxable benefits divided by gross benefits; an
  approximation tells consumers so.

## Unsure

- 133,750 stands on the form, the worksheet and the statute's equality rule, not on a Rhode Island statement that the Guide
  is wrong. A household between 133,500 and 133,750 would lose everything if the Guide were right.
- The date and full retirement age being one test is my arithmetic; no source says so. A person's own test uses year
  end in the planner, which matches the form for 2025.
- The phase-out steps rest on a page marked DRAFT 10/01/2025; 7,250, 29,000 and the percentages have no final source yet.
- Pension boundary: form against statute, one figure's difference.
- Roth conversion reported on federal line 5b (from an employer plan): "whatever you properly include ... on that line"
  might take it, "Completed rollovers" might not. Left unclear.

## 2026-11-07: final worksheets

The final 2025 Tax Rate and Worksheets (address folder 2026-01) is archived. Its text matches the October draft word for word, without the 'DRAFT 10/01/2025' watermark, so 7,250, 29,000 and the 80% to 20% shares now have a final source. Cites point to the final file; the DRAFT approximation is removed. No figure changes.

## 2026-11-08: marker ids and indexing covers

- Marker ids: all 5 markers have an `id`. Descriptive ids (no from_record id of their own): `ri_hr1_addbacks`, `ri_other_schedule_m_lines`, `ri_credits`; the rest take their first from_record id, so their warning codes are unchanged. `tools.checks --fix-warnings` rewrote the cases' accepted_warnings (the old shared code state_rule_not_modelled:unnamed becomes the new ids); nothing else in the cases changed.
- Indexing covers: `brackets` and `deductions` (indexed, booklet What's New); `relief_thresholds` (indexed) covers reliefs.income_test; `relief_caps` (assumed) covers reliefs.cap. The deductions' phase-out is covered whole by `deductions` (indexed), although the record says the 7,250 band width and 29,000 are not said to be adjusted; a selector cannot separate the phase-out's threshold from its width.
- Assumed entries: `relief_caps` stays assumed. The Retirement Income Guide reproduces R.I. Gen. Laws 44-30-12(c)(9): the inflation adjustment applies to 'the dollar amount contained by reference', which (vi) ties to the Social Security AGI limits; the 50,000 cap is written per tax year and no sentence says it is fixed or indexed, as the record already notes.

## 2026-11-08: indexing settled from statutes

Statute research (work/indexing/findings*.json) settled every projection indexing entry that was `assumed: true`:

- `relief_caps` (reliefs.cap): not indexed, R.I. Gen. Laws 44-30-12(c)(9)(i)-(vi)
- Record `indexing`: kept existing ri_pension_annuity_modification (yes, booklet cite, about another figure of it); the statute says its cap is not indexed.
- The record's existing `ri_pension_annuity_modification` entry (yes, for the AGI limits; it already says the 50,000 cap is fixed) is kept unchanged, so the record and its sha256 did not change. The finding's url is http only (webserver.rilegislature.gov), which the cite schema would not accept anyway.
