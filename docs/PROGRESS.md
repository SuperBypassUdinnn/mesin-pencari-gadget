# Living Progress Tracker & Dependency Map

- **Proyek**: Mesin Pencari Ulasan & Spesifikasi Gadget (`mesin-pencari-gadget`)
- **Mata Kuliah**: Penelusuran Informasi (Information Retrieval) 2025/2026
- **Institusi**: FMIPA Universitas Syiah Kuala (USK)
- **Status Terakhir**: Minggu 1 (Fondasi & Algoritma Core Selesai Dibangun)

> **ATURAN WAJIB WORKFLOW**:
> 1. Setiap anggota tim atau AI agent yang menyelesaikan suatu tugas **WAJIB** mencentang checkbox (`- [x]`) pada dokumen ini sebelum membuat Pull Request (PR).
> 2. Jangan ubah status tugas anggota lain tanpa konfirmasi di grup.
> 3. Dokumen ini menjadi acuan utama seluruh tim untuk memantau progres tanpa harus memeriksa seluruh baris kode atau menanyakan satu per satu.

---

## 1. Peta Dependensi: Tugas Paralel vs Tugas Berurutan

Diagram alur berikut menjelaskan mana tugas yang **BISA DIKERJAKAN LANGSUNG (PARALEL)** dan mana yang **HARUS MENUNGGU DEPENDENSI ANGGOTA LAIN (SEKUENSIAL)**:

```
┌────────────────────────────────────────────────────────────────────────┐
│                        FASE 1: PENGERJAAN PARALEL                      │
│                  (Bisa Dikerjakan Bersamaan Tanpa Menunggu)            │
└────────────────────────────────────────────────────────────────────────┘
       │                                │                                │
       ▼                                ▼                                ▼
[MEMBER 1 - FRONTEND]         [MEMBER 2 (FADHLUR) - IR]        [MEMBER 3 - DATA & REPORT]
• Inisialisasi React Vite     • Preprocessor PySastrawi        • Script Scraper Gadgetren
• Mockup Hero Search Bar      • Inverted Index & BM25          • Script Scraper JagatReview
• Desain ResultCard & Badges  • Sentence-BERT Embeddings       • Script Scraper Droidlime
• Desain Modal Specs Drawer   • IREvaluator (P/R/F1/MAP)       • Tulis Draf Laporan BAB I
• Desain Slide PPTX / Canva   • Setup Docker & REST API        • Tulis Draf Laporan BAB II
       │                                │                                │
       └────────────────┬───────────────┴────────────────┬───────────────┘
                        │                                │
                        ▼                                ▼
┌────────────────────────────────────────────────────────────────────────┐
│                      FASE 2: INTEGRASI & DEPENDENSI                    │
│                      (Wajib Menunggu Pekerjaan Terkait)                │
└────────────────────────────────────────────────────────────────────────┘
  Jalur Integrasi A (Data ➔ Core Indexing):
  [Member 3 Scrape ≥700 Artikel] ──────────────▶ [Member 2 Jalankan 'make index']
                                                           │
  Jalur Integrasi B (Backend ➔ Frontend Live Search):      │
  [Member 2 FastAPI Search Endpoints Siap] ────▶ [Member 1 Hubungkan API Live]
                                                           │
  Jalur Integrasi C (Ground Truth ➔ Benchmarking):         │
  [Semua Anggota Sepakati 12 Kueri Uji] ────────▶ [Member 2 Jalankan 'make eval']
                                                           │
                                                           ▼
┌────────────────────────────────────────────────────────────────────────┐
│                        FASE 3: FINALISASI & LUARAN                     │
│                        (Semua Komponen Terhubung)                      │
└────────────────────────────────────────────────────────────────────────┘
  Jalur Laporan & Evaluasi Dashboard:
  [Hasil Evaluasi 'metrics_summary.json'] ────┬─▶ [Member 1: Dashboard Recharts UI]
                                              └─▶ [Member 3: Tulis Laporan BAB IV & V]

  Jalur Video Presentasi & Demo 5 Menit:
  [Docker 'make up' Running] ───────────────────▶ [Semua Anggota Rekam Video YouTube]
                                                  [Semua Anggota Latihan Demo 5 Menit]
```

