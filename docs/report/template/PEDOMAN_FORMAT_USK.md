# Pedoman Format Dokumen Akademik FMIPA Universitas Syiah Kuala (USK)

Dokumen ini merupakan acuan resmi standarisasi penulisan Laporan Tugas Akhir / Proyek Akhir pada Fakultas Matematika dan Ilmu Pengetahuan Alam (FMIPA) Universitas Syiah Kuala, diadopsi dari berkas resmi:
- **File Sumber**: `docs/report/template/template_ta_fmipa_usk_2024.pdf` (Lampiran 7–17 Pedoman Penulisan Tugas Akhir FMIPA USK 2024).

---

## 1. Aturan Tipografi & Tata Letak Halaman (Page Setup)

| Parameter | Ketentuan Baku USK FMIPA |
| :--- | :--- |
| **Kertas** | A4 (210 x 297 mm), 80 gram (untuk naskah fisik) |
| **Margin** | **Kiri**: 4,0 cm (1,57 in)<br>**Atas**: 3,0 cm (1,18 in)<br>**Kanan**: 3,0 cm (1,18 in)<br>**Bawah**: 3,0 cm (1,18 in) |
| **Jenis Huruf** | **Times New Roman** untuk seluruh teks naskah |
| **Spasi Baris** | **1,5 spasi** untuk teks utama badan bab.<br>**1,0 spasi (tunggal)** untuk: Sampul, Judul dalam, Abstrak, Kutipan langsung >4 baris, Judul tabel/gambar, dan Daftar Pustaka. |
| **Ukuran Font Utama** | **12 pt** untuk teks naskah |
| **Paragraf** | Rata kiri-kanan (justified), indentasi baris pertama 1 cm atau 5–7 ketukan |
| **Penomoran Halaman** | **Bagian Awal** (Judul s.d. Daftar Lampiran): Angka Romawi kecil (`i, ii, iii, iv...`), posisi tengah bawah.<br>**Bagian Utama** (Bab I s.d. Lampiran): Angka Arab (`1, 2, 3...`), posisi kanan atas; kecuali halaman judul bab (halaman pertama bab) diletakkan di **tengah bawah**. |

---

## 2. Struktur Dokumen Bagian Awal (Front Matter)

### A. Sampul Depan (Cover Luar) - Lampiran 7
- **Judul**: Times New Roman 18–20 pt, Center, Bold, Huruf Kapital semua (UPPERCASE), 4 spasi dari margin atas.
- **Jenis Dokumen**: `LAPORAN PROYEK AKHIR` / `TUGAS AKHIR`, Times New Roman 16 pt, Center, Bold, UPPERCASE, 3 spasi setelah judul.
- **Teks Tujuan**: *"Diajukan untuk melengkapi tugas-tugas dan memenuhi syarat-syarat guna memperoleh gelar Sarjana Komputer / menyelesaikan mata kuliah Penelusuran Informasi"*, Times New Roman 12 pt, Center.
- **Penyusun**:
  - *"Oleh:"* (Times New Roman 14 pt, Center)
  - **Nama Mahasiswa & NPM**: Times New Roman 14 pt, Center, Bold, UPPERCASE, Underlined.
- **Logo Universitas**: Logo resmi USK, diletakkan tepat di tengah antara nama penyusun dan nama institusi.
- **Institusi**:
  - `PROGRAM STUDI INFORMATIKA JURUSAN ILMU KOMPUTER`
  - `FAKULTAS MATEMATIKA DAN ILMU PENGETAHUAN ALAM`
  - `UNIVERSITAS SYIAH KUALA, BANDA ACEH`
  - `BULAN, TAHUN` (Times New Roman 14 pt, Center, Bold, UPPERCASE, margin bawah).

### B. Halaman Pengesahan - Lampiran 8
- Judul halaman: `PENGESAHAN` (16 pt, Center, Bold, UPPERCASE, 2 spasi dari margin atas).
- Judul Proyek: Bahasa Indonesia (16–18 pt, Center, Bold, UPPERCASE) diikuti Judul Bahasa Inggris (16–18 pt, Center, Bold, UPPERCASE).
- Data Mahasiswa: Nama, NPM, Program Studi (indent 3,5 cm, 12 pt).
- Blok Tanda Tangan:
  - Pembimbing I / Dosen Pengampu Mata Kuliah
  - Pembimbing II (jika ada)
  - Mengetahui: Koordinator Program Studi Informatika & Dekan FMIPA USK.
  - Tanggal kelulusan / pengesahan diletakkan di margin bawah.

