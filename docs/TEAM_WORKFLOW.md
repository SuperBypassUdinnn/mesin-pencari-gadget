# Team Task Distribution & Collaboration Workflow

- **Course**: Penelusuran Informasi (Information Retrieval)
- **Institution**: Universitas Syiah Kuala (USK) - FMIPA
- **Project**: Indonesian Gadget Vertical Search Engine (`mesin-pencari-gadget`)
- **Team Size**: 3 Members

---

## 1. Overview & Work Allocation Philosophy

To ensure balanced accountability, clear individual ownership, and seamless GitHub collaboration without merge conflicts, the project is strictly decomposed into three specialized roles. Each member owns a dedicated directory and distinct deliverables required for the final evaluation, report, and video presentation.

```
┌───────────────────────────────────────────────────────────────────────────┐
│                               TEAM ROLES                                  │
├──────────────────────┬────────────────────────────┬───────────────────────┤
│   MEMBER 1           │   MEMBER 2 (Fadhlur)       │   MEMBER 3            │
│   Frontend & UI Lead │   Core IR & Backend Lead   │   Data & Report Lead  │
├──────────────────────┼────────────────────────────┼───────────────────────┤
│ • React + Vite UI    │ • Preprocessing (Sastrawi) │ • Multi-source Spiders│
│ • Side-by-Side View  │ • Inverted Index & BM25    │ • 700-1000 Docs Crawl │
│ • Evaluation Charts  │ • Sentence-BERT Embeddings │ • Ground Truth Label  │
│ • Specs Modal Drawer │ • MAP / P / R / F1 Engine  │ • USK TA Report (I-V) │
│ • Demo Slides Deck   │ • FastAPI & Docker Compose │ • YouTube Video Coord │
│                      │                            │                       │
│ Workspace:           │ Workspace:                 │ Workspace:            │
│ `frontend/`          │ `backend/`                 │ `crawler/` & `docs/`  │
└──────────────────────┴────────────────────────────┴───────────────────────┘
```

## 2. Detailed Member Responsibilities

### Member 1: Frontend Engineer & UI Lead
- **Primary Objective**: Build an intuitive, responsive consumer web application that highlights the side-by-side performance of both IR algorithms, presents structured gadget specifications, and renders evaluation graphs.
- **Dedicated Workspace**: `frontend/`
- **Tech Stack**: React (Vite), Tailwind CSS, Lucide Icons, Recharts / Chart.js.
- **Key Tasks**:
  1. Initialize React + Tailwind layout with a clean search engine aesthetic (dark/light mode).
  2. Implement Hero Search Bar with quick-suggestion pills (e.g., *"HP Kamera Low-light"*, *"Laptop Coding 10 Jutaan"*).
  3. Develop the **Side-by-Side Split View** comparing Okapi BM25 (left) vs Sentence-BERT (right), showing rank, similarity score, execution latency (ms), and portal source badge (`[Gadgetren]`, `[Jagat Review]`, `[Droidlime]`).
  4. Implement keyword snippet highlighting and a modal drawer for full gadget specifications.
  5. Build the **Interactive Evaluation Dashboard** page displaying comparative bar/radar charts and metrics tables (Precision@5, Precision@10, Recall, F1, MAP).
  6. Design the 5-minute presentation slideshow deck (Canva or PowerPoint).

