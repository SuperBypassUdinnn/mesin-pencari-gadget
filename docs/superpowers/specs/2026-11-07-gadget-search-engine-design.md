# Architectural Design Specification: Indonesian Gadget Vertical Search Engine

- **Project**: Vertical Search Engine for Indonesian Gadget Reviews & Technical Specifications (`mesin-pencari-gadget`)
- **Course**: Penelusuran Informasi (Information Retrieval) 2025/2026
- **Institution**: Universitas Syiah Kuala (USK) - FMIPA
- **Team Size**: 3 Members
- **Date**: 2026-11-07
- **Status**: Draft for Review

---

## 1. Executive Summary & Goals

The objective of this project is to build an end-to-end Indonesian Vertical Search Engine specialized in gadget reviews and hardware specifications. The system processes a crawled corpus of at least 300 Indonesian documents, implements two distinct Information Retrieval (IR) algorithms (**Okapi BM25** and **Sentence-BERT Semantic Retrieval**), provides an interactive web interface with side-by-side search comparison and evaluation dashboards, and encapsulates all services in Docker containers for single-command portability.

### Key Success Criteria:
1. **Corpus**: $700 - 1.000+$ comprehensive Indonesian gadget review & specification articles crawled from multi-source tech portals (**Gadgetren**, **Jagat Review**, and **Droidlime**).
2. **Core IR Algorithms**:
   - Probabilistic Lexical: Custom Inverted Index with **Okapi BM25** scoring ($k_1=1.5, b=0.75$).
   - Dense Semantic: **Sentence-BERT** embeddings (`paraphrase-multilingual-MiniLM-L12-v2` / IndoBERT) with Cosine Similarity vector search.
3. **Comprehensive IR Evaluation**: Precision@K, Recall@K, F1@K, and Mean Average Precision (MAP) evaluated against 10–15 annotated ground-truth test queries across the enlarged corpus.
4. **Interactive Web UI**: Modern React + Vite + Tailwind CSS interface featuring multi-source badges, Side-by-Side split view, snippet highlighting, and an interactive evaluation analytics dashboard.
5. **Portability & Deployment**: 1-command startup via `docker-compose up --build` serving both frontend and FastAPI backend without dependency conflicts.
6. **Academic Reporting & Presentation**: Full final report compliant with the USK FMIPA thesis report guidelines (Bab I–V, Lampiran Kontribusi Anggota), YouTube presentation video, and 5-minute live demo deck.

## 2. System Architecture & Containerization

The system follows a decoupled client-server architecture containerized via Docker Compose.

