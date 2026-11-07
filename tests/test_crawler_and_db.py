import os
import sqlite3
import pytest
from backend.app.db import init_db, insert_document, get_all_documents, get_document_by_id
from crawler.spiders.base import BaseSpider

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
        "content": "Ini adalah isi artikel ulasan gadget yang lengkap dengan kamera Leica."
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
        content="Artikel ulasan laptop untuk coding."
    )
    assert valid_doc["id"] == "doc_test_1"
    assert valid_doc["source"] == "TestPortal"
    assert "specs" in valid_doc
