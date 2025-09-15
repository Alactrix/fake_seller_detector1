import requests
from bs4 import BeautifulSoup
import re

def get_reviews_trustpilot(domain: str, max_reviews=10):
    base = "https://www.trustpilot.com"
    search_url = f"{base}/search?query={domain}"

    try:
        # Step 1: Get the company page
        r = requests.get(search_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(r.text, "html.parser")
        link = soup.find("a", href=re.compile("/review/"))
        if not link:
            return []

        company_url = base + link['href']

        # Step 2: Get the first page of reviews
        r2 = requests.get(company_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        soup2 = BeautifulSoup(r2.text, "html.parser")
        blocks = soup2.find_all("p", {"data-consumer-review-title-typography": "true"})

        reviews = [b.text.strip() for b in blocks if b.text.strip()]
        return reviews[:max_reviews]

    except Exception as e:
        return [f"(Error getting reviews: {str(e)})"]