```
[ User / Evaluator / Lecturer ]
               │
               ▼ (Port 3000 / 80)
┌─────────────────────────────────────────────────────────────────┐
│ Docker Environment (docker-compose)                            │
│                                                                 │
│  ┌─────────────────────────┐         ┌───────────────────────┐  │
│  │   Frontend Service      │         │    Backend Service    │  │
│  │   (React + Vite +       │────────▶│    (Python FastAPI)   │  │
│  │    Tailwind CSS)        │  REST   │                       │  │
│  └─────────────────────────┘  Calls  └───────────┬───────────┘  │
│                                                  │              │
│                                      ┌───────────▼───────────┐  │
│                                      │     Storage Layer     │  │
│                                      │ - SQLite (Metadata)   │  │
│                                      │ - Inverted Index JSON │  │
│                                      │ - S-BERT Matrix (.npy)│  │
│                                      └───────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

### 2.1 Backend Service (`backend/`)
- **Runtime**: Python 3.11 with FastAPI and Uvicorn.
- **Role**: Serves the REST API, manages data ingestion, handles real-time text preprocessing, runs the BM25 and Sentence-BERT retrieval engines, and calculates evaluation benchmarks.
- **Key API Endpoints**:
  - `GET /api/search?q={query}&algo={bm25|sbert|both}&top_k=10`: Returns ranked results, relevance scores, and execution latency in milliseconds.
  - `GET /api/documents/{id}`: Returns complete review body and parsed technical specs for a given gadget.
  - `GET /api/evaluation`: Returns computed Precision@5, Precision@10, Recall@K, F1@K, MAP, and latency metrics across test queries.
  - `GET /api/health`: Health check endpoint.

### 2.2 Frontend Service (`frontend/`)
- **Runtime**: Node.js 20 build stage, served in production via Nginx (or Vite preview).
- **Role**: Responsive consumer search interface and academic analytics portal.
- **Key Views**:
  - **Search Page**: Search input with quick suggestion pills, algorithmic view switcher (`Side-by-Side Split View`, `Single Tab View`).
  - **Result Card**: Displays gadget title, algorithm badge, similarity/relevance score, latency badge, highlighted matching snippets, specs tag chips, and external source link.
  - **Document Detail Modal**: Full specification drawer and readable article text.
  - **Evaluation Dashboard Page**: Comparative metrics tables, radar/bar charts comparing BM25 vs S-BERT, and per-query drilldown.

### 2.3 Storage Architecture (Option 1: SQLite + In-Memory Python / NumPy)
- **Document Store (`data/gadget.db`)**: SQLite relational database storing document ID, title, publication date, URL, category, parsed JSON specs, and raw content.
- **BM25 Lexical Store (`data/processed/inverted_index.json`)**: Inverted index posting list (`term -> {doc_id: term_frequency}`), document lengths dictionary (`doc_id -> length`), and average document length (`avgdl`).
- **Semantic Vector Store (`data/processed/embeddings.npy` & `doc_ids.json`)**: Precomputed L2-normalized dense vector matrix of dimension $N \times 384$. Dot product with query vector provides exact Cosine Similarity in $\le 1$ ms without external vector DB dependencies.

## 3. Data Pipeline & Core IR Engine (Member 2 (Fadhlur) Lead)

### 3.1 Indonesian Text Preprocessing Pipeline
1. **Case Folding & Normalization**: Convert all characters to lowercase; remove non-alphanumeric symbols while preserving technical specs hyphenations (e.g., `snapdragon 8 gen 2`).
2. **Tokenization**: Whitespace and regex tokenization into distinct word tokens.
3. **Stopword Removal**: Filter non-informative Indonesian tokens using the Sastrawi/Tala stopword lexicon. Whitelist critical technical modifiers (e.g., `tanpa`, `tidak`, `anti`).
4. **Stemming**: Apply **PySastrawi** (Nazief-Adriani morphological rules) to obtain root base words.
5. **Offline Indexing Strategy**: Preprocessing all $\ge 300$ multi-paragraph articles is done once offline via `python -m app.engine.indexer`. The indexed tokens and vectors are cached to disk so runtime query processing only stems the short incoming query ($\le 20$ ms latency).

### 3.2 Algoritma 1: Okapi BM25 Retrieval Engine
- **Mathematical Formulation**:
  $$Score(D, Q) = \sum_{q \in Q} IDF(q) \cdot \frac{f(q, D) \cdot (k_1 + 1)}{f(q, D) + k_1 \cdot \left(1 - b + b \cdot \frac{|D|}{avgdl}\right)}$$
  Where:
  $$IDF(q) = \ln \left( \frac{N - n(q) + 0.5}{n(q) + 0.5} + 1 \right)$$
  - $N$: Total number of documents in corpus.
  - $n(q)$: Number of documents containing query term $q$.
  - $f(q, D)$: Term frequency of $q$ in document $D$.
  - $|D|$ and $avgdl$: Length of document $D$ and average document length across the corpus.
  - Parameters: $k_1 = 1.5$ (term saturation), $b = 0.75$ (length normalization).
- **Inverted Index Posting List**:
  ```python
  {
      "baterai": {"doc_001": 3, "doc_004": 1, "doc_012": 5},
      "kamera": {"doc_001": 6, "doc_002": 2}
  }
  ```

### 3.3 Algoritma 2: Sentence-BERT Dense Semantic Retrieval
- **Embedding Model**: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` (384-dimensional dense vectors) cached locally in `models/cache`.
- **Document Vectorization**: Concatenation of gadget title, extracted key specifications, and review summary encoded into dense vector $\vec{d} \in \mathbb{R}^{384}$.
- **Normalization & Similarity**:
  $$\vec{u}_{norm} = \frac{\vec{u}}{\|\vec{u}\|_2}, \quad \vec{v}_{norm} = \frac{\vec{v}}{\|\vec{v}\|_2}$$
  $$\text{Cosine Similarity}(\vec{u}, \vec{v}) = \vec{u}_{norm} \cdot \vec{v}_{norm}$$
- **Fast Search Execution**: Single matrix-vector dot product `similarities = np.dot(doc_embeddings, query_embedding)` followed by `np.argpartition` / `argsort` for Top-K retrieval in $< 2$ ms.

