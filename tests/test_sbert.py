import json
import math
import os
import tempfile

import numpy as np
import pytest

from backend.app.engine.sbert import SBERTEngine


class MockModel:
    """Deterministic mock encoder: returns fixed, dimension-consistent vectors."""

    def __init__(self, dim: int = 8) -> None:
        self.dim = dim
        self.encoded: list[str] = []

    def encode(self, texts: list[str]) -> np.ndarray:
        self.encoded.extend(texts)
        vectors = []
        for text in texts:
            rng = np.random.RandomState(hash(text) % (2**31))
            vec = rng.randn(self.dim).astype(np.float32)
            norm = np.linalg.norm(vec)
            vectors.append(vec / norm if norm > 0 else vec)
        return np.stack(vectors)


@pytest.fixture
def mock_model() -> MockModel:
    return MockModel(dim=8)


@pytest.fixture
def corpus() -> list[dict]:
    return [
        {"id": "doc1", "text": "xiaomi 13t smartphone"},
        {"id": "doc2", "text": "samsung galaxy s24"},
        {"id": "doc3", "text": "iphone 15 pro max"},
    ]


@pytest.fixture
def engine(mock_model: MockModel, corpus: list[dict]) -> SBERTEngine:
    eng = SBERTEngine(model_instance=mock_model)
    eng.fit(corpus)
    return eng


class TestConstructor:
    def test_default_parameters(self) -> None:
        eng = SBERTEngine()
        assert eng.model_name == "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
        assert eng.cache_dir == "models/cache"
        assert eng.model is None
        assert eng.doc_ids == []
        assert eng.embeddings is None

    def test_custom_parameters(self) -> None:
        eng = SBERTEngine(model_name="custom/model", cache_dir="custom/cache")
        assert eng.model_name == "custom/model"
        assert eng.cache_dir == "custom/cache"

    def test_injected_model_stored(self, mock_model: MockModel) -> None:
        eng = SBERTEngine(model_instance=mock_model)
        assert eng.model is mock_model


class TestEncode:
    def test_returns_float32_array(self, engine: SBERTEngine) -> None:
        vec = engine.encode(["hello"])
        assert isinstance(vec, np.ndarray)
        assert vec.dtype == np.float32

    def test_l2_normalized(self, engine: SBERTEngine) -> None:
        vec = engine.encode(["hello world"])
        norms = np.linalg.norm(vec, axis=1)
        assert np.allclose(norms, 1.0, atol=1e-6)

    def test_empty_input(self, engine: SBERTEngine) -> None:
        vec = engine.encode([])
        assert vec.shape[0] == 0


class TestFit:
    def test_stores_doc_ids_and_embeddings(self, engine: SBERTEngine, corpus: list[dict]) -> None:
        assert engine.doc_ids == ["doc1", "doc2", "doc3"]
        assert engine.embeddings.shape == (3, 8)
        assert engine.embeddings.dtype == np.float32

    def test_embeddings_are_l2_normalized(self, engine: SBERTEngine) -> None:
        norms = np.linalg.norm(engine.embeddings, axis=1)
        assert np.allclose(norms, 1.0, atol=1e-6)

    def test_handles_title_and_content(self, mock_model: MockModel) -> None:
        eng = SBERTEngine(model_instance=mock_model)
        eng.fit([{"id": "a", "title": "foo", "content": "bar"}])
        assert eng.doc_ids == ["a"]
        assert mock_model.encoded == ["foo bar"]

    def test_fit_empty_corpus(self, mock_model: MockModel) -> None:
        eng = SBERTEngine(model_instance=mock_model)
        eng.fit([])
        assert eng.doc_ids == []
        assert eng.embeddings.shape[0] == 0


class TestSearch:
    def test_returns_top_k_ranked_results(
        self, engine: SBERTEngine
    ) -> None:
        results = engine.search("xiaomi smartphone", top_k=2)
        assert isinstance(results, list)
        assert len(results) == 2
        assert all(isinstance(doc_id, str) and isinstance(score, float) for doc_id, score in results)
        scores = [score for _, score in results]
        assert scores == sorted(scores, reverse=True)

    def test_returns_all_when_top_k_exceeds_corpus(self, engine: SBERTEngine) -> None:
        results = engine.search("smartphone", top_k=100)
        assert len(results) == 3

    def test_best_match_is_exact_query_vector(self, mock_model: MockModel) -> None:
        eng = SBERTEngine(model_instance=mock_model)
        eng.fit([{"id": "d1", "text": "apple"}, {"id": "d2", "text": "banana"}])
        results = eng.search("apple", top_k=1)
        assert results[0][0] == "d1"

    def test_empty_corpus_returns_empty(self, mock_model: MockModel) -> None:
        eng = SBERTEngine(model_instance=mock_model)
        eng.fit([])
        assert eng.search("anything", top_k=10) == []

    def test_empty_query_returns_empty(self, engine: SBERTEngine) -> None:
        assert engine.search("", top_k=10) == []

    def test_zero_results_when_no_embeddings(self, mock_model: MockModel) -> None:
        eng = SBERTEngine(model_instance=mock_model)
        assert eng.search("x", top_k=10) == []


class TestSaveLoad:
    def test_save_and_load_roundtrip(self, engine: SBERTEngine) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            engine.save(tmpdir)
            assert os.path.isfile(os.path.join(tmpdir, "embeddings.npy"))
            assert os.path.isfile(os.path.join(tmpdir, "doc_ids.json"))

            loaded = SBERTEngine()
            loaded.model = engine.model
            loaded.load(tmpdir)

            assert loaded.doc_ids == engine.doc_ids
            assert loaded.embeddings.shape == engine.embeddings.shape
            assert np.allclose(loaded.embeddings, engine.embeddings)
            assert loaded.search("xiaomi", top_k=10) == engine.search("xiaomi", top_k=10)

    def test_load_reads_json_and_npy(self, engine: SBERTEngine) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            engine.save(tmpdir)
            with open(os.path.join(tmpdir, "doc_ids.json")) as fh:
                saved_ids = json.load(fh)
            assert saved_ids == engine.doc_ids
