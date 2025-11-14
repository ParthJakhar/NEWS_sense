import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_summary(headline, news_link=None):
    try:
        prompt = f"""
Summarize the following news headline in 2–3 paragraphs:

Headline: {headline}

"""
        if news_link:
            prompt += f"Article URL: {news_link}\n\n"

        prompt += """Requirements:
- Mention key points
- Provide meaningful context
- Write clearly and factually
- 2–3 medium length paragraphs

Summary:"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )
        return response.text.strip()

    except Exception as e:
        print("⚠️ Error generating summary with Gemini:", e)
        return "Failed to generate summary."
