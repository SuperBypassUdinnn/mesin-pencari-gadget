# Halaman Judul dan Pengesahan

## Sampul

LAPORAN PROYEK AKHIR MATA KULIAH PENELUSURAN INFORMASI

PEMBUATAN MESIN PENCARI VERTIKAL ULASAN & SPESIFIKASI GADGET DENGAN ALGORITMA OKAPI BM25 DAN SENTENCE-BERT PADA KORPUS TEKS BAHASA INDONESIA

Disusun oleh:
Kelompok [Nomor Kelompok]

1. [Nama Anggota 1] (NPM. [NPM])
2. Fadhlurrahman Alaudin (NPM. [NPM])
3. [Nama Anggota 3] (NPM. [NPM])

Dosen Pengampu Mata Kuliah:
[Nama Dosen Pengampu Mata Kuliah], [Gelar]
NIP. [NIP Dosen]

PROGRAM STUDI INFORMATIKA / ILMU KOMPUTER
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
Kelompok [Nomor Kelompok]

1. [Nama Anggota 1] (NPM. [NPM])
2. Fadhlurrahman Alaudin (NPM. [NPM])
3. [Nama Anggota 3] (NPM. [NPM])

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
Kelompok: [Nomor Kelompok]

Anggota Tim:
1. Nama: [Nama Anggota 1] | NPM: [NPM] | Peran: Frontend & UI Lead
2. Nama: Fadhlurrahman Alaudin | NPM: [NPM] | Peran: Core IR & Backend Lead
3. Nama: [Nama Anggota 3] | NPM: [NPM] | Peran: Data Engineering & Report Lead

Laporan Proyek Akhir ini telah diperiksa, diuji melalui live demo sistem, dan disetujui untuk memenuhi penilaian akhir mata kuliah Penelusuran Informasi.

Banda Aceh, [Tanggal Pengesahan] 2026

Menyetujui,
Dosen Pengampu Mata Kuliah Penelusuran Informasi

( [Nama Dosen Pengampu Mata Kuliah], [Gelar] )
NIP. [NIP Dosen]

---

## Pernyataan Bebas Plagiasi

Kami yang bertanda tangan di bawah ini menyatakan dengan sesungguhnya bahwa Laporan Proyek Akhir Mata Kuliah Penelusuran Informasi dengan judul di atas adalah hasil karya orisinal kelompok kami sendiri. Seluruh data korpus teks hasil crawling, implementasi kode algoritma Okapi BM25 dan Sentence-BERT, antarmuka web, serta analisis evaluasi metrik (MAP, Precision, Recall, F1) yang dipaparkan dalam laporan ini dikerjakan secara mandiri dan bebas dari tindakan plagiasi. Semua referensi dan kepustakaan yang dirujuk telah dicantumkan secara tertib pada Daftar Pustaka.

Banda Aceh, [Tanggal] 2026

Tim Penyusun (Kelompok [Nomor Kelompok]):

1. [Nama Anggota 1] (NPM. [NPM]) ........................
2. Fadhlurrahman Alaudin (NPM. [NPM]) ........................
3. [Nama Anggota 3] (NPM. [NPM]) ........................

---

## Kata Pengantar

Puji syukur kami panjatkan ke hadirat Allah SWT atas rahmat dan hidayah-Nya, sehingga Laporan Proyek Akhir Mata Kuliah Penelusuran Informasi (Information Retrieval) yang berjudul "Pembuatan Mesin Pencari Vertikal Ulasan & Spesifikasi Gadget dengan Algoritma Okapi BM25 dan Sentence-BERT pada Korpus Teks Bahasa Indonesia" ini dapat diselesaikan dengan baik dan tepat waktu.

Proyek ini dilaksanakan secara berkelompok guna mengimplementasikan konsep teoritis penelusuran informasi ke dalam bentuk aplikasi nyata, mencakup proses pengumpulan korpus ulasan gadget multi-sumber, prapemrosesan teks Bahasa Indonesia, pengindeksan Inverted Index, perankingan probabilistik Okapi BM25, pencarian semantik Sentence-BERT, serta evaluasi kuantitatif komparatif (Precision@K, Recall@K, F1@K, dan Mean Average Precision).

Penyelesaian tugas ini tidak terlepas dari bimbingan dan dukungan berbagai pihak. Oleh karena itu, kami menyampaikan terima kasih yang sebesar-besarnya kepada:
1. Bapak/Ibu Dosen Pengampu Mata Kuliah Penelusuran Informasi, Fakultas Matematika dan Ilmu Pengetahuan Alam, Universitas Syiah Kuala, atas arahan materi, masukan teknis, dan bimbingan selama perkuliahan dan pengerjaan proyek akhir ini.
2. Rekan-rekan satu kelompok atas dedikasi, kolaborasi aktif, dan kerja sama yang solid dalam menyelesaikan pembagian tugas crawling, pembangunan core search engine, perancangan antarmuka web, dan penyusunan laporan.
3. Rekan-rekan mahasiswa Program Studi Informatika USK atas diskusi ilmiah dan pertukaran gagasan seputar implementasi sistem temu balik informasi.

Kami menyadari bahwa laporan dan sistem ini masih memiliki keterbatasan. Kritik dan masukan yang membangun sangat kami harapkan guna penyempurnaan sistem di masa mendatang. Semoga laporan ini dapat memberikan manfaat bagi pembelajaran penelusuran informasi.

Banda Aceh, [Bulan] 2026

Tim Penyusun

---

## Daftar Isi

Halaman Judul dan Pengesahan ........................................ ii
Abstrak dan Abstract ............................................... iv
BAB I Pendahuluan ................................................. 1
  1.1 Latar Belakang .............................................. 1
  1.2 Rumusan Masalah ............................................. 2
  1.3 Maksud dan Tujuan ........................................... 3
  1.4 Manfaat Penelitian .......................................... 3
BAB II Tinjauan Kepustakaan ....................................... 4
  2.1 Konsep Dasar Information Retrieval .......................... 4
  2.2 Text Preprocessing Bahasa Indonesia ......................... 5
  2.3 Algoritma Okapi BM25 ........................................ 6
  2.4 Algoritma Sentence-BERT & Semantic Retrieval ................ 7
  2.5 Metrik Evaluasi Kinerja (MAP, Precision, Recall, F1) ........ 8
BAB III Metode Penelitian ......................................... 10
  3.1 Waktu dan Lingkungan Implementasi ........................... 10
  3.2 Arsitektur Sistem dan Alur Kerja ............................ 11
  3.3 Pengumpulan Korpus Data (Multi-Source Crawling) ............. 12
  3.4 Skema Database dan Pengindeksan ............................. 13
  3.5 Prosedur Pengujian dan Evaluasi Kuantitatif ................. 14
BAB IV Hasil dan Pembahasan ....................................... 16
  4.1 Karakteristik Korpus Data Ulasan Gadget ..................... 16
  4.2 Hasil Pengujian Pencarian Komparatif Side-by-Side ........... 17
  4.3 Hasil Evaluasi Kuantitatif (BM25 vs Sentence-BERT) .......... 19
  4.4 Analisis Perbandingan dan Temuan Kinerja .................... 21
BAB V Kesimpulan dan Saran ........................................ 23
  5.1 Kesimpulan .................................................. 23
  5.2 Saran Pengembangan Lanjutan ................................. 24
Daftar Pustaka .................................................... 25
Lampiran Kontribusi Anggota ....................................... 27
