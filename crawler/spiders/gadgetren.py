import re
from typing import Any, Dict, List
from crawler.spiders.base import BaseSpider

class GadgetrenSpider(BaseSpider):
    def __init__(self, delay_seconds: float = 1.0):
        super().__init__(
            name="Gadgetren",
            base_url="https://gadgetren.com/category/review/",
            delay_seconds=delay_seconds
        )

    def extract_specs(self, soup) -> Dict[str, str]:
        specs = {}
        # Gadgetren often includes a summary table or list in reviews
        tables = soup.find_all("table")
        for table in tables:
            rows = table.find_all("tr")
            for row in rows:
                cols = row.find_all(["td", "th"])
                if len(cols) == 2:
                    k = cols[0].get_text(strip=True).lower()
                    v = cols[1].get_text(strip=True)
                    if any(term in k for term in ["layar", "chipset", "prosesor", "ram", "memori", "kamera", "baterai", "harga", "os"]):
                        specs[k] = v
        return specs

    def crawl(self, max_documents: int = 350) -> List[Dict[str, Any]]:
        documents = []
        page = 1
        doc_count = 0

        while doc_count < max_documents:
            url = f"{self.base_url}page/{page}/" if page > 1 else self.base_url
            soup = self.fetch(url)
            if not soup:
                break

            articles = soup.find_all("article")
            if not articles:
                break

            for article in articles:
                if doc_count >= max_documents:
                    break
                link_tag = article.find("a", href=True)
                if not link_tag:
                    continue
                article_url = link_tag["href"]
                
                article_soup = self.fetch(article_url)
                if not article_soup:
                    continue

                title_tag = article_soup.find("h1", class_=re.compile("entry-title|post-title|title"))
                title = title_tag.get_text(strip=True) if title_tag else "Review Gadgetren"

                date_tag = article_soup.find("time")
                date_str = date_tag.get_text(strip=True) if date_tag else ""

                content_div = article_soup.find("div", class_=re.compile("entry-content|post-content"))
                if not content_div:
                    continue

                paragraphs = [p.get_text(strip=True) for p in content_div.find_all("p") if len(p.get_text(strip=True)) > 20]
                content = " ".join(paragraphs)
                if len(content) < 100:
                    continue

                specs = self.extract_specs(article_soup)
                doc_count += 1
                doc_id = f"gadgetren_{doc_count:04d}"

                doc = self.build_document(
                    doc_id=doc_id,
                    title=title,
                    source="Gadgetren",
                    url=article_url,
                    category="smartphone",
                    date=date_str,
                    specs=specs,
                    content=content
                )
                documents.append(doc)

            page += 1

        return documents
