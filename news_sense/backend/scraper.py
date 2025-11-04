import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE_URL = "https://edition.cnn.com/world"
headers = {"User-Agent": "Mozilla/5.0"}

def get_headlines():
    resp = requests.get(BASE_URL, headers=headers, timeout=10)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    headlines = []
    for card in soup.select('a:has(span[class*="headline-text"])'):
        headline = card.get_text(strip=True)
        href = card.get("href")
        link = urljoin(BASE_URL, href)

        # Try to find image inside the card
        img_tag = card.select_one("img")
        if img_tag and img_tag.get("data-src-medium"):
            img = img_tag["data-src-medium"]   # CNN often lazy loads
        elif img_tag and img_tag.get("src"):
            img = img_tag["src"]
        else:
            img = None

        # Priority detection
        span = card.select_one("span[class*='headline-text']")
        size_class = span.get("class", [])
        if any("xl" in c or "large" in c for c in size_class):
            priority = 3
        elif any("md" in c or "medium" in c for c in size_class):
            priority = 2
        else:
            priority = 1

        headlines.append({
            "headline": headline,
            "link": link,
            "priority": priority,
            "image": img
        })

    # Sort by priority (highest first)
    headlines.sort(key=lambda x: x["priority"], reverse=True)
    return headlines
