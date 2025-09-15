from utils.forum_scraper import search_reddit_forum_mentions

found, results = search_reddit_forum_mentions("https://blauxstore.com")
print("Reported as scam?", found)
for r in results:
    print(r['url'])
