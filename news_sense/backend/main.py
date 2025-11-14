from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from redditSearch import get_reddit_links
from categorize_news import categorize_headline
from db import save_news_item, track_read_more_click, track_reddit_click, track_watch_time
from gemini_summary import generate_summary

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SummaryRequest(BaseModel):
    headline: str
    news_link: str = None

class AnalyticsRequest(BaseModel):
    headline: str

class WatchTimeRequest(BaseModel):
    headline: str
    watch_time: int

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
        image = item.get("image", "")

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
            "news_link": news_link,
            "image": image
        })

    # Step 3: Return response
    return {"articles": categorized_articles}

@app.post("/news/summary")
async def get_summary(request: SummaryRequest):
    """Generate a summary using Gemini AI. Only runs when this endpoint is called."""
    try:
        summary = generate_summary(request.headline, request.news_link)
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating summary: {str(e)}")

@app.post("/analytics/read-more-click")
async def track_read_more(request: AnalyticsRequest):
    """Track a 'Read more' button click."""
    try:
        track_read_more_click(request.headline)
        return {"status": "success", "message": "Read more click tracked"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error tracking click: {str(e)}")

@app.post("/analytics/reddit-click")
async def track_reddit(request: AnalyticsRequest):
    """Track a 'Discuss on Reddit' button click."""
    try:
        track_reddit_click(request.headline)
        return {"status": "success", "message": "Reddit click tracked"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error tracking click: {str(e)}")

@app.post("/analytics/watch-time")
async def track_watch_time_endpoint(request: WatchTimeRequest):
    """Track watch time for a news item."""
    try:
        track_watch_time(request.headline, request.watch_time)
        return {"status": "success", "message": "Watch time tracked"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error tracking watch time: {str(e)}")
