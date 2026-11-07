import time
from typing import Callable, Dict, List, Set, Tuple


class IREvaluator:
    """Information Retrieval evaluation engine conforming to trec_eval metrics.

    Computes Precision@K, Recall@K, F1@K, Average Precision (AP), and Mean
    Average Precision (MAP), plus latency benchmarking for end-to-end system
    evaluation.

    All metrics follow the standard definitions:

        P@k = |Retrieved[:k] n Relevant| / k
        R@k = |Retrieved[:k] n Relevant| / |Relevant|
        F1@k = 2 * P@k * R@k / (P@k + R@k)
        AP  = sum_{i=1}^{N} (P@i * rel(i)) / |Relevant|
        MAP = mean of AP over all queries

    where rel(i) = 1 if the i-th retrieved document is relevant, else 0.
    """

    def precision_at_k(
        self, retrieved_ids: List[str], relevant_ids: Set[str], k: int
    ) -> float:
        """Precision at rank k.

        Returns 0.0 if k <= 0.
        """
        if k <= 0:
            return 0.0
        retrieved_at_k = retrieved_ids[:k]
        relevant_retrieved = len(
            set(retrieved_at_k) & relevant_ids
        )
        return relevant_retrieved / k

    def recall_at_k(
        self, retrieved_ids: List[str], relevant_ids: Set[str], k: int
    ) -> float:
        """Recall at rank k.

        Returns 0.0 if |Relevant| = 0 or k <= 0.
        """
        if k <= 0 or not relevant_ids:
            return 0.0
        retrieved_at_k = retrieved_ids[:k]
        relevant_retrieved = len(
            set(retrieved_at_k) & relevant_ids
        )
        return relevant_retrieved / len(relevant_ids)

    def f1_at_k(
        self, retrieved_ids: List[str], relevant_ids: Set[str], k: int
    ) -> float:
        """F1 score at rank k (harmonic mean of P@k and R@k).

        Returns 0.0 if P@k + R@k = 0.
        """
        precision = self.precision_at_k(retrieved_ids, relevant_ids, k)
        recall = self.recall_at_k(retrieved_ids, relevant_ids, k)
        denominator = precision + recall
        if denominator == 0.0:
            return 0.0
        return 2 * precision * recall / denominator

    def average_precision(
        self, retrieved_ids: List[str], relevant_ids: Set[str]
    ) -> float:
        """Average Precision over the full retrieved ranking.

        Returns 0.0 if |Relevant| = 0 or no relevant documents are retrieved.
        """
        if not relevant_ids:
            return 0.0

        precision_sum = 0.0
        relevant_retrieved = 0
        for i, doc_id in enumerate(retrieved_ids, start=1):
            if doc_id in relevant_ids:
                relevant_retrieved += 1
                precision_at_i = relevant_retrieved / i
                precision_sum += precision_at_i

        if relevant_retrieved == 0:
            return 0.0
        return precision_sum / len(relevant_ids)

    def evaluate_query(
        self,
        retrieved_ids: List[str],
        relevant_ids: Set[str],
        k_values: List[int] = [5, 10],
    ) -> Dict[str, float]:
        """Compute per-query metrics for the given k values.

        Returns a dict with keys ``p@{k}``, ``r@{k}``, ``f1@{k}`` for each
        ``k`` in ``k_values`` plus ``ap``. With the default ``k_values=[5, 10]``
        the keys are ``p@5``, ``p@10``, ``r@5``, ``r@10``, ``f1@5``, ``f1@10``,
        ``ap``.
        """
        results: Dict[str, float] = {}
        for k in k_values:
            results[f"p@{k}"] = self.precision_at_k(retrieved_ids, relevant_ids, k)
            results[f"r@{k}"] = self.recall_at_k(retrieved_ids, relevant_ids, k)
            results[f"f1@{k}"] = self.f1_at_k(retrieved_ids, relevant_ids, k)
        results["ap"] = self.average_precision(retrieved_ids, relevant_ids)
        return results

    def evaluate_system(
        self,
        search_fn: Callable[[str], List[str] | List[Tuple[str, float]]],
        test_queries: List[Dict],
        ground_truth: Dict[str, Set[str] | List[str]],
    ) -> Dict:
        """Evaluate a search function over a set of test queries.

        For each test query (dict with ``id`` and ``query`` keys), runs
        ``search_fn(query_text)``, measures latency in milliseconds via
        ``time.perf_counter()``, computes per-query metrics, and returns
        macro-averaged aggregates:

        - ``mean_p5``, ``mean_p10``, ``mean_r5``, ``mean_r10``,
          ``mean_f1_5``, ``mean_f1_10``
        - ``map``: mean of per-query Average Precision
        - ``avg_latency_ms``
        - ``per_query_results``: list of per-query metric dicts
        """
        per_query_results: List[Dict] = []
        latencies: List[float] = []

        for query in test_queries:
            query_id = query.get("id", query.get("query_id", ""))
            query_text = query.get("query", query.get("text", query.get("q", "")))

            relevant = ground_truth.get(query_id, set())
            if isinstance(relevant, list):
                relevant = set(relevant)

            start = time.perf_counter()
            retrieved = search_fn(query_text) or []
            end = time.perf_counter()
            latency_ms = (end - start) * 1000.0
            latencies.append(latency_ms)

            retrieved_ids: List[str] = [
                item[0] if isinstance(item, tuple) else item for item in retrieved
            ]

            metrics = self.evaluate_query(retrieved_ids, relevant)
            per_query_results.append(
                {"query_id": query_id, "latency_ms": latency_ms, **metrics}
            )

        n_queries = len(test_queries)
        if n_queries == 0:
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

        mean_p5 = sum(item["p@5"] for item in per_query_results) / n_queries
        mean_p10 = sum(item["p@10"] for item in per_query_results) / n_queries
        mean_r5 = sum(item["r@5"] for item in per_query_results) / n_queries
        mean_r10 = sum(item["r@10"] for item in per_query_results) / n_queries
        mean_f1_5 = sum(item["f1@5"] for item in per_query_results) / n_queries
        mean_f1_10 = sum(item["f1@10"] for item in per_query_results) / n_queries
        map_value = sum(item["ap"] for item in per_query_results) / n_queries
        avg_latency_ms = sum(latencies) / n_queries

        return {
            "mean_p5": mean_p5,
            "mean_p10": mean_p10,
            "mean_r5": mean_r5,
            "mean_r10": mean_r10,
            "mean_f1_5": mean_f1_5,
            "mean_f1_10": mean_f1_10,
            "map": map_value,
            "avg_latency_ms": avg_latency_ms,
            "per_query_results": per_query_results,
        }