### 3.4 Evaluation Engine & Benchmark Matrix
- **Test Query Set**: 10–15 representative queries covering:
  - Exact technical queries (e.g., `"Snapdragon 8 Gen 2"`, `"Layar AMOLED 120Hz"`, `"RAM 16GB Fast Charging"`).
  - High-level semantic/intent queries (e.g., `"HP untuk fotografi malam hari"`, `"Laptop murah untuk mahasiswa teknik"`, `"Gadget baterai awet seharian"`).
- **Ground Truth**: Binary relevance matrix ($1 = \text{relevant}, 0 = \text{non-relevant}$) stored in `data/ground_truth/relevance_judgments.json`.
- **Metrics Computed**:
  - $\text{Precision}@K = \frac{|\text{Relevant Docs} \cap \text{Top-K Retrieved Docs}|}{K}$
  - $\text{Recall}@K = \frac{|\text{Relevant Docs} \cap \text{Top-K Retrieved Docs}|}{|\text{Total Relevant Docs in Corpus}|}$
  - $\text{F1-Score}@K = 2 \cdot \frac{\text{Precision}@K \cdot \text{Recall}@K}{\text{Precision}@K + \text{Recall}@K}$
  - **Mean Average Precision (MAP)**:
    $$AP = \frac{\sum_{k=1}^{N} (P@k \cdot \text{rel}(k))}{|\text{Total Relevant Docs}|}, \quad MAP = \frac{1}{|Q|} \sum_{q=1}^{|Q|} AP(q)$$
  - **Latency**: Mean query response time (ms) across test runs.

## 4. Team Work Breakdown & Concrete 3-Week Workflow

### 4.1 Responsibilities Matrix

| Member | Primary Role | Concrete Deliverables |
| :--- | :--- | :--- |
| **Member 1** | Frontend UI & Visuals Lead | - React + Vite + Tailwind application setup.<br>- Hero Search Bar with quick pill suggestions.<br>- Side-by-Side comparison layout & Result Cards.<br>- Modal specification drawer.<br>- Interactive Evaluation Dashboard (Charts & Metric Tables via Recharts).<br>- Presentation Slides deck design. |
| **Member 2 (Fadhlur)** | Core IR Engine & Backend Lead | - FastAPI backend architecture & REST endpoints.<br>- Indonesian Text Preprocessor (Cleaning, Tokenizer, Stopword, Sastrawi Stemmer).<br>- Inverted Index structure & Okapi BM25 implementation from scratch.<br>- Sentence-BERT multilingual embedding pipeline & Cosine Similarity search.<br>- Evaluation Engine calculating Precision@K, Recall@K, F1@K, MAP, & Latency.<br>- Docker Compose setup & container orchestration. |
| **Member 3** | Data Engineering & Report Lead | - Multi-source scraper for `gadgetren.com`, `jagatreview.com`, and `droidlime.com` crawling $700 - 1.000+$ full review articles.<br>- Structured JSON data schema with source provenance (`source`: Gadgetren/JagatReview/Droidlime) & SQLite ingestion script.<br>- Coordination with team on 10–15 test queries & ground-truth relevance labeling.<br>- Lead author for Final Report following USK FMIPA TA guidelines (Bab I–V).<br>- Scripting & recording coordinator for the YouTube presentation video. |

### 4.2 3-Week Concrete Sprint Schedule

#### Sprint 1 (Days 1–7): Data Ingestion & Core Foundation
- **Member 3**: Implement modular scrapers in `crawler/` (`spiders/gadgetren.py`, `spiders/jagatreview.py`, `spiders/droidlime.py`), collect 700–1.000+ articles, output `data/raw/documents.json`. Populate `docs/report/BAB_I_Pendahuluan.md` and `BAB_II_Tinjauan_Kepustakaan.md`.
- **Member 2 (Fadhlur)**: Build `preprocessor.py` with Sastrawi stemming and tokenization tests. Implement Inverted Index builder and verify offline batch indexing on the enlarged multi-source dataset.
- **Member 1**: Initialize React Vite Tailwind project, build wireframes for Search Page, source badge pills (`[Gadgetren]`, `[Jagat Review]`), and Side-by-Side result view.
- **Milestone 1**: 700–1.000+ clean documents in SQLite and preprocessed token cache verified.

