# Halaman Judul dan Pengesahan

## Sampul

LAPORAN PROYEK AKHIR MATA KULIAH PENELUSURAN INFORMASI

PEMBUATAN MESIN PENCARI VERTIKAL ULASAN & SPESIFIKASI GADGET DENGAN ALGORITMA OKAPI BM25 DAN SENTENCE-BERT PADA KORPUS TEKS BAHASA INDONESIA

Disusun oleh:
Kelompok 4

1. [Nama Anggota 1] (NPM. [NPM])
2. Fadhlurrahman Alaudin (NPM. [NPM])
3. Khalish (NPM. [NPM])

Dosen Pengampu Mata Kuliah:
[Nama Dosen Pengampu Mata Kuliah], [Gelar]
NIP. [NIP Dosen]

PROGRAM STUDI INFORMATIKA
FAKULTAS MATEMATIKA DAN ILMU PENGETAHUAN ALAM
UNIVERSITAS SYIAH KUALA
BANDA ACEH
2026

---

## Halaman Judul

LAPORAN PROYEK AKHIR MATA KULIAH PENELUSURAN INFORMASI

PEMBUATAN MESIN PENCARI VERTIKAL ULASAN & SPESIFIKASI GADGET DENGAN ALGORITMA OKAPI BM25 DAN SENTENCE-BERT PADA KORPUS TEKS BAHASA INDONESIA

Diajukan sebagai salah satu syarat penilaian kelulusan pada Mata Kuliah Penelusuran Informasi (Information Retrieval) Semester Genap Tahun Akademik 2025/2026

Disusun oleh:
Kelompok 4

1. [Nama Anggota 1] (NPM. [NPM])
2. Fadhlurrahman Alaudin (NPM. [NPM])
3. Khalish (NPM. [NPM])

PROGRAM STUDI INFORMATIKA
FAKULTAS MATEMATIKA DAN ILMU PENGETAHUAN ALAM
UNIVERSITAS SYIAH KUALA
BANDA ACEH
2026

---

## Lembar Pengesahan

LEMBAR PENGESAHAN LAPORAN PROYEK AKHIR MATA KULIAH

Judul Proyek: Pembuatan Mesin Pencari Vertikal Ulasan & Spesifikasi Gadget dengan Algoritma Okapi BM25 dan Sentence-BERT pada Korpus Teks Bahasa Indonesia
Mata Kuliah: Penelusuran Informasi (Information Retrieval)
Kelompok: 4

Anggota Tim:
1. Nama: [Nama Anggota 1] | NPM: [NPM] | Peran: Frontend & UI Lead
2. Nama: Fadhlurrahman Alaudin | NPM: [NPM] | Peran: Core IR & Backend Lead
3. Nama: Khalish | NPM: [NPM] | Peran: Data Engineering & Report Lead

Laporan Proyek Akhir ini telah diperiksa, diuji melalui live demo sistem, dan disetujui untuk memenuhi penilaian akhir mata kuliah Penelusuran Informasi.

Banda Aceh, November 2026

Menyetujui,
Dosen Pengampu Mata Kuliah Penelusuran Informasi

( [Nama Dosen Pengampu Mata Kuliah], [Gelar] )
NIP. [NIP Dosen]

---

## Pernyataan Bebas Plagiasi

Kami yang bertanda tangan di bawah ini menyatakan dengan sesungguhnya bahwa Laporan Proyek Akhir Mata Kuliah Penelusuran Informasi dengan judul di atas adalah hasil karya orisinal kelompok kami sendiri. Seluruh data korpus teks hasil crawling, implementasi kode algoritma Okapi BM25 dan Sentence-BERT, antarmuka web, serta analisis evaluasi metrik (MAP, Precision, Recall, F1) yang dipaparkan dalam laporan ini dikerjakan secara mandiri dan bebas dari tindakan plagiasi. Semua referensi dan kepustakaan yang dirujuk telah dicantumkan secara tertib pada Daftar Pustaka.

Banda Aceh, November 2026

Tim Penyusun (Kelompok 4):

1. [Nama Anggota 1] (NPM. [NPM]) ........................
2. Fadhlurrahman Alaudin (NPM. [NPM]) ........................
3. Khalish (NPM. [NPM]) ........................

---

## Kata Pengantar

Puji syukur kami panjatkan ke hadirat Allah SWT atas rahmat dan hidayah-Nya, sehingga Laporan Proyek Akhir Mata Kuliah Penelusuran Informasi (Information Retrieval) yang berjudul "Pembuatan Mesin Pencari Vertikal Ulasan & Spesifikasi Gadget dengan Algoritma Okapi BM25 dan Sentence-BERT pada Korpus Teks Bahasa Indonesia" ini dapat diselesaikan dengan baik dan tepat waktu.

