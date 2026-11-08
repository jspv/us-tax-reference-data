# Brief: reading the federal figures for one tax year

You fill `data/federal/<year>/US.federal.json` (format: `schema/federal.schema.json`; read every
description in it first) from the archived official sources only:
`sources/archive/<year>/US/` (the `*.docling.md`, `*.pypdf.txt` and `*.page.txt` files, with
`=====PAGE n=====` markers) and the list of what each file is in `sources/archive/<year>/US/fetch.json`.
Never use memory, a search result or a secondary site for a figure. If a figure is not in the
archived sources, leave the optional group out and say so in `notes`.

## Rules

1. **As printed.** Every amount and rate is a string holding a decimal number (`"15750"`,
   `"0.22"`). Rates as decimals: 22% is `"0.22"`. No thousands commas.
2. **Cite every group.** `cite.url` is the source's address exactly as in `fetch.json` (`url`).
   `cite.section` names the PDF page and the table, line or code paragraph, and quotes the words
   that carry the figure when they are short. If a group's figures sit in two documents, cite the
   main one and list the other in `cite.also`. The validator checks that each figure is printed in a
   cited document.
3. **The law in force for that tax year.** For 2025, P.L. 119-21 (July 4, 2025) changed figures that
   Rev. Proc. 2024-40 had already published (the standard deduction among them). Use the figure the
   2025 Form 1040 instructions print and cite them; say in `notes` where the Rev. Proc. differs.
   For 2026, Rev. Proc. 2025-32 already reflects P.L. 119-21.
4. **Indexing, from the statute.** Every group has `indexing`, cited to the U.S. Code section (or the
   CFR) that says how the figure changes: `fixed` when the statute writes the amount and never adjusts
   it (the Social Security base amounts, the NIIT thresholds, the additional Medicare tax thresholds,
   the senior deduction); `inflation` with the index, the base period and the rounding exactly as the
   statute words them ("rounded to the next lowest multiple of $50" is multiple 50, direction down);
   `wage_index` for the Social Security wage base; `scheduled` when the statute prints the later
   amounts (the SALT cap); `set_yearly` for the Part B premium. A rule that ends gets
   `applies_through` and `then` (the senior deduction ends after 2028; the SALT cap's higher amount
   ends after 2029). If the statute gives different rounding for married filing separately, say so in
   `rounding.notes`.
5. **Medicare figures are for calendar year `<year>`** (the premium year), with `lookback_years` set
   to the number of years between the premium year and the tax return whose income sets the tier.
   IRMAA tiers: copy every printed tier for single, married_joint and the married-separate-lived-with-
   spouse table; `part_b_monthly_total` is the total premium the table prints, and
   `part_b_monthly_adjustment` the adjustment if printed.
6. **RMD tables:** every row of the Uniform Lifetime Table and the Single Life Table as printed in
   26 CFR 1.401(a)(9)-9 (or Publication 590-B Appendix B, which prints the same tables). `start_age`
   from 26 U.S.C. 401(a)(9)(C) by year of birth; if the statute's wording leaves a birth year unclear,
   record what it says and the reading you used in `notes`.
7. **Derived figures.** Some figures are not indexed on their own: the statute sets them from another
   figure of the same year, after that figure's indexing and rounding. Record each as a `derivations`
   entry in its group (rule `times` with a factor, or `minus`), cited to the statute that says so, and
   check the printed figures obey it (the validator re-does the arithmetic exactly). Look for at least:
   the ordinary bracket edges (married filing separately and single from married filing jointly,
   26 U.S.C. 1(f)(8), 1(j)(2)) and which edges are own-indexed (single's 37% edge); the qualified
   dividend and capital gain bands (26 U.S.C. 1(j)(5)), including which separate figure is its own;
   the standard deduction (joint = 2 x single, separate = single, 63(c)(2)); the IRMAA limits (joint =
   2 x individual, joint top = 1.5 x individual top, 42 U.S.C. 1395r(i)(3)(C)(ii) and (i)(2)(B); the
   lived-with-spouse separate limit = individual top minus the individual first limit). Write only
   what the statute says; if the printed figures don't obey a rule you read, stop and say so in
   `notes`. A derived figure gets no indexing of its own; when a group's figures index differently,
   give `indexing` as a list with `applies_to` on each entry.
8. **Indexing details.** `indexed_from` when a figure starts indexing later (the IRMAA top limits,
   42 U.S.C. 1395r(i)(5)(C)), with the base period the statute names; `never_decreases` for the wage
   base (42 U.S.C. 430); `rounding.multiple_by_status` when a status rounds to a different unit; the
   rounding of Medicare premiums (42 CFR 408.27) when a source states it. The top IRMAA tier is
   "greater than or equal to": set `applies_when: at_or_over` on it.
9. **Statuses.** `by_status` keys: single, married_joint, married_separate, head_of_household; add
   qualifying_surviving_spouse only when its figure differs from married_joint. Use `all` when one
   figure applies to every status.
10. **Write only your output file.** No edits elsewhere, no commits. Then run
   `uv run python -m tools.validate <your file>` and fix every problem it reports (a provenance
   problem means a wrong figure, a wrong cite, or a figure printed in another source: find it, don't
   force it).
