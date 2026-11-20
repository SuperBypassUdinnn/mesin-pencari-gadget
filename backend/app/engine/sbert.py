import json
import os
from typing import List, Tuple

import numpy as np


class SBERTEngine:
    """Dense semantic vector search engine using Sentence-BERT embeddings.

    Encodes documents and queries into L2-normalized dense vectors and ranks
    documents by cosine similarity (computed as a single NumPy dot product
    between the normalized query vector and the normalized embedding matrix).

    The ``model_instance`` constructor parameter allows dependency injection of
    a deterministic mock encoder so unit tests run completely offline without
    downloading heavy models.
    """

    def __init__(
        self,
        model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        cache_dir: str = "models/cache",
        model_instance=None,
    ) -> None:
        self.model_name: str = model_name
        self.cache_dir: str = cache_dir
        self.model = model_instance
        self.doc_ids: List[str] = []
        self.embeddings: np.ndarray | None = None

    def _extract_text(self, item: dict) -> str:
        """Extract searchable text from a corpus item.

        Prefers the ``text`` field; otherwise concatenates ``title`` and
        ``content``.
        """
        if "text" in item and item["text"]:
            return str(item["text"])
        title = str(item.get("title", ""))
        content = str(item.get("content", ""))
        return (title + " " + content).strip()

    def _ensure_model(self):
        """Load the SentenceTransformer model on first use.

        Fails loudly when the model cannot be loaded. A silent degraded mode
        would produce meaningless embeddings and silently corrupt benchmark
        artifacts (observed: ``make eval`` writing random S-BERT metrics when
        ``sentence-transformers`` was missing), so any load failure raises.
        Unit tests must inject a deterministic encoder via ``model_instance``.
        """
        if self.model is not None:
            return
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:
            raise RuntimeError(
                "sentence-transformers is not installed. "
                "Install backend requirements (pip install -r backend/requirements.txt) "
                "or inject a deterministic encoder via SBERTEngine(model_instance=...) in tests."
            ) from exc
        try:
            os.makedirs(self.cache_dir, exist_ok=True)
            self.model = SentenceTransformer(self.model_name, cache_folder=self.cache_dir)
        except Exception as exc:
            raise RuntimeError(
                f"Failed to load Sentence-BERT model '{self.model_name}' "
                f"(cache: {self.cache_dir}). Check network access to Hugging Face "
                "or provide a pre-populated model cache."
            ) from exc

    def encode(self, texts: List[str]) -> np.ndarray:
        """Encode a list of strings into an L2-normalized float32 matrix.

        Each row is a unit vector computed as::

            norm = np.linalg.norm(vec, axis=1, keepdims=True)
            vec / np.maximum(norm, 1e-9)
        """
        if not texts:
            return np.empty((0, 0), dtype=np.float32)

        if self.model is None:
            self._ensure_model()

        vecs = np.asarray(self.model.encode(texts), dtype=np.float32)
        norms = np.linalg.norm(vecs, axis=1, keepdims=True)
        return vecs / np.maximum(norms, 1e-9)

    def fit(self, corpus: List[dict]) -> None:
        """Encode the corpus and store document IDs and the embedding matrix.

        Each item in ``corpus`` is ``{"id": str, "text": str}`` or
        ``{"id": str, "title": str, "content": str}``.
        """
        self.doc_ids = [str(item["id"]) for item in corpus]
        texts = [self._extract_text(item) for item in corpus]
        self.embeddings = self.encode(texts)

    def search(self, query: str, top_k: int = 10) -> List[Tuple[str, float]]:
        """Rank documents by cosine similarity to the query.

        Returns the top-K results as ``[(doc_id, float(score)), ...]`` sorted
        descending by score. Returns an empty list for an empty corpus, an
        empty query, or when no embeddings are available.
        """
        if not query or self.embeddings is None or self.embeddings.shape[0] == 0:
            return []

        query_vec = self.encode([query])[0]
        if query_vec.shape[0] != self.embeddings.shape[1]:
            raise RuntimeError(
                "Dimension mismatch between query embedding "
                f"({query_vec.shape[0]}d) and document embedding matrix "
                f"({self.embeddings.shape[1]}d). The stored embeddings were "
                "probably built with a different encoder; rebuild the index "
                "with 'make index'."
            )
        scores = np.dot(self.embeddings, query_vec)
        ranked = sorted(
            zip(self.doc_ids, scores.tolist()), key=lambda item: item[1], reverse=True
        )
        return [(doc_id, float(score)) for doc_id, score in ranked[:top_k]]

    def save(self, directory: str) -> None:
        """Serialize ``embeddings.npy`` and ``doc_ids.json`` into the directory."""
        os.makedirs(directory, exist_ok=True)
        np.save(os.path.join(directory, "embeddings.npy"), self.embeddings)
        with open(os.path.join(directory, "doc_ids.json"), "w", encoding="utf-8") as fh:
            json.dump(self.doc_ids, fh, ensure_ascii=False)

    def load(self, directory: str) -> None:
        """Deserialize ``embeddings.npy`` and ``doc_ids.json`` from the directory."""
        self.embeddings = np.load(os.path.join(directory, "embeddings.npy")).astype(
            np.float32
        )
        with open(os.path.join(directory, "doc_ids.json"), "r", encoding="utf-8") as fh:
            self.doc_ids = [str(doc_id) for doc_id in json.load(fh)]
