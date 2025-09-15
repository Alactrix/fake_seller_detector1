# features/features.py

from model.https_check import is_https
from model.domain import is_domain_suspicious, get_domain_age_days
from model.page_check import check_page_features
from ml_model.predict_model import predict_fake_review
from utils.review_scraper import get_reviews_trustpilot
from utils.forum_scraper import search_reddit_forum_mentions

import json
import os

# Load weights from config.json
CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'config.json')
with open(CONFIG_PATH, 'r') as f:
    WEIGHTS = json.load(f)


def calculate_score(url: str, review_text: str = None) -> (float, list):
    reasons = []
    total_score = 0

    # ✅ HTTPS check
    if is_https(url):
        total_score += WEIGHTS["https"]
        reasons.append("✅ Uses HTTPS")
    else:
        reasons.append("❌ Does not use HTTPS")

    # ✅ Domain name check
    if not is_domain_suspicious(url):
        total_score += WEIGHTS["domain_name"]
        reasons.append("✅ Domain looks normal")
    else:
        reasons.append("❌ Domain name looks suspicious")

    # ✅ Domain age check
    domain_age = get_domain_age_days(url)
    if domain_age == -1:
        reasons.append("❌ Could not determine domain age")
    elif domain_age < 180:
        reasons.append(f"❌ Domain is too new ({domain_age} days old)")
    else:
        total_score += WEIGHTS["domain_age"]
        reasons.append(f"✅ Domain age is acceptable ({domain_age} days old)")

    # ✅ Page content check
    page_features = check_page_features(url)
    if "error" in page_features:
        reasons.append(f"❌ Failed to analyze page content: {page_features['error']}")
    else:
        if any([
            page_features.get("is_informative"),
            page_features.get("has_h1"),
            page_features.get("has_important_links"),
            page_features.get("has_product_listings"),
            page_features.get("has_social_links")
        ]):
            total_score += WEIGHTS["page"]
            reasons.append("✅ Page looks informative")
        else:
            reasons.append("❌ Page content looks too thin")

    # ✅ ML review scoring
    auto_reviews = get_reviews_trustpilot(url)
    fake_count = 0
    for rev in auto_reviews:
        label, _ = predict_fake_review(rev)
        if label == "Fake Review":
            fake_count += 1

    if fake_count <= 2:
        total_score += WEIGHTS["reviews"]
        reasons.append("✅ Most public reviews seem genuine")
    else:
        reasons.append(f"❌ {fake_count}/10 reviews seem fake")

    # ✅ Reddit/forum mention check
    is_reported, mentions = search_reddit_forum_mentions(url)
    print(f"[DEBUG] Reddit scam found for {url}: {is_reported}, mentions: {mentions}")
    if is_reported:
        reasons.append("❌ Reported in scam forums like Reddit")
        print(['url'])
    else:
        total_score += WEIGHTS["forum"]
        reasons.append("✅ No scam reports found on public forums")

    return round(total_score, 2), reasons
