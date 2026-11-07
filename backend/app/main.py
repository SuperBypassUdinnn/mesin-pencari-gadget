import json
import os
import time
from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from backend.app.db import init_db, get_all_documents
from backend.app.engine.preprocessor import IndonesianPreprocessor
from backend.app.engine.bm25 import BM25Engine
from backend.app.engine.sbert import SBERTEngine
from backend.app.engine.evaluator import IREvaluator
from backend.app.engine.indexer import build_index

DEFAULT_TEST_QUERIES: List[Dict[str, Any]] = [
    {"id": "q01", "query": "Xiaomi 13T kamera Leica"},
    {"id": "q02", "query": "laptop gaming tipis performa kencang"},
    {"id": "q03", "query": "Samsung Galaxy baterai awet"},
    {"id": "q04", "query": "Infinix GT 10 Pro gaming"},
    {"id": "q05", "query": "Lenovo Legion prosesor Intel RTX"},
    {"id": "q06", "query": "smartphone fotografi malam hari redup"},
]

DEFAULT_GROUND_TRUTH: Dict[str, List[str]] = {
    "q01": ["gadgetren_0001"],
    "q02": ["jagatreview_0001", "jagatreview_0002"],
    "q03": ["droidlime_0001"],
    "q04": ["gadgetren_0002"],
    "q05": ["jagatreview_0002"],
    "q06": ["gadgetren_0001"],
}

def _empty_result() -> Dict[str, Any]:
    return {"results": [], "latency_ms": 0.0}

def _build_result_items(
    doc_lookup: Dict[str, Dict[str, Any]], ranked: List[tuple], top_k: int
) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
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

def _query_tokens(query_text: str, preprocessor: Optional[Any]) -> List[str]:
    if preprocessor is not None:
        return preprocessor.preprocess(query_text)
    return query_text.lower().split()

def load_ground_truth_from_disk(
    queries_path: str = "data/ground_truth/test_queries.json",
    rel_path: str = "data/ground_truth/relevance_judgments.json",
) -> tuple[List[Dict[str, Any]], Dict[str, List[str]]]:
    queries = DEFAULT_TEST_QUERIES
    truth = DEFAULT_GROUND_TRUTH
    if os.path.exists(queries_path):
        try:
            with open(queries_path, "r", encoding="utf-8") as f:
                queries = json.load(f)
        except Exception:
            pass
    if os.path.exists(rel_path):
        try:
            with open(rel_path, "r", encoding="utf-8") as f:
                truth = json.load(f)
        except Exception:
            pass
    return queries, truth

