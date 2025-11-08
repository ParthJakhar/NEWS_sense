import httpx
import asyncio
import json
import os
from datetime import datetime
from scraper import get_headlines
import load_dotenv from dotenv

load_dotenv()

MY_API_KEY = os.getenv("MY_API_KEY")
MY_SEARCH_ENGINE_ID = os.getenv("MY_SEARCH_ENGINE_ID")
CACHE_FILE = "cache.json"
MAX_REQUESTS_PER_DAY = 100
MAX_HEADLINES = 70  # Limit per request


def load_cache():
    """Load cache file or create a new one."""
    if not os.path.exists(CACHE_FILE):
        return {"date": str(datetime.now().date()), "count": 0, "data": {}}

    with open(CACHE_FILE, "r") as f:
        cache = json.load(f)

    # Reset daily count if it's a new day
    if cache["date"] != str(datetime.now().date()):
        cache = {"date": str(datetime.now().date()), "count": 0, "data": {}}

    return cache


def save_cache(cache):
    """Save cache to file."""
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)


async def get_first_reddit_link(search_query, client):
    """Search Google for the Reddit link."""
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": MY_API_KEY,
        "cx": MY_SEARCH_ENGINE_ID,
        "q": f'"{search_query}" reddit.com',
        "num": 1
    }

    try:
        response = await client.get(url, params=params)
        response.raise_for_status()
        search_results = response.json()

        if "items" in search_results and len(search_results["items"]) > 0:
            return search_results["items"][0].get("link")
        else:
            return None
    except Exception as e:
        print(f"Error during search for '{search_query}': {e}")
        return None

async def get_reddit_links():
    """Get Reddit links with caching and rate limiting."""
    headlines = get_headlines()[:MAX_HEADLINES]
    cache = load_cache()

    results = []
    async with httpx.AsyncClient(timeout=10) as client:
        for item in headlines:
            # Extract actual headline text
            headline_text = item["headline"] if isinstance(item, dict) else item

            # Use cached result if available
            if headline_text in cache["data"]:
                print(f"Using cached result for: {headline_text}")
                reddit_link = cache["data"][headline_text]
            else:
                # Check if daily limit reached
                if cache["count"] >= MAX_REQUESTS_PER_DAY:
                    print("Daily limit reached. Skipping further API calls.")
                    reddit_link = None
                else:
                    reddit_link = await get_first_reddit_link(headline_text, client)
                    cache["data"][headline_text] = reddit_link
                    cache["count"] += 1

            # Preserve other fields (link, image, etc.)
            result = {
                "headline": headline_text,
                "reddit_link": reddit_link
            }
            if isinstance(item, dict):
                result.update({k: v for k, v in item.items() if k != "headline"})
            results.append(result)

    save_cache(cache)
    return results

