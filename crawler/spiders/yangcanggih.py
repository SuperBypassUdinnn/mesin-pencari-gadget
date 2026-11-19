from crawler.spiders.wp_rest import WPJsonSpider


class YangcanggihSpider(WPJsonSpider):
    """WordPress REST API spider for Yangcanggih dedicated Review category."""

    def __init__(self, delay_seconds: float = 0.4):
        super().__init__(
            name="Yangcanggih",
            base_url="https://yangcanggih.com/",
            api_url="https://yangcanggih.com/wp-json/wp/v2/posts",
            doc_id_prefix="yangcanggih",
            # Category 569: Review (dedicated review articles with spec tables)
            category_batches=[("569", 1.0)],
            delay_seconds=delay_seconds,
            per_page=50,
            min_chars=700,
            default_category="smartphone",
        )
