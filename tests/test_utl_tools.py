from scrapenest.url_tools import normalize_url, is_same_domain

def test_normalize_url():
    assert normalize_url('http://www.Example.com/path/') == 'https://example.com/path'
    assert normalize_url('https://example.com/double//') == 'https://example.com/double'
    assert normalize_url('http://blog.example.com') == 'https://blog.example.com'
    
def test_is_same_domain():
    assert is_same_domain('https://www.example.com', 'https://www.example.com/about') is True
    assert is_same_domain('https://sub.example.com', 'https://example.com') is False
    
    assert is_same_domain('http://example.com', 'https://example.com:8080') is True
    
    