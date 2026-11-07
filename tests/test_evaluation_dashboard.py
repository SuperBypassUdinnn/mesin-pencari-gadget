"""Evaluation dashboard component verification tests.

Verifies that `MetricsTable`, `MetricsBarChart`, and `EvaluationDashboard`
exist with correct exports and JSX structure, and that `App.jsx` handles tab
routing between `SearchPage` and `EvaluationDashboard`.

Run with: PYTHONPATH=. pytest tests/test_evaluation_dashboard.py -v
"""

import os
import re

FRONTEND = "frontend"


def _read(relative_path):
    path = os.path.join(FRONTEND, relative_path)
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


# ---------------------------------------------------------------------------
# Helpers (lightweight JSX validation, dependency-free)
# ---------------------------------------------------------------------------

_VOID_ELEMENTS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "source", "track", "wbr",
}


def _strip_comments(code):
    code = re.sub(r"/\*.*?\*/", "", code, flags=re.DOTALL)
    code = re.sub(r"//[^\n]*", "", code)
    return code


def _strip_strings(code):
    out = []
    i = 0
    n = len(code)
    while i < n:
        c = code[i]
        if c in ('"', "'", "`"):
            quote = c
            i += 1
            while i < n:
                ch = code[i]
                if ch == "\\":
                    i += 2
                    continue
                if ch == quote:
                    i += 1
                    break
                i += 1
        else:
            out.append(c)
            i += 1
    return "".join(out)


def _iter_tags(code):
    """Yield (closing, name, self_closing) for each JSX/HTML tag."""
    i = 0
    n = len(code)
    while i < n:
        if code[i] != "<":
            i += 1
            continue
        j = i + 1
        if j >= n:
            i += 1
            continue
        closing = code[j] == "/"
        if closing:
            j += 1
        if j >= n:
            i += 1
            continue
        c = code[j]
        if not (c.isalpha() or c == "_" or c == "-"):
            i += 1
            continue
        k = j
        while k < n and (code[k].isalnum() or code[k] in "-:_"):
            k += 1
        name = code[j:k]
        m = k
        self_closing = False
        while m < n:
            if code[m] == ">":
                m += 1
                break
            if code[m] == "/" and m + 1 < n and code[m + 1] == ">":
                self_closing = True
                m += 2
                break
            m += 1
        else:
            i += 1
            continue
        yield (closing, name, self_closing)
        i = m


def is_valid_jsx(code):
    code = _strip_comments(code)
    code = _strip_strings(code)
    stack = []
    for closing, name, self_closing in _iter_tags(code):
        if self_closing or name.lower() in _VOID_ELEMENTS:
            continue
        if closing:
            if not stack or stack[-1] != name:
                return False
            stack.pop()
        else:
            stack.append(name)
    return not stack


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestMetricsTableExists:
    def test_metrics_table_file_exists(self):
        path = os.path.join(FRONTEND, "src/components/MetricsTable.jsx")
        assert os.path.isfile(path), f"{path} missing"

    def test_metrics_table_export_default(self):
        content = _read("src/components/MetricsTable.jsx")
        assert re.search(r"export\s+default\b", content), (
            "MetricsTable.jsx missing export default signature"
        )

    def test_metrics_table_structure(self):
        content = _read("src/components/MetricsTable.jsx")
        for token in ("Okapi BM25", "Sentence-BERT", "P@5", "P@10", "R@5",
                      "R@10", "F1@5", "F1@10", "MAP", "Latency"):
            assert token in content, f"MetricsTable.jsx missing token: {token}"
        assert "<table" in content.lower(), (
            "MetricsTable.jsx missing table element"
        )

    def test_metrics_table_jsx_valid(self):
        assert is_valid_jsx(_read("src/components/MetricsTable.jsx")), (
            "MetricsTable.jsx contains invalid / unbalanced JSX"
        )


class TestMetricsBarChartExists:
    def test_metrics_bar_chart_file_exists(self):
        path = os.path.join(FRONTEND, "src/components/MetricsBarChart.jsx")
        assert os.path.isfile(path), f"{path} missing"

    def test_metrics_bar_chart_export_default(self):
        content = _read("src/components/MetricsBarChart.jsx")
        assert re.search(r"export\s+default\b", content), (
            "MetricsBarChart.jsx missing export default signature"
        )

    def test_metrics_bar_chart_structure(self):
        content = _read("src/components/MetricsBarChart.jsx")
        for token in ("Okapi BM25", "Sentence-BERT", "MAP", "P@5", "R@5",
                      "F1@5", "BarChart"):
            assert token in content, f"MetricsBarChart.jsx missing token: {token}"

    def test_metrics_bar_chart_jsx_valid(self):
        assert is_valid_jsx(_read("src/components/MetricsBarChart.jsx")), (
            "MetricsBarChart.jsx contains invalid / unbalanced JSX"
        )


class TestEvaluationDashboardExists:
    def test_evaluation_dashboard_file_exists(self):
        path = os.path.join(FRONTEND, "src/pages/EvaluationDashboard.jsx")
        assert os.path.isfile(path), f"{path} missing"

    def test_evaluation_dashboard_export_default(self):
        content = _read("src/pages/EvaluationDashboard.jsx")
        assert re.search(r"export\s+default\b", content), (
            "EvaluationDashboard.jsx missing export default signature"
        )

    def test_evaluation_dashboard_structure(self):
        content = _read("src/pages/EvaluationDashboard.jsx")
        for token in ("MetricsTable", "MetricsBarChart", "reload", "latency",
                      "MAP", "P@5"):
            assert token in content, f"EvaluationDashboard.jsx missing token: {token}"

    def test_evaluation_dashboard_jsx_valid(self):
        assert is_valid_jsx(_read("src/pages/EvaluationDashboard.jsx")), (
            "EvaluationDashboard.jsx contains invalid / unbalanced JSX"
        )


class TestAppTabRouting:
    def test_app_renders_evaluation_dashboard(self):
        content = _read("src/App.jsx")
        assert "EvaluationDashboard" in content, (
            "App.jsx missing EvaluationDashboard import/reference"
        )
        assert "evaluation" in content.lower(), (
            "App.jsx missing evaluation tab routing"
        )

    def test_app_jsx_valid(self):
        assert is_valid_jsx(_read("src/App.jsx")), (
            "App.jsx contains invalid / unbalanced JSX"
        )
