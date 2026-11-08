"""Convert archived PDFs to text with two independent converters.

    uv run python -m tools.convert --year 2025 --state GA [--state UT ...] | --all

For each PDF in sources/archive/<year>/<ST>/ writes, next to it:
  <stem>.docling.md   Docling (layout and table aware): the primary text, read by extraction pass A and B
  <stem>.pypdf.txt    pypdf (plain text layer): a second, independent text for spot checks

Both put `=====PAGE n=====` markers between pages so a citation can name the PDF page.
Decision record: docs/decisions.md (converter bake-off, 2026-11-06).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAGE_MARK = "\n=====PAGE {n}=====\n"
DOCLING_BREAK = "\n<<<PAGE-BREAK>>>\n"


def convert_pypdf(pdf: Path) -> str:
    from pypdf import PdfReader

    reader = PdfReader(str(pdf))
    return "".join(PAGE_MARK.format(n=i) + (page.extract_text() or "") for i, page in enumerate(reader.pages, 1))


_DOCLING = None


def convert_docling(pdf: Path) -> str:
    global _DOCLING
    if _DOCLING is None:
        from docling.document_converter import DocumentConverter

        _DOCLING = DocumentConverter()
    document = _DOCLING.convert(str(pdf)).document
    from pypdf import PdfReader

    count = len(PdfReader(str(pdf)).pages)  # one marker per PDF page, blank pages included
    # Page by page: a single export with a page-break placeholder skips breaks for some pages, so markers
    # drifted from the PDF's page numbers (CO, DC and VA 2025 booklets).
    return "".join(PAGE_MARK.format(n=n) + document.export_to_markdown(page_no=n) for n in range(1, count + 1))


def convert_state(archive: Path, year: int, state: str) -> list[str]:
    directory = archive / str(year) / state
    done = []
    for pdf in sorted(directory.glob("*.pdf")):
        for suffix, function in ((".pypdf.txt", convert_pypdf), (".docling.md", convert_docling)):
            target = pdf.with_name(pdf.stem + suffix)
            if target.exists() and target.stat().st_mtime >= pdf.stat().st_mtime:
                continue  # up to date
            target.write_text(function(pdf))
            done.append(target.name)
    return done


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--state", action="append", default=[])
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--archive", type=Path, default=ROOT / "sources" / "archive")
    args = parser.parse_args(argv)
    year_dir = args.archive / str(args.year)
    states = sorted(p.name for p in year_dir.iterdir() if p.is_dir()) if args.all else [s.upper() for s in args.state]
    if not states:
        parser.error("give --state or --all")
    for state in states:
        print(state, json.dumps(convert_state(args.archive, args.year, state)), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
