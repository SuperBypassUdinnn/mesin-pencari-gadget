# BAB I Pendahuluan

## 1.1 Latar Belakang

Perkembangan teknologi informasi dan komunikasi telah mengubah pola konsumsi masyarakat terhadap produk elektronik, terutama gadget seperti smartphone, laptop, tablet, perangkat wearable, audio, dan kamera. Saat ini, informasi mengenai ulasan mendalam dan spesifikasi teknis gadget berbahasa Indonesia tersebar di banyak portal teknologi, seperti Jagat Review, Yangcanggih, Droidlime, Gadgetren, dan Hybrid. Setiap portal memiliki format, struktur HTML, tata letak tabel spesifikasi, serta gaya penulisan yang berbeda-beda, sehingga menyulitkan pengguna untuk membandingkan ulasan dan spesifikasi antarproduk secara terpadu.

Masalah utama yang dihadapi pengguna adalah ketersediaan informasi yang terpecah dan tidak terstruktur. Ulasan kamera sebuah smartphone dapat berada di satu portal, sedangkan pengujian daya tahan baterai atau performa gaming berada di portal lain. Di sisi lain, mesin pencari umum berskala luas menampilkan hasil yang terlalu heterogen, sering kali didominasi oleh halaman toko daring, forum diskusi, atau iklan komersial, sehingga pengguna harus menyaring artikel ulasan teknis secara manual.

Dalam bidang penelusuran informasi (information retrieval), terdapat dua pendekatan utama untuk mencocokkan kueri pengguna dengan dokumen, yaitu pendekatan leksikal dan pendekatan semantik. Pendekatan leksikal seperti Okapi BM25 menghitung relevansi berdasarkan frekuensi kemunculan kata kunci dan normalisasi panjang dokumen. Pendekatan ini sangat kuat untuk kueri teknis eksak yang mencantumkan kode chipset, jenis panel layar, atau model GPU tertentu. Sebaliknya, pendekatan semantik seperti Sentence-BERT merepresentasikan teks dalam bentuk vektor dens (dense vector) guna menangkap makna kontekstual, sehingga mampu mengatasi sinonim dan ambiguitas bahasa pada kueri berbasis niat (intent-based), misalnya "HP baterai tahan lama seharian tanpa sering cas".

Berdasarkan latar belakang tersebut, proyek ini membangun sebuah mesin pencari vertikal khusus ulasan dan spesifikasi gadget berbahasa Indonesia yang menggabungkan korpus multi-sumber berskala ratusan artikel serta membandingkan performa algoritma Okapi BM25 dan Sentence-BERT secara langsung melalui antarmuka side-by-side dan dasbor evaluasi kuantitatif.

## 1.2 Rumusan Masalah

Berdasarkan latar belakang di atas, rumusan masalah dalam penelitian ini adalah sebagai berikut:

1. Bagaimana merancang dan membangun crawler multi-sumber yang mengumpulkan, membersihkan, dan mengekstrak spesifikasi teknis dari minimal 300 artikel ulasan gadget berbahasa Indonesia dari portal teknologi populer (Jagat Review, Yangcanggih, Droidlime, Gadgetren, dan Hybrid)?
2. Bagaimana mengimplementasikan dan membandingkan algoritma penelusuran leksikal Okapi BM25 dengan pendekatan semantik Sentence-BERT pada korpus terindeks berbahasa Indonesia?
3. Bagaimana kinerja kuantitatif kedua algoritma tersebut ketika dievaluasi menggunakan metrik Precision@K, Recall@K, F1-Score, Mean Average Precision (MAP), dan latensi eksekusi pada kueri teknis eksak maupun kueri semantik?

## 1.3 Maksud dan Tujuan

Maksud dari penelitian ini adalah membangun prototipe sistem penelusuran informasi vertikal untuk ulasan dan spesifikasi gadget yang membantu pengguna menemukan informasi gadget yang relevan secara cepat, terstruktur, dan akurat.

Tujuan spesifik dari penelitian ini adalah:

1. Mengumpulkan dan menyimpan korpus sebanyak 900 artikel ulasan gadget berbahasa Indonesia dari lima portal teknologi (Jagat Review, Yangcanggih, Droidlime, Gadgetren, dan Hybrid) ke dalam database SQLite dan arsip JSON terstruktur beserta ekstraksi spesifikasi teknis.
2. Membangun pipeline prapemrosesan teks Bahasa Indonesia dengan PySastrawi dan struktur data Inverted Index untuk algoritma Okapi BM25 ($k_1 = 1{,}5$, $b = 0{,}75$).
3. Mengimplementasikan pencarian semantik menggunakan model multibahasa Sentence-BERT (`paraphrase-multilingual-MiniLM-L12-v2`) dengan normalisasi L2 dan perhitungan Cosine Similarity berbasis NumPy.
4. Mengevaluasi dan membandingkan performa kedua algoritma menggunakan metrik Precision@5, Precision@10, Recall@5, Recall@10, F1-Score, MAP, dan latensi terhadap 15 kueri uji berlabel ground truth serta menampilkannya dalam antarmuka web interaktif.

## 1.4 Manfaat Penelitian

Manfaat dari penelitian ini adalah sebagai berikut:

1. Bagi pengguna umum dan calon pembeli gadget, sistem ini mempermudah pencarian serta perbandingan ulasan dan spesifikasi teknis dari berbagai portal teknologi tepercaya dalam satu antarmuka terpadu.
2. Bagi mahasiswa dan peneliti bidang Information Retrieval, proyek ini menyediakan korpus terkurasi berisi 900 artikel ulasan gadget berbahasa Indonesia lengkap dengan ground truth 15 kueri uji sebagai bahan eksperimen lanjutan.
3. Bagi pengembang sistem, penelitian ini menyajikan implementasi nyata arsitektur dual-engine retrieval (leksikal dan semantik) yang siap dijalankan secara terkontainerisasi dengan Docker Compose.
