# BAB II Tinjauan Kepustakaan

## 2.1 Information Retrieval

Information Retrieval (IR) atau Penelusuran Informasi adalah ilmu yang mempelajari cara menyimpan, mengorganisasi, mengindeks, dan menemukan kembali informasi yang relevan dari koleksi dokumen tidak terstruktur atau semi-terstruktur (Manning, Raghavan, & Schütze, 2008). Tujuan utama sistem IR adalah mengembalikan daftar dokumen terurut berdasarkan tingkat relevansinya terhadap kebutuhan informasi pengguna yang dinyatakan dalam bentuk kueri. Dalam konteks mesin pencari vertikal gadget, IR berfokus pada domain spesifik ulasan dan spesifikasi perangkat elektronik sehingga hasil pencarian terhindar dari derau halaman web umum.

Proses inti dalam sistem IR meliputi akuisisi dokumen (crawling), prapemrosesan teks, representasi dan pengindeksan (baik berupa inverted index maupun dense vector index), pencocokan serta perankingan (retrieval and ranking), hingga evaluasi kinerja secara kuantitatif.

## 2.2 Text Preprocessing Bahasa Indonesia

Sebelum dokumen dan kueri diindeks dalam sistem pencarian leksikal, teks mentah perlu dibersihkan dan dinormalisasi agar variasi penulisan kata tidak menurunkan kecocokan. Tahapan text preprocessing dalam penelitian ini meliputi:

1. Case folding: Mengubah seluruh huruf menjadi huruf kecil agar pencocokan tidak sensitif terhadap huruf kapital.
2. Tokenization: Memecah teks menjadi token kata atau istilah teknis menggunakan ekspresi reguler alfanumerik (`[a-z0-9]`) sehingga nama prosesor, kapasitas memori, dan seri perangkat tetap terjaga utuh.
3. Stopword removal: Menghapus kata-kata umum yang memiliki daya pembeda rendah menggunakan kamus stopword Bahasa Indonesia dari Sastrawi.
4. Stemming: Mengubah kata berimbuhan menjadi kata dasarnya (root word) menggunakan PySastrawi yang menerapkan algoritma Nazief-Adriani (Nazief & Adriani, 2006).

Stemming Bahasa Indonesia berperan penting karena kekayaan afiksasi (awalan, sisipan, akhiran, dan konfiks). Dengan stemming, kata seperti "menguji", "diuji", dan "pengujian" dipetakan ke kata dasar yang sama, sehingga mengurangi ukuran kosakata dan meningkatkan recall pada pencarian leksikal.

## 2.3 Algoritma Okapi BM25

Okapi BM25 adalah algoritma perankingan berbasis kerangka probabilistik yang dikembangkan oleh Robertson dan Zaragoza (2009). Algoritma ini menyempurnakan pembobotan TF-IDF klasik dengan menambahkan saturasi frekuensi istilah (term frequency saturation) dan normalisasi panjang dokumen relatif terhadap panjang rata-rata korpus. Rumus skor relevansi dokumen $D$ terhadap kueri $Q$ adalah:

$$\text{Score}(D, Q) = \sum_{q \in Q} \text{IDF}(q) \cdot \frac{f(q, D) \cdot (k_1 + 1)}{f(q, D) + k_1 \cdot \left(1 - b + b \cdot \frac{|D|}{\text{avgdl}}\right)}$$

dengan nilai Inverse Document Frequency (IDF) Robertson-Spärck Jones yang dihaluskan:

$$\text{IDF}(q) = \ln\left(\frac{N - n(q) + 0,5}{n(q) + 0,5} + 1\right)$$

Keterangan parameter dalam persamaan di atas adalah:
- $N$: Jumlah total dokumen dalam korpus (900 dokumen).
- $n(q)$: Jumlah dokumen yang mengandung istilah kueri $q$.
- $f(q, D)$: Frekuensi kemunculan istilah $q$ dalam dokumen $D$.
- $|D|$ dan $\text{avgdl}$: Panjang dokumen $D$ (dalam jumlah token terindeks) dan rata-rata panjang dokumen korpus.
- $k_1$: Parameter saturasi frekuensi istilah (ditetapkan sebesar $1{,}5$).
- $b$: Parameter kontrol normalisasi panjang dokumen (ditetapkan sebesar $0{,}75$).

