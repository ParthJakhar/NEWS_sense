import React, { useEffect, useState } from "react";
import axios from "axios";

export default function NewsList() {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchNews = async () => {
      try {
        const res = await axios.get("http://127.0.0.1:8000/news");
        const data = res.data.articles || [];

        if (data.length === 0) {
          setError("No results available or daily limit reached.");
        }

        setArticles(data);
      } catch (err) {
        console.error("Error fetching news:", err);
        setError("Failed to fetch news. Please try again later.");
      } finally {
        setLoading(false);
      }
    };

    fetchNews();
  }, []);

  if (loading) {
    return (
      <div className="loading-screen">
        <div className="spinner"></div>
        <p>Fetching latest headlines...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-message text-center mt-10">
        <h2>⚠️ {error}</h2>
        <button onClick={() => window.location.reload()} className="retry-btn">
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="news-container">
      
      <div className="news-grid">
        {articles.map((a, idx) => (
          <div key={idx} className="news-card">
            {a.image && (
              <img
                src={a.image}
                alt={a.headline}
                className="news-img"
                loading="lazy"
              />
            )}

            <h2>
              <a
                href={a.link || "#"}
                target="_blank"
                rel="noopener noreferrer"
                className="headline-link"
              >
                {a.headline}
              </a>
            </h2>

            <div className="discuss-reddit">
              {a.reddit_link ? (
                <button
                  onClick={() => window.open(a.reddit_link, "_blank")}
                  className="discuss-button active"
                >
                  Discuss on Reddit
                </button>
              ) : (
                <button className="discuss-button disabled" disabled>
                  No Reddit Thread
                </button>
              )}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
