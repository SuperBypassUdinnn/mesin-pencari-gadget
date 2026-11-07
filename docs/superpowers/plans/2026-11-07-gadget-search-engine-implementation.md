# Indonesian Gadget Vertical Search Engine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a complete, containerized vertical search engine for Indonesian gadget reviews and specifications with multi-source crawling ($700 - 1.000+$ articles), custom Okapi BM25 vs Sentence-BERT semantic search, quantitative evaluation (MAP, Precision@K, Recall@K, F1@K), a modern React split-view UI, and comprehensive academic report templates adhering to USK FMIPA thesis standards.

**Architecture:** Decoupled containerized system with a Python FastAPI backend executing offline indexing and real-time retrieval (Inverted Index BM25 and in-memory S-BERT Cosine Similarity via NumPy/PyTorch) alongside a responsive React + Vite + Tailwind CSS frontend featuring side-by-side search comparison and an interactive evaluation analytics dashboard.

**Tech Stack:** Python 3.11+, FastAPI, Uvicorn, PySastrawi, Sentence-Transformers, NumPy, SQLite, React 18/19, Vite, Tailwind CSS, Lucide Icons, Recharts, Docker & Docker Compose.

**Spec:** `docs/superpowers/specs/2026-11-07-gadget-search-engine-design.md`

## Global Constraints

- **Corpus Scale**: Multi-source corpus targeting $700 - 1.000+$ Indonesian review documents from Gadgetren, Jagat Review, and Droidlime.
- **Language**: Formal technical English for all codebase files, comments, docstrings, commits, and engineering plans; Indonesian for final academic report sections (`docs/report/`).
- **Container Portability**: Single-command startup via `docker compose up --build` with persistent caching of embeddings and models in local volume mounts.
- **Clean Text Policy**: No decorative icons or emojis in code, commits, or technical artifacts.

## Review Focus

1. **Empty / No-Hit Queries**: Handled gracefully with zero-division protection in BM25 IDF and empty-state feedback in UI without crashing.
2. **Special Characters in Tech Names**: Handling queries like `"Snapdragon 8+ Gen 1"` or `"Wi-Fi 6E"` without losing essential alphanumeric tokens during text cleaning.
3. **Out-of-Vocabulary (OOV) Terms in BM25**: Returning empty posting list matches gracefully while Sentence-BERT still scores semantic proximity.
4. **Offline vs Online Preprocessing Latency**: Heavy corpus stemming and embedding generation must happen offline during indexing; online search latency must remain $< 30$ ms.
5. **Zero-Division in Evaluation Metrics**: Queries with 0 retrieved relevant documents must safely yield 0.0 Precision, Recall, and F1 without runtime ZeroDivisionError.

---

### Task 1: Repository Scaffolding, Docker Compose, & Environment Baseline

**Files:**
- Create: `docker-compose.yml`
- Create: `Makefile`
- Create: `backend/requirements.txt`
- Create: `backend/Dockerfile`
- Create: `frontend/package.json`
- Create: `frontend/Dockerfile`
- Create: `.gitignore`
- Test: `tests/test_scaffolding.py`

**Interfaces:**
- Consumes: Docker engine and local file system.
- Produces: Base container architecture, package definitions, and directory structure.

- [ ] **Step 1: Write the failing test for project directories and configs**

```python
# tests/test_scaffolding.py
import os

def test_project_structure_exists():
    required_dirs = [
        "data/raw", "data/processed", "data/ground_truth",
        "crawler/spiders", "backend/app/engine", "frontend/src",
        "evaluation_results/charts", "docs/report", "docs/screenshots"
    ]
    for d in required_dirs:
        assert os.path.exists(d), f"Directory {d} missing"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_scaffolding.py -v`
Expected: FAIL with missing directories.

- [ ] **Step 3: Create directories, `.gitignore`, `docker-compose.yml`, and `Makefile`**

