from pymongo import MongoClient

MONGO_URI = "mongodb+srv://jakharparth12:BIaOdjNB5i9OGwbA@cluster0.fzerzt1.mongodb.net/news_database3?retryWrites=true&w=majority&tls=true"
client = MongoClient(MONGO_URI)
db = client["news_database3"]

def get_category_collection(category_name):
    """Return or create a MongoDB collection for a category."""
    return db[category_name]

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
