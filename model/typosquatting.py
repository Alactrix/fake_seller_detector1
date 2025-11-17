import re
import tldextract

# Common brand names (expand this list as needed)
POPULAR_BRANDS = [
    "amazon", "flipkart", "myntra", "paypal", "facebook",
    "instagram", "whatsapp", "apple", "microsoft", "google",
    "netflix", "snapchat", "nike", "adidas", "samsung", "xiaomi"
]

# Common substitutions or suspicious patterns
SUSPICIOUS_PATTERNS = [
    r"0", r"1", r"l", r"!", r"@", r"\$", r"%", r"&", r"\*",
    r"-", r"_", r"\.", r"x{2,}", r"z{2,}", r"shop", r"store", r"sale"
]

def is_typosquatted(url: str) -> bool:
    """
    Checks whether the given URL's domain appears to be typosquatting
    on a known popular brand.
    """
    extracted = tldextract.extract(url)
    domain = extracted.domain.lower()

    # Compare with popular brands for close resemblance
    for brand in POPULAR_BRANDS:
        if brand in domain:
            # direct matches are fine (like amazon.com)
            if domain == brand:
                return False
            # if brand name mixed with weird chars -> suspicious
            if re.search(r"[^a-z]*".join(list(brand)), domain):
                return True
            # if brand name + extra chars
            if len(domain) > len(brand) + 3:
                return True

    # Check for suspicious symbols or repeated characters
    for pattern in SUSPICIOUS_PATTERNS:
        if re.search(pattern, domain):
            return True

    return False
