# 5 Minute Demo Script

## Panduan Naskah Pembagian Waktu 5 Menit Presentasi & Video YouTube

Demo ini dipresentasikan oleh seluruh anggota tim Kelompok 4 (Member 1, Member 2 (Fadhlur), dan Member 3 (Khalish)), masing-masing berbicara pada segmen waktunya. Video presentasi berdurasi 5 menit diunggah ke YouTube sebagai salah satu syarat luaran tugas akhir.

## 0:00 - 1:00 | Intro & Background (Member 3 - Khalish)

Member 3 (Khalish) membuka presentasi dan memaparkan latar belakang masalah: ulasan serta spesifikasi teknis gadget berbahasa Indonesia tersebar di banyak portal (Jagat Review, Yangcanggih, Droidlime, Gadgetren, dan Hybrid) dalam format yang berbeda-beda, sementara mesin pencari umum tercampur iklan dan toko daring. Khalish menjelaskan proses crawling 900 artikel ulasan gadget unik dengan ekstraksi spesifikasi otomatis (77,22% coverage) ke SQLite serta alur arsitektur sistem (crawling, preprocessing PySastrawi, indexing BM25 & S-BERT, retrieval, evaluation).

## 1:00 - 3:00 | Live Search & Algorithmic Comparison (Member 2 - Fadhlur)

Member 2 (Fadhlur) menjalankan demo live sistem menggunakan Docker (`docker compose up --build` di `http://localhost:3000`). Fadhlur menguji kueri teknis eksak `"ASUS Zenbook Intel OLED"` (`q02`) untuk menunjukkan presisi tinggi Okapi BM25 (`AP = 0,9861`, latensi ~1,3 ms) beserta modal spesifikasi teknisnya, lalu menguji kueri berbasis niat dengan jebakan polisemi `"HP baterai tahan lama seharian tanpa sering cas"` (`q11`) untuk memperlihatkan keunggulan semantik Sentence-BERT (`P@5 = 0,80`, `AP = 0,5047`) dalam membedakan smartphone dari laptop merek HP.

## 3:00 - 4:15 | Interactive Evaluation Dashboard (Member 1)

Member 1 membuka tab Evaluation Dashboard pada antarmuka web, meninjau grafik dan tabel komparasi 15 kueri uji (BM25 MAP `0,4647` vs Sentence-BERT MAP `0,2993`, P@5 `0,7467` vs `0,5467`, serta latensi steady-state `1,28 ms` vs `18,00 ms`). Member 1 menjelaskan inspeksi per kueri serta alasan mengapa BM25 unggul di dokumen panjang sementara Sentence-BERT unggul pada kueri polisemi/semantik.

## 4:15 - 5:00 | Conclusion & Q&A Readiness (Semua Anggota)

Semua anggota merangkum temuan utama secara bergantian: integrasi dual-engine Okapi BM25 dan Sentence-BERT secara berdampingan memberikan cakupan pencarian yang cepat sekaligus adaptif terhadap variasi bahasa alami, siap dilanjutkan ke sesi tanya jawab penguji.

## Persyaratan Video YouTube

- Seluruh anggota tim (Member 1, Fadhlur, Khalish) wajib berbicara di video.
- Durasi total maksimal 5 menit sesuai alokasi segmen di atas.
- Tautan video YouTube dicantumkan pada `README.md` setelah rekaman selesai diunggah.
