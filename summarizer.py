import requests
from bs4 import BeautifulSoup
import re

def fetch_and_clean(url: str) -> str:
    """
    Fetches content from a URL and extracts paragraph text.

    Args:
        url: The URL to fetch content from.

    Returns:
        The concatenated text from paragraph tags, cleaned of excessive whitespace.

    Raises:
        requests.exceptions.RequestException: If the URL fetch fails.
        ValueError: If no readable paragraph text is found.
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise requests.exceptions.RequestException(f"Failed to fetch URL: {url}. Error: {e}")

    soup = BeautifulSoup(resp.content, "html.parser")

    paragraphs = soup.find_all("p")
    text_content = " ".join([p.get_text(strip=True) for p in paragraphs])
    text_content = re.sub(r'\s+', ' ', text_content).strip()

    if not text_content:
        if not text_content:
             raise ValueError(f"No readable paragraph text found at the provided URL: {url}")

    return text_content