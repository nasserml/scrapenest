# 🕸️ ScrapeNest: Intelligent Web Crawling with Content Nesting 🌐

Welcome to **ScrapeNest**! 🎉

ScrapeNest is a powerful and intelligent web crawler designed for efficient and customizable web scraping. Dive deep into websites, collect content, and analyze data with ease. 🚀

---

## 📖 Table of Contents

- [✨ Features](#-features)
- [📁 Project Structure](#-project-structure)
- [🛠 Installation](#-installation)
- [🚀 Usage](#-usage)
- [⚙️ Configuration](#%EF%B8%8F-configuration)
- [🔍 How It Works](#-how-it-works)
- [📝 Notes](#-notes)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [📬 Contact](#-contact)
- [🙏 Acknowledgements](#-acknowledgements)
- [🎉 Happy Scraping!](#-happy-scraping)

---

## ✨ Features

- 🔍 **Depth-Controlled Crawling**: Define the level of depth for recursive crawling.
- 🌐 **Domain-Specific Scraping**: Restrict crawling to a single domain to keep data relevant.
- ⏱️ **Adjustable Delays**: Set custom delays between requests to respect server load.
- 🕵️ **Random User Agents**: Use random User-Agent headers to avoid detection.
- 📦 **Content Nesting**: Collect and store page content in a structured format.
- 🎯 **Customizable Limits**: Control maximum pages to scrape to avoid overloading servers.

---

## 📁 Project Structure

Here's a quick overview of the project's directory structure:

```
nasserml-scrapenest/
├── README.md
├── requirements.txt
├── setup.py
└── scrapenest/
    ├── __init__.py
    ├── config.py
    ├── crawler.py
    └── url_tools.py
```

### 📄 Files Content

---

#### `requirements.txt`

Lists the Python dependencies required to run ScrapeNest:

```text
beautifulsoup4
fake-useragent
```

---

#### `setup.py`

The setup script to install ScrapeNest as a package:

```python
from setuptools import setup, find_packages

setup(
    name="scrapenest",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'beautifulsoup4>=4.11.1',
        'requests>=2.28.1',
        'fake-useragent>=1.1.3',
        'tldextract>=3.4.0'
    ],
    author="naserml",
    author_email='mnasserone@gmail.com',
    description="Intelligent web crawling with content nesting",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ], 
    python_requires='>=3.6',
    url="https://github.com/nasserml/scrapenest"
)
```

---

#### `scrapenest/crawler.py`

Contains the `ScrapeNest` class which handles the crawling process:

```python
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
            response = requests.get(normalized, headers==headers, timeout=10)
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
```

---

#### `scrapenest/url_tools.py`

Utility functions for URL processing:

```python
from urllib.parse import urlparse, urlunparse

def normalize_url(url):
    parsed= urlparse(url)
    schema = parsed.scheme or 'https'
    netloc = parsed.netloc.lower().lstrip('www.')
    path = parsed.path.rstrip('/')
    return urlunparse((schema, netloc, path, '', '' ,''))
    
def is_same_domain(url1, url2):
    return normalize_url(url1).split('/')[2] == normalize_url(url2).split('/')[2]
```

---

## 🛠 Installation

Install ScrapeNest easily using the following steps:

1. **Clone the repository**:

   ```bash
   git clone https://github.com/nasserml/scrapenest.git
   ```

2. **Navigate to the project directory**:

   ```bash
   cd scrapenest
   ```

3. **Install the required dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Install the ScrapeNest package**:

   ```bash
   python setup.py install
   ```

---

## 🚀 Usage

Start crawling the web with just a few lines of code! 🐍

```python
from scrapenest.crawler import ScrapeNest

# Initialize the ScrapeNest crawler
crawler = ScrapeNest(max_depth=2, max_pages=5, delay=1)

# Start crawling from a specific URL
content = crawler.crawl('https://www.example.com')

# Iterate through the collected content
for url, text in content.items():
    print(f"URL: {url}")
    print(f"Content Snippet: {text[:200]}...")  # Print the first 200 characters
    print("-" * 80)
```

---

## ⚙️ Configuration

Customize ScrapeNest to fit your needs:

- **`max_depth`** (`int`): Maximum depth to crawl (default: `5`).
- **`max_pages`** (`int`): Maximum number of pages to collect (default: `10`).
- **`delay`** (`int`): Delay between requests in seconds (default: `1`).

---

## 🔍 How It Works

Under the hood, ScrapeNest performs the following steps:

1. **Initialization**: Set up crawler parameters.
2. **Normalization**: Standardize URLs using `normalize_url`.
3. **HTTP Requests**: Fetch pages using `requests` with random User-Agent headers.
4. **Parsing**: Use `BeautifulSoup` to parse HTML content.
5. **Content Extraction**: Extract text content from pages.
6. **Recursion**: Follow links within the same domain, respecting `max_depth`.
7. **Data Collection**: Store content in a nested dictionary structure.

---

## 📝 Notes

- 💡 **Ethical Scraping**: Always respect the website's `robots.txt` file and terms of service.
- 🕰️ **Be Patient**: Use appropriate delays to avoid overwhelming web servers.
- 🔒 **Privacy**: Ensure you handle data responsibly and comply with data protection regulations.

---

## 🤝 Contributing

We welcome contributions! If you'd like to enhance ScrapeNest:

1. **Fork the repository**.
2. **Create a new branch**: `git checkout -b feature/YourFeature`.
3. **Commit your changes**: `git commit -am 'Add your feature'`.
4. **Push to the branch**: `git push origin feature/YourFeature`.
5. **Create a Pull Request**.

---

## 📄 License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

---

## 📬 Contact

- **Author**: naserml
- **Email**: [mnasserone@gmail.com](mailto:mnasserone@gmail.com)
- **GitHub**: [nasserml](https://github.com/nasserml/scrapenest)

---

## 🙏 Acknowledgements

- **BeautifulSoup** for HTML parsing.
- **Requests** for HTTP requests.
- **fake-useragent** for rotating User-Agent headers.
- **Community** for continuous support and contributions.

---

## 🎉 Happy Scraping!

Feel free to reach out if you have any questions or need assistance. Enjoy exploring the web with ScrapeNest! 🚀

---

# Quick Links

- [GitHub Repository](https://github.com/nasserml/scrapenest)
- [Issues](https://github.com/nasserml/scrapenest/issues)
- [Pull Requests](https://github.com/nasserml/scrapenest/pulls)

---

**Note**: Always ensure that your web scraping activities comply with legal requirements and the terms of service of the websites you are scraping. Responsible use of ScrapeNest is expected. 🙌

# 🎉 Thank you for choosing ScrapeNest!

Enjoy your web scraping journey, and may your data collection be fruitful and enlightening! 🌟

---

# Revision Notes

This README includes:

- A detailed project description with features and usage instructions.
- An overview of the project structure and the contents of key files.
- Installation and usage guides with code examples.
- Notes on ethical considerations for web scraping.
- Contact information and contribution guidelines.
- Plenty of emojis to make it engaging and visually appealing.

Happy coding! 😊