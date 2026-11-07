import math
import os
import tempfile

import pytest

from backend.app.engine.bm25 import BM25Engine


@pytest.fixture
def corpus() -> list[dict]:
    return [
        {"id": "doc1", "tokens": ["cat", "cat", "dog"]},
        {"id": "doc2", "tokens": ["cat"]},
        {"id": "doc3", "tokens": ["dog", "mouse"]},
    ]


@pytest.fixture
def engine(corpus: list[dict]) -> BM25Engine:
    eng = BM25Engine(k1=1.5, b=0.75)
    eng.fit(corpus)
    return eng


def expected_idf(n_docs: int, n_q: int) -> float:
    """Robertson-Sparck Jones IDF with the +1 floor (independent of the impl)."""
    return math.log((n_docs - n_q + 0.5) / (n_q + 0.5) + 1)


def expected_bm25(f: int, dl: int, avgdl: float, idfv: float, k1: float = 1.5, b: float = 0.75) -> float:
    """Independent Okapi BM25 term score per the spec formula."""
    return idfv * (f * (k1 + 1)) / (f + k1 * (1 - b + b * (dl / avgdl)))


class TestConstructor:
    def test_default_parameters(self) -> None:
        eng = BM25Engine()
        assert eng.k1 == 1.5
        assert eng.b == 0.75
        assert eng.inverted_index == {}
        assert eng.doc_lengths == {}
        assert eng.avgdl == 0.0
        assert eng.n_docs == 0
        assert eng.idf == {}

    def test_custom_parameters(self) -> None:
        eng = BM25Engine(k1=2.0, b=0.5)
        assert eng.k1 == 2.0
        assert eng.b == 0.5


class TestFit:
    def test_builds_inverted_index(self, engine: BM25Engine) -> None:
        assert engine.inverted_index == {
            "cat": {"doc1": 2, "doc2": 1},
            "dog": {"doc1": 1, "doc3": 1},
            "mouse": {"doc3": 1},
        }

    def test_computes_doc_lengths(self, engine: BM25Engine) -> None:
        assert engine.doc_lengths == {"doc1": 3, "doc2": 1, "doc3": 2}

    def test_computes_avgdl(self, engine: BM25Engine) -> None:
        assert engine.avgdl == pytest.approx(2.0)

    def test_computes_n_docs(self, engine: BM25Engine) -> None:
        assert engine.n_docs == 3

    def test_computes_idf(self, engine: BM25Engine) -> None:
        n_docs = 3
        expected = {
            "cat": expected_idf(n_docs, 2),
            "dog": expected_idf(n_docs, 2),
            "mouse": expected_idf(n_docs, 1),
        }
        for term, value in expected.items():
            assert engine.idf[term] == pytest.approx(value, rel=1e-9)

    def test_idf_is_non_negative(self, engine: BM25Engine) -> None:
        for value in engine.idf.values():
            assert value >= 0.0

    def test_fit_empty_corpus(self) -> None:
        eng = BM25Engine()
        eng.fit([])
        assert eng.inverted_index == {}
        assert eng.doc_lengths == {}
        assert eng.avgdl == 0.0
        assert eng.n_docs == 0
        assert eng.idf == {}


class TestSearch:
    def test_ranks_documents_by_bm25_score(self, engine: BM25Engine) -> None:
        results = engine.search(["cat"], top_k=10)
        assert results == [
            ("doc2", pytest.approx(0.6064562958009492, rel=1e-6)),
            ("doc1", pytest.approx(0.5784660052255207, rel=1e-6)),
        ]

    def test_doc_without_query_term_scores_zero(self, engine: BM25Engine) -> None:
        # doc3 does not contain "cat", so it must not appear in results.
        results = engine.search(["cat"], top_k=10)
        doc_ids = [doc_id for doc_id, _ in results]
        assert "doc3" not in doc_ids

    def test_oov_tokens_score_zero(self, engine: BM25Engine) -> None:
        assert engine.search(["nonexistent"], top_k=10) == []

    def test_multi_term_query(self, engine: BM25Engine) -> None:
        results = engine.search(["dog", "mouse"], top_k=10)
        assert results[0][0] == "doc3"
        assert results[0][1] == pytest.approx(
            expected_bm25(1, 2, 2.0, expected_idf(3, 1)) + expected_bm25(1, 2, 2.0, expected_idf(3, 2)),
            rel=1e-6,
        )
        assert results[1][0] == "doc1"
        assert results[1][1] == pytest.approx(expected_bm25(1, 3, 2.0, expected_idf(3, 2)), rel=1e-6)

    def test_top_k_limits_results(self, engine: BM25Engine) -> None:
        results = engine.search(["cat", "dog", "mouse"], top_k=1)
        assert len(results) == 1

    def test_returns_list_of_str_float_tuples(self, engine: BM25Engine) -> None:
        results = engine.search(["cat", "dog"], top_k=10)
        assert all(isinstance(doc_id, str) and isinstance(score, float) for doc_id, score in results)

    def test_empty_query_returns_empty(self, engine: BM25Engine) -> None:
        assert engine.search([], top_k=10) == []

    def test_scores_are_descending(self, engine: BM25Engine) -> None:
        results = engine.search(["cat", "dog", "mouse"], top_k=10)
        scores = [score for _, score in results]
        assert scores == sorted(scores, reverse=True)


class TestSaveLoad:
    def test_save_and_load_roundtrip(self, engine: BM25Engine) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "bm25_index.json")
            engine.save(path)

            loaded = BM25Engine(k1=2.0, b=0.5)
            loaded.load(path)

            assert loaded.k1 == 1.5
            assert loaded.b == 0.75
            assert loaded.inverted_index == engine.inverted_index
            assert loaded.doc_lengths == engine.doc_lengths
            assert loaded.avgdl == engine.avgdl
            assert loaded.n_docs == engine.n_docs
            assert loaded.idf == engine.idf
            assert loaded.search(["cat"], top_k=10) == engine.search(["cat"], top_k=10)

    def test_save_creates_json_file(self, engine: BM25Engine) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "index.json")
            engine.save(path)
            assert os.path.isfile(path)
