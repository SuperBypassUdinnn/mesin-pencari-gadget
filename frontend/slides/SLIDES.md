# Slide Demo 5 Menit - Mesin Pencari Gadget Vertikal

Bahan tayang untuk presentasi dan video YouTube Kelompok 4. Deck dibuat sebagai satu file HTML mandiri tanpa dependency eksternal, sehingga dapat dibuka langsung di browser secara offline.

## Cara Membuka

1. Buka `frontend/slides/index.html` di browser modern (Chrome, Edge, Firefox).
2. Gunakan tombol panah kiri/kanan, spasi, PageUp/PageDown, atau klik sisi layar untuk berpindah slide.
3. Tekan `N` untuk menampilkan atau menyembunyikan catatan pembicara.
4. Tekan `Home` atau `End` untuk lompat ke slide pertama atau terakhir.
5. Untuk mengekspor ke PDF, gunakan `Ctrl+P` lalu pilih "Save as PDF" (setiap slide menjadi satu halaman).

## Alokasi Waktu dan Pembicara

| Waktu | Segmen | Pembicara | Slide |
| :--- | :--- | :--- | :--- |
| 0:00 - 0:10 | Pembuka dan judul | Semua (diwakili Khalish) | 1 |
| 0:10 - 1:00 | Latar belakang dan korpus | Khalish | 2 - 3 |
| 1:00 - 3:00 | Preprocessing, BM25, Sentence-BERT, demo | Fadhlur | 4 - 7 |
| 3:00 - 4:15 | Dashboard evaluasi dan insight | Irfan | 8 - 9 |
| 4:15 - 5:00 | Kesimpulan dan tanya jawab | Semua anggota | 10 - 11 |

## Catatan Pembicara per Slide

### Slide 1 - Judul

Sebutkan judul proyek, mata kuliah, dan anggota kelompok. Jelaskan bahwa demo membandingkan dua pendekatan information retrieval pada korpus gadget Indonesia yang riil.

### Slide 2 - Latar Belakang

Tekankan fragmentasi ulasan gadget di lima portal. Sebutkan bahwa mesin pencari umum mencampur iklan dan toko daring sehingga pengguna sulit membandingkan ulasan teknis secara adil.

### Slide 3 - Korpus dan Arsitektur

Sebutkan 900 dokumen unik, lima portal, cakupan ekstraksi spesifikasi 77,22 persen, dan 15 kueri ground truth. Jelaskan alur singkat dari crawling sampai evaluasi.

### Slide 4 - Preprocessing dan Okapi BM25

Jelaskan empat tahap preprocessing: normalisasi, tokenisasi, stopword removal, dan stemming PySastrawi. Sebutkan inverted index dibangun dari nol serta parameter k1 = 1,5 dan b = 0,75. Tunjukkan formula BM25 dan alasan penggunaan IDF dengan floor +1.

### Slide 5 - Sentence-BERT

Sebutkan model `paraphrase-multilingual-MiniLM-L12-v2`, matriks embedding 900 x 384, normalisasi L2, dan cosine similarity melalui dot product. Tekankan bahwa model dimuat secara fail-loud agar evaluasi tidak menghasilkan angka palsu.

### Slide 6 - Demo Kueri Teknis q02

Jalankan pencarian `"ASUS Zenbook Intel OLED"`. Tunjukkan kolom BM25, AP 0,9861, latensi sekitar 1,3 ms, lalu buka modal spesifikasi. Jelaskan mengapa pencocokan term eksak sangat efektif untuk kueri ini.

### Slide 7 - Demo Kueri Semantik q11

Jalankan pencarian `"HP baterai tahan lama seharian tanpa sering cas"`. Tunjukkan kolom Sentence-BERT dengan P@5 0,80 dan AP 0,5047. Jelaskan jebakan polisemi "HP" dan mengapa pemahaman makna membantu di sini.

### Slide 8 - Dashboard Evaluasi

Buka tab Evaluasi. Tunjukkan tiga kartu ringkasan, tabel metrik, grafik batang, dan tabel per kueri. Sebutkan angka utama: MAP 0,4647 vs 0,2993; P@5 0,7467 vs 0,5467; latensi 1,28 ms vs 18,00 ms.

### Slide 9 - Insight

Bandingkan kekuatan masing-masing pendekatan. BM25 unggul pada istilah teknis eksak dan dokumen panjang. Sentence-BERT unggul pada parafrase, sinonim, polisemi, dan kueri niat. Tegaskan nilai split view bagi pengguna.

### Slide 10 - Kesimpulan

Sampaikan tiga poin: integrasi end-to-end berhasil, BM25 unggul pada MAP dan latensi, Sentence-BERT melengkapi kueri semantik. Sebutkan rencana lanjutan: pembobotan hybrid, cross-encoder reranking, dan korpus lebih besar.

### Slide 11 - Penutup

Ucapkan terima kasih, tampilkan peran tim, dan buka sesi tanya jawab. Pastikan ketiga anggota tampil berbicara di video sesuai ketentuan tugas.

## Checklist Sebelum Rekaman

- [ ] Docker Compose berjalan dan aplikasi dapat dibuka di `http://localhost:3000`.
- [ ] Backend sehat di `http://localhost:8000/api/health`.
- [ ] Data evaluasi termuat di tab Evaluasi.
- [ ] Kueri q02 dan q11 sudah diuji sebelum rekaman.
- [ ] Modal spesifikasi dapat dibuka dan ditutup.
- [ ] Slide dibuka dalam mode fullscreen.
- [ ] Durasi total tidak melebihi 5 menit.
- [ ] Ketiga anggota berbicara sesuai pembagian segmen.
