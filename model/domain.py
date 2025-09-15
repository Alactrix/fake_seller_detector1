import re
import whois
from datetime import datetime

SUSPICIOUS_KEYWORDS = ['cheap', 'offer', 'deal', 'discount', 'promo', 'get', 'free']

def is_domain_suspicious(url: str) -> bool:
    domain = extract_domain(url)
    return any(keyword in domain for keyword in SUSPICIOUS_KEYWORDS)

def extract_domain(url: str) -> str:
    return re.sub(r'^www\.', '', re.findall(r'://([^/]+)/?', url)[0])

def get_domain_age_days(url: str) -> int:
    try:
        domain = extract_domain(url)
        w = whois.whois(domain)
        creation_date = w.creation_date

        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        if creation_date is None:
            return -1

        now = datetime.utcnow()
        age = (now - creation_date).days
        return age
    except Exception:
        return -1
