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

## 2. Ringkasan Status Proyek & GitHub Issues Mapping

| Komponen Proyek & GitHub Issue | Penanggung Jawab | Status | Catatan Dependensi |
| :--- | :--- | :--- | :--- |
| **Arsitektur & Scaffolding** | Tim / Fadhlur | **SELESAI (100%)** | Struktur repo, Dockerfile, requirements, dan Makefile siap |
| **[#3] Core IR: Preprocessing Sastrawi & BM25** | Member 2 (Fadhlur) | **CLOSED (100%)** | Lulus 155 unit tests, formula Okapi BM25 murni ([Issue #3](https://github.com/SuperBypassUdinnn/mesin-pencari-gadget/issues/3)) |
| **[#4] Core IR: S-BERT & FastAPI REST API** | Member 2 (Fadhlur) | **CLOSED (100%)** | S-BERT cosine similarity, Evaluator, FastAPI, Docker ([Issue #4](https://github.com/SuperBypassUdinnn/mesin-pencari-gadget/issues/4)) |
| **[#1] Frontend: Komponen UI & Search** | Member 1 | **OPEN (90%)** | React 18, SearchBar, ResultCard, SplitView, Vitest ([Issue #1](https://github.com/SuperBypassUdinnn/mesin-pencari-gadget/issues/1)) |
| **[#2] Frontend: Dashboard Evaluasi & Slides** | Member 1 | **OPEN (75%)** | Dashboard Recharts siap, slide demo in progress ([Issue #2](https://github.com/SuperBypassUdinnn/mesin-pencari-gadget/issues/2)) |
| **[#5] Scraper Multi-Sumber (700+ Dokumen)** | Member 3 | **OPEN (30%)** | Spider siap, crawling korpus penuh in progress ([Issue #5](https://github.com/SuperBypassUdinnn/mesin-pencari-gadget/issues/5)) |
| **[#6] Naskah Laporan USK FMIPA (Bab I-V)** | Member 3 Lead | **OPEN (60%)** | Bab I–III siap, Bab IV–V menunggu evaluasi korpus penuh ([Issue #6](https://github.com/SuperBypassUdinnn/mesin-pencari-gadget/issues/6)) |
| **[#7] Demo 5 Menit, Video, & Delivery** | Bersama (M1, M2, M3) | **OPEN (10%)** | Menunggu korpus penuh & perekaman video YouTube ([Issue #7](https://github.com/SuperBypassUdinnn/mesin-pencari-gadget/issues/7)) |

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