### C. Pernyataan Bebas Plagiasi - Lampiran 9
- Judul: `PERNYATAAN BEBAS PLAGIASI` (14 pt, Center, Bold, UPPERCASE).
- Pernyataan bermaterai / bertandatangan di atas nama penyusun bahwa dokumen merupakan karya orisinal mandiri dan bebas plagiasi.

### D. Abstrak (Bahasa Indonesia) - Lampiran 11a
- Judul: `ABSTRAK` (14 pt, Center, Bold, UPPERCASE, 2 spasi dari margin atas).
- Panjang teks: **Maksimum 250 kata**, 1 spasi tunggal, justified, memuat: latar belakang/tujuan, metode, hasil utama, dan simpulan.
- **Kata kunci**: 4–6 kata/frasa signifikan, dipisahkan koma, italic.

### E. Abstract (Bahasa Inggris) - Lampiran 11b
- Judul: `ABSTRACT` (14 pt, Center, Bold, UPPERCASE).
- Panjang teks: **Maksimum 250 kata**, 1 spasi tunggal, justified, italic.
- **Keywords**: 4–6 kata kunci berbahasa Inggris.

### F. Kata Pengantar - Lampiran 12
- Puji syukur, selawat, konteks proyek, ucapan terima kasih kepada Dekan, Ketua Jurusan/Departemen, Koordinator Prodi, Dosen Pengampu, rekan tim, dan orang tua.

### G. Daftar Isi, Daftar Tabel, Daftar Gambar - Lampiran 13
- Format penulisan titik-titik (dot leader) dengan nomor halaman rata kanan.

---

## 3. Sistematika Bagian Utama (Body Chapters)

Setiap bab dimulai pada halaman baru (Page Break):
1. **BAB I PENDAHULUAN**
   - 1.1 Latar Belakang
   - 1.2 Rumusan Masalah
   - 1.3 Maksud dan Tujuan
   - 1.4 Manfaat Penelitian
2. **BAB II TINJAUAN KEPUSTAKAAN**
   - Teori penelusuran informasi, prapemrosesan teks Sastrawi, pembobotan TF-IDF, Okapi BM25, representasi vektor Sentence-BERT, dan metrik evaluasi trec_eval (P@K, R@K, F1@K, MAP).
3. **BAB III METODE PENELITIAN**
   - 3.1 Arsitektur Sistem
   - 3.2 Pengumpulan Korpus (Crawling multi-portal)
   - 3.3 Prapemrosesan Teks & Normalisasi
   - 3.4 Pembangunan Indeks (Inverted Index & S-BERT Matrix)
   - 3.5 Protokol Evaluasi & Ground Truth (TREC-style pooling 15 kueri)
4. **BAB IV HASIL DAN PEMBAHASAN**
   - 4.1 Karakteristik Korpus Data (Distribusi portal, Zipf's Law)
   - 4.2 Analisis Hasil Pencarian (Kueri teknis vs kueri polisemi semantik)
   - 4.3 Evaluasi Kuantitatif Komparatif (Tabel metrik & latensi)
   - 4.4 Pembahasan Trade-off & Limitasi S-BERT
5. **BAB V KESIMPULAN DAN SARAN**
   - 5.1 Kesimpulan
   - 5.2 Saran (Pengembangan hybrid retriever, caching, model reranking)
6. **DAFTAR PUSTAKA**
   - Standar sitasi APA 7th Edition alfabetis, seluruh entri wajib dikutip dalam naskah bab (1:1 parity).
7. **LAMPIRAN**
   - Lampiran 1: Matriks Kontribusi Anggota Tim
   - Lampiran 2: Ground Truth Kueri Uji (q01–q15)

---

## 4. Referensi dan Integritas

Berkas template PDF asli tersimpan secara permanen di repositori pada lokasi:
`docs/report/template/template_ta_fmipa_usk_2024.pdf`

Setiap anggota tim dan AI agent wajib mengacu pada template ini saat memperbarui atau meregenerasi laporan proyek akhir via:
```bash
make report
# atau
python3 -m crawler.build_report_pdf
```
