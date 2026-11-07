# BAB I Pendahuluan

## 1.1 Latar Belakang

Perkembangan teknologi informasi dan komunikasi telah mengubah pola konsumsi masyarakat terhadap produk elektronik, terutama gadget seperti smartphone, laptop, tablet, dan aksesori pendukung. Saat ini, informasi mengenai ulasan dan spesifikasi teknis gadget tersebar di banyak portal teknologi Indonesia, seperti Gadgetren, Jagat Review, dan Droidlime. Setiap portal memiliki format, tata letak, dan gaya penulisan yang berbeda-beda, sehingga sulit bagi pengguna untuk membandingkan spesifikasi dan ulasan dari berbagai sumber secara terpadu.

Masalah utama yang dihadapi pengguna adalah ketersediaan informasi yang terpencil dan tidak terstruktur. Sebuah ulasan kamera smartphone mungkin berada di satu portal, sementara ulasan baterai dan performa berada di portal lain. Selain itu, mesin pencari umum seperti Google menampilkan hasil yang terlalu luas dan tidak spesifik untuk kebutuhan pencarian vertikal gadget. Hasil pencarian sering kali mencakup toko online, forum diskusi, dan artikel yang tidak relevan, sehingga pengguna harus menyaring hasil secara manual.

Dalam konteks penelusuran informasi (information retrieval), terdapat dua pendekatan utama dalam pencarian, yaitu pendekatan leksikal dan pendekatan semantik. Pendekatan leksikal, exemplified by Okapi BM25, mencocokkan kata kunci kueri dengan kata yang terdapat dalam dokumen berdasarkan frekuensi kemunculan kata. Pendekatan ini efektif untuk kueri teknis eksak, seperti model chipset atau ukuran layar tertentu. Di sisi lain, pendekatan semantik, exemplified by Sentence-BERT, memahami makna dan konteks kueri melalui representasi vektor dens, sehingga efektif untuk kueri berbasis niat (intent-based), seperti "HP untuk fotografi malam hari" atau "laptop murah untuk mahasiswa teknik".

Berdasarkan uraian di atas, diperlukan sebuah mesin pencari vertikal yang khusus mengindeks ulasan dan spesifikasi gadget dari berbagai portal teknologi Indonesia, dengan dukungan kedua pendekatan pencarian leksikal dan semantik, sehingga pengguna dapat menemukan informasi gadget yang relevan secara cepat dan akurat.

## 1.2 Rumusan Masalah

Berdasarkan latar belakang di atas, rumusan masalah dalam penelitian ini adalah sebagai berikut:

1. Bagaimana membangun mesin pencari vertikal yang mengindeks ulasan dan spesifikasi gadget dari tiga portal teknologi Indonesia (Gadgetren, Jagat Review, dan Droidlime)?
2. Bagaimana mengimplementasikan algoritma Okapi BM25 dan Sentence-BERT dalam mesin pencari vertikal gadget?
3. Bagaimana performa Okapi BM25 dan Sentence-BERT dalam mengembalikan hasil pencarian gadget yang relevan, diukur menggunakan Precision@K, Recall@K, F1-Score, dan MAP?

## 1.3 Maksud dan Tujuan

Maksud dari penelitian ini adalah membangun sistem pencarian vertikal untuk ulasan dan spesifikasi gadget yang membantu pengguna menemukan informasi gadek yang relevan secara cepat dan akurat.

Tujuan spesifik dari penelitian ini adalah:

1. Membangun mesin pencari vertikal yang mengumpulkan dan mengindeks 700 hingga 1.000 artikel ulasan gadget dari Gadgetren, Jagat Review, dan Droidlime.
2. Mengimplementasikan algoritma Okapi BM25 untuk pencarian leksikal berbasis kata kunci.
3. Mengimplementasikan algoritma Sentence-BERT untuk pencarian semantik berbasis vektor dens dan cosine similarity.
4. Mengevaluasi performa kedua algoritma menggunakan metrik Precision@K, Recall@K, F1-Score, dan MAP terhadap 10 hingga 15 kueri uji dengan ground truth relevansi.

## 1.4 Manfaat Penelitian

Manfaat dari penelitian ini adalah sebagai berikut:

1. Bagi pengguna umum, mesin pencari ini membantu menemukan informasi ulasan dan spesifikasi gadget dari berbagai portal dalam satu tempat.
2. Bagi mahasiswa dan peneliti, sistem ini menyediakan korpus data ulasan gadget berbahasa Indonesia yang dapat digunakan untuk penelitian lanjutan dalam bidang penelusuran informasi.
3. Bagi pengembang sistem, penelitian ini memberikan referensi implementasi dual-engine retrieval (lexical dan semantic) dalam satu sistem pencarian vertikal.
