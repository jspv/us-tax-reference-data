# Tax reference data: design

## Purpose

A single, cited, machine-readable source of the federal and state tax figures a retirement
planner needs, plus the tooling that fetches the official publications, converts them to text,
extracts the figures, checks them two independent ways, and refreshes them every year.

Every figure traces to a government publication (an agency instruction booklet, a statute, a
revenue procedure, a CMS notice), with the page or line, the retrieval date and a hash of the
exact file read. Nothing is copied from a third-party tax dataset, aggregator or another
project's parameter files.

The data is not written for any one application. A consumer takes a tagged release, never the live
repository (see "Using the data").

## Goals

- Federal: IRS brackets and deductions (Rev. Proc.), IRMAA tiers and Medicare premiums (CMS),
  Social Security wage base (SSA), payroll rates.
- States: all 50 states and DC, per tax year: brackets, where taxable income starts, Social
  Security treatment, retirement-income relief by kind, municipal interest, whether the state
  indexes its figures, estimated-tax rules.
- A repeatable yearly refresh that reports which sources changed.
- Hand-worked checks (one per rule, from the publication's own worksheet) that prove a value.

## Non-goals

- Computing tax. This repository holds figures and rules as data; engines live elsewhere.
- Local income taxes (county, city, school district): out of scope for now (maintainer, 2026-11-06);
  they may be added later.
- Credits other than relief for retirement income and Social Security.
- A live service. Consumers take tagged releases.

## Tax-year policy

State booklets for a tax year appear in December to January of the following year, so the newest
complete year is the previous one (2025 in November 2026). Data is keyed by tax year. When a state
has enacted a change for a later year, a second dated entry records it from the session law or
agency notice, and is marked as such until that year's booklet confirms it.

## Layout

```
data/federal/<year>/US.federal.json   federal figures (format: schema/federal.schema.json; brief: docs/federal-brief.md)
data/states/<year>/<ST>.record.json, <ST>.projection.json   two files per jurisdiction (see "Two layers")
schema/                       JSON Schemas for each kind of file
sources/registry.json         per jurisdiction: agency, booklet title, edition, address
sources/archive/<year>/<ST>/  fetch.json (a record of each source), and the converted text of web-page sources
checks/<year>/<ST>/           hand-worked examples, one per rule, with citations
tools/                        fetch, convert, extract support, compare, validate, sources, export
releases/                     changelog per tagged release (YYYY.N)
docs/                         this design, the format reference, the refresh runbook, decisions
```

`sources/archive/<year>/<ST>/fetch.json` records, for each source, the address it was downloaded
from, the sha256 of the exact file read and the address of an Internet Archive copy (`archived_url`).
The source PDFs are not needed to use the data. Anyone who wants to re-check a figure pulls them on
demand: `uv run python -m tools.sources pull --year 2025` (`tools/sources.py`) downloads each missing
file from its archived copy, or failing that from the agency, and keeps it only if its sha256 matches
the record. For a source that is a web page, the converted page text (`.page.txt`) is kept in the
repository.

## Two layers

Each jurisdiction and year has two files, because two different questions are checked by
different means:

1. **Layer 1, the record** (`data/states/<year>/<ST>.record.json`, `schema/record.schema.json`):
   what the publication says, faithfully, structured enough for two independent readings to be
   compared field by field. Checked by the two-reader comparison and by figure presence (every
   figure is printed in the booklet). Any consumer can use it.
2. **Layer 2, the projection model** (`data/states/<year>/<ST>.projection.json`,
   `schema/projection.schema.json`): what a long-range planner evaluates each year, derived from one
   record (named with its sha256, so a changed record makes it stale). It holds only rules a
   projection can compute from a household's yearly facts, marks the rest `not_modelled` with when
   a run should warn, and lists every approximation with its direction. It adds no figures of its own: every
   amount is in the record, or is listed in `derived_figures` as a sum or difference of record figures
   that the validator re-does (a folded surtax band). Checked by hand-worked examples. Rules for building it:
   `docs/projection-guide.md`.

Keeping them apart separates "did we read the booklet correctly" from "did we decide correctly
what a projection needs"; they are different mistakes with different reviewers.

### What layer 2 holds (maintainer, 2026-11-06)

- **Must have:** rate schedule per filing status; Social Security treatment; every computable
  retirement relief branch, broken down by the income a projection produces (public, private and
  military pensions; IRA and employer-plan withdrawals, RMDs included; Roth conversions), with whose
  age or birth date, the cap and whether per person or per return, sub-limits, income tests on a
  computable measure and their effect, credit or subtraction, which reliefs exclude each other, and
  "take the better of" groups; where state income starts and the state's own standard deduction and
  personal exemptions (per return or per person, with any age-65 amounts and income phase-outs),
  because borrowing the federal deductions understates a retired couple's state tax by roughly
  1,500 a year in Michigan, Pennsylvania or Massachusetts (maintainer, 2026-11-06); indexing as a yes or no
  per figure family, deductions included.
- **Should have:** surtaxes (Massachusetts 4% over 1,083,150; layer 2 folds a surtax on taxable income into
  the brackets as one more band, so a consumer needs only bracket code); municipal interest;
  capital gains treatment (own rates, deducted shares).
- **Not modelled, with a warning marker:** disability tests, Social Security-exempt employment,
  fire/police/corrections pensions, per-dependent amounts, low-income and renter credits,
  part-year residence, estimated-tax schedules.

### Record format notes

Every amount and rate is a string holding a decimal number. Every item carries `cite`:
`{publication, section, url, accessed}`; `section` is the page and line, never just the title. The
pilot (GA, UT, MI, MA; `docs/pilot-2025-ledger.md`) shaped it: indexing is per figure; deductions say
what they are per; a relief is one entry per branch with its own conditions (Michigan's rules turn
on birth year, public or private income and kind of employment at once); covered income is a fixed
list, and Roth conversions are listed only when the booklet says so.

## Process

1. **Registry.** For each jurisdiction, the agency's own forms page (found from the Federation of
   Tax Administrators list) leads to the instruction booklet for the year. An address is
   recorded only after it was opened.
