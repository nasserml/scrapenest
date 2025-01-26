from bs4 import BeautifulSoup
import requests
from .url_tools import normalize_url, is_same_domain
from fake_useragent import UserAgent
import time
from urllib.parse import urlparse, urljoin, urlunparse

class ScrapeNest:
    def __init__(self, max_depth=5, max_pages=10, delay=1):
        self.max_depth = max_depth
        self.max_pages = max_pages
        self.delay = delay
        self.page_content = {}
        self.visited_urls = set()
        self.ua = UserAgent()
    
    def crawl(self, start_url):
        self._crawl_recursive(start_url, self.max_depth)
        return self.page_content
    
    def _crawl_recursive(self, url, depth):
        if depth < 0 or len(self.page_content) >= self.max_pages:
            return
        
        normalized = normalize_url(url)
        if normalized in self.visited_urls:
            return
        
        try:
            headers = {'User-Agent': self.ua.random}
            response = requests.get(normalized, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            self.page_content[normalized] = soup.get_text(separator=" ", strip=True)
            self.visited_urls.add(normalized)
            
            time.sleep(self.delay)
            
            if depth > 0:
                for link in soup.find_all('a', href=True):
                    next_url = urljoin(normalized, link['href'])
                    next_url = normalize_url(next_url)
                    if is_same_domain(normalized, next_url): 
                        self._crawl_recursive(next_url, depth - 1)
        
        except Exception as e:
            print(f'Error crawling {url} : {str(e)}')
        
        