### Member 2 (Fadhlur): Core IR Engineer & Backend Lead
- **Primary Objective**: Build the mathematical search engine algorithms, data preprocessing pipeline, vector embeddings, quantitative evaluation benchmark, and orchestrate Docker Compose.
- **Dedicated Workspace**: `backend/` and root `docker-compose.yml`
- **Tech Stack**: Python 3.11+, FastAPI, Uvicorn, PySastrawi, Sentence-Transformers (`paraphrase-multilingual-MiniLM-L12-v2`), NumPy, SQLite.
- **Key Tasks**:
  1. Build the Indonesian NLP Preprocessing pipeline (`clean_text`, `tokenize`, `remove_stopwords`, and PySastrawi `stem_tokens`).
  2. Implement the **Inverted Index** data structure and Robertson-Spärck Jones **Okapi BM25** ranking algorithm ($k_1=1.5, b=0.75$).
  3. Implement **Sentence-BERT dense semantic retrieval** via normalized vector matrix dot-product Cosine Similarity.
  4. Build the **Evaluation Engine** calculating Precision@K, Recall@K, F1@K, Mean Average Precision (MAP), and execution latencies across 10–15 test queries.
  5. Expose REST endpoints (`/api/search`, `/api/documents/{id}`, `/api/evaluation`).
  6. Package the complete system into `docker-compose.yml` for 1-command execution.

### Member 3: Data Engineer & Report Lead
- **Primary Objective**: Crawl and clean a diverse multi-source corpus of $700 - 1.000+$ gadget reviews, coordinate evaluation query labeling, lead the authoring of the USK FMIPA final report, and manage YouTube demo production.
- **Dedicated Workspace**: `crawler/`, `data/raw/`, and `docs/report/`
- **Tech Stack**: Python (`requests`, `beautifulsoup4`), SQLite, Markdown / LaTeX / Microsoft Word.
- **Key Tasks**:
  1. Develop modular scrapers for Gadgetren, Jagat Review, and Droidlime, extracting titles, URLs, categories, dates, specifications, and full text into `data/raw/documents.json`.
  2. Ingest corpus into SQLite database (`data/gadget.db`).
  3. Lead the compilation of 10–15 standard test queries and annotate binary relevance judgments (`data/ground_truth/relevance_judgments.json`) with team members.
  4. Author the Final Academic Report adhering to USK FMIPA thesis format:
     - Front Matter (Judul, Pengesahan, Bebas Plagiasi, Abstrak ID & EN, Kata Pengantar, Daftar Isi/Tabel/Gambar).
     - Bab I: Pendahuluan.
     - Bab II: Tinjauan Kepustakaan.
     - Bab III: Metode Penelitian.
     - Bab IV: Hasil dan Pembahasan (Corpus characteristics, Zipf distribution, algorithm comparison, evaluation tables).
     - Bab V: Kesimpulan dan Saran.
     - Lampiran: **Individual Contribution Table** (Mandatory Requirement 8).
  5. Coordinate scriptwriting and video editing for the YouTube presentation (ensuring all 3 members speak).

## 3. Git Branching Strategy & Coordination Protocol

To avoid merge conflicts, each member works on dedicated git branches corresponding to their directory ownership.

```
main (Production-ready & demo branch)
  ▲
  │ Pull Request (Review & Merge)
  ├── feature/frontend-ui       ──▶ Owned by Member 1 (Touches `frontend/`)
  ├── feature/core-ir-engine    ──▶ Owned by Member 2 (Touches `backend/`)
  ├── feature/crawler-data      ──▶ Owned by Member 3 (Touches `crawler/` & `data/`)
  └── docs/academic-report      ──▶ Owned by Member 3 & Collaborators (`docs/`)
```

### Git Collaboration Rules:
1. **Never commit directly to `main`**: All features must be developed on the respective feature branch.
2. **Directory Isolation**:
   - Member 1 only modifies `frontend/`.
   - Member 2 (Fadhlur) only modifies `backend/` and root configuration.
   - Member 3 only modifies `crawler/`, `data/raw/`, and `docs/report/`.
3. **Mandatory Progress Update**:
   - Before opening a Pull Request, the author **MUST** update `docs/PROGRESS.md` to check off completed items (`- [x]`) and record current status so all team members stay synchronized without needing to ask.
4. **Mandatory Pre-PR Pipeline Verification**:
   - Before opening a Pull Request, the author **MUST** run the automated verification script:
     ```bash
     python3 scripts/verify_pipeline.py
     ```
     or `make verify`. All 7 quality gates must report `[PASS]` before requesting review.
