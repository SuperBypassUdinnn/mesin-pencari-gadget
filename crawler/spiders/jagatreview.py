import re
from typing import Any, Dict, List
from crawler.spiders.base import BaseSpider

class JagatReviewSpider(BaseSpider):
    def __init__(self, delay_seconds: float = 1.0):
        super().__init__(
            name="Jagat Review",
            base_url="https://www.jagatreview.com/category/gadget-review/",
            delay_seconds=delay_seconds
        )

    def extract_specs(self, soup) -> Dict[str, str]:
        specs = {}
        # Jagat Review often uses strong/b tags or lists for hardware specs
        for li in soup.find_all("li"):
            text = li.get_text(strip=True)
            if ":" in text:
                parts = text.split(":", 1)
                k = parts[0].strip().lower()
                v = parts[1].strip()
                if any(term in k for term in ["soc", "prosesor", "cpu", "gpu", "ram", "storage", "layar", "baterai", "os"]):
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

            posts = soup.find_all("div", class_=re.compile("post|entry|item"))
            if not posts:
                break

            for post in posts:
                if doc_count >= max_documents:
                    break
                link_tag = post.find("a", href=True)
                if not link_tag:
                    continue
                article_url = link_tag["href"]
                if "jagatreview.com" not in article_url:
                    continue

                article_soup = self.fetch(article_url)
                if not article_soup:
                    continue

                title_tag = article_soup.find("h1")
                title = title_tag.get_text(strip=True) if title_tag else "Review Jagat Review"

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
                doc_id = f"jagatreview_{doc_count:04d}"

                category = "laptop" if any(w in title.lower() for w in ["laptop", "notebook", "pc", "desktop"]) else "smartphone"

                doc = self.build_document(
                    doc_id=doc_id,
                    title=title,
                    source="Jagat Review",
                    url=article_url,
                    category=category,
                    date=date_str,
                    specs=specs,
                    content=content
                )
                documents.append(doc)

            page += 1

        return documents
