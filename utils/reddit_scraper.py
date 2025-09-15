import requests

def get_latest_scam_domains(limit=10):
    url = f"https://www.reddit.com/r/scams/new.json?limit={limit}"
    headers = {"User-Agent": "Mozilla/5.0 (fake_seller_bot)"}
    domains = []

    try:
        response = requests.get(url, headers=headers, timeout=10)
        posts = response.json()["data"]["children"]

        for post in posts:
            text = post["data"]["title"] + " " + post["data"].get("selftext", "")
            found = extract_domains(text)
            domains.extend(found)

    except Exception as e:
        return [f"(Error fetching from Reddit: {str(e)})"]

    return list(set(domains))[:limit]

def extract_domains(text):
    import re
    pattern = r"(https?://)?([a-zA-Z0-9-]+\.[a-zA-Z]{2,})(/[^\s]*)?"
    matches = re.findall(pattern, text)
    domains = [match[1] for match in matches]
    return domains
