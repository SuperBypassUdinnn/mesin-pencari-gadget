# Indonesian Gadget Vertical Search Engine (Mesin Pencari Gadget)

A modern, containerized vertical search engine for Indonesian gadget reviews and technical specifications, comparing traditional probabilistic lexical retrieval (**Okapi BM25**) and dense neural semantic retrieval (**Sentence-BERT**).

Developed for the **Penelusuran Informasi (Information Retrieval) 2025/2026** course at **Universitas Syiah Kuala (USK) - FMIPA**.

---

## Architecture Overview

```
[ User / Evaluator ]
        │
        ▼ (Port 3000 / 80)
┌─────────────────────────────────────────────────────────────┐
│ Docker Environment (docker compose up --build)             │
│                                                             │
│  ┌───────────────────────┐       ┌───────────────────────┐  │
│  │     Frontend Web      │       │      Backend API      │  │
│  │   (React + Vite +     │──────▶│   (Python FastAPI)    │  │
│  │    Tailwind CSS)      │ REST  │                       │  │
│  └───────────────────────┘       └───────────┬───────────┘  │
│                                              │              │
│                                  ┌───────────▼───────────┐  │
│                                  │     Storage Layer     │  │
│                                  │ - SQLite (gadget.db)  │  │
│                                  │ - Inverted Index JSON │  │
│                                  │ - S-BERT Embeddings   │  │
│                                  └───────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

- **Frontend**: React 18, Vite, Tailwind CSS, Lucide Icons, Recharts. Features Split View (BM25 vs S-BERT), quick suggestion pills, source portal badges, and an interactive evaluation dashboard.
- **Backend**: FastAPI, Uvicorn, PySastrawi, Sentence-Transformers, NumPy. Provides high-throughput, low-latency REST endpoints.
- **Corpus & Data Layer**: Multi-source Indonesian gadget reviews (Gadgetren, Jagat Review, Droidlime) stored in SQLite (`data/gadget.db`).
- **Core Algorithms**:
  - **Okapi BM25**: Custom Inverted Index, Robertson-Spärck Jones IDF smoothing ($k_1=1.5, b=0.75$).
  - **Sentence-BERT**: Multilingual dense semantic embeddings (`paraphrase-multilingual-MiniLM-L12-v2`) with Cosine Similarity vector search.
- **Evaluation Engine**: Automated benchmark computing Precision@K, Recall@K, F1@K, Mean Average Precision (MAP), and execution latency across 12 annotated test queries.

---

## Quickstart (Single Command with Docker)

To run the entire system (Frontend + Backend + Indexed Data):

```bash
docker compose up --build
```

- **Web Application**: Open [http://localhost:3000](http://localhost:3000)
- **FastAPI Documentation**: Open [http://localhost:8000/docs](http://localhost:8000/docs)
- **API Health Check**: Open [http://localhost:8000/api/health](http://localhost:8000/api/health)

---

## Local Development (Without Docker)

### 1. Prerequisites
- Python 3.11+
- Node.js 18+ & npm

### 2. Backend Setup
```bash
# Install Python dependencies
pip install -r backend/requirements.txt

# Run offline indexing (builds Inverted Index & S-BERT embeddings)
python3 -m backend.app.engine.indexer

# Run quantitative evaluation benchmarks
python3 -m backend.app.engine.evaluator

# Start FastAPI backend server
uvicorn backend.app.main:app --reload --port 8000
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
Open [http://localhost:5173](http://localhost:5173) in your browser.

---

## Running Test Suite

Run the complete test suite (155 automated tests):

```bash
PYTHONPATH=. pytest tests/ -v
```

---

## Project Structure & Team Deliverables

- `crawler/`: Multi-source spiders for Gadgetren, Jagat Review, and Droidlime.
- `backend/app/engine/`: Text preprocessor (Sastrawi), BM25 engine, S-BERT engine, evaluator, and indexer.
- `frontend/`: React components, pages (Search, Evaluation Dashboard), and Tailwind styling.
- `data/`: SQLite database (`gadget.db`), processed inverted indices, and ground-truth test queries.
- `evaluation_results/`: Exported metrics summary (`metrics_summary.json`) and per-query benchmarks (`per_query_benchmark.csv`).
- `docs/report/`: USK FMIPA thesis format final report (Bab I–V, Lampiran Kontribusi Anggota).
- `docs/presentation/`: 5-minute live demo script and presentation guide.
- `docs/TEAM_WORKFLOW.md`: Complete task division, Git branching protocol, and artifact archiving standard.
