# features/features.py

from model.https_check import is_https
from model.domain import is_domain_suspicious, get_domain_age_days
from model.page_check import check_page_features
from ml_model.predict_model import predict_fake_review
from utils.review_scraper import get_reviews_trustpilot
from utils.forum_scraper import search_reddit_forum_mentions
from model.typosquatting import is_typosquatted
from model.traffic_rank import get_traffic_rank


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

    # ML review scoring
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


    # ✅ Typosquatting check
    if is_typosquatted(url):
        reasons.append("❌ Domain resembles a known brand (possible typosquatting)")
    else:
        total_score += WEIGHTS.get("typosquatting", 1)
        reasons.append("✅ Domain doesn’t appear to imitate known brands")



    # ✅ Traffic Rank / Visits scoring
    traffic = get_traffic_rank(url)

    if not traffic:
        reasons.append("❌ Could not determine website traffic")
    else:
        rank = traffic.get("rank")
        visits = traffic.get("visits")

        # --- Rank-based scoring ---
        if rank is not None and isinstance(rank, int) and rank > 0:
            if rank <= 100_000:
                total_score += WEIGHTS.get("traffic_rank", 2)
                reasons.append(f"✅ Very high traffic (Global Rank #{rank:,})")
            elif rank <= 500_000:
                total_score += WEIGHTS.get("traffic_rank", 1.5)
                reasons.append(f"⚠️ Good traffic (Global Rank #{rank:,})")
            elif rank <= 1_000_000:
                total_score += WEIGHTS.get("traffic_rank", 1)
                reasons.append(f"⚠️ Moderate traffic (Global Rank #{rank:,})")
            else:
                reasons.append(f"❌ Low traffic (Global Rank #{rank:,}) — possibly new or suspicious")

        # --- Visits-based scoring (fallback if no rank) ---
        elif visits is not None and isinstance(visits, int) and visits > 0:
            if visits >= 50_000_000:
                total_score += WEIGHTS.get("traffic_rank", 2)
                reasons.append(f"✅ Very high traffic ({visits:,} monthly visits)")
            elif visits >= 10_000_000:
                total_score += WEIGHTS.get("traffic_rank", 1.5)
                reasons.append(f"⚠️ Good traffic ({visits:,} monthly visits)")
            elif visits >= 1_000_000:
                total_score += WEIGHTS.get("traffic_rank", 1)
                reasons.append(f"⚠️ Moderate traffic ({visits:,} monthly visits)")
            else:
                reasons.append(f"❌ Very low traffic ({visits:,} monthly visits) — possibly suspicious")

        else:
            reasons.append("❌ Could not determine website traffic metrics")

    
    
    return round(total_score, 2), reasons

