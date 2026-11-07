import time
from typing import Any, Dict, List, Optional
import requests
from bs4 import BeautifulSoup

class BaseSpider:
    def __init__(self, name: str, base_url: str, delay_seconds: float = 1.0):
        self.name = name
        self.base_url = base_url
        self.delay_seconds = delay_seconds
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 GadgetSearchBot/1.0"
        })

    def fetch(self, url: str) -> Optional[BeautifulSoup]:
        try:
            time.sleep(self.delay_seconds)
            response = self.session.get(url, timeout=15)
            if response.status_code == 200:
                return BeautifulSoup(response.text, "html.parser")
            return None
        except Exception as e:
            print(f"[{self.name}] Error fetching {url}: {e}")
            return None

    def build_document(
        self,
        doc_id: str,
        title: str,
        source: str,
        url: str,
        category: str,
        date: str,
        specs: Dict[str, Any],
        content: str
    ) -> Dict[str, Any]:
        return {
            "id": doc_id,
            "title": title.strip(),
            "source": source.strip(),
            "url": url.strip(),
            "category": category.strip().lower(),
            "date": date.strip(),
            "specs": specs or {},
            "content": content.strip()
        }

    def crawl(self, max_documents: int = 350) -> List[Dict[str, Any]]:
        raise NotImplementedError("Subclasses must implement crawl()")
