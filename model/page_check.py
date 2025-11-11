from utils.net_utils import get_html_content
from bs4 import BeautifulSoup

def check_page_features(url: str) -> dict:
    try:
        html = get_html_content(url)
        soup = BeautifulSoup(html, 'html.parser')

        # <h1> presence
        has_h1 = bool(soup.find('h1'))

        # Sufficient text
        page_text = soup.get_text(separator=' ')
        is_informative = len(page_text.strip()) > 500

        # Look for Contact/About/Return links in footer/nav
        footer_nav = soup.find_all(['footer', 'nav', 'a'])
        links_text = " ".join([tag.get_text().lower() for tag in footer_nav])
        has_important_links = any(keyword in links_text for keyword in [
            'contact', 'about', 'privacy', 'terms', 'return', 'refund'
        ])

        # Check for product-like elements (very naive check)
        product_like_divs = soup.find_all('div', class_=lambda x: x and 'product' in x.lower())
        has_product_listings = len(product_like_divs) >= 3

        # Social media presence
        social_links = ['facebook.com', 'instagram.com', 'X.com', 'linkedin.com']
        has_social_links = any(link in html for link in social_links)

        return {
            "has_h1": has_h1,
            "is_informative": is_informative,
            "has_important_links": has_important_links,
            "has_product_listings": has_product_listings,
            "has_social_links": has_social_links
        }

    except Exception as e:
        return {
            "error": str(e)
        }
