from crawler.spiders.wp_rest import WPJsonSpider


class DroidlimeSpider(WPJsonSpider):
    """WordPress REST API spider for Droidlime reviews, hands-on, prices, and features."""

    def __init__(self, delay_seconds: float = 0.4):
        super().__init__(
            name="Droidlime",
            base_url="https://www.droidlime.com/",
            api_url="https://www.droidlime.com/wp-json/wp/v2/posts",
            doc_id_prefix="droidlime",
            # Categories: 3=Review, 831=Hands-on, 43721=Harga HP, 4=Fitur
            category_batches=[("3", None), ("831", None), ("43721", None), ("4", None)],
            delay_seconds=delay_seconds,
            per_page=50,
            min_chars=500,
            default_category="smartphone",
        )
