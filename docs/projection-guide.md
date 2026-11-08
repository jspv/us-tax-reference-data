# Projection guide: layer 2, from a settled record

Layer 2 is what a long-range planner evaluates each year. It is derived from one settled layer-1
record (`schema/projection.schema.json`) and adds no figures of its own: the validator rejects any
amount that is not in the record, and marks the projection stale when the record changes.

## The test for each record entry

Keep a rule when **both** hold:
1. **A projection can compute it** from a household's yearly facts: filing status; each person's
   birth date; wages and self-employment; pensions; IRA and employer-plan withdrawals (RMDs
   included); Roth conversions; Social Security; interest, dividends, gains; tax-exempt interest.
2. **It is material**: it changes a planning decision (retirement date, Social Security claiming,
   Roth conversion size, which account to draw, where to live) or the tax by more than a token amount.

Otherwise it goes in `not_modelled` with `warn_when`, so a run can say it may apply to this household.

## Must have

Rate schedule per filing status; Social Security treatment; every relief branch a projection can
compute (who, covers, cap, cap_per, sub-limits, income test on a computable measure, credit or
subtraction, cannot-combine, best-of group); where state income starts and the state's own
standard deduction and personal exemptions (a projection starts from federal AGI and subtracts these,
never the federal deductions, unless the state's law itself starts from federal taxable income);
indexing as a yes or no for every figure family grown, with a `deductions` entry whenever there are
deductions.

## Should have

Surtaxes (folded into the brackets, below); municipal interest; capital gains treatment.

## Mapping rules

- **Pension kinds.** A relief that treats public, private or military pensions differently lists
  `needs_input: ["pension_source"]` (and `pension_contributory` when it turns on a contributory plan).
  These are supported inputs, not gaps: a consumer can ask the household for them, and needs to ask only
  when it lives in such a state. So model the relief (don't put it in `not_modelled`), with `covers`
  split by pension kind exactly as the record has it.
- **Surtaxes are folded into the brackets.** A surtax on taxable income becomes one more band in every
  filing status's schedule, at the bracket rate plus the surtax (Massachusetts: 5% from 0, 9% from
  1,083,150, the same threshold for single and joint because the booklet prints one). The 9% goes in
  `derived_figures` as the sum of 0.05 and 0.04. A surtax on another measure can't be folded and goes in
  `approximations`.
- **A table that steps up at a threshold** (Ohio) uses the band's optional `base`: the printed tax at the start, replacing the sum of the lower bands. Never hide a lump sum in a very narrow band with an invented rate; consumers read rates as marginal rates.
- **Gains with their own rate** run through the brackets and pay `extra_rate` on top, so they also pay
  any surtax band (Massachusetts short-term gains: 0.085 - 0.05 = 0.035, in `derived_figures`).
- **Income measures** outside the projection list map to the nearest one, with an `approximations`
  entry saying the direction and size.
- **`state_own` base** maps to `federal_agi` with an approximation.
- **Deductions.** Every record deduction a projection can apply goes in `base.deductions`: per return,
  or per person (an exemption "for each exemption claimed" counts the filer and spouse; dependents are
  `not_modelled`); an age-65 amount gets `min_age`; an income phase-out goes in `phase_out`. A state
  that allows itemizing gets its standard amount and an approximation.
- **Per-dependent amounts, disability, Social Security-exempt employment, fire/police/corrections,
  part-year residence, low-income and renter credits**: `not_modelled`.
- **Indexing `not_stated`** becomes `indexed: false, assumed: true` until the statute is read.
- **Roth conversions in `covers_unclear`**: leave them out of `covers` and add an approximation
  (overstates tax for a converter if the state does exempt them).
- **`all_income` reliefs** (age deductions) are amounts that offset the return's whole income, any person's, with one cap per qualifying person when `who.basis` is `each_person`.
- **A straight-line phase-out** (the relief loses (income - threshold) / width of itself) uses
  `income_test.effect: share_phase_out` with `width`, and `share_decimals` when the form rounds the share
  (Maine's pension deduction: width 100,000, 50,000 married separate, 4 decimals). Don't approximate it
  with equal steps.
- **A test measured partway through the reliefs** (Missouri's Line 6) lists the reliefs taken off first in
  `measure.minus_reliefs`.
- **A relief applied on an assumption** about a fact the projection lacks (North Carolina: every military
  pension meets the 20-year test) is modelled, carries an `assumption` with its own `warn_when`, and repeats
  the text in `approximations`. Use it only on a maintainer decision recorded in docs/decisions.md.
- **Warnings fire only when the household hits the case.** Pick the narrowest `warn_when`:
  `has_retirement_account_distribution` (with `age_range` for an early payout), `has_long_term_gains`,
  `has_other_state_public_pension`, `income_over` (with its measure and threshold). `always` is for a rule
  every household may meet; never use an age range alone as a stand-in for a kind of income.
- **Refundable credits** set `refundable: true`; checks may then show `state_income_tax` below 0.
- **Cap reduction order**: `cap_reduction: from_lesser_of_income_and_cap` when the booklet takes the
  reducing income off the lesser of the income and the cap (Indiana).
- **Capital gains above an income level** (Maryland) use the entry's `applies_over`.
- **U.S. obligation interest** is exempt in every state with an income tax (31 U.S.C. 3124). Each
  projection keeps an approximation that it is taxed, for a consumer that does not separate Treasury
  interest from other interest; a consumer that does separate it can exempt it and drop the
  approximation. There is no per-state field because the answer never differs.
- **Fields added within format 1 that change a relief's meaning** (`applies_over`, `keeps_taxable`) are listed in the relief's `requires`; a reader that lacks one skips the relief and warns. Connecticut's partial Social Security subtraction is the first.
- Every relief and marker names its record ids in `from_record`.

Out of scope for now: local income taxes.