BM25 sangat efektif untuk kueri teknis eksak karena istilah yang jarang muncul pada korpus (seperti seri prosesor atau fitur kamera khusus) memperoleh bobot IDF tinggi, sementara struktur Inverted Index memungkinkan eksekusi kueri hanya dalam hitungan milidetik.

## 2.4 Sentence-BERT dan Cosine Similarity

Sentence-BERT (SBERT) adalah modifikasi arsitektur BERT menggunakan jaringan Siamese dan Triplet untuk menghasilkan representasi vektor berdimensi tetap (dense sentence embedding) yang bermakna secara semantik (Reimers & Gurevych, 2019). Pada penelitian ini digunakan model pralatih multibahasa `paraphrase-multilingual-MiniLM-L12-v2` yang mendukung Bahasa Indonesia maupun istilah teknis Bahasa Inggris dengan dimensi vektor $d = 384$.

Setiap dokumen dan kueri dipetakan ke dalam vektor berdimensi 384 yang dinormalisasi menggunakan L2 norm ($\hat{v} = v / \|v\|_2$). Dengan normalisasi L2, perhitungan Cosine Similarity antara vektor kueri $\hat{u}$ dan matriks embedding dokumen $\hat{V}$ dapat disederhanakan menjadi perkalian titik (dot product) tunggal:

$$\text{Cosine Similarity}(\hat{u}, \hat{v}) = \frac{u \cdot v}{\|u\|_2 \|v\|_2} = \hat{u} \cdot \hat{v}$$

Pendekatan ini unggul dalam memahami konteks, sinonim, dan maksud kueri berbasis niat (intent-based) walaupun kata kunci pada kueri tidak muncul secara harfiah di dalam dokumen. Namun demikian, arsitektur berbasis transformer memiliki batasan panjang urutan token masukan (128 token pada MiniLM-L12-v2) serta memerlukan biaya komputasi lebih tinggi dibandingkan BM25 saat melakukan encoding kueri.

## 2.5 Metrik Evaluasi Information Retrieval

Evaluasi kinerja kedua algoritma dilakukan mengikuti standar `trec_eval` (Voorhees & Harman, 2005) menggunakan lima metrik utama:

1. Precision@K: Proporsi dokumen relevan di antara $K$ dokumen peringkat teratas yang dikembalikan sistem:
   $$\text{Precision@K} = \frac{|\text{Retrieved}_{[:K]} \cap \text{Relevant}|}{K}$$
2. Recall@K: Proporsi dokumen relevan yang berhasil ditemukan pada $K$ hasil teratas terhadap seluruh dokumen relevan yang diketahui pada ground truth:
   $$\text{Recall@K} = \frac{|\text{Retrieved}_{[:K]} \cap \text{Relevant}|}{|\text{Relevant}|}$$
3. F1-Score@K: Rata-rata harmonik antara Precision@K dan Recall@K:
   $$\text{F1@K} = \frac{2 \cdot \text{Precision@K} \cdot \text{Recall@K}}{\text{Precision@K} + \text{Recall@K}}$$
4. Mean Average Precision (MAP): Rata-rata nilai Average Precision (AP) pada seluruh kueri uji $|Q|$, yang mengevaluasi ketepatan urutan ranking secara menyeluruh:
   $$\text{AP} = \frac{1}{|\text{Relevant}|} \sum_{i=1}^{N} \text{Precision@}i \cdot \text{rel}(i), \quad \text{MAP} = \frac{1}{|Q|} \sum_{q=1}^{|Q|} \text{AP}(q)$$
5. Latensi (Latency): Waktu respons pencarian per kueri yang diukur dalam milidetik menggunakan penghitung waktu presisi tinggi (`time.perf_counter()`).

Seluruh perhitungan metrik dilengkapi pengamanan pembagian nol apabila himpunan relevan kosong atau tidak ada dokumen relevan yang terambil.
