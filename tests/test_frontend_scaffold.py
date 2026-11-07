"""Scaffold verification for the React frontend of the gadget search engine.

Verifies that every required frontend component, build config, and export
signature exists and that the JSX sources are syntactically well-formed.

Run with: PYTHONPATH=. pytest tests/test_frontend_scaffold.py -v
"""

import os
import re

FRONTEND = "frontend"

REQUIRED_FILES = [
    "index.html",
    "vite.config.js",
    "tailwind.config.js",
    "postcss.config.js",
    "src/index.css",
    "src/main.jsx",
    "src/App.jsx",
    "src/services/api.js",
    "src/components/Navbar.jsx",
    "src/components/SearchBar.jsx",
    "src/components/ResultCard.jsx",
    "src/components/SplitView.jsx",
    "src/components/SpecsModal.jsx",
    "src/pages/SearchPage.jsx",
]

REQUIRED_DIRS = [
    "src",
    "src/components",
    "src/pages",
    "src/services",
]

# Each component/module must expose an `export default` signature.
EXPORT_DEFAULT_MODULES = [
    "src/components/Navbar.jsx",
    "src/components/SearchBar.jsx",
    "src/components/ResultCard.jsx",
    "src/components/SplitView.jsx",
    "src/components/SpecsModal.jsx",
    "src/pages/SearchPage.jsx",
    "src/App.jsx",
]

# The API service module must export at least one named binding.
API_MODULE = "src/services/api.js"


def _read(relative_path):
    path = os.path.join(FRONTEND, relative_path)
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


# ---------------------------------------------------------------------------
# JSX syntax validation (lightweight, dependency-free)
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
        # A tag name must start with a letter, underscore, or hyphen. This
        # keeps comparisons such as `a < b` inside expressions from being
        # mistaken for tags.
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
            # No closing angle bracket: not a complete tag.
            i += 1
            continue
        yield (closing, name, self_closing)
        i = m


def is_valid_jsx(code):
    """Return True when angle-bracket tags are balanced and well-formed."""
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


class TestFrontendFilesExist:
    def test_required_directories_exist(self):
        for directory in REQUIRED_DIRS:
            assert os.path.isdir(
                os.path.join(FRONTEND, directory)
            ), f"Directory {directory} missing"

    def test_required_files_exist(self):
        for relative_path in REQUIRED_FILES:
            full = os.path.join(FRONTEND, relative_path)
            assert os.path.isfile(full), f"File {full} missing"


class TestExportSignatures:
    def test_components_export_default(self):
        for relative_path in EXPORT_DEFAULT_MODULES:
            content = _read(relative_path)
            assert re.search(
                r"export\s+default\b", content
            ), f"{relative_path} missing export default signature"

    def test_api_module_exports_named_binding(self):
        content = _read(API_MODULE)
        assert re.search(r"\bexport\b", content), (
            f"{API_MODULE} missing export signature"
        )


class TestContentSignatures:
    def test_index_html_has_root_and_module_script(self):
        content = _read("index.html")
        assert 'id="root"' in content, "index.html missing #root mount node"
        assert 'type="module"' in content, "index.html missing module script"

    def test_vite_config_uses_react_plugin(self):
        content = _read("vite.config.js")
        assert "@vitejs/plugin-react" in content, (
            "vite.config.js missing @vitejs/plugin-react"
        )

    def test_tailwind_config_has_content_and_theme(self):
        content = _read("tailwind.config.js")
        assert "content" in content, "tailwind.config.js missing content"
        assert "theme" in content, "tailwind.config.js missing theme"

    def test_postcss_config_uses_tailwind_and_autoprefixer(self):
        content = _read("postcss.config.js")
        assert "tailwindcss" in content, "postcss.config.js missing tailwindcss"
        assert "autoprefixer" in content, "postcss.config.js missing autoprefixer"

    def test_index_css_has_tailwind_directives(self):
        content = _read("src/index.css")
        for directive in ("@tailwind base", "@tailwind components", "@tailwind utilities"):
            assert directive in content, f"src/index.css missing {directive}"

    def test_main_jsx_renders_app_into_root(self):
        content = _read("src/main.jsx")
        assert "ReactDOM.createRoot" in content, "src/main.jsx missing ReactDOM.createRoot"
        assert "getElementById" in content and "root" in content, (
            "src/main.jsx missing root mount"
        )
        assert "<App" in content, "src/main.jsx missing <App"

    def test_api_js_connects_to_localhost_8000(self):
        content = _read(API_MODULE)
        assert "axios" in content, "src/services/api.js missing axios"
        assert "http://localhost:8000" in content, (
            "src/services/api.js missing http://localhost:8000"
        )

    def test_navbar_has_pencarian_and_evaluasi_tabs(self):
        content = _read("src/components/Navbar.jsx")
        assert "Pencarian" in content, "Navbar missing Pencarian tab"
        assert "Evaluasi" in content, "Navbar missing Evaluasi tab"

    def test_searchbar_has_suggestion_pills(self):
        content = _read("src/components/SearchBar.jsx")
        for pill in ("HP Kamera Low-light", "Laptop Coding 10 Jutaan", "Fast Charging 120W"):
            assert pill in content, f"SearchBar missing suggestion pill: {pill}"

    def test_resultcard_has_source_badges_and_fields(self):
        content = _read("src/components/ResultCard.jsx")
        for badge in ("Gadgetren", "Jagat Review", "Droidlime"):
            assert badge in content, f"ResultCard missing source badge: {badge}"
        for field in ("score", "latency_ms", "snippet", "specs"):
            assert field in content, f"ResultCard missing field: {field}"

    def test_splitview_has_bm25_and_sbert_columns(self):
        content = _read("src/components/SplitView.jsx")
        assert "Okapi BM25" in content, "SplitView missing Okapi BM25 column"
        assert ("Sentence-BERT" in content or "S-BERT" in content), (
            "SplitView missing Sentence-BERT column"
        )

    def test_specsmodal_shows_table_and_review(self):
        content = _read("src/components/SpecsModal.jsx")
        assert "<table" in content.lower(), "SpecsModal missing specs table"
        assert ("review" in content.lower() or "content" in content.lower()), (
            "SpecsModal missing review content"
        )

    def test_searchpage_wires_api_and_view_mode(self):
        content = _read("src/pages/SearchPage.jsx")
        assert ("api" in content.lower() or "searchGadgets" in content), (
            "SearchPage missing API wiring"
        )
        assert ("view" in content.lower() or "split" in content.lower() or "tab" in content.lower()), (
            "SearchPage missing view mode handling"
        )


class TestJsxValidity:
    def test_all_jsx_files_are_syntactically_valid(self):
        jsx_files = [
            p for p in REQUIRED_FILES if p.endswith(".jsx")
        ]
        for relative_path in jsx_files:
            content = _read(relative_path)
            assert is_valid_jsx(content), (
                f"{relative_path} contains invalid / unbalanced JSX"
            )