Proyek ini dilaksanakan secara berkelompok guna mengimplementasikan konsep teoritis penelusuran informasi ke dalam bentuk aplikasi nyata, mencakup proses pengumpulan 900 artikel ulasan gadget dari lima portal teknologi Indonesia, prapemrosesan teks Bahasa Indonesia menggunakan PySastrawi, pengindeksan Inverted Index, perankingan probabilistik Okapi BM25, pencarian semantik Sentence-BERT, serta evaluasi kuantitatif komparatif (Precision@K, Recall@K, F1@K, Mean Average Precision, dan latensi).

Penyelesaian tugas ini tidak terlepas dari bimbingan dan dukungan berbagai pihak. Oleh karena itu, kami menyampaikan terima kasih yang sebesar-besarnya kepada:
1. Bapak/Ibu Dosen Pengampu Mata Kuliah Penelusuran Informasi, Fakultas Matematika dan Ilmu Pengetahuan Alam, Universitas Syiah Kuala, atas arahan materi, masukan teknis, dan bimbingan selama perkuliahan dan pengerjaan proyek akhir ini.
2. Rekan-rekan satu kelompok atas dedikasi, kolaborasi aktif, dan kerja sama yang solid dalam menyelesaikan pembagian tugas crawling, pembangunan core search engine, perancangan antarmuka web, dan penyusunan laporan.
3. Rekan-rekan mahasiswa Program Studi Informatika USK atas diskusi ilmiah dan pertukaran gagasan seputar implementasi sistem temu balik informasi.

Kami menyadari bahwa laporan dan sistem ini masih memiliki keterbatasan. Kritik dan masukan yang membangun sangat kami harapkan guna penyempurnaan sistem di masa mendatang. Semoga laporan ini dapat memberikan manfaat bagi pembelajaran penelusuran informasi.

Banda Aceh, November 2026

Tim Penyusun (Kelompok 4)

---

## Daftar Isi

- Halaman Judul dan Pengesahan
- Abstrak dan Abstract
- BAB I Pendahuluan
  - 1.1 Latar Belakang
  - 1.2 Rumusan Masalah
  - 1.3 Maksud dan Tujuan
  - 1.4 Manfaat Penelitian
- BAB II Tinjauan Kepustakaan
  - 2.1 Information Retrieval
  - 2.2 Text Preprocessing Bahasa Indonesia
  - 2.3 Algoritma Okapi BM25
  - 2.4 Sentence-BERT dan Cosine Similarity
  - 2.5 Metrik Evaluasi Information Retrieval
- BAB III Metode Penelitian
  - 3.1 Lingkungan Implementasi
  - 3.2 Arsitektur Sistem
  - 3.3 Multi-source Crawler
  - 3.4 Skema Database SQLite
  - 3.5 Ground Truth Labeling
  - 3.6 Prosedur Evaluasi
- BAB IV Hasil dan Pembahasan
  - 4.1 Analisis Karakteristik Korpus
  - 4.2 Distribusi Kata (Hukum Zipf)
  - 4.3 Pengujian Kueri Eksak vs Kueri Semantik
  - 4.4 Tabel Komparasi Evaluasi Kuantitatif
  - 4.5 Analisis Kelebihan dan Kelemahan BM25 vs Sentence-BERT
- BAB V Kesimpulan dan Saran
  - 5.1 Kesimpulan
  - 5.2 Saran
- Daftar Pustaka
- Lampiran Kontribusi Anggota

## Daftar Tabel

- Tabel 3.1 Skema Tabel `documents` pada SQLite (`data/gadget.db`)
- Tabel 4.1 Distribusi Dokumen Berdasarkan Portal Sumber dan Kategori Gadget
- Tabel 4.2 Sepuluh Istilah Berfrekuensi Tertinggi pada Korpus Terindeks
- Tabel 4.3 Hasil Pengujian Per Kueri (15 Kueri Uji: Eksak vs Semantik)
- Tabel 4.4 Perbandingan Metrik Evaluasi Kuantitatif Okapi BM25 vs Sentence-BERT
- Tabel Lampiran Kontribusi Anggota Kelompok 4

## Daftar Gambar

- Gambar 3.1 Bukti Eksekusi Crawler Multi-Sumber dan Ringkasan SQLite
- Gambar 4.1 Distribusi Dokumen Korpus Berdasarkan Portal Sumber dan Kategori Gadget
- Gambar 4.2 Kurva Distribusi Hukum Zipf Korpus Ulasan Gadget (Log-Log)
- Gambar 4.3 Perbandingan Average Precision Per Kueri (Eksak vs Semantik)
- Gambar 4.4 Perbandingan Metrik Evaluasi Kuantitatif Okapi BM25 vs Sentence-BERT
- Gambar 4.5 Perbandingan Latensi Steady-State Per Kueri (Okapi BM25 vs Sentence-BERT)
