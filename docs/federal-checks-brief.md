# Brief: hand-worked federal checks

Each case is one household worked by hand from the federal publications, to prove the figures in
`data/federal/<year>/US.federal.json`. Format: `schema/federal-check.schema.json`. Files:
`checks/<year>/US/<id>.json`, id `US-<year>-<words>`. Gate: `uv run python -m tools.federal_checks --year <year>`.

## Rules

1. **Work from the publications' own worksheets and the federal file's figures**, naming each line in
   `worked`: Form 1040 (lines 1-15), the Social Security Benefits Worksheet (Form 1040 instructions /
   Publication 915), Schedule 1-A Part V (senior deduction), the Qualified Dividends and Capital Gain Tax
   Worksheet, Form 8960 (NIIT), Form 8959 (additional Medicare tax), the CMS IRMAA tables, the Uniform
   Lifetime Table.
2. **Tax on ordinary income uses the Tax Rate Schedules, to the cent, never the Tax Table** (the Tax
   Table rounds to $50 bands below 100,000; a planner uses the schedules). Round only where a form says to.
3. **Standard deduction only.** No itemizing, no credits, no dependents. Ages follow the tax rule (a person
   born on January 1 is a year older at the end of the year). Amounts are strings with two decimals where
   cents can arise.
4. **Inputs given, not derived:** a case lists only the inputs its kind uses (see the schema). For IRMAA,
   `magi` is the income from the return the premium year looks back to; the case states which year.
5. **Coverage** (the gate enforces it): each of brackets, standard deduction, additional standard deduction,
   capital gains, Part B, payroll Medicare and the Uniform Lifetime Table has a case; each of the senior
   deduction, NIIT, additional Medicare tax, taxable Social Security, IRMAA, the Social Security wage base and
   the RMD start age has a `below` and an `at_or_above` case. Put the household exactly at a threshold where
   the form's words make "at" matter (IRMAA's top tier is "greater than or equal to"; most others are
   "more than").
6. **Expected lines:** give every expected line the case can show; at least the lines that prove the groups
   in `tests`. `total_tax` = `regular_tax` + `net_investment_income_tax` + `additional_medicare_tax`.
7. A separate model session works the same inputs blind (`uv run python -m tools.checks_compare prepare|compare
   --year <year> --state US`); only agreeing cases ship.
