import requests
import json
import os
from urllib.parse import quote_plus

# ✅ Load config.json (from project root)
CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")

try:
    with open(CONFIG_PATH, "r") as f:
        CONFIG = json.load(f)
except Exception as e:
    print(f"⚠️ Could not load config.json: {e}")
    CONFIG = {}

API_KEY = CONFIG.get("TRAFFIC_API_KEY", "")
API_HOST = CONFIG.get("RAPIDAPI_TRAFFIC_HOST", "")

def get_traffic_rank(url: str):
    """Fetch global traffic rank for a given website using RapidAPI."""
    try:
        encoded_site = quote_plus(url)
        endpoint = f"https://{API_HOST}/webtraffic/getTraffic?site={encoded_site}"

        headers = {
            "x-rapidapi-key": API_KEY,
            "x-rapidapi-host": API_HOST
        }

        print(f"🔍 Fetching rank for: {url}")
        response = requests.get(endpoint, headers=headers, timeout=15)
        print(f"🔍 Status Code: {response.status_code}")

        if response.status_code != 200:
            print(f"❌ API Error: {response.text}")
            return -1

        data = response.json()
        print(f"🔍 Raw API Response keys: {list(data.keys())}")

        # ✅ Try different possible rank fields
        rank = None
        if "ranks" in data:
            if "globalRank" in data["ranks"]:
                rank = data["ranks"]["globalRank"].get("rank")
            elif isinstance(data["ranks"], dict):
                rank = next(iter(data["ranks"].values())).get("rank", None)

        if rank is None and "rankings" in data:
            rank = data["rankings"].get("globalRank", None)

        if rank is None:
            print("⚠️ No rank field found in response.")
            return -1

        return int(rank)

    except Exception as e:
        print(f"⚠️ Exception in get_traffic_rank(): {e}")
        return -1


# Debug run
if __name__ == "__main__":
    print(get_traffic_rank("https://amazon.in"))
