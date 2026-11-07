import json
import math
import os
from typing import Dict, List, Tuple


class BM25Engine:
    """Inverted index with Robertson-Sparck Jones Okapi BM25 ranking.

    Builds a term -> {doc_id: term_frequency} inverted index over a tokenized
    corpus, computes document lengths, average document length, and IDF values,
    then ranks documents for a query using the Okapi BM25 formula:

        Score(D, Q) = sum_{q in Q} IDF(q) *
            (f(q, D) * (k1 + 1)) /
            (f(q, D) + k1 * (1 - b + b * (|D| / avgdl)))

    IDF(q) = ln((N - n(q) + 0.5) / (n(q) + 0.5) + 1)

    The ``+1`` floor guarantees non-negative IDF scores. Unknown/OOV query
    tokens contribute a score of 0 and are skipped gracefully.
    """

    def __init__(self, k1: float = 1.5, b: float = 0.75) -> None:
        self.k1: float = k1
        self.b: float = b
        self.inverted_index: Dict[str, Dict[str, int]] = {}
        self.doc_lengths: Dict[str, int] = {}
        self.avgdl: float = 0.0
        self.n_docs: int = 0
        self.idf: Dict[str, float] = {}

    def fit(self, corpus: List[Dict]) -> None:
        """Build the inverted index and IDF table from a tokenized corpus.

        Each item in ``corpus`` must be ``{"id": str, "tokens": list[str]}``.
        """
        self.inverted_index = {}
        self.doc_lengths = {}
        self.n_docs = len(corpus)

        total_length = 0
        for doc in corpus:
            doc_id = doc["id"]
            tokens = doc["tokens"]
            length = len(tokens)
            self.doc_lengths[doc_id] = length
            total_length += length

            term_freqs: Dict[str, int] = {}
            for token in tokens:
                term_freqs[token] = term_freqs.get(token, 0) + 1
            for term, freq in term_freqs.items():
                self.inverted_index.setdefault(term, {})[doc_id] = freq

        self.avgdl = total_length / self.n_docs if self.n_docs > 0 else 0.0
        self._compute_idf()

    def _compute_idf(self) -> None:
        """Compute IDF for every term in the inverted index."""
        self.idf = {}
        for term, doc_freqs in self.inverted_index.items():
            n_q = len(doc_freqs)
            self.idf[term] = math.log(
                (self.n_docs - n_q + 0.5) / (n_q + 0.5) + 1.0
            )

    def _term_score(self, term: str, freq: int, doc_len: int) -> float:
        """Okapi BM25 contribution of a single term in a single document."""
        idf = self.idf.get(term, 0.0)
        if idf == 0.0:
            return 0.0
        if self.avgdl == 0.0:
            return 0.0
        length_norm = 1.0 - self.b + self.b * (doc_len / self.avgdl)
        return idf * (freq * (self.k1 + 1)) / (freq + self.k1 * length_norm)

    def search(
        self, query_tokens: List[str], top_k: int = 10
    ) -> List[Tuple[str, float]]:
        """Rank documents for a query and return the top-K results.

        Returns ``[(doc_id, score), ...]`` sorted descending by score.
        Unknown/OOV tokens contribute 0 and are skipped.
        """
        if not query_tokens or self.n_docs == 0:
            return []

        scores: Dict[str, float] = {}
        for token in query_tokens:
            if token not in self.inverted_index:
                continue
            for doc_id, freq in self.inverted_index[token].items():
                scores[doc_id] = scores.get(doc_id, 0.0) + self._term_score(
                    token, freq, self.doc_lengths[doc_id]
                )

        ranked = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        return [(doc_id, score) for doc_id, score in ranked[:top_k]]

    def save(self, path: str) -> None:
        """Serialize the index, document lengths, avgdl, and params to JSON."""
        payload = {
            "k1": self.k1,
            "b": self.b,
            "n_docs": self.n_docs,
            "avgdl": self.avgdl,
            "inverted_index": self.inverted_index,
            "doc_lengths": self.doc_lengths,
        }
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False)

    def load(self, path: str) -> None:
        """Deserialize a previously saved JSON index."""
        with open(path, "r", encoding="utf-8") as handle:
            payload = json.load(handle)

        self.k1 = float(payload.get("k1", 1.5))
        self.b = float(payload.get("b", 0.75))
        self.n_docs = int(payload.get("n_docs", 0))
        self.avgdl = float(payload.get("avgdl", 0.0))
        self.inverted_index = {
            term: {doc_id: int(freq) for doc_id, freq in doc_freqs.items()}
            for term, doc_freqs in payload.get("inverted_index", {}).items()
        }
        self.doc_lengths = {
            doc_id: int(length) for doc_id, length in payload.get("doc_lengths", {}).items()
        }
        self._compute_idf()
