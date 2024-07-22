import pytest
import requests
from bs4 import BeautifulSoup
from unittest.mock import patch
from parser.link_parser import (
    is_valid_url,
    get_external_links,
    crawl_links,
    visited_links,
)


def test_is_valid_url():
    assert is_valid_url("http://example.com") == True
    assert is_valid_url("https://example.com") == True
    assert is_valid_url("ftp://example.com") == False
    assert is_valid_url("example.com") == False


@patch("requests.get")
def test_get_external_links(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = """
    <html>
        <body>
            <a href="http://example.com">Example</a>
            <a href="https://example.com">Example</a>
            <a href="ftp://example.com">Invalid</a>
        </body>
    </html>
    """
    url = "http://test.com"
    links = get_external_links(url)
    assert len(links) == 2
    assert "http://example.com" in links
    assert "https://example.com" in links


@pytest.fixture(autouse=True)
def clear_visited_links():
    visited_links.clear()


@patch("requests.get")
def test_crawl_links(mock_get, clear_visited_links):
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = """
    <html>
        <body>
            <a href="http://example.com">Example</a>
        </body>
    </html>
    """
    url = "http://test.com"
    crawl_links(url, max_depth=1)
    assert "http://example.com" in visited_links
