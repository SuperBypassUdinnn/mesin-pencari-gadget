# BAB V Kesimpulan dan Saran

## 5.1 Kesimpulan

Berdasarkan hasil penelitian dan pengujian yang telah dilakukan, dapat disimpulkan sebagai berikut:

1. Mesin pencari vertikal untuk ulasan dan spesifikasi gadget telah berhasil dibangun dengan arsitektur terpisah yang terdiri dari backend FastAPI, frontend React, dan storage layer SQLite.
2. Dua algoritma penelusuran informasi berhasil diimplementasikan, yaitu Okapi BM25 untuk pencarian leksikal dan Sentence-BERT untuk pencarian semantik dengan cosine similarity.
3. Korpus consisting of 700 hingga 1.000 artikel ulasan gadget dari Gadgetren, Jagat Review, dan Droidlime telah berhasil dikumpulkan dan diindeks.
4. Hasil evaluasi menunjukkan bahwa Sentence-BERT unggul dalam MAP dan Recall, terutama untuk kueri semantik dan berbasis niat, sedangkan Okapi BM25 lebih efektif untuk kueri teknis eksak dengan latensi yang lebih rendah.
5. Kombinasi kedua algoritma dalam satu sistem memberikan hasil pencarian yang lebih komprehensif untuk berbagai jenis kebutuhan pencarian gadget.

## 5.2 Saran

Berdasarkan temuan penelitian ini, saran untuk penelitian lanjutan adalah sebagai berikut:

1. Mengembangkan sistem hybrid yang secara otomatis memilih algoritma terbaik berdasarkan jenis kueri yang diajukan pengguna.
2. Menambahkan fitur personalisasi pencarian berdasarkan riwayat pencarian dan preferensi pengguna.
3. Memperluas korpus dengan menambahkan lebih banyak portal teknologi dan artikel ulasan gadget.
4. Mengimplementasikan fitur filter lanjutan berdasarkan spesifikasi teknis, rentang harga, dan merek gadget.
5. Mengoptimalkan latensi Sentence-BERT dengan teknik kuantisasi model atau approximate nearest neighbor search.