Create folder hierarchy, ignore virtualenvs/node_modules/cache, and define `docker-compose.yml` with services `backend` (FastAPI port 8000) and `frontend` (React port 3000) with volume mounts for `data/` and `models/cache`.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_scaffolding.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add .
git commit -m "chore: scaffold repository structure and docker compose baseline"
```

---

### Task 2: Multi-Source Crawler Module & SQLite Data Layer

**Files:**
- Create: `crawler/spiders/base.py`
- Create: `crawler/spiders/gadgetren.py`
- Create: `crawler/spiders/jagatreview.py`
- Create: `crawler/spiders/droidlime.py`
- Create: `crawler/main_crawler.py`
- Create: `backend/app/db.py`
- Test: `tests/test_crawler_and_db.py`

**Interfaces:**
- Consumes: Target website HTML content.
- Produces:
  - `data/raw/documents.json`: JSON corpus of $700 - 1.000+$ documents.
  - `data/gadget.db`: SQLite database storing table `documents` with schema `(id, title, source, url, category, date, specs_json, content)`.
  - Function: `init_db(db_path: str) -> sqlite3.Connection`
  - Function: `insert_document(conn: sqlite3.Connection, doc: dict) -> None`
  - Function: `get_all_documents(conn: sqlite3.Connection) -> list[dict]`

- [ ] **Step 1: Write the failing test for database storage and crawler document schema**

```python
# tests/test_crawler_and_db.py
import sqlite3
from backend.app.db import init_db, insert_document, get_all_documents

def test_db_insert_and_retrieve(tmp_path):
    db_file = str(tmp_path / "test_gadget.db")
    conn = init_db(db_file)
    sample_doc = {
        "id": "doc_001",
        "title": "Review Xiaomi 13T",
        "source": "Gadgetren",
        "url": "https://gadgetren.com/sample",
        "category": "smartphone",
        "date": "2024-01-15",
        "specs": {"chipset": "Dimensity 8200 Ultra", "ram": "12GB"},
        "content": "Ini adalah isi artikel ulasan gadget yang lengkap."
    }
    insert_document(conn, sample_doc)
    docs = get_all_documents(conn)
    assert len(docs) == 1
    assert docs[0]["title"] == "Review Xiaomi 13T"
    assert docs[0]["source"] == "Gadgetren"
    assert docs[0]["specs"]["ram"] == "12GB"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_crawler_and_db.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'backend.app.db'`

- [ ] **Step 3: Implement `backend/app/db.py` and modular spiders in `crawler/`**

Implement SQLite table setup with JSON serialization for `specs`. Implement `base.py` crawler with checkpointing, rate limiting (1s delay), and specialized BeautifulSoup parsing for Gadgetren, Jagat Review, and Droidlime.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_crawler_and_db.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add crawler/ backend/app/db.py tests/test_crawler_and_db.py
git commit -m "feat: add multi-source crawler spiders and sqlite data layer"
```

---

### Task 3: Indonesian Text Preprocessor with PySastrawi

**Files:**
- Create: `backend/app/engine/preprocessor.py`
- Test: `tests/test_preprocessor.py`

**Interfaces:**
- Consumes: Raw text strings from article bodies and titles.
- Produces:
  - Class: `IndonesianPreprocessor`
  - Method: `clean_text(text: str) -> str`
  - Method: `tokenize(text: str) -> list[str]`
  - Method: `remove_stopwords(tokens: list[str]) -> list[str]`
  - Method: `stem_tokens(tokens: list[str]) -> list[str]`
  - Method: `preprocess(text: str) -> list[str]` (combined pipeline)

- [ ] **Step 1: Write the failing test for preprocessing pipeline**

```python
# tests/test_preprocessor.py
from backend.app.engine.preprocessor import IndonesianPreprocessor

def test_preprocessing_pipeline():
    prep = IndonesianPreprocessor()
    text = "Review HP Xiaomi 13T dengan kamera Leica yang sangat memukau di malam hari!"
    tokens = prep.preprocess(text)
    # Check lowercased, punctuation removed, stopwords like 'yang', 'sangat', 'di' filtered
    assert "review" in tokens
    assert "xiaomi" in tokens
    assert "13t" in tokens
    assert "kamera" in tokens
    assert "leica" in tokens
    assert "yang" not in tokens
    assert "sangat" not in tokens
    # Punctuation stripped
    assert "hari!" not in tokens
    assert "hari" in tokens
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_preprocessor.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Implement `IndonesianPreprocessor` in `backend/app/engine/preprocessor.py`**

Utilize `Sastrawi.StopWordRemover` and `Sastrawi.Stemmer` with cached stemmer initialization, regex-based token cleaning preserving alphanumeric technical strings (e.g., `8gen2`, `120hz`, `4k`).

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_preprocessor.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/app/engine/preprocessor.py tests/test_preprocessor.py
git commit -m "feat: implement indonesian text preprocessing with sastrawi"
```

