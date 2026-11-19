import html
from typing import Any, Dict, List, Optional, Tuple
from bs4 import BeautifulSoup
from crawler.spiders.base import BaseSpider


class WPJsonSpider(BaseSpider):
    """Reusable WordPress REST API v2 spider for Indonesian gadget portals."""

    def __init__(
        self,
        name: str,
        base_url: str,
        api_url: str,
        doc_id_prefix: str,
        category_batches: List[Tuple[str, Optional[float]]],
        delay_seconds: float = 0.4,
        per_page: int = 50,
        min_chars: int = 700,
        default_category: str = "smartphone",
        max_pages: int = 30,
    ):
        super().__init__(name=name, base_url=base_url, delay_seconds=delay_seconds)
        self.api_url = api_url
        self.doc_id_prefix = doc_id_prefix
        self.category_batches = category_batches
        self.per_page = per_page
        self.min_chars = min_chars
        self.default_category = default_category
        self.max_pages = max_pages

    def passes_portal_filter(self, title: str, content: str) -> bool:
        """Optional subclass hook for portal-specific content filtering."""
        return True

    def _parse_post(
        self,
        post: Dict[str, Any],
        seen_urls: set,
        next_index: int,
    ) -> Optional[Dict[str, Any]]:
        article_url = str(post.get("link") or "").strip()
        if not article_url:
            return None

        norm_url = article_url.rstrip("/").lower()
        if norm_url in seen_urls:
            return None

        raw_title = (post.get("title") or {}).get("rendered", "")
        title = self.clean_title(raw_title)

        raw_html = (post.get("content") or {}).get("rendered", "")
        if not raw_html:
            return None

        content = self.clean_html_content(raw_html)
        if not self.is_valid_gadget_review(title, content, min_chars=self.min_chars):
            return None
        if not self.passes_portal_filter(title, content):
            return None

        soup = BeautifulSoup(html.unescape(raw_html), "html.parser")
        specs = self.extract_specs_from_soup(soup, full_text=f"{title} {content}")
        enriched_content = self.append_specs_summary(content, specs)
        category = self.infer_category(title, enriched_content, default=self.default_category)
        date_str = str(post.get("date") or "")[:10]

        seen_urls.add(norm_url)
        doc_id = f"{self.doc_id_prefix}_{next_index:04d}"
        return self.build_document(
            doc_id=doc_id,
            title=title,
            source=self.name,
            url=article_url,
            category=category,
            date=date_str,
            specs=specs,
            content=enriched_content,
        )

    def _crawl_batch(
        self,
        cat_param: str,
        target_count: int,
        documents: List[Dict[str, Any]],
        seen_urls: set,
    ) -> None:
        page = 1
        while len(documents) < target_count and page <= self.max_pages:
            params: Dict[str, Any] = {
                "per_page": self.per_page,
                "page": page,
                "_fields": "id,date,link,title,content,categories",
            }
            if cat_param:
                params["categories"] = cat_param

            posts = self.fetch_json(self.api_url, params=params)
            if not posts or not isinstance(posts, list):
                break

            for post in posts:
                if len(documents) >= target_count:
                    break
                doc = self._parse_post(post, seen_urls, len(documents) + 1)
                if doc is not None:
                    documents.append(doc)

            if len(posts) < self.per_page:
                break
            page += 1

    def crawl(self, max_documents: int = 300) -> List[Dict[str, Any]]:
        """Crawl WordPress REST API posts across configured category batches."""
        documents: List[Dict[str, Any]] = []
        seen_urls = set()

        for idx, (cat_param, fraction) in enumerate(self.category_batches):
            if len(documents) >= max_documents:
                break
            if fraction is None or idx == len(self.category_batches) - 1:
                batch_target = max_documents
            else:
                batch_quota = max(1, int(round(max_documents * fraction)))
                batch_target = min(max_documents, len(documents) + batch_quota)
            self._crawl_batch(cat_param, batch_target, documents, seen_urls)

        # Second pass if earlier quota-limited batches left room below max_documents
        if len(documents) < max_documents and any(f is not None for _, f in self.category_batches):
            for cat_param, _ in self.category_batches:
                if len(documents) >= max_documents:
                    break
                self._crawl_batch(cat_param, max_documents, documents, seen_urls)

        return documents[:max_documents]