---

## 2. Ringkasan Status Proyek Saat Ini

| Komponen Proyek | Penanggung Jawab | Status | Catatan Dependensi |
| :--- | :--- | :--- | :--- |
| **Arsitektur & Scaffolding** | Tim / Fadhlur | **SELESAI (100%)** | Struktur repo, Dockerfile, requirements, dan Makefile siap |
| **Core IR: Preprocessing Sastrawi** | Member 2 (Fadhlur) | **SELESAI (100%)** | Lulus 15 unit tests, filter stopword & stemmer aktif |
| **Core IR: Inverted Index & BM25** | Member 2 (Fadhlur) | **SELESAI (100%)** | Formula Okapi BM25 murni dari nol ($k_1=1.5, b=0.75$) |
| **Core IR: Sentence-BERT Retrieval** | Member 2 (Fadhlur) | **SELESAI (100%)** | Vektor normalisasi L2 & Cosine Similarity NumPy ($< 1$ ms) |
| **Core IR: Evaluator Engine** | Member 2 (Fadhlur) | **SELESAI (100%)** | Precision@K, Recall@K, F1@K, MAP terverifikasi trec_eval |
| **Backend REST API (FastAPI)** | Member 2 (Fadhlur) | **SELESAI (100%)** | Endpoint `/api/search`, `/api/documents`, `/api/evaluation` siap |
| **Ground Truth (12 Kueri Uji)** | Bersama (M1, M2, M3) | **SELESAI (100%)** | Kueri eksak & semantik tersimpan di `data/ground_truth/` |
| **Benchmark Awal (make eval)** | Member 2 (Fadhlur) | **SELESAI (100%)** | Data metrik tersimpan di `evaluation_results/` |
| **Frontend: Komponen UI & Search** | Member 1 | **SELESAI (100%)** | React 18 + Tailwind, SearchBar, ResultCard, SplitView |
| **Frontend: Dashboard Evaluasi** | Member 1 | **SELESAI (100%)** | Halaman Evaluasi, tabel metrik komparasi, grafik Recharts |
| **Scraper Multi-Sumber (Crawling)** | Member 3 | **FONDASI SIAP** | Spider Gadgetren, JagatReview, Droidlime siap dijalankan |
| **Koleksi Korpus $\ge 700$ Dokumen** | Member 3 | **DALAM PROSES** | Target: 350 Gadgetren + 350 Jagat Review + 100 Droidlime |
| **Naskah Laporan USK (Bab I - V)** | Member 3 Lead | **DRAF SIAP** | Format TA FMIPA USK, Lampiran Kontribusi Anggota siap |
| **Video Presentasi YouTube** | Bersama (M1, M2, M3) | **MENUNGGU** | Menunggu penyelesaian scraping korpus penuh |

---

## 3. Checklist Detail per Anggota Tim

### Anggota 1: Frontend & UI Lead
*Workspace: `frontend/`*
*Tugas Mandiri / Paralel:*
- [x] Inisialisasi React + Vite + Tailwind CSS (`frontend/`)
- [x] Pembuatan komponen `Navbar.jsx` (navigasi tab Pencarian vs Evaluasi)
- [x] Pembuatan komponen `SearchBar.jsx` dengan 3 tombol pill saran kueri cepat
- [x] Pembuatan komponen `ResultCard.jsx` dengan badge sumber (`[Gadgetren]`, `[Jagat Review]`, `[Droidlime]`)
- [x] Pembuatan tampilan `SplitView.jsx` (komparasi berdampingan BM25 vs S-BERT)
- [x] Pembuatan modal drawer `SpecsModal.jsx` untuk spesifikasi teknis lengkap
- [x] Desain halaman `EvaluationDashboard.jsx` (tabel metrik dan grafik Recharts)
*Tugas Integrasi:*
- [x] Sambungkan `frontend/src/services/api.js` ke backend FastAPI (`http://localhost:8000/api`)
- [ ] Uji responsivitas UI pada tampilan mobile dan desktop
- [ ] Buat bahan tayang presentasi live demo (Canva / PPTX) mengikuti naskah `docs/presentation/5_MINUTE_DEMO_SCRIPT.md`

