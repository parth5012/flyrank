"""Stage 1: Discover all book URLs across catalogue pages 1-3."""
import time
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"
START_URL = urljoin(BASE_URL, "catalogue/page-1.html")
CACHE_DIR = Path(__file__).resolve().parent.parent / "cache"
USER_AGENT = "FlyRankInternship-A9/1.0 (+https://github.com/parth5012/flyrank)"
TIMEOUT_SECONDS = 10
REQUEST_DELAY_SECONDS = 0.5
MAX_PAGES = 3


def cache_path(page_number: int) -> Path:
    return CACHE_DIR / f"catalogue-page-{page_number}.html"


def load_page(url: str, page_number: int) -> str:
    """Return HTML from cache if present, else fetch (with delay) and cache."""
    path = cache_path(page_number)
    if path.exists():
        html = path.read_text(encoding="utf-8")
        print(f"CACHE HIT page={page_number} size={len(html.encode('utf-8'))}")
        return html

    # Only delay before real network requests, never for cache hits
    if page_number > 1:
        time.sleep(REQUEST_DELAY_SECONDS)

    print(f"FETCH page={page_number} url={url}")
    resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=TIMEOUT_SECONDS)
    if resp.status_code != 200:
        raise RuntimeError(f"Catalogue page {page_number} returned {resp.status_code}")
    html = resp.text
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    print(f"FETCHED page={page_number} size={len(html.encode('utf-8'))}")
    return html


def discover_books_and_next(html: str, page_url: str):
    """Parse with BeautifulSoup, resolve relative hrefs via urljoin, find next link."""
    soup = BeautifulSoup(html, "html.parser")
    book_urls = {
        urljoin(page_url, a["href"])
        for a in soup.select("article.product_pod h3 a[href]")
    }
    next_el = soup.select_one("li.next a[href]")
    next_url = urljoin(page_url, next_el["href"]) if next_el else None
    return book_urls, next_url


def crawl_catalogue():
    current_url = START_URL
    page_number = 1
    discovered_urls: list[str] = []

    while current_url and page_number <= MAX_PAGES:
        html = load_page(current_url, page_number)
        book_urls, current_url = discover_books_and_next(html, current_url)
        discovered_urls.extend(book_urls)
        page_number += 1

    unique_urls = set(discovered_urls)
    # CHECKPOINT — exact format required
    print(f"catalogue_pages={page_number - 1} discovered={len(discovered_urls)} unique_urls={len(unique_urls)}")
    return unique_urls


def main():
    crawl_catalogue()


if __name__ == "__main__":
    main()
