"""Configuration for the data pipeline"""
import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data" / "daily_fetch"

# Create data directory if it doesn't exist
DATA_DIR.mkdir(parents=True, exist_ok=True)

# News sources for CAN 2025
NEWS_SOURCES = {
    "cafonline_afcon": {
        "url": "https://www.cafonline.com/afcon2025/news",
        "name": "CAF AFCON 2025 Official",
        "selectors": {
            "article": "div.article-card, article, div.news-item",
            "title": "h3, h2, h4",
            "content": "p, div.description",
            "date": "time, span.date, div.date",
            "link": "a"
        }
    },
    "cafonline_main": {
        "url": "https://www.cafonline.com/news/",
        "name": "CAF Official News",
        "selectors": {
            "article": "div.article-card, article",
            "title": "h3, h2",
            "content": "p, div.excerpt",
            "date": "time, span.date",
            "link": "a"
        }
    },
    "bbc_afcon": {
        "url": "https://www.bbc.com/sport/football/africa-cup-of-nations",
        "name": "BBC Sport AFCON",
        "selectors": {
            "article": "div[data-testid='liverpool-card'], article",
            "title": "h2, h3",
            "content": "p",
            "date": "time",
            "link": "a"
        }
    }
}

# Scraping settings
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
REQUEST_TIMEOUT = 30
MAX_RETRIES = 3
DELAY_BETWEEN_REQUESTS = 2  # seconds

# Data storage settings
MAX_ARTICLES_PER_FETCH = 50
DATE_FORMAT = "%Y-%m-%d"
TIMESTAMP_FORMAT = "%Y-%m-%d_%H-%M-%S"