---

### Member 2 (Fadhlur): Core IR & Backend Lead
*Workspace: `backend/`, root `docker-compose.yml`, `Makefile`*
*Tugas Mandiri / Paralel:*
- [x] Setup repositori, Makefile, dan konfigurasi Docker Compose (`backend` + `frontend`)
- [x] Implementasi modul preprocessing teks Bahasa Indonesia dengan PySastrawi (`backend/app/engine/preprocessor.py`)
- [x] Implementasi struktur data Inverted Index dan algoritma Okapi BM25 dari nol (`backend/app/engine/bm25.py`)
- [x] Implementasi dense semantic retrieval Sentence-BERT dengan Cosine Similarity NumPy (`backend/app/engine/sbert.py`)
- [x] Implementasi kalkulator metrik evaluasi IR: P@K, R@K, F1@K, MAP, dan latensi (`backend/app/engine/evaluator.py`)
- [x] Implementasi REST API FastAPI dengan CORS dan endpoint lengkap (`backend/app/main.py`)
- [x] Implementasi script offline indexer (`backend/app/engine/indexer.py`)
*Tugas Integrasi:*
- [x] Jalankan baseline benchmark evaluasi dan ekspor `evaluation_results/metrics_summary.json`
- [x] Setup CI/CD GitHub Actions (`.github/workflows/ci.yml`) dan Branch Protection
- [ ] Setelah korpus $\ge 700$ artikel di-scrape oleh Member 3, jalankan kembali `make index` dan `make eval` untuk memproses seluruh data riil
- [ ] Verifikasi kestabilan container `docker compose up --build` sebelum jadwal demo

---

### Anggota 3: Data Engineer & Laporan Lead
*Workspace: `crawler/`, `data/raw/`, `docs/report/`*
*Tugas Mandiri / Paralel:*
- [x] Pembangunan spider crawler modular (`crawler/spiders/gadgetren.py`, `jagatreview.py`, `droidlime.py`)
- [x] Pembangunan database SQLite `data/gadget.db` dan skema tabel dokumen
- [x] Penyusunan draf Laporan Akhir format TA FMIPA USK (Bab I Pendahuluan, Bab II Tinjauan Pustaka)
- [x] Penyusunan draf Bab III Metode Penelitian, Bab IV Hasil & Pembahasan, Bab V Kesimpulan & Saran
- [x] Penyusunan Halaman Judul, Pengesahan, Pernyataan Bebas Plagiasi, Abstrak ID & EN, dan Tabel Kontribusi Anggota
*Tugas Integrasi & Tindak Lanjut:*
- [ ] Jalankan crawler multi-sumber (`python3 -m crawler.main_crawler`) hingga mencapai kuota target $700 - 1.000+$ artikel
- [ ] Pastikan file `data/raw/documents.json` terisi artikel lengkap dengan spesifikasi
- [ ] Hubungi Member 2 (Fadhlur) untuk menjalankan `make index` pada korpus penuh
- [ ] Masukkan tangkapan layar (screenshot) bukti crawling ke folder `docs/screenshots/crawling/`
- [ ] Masukkan grafik evaluasi dari `evaluation_results/charts/` ke Bab IV Laporan
- [ ] Koordinasikan perekaman video presentasi YouTube (alokasi waktu ketiga anggota sesuai `docs/presentation/5_MINUTE_DEMO_SCRIPT.md`)
- [ ] Ekspor Laporan Akhir ke format PDF `Kelompok_X.pdf` untuk dikumpulkan ke e-learning
