import pytest

from backend.app.engine.evaluator import IREvaluator


@pytest.fixture
def evaluator() -> IREvaluator:
    return IREvaluator()


class TestPrecisionAtK:
    def test_precision_at_k_partial_overlap(self, evaluator: IREvaluator) -> None:
        retrieved = ["d1", "d2", "d3", "d4", "d5"]
        relevant = {"d1", "d3"}
        assert evaluator.precision_at_k(retrieved, relevant, 5) == pytest.approx(2 / 5)

    def test_precision_at_k_denominator_is_k(self, evaluator: IREvaluator) -> None:
        # Fewer documents retrieved than k: denominator stays k per spec.
        retrieved = ["d1", "d2"]
        relevant = {"d1", "d2", "d3"}
        assert evaluator.precision_at_k(retrieved, relevant, 5) == pytest.approx(2 / 5)

    def test_precision_at_k_all_relevant(self, evaluator: IREvaluator) -> None:
        retrieved = ["d1", "d2", "d3"]
        relevant = {"d1", "d2", "d3"}
        assert evaluator.precision_at_k(retrieved, relevant, 3) == pytest.approx(1.0)

    def test_precision_at_k_none_relevant(self, evaluator: IREvaluator) -> None:
        retrieved = ["d1", "d2", "d3"]
        relevant = {"d4", "d5"}
        assert evaluator.precision_at_k(retrieved, relevant, 3) == pytest.approx(0.0)

    def test_precision_at_k_empty_retrieved(self, evaluator: IREvaluator) -> None:
        assert evaluator.precision_at_k([], {"d1"}, 5) == pytest.approx(0.0)

    def test_precision_at_k_zero_k(self, evaluator: IREvaluator) -> None:
        assert evaluator.precision_at_k(["d1"], {"d1"}, 0) == pytest.approx(0.0)

    def test_precision_at_k_negative_k(self, evaluator: IREvaluator) -> None:
        assert evaluator.precision_at_k(["d1"], {"d1"}, -3) == pytest.approx(0.0)


class TestRecallAtK:
    def test_recall_at_k_partial_overlap(self, evaluator: IREvaluator) -> None:
        retrieved = ["d1", "d2", "d3", "d4", "d5"]
        relevant = {"d1", "d3", "d6"}
        assert evaluator.recall_at_k(retrieved, relevant, 5) == pytest.approx(2 / 3)

    def test_recall_at_k_all_relevant_retrieved(self, evaluator: IREvaluator) -> None:
        retrieved = ["d1", "d2", "d3"]
        relevant = {"d1", "d3"}
        assert evaluator.recall_at_k(retrieved, relevant, 3) == pytest.approx(1.0)

    def test_recall_at_k_empty_relevant(self, evaluator: IREvaluator) -> None:
        assert evaluator.recall_at_k(["d1", "d2"], set(), 5) == pytest.approx(0.0)

    def test_recall_at_k_empty_retrieved(self, evaluator: IREvaluator) -> None:
        assert evaluator.recall_at_k([], {"d1"}, 5) == pytest.approx(0.0)

    def test_recall_at_k_zero_k(self, evaluator: IREvaluator) -> None:
        assert evaluator.recall_at_k(["d1"], {"d1"}, 0) == pytest.approx(0.0)

    def test_recall_at_k_negative_k(self, evaluator: IREvaluator) -> None:
        assert evaluator.recall_at_k(["d1"], {"d1"}, -1) == pytest.approx(0.0)


class TestF1AtK:
    def test_f1_at_k_harmonic_mean(self, evaluator: IREvaluator) -> None:
        # P@5 = 2/5 = 0.4, R@5 = 2/2 = 1.0
        # F1 = 2 * 0.4 * 1.0 / (0.4 + 1.0) = 0.8 / 1.4
        retrieved = ["d1", "d2", "d3", "d4", "d5"]
        relevant = {"d1", "d2"}
        expected = 2 * (2 / 5) * 1.0 / ((2 / 5) + 1.0)
        assert evaluator.f1_at_k(retrieved, relevant, 5) == pytest.approx(expected)

    def test_f1_at_k_zero_when_precision_and_recall_zero(self, evaluator: IREvaluator) -> None:
        retrieved = ["d1", "d2"]
        relevant = {"d3", "d4"}
        assert evaluator.f1_at_k(retrieved, relevant, 2) == pytest.approx(0.0)

    def test_f1_at_k_zero_when_k_zero(self, evaluator: IREvaluator) -> None:
        assert evaluator.f1_at_k(["d1"], {"d1"}, 0) == pytest.approx(0.0)

    def test_f1_at_k_one_when_perfect(self, evaluator: IREvaluator) -> None:
        retrieved = ["d1", "d2"]
        relevant = {"d1", "d2"}
        assert evaluator.f1_at_k(retrieved, relevant, 2) == pytest.approx(1.0)


