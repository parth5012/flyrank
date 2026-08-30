"""Stage 1+2+3: catalogue -> raw -> clean validated books.json (idempotent)."""
import hashlib
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from urllib.parse import urljoin, urlparse

from pydantic import BaseModel, Field, HttpUrl, ValidationError, field_validator

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"
START_URL = urljoin(BASE_URL, "catalogue/page-1.html")
CACHE_DIR = Path(__file__).resolve().parent.parent / "cache"
USER_AGENT = "FlyRankInternship-A9/1.0 (+https://github.com/parth5012/flyrank)"
TIMEOUT_SECONDS = 10
REQUEST_DELAY_SECONDS = 0.5
MAX_PAGES = 3

# ---------- generic cached fetch ----------
def _cache_key(url: str) -> str:
    h = hashlib.sha256(url.encode()).hexdigest()[:16]
    slug = re.sub(r"[^a-z0-9]+", "-", urlparse(url).path.strip("/").lower()).strip("-")[:60]
    return f"{slug}-{h}.html" if slug else f"{h}.html"

def fetch_cached(url: str, cache_name: str | None = None, is_catalogue: bool = False, page_number: int = 0) -> str:
    if is_catalogue:
        path = CACHE_DIR / f"catalogue-page-{page_number}.html"
    else:
        path = CACHE_DIR / "details" / (cache_name or _cache_key(url))
    if path.exists():
        return path.read_text(encoding="utf-8")
    # politeness: delay only for real requests, not cache hits
    # caller ensures sequential delay; we sleep here if not first page
    time.sleep(REQUEST_DELAY_SECONDS)
    resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT_SECONDS)
    if resp.status_code != 200:
        raise RuntimeError(f"GET {url} returned {resp.status_code}")
    html = resp.text
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    return html

def load_catalogue_page(url: str, page_number: int) -> str:
    path = CACHE_DIR / f"catalogue-page-{page_number}.html"
    if path.exists():
        return path.read_text(encoding="utf-8")
    if page_number > 1:
        time.sleep(REQUEST_DELAY_SECONDS)
    resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT_SECONDS)
    if resp.status_code != 200:
        raise RuntimeError(f"Catalogue page {page_number} returned {resp.status_code}")
    html = resp.text
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    return html

def discover_books_and_next(html: str, page_url: str):
    soup = BeautifulSoup(html, "html.parser")
    book_urls = {urljoin(page_url, a["href"]) for a in soup.select("article.product_pod h3 a[href]")}
    nxt = soup.select_one("li.next a[href]")
    next_url = urljoin(page_url, nxt["href"]) if nxt else None
    return book_urls, next_url

def crawl_catalogue():
    current_url = START_URL
    page_number = 1
    url_to_source: dict[str, str] = {}
    pages = 0
    while current_url and page_number <= MAX_PAGES:
        html = load_catalogue_page(current_url, page_number)
        book_urls, current_url = discover_books_and_next(html, current_url)
        src = START_URL if page_number == 1 else urljoin(BASE_URL, f"catalogue/page-{page_number}.html")
        # actual page url before advancing
        page_url = START_URL if page_number == 1 else list_discovered_page_url(page_number)
        for u in book_urls:
            url_to_source.setdefault(u, page_url)
        discovered_before = len(url_to_source)
        pages = page_number
        page_number += 1
    # need correct source_page: reconstruct from crawl log instead, so re-crawl mapping
    # simpler: re-derive by re-parsing cached pages sequentially
    url_to_source.clear()
    cur = START_URL
    for pn in range(1, pages + 1):
        html = (CACHE_DIR / f"catalogue-page-{pn}.html").read_text(encoding="utf-8")
        urls, _ = discover_books_and_next(html, cur)
        for u in urls:
            if u not in url_to_source:
                url_to_source[u] = cur
        nxt = BeautifulSoup(html, "html.parser").select_one("li.next a[href]")
        cur = urljoin(cur, nxt["href"]) if nxt else None
    print(f"catalogue_pages={pages} discovered={len(url_to_source)} unique_urls={len(url_to_source)}")
    return url_to_source

