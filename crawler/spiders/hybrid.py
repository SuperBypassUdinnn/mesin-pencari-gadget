import re
from crawler.spiders.wp_rest import WPJsonSpider

HYBRID_REQUIRED_SIGNALS = (
    "review",
    "ulasan",
    "hands-on",
    "spesifikasi",
    "fitur",
    "performa",
    "kamera",
    "layar",
    "chipset",
    "laptop",
    "smartphone",
    "tablet",
    "smartwatch",
    "tws",
    "headset",
)

HYBRID_ESPORTS_EXCLUSION = re.compile(
    r"\b(esports?|turnamen|mpl|liga|juara|roster|valorant|mobile legends|dota|free fire)\b",
    re.IGNORECASE,
)


class HybridSpider(WPJsonSpider):
    """WordPress REST API spider for Hybrid.co.id substantive gadget articles."""

    def __init__(self, delay_seconds: float = 0.4):
        super().__init__(
            name="Hybrid",
            base_url="https://hybrid.co.id/",
            api_url="https://hybrid.co.id/wp-json/wp/v2/posts",
            doc_id_prefix="hybrid",
            # Categories: 80523=Gadget, 12748=Gadget DS
            category_batches=[("80523,12748", 1.0)],
            delay_seconds=delay_seconds,
            per_page=50,
            min_chars=900,
            default_category="smartphone",
        )

    def passes_portal_filter(self, title: str, content: str) -> bool:
        """Keep substantive gadget hardware reviews/features and skip short news or esports."""
        title_l = title.lower()
        if HYBRID_ESPORTS_EXCLUSION.search(title_l) and not any(
            kw in title_l for kw in ("review", "ulasan", "spesifikasi", "hands-on", "laptop", "smartphone")
        ):
            return False
        combined = f"{title_l} {content.lower()}"
        return sum(1 for sig in HYBRID_REQUIRED_SIGNALS if sig in combined) >= 3
