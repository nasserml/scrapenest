import pytest
from scrapenest.crawler import ScrapeNest
from bs4 import BeautifulSoup

def test_crawler_initialization():
    crawler = ScrapeNest(max_depth=3, max_pages=5)
    assert crawler.max_depth == 3
    assert crawler.max_pages == 5

def test_crawler_limit(mocker):
    mock_get = mocker.path('requests.get')
    mock_get.return_value.content = """
    <html>
        <body>
            <a href="/page1>Link 1</a>
            <a href="/page2>Link 2</a>
        </body>
    </html>
    """
    
    crawler = ScrapeNest(max_pages=2)
    result = crawler.crawl('https://example.com')
    assert len(result) == 2
    
def test_depth_limit(mocker):
    mock_get = mocker.patch('requests.get')
    mock_get.return_value.content = "<html><a href='/next'></a></html>"
    
    crawler = ScrapeNest(max_depth=1)
    crawler.crawl("https://example.com")
    
    assert len(crawler.visited_urls) == 2  # Initial + 1 level