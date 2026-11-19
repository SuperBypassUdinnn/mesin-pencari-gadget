from crawler.spiders.base import BaseSpider
from crawler.spiders.droidlime import DroidlimeSpider
from crawler.spiders.gadgetren import GadgetrenSpider
from crawler.spiders.hybrid import HybridSpider
from crawler.spiders.jagatreview import JagatReviewSpider
from crawler.spiders.wp_rest import WPJsonSpider
from crawler.spiders.yangcanggih import YangcanggihSpider

__all__ = [
    "BaseSpider",
    "WPJsonSpider",
    "GadgetrenSpider",
    "JagatReviewSpider",
    "DroidlimeSpider",
    "YangcanggihSpider",
    "HybridSpider",
]