def create_app(
    db_conn: Optional[Any] = None,
    bm25_engine: Optional[Any] = None,
    sbert_engine: Optional[Any] = None,
    preprocessor: Optional[Any] = None,
    evaluator: Optional[Any] = None,
    db_path: str = "data/gadget.db",
    processed_dir: str = "data/processed",
) -> FastAPI:
    app = FastAPI(title="Indonesian Gadget Vertical Search Engine API")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 1. Initialize or connect SQLite
    if db_conn is None:
        if not os.path.exists(db_path) or not os.path.exists(os.path.join(processed_dir, "inverted_index.json")):
            try:
                build_index(db_path, processed_dir)
            except Exception as e:
                print(f"[API Startup] Indexer notice: {e}")
        db_conn = init_db(db_path)

    # 2. Initialize Preprocessor
    if preprocessor is None:
        try:
            preprocessor = IndonesianPreprocessor()
        except Exception:
            preprocessor = None

    # 3. Initialize BM25 Engine
    if bm25_engine is None:
        bm25_file = os.path.join(processed_dir, "inverted_index.json")
        if os.path.exists(bm25_file):
            try:
                bm25_engine = BM25Engine()
                bm25_engine.load(bm25_file)
            except Exception as e:
                print(f"[API Startup] Could not load BM25 index: {e}")

    # 4. Initialize S-BERT Engine
    if sbert_engine is None:
        npy_file = os.path.join(processed_dir, "embeddings.npy")
        if os.path.exists(npy_file):
            try:
                sbert_engine = SBERTEngine(cache_dir="models/cache")
                sbert_engine.load(processed_dir)
            except Exception as e:
                print(f"[API Startup] Could not load S-BERT embeddings: {e}")

    # 5. Initialize Evaluator
    if evaluator is None:
        evaluator = IREvaluator()

    app.state.bm25_engine = bm25_engine
    app.state.sbert_engine = sbert_engine
    app.state.preprocessor = preprocessor
    app.state.evaluator = evaluator

    app.state.docs: Dict[str, Dict[str, Any]] = {}
    if db_conn is not None:
        for doc in get_all_documents(db_conn):
            app.state.docs[doc["id"]] = doc

    @app.get("/api/health")
    def health() -> Dict[str, Any]:
        return {"status": "ok", "docs_count": len(app.state.docs)}

    @app.get("/api/search")
    def search(
        q: str = Query(default=""),
        algo: str = Query(default="both"),
        top_k: int = Query(default=10, ge=1),
    ) -> Dict[str, Any]:
        bm25_eng = app.state.bm25_engine
        sbert_eng = app.state.sbert_engine
        prep = app.state.preprocessor

        response: Dict[str, Any] = {}
        query = (q or "").strip()

        if algo not in ("bm25", "sbert", "both"):
            algo = "both"

        if not query:
            if algo in ("bm25", "both"):
                response["bm25"] = _empty_result()
            if algo in ("sbert", "both"):
                response["sbert"] = _empty_result()
            return response

        if algo in ("bm25", "both"):
            if bm25_eng is not None:
                start = time.perf_counter()
                ranked = bm25_eng.search(_query_tokens(query, prep), top_k=top_k)
                latency_ms = (time.perf_counter() - start) * 1000.0
                response["bm25"] = {
                    "results": _build_result_items(app.state.docs, ranked, top_k),
                    "latency_ms": round(latency_ms, 4),
                }
            else:
                response["bm25"] = _empty_result()

        if algo in ("sbert", "both"):
            if sbert_eng is not None:
                start = time.perf_counter()
                ranked = sbert_eng.search(query, top_k=top_k)
                latency_ms = (time.perf_counter() - start) * 1000.0
                response["sbert"] = {
                    "results": _build_result_items(app.state.docs, ranked, top_k),
                    "latency_ms": round(latency_ms, 4),
                }
            else:
                response["sbert"] = _empty_result()

        return response

    @app.get("/api/documents/{doc_id}")
    def document_detail(doc_id: str) -> Dict[str, Any]:
        doc = app.state.docs.get(doc_id)
        if doc is None:
            raise HTTPException(status_code=404, detail="Document not found")
        return doc

    @app.get("/api/evaluation")
    def evaluation() -> Dict[str, Any]:
        test_queries, ground_truth = load_ground_truth_from_disk()

        def empty_metrics() -> Dict[str, Any]:
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
            def bm25_search_fn(query_text: str) -> List[str]:
                if app.state.bm25_engine is None:
                    return []
                ranked = app.state.bm25_engine.search(
                    _query_tokens(query_text, app.state.preprocessor), top_k=10
                )
                return [doc_id for doc_id, _ in ranked]

            def sbert_search_fn(query_text: str) -> List[str]:
                if app.state.sbert_engine is None:
                    return []
                ranked = app.state.sbert_engine.search(query_text, top_k=10)
                return [doc_id for doc_id, _ in ranked]

            bm25_metrics = app.state.evaluator.evaluate_system(
                bm25_search_fn, test_queries, ground_truth
            )
            sbert_metrics = app.state.evaluator.evaluate_system(
                sbert_search_fn, test_queries, ground_truth
            )

        return {
            "bm25": bm25_metrics,
            "sbert": sbert_metrics,
            "test_queries_count": len(test_queries),
        }

    return app

# Module-level app instance for Uvicorn / Docker entrypoint:
app = create_app()
