import html
import re
import time
from typing import Any, Dict, List, Optional
import requests
from bs4 import BeautifulSoup

BOILERPLATE_PREFIXES = (
    "baca juga",
    "simak juga",
    "ikuti berita",
    "advertisement",
    "tag:",
    "artikel terkait",
    "lihat juga",
)

OFFTOPIC_TITLE_PATTERNS = (
    r"\bfossil\b.*\bwatch\b",
    r"\btrailer\b",
    r"\bsinopsis\b",
    r"\bbioskop\b",
    r"\bnetflix\b",
    r"\banime\b",
    r"\bmanga\b",
    r"\bgiveaway\b",
    r"\bundian\b",
    r"\bihsg\b",
    r"\bsaham\b",
    r"\bpaket data\b",
    r"\bkuota internet\b",
    r"\btarif\b",
    r"\bpromo pulsa\b",
    r"\baction figure\b",
    r"\blego\b",
)

GADGET_RELEVANCE_TERMS = (
    "smartphone",
    "ponsel",
    "hp",
    "laptop",
    "notebook",
    "ultrabook",
    "tablet",
    "ipad",
    "smartwatch",
    "wearable",
    "earbuds",
    "tws",
    "headphone",
    "headset",
    "kamera",
    "lensa",
    "prosesor",
    "chipset",
    "snapdragon",
    "dimensity",
    "exynos",
    "intel",
    "ryzen",
    "gpu",
    "rtx",
    "ram",
    "ssd",
    "baterai",
    "layar",
    "amoled",
    "oled",
    "refresh rate",
    "fast charging",
    "spesifikasi",
    "review",
    "ulasan",
    "hands-on",
    "benchmark",
    "keyboard",
    "mouse",
    "monitor",
    "router",
)

SPEC_KEY_MAP = {
    "chipset": "chipset",
    "soc": "chipset",
    "system on chip": "chipset",
    "prosesor": "prosesor",
    "processor": "prosesor",
    "cpu": "prosesor",
    "gpu": "gpu",
    "grafis": "gpu",
    "kartu grafis": "gpu",
    "vga": "gpu",
    "ram": "ram",
    "memori": "ram",
    "memory": "ram",
    "storage": "storage",
    "penyimpanan": "storage",
    "memori internal": "storage",
    "rom": "storage",
    "ssd": "storage",
    "layar": "layar",
    "display": "layar",
    "screen": "layar",
    "kamera": "kamera",
    "camera": "kamera",
    "kamera utama": "kamera",
    "kamera belakang": "kamera",
    "baterai": "baterai",
    "battery": "baterai",
    "daya": "baterai",
    "sistem operasi": "os",
    "operating system": "os",
    "os": "os",
    "harga": "harga",
    "price": "harga",
}


