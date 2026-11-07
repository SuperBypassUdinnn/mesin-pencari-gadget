import re
from typing import Any, Dict, List
from crawler.spiders.base import BaseSpider

class DroidlimeSpider(BaseSpider):
    def __init__(self, delay_seconds: float = 1.0):
        super().__init__(
            name="Droidlime",
            base_url="https://www.droidlime.com/artikel/",
            delay_seconds=delay_seconds
        )

    def extract_specs(self, soup) -> Dict[str, str]:
        specs = {}
        for tr in soup.find_all("tr"):
            tds = tr.find_all("td")
            if len(tds) == 2:
                k = tds[0].get_text(strip=True).lower()
                v = tds[1].get_text(strip=True)
                if any(term in k for term in ["chipset", "layar", "ram", "memori", "kamera", "baterai"]):
                    specs[k] = v
        return specs

    def crawl(self, max_documents: int = 200) -> List[Dict[str, Any]]:
        documents = []
        page = 1
        doc_count = 0

        while doc_count < max_documents:
            url = f"{self.base_url}page/{page}/" if page > 1 else self.base_url
            soup = self.fetch(url)
            if not soup:
                break

            items = soup.find_all("div", class_=re.compile("article|post|card"))
            if not items:
                break

            for item in items:
                if doc_count >= max_documents:
                    break
                link = item.find("a", href=True)
                if not link:
                    continue
                article_url = link["href"]
                article_soup = self.fetch(article_url)
                if not article_soup:
                    continue

                title_tag = article_soup.find("h1")
                title = title_tag.get_text(strip=True) if title_tag else "Review Droidlime"

                content_div = article_soup.find("div", class_=re.compile("entry-content|content"))
                if not content_div:
                    continue

                paragraphs = [p.get_text(strip=True) for p in content_div.find_all("p") if len(p.get_text(strip=True)) > 20]
                content = " ".join(paragraphs)
                if len(content) < 100:
                    continue

                specs = self.extract_specs(article_soup)
                doc_count += 1
                doc_id = f"droidlime_{doc_count:04d}"

                doc = self.build_document(
                    doc_id=doc_id,
                    title=title,
                    source="Droidlime",
                    url=article_url,
                    category="smartphone",
                    date="",
                    specs=specs,
                    content=content
                )
                documents.append(doc)

            page += 1

        return documents
