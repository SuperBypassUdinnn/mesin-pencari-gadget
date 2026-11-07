# BAB III Metode Penelitian

## 3.1 Lingkungan Implementasi

Sistem dikembangkan dalam arsitektur terpisah (decoupled client-server) yang dikontainerisasi menggunakan Docker Compose. Lingkungan implementasi terdiri dari:

1. Backend Service: Python 3.11 dengan FastAPI dan Uvicorn. Backend bertanggung jawab atas REST API, ingesti data, preprocessing teks, mesin pengambilan BM25 dan Sentence-BERT, serta perhitungan evaluasi.
2. Frontend Service: React dengan Vite dan Tailwind CSS, disajikan dalam produksi melalui Nginx. Frontend menyediakan antarmuka pencarian interaktif dan dasbor evaluasi.
3. Storage Layer: SQLite untuk metadata dokumen, file JSON untuk inverted index, dan file .npy untuk matriks embedding Sentence-BERT.

Semua layanan dapat dijalankan dengan satu perintah melalui `docker compose up --build`.

## 3.2 Arsitektur Sistem

Arsitektur sistem terdiri dari alur data sebagai berikut:

Crawling -> Preprocessing -> Indexing -> Retrieval -> Evaluation

1. Crawling: Multi-source crawler mengumpulkan artikel ulasan gadget dari Gadgetren, Jagat Review, dan Droidlime.
2. Preprocessing: Teks artikel melalui case folding, tokenisasi, penghapusan stopwords, dan stemming dengan PySastrawi.
3. Indexing: Hasil preprocessing diindeks dalam inverted index untuk BM25 dan dienkode menjadi vektor dens untuk Sentence-BERT.
4. Retrieval: Pengguna mengajukan kueri melalui antarmuka web, sistem mengembalikan hasil dari BM25 dan Sentence-BERT secara side-by-side.
5. Evaluation: Hasil pencarian dievaluasi terhadap ground truth menggunakan metrik Precision@K, Recall@K, F1-Score, MAP, dan latensi.

## 3.3 Multi-source Crawler

Crawler mengumpulkan data dari tiga portal teknologi Indonesia:

1. Gadgetren: Portal ulasan gadget Indonesia dengan artikel tentang smartphone, laptop, dan aksesori.
2. Jagat Review: Portal ulasan teknologi dengan ulasan mendalam mengenai gadget dan perangkat elektronik.
3. Droidlime: Portal yang berfokus pada ulasan smartphone dan spesifikasi teknis.

Setiap artikel yang di-crawl disimpan dalam format JSON dengan metadata berupa judul, sumber, URL, kategori, tanggal publikasi, spesifikasi teknis (dalam format JSON), dan isi artikel. Data kemudian dimasukkan ke dalam database SQLite dengan skema tabel documents(id, title, source, url, category, date, specs_json, content).

Target korpus adalah 700 hingga 1.000 artikel ulasan gadget berbahasa Indonesia.

## 3.4 Skema Database SQLite

Database SQLite menyimpan metadata dokumen dalam tabel berikut:

Tabel documents:
- id: Identifikasi unik dokumen.
- title: Judul artikel ulasan.
- source: Sumber artikel (Gadgetren, Jagat Review, atau Droidlime).
- url: URL asli artikel.
- category: Kategori gadget (smartphone, laptop, tablet, dll.).
- date: Tanggal publikasi artikel.
- specs_json: Spesifikasi teknis dalam format JSON.
- content: Isi lengkap artikel ulasan.

## 3.5 Ground Truth Labeling

Ground truth adalah matriks relevansi biner (1 = relevan, 0 = tidak relevan) yang ditetapkan untuk 10 hingga 15 kueri uji. Kueri uji mencakup kueri teknis eksak (misalnya "Snapdragon 8 Gen 2", "Layar AMOLED 120Hz") dan kueri semantik berbasis niat (misalnya "HP untuk fotografi malam hari", "laptop murah untuk mahasiswa teknik"). Setiap kueri memiliki daftar ID dokumen yang relevan berdasarkan penilaiman manual oleh anggota tim.

## 3.6 Prosedur Evaluasi

Evaluasi dilakukan dengan menjalankan setiap kueri uji terhadap kedua algoritma (BM25 dan Sentence-BERT), kemudian menghitung Precision@K, Recall@K, F1-Score@K, MAP, dan latensi untuk setiap kueri. Hasil evaluasi dibandingkan antara kedua algoritma untuk menentukan kelebihan dan kelemahan masing-masing dalam berbagai jenis kueri.