#### Sprint 2 (Days 8–14): IR Algorithms, Evaluation, & Integration
- **Member 2 (Fadhlur)**: Complete BM25 ranking algorithm and S-BERT dense vector retriever. Build `evaluator.py`. Expose FastAPI `/api/search` and `/api/evaluation` endpoints.
- **Member 3 & Team**: Define 10–15 standard queries and annotate binary relevance judgments in `relevance_judgments.json`. Member 3 drafts `docs/report/BAB_III_Metode_Penelitian.md`.
- **Member 1**: Wire React frontend to FastAPI API. Implement live search, side-by-side display, snippet keyword highlighting, and interactive evaluation metrics dashboard.
- **Milestone 2**: Full end-to-end working system with quantifiable BM25 vs S-BERT benchmark results.

#### Sprint 3 (Days 15–21): Containerization, Presentation, & Report Finalization
- **Member 2 (Fadhlur)**: Verify multi-container `docker compose up --build` performance and test 1-command startup on fresh environment.
- **Member 1 & Team**: Polish UI aesthetics, create presentation slides (PPTX/Canva) for the 5-minute live demo. Record and edit YouTube presentation video (all 3 members speaking).
- **Member 3 & Team**: Finalize `BAB_IV_Hasil_dan_Pembahasan.md`, `BAB_V_Kesimpulan.md`, Abstract (ID & EN), and compile the complete PDF report `Kelompok_X.pdf` according to the USK FMIPA template.
- **Milestone 3**: Final deliverables submitted (GitHub repository, YouTube video link, PDF report).

---

## 5. Repository Structure & Artifact Management

```text
mesin-pencari-gadget/
├── .github/
│   └── workflows/ci.yml         # Automated lint and unit testing
├── docker-compose.yml           # Unified 1-command execution
├── Makefile                     # Commands: make dev, make build, make eval, make test
├── README.md                    # Setup guide, system architecture, & YouTube demo link
│
├── data/                        # Persistent Data Layer
│   ├── raw/documents.json       # Crawled 700-1000+ raw gadget articles across 3 portals
│   ├── processed/               # Preprocessed tokens, inverted index, embeddings.npy
│   ├── ground_truth/            # test_queries.json & relevance_judgments.json
│   └── gadget.db                # SQLite database for document metadata
│
├── crawler/                     # [Member 3] Multi-Source Data Extraction
│   ├── main_crawler.py          # Master runner orchestrating all portals
│   ├── spiders/                 # Modular site extractors
│   │   ├── gadgetren.py         # Parser for Gadgetren review pages
│   │   ├── jagatreview.py       # Parser for Jagat Review articles
│   │   └── droidlime.py         # Parser for Droidlime reviews
│   ├── parse_specs.py           # Technical specs extractor
│   └── requirements.txt
│
├── backend/                     # [Member 2 (Fadhlur)] Core IR Engine & API
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py              # FastAPI endpoints
│   │   ├── config.py            # Environment & path settings
│   │   ├── engine/
│   │   │   ├── preprocessor.py  # Text cleaner, stopword removal, Sastrawi stemmer
│   │   │   ├── indexer.py       # Builds Inverted Index & S-BERT embeddings
│   │   │   ├── bm25.py          # Okapi BM25 implementation
│   │   │   ├── sbert.py         # S-BERT semantic similarity retriever
│   │   │   └── evaluator.py     # MAP, Precision@K, Recall@K, F1@K, Latency
│   │   └── tests/               # Pytest suites for algorithms and API
│   └── README.md
│
├── frontend/                    # [Member 1] Modern Web Interface
│   ├── Dockerfile
│   ├── package.json
│   ├── tailwind.config.js
│   ├── src/
│   │   ├── components/          # SearchBar, SplitView, ResultCard, SpecsModal
│   │   ├── pages/               # SearchPage, EvaluationDashboard
│   │   └── services/api.js      # Axios / Fetch client for FastAPI
│   └── README.md
│
├── evaluation_results/          # Benchmarking Outputs & Reports
│   ├── metrics_summary.json     # P@K, R@K, F1@K, MAP for BM25 and S-BERT
│   ├── per_query_benchmark.csv  # Detailed query-by-query performance
│   └── charts/                  # Visual charts exported for reports & slides
│
└── docs/                        # Complete Academic Documentation & Evidence
    ├── report/                  # USK FMIPA Final Report Drafts (Markdown / LaTeX / Docx)
    │   ├── 00_Halaman_Judul_dan_Pengesahan.md
    │   ├── 01_Abstrak_dan_Abstract.md
    │   ├── BAB_I_Pendahuluan.md
    │   ├── BAB_II_Tinjauan_Kepustakaan.md
    │   ├── BAB_III_Metode_Penelitian.md
    │   ├── BAB_IV_Hasil_dan_Pembahasan.md
    │   ├── BAB_V_Kesimpulan_dan_Saran.md
    │   ├── Daftar_Pustaka.md
    │   └── Lampiran_Kontribusi_Anggota.md
    ├── presentation/            # 5-minute demo deck & YouTube video script
    ├── screenshots/             # Visual proof of crawling, indexing, UI, & evaluation
    └── references/              # Original assignment PDF & USK TA guidelines
```

