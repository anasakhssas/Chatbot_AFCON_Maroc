"""Web scraper for CAN 2025 news"""
import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime
from pathlib import Path
import logging
from typing import List, Dict, Optional
from .config import (
    NEWS_SOURCES, USER_AGENT, REQUEST_TIMEOUT, 
    MAX_RETRIES, DELAY_BETWEEN_REQUESTS, DATA_DIR,
    MAX_ARTICLES_PER_FETCH, TIMESTAMP_FORMAT
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NewsScraperCAN2025:
    """Scraper for CAN 2025 news articles"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': USER_AGENT})
        
    def fetch_page(self, url: str) -> Optional[str]:
        """Fetch a web page with retry logic"""
        for attempt in range(MAX_RETRIES):
            try:
                response = self.session.get(url, timeout=REQUEST_TIMEOUT)
                response.raise_for_status()
                logger.info(f"Successfully fetched: {url}")
                return response.text
            except requests.RequestException as e:
                logger.warning(f"Attempt {attempt + 1}/{MAX_RETRIES} failed for {url}: {e}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(DELAY_BETWEEN_REQUESTS)
                else:
                    logger.error(f"Failed to fetch {url} after {MAX_RETRIES} attempts")
                    return None
    
    def parse_generic_news(self, html: str, source_config: Dict) -> List[Dict]:
        """Parse news articles using generic selectors"""
        soup = BeautifulSoup(html, 'html.parser')
        articles = []
        
        article_elements = soup.select(source_config['selectors'].get('article', 'article'))
        
        for idx, article in enumerate(article_elements[:MAX_ARTICLES_PER_FETCH]):
            try:
                # Extract title
                title_elem = article.select_one(source_config['selectors'].get('title', 'h3'))
                title = title_elem.get_text(strip=True) if title_elem else "No title"
                
                # Extract content/description
                content_elem = article.select_one(source_config['selectors'].get('content', 'p'))
                content = content_elem.get_text(strip=True) if content_elem else ""
                
                # Extract date
                date_elem = article.select_one(source_config['selectors'].get('date', 'time'))
                date = date_elem.get_text(strip=True) if date_elem else datetime.now().strftime("%Y-%m-%d")
                
                # Extract link
                link_elem = article.select_one(source_config['selectors'].get('link', 'a'))
                link = link_elem.get('href', '') if link_elem else ""
                
                # Make sure link is absolute
                if link and not link.startswith('http'):
                    base_url = source_config['url'].split('/')[0:3]
                    link = '/'.join(base_url) + ('/' if not link.startswith('/') else '') + link
                
                article_data = {
                    'id': f"{source_config['name']}_{idx}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                    'title': title,
                    'content': content,
                    'date': date,
                    'link': link,
                    'source': source_config['name'],
                    'fetched_at': datetime.now().isoformat(),
                    'keywords': ['CAN 2025', 'AFCON', 'Football', 'Africa']
                }
                
                articles.append(article_data)
                logger.info(f"Parsed article: {title[:50]}...")
                
            except Exception as e:
                logger.error(f"Error parsing article {idx}: {e}")
                continue
        
        return articles
    
    def scrape_source(self, source_key: str) -> List[Dict]:
        """Scrape news from a specific source"""
        source_config = NEWS_SOURCES.get(source_key)
        if not source_config:
            logger.error(f"Unknown source: {source_key}")
            return []
        
        logger.info(f"Scraping {source_config['name']}...")
        html = self.fetch_page(source_config['url'])
        
        if not html:
            return []
        
        # Add delay to be respectful
        time.sleep(DELAY_BETWEEN_REQUESTS)
        
        articles = self.parse_generic_news(html, source_config)
        logger.info(f"Scraped {len(articles)} articles from {source_config['name']}")
        
        return articles
    
    def scrape_all_sources(self) -> List[Dict]:
        """Scrape all configured news sources"""
        all_articles = []
        
        for source_key in NEWS_SOURCES.keys():
            articles = self.scrape_source(source_key)
            all_articles.extend(articles)
        
        logger.info(f"Total articles scraped: {len(all_articles)}")
        return all_articles
    
    def save_articles(self, articles: List[Dict], filename: Optional[str] = None) -> str:
        """Save articles to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime(TIMESTAMP_FORMAT)
            filename = f"can2025_news_{timestamp}.json"
        
        filepath = DATA_DIR / filename
        
        data = {
            'metadata': {
                'total_articles': len(articles),
                'fetch_date': datetime.now().isoformat(),
                'sources': list(set([article['source'] for article in articles]))
            },
            'articles': articles
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Saved {len(articles)} articles to {filepath}")
        return str(filepath)


def run_pipeline():
    """Main pipeline function to fetch and store news"""
    logger.info("Starting CAN 2025 news scraping pipeline...")
    
    scraper = NewsScraperCAN2025()
    articles = scraper.scrape_all_sources()
    
    if articles:
        filepath = scraper.save_articles(articles)
        logger.info(f"Pipeline completed successfully. Data saved to: {filepath}")
        return filepath
    else:
        logger.warning("No articles were scraped.")
        return None


if __name__ == "__main__":
    run_pipeline()
