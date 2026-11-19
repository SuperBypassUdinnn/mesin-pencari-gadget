# BAB V Kesimpulan dan Saran

## 5.1 Kesimpulan

Berdasarkan perancangan, implementasi, dan evaluasi sistem mesin pencari vertikal ulasan gadget berbahasa Indonesia, dapat disimpulkan hal-hal berikut:

1. Sistem mesin pencari vertikal untuk ulasan dan spesifikasi gadget telah berhasil dibangun dengan arsitektur terpisah menggunakan backend FastAPI, frontend React, penyimpanan SQLite, dan dikontainerisasi menggunakan Docker Compose.
2. Korpus teks Bahasa Indonesia sebanyak **900 artikel ulasan gadget unik** berhasil dikumpulkan dari lima portal teknologi Indonesia (Jagat Review 252, Yangcanggih 252, Droidlime 153, Gadgetren 135, dan Hybrid 108) dengan rata-rata panjang 617,43 kata serta cakupan ekstraksi spesifikasi teknis sebesar 77,22% (695 dokumen).
3. Pengindeksan Inverted Index menghasilkan 11.802 token dasar unik (`avgdl = 388,89` token) yang mengikuti distribusi Hukum Zipf dengan gradien `-1,5891` dan $R^2 = 0{,}9510$, sementara model Sentence-BERT `paraphrase-multilingual-MiniLM-L12-v2` menghasilkan matriks embedding padat berdimensi `(900, 384)`.
4. Evaluasi kuantitatif terhadap 15 kueri uji berlabel ground truth menunjukkan bahwa Okapi BM25 mencapai Precision@5 sebesar `0,7467`, Precision@10 sebesar `0,6600`, MAP sebesar `0,4647`, dan latensi steady-state `1,28 ms`, lebih tinggi secara keseluruhan dibandingkan Sentence-BERT (`Precision@5 = 0,5467`, `Precision@10 = 0,4800`, `MAP = 0,2993`, latensi steady-state `18,00 ms`) karena keterbatasan panjang sekuens 128 token pada model transformer terhadap artikel ulasan panjang.
5. Di sisi lain, Sentence-BERT unggul tajam dalam memahami maksud semantik dan mengatasi ambiguitas leksikal (polisemi), terbukti pada kueri `"HP baterai tahan lama seharian tanpa sering cas"` di mana Sentence-BERT mencapai AP `0,5047` (15 kali lebih tinggi dibanding BM25 sebesar `0,0333`), sehingga penyajian kedua algoritma secara side-by-side saling melengkapi.

## 5.2 Saran

Berdasarkan temuan empiris dalam penelitian ini, saran untuk pengembangan lanjutan adalah sebagai berikut:

1. Mengimplementasikan metode *hybrid retrieval* seperti Reciprocal Rank Fusion (RRF) yang menggabungkan skor Okapi BM25 dan Sentence-BERT agar memperoleh presisi leksikal tinggi sekaligus ketahanan terhadap ambiguitas semantik.
2. Menerapkan strategi *passage chunking* (pemecahan dokumen panjang per paragraf atau per bagian spesifikasi) sebelum di-encode oleh Sentence-BERT agar informasi teknis yang berada setelah 128 token awal tetap terekam dalam indeks vektor.
3. Menambahkan pemanasan model (*eager warmup*) saat startup server FastAPI sehingga latensi *cold-start* pada kueri pertama (`7.982,79 ms`) tidak dirasakan oleh pengguna akhir.
4. Mengembangkan penyaringan terstruktur (faceted search) berdasarkan rentang harga, kategori perangkat, dan jenis chipset langsung dari kolom `specs_json` SQLite.
5. Menambahkan ekspansi frasa bigram/n-gram untuk istilah teknis gabungan seperti `"Snapdragon 8"` atau `"RAM 16GB"` guna meningkatkan ketepatan pencarian pada istilah bernomor.
