# Extraction brief: layer 1, the record (given to each reader, pass A and pass B)

You are writing down what one state's own published booklet says, for one tax year. Your output is
read by software and by a person who will rely on it, so a missing value is better than a guessed one.
You record what the booklet says; you do not simplify it for any consumer (that is layer 2, done later).

## Inputs

- State code `{ST}`, tax year `{YEAR}`.
- The converted booklet text under `sources/archive/{YEAR}/{ST}/`: `*.docling.md` (layout-aware, the
  main text) and `*.pypdf.txt` (plain text layer, for checking a figure). Pages are marked
  `=====PAGE n=====`; n is the PDF page number, which is what you cite. If the two files' markers disagree
  for a page, the `*.pypdf.txt` number is the PDF's own; cite that.
- Agency web pages saved as `*.page.txt` (their visible text), when the registry lists one: guidance
  pages that state a rule outright (New York's "Information for retired persons"). Cite them like a
  booklet, with the page's address and the section heading.
- `sources/archive/{YEAR}/{ST}/fetch.json` for each document's address and retrieval date.
- The format: `schema/record.schema.json`. Read it first; every field and its meaning is there.
  Set `"layer": "record"`.

## Rules

0. **Read the return form as well as the instructions.** The form's own line list can hold a fact the
   instructions never describe (New York's subtraction of taxable Social Security is printed only on
   Form IT-201 line 27). The form is one of the documents in your folder when the registry has it.

1. **Only what the booklet prints.** Use no other source, no memory of what a state's law is, and no
   other dataset. If the booklet does not say, leave the optional field out (or use the schema's
   `not_stated` value) and add a line to `notes` saying what is missing. Never fill a gap with what
   seems likely. Never write that something does not exist unless the booklet says so: "not found"
   goes in `notes` as "not found in the booklet", which is different from "the booklet says there is none".
2. **Search, then read.** Booklets are long. Search the text for the topics (tax rate, rate schedule,
   surtax, standard deduction, exemption, retirement, pension, annuity, IRA, 401(k), Roth, conversion,
   Social Security, military, railroad, age 65, born, subtraction, exclusion, deduction, credit,
   municipal, capital gain, inflation, indexed, adjusted annually), then read the whole page around
   each hit, and the worksheet if there is one. Read every heading of a retirement section: rules are
   often split by birth year under separate headings.
3. **One relief entry per branch.** When a rule differs by age, by birth date, by public or private
   income, or by kind of employment, write one entry per branch, each with its own `who`, `covers`
   and `cap`. When the filer may choose between entries (a subtraction or a larger deduction), give
   them the same `best_of_group`. When one cannot be claimed with another, list it in
   `cannot_combine_with`.
4. **`covers` is a list of income kinds from the schema, and only those the booklet names** (or a
   worksheet line takes). IRA distributions, employer-plan distributions and Roth conversions are
   separate kinds: list `roth_conversion` only if the booklet says conversions count; if it doesn't
   settle it, put it in `covers_unclear`. Anything the booklet says does not qualify goes in
   `not_covered`, in its words. **Pensions are always split by source** when the booklet treats them
   differently: `public_pension` (federal, state, local government), `private_pension`,
   `military_pension`, each in its own entry when caps or rules differ. A test on whether a public plan
   is contributory goes in `who.other_conditions` as "contributory plan" (consumers supply this fact).
5. **Whose age.** `who.basis` is `each_person` when each spouse qualifies on their own,
   `older_spouse` when the booklet uses the older spouse's birth year for the return, `return` when
   neither. Use dates exactly as printed (`born_on_or_before: "1945-12-31"` for "born before 1946").
   Tests a planner may not know (disability, Social Security-exempt employment, fire or police,
   retired by a date) go in `who.other_conditions`, in plain words.
6. **Caps and limits.** `cap` is an amount per filing status (`all` when the booklet gives one
   amount), `cap_per` says person or return; reductions and sharing go in `cap_rule`; a limit on one
   kind of income inside the cap is a `sub_limit`. Income tests name the measure from the schema list
   and also copy the booklet's own definition into `as_printed`.
7. **Deductions and exemptions are always recorded**, with every amount the booklet prints: the
   standard deduction, personal and dependent exemptions, age-65 and blindness amounts, by filing
   status, and what each is per (return, person, dependent, or each exemption claimed). Record any
   income phase-out of them in `phase_out`, any condition (only if the federal standard deduction is
   taken) in `condition`, and whether the booklet says they are adjusted for inflation in `indexing`.
   If the state has none, say so in `notes` ("the booklet prints no standard deduction").
8. **Indexing per figure.** For each figure the booklet says is (or is not) adjusted for inflation, an
   `indexing` entry naming the figure's id. Always add one entry with figure `all_other` for the rest,
   usually `not_stated`.
9. **Capital gains and surtaxes.** Record any rate on gains that differs from the ordinary rate, any
   share of gains deducted, and any extra rate over a threshold.
10. **Amounts are strings** (`"65000"`, `"0.0519"`), rates as decimals (5.19% is `"0.0519"`).
11. **Cite every item**: `cite.section` names the PDF page and the line, worksheet or code section.
    `cite.url` and `cite.accessed` come from `fetch.json`.
12. **Judgement calls go in `notes`**, one line each.
13. **Social Security is never inferred.** `exempt` needs a subtraction line, worksheet or sentence that
    says so; `taxed` needs a sentence that says so. Silence is `not_stated`, with a note.
14. **"Against any income."** A deduction or relief that applies to any income (an age deduction) has
    `covers: ["all_income"]`. A government pension from another state is `public_pension_other_state`,
    never `public_pension`, when the state treats it differently from its own.
15. **Ages** are numbers: 59.5 for "59½". `max_age` is inclusive: "under 65" is 64.
15a. **Pensions from other states' governments.** Say how the state treats them, from its own words:
    in the same entry as its own public pensions (`public_pension_other_state` in `covers`), in another
    entry, or not at all (then "not found in the booklet" in `notes`). When the treatment depends on which
    state pays (a reciprocity rule), write one entry per paying state named in the sources, with
    `paying_states`.
16. **Recapture.** A rule that takes back the benefit of the lower brackets above an income level goes in
    `recapture` with its thresholds; an empty list when there is none.
17. **No-income-tax state:** `has_income_tax: false`, empty bracket lists, and cite the page that says so.

## Output

One JSON file at the path you are given. Then run `uv run python -m tools.validate <your file>` from
the repository root and fix every problem it reports; a figure it cannot find in the booklet text is
wrong, or derived (cite the arithmetic in `notes`), or misread.

Pass A and pass B do not see each other's output. Do not look for it.

## Working files

Write helper scripts and scratch files only in the private folder your dispatch names. Do not open,
run or list anything in another folder there: other readers' files may be in neighbouring folders.

## Safety

Never run a recursive delete (`rm -r`, `rm -rf`) built from a variable. You write one file and read
others; you delete nothing.