### Task 4: Inverted Index & Okapi BM25 Ranking Engine

**Files:**
- Create: `backend/app/engine/bm25.py`
- Test: `tests/test_bm25.py`

**Interfaces:**
- Consumes: Tokenized documents from Task 3.
- Produces:
  - Class: `BM25Engine`
  - Method: `fit(corpus: list[dict]) -> None` (builds inverted index, doc lengths, avgdl)
  - Method: `save(index_path: str) -> None` / `load(index_path: str) -> None`
  - Method: `search(query_tokens: list[str], top_k: int = 10) -> list[tuple[str, float]]` (returns `[(doc_id, score), ...]`)

- [ ] **Step 1: Write the failing test for Inverted Index construction and BM25 ranking**

```python
# tests/test_bm25.py
from backend.app.engine.bm25 import BM25Engine

def test_bm25_retrieval():
    corpus = [
        {"id": "doc_1", "tokens": ["xiaomi", "kamera", "leica", "malam", "bagus"]},
        {"id": "doc_2", "tokens": ["samsung", "galaxy", "baterai", "awet", "layar", "amoled"]},
        {"id": "doc_3", "tokens": ["iphone", "kamera", "video", "sinematik", "jernih"]}
    ]
    bm25 = BM25Engine(k1=1.5, b=0.75)
    bm25.fit(corpus)
    
    results = bm25.search(["kamera", "leica"], top_k=2)
    assert len(results) > 0
    top_doc_id, top_score = results[0]
    assert top_doc_id == "doc_1"
    assert top_score > 0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_bm25.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Implement `BM25Engine` in `backend/app/engine/bm25.py`**

Construct posting list `term -> {doc_id: freq}`, compute document lengths, corpus `avgdl`, and Robertson-Spärck Jones IDF formula with add-1 smoothing to guarantee non-negative scores. Implement top-K score heap selection.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_bm25.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/app/engine/bm25.py tests/test_bm25.py
git commit -m "feat: implement inverted index and okapi bm25 search engine"
```

---

### Task 5: Sentence-BERT Multilingual Dense Vector Search Engine

**Files:**
- Create: `backend/app/engine/sbert.py`
- Test: `tests/test_sbert.py`

**Interfaces:**
- Consumes: Raw text strings (Title + Specs + Body snippet).
- Produces:
  - Class: `SBERTEngine`
  - Method: `encode(texts: list[str]) -> np.ndarray` (returns normalized $N \times D$ float32 matrix)
  - Method: `fit(corpus: list[dict], save_path: str = None) -> None`
  - Method: `search(query: str, top_k: int = 10) -> list[tuple[str, float]]` (returns `[(doc_id, cosine_score), ...]`)

- [ ] **Step 1: Write the failing test for S-BERT dense retrieval**

```python
# tests/test_sbert.py
import numpy as np
from backend.app.engine.sbert import SBERTEngine

def test_sbert_semantic_matching():
    corpus = [
        {"id": "doc_1", "text": "Smartphone fotografi dengan kemampuan potret malam hari sangat jernih."},
        {"id": "doc_2", "text": "Laptop untuk keperluan coding dan programming performa kencang."},
        {"id": "doc_3", "text": "Ponsel dengan daya tahan baterai sangat lama dua hari penuh."}
    ]
    engine = SBERTEngine(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
    engine.fit(corpus)
    
    # Query without exact words (semantic query)
    results = engine.search("HP foto malam bagus", top_k=2)
    assert len(results) > 0
    top_doc_id, score = results[0]
    assert top_doc_id == "doc_1"
    assert -1.0 <= score <= 1.0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_sbert.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Implement `SBERTEngine` in `backend/app/engine/sbert.py`**

Load `SentenceTransformer` with local cache directory in `models/cache`. Normalize embeddings with L2 norm so Cosine Similarity is computed via single matrix multiplication `np.dot(embeddings, query_vector)`.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_sbert.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/app/engine/sbert.py tests/test_sbert.py
git commit -m "feat: implement sentence-bert dense semantic vector retriever"
```