2. **Fetch.** A headless Chromium browser downloads each file, one at a time with a pause between
   requests. Plain HTTP downloads are refused by some agencies (Massachusetts) and the browser is
   the one path that works for all, so it is the only path. A result that is not a PDF is a
   failure, and the state goes on a manual list (the maintainer saves the file by hand).
3. **Convert.** A converter turns the PDF into text or structured JSON that keeps worksheet and
   table layout. The converter sits behind one interface so it can be replaced. Which one is
   decided by the bake-off (docs/decisions.md).
4. **Extract, pass A.** A reader (a model, with the converted text and `docs/extraction-brief.md`)
   writes the layer-1 record.
5. **Extract, pass B.** A second reader, with no sight of pass A, writes the same record.
6. **Compare.** `tools/compare.py` diffs the two field by field, matching entries by meaning. Every
   difference is settled against the booklet by a third read, and the settlement is logged.
7. **Project.** The settled record is mapped to layer 2 by `docs/projection-guide.md`.
8. **Validate.** `tools/validate.py`: schema; figure presence (record); hash, ids and no-new-figures
   (projection); hand-worked checks re-run from their own inputs.
9. **Release.** A tagged release `YYYY.N` (or `YYYY.N-draft.M` before the schema is frozen), built by
   `tools/export.py`, with a manifest of every file's sha256. **Releases are immutable:** a published tag
   and its bundle are never changed; any change, however small, is a new version. Consumers pin a version
   and verify its hashes.

Refresh each year: re-run steps 2 and 3 for every source, compare hashes to the last release,
and re-extract only the states whose source changed.

## Using the data

A consumer pins one tagged release (a version such as `2025.1`) and never reads the live
repository. Releases are immutable, so the pinned files never change under it. The release's
`manifest.json` lists the sha256 of every file; the consumer checks its copy against those hashes,
so a copied file that was edited or swapped is caught. Moving to a newer release is a deliberate
step: pin the new tag, copy its files, check the hashes again.

A projection engine reads layer 2. Some reliefs turn on facts about a household's pensions: the
pension's source (`public`, `private` or `military`) and, for a public pension, whether the plan is
contributory. Those reliefs say so in `needs_input`. A consumer can ask the household for these facts
only when its state has such a relief. So the data records them fully: every relief that treats
pension kinds differently splits its `covers` into `public_pension`, `private_pension` and
`military_pension`, and names the contributory test in the record's `who.other_conditions` and in
layer 2's `needs_input`.

This repository's `checks/` prove the data values: each case is worked by hand from the state's own
form. A consumer still needs its own tests of its engine.

## Licence

Private for now. The data is public law and agency publications and brings no licence
obligations; the licence of what this repository publishes is the maintainer's choice.
