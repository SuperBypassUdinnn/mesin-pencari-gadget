---
name: gadget-search-workflow
description: End-to-end guidance for the Indonesian Gadget Vertical Search Engine (multi-source crawling, Okapi BM25 vs Sentence-BERT, React split-view UI, USK FMIPA thesis reporting, and pre-flight quality verification).
---

# Gadget Search Workflow — Team & Agent Guide

This skill directs AI agents and team members working on the **Indonesian Gadget Vertical Search Engine** (`mesin-pencari-gadget`) for the Penelusuran Informasi (Information Retrieval) course at FMIPA Universitas Syiah Kuala.

---

## Trigger Keywords

`gadget search`, `mesin pencari`, `crawling`, `gadgetren`, `jagat review`, `droidlime`, `bm25`, `sentence-bert`, `sbert`, `evaluator`, `map`, `precision`, `laporan usk`, `verify pipeline`

---

## 1. Team Role Allocation & Workspaces

Before starting any task, determine which member is being assisted:

| Member | Primary Role | Designated Workspace | Dedicated Git Branch | Key Deliverables |
| :--- | :--- | :--- | :--- | :--- |
| **Member 1** | Frontend & UI Lead | `frontend/` | `feature/frontend-ui` | React 18, Tailwind, SplitView (BM25 vs S-BERT), SpecsModal, Evaluation Dashboard, presentation slides |
| **Member 2 (Fadhlur)** | Core IR & Backend Lead | `backend/`<br>`docker-compose.yml` | `feature/core-ir-engine` | Preprocessing PySastrawi, Inverted Index & Okapi BM25, Sentence-BERT, Evaluator (MAP/P/R/F1), FastAPI, Docker |
| **Member 3** | Data Engineering & Report Lead | `crawler/`<br>`data/raw/`<br>`docs/report/` | `feature/crawler-data`<br>`docs/academic-report` | Modular scrapers ($700 - 1.000+$ articles), SQLite ingestion, ground-truth queries, USK FMIPA Report Bab I–V |

---

## 2. Parallel vs Sequential Dependency Rules

To prevent workflow bottlenecks:

### Tasks that can be worked on IMMEDIATELY in PARALLEL:
- **Member 1**: Wireframe and style React components using mock data in `frontend/`. Design presentation slide deck.
- **Member 2 (Fadhlur)**: Develop, optimize, and test core algorithmic math (BM25 formulas, S-BERT matrix multiplication, evaluation metrics).
- **Member 3**: Implement web scraping spiders in `crawler/spiders/` and write Bab I & Bab II of the academic report.

### Tasks that have SEQUENTIAL DEPENDENCIES:
1. **Full Offline Indexing**: Member 2 runs `python3 -m backend.app.engine.indexer` or `make index` **after** Member 3 scrapes $\ge 700$ articles to `data/raw/documents.json`.
2. **Frontend Live Integration**: Member 1 connects `frontend/src/services/api.js` to live search **after** Member 2's FastAPI endpoints are verified.
3. **Full Benchmark Reporting**: Member 3 writes Bab IV (Hasil & Pembahasan) **after** Member 2 runs `make eval` and produces `evaluation_results/metrics_summary.json`.
4. **YouTube Video & Live Demo**: All members record segments **after** Docker Compose runs cleanly end-to-end.

Consult `docs/PROGRESS.md` for live dependency blockers!

---

## 3. Workflow Steps for Agents

### Step 1: Pre-Flight Context Check
1. Read `docs/PROGRESS.md` to see which tasks are completed and which are pending.
2. Ensure working directory matches the active member's workspace.
3. Confirm git branch is NOT `main` (use `feature/frontend-ui`, `feature/core-ir-engine`, `feature/crawler-data`, or `docs/academic-report`).

### Step 2: Implementation & TDD
- Always follow Test-Driven Development (TDD): write unit tests in `tests/`, watch them fail, implement minimal code, verify green.
- Respect Clean Text policy: ZERO decorative pictographic emojis in code or docs.

### Step 3: Pre-PR Quality Verification (Mandatory Gate)
Before suggesting or opening a Pull Request, run:
```bash
python3 scripts/verify_pipeline.py
```
or
```bash
make verify
```
All 7 quality gates must pass:
- Gate 1: Directory & Scaffolding Hygiene
- Gate 2: Data Layer & Ground Truth Integrity
- Gate 3: Offline Index Verification
- Gate 4: Academic Report Completeness (USK FMIPA format)
- Gate 5: Living Progress Tracker & Workflow Parity (`docs/PROGRESS.md`)
- Gate 6: Clean Text Policy Audit
- Gate 7: Automated Pytest Regression Test Suite (155+ tests)

### Step 4: Update Progress Checklist
Open `docs/PROGRESS.md`, check off completed items (`- [x]`), and update milestone status.

### Step 5: Pull Request & Mandatory Issue Linking
Commit changes with concise Conventional Commits (`feat: ...`, `fix: ...`, `docs: ...`) and create a Pull Request targeting `main`.
**MANDATORY**: Every PR description MUST explicitly reference the associated milestone issue using standard closing keywords (e.g. `Closes #1` or `Closes #2` for Frontend, `Closes #3` or `Closes #4` for Core IR, `Closes #5` or `Closes #6` for Crawler/Report, `Closes #7` for Demo/Delivery). Never submit or approve a PR without linking to an issue.

---

## 4. Issue Creation Protocol for Additional Tasks & Bugfixes

If unexpected bugs, additional tasks, or scope extensions arise:
1. **Never commit without an Issue**: Create an issue first using `ghx issue create`:
   ```bash
   ghx issue create \
     --title "[<Category>] <Clear Title>" \
     --label "<category-label>,<type-label>" \
     --body "### Penanggung Jawab: ...\n**Branch**: ...\n#### Deskripsi Tugas:\n- [ ] ...\n#### Kriteria Sukses:\n- Lulus 'make verify'"
   ```
   Valid categories: `[Frontend]`, `[Core IR]`, `[Data]`, `[Report]`, `[Demo]`, `[Bugfix]`.
2. **Register in `docs/PROGRESS.md`**: Append the newly created issue number and task items to the living tracker.
3. **Closing Explanatory Comments**: When resolving or closing an issue, always provide an explanatory comment detailing what was accomplished and verified.