---

### Task 6: IR Evaluation Benchmark Engine (MAP, Precision@K, Recall@K, F1@K)

**Files:**
- Create: `backend/app/engine/evaluator.py`
- Test: `tests/test_evaluator.py`

**Interfaces:**
- Consumes: Test queries, ground truth binary relevance judgments, and ranked retrieval results.
- Produces:
  - Class: `IREvaluator`
  - Method: `precision_at_k(retrieved_ids: list[str], relevant_ids: set[str], k: int) -> float`
  - Method: `recall_at_k(retrieved_ids: list[str], relevant_ids: set[str], k: int) -> float`
  - Method: `f1_at_k(retrieved_ids: list[str], relevant_ids: set[str], k: int) -> float`
  - Method: `average_precision(retrieved_ids: list[str], relevant_ids: set[str]) -> float`
  - Method: `evaluate_system(retrieval_fn, test_queries: list[dict], ground_truth: dict) -> dict`

- [ ] **Step 1: Write the failing test for evaluation metrics computation**

```python
# tests/test_evaluator.py
from backend.app.engine.evaluator import IREvaluator

def test_evaluator_metrics():
    evaluator = IREvaluator()
    retrieved = ["doc_1", "doc_2", "doc_3", "doc_4", "doc_5"]
    relevant = {"doc_1", "doc_3", "doc_7"}
    
    p5 = evaluator.precision_at_k(retrieved, relevant, k=5)
    r5 = evaluator.recall_at_k(retrieved, relevant, k=5)
    f1 = evaluator.f1_at_k(retrieved, relevant, k=5)
    ap = evaluator.average_precision(retrieved, relevant)
    
    # 2 out of 5 retrieved are relevant -> P@5 = 0.4
    assert round(p5, 2) == 0.4
    # 2 out of 3 total relevant retrieved in top 5 -> R@5 = 0.67
    assert round(r5, 2) == 0.67
    assert round(f1, 2) == round(2 * (p5 * r5) / (p5 + r5), 2)
    # Hits at rank 1 (P@1 = 1/1 = 1.0) and rank 3 (P@3 = 2/3 = 0.667) -> AP = (1.0 + 0.667) / 3 = 0.556
    assert round(ap, 2) == 0.56
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_evaluator.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Implement `IREvaluator` in `backend/app/engine/evaluator.py`**

Implement standard trec_eval metric calculations with zero-division safety. Include batch evaluation calculating Mean Average Precision (MAP) and average latency across all queries.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_evaluator.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/app/engine/evaluator.py tests/test_evaluator.py
git commit -m "feat: implement ir evaluation engine for precision, recall, f1, and map"
```

### Task 7: FastAPI REST API Endpoints & Backend Service

**Files:**
- Create: `backend/app/main.py`
- Test: `tests/test_api.py`

**Interfaces:**
- Consumes: `BM25Engine`, `SBERTEngine`, `IREvaluator`, and `db.py`.
- Produces:
  - `GET /api/search?q={query}&algo={bm25|sbert|both}&top_k=10`
  - `GET /api/documents/{id}`
  - `GET /api/evaluation`
  - `GET /api/health`

- [ ] **Step 1: Write the failing test for FastAPI search and evaluation endpoints**

```python
# tests/test_api.py
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_api_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"

def test_api_search_both():
    res = client.get("/api/search?q=kamera&algo=both&top_k=5")
    assert res.status_code == 200
    data = res.json()
    assert "bm25" in data
    assert "sbert" in data
    assert "latency_ms" in data["bm25"]
    assert "results" in data["bm25"]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_api.py -v`
Expected: FAIL with `ModuleNotFoundError`

- [ ] **Step 3: Implement `backend/app/main.py`**

