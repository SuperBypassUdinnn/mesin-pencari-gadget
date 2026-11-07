import time
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from backend.app.db import get_all_documents

DEFAULT_TEST_QUERIES: list[dict[str, Any]] = [
    {"id": "q1", "query": "xiaomi 13t"},
    {"id": "q2", "query": "samsung galaxy"},
]

DEFAULT_GROUND_TRUTH: dict[str, set] = {
    "q1": {"doc1"},
    "q2": {"doc2"},
}


def _empty_result() -> dict[str, Any]:
    return {"results": [], "latency_ms": 0.0}


def _build_result_items(
    doc_lookup: dict[str, dict[str, Any]], ranked: list[tuple], top_k: int
) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for doc_id, score in ranked[:top_k]:
        doc = doc_lookup.get(doc_id)
        if doc is None:
            continue
        content = str(doc.get("content", ""))
        snippet = content[:200]
        items.append(
            {
                "id": doc["id"],
                "title": doc["title"],
                "source": doc["source"],
                "url": doc["url"],
                "category": doc["category"],
                "score": float(score),
                "specs": doc.get("specs", {}),
                "snippet": snippet,
            }
        )
    return items


def _query_tokens(query_text: str, preprocessor: Any | None) -> list[str]:
    if preprocessor is not None:
        return preprocessor.preprocess(query_text)
    return query_text.lower().split()


def create_app(
    db_conn: Any | None = None,
    bm25_engine: Any | None = None,
    sbert_engine: Any | None = None,
    preprocessor: Any | None = None,
    evaluator: Any | None = None,
) -> FastAPI:
    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.state.bm25_engine = bm25_engine
    app.state.sbert_engine = sbert_engine
    app.state.preprocessor = preprocessor
    app.state.evaluator = evaluator

    # Load documents into memory at startup so endpoints do not need to access
    # the SQLite connection across threads (TestClient runs endpoints in a
    # worker thread; sqlite3 connections are thread-bound by default).
    app.state.docs: dict[str, dict[str, Any]] = {}
    if db_conn is not None:
        for doc in get_all_documents(db_conn):
            app.state.docs[doc["id"]] = doc

    @app.get("/api/health")
    def health() -> dict[str, Any]:
        return {"status": "ok", "docs_count": len(app.state.docs)}

    @app.get("/api/search")
    def search(
        q: str = Query(default=""),
        algo: str = Query(default="both"),
        top_k: int = Query(default=10, ge=1),
    ) -> dict[str, Any]:
        bm25_engine = app.state.bm25_engine
        sbert_engine = app.state.sbert_engine
        preprocessor = app.state.preprocessor

        response: dict[str, Any] = {}
        query = (q or "").strip()

        if algo not in ("bm25", "sbert", "both"):
            algo = "both"

        # Empty query returns empty results with 0.0 latency per spec.
        if not query:
            if algo in ("bm25", "both"):
                response["bm25"] = _empty_result()
            if algo in ("sbert", "both"):
                response["sbert"] = _empty_result()
            return response

        if algo in ("bm25", "both"):
            if bm25_engine is not None:
                start = time.perf_counter()
                ranked = bm25_engine.search(
                    _query_tokens(query, preprocessor), top_k=top_k
                )
                latency_ms = (time.perf_counter() - start) * 1000.0
                response["bm25"] = {
                    "results": _build_result_items(app.state.docs, ranked, top_k),
                    "latency_ms": round(latency_ms, 4),
                }
            else:
                response["bm25"] = _empty_result()

        if algo in ("sbert", "both"):
            if sbert_engine is not None:
                start = time.perf_counter()
                ranked = sbert_engine.search(query, top_k=top_k)
                latency_ms = (time.perf_counter() - start) * 1000.0
                response["sbert"] = {
                    "results": _build_result_items(app.state.docs, ranked, top_k),
                    "latency_ms": round(latency_ms, 4),
                }
            else:
                response["sbert"] = _empty_result()

        return response

    @app.get("/api/documents/{doc_id}")
    def document_detail(doc_id: str) -> dict[str, Any]:
        doc = app.state.docs.get(doc_id)
        if doc is None:
            raise HTTPException(status_code=404, detail="Document not found")
        return doc

    @app.get("/api/evaluation")
    def evaluation() -> dict[str, Any]:
        test_queries_count = len(DEFAULT_TEST_QUERIES)

        def empty_metrics() -> dict[str, Any]:
            return {
                "mean_p5": 0.0,
                "mean_p10": 0.0,
                "mean_r5": 0.0,
                "mean_r10": 0.0,
                "mean_f1_5": 0.0,
                "mean_f1_10": 0.0,
                "map": 0.0,
                "avg_latency_ms": 0.0,
                "per_query_results": [],
            }

        bm25_metrics = empty_metrics()
        sbert_metrics = empty_metrics()

        if app.state.evaluator is not None:

            def bm25_search_fn(query_text: str) -> list[str]:
                if app.state.bm25_engine is None:
                    return []
                ranked = app.state.bm25_engine.search(
                    _query_tokens(query_text, app.state.preprocessor), top_k=10
                )
                return [doc_id for doc_id, _ in ranked]

            def sbert_search_fn(query_text: str) -> list[str]:
                if app.state.sbert_engine is None:
                    return []
                ranked = app.state.sbert_engine.search(query_text, top_k=10)
                return [doc_id for doc_id, _ in ranked]

            bm25_metrics = app.state.evaluator.evaluate_system(
                bm25_search_fn, DEFAULT_TEST_QUERIES, DEFAULT_GROUND_TRUTH
            )
            sbert_metrics = app.state.evaluator.evaluate_system(
                sbert_search_fn, DEFAULT_TEST_QUERIES, DEFAULT_GROUND_TRUTH
            )

        return {
            "bm25": bm25_metrics,
            "sbert": sbert_metrics,
            "test_queries_count": test_queries_count,
        }

    return app