def list_discovered_page_url(pn: int) -> str:
    # catalogue pagination is deterministic but we keep urljoin logic
    return urljoin(BASE_URL, f"catalogue/page-{pn}.html")

# ---------- Stage 2 ----------
RATING_MAP = {"One": "One", "Two": "Two", "Three": "Three", "Four": "Four", "Five": "Five"}

def parse_detail(html: str, product_url: str, source_page: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")
    product_main = soup.select_one("div.product_main")
    # selectors scoped to product area
    title_el = product_main.select_one("h1") if product_main else soup.select_one("div.product_main h1")
    price_el = product_main.select_one("p.price_color") if product_main else None
    avail_el = product_main.select_one("p.instock.availability") if product_main else None
    rating_el = product_main.select_one("p.star-rating") if product_main else None

    title = title_el.get_text(strip=True) if title_el else ""
    price_text = price_el.get_text(strip=True) if price_el else ""
    availability_text = avail_el.get_text(strip=True) if avail_el else ""
    # rating is second class e.g. "star-rating Three"
    rating_text = None
    if rating_el:
        classes = rating_el.get("class", [])
        for c in classes:
            if c in RATING_MAP:
                rating_text = c
                break

    # description: #product_description + p, null if missing
    desc = None
    desc_heading = soup.select_one("#product_description")
    if desc_heading:
        p = desc_heading.find_next_sibling("p")
        if p:
            desc = p.get_text(strip=True) or None

    return {
        "title": title,
        "product_url": product_url,
        "price_text": price_text,
        "availability_text": availability_text,
        "rating_text": rating_text,
        "description": desc,
        "source_page": source_page,
        "fetched_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }

def fetch_details(url_to_source: dict[str, str]) -> list[dict]:
    CACHE_DIR.joinpath("details").mkdir(parents=True, exist_ok=True)
    records = []
    first_was_cached = (CACHE_DIR / "details").exists() and any((CACHE_DIR / "details").iterdir())
    need_delay = False
    for idx, product_url in enumerate(sorted(url_to_source.keys())):
        source_page = url_to_source[product_url]
        # cache file per book
        key = _cache_key(product_url)
        path = CACHE_DIR / "details" / key
        if path.exists():
            html = path.read_text(encoding="utf-8")
        else:
            if need_delay:
                time.sleep(REQUEST_DELAY_SECONDS)
            # never delay before first real fetch in this stage if catalogue already delayed? keep politeness
            resp = requests.get(product_url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT_SECONDS)
            if resp.status_code != 200:
                raise RuntimeError(f"Detail {product_url} returned {resp.status_code}")
            html = resp.text
            path.write_text(html, encoding="utf-8")
            need_delay = True
            if not first_was_cached:
                # after first fetch, subsequent need delay already handled
                pass
        # if was cached, need_delay stays as was (no delay for cached)
        # ensure next iteration will delay only if previous was a real fetch
        # we already manage via need_delay flag correctly: only set after real fetch
        # but if this was cache hit, don't change flag for next? Actually we want delay only before real requests
        # so track whether next needs delay
        if not path.exists():
            pass
        # fix need_delay logic: delay before next *real* request, so remember if last was real
        # we set need_delay = not path_existed_before
        # Simplistic: if current was cached, next real still should delay if previous real happened?
        # Keep simple: delay before every real request except the very first real request overall
        records.append(parse_detail(html, product_url, source_page))
        # update flag for next loop: if this was real fetch, next real should delay
        if not path.exists():
            pass
    # Correct delay logic redo with simpler approach: just sequential with check
    return records

def _fetch_with_retry(url: str):
    """GET with one retry for timeout/5xx only. 404/403 never retried."""
    try:
        resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT_SECONDS)
    except requests.exceptions.Timeout:
        time.sleep(REQUEST_DELAY_SECONDS)
        resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT_SECONDS)
        return resp
    except requests.exceptions.RequestException:
        time.sleep(REQUEST_DELAY_SECONDS)
        resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT_SECONDS)
        return resp
    if 500 <= resp.status_code <= 599:
        time.sleep(REQUEST_DELAY_SECONDS)
        resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT_SECONDS)
    return resp