Wire the initialized SQLite connection, load `BM25Engine` and `SBERTEngine` upon startup event (`lifespan`), measure latency per algorithm with `time.perf_counter()`, enrich returned document IDs with title, source, specs, and highlighted snippets.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_api.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add backend/app/main.py tests/test_api.py
git commit -m "feat: implement fastapi rest api for dual-engine search and evaluation"
```

---

### Task 8: React Web UI Components & Side-by-Side Search

**Files:**
- Create: `frontend/src/components/Navbar.jsx`
- Create: `frontend/src/components/SearchBar.jsx`
- Create: `frontend/src/components/ResultCard.jsx`
- Create: `frontend/src/components/SplitView.jsx`
- Create: `frontend/src/components/SpecsModal.jsx`
- Create: `frontend/src/pages/SearchPage.jsx`
- Create: `frontend/src/services/api.js`
- Test: `frontend/src/components/ResultCard.test.jsx`

**Interfaces:**
- Consumes: REST endpoints from Task 7.
- Produces: Interactive React UI supporting Hero search, quick suggestion pills, source badges (`[Gadgetren]`, `[Jagat Review]`, `[Droidlime]`), side-by-side comparison, and specifications drawer.

- [ ] **Step 1: Write component unit test for ResultCard**

```jsx
// frontend/src/components/ResultCard.test.jsx
import { render, screen } from '@testing-library/react';
import ResultCard from './ResultCard';