5. **Pull Request Protocol**:
   - Open a Pull Request on GitHub from your feature branch to `main`.
   - At least one other team member must review and approve the PR.
   - GitHub Actions CI/CD tests must pass automatically.
6. **Mandatory GitHub Issue Reference**:
   - Every Pull Request description **MUST** explicitly link to the corresponding milestone issue using standard GitHub keywords (e.g. `Closes #1`, `Closes #3`, `Closes #5`).
   - A PR submitted without an associated issue link will **NOT** be approved or merged. This ensures 100% digital traceability of individual contributions for academic grading.

### Issue Management Protocol for New Tasks & Bugfixes:
Whenever new requirements, bugfixes, or additional features arise outside the initial 7 milestone issues:
1. **Create Issue First**: Never develop or submit a PR without a tracking issue. Create the issue via `ghx`:
   ```bash
   ghx issue create \
     --title "[<Category>] <Clear Title>" \
     --label "<category-label>,<type-label>" \
     --body "### Penanggung Jawab: ...\n**Branch**: ...\n#### Deskripsi Tugas:\n- [ ] ...\n#### Kriteria Sukses:\n- Lulus 'make verify'"
   ```
   Valid Categories: `[Frontend]`, `[Core IR]`, `[Data]`, `[Report]`, `[Demo]`, `[Bugfix]`.
   Valid Labels: `frontend`, `core-ir`, `crawler-data`, `report`, `demo`, `enhancement`, `bug`, `documentation`.
2. **Register in Progress Tracker**: Add the newly created issue number and task checklist into `docs/PROGRESS.md`.
3. **Closing Explanatory Comments**: When resolving an issue, always close with a descriptive comment explaining what was implemented and verified.

---

## 4. Evidence & Artifact Archiving Standard

The assignment guidelines award points for documented proof of execution, aesthetic quality, and rigorous reporting. All raw artifacts must be saved directly to the repository:

1. **Crawler Proofs (`docs/screenshots/crawling/`)**:
   - Terminal logs showing 700–1000 articles crawled.
   - Sample raw JSON and SQLite database schema viewer.
2. **Core IR Proofs (`docs/screenshots/core_ir/`)**:
   - Execution logs of offline indexing (vocabulary size, token counts).
   - Inverted index JSON sample and embedding matrix dimensions.
   - Unit test pass outputs (`pytest`).
3. **UI Demonstration Proofs (`docs/screenshots/ui/`)**:
   - Full-page capture of Hero Search Bar.
   - Side-by-Side comparison on specific technical queries vs semantic queries.
   - Modal drawer showing full technical specs.
   - Evaluation Dashboard showing metrics tables and Recharts visual graphs.
4. **Evaluation Outputs (`evaluation_results/`)**:
   - `metrics_summary.json`: Exported numerical metrics for both BM25 and S-BERT.
   - `charts/`: High-resolution PNG graphs of Precision@K, Recall@K, MAP, and latency for direct inclusion in the report and slide deck.
5. **Presentation & Submission (`docs/presentation/`)**:
   - PDF/PPTX slide deck.
   - YouTube video link and video transcript/script.

---

## 5. Synchronized 3-Week Timeline

```
Week 1: Foundations
[M3] Crawl 700-1000 Articles ────▶ [M2] SQLite Setup & Preprocessor ────▶ [M1] React Wireframes

Week 2: Core Development & Integration
[M2] BM25 & S-BERT Engine ───────▶ [M2] FastAPI Endpoints ──────────────▶ [M1] Connect UI Side-by-Side
                                       ▲
[M3 + Team] Ground Truth Queries ──────┘

Week 3: Final Delivery
[M1] Polish UI & Slide Deck ─────▶ [M2] Dockerize & Benchmark ──────────▶ [M3] Finalize USK Report PDF
[All] Record YouTube Presentation Video (All members speak)
```
