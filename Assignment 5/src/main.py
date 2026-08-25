"""Stage 1+2: catalogue discovery + raw detail records."""
import hashlib
import json
import re
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

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

def fetch_details_simple(url_to_source: dict[str, str]) -> list[dict]:
    records = []
    first_real = True
    for product_url in sorted(url_to_source.keys()):
        source_page = url_to_source[product_url]
        key = _cache_key(product_url)
        path = CACHE_DIR / "details" / key
        if path.exists():
            html = path.read_text(encoding="utf-8")
        else:
            if not first_real:
                time.sleep(REQUEST_DELAY_SECONDS)
            resp = requests.get(product_url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT_SECONDS)
            if resp.status_code != 200:
                raise RuntimeError(f"Detail {product_url} returned {resp.status_code}")
            html = resp.text
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(html, encoding="utf-8")
            first_real = False
        records.append(parse_detail(html, product_url, source_page))
    return records

def main():
    url_to_source = crawl_catalogue()
    records = fetch_details_simple(url_to_source)
    # checkpoint
    if records:
        print(json.dumps(records[0], indent=2, ensure_ascii=False))
    print(f"detail_pages={len(records)}")

if __name__ == "__main__":
    main()
