from bs4 import BeautifulSoup
from backend.app.db import init_db, insert_document, get_all_documents, get_document_by_id
from crawler.spiders.base import BaseSpider
from crawler.spiders.droidlime import DroidlimeSpider
from crawler.spiders.gadgetren import GadgetrenSpider
from crawler.spiders.hybrid import HybridSpider
from crawler.spiders.jagatreview import JagatReviewSpider
from crawler.spiders.yangcanggih import YangcanggihSpider


def test_db_insert_and_retrieve(tmp_path):
    db_file = str(tmp_path / "test_gadget.db")
    conn = init_db(db_file)
    sample_doc = {
        "id": "doc_001",
        "title": "Review Xiaomi 13T",
        "source": "Gadgetren",
        "url": "https://gadgetren.com/sample",
        "category": "smartphone",
        "date": "2024-01-15",
        "specs": {"chipset": "Dimensity 8200 Ultra", "ram": "12GB"},
        "content": "Ini adalah isi artikel ulasan gadget yang lengkap dengan kamera Leica.",
    }
    insert_document(conn, sample_doc)
    docs = get_all_documents(conn)
    assert len(docs) == 1
    assert docs[0]["title"] == "Review Xiaomi 13T"
    assert docs[0]["source"] == "Gadgetren"
    assert docs[0]["specs"]["ram"] == "12GB"

    retrieved = get_document_by_id(conn, "doc_001")
    assert retrieved is not None
    assert retrieved["title"] == "Review Xiaomi 13T"

    missing = get_document_by_id(conn, "doc_999")
    assert missing is None


def test_base_spider_schema_validation():
    spider = BaseSpider(name="TestSpider", base_url="https://example.com")
    valid_doc = spider.build_document(
        doc_id="doc_test_1",
        title="Laptop Test",
        source="TestPortal",
        url="https://example.com/test",
        category="laptop",
        date="2024-02-01",
        specs={"ram": "16GB"},
        content="Artikel ulasan laptop untuk coding.",
    )
    assert valid_doc["id"] == "doc_test_1"
    assert valid_doc["source"] == "TestPortal"
    assert "specs" in valid_doc


def test_clean_html_content_strips_noise():
    spider = BaseSpider(name="Test", base_url="https://example.com", delay_seconds=0.0)
    raw_html = """
    <div class="sharedaddy"><div class="inner-share">Share this post</div></div>
    <p>Baca juga: Artikel lain yang tidak relevan.</p>
    <p>Smartphone ini hadir dengan layar AMOLED 120Hz yang sangat cerah di luar ruangan dan responsif untuk gaming.</p>
    <script>alert('xss');</script>
    <p>Baterai berkapasitas 5000 mAh mampu bertahan seharian penuh dengan dukungan pengisian cepat 67W.</p>
    """
    cleaned = spider.clean_html_content(raw_html)
    assert "alert" not in cleaned
    assert "Share this" not in cleaned
    assert "Baca juga" not in cleaned
    assert "AMOLED 120Hz" in cleaned
    assert "5000 mAh" in cleaned


def test_extract_specs_table_and_regex_fallback():
    spider = BaseSpider(name="Test", base_url="https://example.com", delay_seconds=0.0)
    html_block = """
    <table>
      <tr><th>Chipset</th><td>Snapdragon 8 Gen 2</td></tr>
      <tr><th>RAM</th><td>12GB LPDDR5X</td></tr>
      <tr><th>Layar</th><td>6.7 inci AMOLED 120Hz</td></tr>
    </table>
    """
    soup = BeautifulSoup(html_block, "html.parser")
    prose = "Perangkat ini membawa baterai 5000 mAh fast charging 80W dan kamera 50MP OIS dengan harga Rp 9.999.000."
    specs = spider.extract_specs_from_soup(soup, full_text=prose)
    assert specs["chipset"] == "Snapdragon 8 Gen 2"
    assert specs["ram"] == "12GB LPDDR5X"
    assert specs["layar"] == "6.7 inci AMOLED 120Hz"
    assert "5000 mAh" in specs["baterai"]
    assert "50MP" in specs["kamera"]
    assert "Rp 9.999.000" in specs["harga"]


