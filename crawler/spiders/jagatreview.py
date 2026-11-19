from crawler.spiders.wp_rest import WPJsonSpider


class JagatReviewSpider(WPJsonSpider):
    """WordPress REST API spider for Jagat Review laptop and gadget reviews."""

    def __init__(self, delay_seconds: float = 0.4):
        super().__init__(
            name="Jagat Review",
            base_url="https://www.jagatreview.com/",
            api_url="https://www.jagatreview.com/wp-json/wp/v2/posts",
            doc_id_prefix="jagatreview",
            # Category 46: Notebook/Laptop (55%), Category 38: Gadget/Smartphone (45%)
            category_batches=[("46", 0.55), ("38", 0.45)],
            delay_seconds=delay_seconds,
            per_page=50,
            min_chars=700,
            default_category="smartphone",
        )
