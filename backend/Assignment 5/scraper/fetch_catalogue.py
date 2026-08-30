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


def cache_path(page_number):
    return CACHE_DIR / f"catalogue-page-{page_number}.html"


def load_page(url, page_number):
    path = cache_path(page_number)
    if path.exists():
        html = path.read_text(encoding="utf-8")
        print(f"CACHE HIT page={page_number} size={len(html.encode('utf-8'))}")
        return html

    if page_number > 1:
        import time
        time.sleep(REQUEST_DELAY_SECONDS)

    print(f"FETCH page={page_number} url={url}")
    response = requests.get(
        url,
        headers={"User-Agent": USER_AGENT},
        timeout=TIMEOUT_SECONDS,
    )
    if response.status_code != 200:
        raise RuntimeError(f"Catalogue page {page_number} returned {response.status_code}")

    html = response.text
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    print(f"FETCHED page={page_number} size={len(html.encode('utf-8'))}")
    return html


def discover_books_and_next(html, page_url):
    soup = BeautifulSoup(html, "html.parser")
    book_urls = {
        urljoin(page_url, link["href"])
        for link in soup.select("article.product_pod h3 a[href]")
    }
    next_link = soup.select_one("li.next a[href]")
    next_url = urljoin(page_url, next_link["href"]) if next_link else None
    return book_urls, next_url


def crawl_catalogue():
    current_url = START_URL
    page_number = 1
    discovered_urls = []

    while current_url and page_number <= MAX_PAGES:
        html = load_page(current_url, page_number)
        book_urls, current_url = discover_books_and_next(html, current_url)
        discovered_urls.extend(book_urls)
        page_number += 1

    unique_urls = set(discovered_urls)
    print(
        f"catalogue_pages={page_number - 1} "
        f"discovered={len(discovered_urls)} unique_urls={len(unique_urls)}"
    )
    return unique_urls


if __name__ == "__main__":
    crawl_catalogue()