"""Download source booklets with a headless Chromium browser.

PDFs, and agency web pages (kind 'html': the HTML and its visible text as <stem>.page.txt).
One path only (decision 2026-11-06): some agencies refuse plain HTTP clients, a browser works for
all of them. A download that is not a real PDF is a failure, recorded, and the jurisdiction goes
on the manual list.

    uv run python -m tools.fetch --year 2025 --state GA [--state UT ...]
    uv run python -m tools.fetch --year 2025 --all

Writes sources/archive/<year>/<ST>/<file>.pdf and fetch.json (one record per source: the address
asked for, the final address after redirects, time, HTTP status, sha256, size, ok).
"""

from __future__ import annotations

import argparse
import base64
import glob
import hashlib
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAUSE_SECONDS = 5


def chromium_path() -> str:
    """Chromium executable: $TAXREF_CHROMIUM, else the newest Playwright-cached build."""
    env = os.environ.get("TAXREF_CHROMIUM")
    if env:
        return env
    found = sorted(glob.glob(os.path.expanduser("~/.cache/ms-playwright/chromium-*/chrome-linux/chrome")))
    if not found:
        raise SystemExit("no Chromium found: set TAXREF_CHROMIUM or run `playwright install chromium`")
    return found[-1]


def safe_name(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9._-]", "_", name) or "booklet.pdf"


def is_pdf(path: Path) -> bool:
    with path.open("rb") as handle:
        return handle.read(5) == b"%PDF-"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


_READ_INLINE = """async () => {
  const r = await fetch(location.href, {credentials: 'include'});
  const bytes = new Uint8Array(await r.arrayBuffer());
  let text = '';
  for (let i = 0; i < bytes.length; i += 0x8000) text += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
  return btoa(text);
}"""


def inline_pdf_bytes(page) -> bytes:
    """The PDF behind the page Chromium is showing in its viewer, read with the browser's own
    network stack and cookies (same origin, so no CORS)."""
    return base64.b64decode(page.evaluate(_READ_INLINE))


def fetch_page(page, state: str, source: dict, out_dir: Path) -> dict:
    """Save an agency web page (kind "html"): its HTML and its visible text, page-marked like a PDF's."""
    url = source["url"]
    record = {"state": state, "title": source.get("title"), "url": url, "kind": "html",
              "retrieved": datetime.now(timezone.utc).isoformat(), "ok": False}
    out_dir.mkdir(parents=True, exist_ok=True)
    try:
        response = page.goto(url, wait_until="domcontentloaded", timeout=90000)
        page.wait_for_timeout(4000)  # let scripts fill the page; waiting for an idle network timed out on some agencies
        record["status"] = response.status if response else None
        record["final_url"] = page.url
        if response is None or not response.ok:
            record["error"] = f"HTTP {record['status']}"
            return record
        html = page.content()
        text = page.evaluate("() => document.body.innerText.length > 0 && document.body.textContent.length > 2 * document.body.innerText.length ? document.body.textContent : document.body.innerText")  # collapsed panels hide text from innerText
    except Exception as error:  # noqa: BLE001
        record["error"] = str(error).splitlines()[0][:300]
        return record
    address = Path(url.split("?")[0].rstrip("/"))
    stem = safe_name(address.stem or "page")
    if stem.lower() in {"index", "default", "page", "home"}:  # a generic name would collide with the jurisdiction's other pages
        stem = safe_name(f"{address.parent.name}-{stem}")
    target = out_dir / f"{stem}.html"
    target.write_text(html)
    (out_dir / f"{stem}.page.txt").write_text("\n=====PAGE 1=====\n" + text)
    if len(text.strip()) < 200:
        record["error"] = "page has almost no text (blocked, or built by a script that did not run)"
        return record
    record.update(file=target.name, bytes=len(html.encode()), sha256=sha256(target), text_file=f"{stem}.page.txt", ok=True)
    return record


def plain_get(url: str) -> tuple[int, bytes, str]:
    """A plain HTTP GET (no browser), for agencies that refuse headless Chromium but serve simple clients
    (Maine, Kentucky, Colorado in 2026). Identifies itself honestly; no browser disguise."""
    import urllib.request
    request = urllib.request.Request(url, headers={"User-Agent": "tax-reference-data fetch (python urllib)", "Accept": "*/*"})
    with urllib.request.urlopen(request, timeout=90) as response:
        return response.status, response.read(), response.geturl()