def test_infer_category_and_validity():
    spider = BaseSpider(name="Test", base_url="https://example.com", delay_seconds=0.0)
    laptop_text = " ".join(["Laptop gaming dengan prosesor Intel Core i7, GPU RTX 4060, RAM 16GB, layar OLED, dan SSD NVMe 1TB untuk rendering."] * 10)
    assert spider.infer_category("Review ASUS ROG Zephyrus G16", laptop_text) == "laptop"
    assert spider.is_valid_gadget_review("Review ASUS ROG Zephyrus G16", laptop_text) is True

    offtopic_text = " ".join(["Film aksi terbaru tayang di bioskop bulan ini dengan pemeran utama ternama."] * 15)
    assert spider.is_valid_gadget_review("Sinopsis Film Bioskop Terbaru 2026", offtopic_text) is False


def _make_wp_post(idx: int, title: str, url: str, body: str, date: str = "2026-10-15T10:00:00"):
    return {
        "id": idx,
        "date": date,
        "link": url,
        "title": {"rendered": title},
        "content": {"rendered": body},
        "categories": [1],
    }


def test_wp_rest_spiders_parse_mocked_responses(monkeypatch):
    long_laptop_html = "".join(
        f"<p>Bagian {i}: Ulasan mendalam laptop coding dan gaming dengan prosesor Intel Core Ultra 7, "
        f"RAM 16GB LPDDR5X, layar OLED 14 inci 120Hz, penyimpanan 1TB SSD NVMe, serta baterai 75Wh "
        f"yang sangat awet untuk mahasiswa dan kreator konten.</p>"
        for i in range(1, 6)
    ) + "<table><tr><td>Prosesor</td><td>Intel Core Ultra 7 155H</td></tr><tr><td>RAM</td><td>16GB LPDDR5X</td></tr></table>"
    long_phone_html = "".join(
        f"<p>Bagian {i}: Review smartphone flagship dengan chipset Snapdragon 8 Gen 3, kamera utama 50MP OIS "
        f"untuk fotografi malam hari, layar AMOLED 120Hz, RAM 12GB, serta baterai 5000 mAh fast charging 80W "
        f"dengan harga Rp 10.999.000 di Indonesia.</p>"
        for i in range(1, 6)
    )

    for spider, prefix in [
        (JagatReviewSpider(delay_seconds=0.0), "jagatreview"),
        (YangcanggihSpider(delay_seconds=0.0), "yangcanggih"),
        (DroidlimeSpider(delay_seconds=0.0), "droidlime"),
        (HybridSpider(delay_seconds=0.0), "hybrid"),
    ]:
        mock_posts = [
            _make_wp_post(1, f"Review Laptop Pro {prefix}", f"https://example.com/{prefix}-laptop", long_laptop_html),
            _make_wp_post(2, f"Review Smartphone Flagship {prefix}", f"https://example.com/{prefix}-phone", long_phone_html),
            _make_wp_post(3, "Artikel Pendek", f"https://example.com/{prefix}-short", "<p>Terlalu singkat.</p>"),
        ]

        def fake_fetch_json(url, params=None, retries=3, posts=mock_posts):
            page = (params or {}).get("page", 1)
            return posts if page == 1 else []

        monkeypatch.setattr(spider, "fetch_json", fake_fetch_json)
        docs = spider.crawl(max_documents=2)
        assert len(docs) == 2
        assert docs[0]["id"].startswith(f"{prefix}_")
        assert docs[0]["date"] == "2026-10-15"
        assert docs[0]["category"] == "laptop"
        assert docs[1]["category"] == "smartphone"
        assert docs[0]["specs"]


def test_gadgetren_spider_handles_403_gracefully(monkeypatch):
    spider = GadgetrenSpider(delay_seconds=0.0)

    def fake_fetch(url):
        spider.last_status_code = 403
        return None

    monkeypatch.setattr(spider, "fetch", fake_fetch)
    docs = spider.crawl(max_documents=10)
    assert docs == []
