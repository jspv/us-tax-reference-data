"""Source documents on demand: find a durable public copy of each, and pull them when wanted.

The data files cite each source by its agency address; `sources/archive/<year>/<ST>/fetch.json`
records the sha256 of the exact file that was read. The PDFs themselves are large and are not needed
to use the data, so a checkout can leave them out and pull them when wanted.

    uv run python -m tools.sources pull --year 2025 [--state ST ...]
        For each recorded source missing locally: download it from its Internet Archive copy
        (`archived_url`) or, failing that, the agency address; keep it only if its sha256 matches the
        record. Then convert the PDFs (tools.convert) so tools.validate can check figure presence.
        A file that no longer matches (the agency replaced it, and no archived copy exists) is reported,
        not kept.

    uv run python -m tools.sources archive --year 2025 [--state ST ...] [--save]
        For each local PDF, look up the Internet Archive's captures of its address and record
        `archived_url` when a capture has exactly the same content (the capture index's SHA-1 digest).
        With --save, ask the Archive to capture any address that has no matching copy, then look again.
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ARCHIVE = ROOT / "sources" / "archive"
CDX = "https://web.archive.org/cdx/search/cdx"
AGENT = "tax-reference-data source puller (+https://github.com/jspv)"
PAUSE_SECONDS = 6


def get(url: str, timeout: int = 120) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def sha1_base32(data: bytes) -> str:
    return base64.b32encode(hashlib.sha1(data).digest()).decode()


def records(year: int, states: list[str]):
    """(state folder, fetch.json path, its records) for each requested jurisdiction."""
    for state in states or sorted(p.name for p in (ARCHIVE / str(year)).iterdir() if p.is_dir()):
        path = ARCHIVE / str(year) / state / "fetch.json"
        if path.exists():
            yield path.parent, path, json.loads(path.read_text())


def matching_capture(url: str, digest: str) -> str | None:
    query = urllib.parse.urlencode({"url": url, "output": "json", "filter": "statuscode:200"})
    rows = json.loads(get(f"{CDX}?{query}") or b"[]")
    for row in rows[1:]:
        timestamp, original, row_digest = row[1], row[2], row[5]
        if row_digest == digest:
            return f"https://web.archive.org/web/{timestamp}id_/{original}"
    return None


def archive(year: int, states: list[str], save: bool) -> int:
    missing = 0
    for folder, path, entries in records(year, states):
        changed = False
        for entry in entries:
            if not entry.get("ok") or not entry.get("file", "").endswith(".pdf") or entry.get("archived_url"):
                continue
            local = folder / entry["file"]
            if not local.exists():
                continue
            digest = sha1_base32(local.read_bytes())
            addresses = [entry["url"]] + ([entry["final_url"]] if entry.get("final_url") not in (None, entry["url"]) else [])
            found = None
            for address in addresses:
                time.sleep(PAUSE_SECONDS)
                try:
                    found = matching_capture(address, digest)
                except Exception as error:  # the index is sometimes slow; report and go on
                    print(f"{folder.name}: {entry['file']}: lookup failed: {error}")
                if found:
                    break
            if not found and save:
                try:
                    get(f"https://web.archive.org/save/{addresses[-1]}", timeout=300)
                    time.sleep(20)
                    found = matching_capture(addresses[-1], digest)
                except Exception as error:
                    print(f"{folder.name}: {entry['file']}: save failed: {error}")
            if found:
                entry["archived_url"] = found
                changed = True
                print(f"{folder.name}: {entry['file']}: {found}")
            else:
                missing += 1
                print(f"{folder.name}: {entry['file']}: no archived copy with the same content")
        if changed:
            path.write_text(json.dumps(entries, indent=2) + "\n")
    print(f"{missing} file(s) without an archived copy")
    return 0


def pull(year: int, states: list[str]) -> int:
    failed, converted = [], set()
    for folder, _, entries in records(year, states):
        for entry in entries:
            if not entry.get("ok") or not entry.get("file") or not entry.get("sha256"):
                continue
            local = folder / entry["file"]
            if local.exists() and hashlib.sha256(local.read_bytes()).hexdigest() == entry["sha256"]:
                continue
            got = None
            for address in [entry.get("archived_url"), entry["url"]]:
                if not address:
                    continue
                try:
                    data = get(address)
                except Exception as error:
                    print(f"{folder.name}: {entry['file']}: {address}: {error}")
                    continue
                if hashlib.sha256(data).hexdigest() == entry["sha256"]:
                    got = data
                    break
                print(f"{folder.name}: {entry['file']}: {address} serves a different file now")
            if got is None:
                failed.append(f"{folder.name}/{entry['file']}")
                continue
            local.write_bytes(got)
            converted.add(folder.name)
            print(f"{folder.name}: {entry['file']}: ok")
    for state in sorted(converted):
        subprocess.run([sys.executable, "-m", "tools.convert", "--year", str(year), "--state", state], cwd=ROOT, check=False)
    if failed:
        print("not pulled (no matching copy; fetch by hand or run tools.fetch for a newer edition): " + " ".join(failed), file=sys.stderr)
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("command", choices=("pull", "archive"))
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--state", action="append", default=[])
    parser.add_argument("--save", action="store_true", help="archive: ask the Internet Archive to capture addresses with no matching copy")
    args = parser.parse_args(argv)
    states = [s.upper() for s in args.state]
    return archive(args.year, states, args.save) if args.command == "archive" else pull(args.year, states)


if __name__ == "__main__":
    raise SystemExit(main())