class TestAveragePrecision:
    def test_average_precision_standard(self, evaluator: IREvaluator) -> None:
        # retrieved: d1(rel), d2, d3(rel), d4, d5(rel); relevant = {d1, d3, d5}
        # P@1 = 1/1, P@3 = 2/3, P@5 = 3/5
        # AP = (1 + 2/3 + 3/5) / 3
        retrieved = ["d1", "d2", "d3", "d4", "d5"]
        relevant = {"d1", "d3", "d5"}
        expected = (1.0 + 2 / 3 + 3 / 5) / 3
        assert evaluator.average_precision(retrieved, relevant) == pytest.approx(expected)

    def test_average_precision_empty_relevant(self, evaluator: IREvaluator) -> None:
        assert evaluator.average_precision(["d1", "d2"], set()) == pytest.approx(0.0)

    def test_average_precision_no_relevant_retrieved(self, evaluator: IREvaluator) -> None:
        assert evaluator.average_precision(["d1", "d2"], {"d3", "d4"}) == pytest.approx(0.0)

    def test_average_precision_empty_retrieved(self, evaluator: IREvaluator) -> None:
        assert evaluator.average_precision([], {"d1"}) == pytest.approx(0.0)

    def test_average_precision_all_relevant_first(self, evaluator: IREvaluator) -> None:
        retrieved = ["d1", "d2", "d3"]
        relevant = {"d1", "d2", "d3"}
        # P@1=1, P@2=1, P@3=1 -> AP = 3/3 = 1
        assert evaluator.average_precision(retrieved, relevant) == pytest.approx(1.0)


class TestEvaluateQuery:
    def test_evaluate_query_default_keys(self, evaluator: IREvaluator) -> None:
        retrieved = ["d1", "d2", "d3", "d4", "d5"]
        relevant = {"d1", "d3"}
        result = evaluator.evaluate_query(retrieved, relevant)
        expected_keys = {"p@5", "p@10", "r@5", "r@10", "f1@5", "f1@10", "ap"}
        assert set(result.keys()) == expected_keys
        assert result["p@5"] == pytest.approx(2 / 5)
        assert result["p@10"] == pytest.approx(2 / 10)
        assert result["r@5"] == pytest.approx(1.0)
        assert result["r@10"] == pytest.approx(1.0)
        assert result["f1@5"] == pytest.approx(2 * (2 / 5) * 1.0 / ((2 / 5) + 1.0))
        # AP = (P@1 + P@3) / |Relevant| = (1 + 2/3) / 2 = 5/6
        assert result["ap"] == pytest.approx((1.0 + 2 / 3) / 2)

    def test_evaluate_query_custom_k_values(self, evaluator: IREvaluator) -> None:
        retrieved = ["d1", "d2", "d3"]
        relevant = {"d1"}
        result = evaluator.evaluate_query(retrieved, relevant, k_values=[1, 3])
        assert result["p@1"] == pytest.approx(1.0)
        assert result["p@3"] == pytest.approx(1 / 3)
        assert result["r@1"] == pytest.approx(1.0)
        assert result["r@3"] == pytest.approx(1.0)
        assert result["f1@1"] == pytest.approx(1.0)


class TestEvaluateSystem:
    def test_evaluate_system_macro_averages(self) -> None:
        evaluator = IREvaluator()

        def search_fn(query_text: str) -> list[str]:
            return {
                "cats": ["d1", "d2", "d3"],
                "dogs": ["d4", "d5"],
            }.get(query_text, [])

        test_queries = [
            {"id": "q1", "query": "cats"},
            {"id": "q2", "query": "dogs"},
        ]
        ground_truth = {
            "q1": {"d1", "d3", "d6"},
            "q2": {"d4"},
        }

        report = evaluator.evaluate_system(search_fn, test_queries, ground_truth)

        expected_keys = {
            "mean_p5", "mean_p10", "mean_r5", "mean_r10",
            "mean_f1_5", "mean_f1_10", "map", "avg_latency_ms", "per_query_results",
        }
        assert set(report.keys()) == expected_keys

        # q1: P@5 = 2/5, R@5 = 2/3, AP = (P@1 + P@3) / |Relevant| = (1 + 2/3) / 3 = 5/9
        # q2: P@5 = 1/5, R@5 = 1/1 = 1, AP = P@1 / |Relevant| = 1 / 1 = 1
        assert report["mean_p5"] == pytest.approx((2 / 5 + 1 / 5) / 2)
        assert report["mean_r5"] == pytest.approx((2 / 3 + 1.0) / 2)
        # MAP = (5/9 + 1) / 2 = 7/9
        assert report["map"] == pytest.approx((5 / 9 + 1.0) / 2)
        assert report["avg_latency_ms"] >= 0.0
        assert len(report["per_query_results"]) == 2

        per_query = {item["query_id"]: item for item in report["per_query_results"]}
        assert per_query["q1"]["p@5"] == pytest.approx(2 / 5)
        assert per_query["q1"]["ap"] == pytest.approx(5 / 9)
        assert per_query["q2"]["p@5"] == pytest.approx(1 / 5)
        assert per_query["q2"]["ap"] == pytest.approx(1.0)
        assert "latency_ms" in per_query["q1"]

    def test_evaluate_system_empty_test_queries(self) -> None:
        evaluator = IREvaluator()
        report = evaluator.evaluate_system(lambda q: [], [], {})
        assert report["mean_p5"] == pytest.approx(0.0)
        assert report["map"] == pytest.approx(0.0)
        assert report["avg_latency_ms"] == pytest.approx(0.0)
        assert report["per_query_results"] == []

    def test_evaluate_system_ground_truth_missing_query(self) -> None:
        evaluator = IREvaluator()
        report = evaluator.evaluate_system(
            lambda q: ["d1"],
            [{"id": "q1", "query": "x"}],
            {},
        )
        # Missing ground truth treated as empty relevant set.
        assert report["per_query_results"][0]["r@5"] == pytest.approx(0.0)
        assert report["per_query_results"][0]["ap"] == pytest.approx(0.0)
