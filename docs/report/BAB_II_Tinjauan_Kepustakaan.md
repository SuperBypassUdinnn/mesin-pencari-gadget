# BAB II Tinjauan Kepustakaan

## 2.1 Information Retrieval

Information Retrieval (IR) atau Penelusuran Informasi adalah ilmu yang mempelajari cara menyimpan, mengorganisasi, dan mencari informasi dari koleksi dokumen yang besar. Tujuan utama IR adalah mengembalikan dokumen yang relevan terhadap kebutuhan informasi pengguna yang diungkapkan dalam bentuk kueri. Dalam konteks mesin pencari vertikal gadget, IR digunakan untuk mengindeks dan mencari artikel ulasan serta spesifikasi teknis dari berbagai portal teknologi.

Proses IR umumnya terdiri dari beberapa tahap, yaitu representasi dokumen, representasi kueri, pencocokan (matching), dan penilaian relevansi (ranking). Representasi dokumen dapat berupa vektor istilah (term vector) atau vektor dens yang dihasilkan oleh model pembelajaran mesin.

## 2.2 Text Preprocessing Bahasa Indonesia

Sebelum dokemen dan kueri dapat diindeks dan dicari, teks perlu melalui tahap preprocessing untuk membersihkan dan menstandarkan representasi teks. Tahapan preprocessing dalam penelitian ini meliputi:

1. Case folding: Mengubah semua huruf menjadi huruf kecil agar pencarian tidak bersifat case-sensitive.
2. Tokenization: Memecah teks menjadi token-token terkecil (kata atau frasa) berdasarkan spasi dan pola regex.
3. Stopword removal: Menghapus kata-kata non-informatif (stopwords) menggunakan leksikon Sastrawi/Tala, sambil mempertahankan modifier teknis penting seperti "tanpa", "tidak", dan "anti".
4. Stemming: Mengubah kata menjadi bentuk dasarnya (root word) menggunakan PySastrawi yang menerapkan aturan morfologis Nazief-Adriani.

Stemming bahasa Indonesia sangat penting karena bahasa Indonesia memiliki banyak imbuhan (awalan, akhiran, dan gabungan keduanya) yang dapat mengubah bentuk kata dasar. Dengan stemming, variasi kata seperti "mengulas", "diulas", dan "pengulasan" dapat diubah menjadi bentuk dasar "ulasan", sehingga meningkatkan kemiripan dalam pencarian leksikal.

## 2.3 Algoritma Okapi BM25

Okapi BM25 adalah algoritma penelusuran informasi berbasis model probabilistik yang menghitung skor relevansi dokumen terhadap kueri berdasarkan frekuensi istilah dan panjang dokumen. Rumus matematis Okapi BM25 adalah sebagai berikut:

Score(D, Q) = sum_{q in Q} IDF(q) * (f(q, D) * (k1 + 1)) / (f(q, D) + k1 * (1 - b + b * (|D| / avgdl)))

Di mana IDF(q) dihitung dengan rumus Robertson-Sparck Jones:

IDF(q) = ln((N - n(q) + 0.5) / (n(q) + 0.5) + 1)

Parameter dalam rumus di atas adalah:
- N: Total jumlah dokumen dalam korpus.
- n(q): Jumlah dokumen yang mengandung istilah kueri q.
- f(q, D): Frekuensi kemunculan istilah q dalam dokumen D.
- |D| dan avgdl: Panjang dokumen D dan rata-rata panjang dokumen dalam korpus.
- k1: Parameter saturasi istilah (nilai 1.5).
- b: Parameter normalisasi panjang dokumen (nilai 0.75).

BM25 efektif untuk kueri teknis eksak karena memberikan bobor lebih tinggi pada istilah yang jarang muncul dalam korpus namun sering muncul dalam suatu dokumen tertentu.

## 2.4 Sentence-BERT dan Cosine Similarity

Sentence-BERT (SBERT) adalah variasi dari arsitektur BERT yang dilatih untuk menghasilkan representasi vektor dens dari kalimat atau paragraf. Dalam penelitian ini, model yang digunakan adalah paraphrase-multilingual-MiniLM-L12-v2 yang menghasilkan vektor berdimensi 384 dan mendukung bahasa Indonesia.

Setiap dokumen diwakili sebagai vektor dens yang dihasilkan dari pengkodean gabungan judul, spesifikasi teknis, dan ringkasan ulasan. Query juga dienkode menjadi vektor dens yang sama. Kemudian, kemiripan antara vektor dokumen dan vektor query dihitung menggunakan cosine similarity:

Cosine Similarity(u, v) = (u . v) / (||u|| * ||v||)

Sebelum menghitung cosine similarity, vektor dinormalisasi dengan L2 norm sehingga hasil dot product memberikan nilai cosine similarity langsung. Pencarian dilakukan dengan perkalian matriks-vektor tunggal, diikuti dengan pengurutan untuk mengambil hasil Top-K.

SBERT unggul untuk kueri semantik dan berbasis niat karena menangkap makna dan konteks, bukan hanya kecocokan kata secara harfiah.

## 2.5 Metrik Evaluasi Information Retrieval

Untuk mengevaluasi performa mesin pencari, digunakan metrik evaluasi standar IR sebagai berikut:

1. Precision@K: Proporsi dokumen relevan dalam K hasil teratas.
   Precision@K = |Dokumen Relevan n Hasil Teratas K| / K

2. Recall@K: Proporsi dokumen relevan yang berhasil diambil dari total dokumen relevan dalam korpus.
   Recall@K = |Dokumen Relevan n Hasil Teratas K| / |Total Dokumen Relevan dalam Korpus|

3. F1-Score@K: Rata-rata harmonik antara Precision dan Recall.
   F1@K = 2 * (Precision@K * Recall@K) / (Precision@K + Recall@K)

4. Mean Average Precision (MAP): Rata-rata Average Precision (AP) di seluruh kueri uji.
   AP = sum_{k=1}^{N} (P@k * rel(k)) / |Total Dokumen Relevan|
   MAP = (1 / |Q|) * sum_{q=1}^{|Q|} AP(q)

5. Latensi: Waktu respons rata-rata kueri dalam milidetik.

Semua metrik dihitung dengan proteksi terhadap pembagian nol untuk kueri yang tidak menghasilkan hasil relevan.