class BaseSpider:
    """Base HTTP and WordPress REST API spider for Indonesian gadget portals."""

    def __init__(self, name: str, base_url: str, delay_seconds: float = 1.0):
        self.name = name
        self.base_url = base_url
        self.delay_seconds = delay_seconds
        self.last_status_code: Optional[int] = None
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/122.0.0.0 Safari/537.36 GadgetSearchBot/1.0"
                ),
                "Accept": "application/json, text/html;q=0.9, */*;q=0.8",
            }
        )

    def fetch(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch an HTML page and return a BeautifulSoup parser, or None on error/403."""
        try:
            time.sleep(self.delay_seconds)
            response = self.session.get(url, timeout=15)
            self.last_status_code = response.status_code
            if response.status_code == 200:
                return BeautifulSoup(response.text, "html.parser")
            if response.status_code == 403:
                print(
                    f"[{self.name}] Access restricted (HTTP 403) for {url} - respecting site policy"
                )
                return None
            return None
        except Exception as e:
            self.last_status_code = None
            print(f"[{self.name}] Error fetching {url}: {e}")
            return None

    def fetch_json(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        retries: int = 3,
    ) -> Optional[Any]:
        """Fetch JSON from a REST API endpoint with polite rate limiting and retries."""
        for attempt in range(retries):
            try:
                time.sleep(self.delay_seconds)
                response = self.session.get(url, params=params, timeout=20)
                self.last_status_code = response.status_code
                if response.status_code == 200:
                    return response.json()
                if response.status_code in (400, 404):
                    return None
                if response.status_code == 403:
                    print(
                        f"[{self.name}] Access restricted (HTTP 403) for {url} - respecting site policy"
                    )
                    return None
                if response.status_code in (429, 500, 502, 503, 504):
                    backoff = (attempt + 1) * 1.5
                    print(
                        f"[{self.name}] HTTP {response.status_code} on {url}, retrying in {backoff:.1f}s..."
                    )
                    time.sleep(backoff)
                    continue
                return None
            except Exception as e:
                self.last_status_code = None
                if attempt < retries - 1:
                    time.sleep((attempt + 1) * 1.5)
                    continue
                print(f"[{self.name}] Error fetching JSON {url}: {e}")
                return None
        return None

    def clean_title(self, raw_title: str) -> str:
        """Unescape HTML entities and strip markup from an article title."""
        text = html.unescape(raw_title or "")
        text = BeautifulSoup(text, "html.parser").get_text(" ", strip=True)
        return re.sub(r"\s+", " ", text).strip()

    def clean_html_content(self, html_str: str, max_chars: int = 4500) -> str:
        """Extract clean Indonesian review prose from HTML content."""
        if not html_str:
            return ""
        unescaped = html.unescape(html_str)
        soup = BeautifulSoup(unescaped, "html.parser")

        for tag in soup.find_all(["script", "style", "figure", "figcaption", "iframe", "nav", "footer", "aside"]):
            tag.decompose()

        noise_pattern = re.compile(
            r"(related|baca-juga|share|social|author-box|comment|ads|promo)",
            re.IGNORECASE,
        )
        for el in list(soup.find_all(["div", "section", "aside"])):
            if getattr(el, "decomposed", False) or el.attrs is None:
                continue
            classes = " ".join(el.get("class", []) or [])
            el_id = el.get("id", "") or ""
            if noise_pattern.search(f"{classes} {el_id}"):
                el.decompose()

        chunks: List[str] = []
        seen_lines = set()
        for el in soup.find_all(["p", "li"]):
            text = re.sub(r"\s+", " ", el.get_text(" ", strip=True)).strip()
            if len(text) < 25:
                continue
            lowered = text.lower()
            if any(lowered.startswith(prefix) for prefix in BOILERPLATE_PREFIXES):
                continue
            if lowered in seen_lines:
                continue
            seen_lines.add(lowered)
            chunks.append(text)

        if not chunks:
            fallback = re.sub(r"\s+", " ", soup.get_text(" ", strip=True)).strip()
            content = fallback
        else:
            content = " ".join(chunks)

        content = re.sub(r"\s+", " ", content).strip()
        if len(content) > max_chars:
            truncated = content[:max_chars]
            last_period = truncated.rfind(". ")
            if last_period > int(max_chars * 0.6):
                content = truncated[: last_period + 1].strip()
            else:
                last_space = truncated.rfind(" ")
                content = (truncated[:last_space] if last_space > 0 else truncated).strip()
        return content

    def _map_spec_key(self, raw_key: str) -> Optional[str]:
        cleaned = re.sub(r"[^a-z0-9\s]", " ", raw_key.lower()).strip()
        cleaned = re.sub(r"\s+", " ", cleaned)
        if not cleaned or len(cleaned) > 35:
            return None
        if cleaned in SPEC_KEY_MAP:
            return SPEC_KEY_MAP[cleaned]
        for alias, canonical in SPEC_KEY_MAP.items():
            if alias == "os" and cleaned != "os":
                continue
            if re.search(rf"\b{re.escape(alias)}\b", cleaned):
                return canonical
        return None

    def _clean_spec_value(self, raw_val: str, max_len: int = 90) -> str:
        val = re.sub(r"\s+", " ", html.unescape(raw_val or "")).strip(" :-|")
        if len(val) > max_len:
            cut = val[:max_len]
            last_space = cut.rfind(" ")
            val = (cut[:last_space] if last_space > 20 else cut).strip()
        return val

    def extract_specs_from_soup(
        self, soup: Optional[BeautifulSoup], full_text: str = ""
    ) -> Dict[str, str]:
        """Extract canonical gadget technical specs from HTML tables, lists, and prose."""
        specs: Dict[str, str] = {}

        if soup is not None:
            for table in soup.find_all("table"):
                for row in table.find_all("tr"):
                    cols = row.find_all(["td", "th"])
                    if len(cols) == 2:
                        canonical = self._map_spec_key(cols[0].get_text(" ", strip=True))
                        val = self._clean_spec_value(cols[1].get_text(" ", strip=True))
                        if canonical and val and len(val) <= 160 and canonical not in specs:
                            specs[canonical] = val

            for el in soup.find_all(["li", "p"]):
                text = re.sub(r"\s+", " ", el.get_text(" ", strip=True)).strip()
                if ":" in text and len(text) <= 220:
                    raw_k, raw_v = text.split(":", 1)
                    canonical = self._map_spec_key(raw_k)
                    val = self._clean_spec_value(raw_v)
                    if canonical and val and len(val) <= 160 and canonical not in specs:
                        specs[canonical] = val

        text_source = full_text or (soup.get_text(" ", strip=True) if soup is not None else "")
        if text_source:
            regex_extractors = [
                (
                    "chipset",
                    r"\b((?:Qualcomm\s+)?Snapdragon\s+\d+\s*(?:s\s*Gen\s*\d+|Gen\s*\d+|\+|Plus)?|"
                    r"(?:MediaTek\s+)?Dimensity\s+\d+(?:\s*(?:Ultra|Plus|Pro|Max))?|"
                    r"(?:MediaTek\s+)?Helio\s+[GP]\d+|Exynos\s+\d+|Apple\s+[AM]\d+(?:\s*(?:Pro|Max|Ultra))?|"
                    r"(?:Google\s+)?Tensor\s+G\d+|Unisoc\s+[A-Z]?\d+)\b",
                ),
                (
                    "prosesor",
                    r"\b(Intel\s+Core\s+(?:Ultra\s+)?(?:i[3579]|[3579])(?:-[A-Za-z0-9]+)?|"
                    r"AMD\s+Ryzen\s+(?:AI\s+)?[3579]\s+[A-Za-z0-9]+|"
                    r"Apple\s+M[1-5](?:\s*(?:Pro|Max|Ultra))?)\b",
                ),
                (
                    "gpu",
                    r"\b(NVIDIA\s+(?:GeForce\s+)?RTX\s+\d{4}(?:\s*(?:Ti|Super))?|"
                    r"AMD\s+Radeon\s+(?:RX\s+\d+[A-Z]?|Graphics|\d+M)|"
                    r"Intel\s+Arc\s+Graphics)\b",
                ),
                (
                    "ram",
                    r"\bRAM\s+(?:sebesar\s+)?(\d{1,3}\s*GB(?:\s*(?:LPDDR\dX?|DDR\d))?)|"
                    r"\b(\d{1,3}\s*GB\s+(?:RAM|LPDDR\dX?|DDR\d))\b",
                ),
                (
                    "storage",
                    r"\b((?:128|256|512)\s*GB|(?:1|2|4)\s*TB)\s+"
                    r"(SSD(?:\s*NVMe)?|NVMe(?:\s*PCIe)?|UFS(?:\s*[\d.]+)?|eMMC|storage|memori internal)\b",
                ),
                (
                    "layar",
                    r"\b(\d(?:\.\d{1,2})?\s*(?:inci|inch|\")[^.,;\n]{0,45}?"
                    r"(?:AMOLED|OLED|IPS|LCD|LTPO|Retina|FHD\+|Full\s*HD|QHD\+|2\.8K|3K|4K|\d{2,3}\s*Hz))\b",
                ),
                (
                    "kamera",
                    r"\bkamera(?:\s+(?:utama|belakang))?\s+(\d{2,3}\s*MP(?:\s*(?:OIS|Leica|Zeiss|Hasselblad|Sony|utama))?)|"
                    r"\b(\d{2,3}\s*MP\s*(?:OIS|Leica|Zeiss|Hasselblad|utama|telefoto|periskop))\b",
                ),
                (
                    "baterai",
                    r"\b(\d{4,5}\s*mAh(?:\s*[^.,;\n]{0,30}?(?:W|watt|charging|fast\s*charging))?|\d{2,3}\s*Wh)\b",
                ),
                (
                    "harga",
                    r"\b(Rp\s*\d{1,3}(?:[.,]\d{3})*(?:[.,]\d+)?(?:\s*(?:juta|jt|ribu|rb))?)\b",
                ),
            ]
            for key, pattern in regex_extractors:
                if key in specs:
                    continue
                match = re.search(pattern, text_source, re.IGNORECASE)
                if match:
                    groups = [g for g in match.groups() if g]
                    raw_val = " ".join(groups) if key == "storage" and len(groups) > 1 else (groups[0] if groups else match.group(0))
                    val = self._clean_spec_value(raw_val)
                    if val:
                        specs[key] = val

        return specs

    def infer_category(
        self, title: str, content: str, default: str = "smartphone"
    ) -> str:
        """Infer canonical gadget category with title-weighted keyword matching."""
        title_l = (title or "").lower()
        body_l = (content or "").lower()

        rules = [
            ("laptop", ("laptop", "notebook", "ultrabook", "macbook", "zenbook", "vivobook", "rog", "legion", "thinkpad", "ideapad", "predator", "tuf gaming")),
            ("tablet", ("tablet", "ipad", "galaxy tab", "xpad", "matepad", "pad ")),
            ("wearable", ("smartwatch", "smartband", "watch ", "band ", "wearable", "jam tangan pintar", "cincin pintar")),
            ("audio", ("tws", "earbuds", "headphone", "headset", "earphone", "speaker", "soundbar", "anc")),
            ("camera", ("kamera mirrorless", "dslr", "action cam", "action camera", "fujifilm", "sony alpha", "canon eos", "gopro", "insta360", "drone")),
            ("peripheral", ("keyboard", "mouse", "monitor", "router", "ssd eksternal", "powerbank", "charger", "gan ", "vga", "graphics card", "motherboard")),
            ("smartphone", ("smartphone", "ponsel", "hp ", "iphone", "galaxy a", "galaxy s", "galaxy z", "xiaomi", "redmi", "poco", "oppo", "vivo", "realme", "infinix", "iqoo", "tecno", "asus zenfone")),
        ]

        for cat, keywords in rules:
            if any(kw in title_l for kw in keywords):
                return cat

        best_cat = default
        best_hits = 0
        for cat, keywords in rules:
            hits = sum(1 for kw in keywords if kw in body_l)
            if hits > best_hits:
                best_hits = hits
                best_cat = cat
        return best_cat

    def append_specs_summary(self, content: str, specs: Dict[str, str]) -> str:
        """Append missing extracted spec values so lexical and semantic indices capture them."""
        if not specs:
            return content
        content_lower = content.lower()
        missing_parts: List[str] = []
        for k, v in specs.items():
            if not v:
                continue
            if str(v).lower() not in content_lower:
                missing_parts.append(f"{k} {v}")
        if not missing_parts:
            return content
        summary = " Spesifikasi utama: " + ", ".join(missing_parts) + "."
        return (content.rstrip() + summary).strip()

    def is_valid_gadget_review(
        self, title: str, content: str, min_chars: int = 600
    ) -> bool:
        """Validate article length, gadget domain relevance, and exclude off-topic posts."""
        title_clean = (title or "").strip()
        content_clean = (content or "").strip()
        if not title_clean or len(content_clean) < min_chars:
            return False

        title_l = title_clean.lower()
        for pat in OFFTOPIC_TITLE_PATTERNS:
            if re.search(pat, title_l):
                return False

        combined = f"{title_l} {content_clean.lower()}"
        signal_hits = sum(1 for term in GADGET_RELEVANCE_TERMS if term in combined)
        return signal_hits >= 2

    def build_document(
        self,
        doc_id: str,
        title: str,
        source: str,
        url: str,
        category: str,
        date: str,
        specs: Dict[str, Any],
        content: str,
    ) -> Dict[str, Any]:
        return {
            "id": doc_id,
            "title": title.strip(),
            "source": source.strip(),
            "url": url.strip(),
            "category": category.strip().lower(),
            "date": date.strip(),
            "specs": specs or {},
            "content": content.strip(),
        }

    def crawl(self, max_documents: int = 350) -> List[Dict[str, Any]]:
        raise NotImplementedError("Subclasses must implement crawl()")
