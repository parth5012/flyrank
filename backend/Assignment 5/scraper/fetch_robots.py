import requests
import os
from url import BASE_URL
from utils import save


def fetch_robots(url:str =BASE_URL + "robots.txt"):
    response = requests.get(url)
    return response.text

if __name__ == "__main__":
    content = fetch_robots()
    save(content, "robots.txt")
