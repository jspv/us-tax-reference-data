"""Record a source the maintainer saved by hand (an agency that refuses automated downloads).

    uv run python -m tools.import_manual --year 2025 --state ME --url <registry address> --file <path> [--move]

Copies (or moves) the file into sources/archive/<year>/<ST>/, checks it is a real PDF (or HTML), and
writes its fetch.json record with method "manual", the registry address, the time, size and sha256.
The address must be one the registry lists for that state, so a manual file always maps to a source.
"""

from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from tools.fetch import ROOT, safe_name, sha256


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--state", required=True)
    parser.add_argument("--url", required=True, help="the registry address this file is a copy of")
    parser.add_argument("--file", type=Path, required=True)
    parser.add_argument("--move", action="store_true", help="move the file instead of copying it")
    args = parser.parse_args(argv)

    state = args.state.upper()
    registry = json.loads((ROOT / "sources" / "registry.json").read_text())
    sources = {s["url"]: s for s in registry.get(state, {}).get("sources", [])}
    if args.url not in sources:
        parser.error(f"{args.url} is not a registry source for {state}")
    head = args.file.read_bytes()[:512]
    kind = "pdf" if head.startswith(b"%PDF-") else "html" if b"<html" in head.lower() or b"<!doctype" in head.lower() else None
    if kind is None:
        parser.error(f"{args.file} is neither a PDF nor an HTML page")

    out_dir = ROOT / "sources" / "archive" / str(args.year) / state
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / safe_name(args.file.name)
    shutil.copyfile(str(args.file), str(target))
    if args.move:  # copy, verify, then delete: shutil.move's delete step failed on this shared mount
        if sha256(target) != sha256(args.file):
            parser.error(f"copy of {args.file} does not match; original kept")
        args.file.unlink()

    record = {"state": state, "title": sources[args.url].get("title"), "url": args.url, "kind": kind,
              "retrieved": datetime.now(timezone.utc).isoformat(), "ok": True, "method": "manual",
              "note": "saved by the maintainer from a browser; the agency refused automated downloads",
              "file": target.name, "bytes": target.stat().st_size, "sha256": sha256(target)}
    fetch_json = out_dir / "fetch.json"
    records = json.loads(fetch_json.read_text()) if fetch_json.exists() else []
    records = [r for r in records if r.get("url") != args.url] + [record]
    fetch_json.write_text(json.dumps(records, indent=2) + "\n")
    print(f"{state}: {target.name} recorded ({kind}, {record['bytes']} bytes, sha256 {record['sha256'][:12]})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
