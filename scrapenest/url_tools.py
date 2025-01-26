from urllib.parse import urlparse, urlunparse

def normalize_url(url):
    parsed= urlparse(url)
    schema = parsed.scheme or 'https'
    netloc = parsed.netloc.lower().lstrip('www.')
    path = parsed.path.rstrip('/')
    return urlunparse((schema, netloc, path, '', '' ,''))

def is_same_domain(url1, url2):
    return normalize_url(url1).split('/')[2] == normalize_url(url2).split('/')[2]
    