def fetch_one(page, state: str, source: dict, out_dir: Path) -> dict:
    """Download one source document. Returns the fetch record; never raises for a bad download.

    A link either triggers a browser download (Content-Disposition: attachment) or shows the PDF
    inline; both are handled, the second by reading the response body.
    """
    url = source["url"]
    record = {"state": state, "title": source.get("title"), "url": url,
              "retrieved": datetime.now(timezone.utc).isoformat(), "ok": False}
    out_dir.mkdir(parents=True, exist_ok=True)
    captured: dict = {}
    page.once("download", lambda download: captured.setdefault("download", download))
    body = None
    name = None
    try:
        try:
            response = page.goto(url, wait_until="commit", timeout=60000)
        except Exception as error:  # noqa: BLE001 (Playwright raises for download navigations)
            if "Download is starting" not in str(error):
                raise
            response = None
        if response is not None:
            record["status"] = response.status
            record["final_url"] = response.url  # where the address led after redirects
            if response.ok:
                body = response.body()
                name = Path(response.url.split("?")[0]).name or "document.pdf"
                if not body.startswith(b"%PDF-") and b"pdf_embedder" in body:
                    body = inline_pdf_bytes(page)  # Chromium's PDF viewer wrapper, not the file
        if body is None or not body.startswith(b"%PDF-"):
            for _ in range(60):  # up to 30 s for a download to be announced
                if "download" in captured:
                    break
                page.wait_for_timeout(500)
            download = captured.get("download")
            if download is not None:
                name = download.suggested_filename
                record["final_url"] = download.url
                path = download.path()
                body = Path(path).read_bytes() if path else None
    except Exception as error:  # noqa: BLE001
        record["error"] = str(error).splitlines()[0][:300]
        return record
    if body is None or not body.startswith(b"%PDF-"):
        try:  # fallback: the browser was refused or got no PDF; try a plain request
            status, plain_body, final = plain_get(url)
            if plain_body.startswith(b"%PDF-"):
                body, record["method"], record["final_url"], record["status"] = plain_body, "plain_http", final, status
                name = name or Path(final.split("?")[0]).name
        except Exception as error:  # noqa: BLE001
            record["plain_http_error"] = str(error)[:200]
    if body is None:
        record["error"] = f"no document returned (HTTP {record.get('status')})"
        return record
    record.setdefault("method", "browser")
    if name is None or Path(name).stem.lower() in ("download", "open"):  # ".../download", ".../open" links
        name = url.rstrip("/").rsplit("/", 2)[-2]
    if not name.lower().endswith(".pdf"):
        name += ".pdf"
    target = out_dir / safe_name(name)
    target.write_bytes(body)
    record["file"] = target.name
    record["bytes"] = len(body)
    if not is_pdf(target):
        record["error"] = "downloaded file is not a PDF"
        target.rename(target.with_suffix(".notpdf"))
        return record
    record["sha256"] = sha256(target)
    record["ok"] = True
    return record


def warm_up(page, forms_page_url: str | None) -> None:
    """Open the agency's forms page first, as a person would (some agencies require it)."""
    if not forms_page_url:
        return
    try:
        page.goto(forms_page_url, wait_until="domcontentloaded", timeout=45000)
    except Exception:  # noqa: BLE001 (a failed warm-up is not a failed fetch)
        pass


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--year", type=int, required=True)
    parser.add_argument("--state", action="append", default=[], help="two-letter code; repeatable")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--refresh", action="store_true", help="download again even when a good copy is on record")
    parser.add_argument("--registry", type=Path, default=ROOT / "sources" / "registry.json")
    parser.add_argument("--archive", type=Path, default=ROOT / "sources" / "archive")
    args = parser.parse_args(argv)

    registry = json.loads(args.registry.read_text())
    states = sorted(registry) if args.all else [s.upper() for s in args.state]
    if not states:
        parser.error("give --state or --all")
    missing = [s for s in states if s not in registry]
    if missing:
        parser.error(f"not in the registry: {', '.join(missing)}")

    from playwright.sync_api import sync_playwright  # imported late: the validators don't need it

    failures: list[str] = []
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(executable_path=chromium_path(), headless=True)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()
        for index, state in enumerate(states):
            if index:
                time.sleep(PAUSE_SECONDS)
            out_dir = args.archive / str(args.year) / state
            previous = {}
            if (out_dir / "fetch.json").exists():
                previous = {r["url"]: r for r in json.loads((out_dir / "fetch.json").read_text())}
            records = []
            warm_up(page, registry[state].get("forms_page_url"))
            for number, source in enumerate(registry[state]["sources"]):
                kept = previous.get(source["url"])
                if kept and kept.get("ok") and (out_dir / kept["file"]).exists() and not args.refresh:
                    records.append(kept)  # a good copy is on record: never replace it with a failed retry
                    continue
                if number:
                    time.sleep(PAUSE_SECONDS)
                fetcher = fetch_page if source.get("kind") == "html" else fetch_one
                records.append(fetcher(page, state, source, out_dir))
            current = {source["url"] for source in registry[state]["sources"]}
            records += [r for url, r in previous.items() if url not in current]  # keep records this registry copy doesn't list
            (out_dir / "fetch.json").write_text(json.dumps(records, indent=2) + "\n")
            for record in records:
                status = "ok" if record["ok"] else f"FAILED: {record.get('error')}"
                print(f"{state}: {record['url'].rsplit('/', 2)[-2] + '/' + record['url'].rsplit('/', 1)[-1]} {status}")
            if not all(record["ok"] for record in records):
                failures.append(state)
        browser.close()
    if failures:
        print("manual list (save these by hand): " + " ".join(failures), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
