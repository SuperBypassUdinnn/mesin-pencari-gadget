from fastapi.testclient import TestClient

from backend.app.db import init_db, insert_document
from backend.app.main import create_app


class MockBM25:
    """Deterministic mock BM25 engine returning fixed ranked results."""

    def __init__(self, results):
        self.results = results

    def search(self, query_tokens, top_k=10):
        key = " ".join(query_tokens)
        return self.results.get(key, [])[:top_k]


class MockSBERT:
    """Deterministic mock S-BERT engine returning fixed ranked results."""

    def __init__(self, results):
        self.results = results

    def search(self, query, top_k=10):
        return self.results.get(query, [])[:top_k]


def build_app():
    conn = init_db(":memory:")
    docs = [
        {
            "id": "doc1",
            "title": "Review Xiaomi 13T",
            "source": "Gadgetren",
            "url": "https://gadgetren.com/xiaomi-13t",
            "category": "smartphone",
            "date": "2024-01-15",
            "specs": {"chipset": "Dimensity 8200 Ultra", "ram": "12GB"},
            "content": "Xiaomi 13T adalah smartphone dengan kamera Leica dan layar 120Hz.",
        },
        {
            "id": "doc2",
            "title": "Samsung Galaxy S24 Review",
            "source": "Gadgetren",
            "url": "https://gadgetren.com/samsung-s24",
            "category": "smartphone",
            "date": "2024-02-20",
            "specs": {"chipset": "Snapdragon 8 Gen 2", "ram": "8GB"},
            "content": "Samsung Galaxy S24 dilengkapi dengan layar AMOLED dan kamera 50MP.",
        },
    ]
    for doc in docs:
        insert_document(conn, doc)

    bm25 = MockBM25({"xiaomi 13t": [("doc1", 0.8), ("doc2", 0.2)]})
    sbert = MockSBERT({"xiaomi": [("doc2", 0.9), ("doc1", 0.4)]})

    app = create_app(
        db_conn=conn,
        bm25_engine=bm25,
        sbert_engine=sbert,
    )
    return app


class TestHealth:
    def test_health_returns_ok_and_docs_count(self):
        client = TestClient(build_app())
        response = client.get("/api/health")
        assert response.status_code == 200
        body = response.json()
        assert body["status"] == "ok"
        assert body["docs_count"] == 2


class TestSearch:
    def test_search_algo_both_returns_bm25_and_sbert(self):
        client = TestClient(build_app())
        response = client.get(
            "/api/search", params={"q": "xiaomi 13t", "algo": "both", "top_k": 10}
        )
        assert response.status_code == 200
        body = response.json()
        assert "bm25" in body
        assert "sbert" in body
        assert "results" in body["bm25"]
        assert "latency_ms" in body["bm25"]
        assert "results" in body["sbert"]
        assert "latency_ms" in body["sbert"]
        bm25_ids = [item["id"] for item in body["bm25"]["results"]]
        assert bm25_ids == ["doc1", "doc2"]

    def test_search_algo_bm25_only(self):
        client = TestClient(build_app())
        response = client.get(
            "/api/search", params={"q": "xiaomi 13t", "algo": "bm25", "top_k": 10}
        )
        assert response.status_code == 200
        body = response.json()
        assert "bm25" in body
        assert "sbert" not in body

    def test_search_algo_sbert_only(self):
        client = TestClient(build_app())
        response = client.get(
            "/api/search", params={"q": "xiaomi", "algo": "sbert", "top_k": 10}
        )
        assert response.status_code == 200
        body = response.json()
        assert "sbert" in body
        assert "bm25" not in body

    def test_search_result_item_fields(self):
        client = TestClient(build_app())
        response = client.get(
            "/api/search", params={"q": "xiaomi 13t", "algo": "bm25", "top_k": 10}
        )
        assert response.status_code == 200
        item = response.json()["bm25"]["results"][0]
        for field in (
            "id",
            "title",
            "source",
            "url",
            "category",
            "score",
            "specs",
            "snippet",
        ):
            assert field in item, f"missing field: {field}"
        assert isinstance(item["score"], float)
        assert isinstance(item["specs"], dict)
        assert isinstance(item["snippet"], str)
        assert len(item["snippet"]) <= 200

    def test_search_empty_query_returns_empty_results(self):
        client = TestClient(build_app())
        response = client.get(
            "/api/search", params={"q": "", "algo": "both", "top_k": 10}
        )
        assert response.status_code == 200
        body = response.json()
        assert body["bm25"]["results"] == []
        assert body["bm25"]["latency_ms"] == 0.0
        assert body["sbert"]["results"] == []
        assert body["sbert"]["latency_ms"] == 0.0

    def test_search_defaults_algo_both_and_top_k_10(self):
        client = TestClient(build_app())
        response = client.get("/api/search", params={"q": "xiaomi 13t"})
        assert response.status_code == 200
        body = response.json()
        assert "bm25" in body
        assert "sbert" in body


class TestDocumentDetail:
    def test_document_found(self):
        client = TestClient(build_app())
        response = client.get("/api/documents/doc1")
        assert response.status_code == 200
        body = response.json()
        assert body["id"] == "doc1"
        assert body["title"] == "Review Xiaomi 13T"
        assert body["source"] == "Gadgetren"
        assert body["url"] == "https://gadgetren.com/xiaomi-13t"
        assert body["category"] == "smartphone"
        assert body["date"] == "2024-01-15"
        assert body["specs"] == {"chipset": "Dimensity 8200 Ultra", "ram": "12GB"}
        assert "content" in body

    def test_document_not_found_returns_404(self):
        client = TestClient(build_app())
        response = client.get("/api/documents/nonexistent")
        assert response.status_code == 404
        assert response.json() == {"detail": "Document not found"}


class TestEvaluation:
    def test_evaluation_returns_bm25_and_sbert_metrics(self):
        client = TestClient(build_app())
        response = client.get("/api/evaluation")
        assert response.status_code == 200
        body = response.json()
        assert "bm25" in body
        assert "sbert" in body
        assert "test_queries_count" in body
