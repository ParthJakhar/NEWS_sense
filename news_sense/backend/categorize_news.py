from transformers import pipeline

# Define categories
CATEGORIES = [
    "world", "sports", "entertainment", "technology",
    "politics", "business", "science", "health"
]

# Load once for performance
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def categorize_headline(headline: str):
    """
    Categorizes a single headline into one of the categories.
    Returns category and confidence.
    """
    if not headline.strip():
        return {"category": "other", "confidence": 0.0}

    result = classifier(headline, CATEGORIES)
    category = result["labels"][0]
    confidence = round(result["scores"][0], 3)

    return {"category": category, "confidence": confidence}