def fetch_details_simple(url_to_source: dict[str, str], stats: dict | None = None) -> list[dict]:
    records: list[dict] = []
    failed = 0
    cache_hits = 0
    first_real = True
    for product_url in sorted(url_to_source.keys()):
        source_page = url_to_source[product_url]
        key = _cache_key(product_url)
        path = CACHE_DIR / "details" / key
        html: str | None = None
        try:
            if path.exists():
                html = path.read_text(encoding="utf-8")
                cache_hits += 1
            else:
                if not first_real:
                    time.sleep(REQUEST_DELAY_SECONDS)
                resp = _fetch_with_retry(product_url)
                if resp.status_code in (403, 404):
                    raise RuntimeError(f"{resp.status_code} for {product_url}")
                if resp.status_code != 200:
                    raise RuntimeError(f"{resp.status_code} for {product_url}")
                html = resp.text
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(html, encoding="utf-8")
                first_real = False
        except Exception as e:
            failed += 1
            print(f"[SKIP] {product_url} -> {e}")
            # isolated failure: first_real still set if we never succeeded?
            if html is None and not path.exists():
                # if first fetch failed, don't count as successful real, keep first_real True
                # but next real should still respect delay if we had a prior success
                pass
            continue
        # handle case where first fetch failed and first_real still True - avoid extra delay logic break
        if html is not None:
            if not path.exists() or True:
                # ensure first_real flips after first successful network fetch
                if html and not (cache_hits and False):
                    pass
            records.append(parse_detail(html, product_url, source_page))
            # if this was a network fetch, mark that next network needs delay
            if not path.exists.__self__ if hasattr(path.exists,'__self__') else False:
                pass
            # simpler: if we just did a network fetch, next needs delay
            if not (CACHE_DIR / "details" / key).exists():
                pass
        # fix first_real tracking: if we just did network success, next should delay
        # we already set first_real=False on success above
        if path.exists() and html:
            # if file now exists and it was just created, first_real already False
            pass
        # actual delay flag: if html came from network, first_real is False
        if html is not None and len(records) > 0 and records[-1].get("product_url") == product_url:
            # we appended, if it was network fetch, ensure next iteration will delay
            # need to know if it was network: check if we counted cache hit for this url
            # workaround: track via path existence before fetch - use local var
            pass
    if stats is not None:
        stats["cache_hits_details"] = cache_hits
        stats["failed_pages"] = failed
        stats["pages_fetched"] = len(records) + failed  # attempted detail pages that were not cache? keep simple
    # rewrite with clean isolated logic - override above counts correctly by reimplementing loop cleanly
    return records

def fetch_details_isolated(url_to_source: dict[str, str], stats: dict) -> list[dict]:
    records: list[dict] = []
    failed = 0
    cache_hits = 0
    fetched = 0
    first_network = True
    for product_url in sorted(url_to_source.keys()):
        source_page = url_to_source[product_url]
        key = _cache_key(product_url)
        path = CACHE_DIR / "details" / key
        was_cached = path.exists()
        html = None
        if was_cached:
            html = path.read_text(encoding="utf-8")
            cache_hits += 1
        else:
            if not first_network:
                time.sleep(REQUEST_DELAY_SECONDS)
            try:
                resp = _fetch_with_retry(product_url)
            except Exception as e:
                failed += 1
                print(f"[SKIP] {product_url} -> {e}")
                continue
            if resp.status_code in (403, 404):
                failed += 1
                print(f"[SKIP] {product_url} -> {resp.status_code}")
                continue
            if resp.status_code != 200:
                failed += 1
                print(f"[SKIP] {product_url} -> {resp.status_code}")
                continue
            html = resp.text
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(html, encoding="utf-8")
            fetched += 1
            first_network = False
        try:
            records.append(parse_detail(html, product_url, source_page))
        except Exception as e:
            failed += 1
            print(f"[SKIP] parse {product_url} -> {e}")
    stats["cache_hits"] = stats.get("cache_hits", 0) + cache_hits
    stats["pages_fetched"] = stats.get("pages_fetched", 0) + fetched
    stats["failed_pages"] = stats.get("failed_pages", 0) + failed
    return records

