# FlyRank — Books to Scrape (Assignment 5)

Polite, cached, validated scraper for https://books.toscrape.com — catalogue pages 1-3 → 60 books.

## Target classification (Stage 0)

**Public demo site, no auth/paywall/login, static HTML.** `books.toscrape.com` is explicitly for scraping practice. No browser needed — all data (title, price, availability, rating, description) is in the initial HTML response; no JS rendering required. Respects `robots.txt` (crawl allowed for catalogue).

## Run (one command, <5 min, stranger-friendly)

```bash
git clone https://github.com/parth5012/flyrank.git
cd flyrank/Assignment\ 5
pip install requests beautifulsoup4 pydantic
# or: uv sync  (if uv available)
python src/main.py
# outputs: output/books.json, output/errors.json, output/run-report.json
# second run uses cache, no extra requests:
python src/main.py
```

Lane: **Python / BeautifulSoup + Pydantic**. Requires Python 3.11+.

Install: `pip install -r requirements.txt` or `pip install requests beautifulsoup4 pydantic` (no browser/driver).

## Record schema (Pydantic)

```python
class BookRecord(BaseModel):
    title: str                          # required, non-empty
    product_url: HttpUrl                # canonical, https://books.toscrape.com/...
    price_text: str                     # raw "£51.77"
    price_gbp: float                    # clean 51.77  (kept side-by-side)
    availability_text: str              # "In stock (22 available)"
    rating_text: Optional[str]          # One|Two|Three|Four|Five | None
    description: Optional[str]          # null when page has no description
    source_page: HttpUrl                # catalogue page where URL discovered
    fetched_at: str                     # ISO8601 UTC
```

Dedup: `product_url` is canonical identity — same URL counts once. Invalid records → `output/errors.json` with reason, never into `books.json`. `books.json` is overwritten (idempotent) — 60 after every run, not 120.

## Politeness rules

- **User-Agent:** `FlyRankInternship-A9/1.0 (+https://github.com/parth5012/flyrank)`
- **Delay:** 0.5s between *real* requests; cached pages have no delay (never leave disk)
- **Timeout:** 10s per request
- **Cache:** `cache/catalogue-page-*.html` + `cache/details/*.html` (path-independent, gitignored)
- **Retry:** one retry for timeout / 5xx only; never retry 404/403
- **Scope:** selectors aimed at `div.product_main` / `p.price_color` etc., not first price on whole doc
- **Failure isolation:** one broken detail page is `[SKIP]`-logged, 59/60 survive

## Why no browser

The data is already in the HTML the server sends, so a browser would only add cost — extra CPU, memory, and latency for JS rendering that this site doesn't need. `requests + BeautifulSoup` is faster, cheaper, and deterministic.

## Limitation

Honest: scraper is coupled to current `books.toscrape.com` DOM (`div.product_main`, `#product_description`). A site redesign or anti-bot change would break selectors; no headless fallback is included by design.

## Ethics

Use an official API when one exists; never bypass logins, paywalls, or blocks; collect only what you need. This project hits only the public demo catalogue (3 pages, 60 details) with caching and 0.5s politeness, and respects 403/404 as "do not retry."

## Proof — real run-report.json

```json
{
  "start_time": "2026-08-25T13:37:15.434942Z",
  "duration_seconds": 0.78,
  "pages_fetched": 0,
  "cache_hits": 63,
  "valid_records": 60,
  "invalid_records": 0,
  "failed_pages": 0
}
```

With one injected fake URL (`FAKE_URL=1`): `failed_pages: 1`, `books.json` still 60:

```json
{
  "start_time": "2026-08-25T13:37:05.872910Z",
  "duration_seconds": 1.86,
  "pages_fetched": 0,
  "cache_hits": 63,
  "valid_records": 60,
  "invalid_records": 0,
  "failed_pages": 1
}
```
