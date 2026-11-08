# Settlement brief: from two readings to one record and its projection

You settle one state for one tax year. Two readers wrote independent layer-1 readings (`A` and `B`)
from the same sources. You produce the settled record and its layer-2 projection, and log every
decision. You are the person who reads the booklet when the readers disagree.

## Inputs

- The two readings: `work/extract/{YEAR}/{ST}.{ROUND}.A.json` and `.B.json`.
- Their comparison: `uv run python -m tools.compare <A> <B>` (structured differences count; wording
  differences don't).
- The sources: `sources/archive/{YEAR}/{ST}/` (converted text `*.docling.md`, `*.pypdf.txt`,
  `*.page.txt`; the PDFs).
- `docs/extraction-brief.md` (what a record holds), `docs/projection-guide.md` (what a projection
  holds), both schemas.

## Steps

1. **Run the comparison.** For each structured difference where both readers recorded a value and the
   values differ, read the cited page in the sources and decide. Never split the difference; the
   booklet decides. If the booklet doesn't settle it, use the schema's `not_stated` or leave the field
   out, and note it.
2. **One-sided entries** (only one reader recorded it): keep it if the booklet prints it and it is in
   scope for the record (`docs/extraction-brief.md`); drop it otherwise. Where the readers split one rule
   differently, write it the way the brief asks (one entry per branch with its own conditions; pensions
   split by source when the state treats them differently).
3. **Check the facts most often missed**, each against a second document or line, not just the reader's
   cite: Social Security treatment; every retirement relief's cap, age test and covered income; the
   bracket schedule for every filing status printed; the standard deduction and exemptions.
4. **Use the newer fields where they fit**, even if neither reader did: `income_test.effect: stepped`
   with `steps` for table-driven phase-outs; `brackets.derivation` when brackets come from a tax table
   or formula (record at least three printed table rows spread across the bands, and the formula);
   `credit_basis`; `recapture`; `covers: ["all_income"]`; `public_pension_other_state`.
5. **Write the settled record** to `data/states/{YEAR}/{ST}.record.json`. Add one `notes` line per
   settlement: "Settlement {DATE}: <field>: A said X, B said Y; <page> says Z."
6. **Write the projection** to `data/states/{YEAR}/{ST}.projection.json` by `docs/projection-guide.md`:
   `record.sha256` is the sha256 of the record file as written; every relief and marker names its
   record ids; derived figures go in `derived_figures`; anything the projection can't compute goes in
   `not_modelled` with `warn_when`, and every simplification in `approximations` with its direction.
7. **Validate both**: `uv run python -m tools.validate data/states/{YEAR}/{ST}.record.json
   data/states/{YEAR}/{ST}.projection.json`. Fix every problem.
8. **Log**: write `work/settlement/{YEAR}/{ST}.md`: each structured difference and its settlement with
   the page, each one-sided entry kept or dropped and why, and anything you are unsure of. That file is
   kept; the reviewer reads it.

## Rules

- Figures come only from the sources. No outside knowledge of the state's law, no other dataset.
- When unsure, say so in the log and choose the reading that is printed most directly.
- Write helper scripts only in the private folder your dispatch names.
- Never run a recursive delete built from a variable. Delete nothing; overwrite only the three output
  files named above.