## 6. Academic Report & Presentation Strategy

### 6.1 Report Structure (USK FMIPA Thesis Guidelines)
The report is authored collaboratively under `docs/report/` and exported to `Kelompok_X.pdf`:
1. **Front Matter**:
   - Sampul & Halaman Judul (Format Lampiran 7).
   - Halaman Pengesahan (Format Lampiran 8).
   - Pernyataan Bebas Plagiasi (Format Lampiran 9).
   - Abstrak Bahasa Indonesia (Max 250 kata, 4–6 kata kunci, Lampiran 11a).
   - Abstract Bahasa Inggris (Max 250 kata, 4–6 keywords, Lampiran 11b).
   - Kata Pengantar & Daftar Isi / Tabel / Gambar (Lampiran 12 & 13).
2. **BAB I: Pendahuluan**:
   - Latar Belakang: Urgensi mesin pencari vertikal untuk gadget dan perbandingan pencarian leksikal vs semantik.
   - Rumusan Masalah, Maksud dan Tujuan, serta Manfaat Penelitian.
3. **BAB II: Tinjauan Kepustakaan**:
   - Dasar teori Information Retrieval, Preprocessing Bahasa Indonesia, Sastrawi Stemmer.
   - Formulasi matematis Okapi BM25 dan arsitektur Sentence-BERT / Dense Semantic Retrieval.
   - Metrik evaluasi IR: Precision, Recall, F1-Score, dan Mean Average Precision (MAP).
4. **BAB III: Metode Penelitian**:
   - Waktu & Lingkungan Implementasi (Docker, Python FastAPI, React).
   - Arsitektur sistem dan diagram alir data (*crawling* $\rightarrow$ *preprocessing* $\rightarrow$ *indexing* $\rightarrow$ *retrieval* $\rightarrow$ *evaluation*).
   - Spesifikasi korpus dan pembentukan *ground truth*.
5. **BAB IV: Hasil dan Pembahasan**:
   - Analisis karakteristik korpus gadget (distribusi kata, rata-rata panjang dokumen).
   - Uji coba kueri spesifik vs konseptual (analisis *Side-by-Side*).
   - Tabel perbandingan kuantitatif dan grafik performa (BM25 vs S-BERT).
   - Pembahasan kelebihan dan kelemahan masing-masing algoritma.
6. **BAB V: Kesimpulan dan Saran**:
   - Rekomendasi penggunaan algoritma berdasarkan jenis kebutuhan kueri pengguna.
7. **Lampiran & Kontribusi Anggota (Wajib Poin 8 Petunjuk Dosen)**:
   - Tabel kontribusi spesifik per anggota dengan rincian persentase dan tanggung jawab nyata.

### 6.2 5-Minute Live Demo & YouTube Video Execution Plan
- **Minute 0:00–1:00 (Intro & Background)**: Member 3 explains problem context, corpus crawling results ($\ge 300$ gadget reviews), and system architecture.
- **Minute 1:00–3:00 (Live Search & Algorithmic Comparison)**: Member 2 (Fadhlur) demonstrates the system via Docker, runs exact technical queries (highlighting BM25 accuracy) followed by semantic intent queries (highlighting Sentence-BERT contextual understanding).
- **Minute 3:00–4:15 (Interactive Evaluation Dashboard)**: Member 1 presents the Evaluation Dashboard in the UI, reviewing Precision@K, Recall@K, and MAP charts.
- **Minute 4:15–5:00 (Conclusion & Q&A Readiness)**: Summarize findings and conclude within the allocated 5 minutes.

---

## 7. Spec Self-Review Checklist
- [x] **Placeholders**: No TBDs, unassigned roles, or vague metrics.
- [x] **Internal Consistency**: Docker architecture aligns with FastAPI backend, React frontend, and SQLite/NumPy data layer.
- [x] **Scope**: Clearly focused on 300+ Indonesian gadget corpus, BM25 vs S-BERT comparison, and USK FMIPA reporting standards.
- [x] **Ambiguity Check**: Role assignments, tech stack, formulas, and repository layout are fully defined.

