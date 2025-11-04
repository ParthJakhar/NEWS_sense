from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redditSearch import get_reddit_links

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
    data = await get_reddit_links()
    return {"articles": data}
