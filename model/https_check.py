def is_https(url: str) -> bool:
    return url.lower().startswith("https://")