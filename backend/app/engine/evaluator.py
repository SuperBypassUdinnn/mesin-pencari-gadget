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

if __name__ == "__main__":
    import csv
    import json
    import os
    from backend.app.engine.preprocessor import IndonesianPreprocessor
    from backend.app.engine.bm25 import BM25Engine
    from backend.app.engine.sbert import SBERTEngine

    out_dir = "evaluation_results"
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(os.path.join(out_dir, "charts"), exist_ok=True)

    queries_path = "data/ground_truth/test_queries.json"
    judgments_path = "data/ground_truth/relevance_judgments.json"

    with open(queries_path, "r", encoding="utf-8") as f:
        test_queries = json.load(f)
    with open(judgments_path, "r", encoding="utf-8") as f:
        ground_truth = json.load(f)

    preprocessor = IndonesianPreprocessor()
    bm25 = BM25Engine()
    bm25.load("data/processed/inverted_index.json")

    sbert = SBERTEngine(cache_dir="models/cache")
    sbert.load("data/processed")

    evaluator = IREvaluator()

    def bm25_search(q: str):
        tokens = preprocessor.preprocess(q)
        return [doc_id for doc_id, _ in bm25.search(tokens, top_k=10)]

    def sbert_search(q: str):
        return [doc_id for doc_id, _ in sbert.search(q, top_k=10)]

    print(f"[Benchmark] Evaluating Okapi BM25 and Sentence-BERT on {len(test_queries)} queries...")
    res_bm25 = evaluator.evaluate_system(bm25_search, test_queries, ground_truth)
    res_sbert = evaluator.evaluate_system(sbert_search, test_queries, ground_truth)

    summary = {
        "bm25": res_bm25,
        "sbert": res_sbert,
        "queries_count": len(test_queries)
    }

    with open(os.path.join(out_dir, "metrics_summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    csv_path = os.path.join(out_dir, "per_query_benchmark.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["query_id", "query", "algo", "p@5", "p@10", "r@5", "r@10", "f1@5", "f1@10", "ap", "latency_ms"])
        q_map = {q["id"]: q["query"] for q in test_queries}
        for q_res in res_bm25["per_query_results"]:
            qid = q_res["query_id"]
            writer.writerow([qid, q_map.get(qid, ""), "bm25", q_res["p@5"], q_res["p@10"], q_res["r@5"], q_res["r@10"], q_res["f1@5"], q_res["f1@10"], q_res["ap"], q_res["latency_ms"]])
        for q_res in res_sbert["per_query_results"]:
            qid = q_res["query_id"]
            writer.writerow([qid, q_map.get(qid, ""), "sbert", q_res["p@5"], q_res["p@10"], q_res["r@5"], q_res["r@10"], q_res["f1@5"], q_res["f1@10"], q_res["ap"], q_res["latency_ms"]])

    print("=" * 60)
    print("IR EVALUATION BENCHMARK SUMMARY (12 QUERIES)")
    print("=" * 60)
    print(f"{'Metric':<18} | {'Okapi BM25':<15} | {'Sentence-BERT':<15}")
    print("-" * 60)
    print(f"{'Mean P@5':<18} | {res_bm25['mean_p5']:<15.4f} | {res_sbert['mean_p5']:<15.4f}")
    print(f"{'Mean P@10':<18} | {res_bm25['mean_p10']:<15.4f} | {res_sbert['mean_p10']:<15.4f}")
    print(f"{'Mean R@5':<18} | {res_bm25['mean_r5']:<15.4f} | {res_sbert['mean_r5']:<15.4f}")
    print(f"{'Mean R@10':<18} | {res_bm25['mean_r10']:<15.4f} | {res_sbert['mean_r10']:<15.4f}")
    print(f"{'Mean F1@5':<18} | {res_bm25['mean_f1_5']:<15.4f} | {res_sbert['mean_f1_5']:<15.4f}")
    print(f"{'MAP':<18} | {res_bm25['map']:<15.4f} | {res_sbert['map']:<15.4f}")
    print(f"{'Avg Latency (ms)':<18} | {res_bm25['avg_latency_ms']:<15.4f} | {res_sbert['avg_latency_ms']:<15.4f}")
    print("=" * 60)
    print(f"[Benchmark] Outputs written to {out_dir}/metrics_summary.json and {csv_path}")

