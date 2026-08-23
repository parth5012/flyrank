import requests
from utils import save,BASE_URL


CATALOGUE_URL = BASE_URL + "catalogue/page-{}.html"

def fetch_page(page_num):
    """Fetch a single page from Books to Scrape."""
    url = CATALOGUE_URL.format(page_num)
    print(f"[PAGE {page_num}] Fetching: {url}")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    created = save(response.text, f"catalogue_page_{page_num}.html")
    if created:
        print(f"[PAGE {page_num}] Saved: {url}")
        return "Success!!"
    else:
        print(f"[PAGE {page_num}] Already exists: {url}")
        return "Cache Hit!!"

if __name__ == "__main__":
    for page_num in range(1, PAGES + 1):
        fetch_page(page_num)