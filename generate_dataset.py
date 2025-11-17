import csv
from features.features import calculate_score
from model.domain import is_domain_suspicious, get_domain_age_days
from model.https_check import is_https
from utils.forum_scraper import search_reddit_forum_mentions
from utils.review_scraper import get_reviews_trustpilot
from model.typosquatting import is_typosquatted
from model.traffic_rank import get_traffic_rank

def extract_features(url):
    https_val = 1 if is_https(url) else 0
    domain_suspicious = 1 if is_domain_suspicious(url) else 0
    domain_age = get_domain_age_days(url)
    typosquat = 1 if is_typosquatted(url) else 0
    reddit_mentions = 1 if search_reddit_forum_mentions(url) else 0
    traffic_rank = get_traffic_rank(url)
    
    # ML-based fake review estimation
    reviews = get_reviews_trustpilot(url)
    fake_review_ratio = 0
    if reviews:
        from ml_model.predict_model import predict_fake_review
        fake_count = sum(1 for r in reviews if predict_fake_review(r)[0] == "Fake Review")
        fake_review_ratio = fake_count / len(reviews)
    
    return {
        "https": https_val,
        "domain_suspicious": domain_suspicious,
        "domain_age": domain_age,
        "typosquatting": typosquat,
        "reddit_mentions": reddit_mentions,
        "traffic_rank": traffic_rank,
        "fake_review_ratio": round(fake_review_ratio, 2)
    }

def main():
    urls = [u.strip() for u in open("urls.txt").readlines() if u.strip()]
    
    with open("website_dataset.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "url", "https", "domain_suspicious", "domain_age",
            "typosquatting", "reddit_mentions", "traffic_rank",
            "fake_review_ratio", "score", "label"
        ])
        writer.writeheader()
        
        for url in urls:
            print(f"Analyzing {url}...")
            try:
                features = extract_features(url)
                score, _ = calculate_score(url)
                label = 0 if score >= 50 else 1  # 0=legit, 1=scam
                
                writer.writerow({
                    "url": url,
                    **features,
                    "score": score,
                    "label": label
                })
            except Exception as e:
                print(f"Error for {url}: {e}")

if __name__ == "__main__":
    main()
