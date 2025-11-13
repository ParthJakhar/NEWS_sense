from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redditSearch import get_reddit_links
from categorize_news import categorize_headline
from db import save_news_item

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/news")
async def read_news():
    # Step 1: Fetch Reddit news (cached or new)
    data = await get_reddit_links()

    if not data:
        return {"message": "No news found"}

    categorized_articles = []

    # Step 2: Process and categorize
    for item in data:
        headline = item.get("headline", "")
        reddit_link = item.get("reddit_link", "")
        news_link = item.get("headline_link", "")

        if not headline:
            continue

        # Categorize headline
        result = categorize_headline(headline)
        category = result.get("category", "Other")
        confidence = result.get("confidence", 0.0)

        # Save to MongoDB
        save_news_item(category, headline, reddit_link, news_link)

        # Append to result list
        categorized_articles.append({
            "headline": headline,
            "category": category,
            "confidence": confidence,
            "reddit_link": reddit_link,
            "news_link": news_link
        })

    # Step 3: Return response
    return {"articles": categorized_articles}
