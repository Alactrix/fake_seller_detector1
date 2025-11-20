import re
import whois
from datetime import datetime

WHOIS_API = "https://api.whoisfreaks.com/v1/whois"

def extract_domain(url: str) -> str:
    match = re.search(r'://([^/]+)', url)
    if not match:
        return ""
    domain = match.group(1).lower()
    domain = re.sub(r'^www\.', '', domain)
    return domain.split(':')[0].split('/')[0]

def is_domain_suspicious(url: str) -> bool:
    domain = extract_domain(url)
    keywords = ['cheap', 'offer', 'deal', 'discount', 'promo', 'free', 'sale', 'shop', 'best', 'new']
    return any(k in domain for k in keywords)

def get_domain_age_days(url: str) -> int:
    domain = extract_domain(url)
    if not domain:
        return -1

    try:
        import whois
        w = whois.whois(domain)
        if w.creation_date:
            date = w.creation_date
            if isinstance(date, list):
                date = date[0]
            if isinstance(date, datetime):
                return max(1, (datetime.utcnow() - date).days)
    except:
        pass

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (ScamDetector/1.0)",
            "Accept": "application/json"
        }
        response = requests.get(f"https://whoisfreaks.com/api/v1/{domain}", headers=headers, timeout=12)
        if response.status_code == 200:
            data = response.json()
            creation = data.get("creation_date") or data.get("registered")
            if creation:
                creation = creation.split("T")[0].split(" ")[0]
                creation_date = datetime.strptime(creation, "%Y-%m-%d")
                return max(1, (datetime.utcnow() - creation_date).days)
    except:
        pass

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(f"https://viewdns.info/whois/?domain={domain}", headers=headers, timeout=10)
        if resp.status_code == 200:
            text = resp.text
            match = re.search(r'(Creation Date|Registered On|Domain Registration Date)[\s:]+([0-9]{4}-[0-9]{2}-[0-9]{2})', text, re.I)
            if match:
                date_str = match.group(2)
                creation_date = datetime.strptime(date_str, "%Y-%m-%d")
                return max(1, (datetime.utcnow() - creation_date).days)
    except:
        pass

    return -1