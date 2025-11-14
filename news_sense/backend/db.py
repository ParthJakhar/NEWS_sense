from pymongo import MongoClient
from datetime import datetime

MONGO_URI = "mongodb+srv://jakharparth12:BIaOdjNB5i9OGwbA@cluster0.fzerzt1.mongodb.net/news_database3?retryWrites=true&w=majority&tls=true"
client = MongoClient(MONGO_URI)
db = client["news_database3"]

def get_category_collection(category_name):
    """Return or create a MongoDB collection for a category."""
    return db[category_name]

def get_analytics_collection():
    """Return the analytics collection."""
    return db["news_analytics"]

def save_news_item(category, headline, reddit_link, news_link):
    """
    Save a categorized news item to MongoDB.
    Includes headline, category, reddit_link, and news_link.
    Avoids duplicates by headline.
    """
    try:
        collection = get_category_collection(category)
        # Prevent duplicate insertions based on headline
        if collection.find_one({"headline": headline}):
            print(f"⚠️ Skipped duplicate: '{headline}' already exists in '{category}'.")
            return

        news_data = {
            "headline": headline,
            "category": category,
            "reddit_link": reddit_link,
            "news_link": news_link
        }

        collection.insert_one(news_data)
        print(f"✅ Saved '{headline}' under '{category}'")
    except Exception as e:
        print(f"⚠️ Error saving '{headline}': {e}")

def track_read_more_click(headline):
    """Track a 'Read more' button click for a news item."""
    try:
        analytics_col = get_analytics_collection()
        analytics_col.update_one(
            {"headline": headline},
            {
                "$inc": {"read_more_clicks": 1},
                "$setOnInsert": {
                    "headline": headline,
                    "reddit_clicks": 0,
                    "total_watch_time": 0,
                    "watch_sessions": 0,
                    "created_at": datetime.now()
                }
            },
            upsert=True
        )
        print(f"✅ Tracked read more click for: '{headline}'")
    except Exception as e:
        print(f"⚠️ Error tracking read more click: {e}")

def track_reddit_click(headline):
    """Track a 'Discuss on Reddit' button click for a news item."""
    try:
        analytics_col = get_analytics_collection()
        analytics_col.update_one(
            {"headline": headline},
            {
                "$inc": {"reddit_clicks": 1},
                "$setOnInsert": {
                    "headline": headline,
                    "read_more_clicks": 0,
                    "total_watch_time": 0,
                    "watch_sessions": 0,
                    "created_at": datetime.now()
                }
            },
            upsert=True
        )
        print(f"✅ Tracked reddit click for: '{headline}'")
    except Exception as e:
        print(f"⚠️ Error tracking reddit click: {e}")

def track_watch_time(headline, watch_time_seconds):
    """Track watch time for a news item."""
    try:
        analytics_col = get_analytics_collection()
        analytics_col.update_one(
            {"headline": headline},
            {
                "$inc": {
                    "total_watch_time": watch_time_seconds,
                    "watch_sessions": 1
                },
                "$setOnInsert": {
                    "headline": headline,
                    "read_more_clicks": 0,
                    "reddit_clicks": 0,
                    "created_at": datetime.now()
                }
            },
            upsert=True
        )
        print(f"✅ Tracked watch time ({watch_time_seconds}s) for: '{headline}'")
    except Exception as e:
        print(f"⚠️ Error tracking watch time: {e}")

def get_analytics(headline=None):
    """Get analytics data. If headline is provided, returns data for that headline only."""
    try:
        analytics_col = get_analytics_collection()
        if headline:
            return analytics_col.find_one({"headline": headline})
        else:
            return list(analytics_col.find())
    except Exception as e:
        print(f"⚠️ Error getting analytics: {e}")
        return None