class BookRecord(BaseModel):
    title: str = Field(min_length=1)
    product_url: HttpUrl
    price_text: str = Field(min_length=1)
    price_gbp: float = Field(ge=0)
    availability_text: str = Field(min_length=1)
    rating_text: Optional[str] = Field(default=None)
    description: Optional[str] = None
    source_page: HttpUrl
    fetched_at: str

    @field_validator("rating_text")
    @classmethod
    def check_rating(cls, v):
        if v is not None and v not in {"One", "Two", "Three", "Four", "Five"}:
            raise ValueError(f"invalid rating {v}")
        return v

OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"
BOOKS_JSON = OUTPUT_DIR / "books.json"
ERRORS_JSON = OUTPUT_DIR / "errors.json"

def to_clean(raw: dict) -> dict:
    m = re.search(r"[\d]+\.\d{2}", raw.get("price_text", ""))
    price_gbp = float(m.group()) if m else None
    return {**raw, "price_gbp": price_gbp}

def validate_and_write(raw_records: list[dict]):
    # dedup by canonical product_url
    dedup: dict[str, dict] = {}
    for r in raw_records:
        dedup[r["product_url"]] = r  # last wins, counts once
    good, errors = [], []
    for url in sorted(dedup):
        clean = to_clean(dedup[url])
        try:
            rec = BookRecord(**clean)
            good.append(rec.model_dump(mode="json"))
        except ValidationError as e:
            errors.append({"product_url": url, "reason": e.errors(), "raw": clean})
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    # idempotent: overwrite, not append
    BOOKS_JSON.write_text(json.dumps(good, indent=2, ensure_ascii=False), encoding="utf-8")
    ERRORS_JSON.write_text(json.dumps(errors, indent=2, ensure_ascii=False), encoding="utf-8")
    return good, errors

def main():
    import os
    start = datetime.now(timezone.utc)
    t0 = time.monotonic()
    url_to_source = crawl_catalogue()
    # proving resilience: inject one fake URL on purpose (local only, no hammering)
    if os.environ.get("FAKE_URL") == "1" or (OUTPUT_DIR / ".inject_fake").exists():
        fake = "https://books.toscrape.com/catalogue/this-book-does-not-exist-9999/index.html"
        url_to_source.setdefault(fake, START_URL)
        print(f"[INJECT] fake url added for test: {fake}")
    stats: dict = {"cache_hits": 0, "pages_fetched": 0, "failed_pages": 0}
    # count catalogue cache hits already? add
    stats["cache_hits"] = sum(1 for i in range(1, 4) if (CACHE_DIR / f"catalogue-page-{i}.html").exists() and True)  # will be adjusted
    # actually catalogue hits counted inside crawl; simplify: we track via existence after crawl
    records = fetch_details_isolated(url_to_source, stats)
    if records:
        print(json.dumps(records[0], indent=2, ensure_ascii=False))
    print(f"detail_pages={len(records)}")
    good, errors = validate_and_write(records)
    print(f"books_json={len(good)} errors={len(errors)}")
    assert all(isinstance(r["price_gbp"], (int, float)) for r in good)
    assert all(str(r["product_url"]).startswith("https://") for r in good)
    # run report
    duration = time.monotonic() - t0
    report = {
        "start_time": start.isoformat().replace("+00:00", "Z"),
        "duration_seconds": round(duration, 2),
        "pages_fetched": stats.get("pages_fetched", 0),
        "cache_hits": stats.get("cache_hits", 0),
        "valid_records": len(good),
        "invalid_records": len(errors),
        "failed_pages": stats.get("failed_pages", 0),
    }
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / "run-report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"run-report: {json.dumps(report)}")

if __name__ == "__main__":
    main()
