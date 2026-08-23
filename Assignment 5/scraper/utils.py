import os


BASE_URL = "https://books.toscrape.com/"
PAGES = 3
OUTPUT_FILE = "books_data.csv"
DELAY = 1 
def save(content: str, filename: str):
    if not os.path.exists(os.path.join(os.path.dirname(__file__), '../cache/')):
        os.makedirs(os.path.join(os.path.dirname(__file__), '../cache/'))
    filepath = os.path.join(os.path.dirname(__file__), '../cache/' + filename)
    if os.path.exists(filepath):
        return False
    with open(filepath, 'w') as f:
        f.write(content)
    return True