# us-tax-reference-data

Cited, machine-readable U.S. federal and state individual income tax figures, with the tools that
produced and check them, for testing and developing retirement-planning software.

## Read this first: made by AI, for testing only

**This dataset was produced by large language models (AI).** Language models read the government
publications, extracted the figures, wrote the rules, worked the example cases and checked each
other's work. A person directed the work and made some judgement calls, but no person has checked the
figures line by line. Where these files say a case was "hand-worked", "worked by hand" or worked by a
"second person", that working was done step by step by a language model, and the second working by a
separate model session.

**It will contain errors.** Expect misread figures, missed or misunderstood rules, rules applied to
the wrong people or years, and mistakes in the worked cases. The checks described below compare one AI
working against another. They catch many mistakes, but not the ones both workings make, and two
workings agreeing does not show that either is right. Tax law also changes after a release is made.

**Use it for testing software only. Do not rely on it for any financial decision.** That includes
tax, investment, retirement and benefit decisions, preparing or filing a tax return, and advising
anyone else. Nothing here is tax, legal, investment or financial advice. For a real decision, use the
official publication cited for the figure, or ask a qualified professional.

## What is here

- **Federal** (tax years 2025 and 2026): rate schedules, standard deduction and the additional amount
  at 65, the 2025-2028 senior deduction, capital gains bands, net investment income tax, additional
  Medicare tax, taxable Social Security, SALT cap, Medicare Part B premium and IRMAA tiers (Parts B
  and D), Social Security wage base and payroll rates, retirement-account limits, RMD tables. Each
  figure says how it changes in later years (indexed, fixed by law, or set each year), and which
  figures the statute sets from others (the joint standard deduction is twice the single one).
- **States** (tax year 2025): all 50 states and the District of Columbia. Rate schedules, where state
  taxable income starts, state deductions and exemptions, Social Security treatment, every relief for
  pensions, IRAs and other retirement income, capital gains treatment, municipal interest, indexing.

Every figure cites the government publication it comes from (agency booklet, revenue procedure, CMS
or SSA notice, statute or regulation), with the PDF page and line, and the sha256 of the exact file
read. Nothing is copied from a third-party tax dataset or another project's parameters.

## Getting the data

Most users want a release: each tagged release has a small archive (about 1 MB) with the data,
schemas, worked checks and a `manifest.json` holding the sha256 of every file. Releases never
change once tagged; pin a version and check the hashes.

Cloning the repository gives the same data plus the tools, the decision log and the evidence behind
each state (settlement notes and the second, blind working of every check). It does **not** include
the source PDFs (about 200 MB). To pull them:

```
uv run python -m tools.sources pull --year 2025              # every jurisdiction
uv run python -m tools.sources pull --year 2025 --state GA   # one state
```

Each PDF is downloaded from an Internet Archive copy whose content is byte-for-byte the file that was
read (or, failing that, the agency's own address), kept only if its sha256 matches the record in
`sources/archive/<year>/<ST>/fetch.json`, and converted to page-marked text. Web-page sources, and
the few PDFs with no exact archived copy, are kept in the repository as converted text.

## Layout

```
data/federal/<year>/US.federal.json        federal figures             schema/federal.schema.json
data/states/<year>/<ST>.record.json        what the state publication says (layer 1)   schema/record.schema.json
data/states/<year>/<ST>.projection.json    what a planner computes each year (layer 2)  schema/projection.schema.json
checks/<year>/<ST>/, checks/<year>/US/     worked cases                schema/check.schema.json, federal-check.schema.json
sources/                                   registry of sources; per year and jurisdiction, fetch.json (address, sha256, archived copy)
docs/                                      design, decisions with evidence, briefs for each step, pension report
tools/                                     fetch, convert, compare, validate, checks, sources, export
work/settlement/, work/checks-verify/      evidence: how each state was settled; the blind second workings
```

Start with `docs/design.md`. A planner reads layer 2 (`*.projection.json`): only rules a projection
can compute from a household's yearly figures, each approximation listed with its direction and size,
and rules it cannot compute marked with when to warn. Layer 1 (`*.record.json`) is the faithful record
of the publication.

## How the figures are checked

Every step below is carried out by language models (see "Read this first").

1. **Two independent readings.** Two separate model sessions extract each jurisdiction from the converted sources
   into the record format; `tools/compare.py` diffs them field by field, and every difference is
   settled against the publication (`work/settlement/`).
2. **Every figure is printed.** `tools/validate.py` checks that every amount and rate in a record is
   printed in that jurisdiction's sources (federal: in the very document its citation names), and that
   a projection adds no figure of its own.
3. **Worked checks, worked twice.** Each relief, deduction and threshold has cases worked step by
   step from the publication's own worksheets (below and at each limit). A separate model session works
   the same inputs without seeing the first working; `tools/checks_compare.py` compares every line to the cent, and only agreeing cases
   ship. Releases include only verified jurisdictions.

## Tools

```
uv sync
uv run pytest
uv run python -m tools.validate data/states/2025/*.json data/federal/*/US.federal.json   # needs the sources pulled
uv run python -m tools.checks --year 2025 --require-verified
uv run python -m tools.federal_checks --year 2025 --require-verified
uv run python -m tools.fetch --year 2025 --state GA     # download from the agency (headless Chromium)
uv run python -m tools.convert --year 2025 --state GA   # Docling + pypdf, page-marked text
```

Fetching from agencies needs a Chromium build (`TAXREF_CHROMIUM`, or the newest
`~/.cache/ms-playwright/chromium-*`); pulling archived sources does not.

## Licences

Code: MIT (`LICENSE`). Data and documentation: Creative Commons Attribution 4.0 (`LICENSE-DATA`).
The underlying publications belong to the agencies that issued them; this repository does not
re-host the source PDFs.
