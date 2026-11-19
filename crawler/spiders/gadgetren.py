import re
from typing import Any, Dict, List
from crawler.spiders.base import BaseSpider


class GadgetrenSpider(BaseSpider):
    """Spider for Gadgetren reviews; gracefully skips when HTTP 403 WAF is active."""

    def __init__(self, delay_seconds: float = 1.0):
        super().__init__(
            name="Gadgetren",
            base_url="https://gadgetren.com/category/review/",
            delay_seconds=delay_seconds,
        )

    def extract_specs(self, soup) -> Dict[str, str]:
        return self.extract_specs_from_soup(soup)

    def crawl(self, max_documents: int = 350) -> List[Dict[str, Any]]:
        documents: List[Dict[str, Any]] = []
        page = 1
        doc_count = 0

        while doc_count < max_documents:
            url = f"{self.base_url}page/{page}/" if page > 1 else self.base_url
            soup = self.fetch(url)
            if not soup:
                if self.last_status_code == 403:
                    print(
                        "[Gadgetren] Target returned HTTP 403 (anti-bot restriction); "
                        "skipping Gadgetren without bypass."
                    )
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
                    if self.last_status_code == 403:
                        return documents
                    continue

                title_tag = article_soup.find(
                    "h1", class_=re.compile("entry-title|post-title|title")
                )
                title = self.clean_title(title_tag.get_text(" ", strip=True)) if title_tag else "Review Gadgetren"

                date_tag = article_soup.find("time")
                date_str = date_tag.get_text(strip=True)[:10] if date_tag else ""

                content_div = article_soup.find(
                    "div", class_=re.compile("entry-content|post-content")
                )
                if not content_div:
                    continue

                content = self.clean_html_content(str(content_div))
                if not self.is_valid_gadget_review(title, content, min_chars=500):
                    continue

                specs = self.extract_specs_from_soup(article_soup, full_text=f"{title} {content}")
                enriched_content = self.append_specs_summary(content, specs)
                doc_count += 1
                doc_id = f"gadgetren_{doc_count:04d}"

                doc = self.build_document(
                    doc_id=doc_id,
                    title=title,
                    source="Gadgetren",
                    url=article_url,
                    category=self.infer_category(title, enriched_content),
                    date=date_str,
                    specs=specs,
                    content=enriched_content,
                )
                documents.append(doc)

            page += 1

        return documents
