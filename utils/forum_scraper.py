# utils/forum_scraper.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, quote


def search_reddit_forum_mentions(domain: str) -> (bool, list):
    try:
        # Extract brand keyword (e.g., "blauxstore" from "blauxstore.com")
        parsed_url = urlparse(domain)
        netloc = parsed_url.netloc or parsed_url.path
        keyword = netloc.replace("www.", "").split('.')[0].strip().lower()

        # Google Search URL
        query = f'"{keyword}" site:reddit.com/r/scams'
        search_url = f"https://www.google.com/search?q={quote(query)}"

        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/91.0.4472.124 Safari/537.36"
            )
        }

        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        results = []
        for a in soup.select("a"):
            href = a.get("href")
            if href and "reddit.com/r/scams" in href:
                results.append({
                    "url": href,
                    "text": a.get_text(strip=True)
                })

        return (len(results) > 0), results

    except Exception as e:
        print(f"[ERROR] Forum scraper failed: {e}")
        return False, []