test('renders result card with title, source badge, and score', () => {
  const mockDoc = {
    id: "doc_01",
    title: "Review Xiaomi 13T Leica",
    source: "Gadgetren",
    score: 14.82,
    latency_ms: 4.2,
    category: "smartphone",
    specs: { chipset: "Dimensity 8200" },
    snippet: "Kamera Leica mumpuni untuk kondisi redup."
  };
  render(<ResultCard document={mockDoc} algorithm="bm25" />);
  expect(screen.getByText(/Review Xiaomi 13T Leica/i)).toBeInTheDocument();
  expect(screen.getByText(/Gadgetren/i)).toBeInTheDocument();
  expect(screen.getByText(/14.82/i)).toBeInTheDocument();
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `npm --prefix frontend test -- ResultCard.test.jsx`
Expected: FAIL (component not found).

- [ ] **Step 3: Implement React components and `api.js` client**

Create responsive Tailwind UI:
- `SearchBar`: pill suggestions, clear button, loader.
- `SplitView`: dual column view with BM25 on the left and Sentence-BERT on the right, latency badges, and hit count headers.
- `SpecsModal`: modal drawer presenting technical specs table.

- [ ] **Step 4: Run test to verify it passes**

Run: `npm --prefix frontend test -- ResultCard.test.jsx`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add frontend/
git commit -m "feat: implement react split-view search ui and result cards"
```

---

### Task 9: Evaluation Dashboard UI & Metrics Visualization

**Files:**
- Create: `frontend/src/pages/EvaluationDashboard.jsx`
- Create: `frontend/src/components/MetricsBarChart.jsx`
- Create: `frontend/src/components/MetricsTable.jsx`
- Test: `frontend/src/pages/EvaluationDashboard.test.jsx`

**Interfaces:**
- Consumes: `GET /api/evaluation` data.
- Produces: Comparative tables for Precision@5, Precision@10, Recall, F1, MAP, and interactive charts comparing BM25 vs S-BERT.

- [ ] **Step 1: Write test for EvaluationDashboard rendering**

```jsx
// frontend/src/pages/EvaluationDashboard.test.jsx
import { render, screen } from '@testing-library/react';
import MetricsTable from '../components/MetricsTable';

test('renders comparative metrics table', () => {
  const metricsData = {
    bm25: { p5: 0.8, r5: 0.65, f1: 0.72, map: 0.76, avg_latency_ms: 3.8 },
    sbert: { p5: 0.74, r5: 0.78, f1: 0.76, map: 0.81, avg_latency_ms: 18.5 }
  };
  render(<MetricsTable data={metricsData} />);
  expect(screen.getByText(/Okapi BM25/i)).toBeInTheDocument();
  expect(screen.getByText(/Sentence-BERT/i)).toBeInTheDocument();
  expect(screen.getByText(/0.76/i)).toBeInTheDocument();
  expect(screen.getByText(/0.81/i)).toBeInTheDocument();
});
```

- [ ] **Step 2: Run test to verify it fails**

Run: `npm --prefix frontend test -- EvaluationDashboard.test.jsx`
Expected: FAIL

- [ ] **Step 3: Implement `EvaluationDashboard.jsx` with Recharts**

Build summary cards, radar/bar comparison charts, latency comparison gauge, and per-query ground-truth inspection dropdown.

- [ ] **Step 4: Run test to verify it passes**

Run: `npm --prefix frontend test -- EvaluationDashboard.test.jsx`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add frontend/src/pages/EvaluationDashboard.jsx frontend/src/components/Metrics*
git commit -m "feat: implement interactive ir evaluation dashboard and chart visualizations"
```

---

### Task 10: Academic Report Templates, Evidence Logging, & Workflow Hand-off

**Files:**
- Create: `docs/report/00_Halaman_Judul_dan_Pengesahan.md`
- Create: `docs/report/01_Abstrak_dan_Abstract.md`
- Create: `docs/report/BAB_I_Pendahuluan.md`
- Create: `docs/report/BAB_II_Tinjauan_Kepustakaan.md`
- Create: `docs/report/BAB_III_Metode_Penelitian.md`
- Create: `docs/report/BAB_IV_Hasil_dan_Pembahasan.md`
- Create: `docs/report/BAB_V_Kesimpulan_dan_Saran.md`
- Create: `docs/report/Daftar_Pustaka.md`
- Create: `docs/report/Lampiran_Kontribusi_Anggota.md`
- Create: `docs/presentation/5_MINUTE_DEMO_SCRIPT.md`
- Test: `tests/test_report_structure.py`

**Interfaces:**
- Consumes: Evaluated benchmark results, system screenshots, USK FMIPA thesis report guidelines.
- Produces: Complete draft report structure ready for export to `Kelompok_X.pdf`, presentation script, and individual member contribution table.

- [ ] **Step 1: Write test for report chapters and contribution table verification**

```python
# tests/test_report_structure.py
import os

def test_report_chapters_exist():
    chapters = [
        "docs/report/00_Halaman_Judul_dan_Pengesahan.md",
        "docs/report/01_Abstrak_dan_Abstract.md",
        "docs/report/BAB_I_Pendahuluan.md",
        "docs/report/BAB_II_Tinjauan_Kepustakaan.md",
        "docs/report/BAB_III_Metode_Penelitian.md",
        "docs/report/BAB_IV_Hasil_dan_Pembahasan.md",
        "docs/report/BAB_V_Kesimpulan_dan_Saran.md",
        "docs/report/Lampiran_Kontribusi_Anggota.md"
    ]
    for ch in chapters:
        assert os.path.exists(ch), f"Chapter {ch} is missing"
        with open(ch, "r", encoding="utf-8") as f:
            content = f.read()
            assert len(content) > 100, f"Chapter {ch} is too short"
```

- [ ] **Step 2: Run test to verify it fails**

Run: `pytest tests/test_report_structure.py -v`
Expected: FAIL

- [ ] **Step 3: Draft USK FMIPA report templates and demo script**

Populate all chapters according to the USK FMIPA guidelines (Lampiran 7, 8, 9, 11a, 11b, 12, 13) with academic Indonesian text:
- Title, Approval, Plagiarism statement, Abstract (ID & EN).
- Bab I: Pendahuluan (Latar Belakang, Rumusan Masalah, Tujuan, Manfaat).
- Bab II: Tinjauan Pustaka (IR, Sastrawi, BM25 formulas, S-BERT architecture, MAP/P/R/F1).
- Bab III: Metode Penelitian (Docker setup, Multi-source crawling Gadgetren + Jagat Review + Droidlime, schema, pipeline flow).
- Bab IV: Hasil dan Pembahasan (Analisis karakteristik 1.000 dokumen, Zipf law, komparasi kueri spesifik vs semantik, tabel evaluasi).
- Bab V: Kesimpulan dan Saran.
- Lampiran: Tabel Kontribusi Anggota 1, 2, dan 3 secara transparan.

- [ ] **Step 4: Run test to verify it passes**

Run: `pytest tests/test_report_structure.py -v`
Expected: PASS

- [ ] **Step 5: Commit**

```bash
git add docs/report/ docs/presentation/ tests/test_report_structure.py
git commit -m "docs: establish usk fmipa report chapters, contribution table, and demo script"
```
