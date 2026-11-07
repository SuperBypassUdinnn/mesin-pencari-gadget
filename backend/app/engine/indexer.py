import json
import os
import sqlite3
from typing import List, Dict, Any
import numpy as np

from backend.app.db import init_db, get_all_documents, insert_document
from backend.app.engine.preprocessor import IndonesianPreprocessor
from backend.app.engine.bm25 import BM25Engine
from backend.app.engine.sbert import SBERTEngine

SEED_GADGET_DATA: List[Dict[str, Any]] = [
    {
        "id": "gadgetren_0001",
        "title": "Review Xiaomi 13T: Performa Kencang Kamera Leica Memukau",
        "source": "Gadgetren",
        "url": "https://gadgetren.com/2023/10/review-xiaomi-13t/",
        "category": "smartphone",
        "date": "2023-10-15",
        "specs": {
            "chipset": "MediaTek Dimensity 8200 Ultra",
            "ram": "12GB LPDDR5",
            "storage": "256GB UFS 3.1",
            "layar": "CrystalRes AMOLED 6.67 inci 144Hz",
            "kamera": "50MP Leica Utama + 50MP Telefoto + 12MP Ultrawide",
            "baterai": "5000 mAh 67W Fast Charging"
        },
        "content": "Xiaomi 13T hadir sebagai smartphone flagship killer dengan kolaborasi Leica yang membawa kemampuan fotografi malam hari dan warna otentik luar biasa. Performa chipset Dimensity 8200 Ultra sangat stabil untuk gaming berat dan multitasking harian tanpa panas berlebih."
    },
    {
        "id": "jagatreview_0001",
        "title": "Review ASUS ROG Zephyrus G14: Laptop Gaming Tipis Kencang",
        "source": "Jagat Review",
        "url": "https://www.jagatreview.com/asus-rog-zephyrus-g14/",
        "category": "laptop",
        "date": "2024-01-20",
        "specs": {
            "prosesor": "AMD Ryzen 9 8945HS",
            "gpu": "NVIDIA GeForce RTX 4070 8GB GDDR6",
            "ram": "32GB LPDDR5X",
            "storage": "1TB NVMe PCIe 4.0 SSD",
            "layar": "14 inci 3K OLED 120Hz ROG Nebula Display",
            "baterai": "73Wh"
        },
        "content": "ASUS ROG Zephyrus G14 2024 membuktikan bahwa laptop gaming bertenaga tinggi bisa dikemas dalam bodi aluminium yang sangat tipis dan ringan. Layar OLED 3K memberikan akurasi warna sempurna untuk editing video, rendering konten kreatif, dan gaming kompetitif."
    },
    {
        "id": "droidlime_0001",
        "title": "Review Samsung Galaxy A54 5G: Raja Menengah dengan Desain Elegan",
        "source": "Droidlime",
        "url": "https://www.droidlime.com/artikel/review-samsung-galaxy-a54-5g/",
        "category": "smartphone",
        "date": "2023-04-10",
        "specs": {
            "chipset": "Exynos 1380 5nm",
            "ram": "8GB + RAM Plus",
            "storage": "256GB",
            "layar": "Super AMOLED 6.4 inci 120Hz",
            "kamera": "50MP OIS Utama + 12MP Ultrawide + 5MP Makro",
            "baterai": "5000 mAh 25W"
        },
        "content": "Samsung Galaxy A54 5G menawarkan ketahanan air dan debu IP67, layar Super AMOLED cerah, dan kamera utama 50MP dengan OIS mumpuni untuk kondisi redup malam hari. Daya tahan baterai 5000 mAh sanggup bertahan lebih dari seharian pemakaian intensif."
    },
    {
        "id": "gadgetren_0002",
        "title": "Review Infinix GT 10 Pro: Smartphone Gaming Desain Futuristik",
        "source": "Gadgetren",
        "url": "https://gadgetren.com/review-infinix-gt-10-pro/",
        "category": "smartphone",
        "date": "2023-08-25",
        "specs": {
            "chipset": "MediaTek Dimensity 8050 6nm",
            "ram": "8GB",
            "storage": "256GB",
            "layar": "AMOLED 6.67 inci 120Hz",
            "kamera": "108MP Utama",
            "baterai": "5000 mAh 45W Fast Charging"
        },
        "content": "Infinix GT 10 Pro mengusung desain mecha cyber futuristik dengan mini LED indikator unik. Performa gaming Dimensity 8050 sangat mulus melibas game kompetitif seperti Mobile Legends dan PUBG Mobile pada pengaturan grafis tinggi."
    },
    {
        "id": "jagatreview_0002",
        "title": "Review Lenovo Legion 5i Pro: Performa Ekstrem Layar WQXGA",
        "source": "Jagat Review",
        "url": "https://www.jagatreview.com/lenovo-legion-5i-pro/",
        "category": "laptop",
        "date": "2023-07-18",
        "specs": {
            "prosesor": "Intel Core i7-13700HX",
            "gpu": "NVIDIA GeForce RTX 4060 8GB TGP 140W",
            "ram": "16GB DDR5 4800MHz",
            "storage": "1TB SSD M.2 NVMe",
            "layar": "16 inci WQXGA 240Hz 500 nits",
            "baterai": "80Wh"
        },
        "content": "Lenovo Legion 5i Pro menawarkan pendingin Coldfront 5.0 yang sangat efektif menjaga suhu prosesor Intel Gen 13 dan GPU RTX 4060 tetap dingin saat rendering berat. Keyboard Legion TrueStrike sangat nyaman untuk mengetik koding maupun gaming intensif."
    }
]

def build_index(db_path: str = "data/gadget.db", processed_dir: str = "data/processed"):
    os.makedirs(processed_dir, exist_ok=True)
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = init_db(db_path)

    docs = get_all_documents(conn)
    if not docs:
        print("[Indexer] SQLite database empty. Seeding initial baseline gadget reviews...")
        for seed_doc in SEED_GADGET_DATA:
            insert_document(conn, seed_doc)
        docs = get_all_documents(conn)

    print(f"[Indexer] Building offline inverted index and embeddings for {len(docs)} documents...")

    # 1. Preprocessing for BM25
    preprocessor = IndonesianPreprocessor()
    bm25_corpus = []
    sbert_corpus = []

    for doc in docs:
        full_text = f"{doc['title']} {doc['content']}"
        tokens = preprocessor.preprocess(full_text)
        bm25_corpus.append({"id": doc["id"], "tokens": tokens})

        # Text for S-BERT
        sbert_corpus.append({"id": doc["id"], "text": full_text})

    # 2. Build and save BM25 Inverted Index
    bm25 = BM25Engine(k1=1.5, b=0.75)
    bm25.fit(bm25_corpus)
    bm25_path = os.path.join(processed_dir, "inverted_index.json")
    bm25.save(bm25_path)
    print(f"[Indexer] BM25 inverted index saved to {bm25_path}")

    # 3. Build and save S-BERT Dense Embeddings
    sbert = SBERTEngine(cache_dir="models/cache")
    sbert.fit(sbert_corpus)
    sbert.save(processed_dir)
    print(f"[Indexer] S-BERT embeddings and doc_ids saved to {processed_dir}")
    print("[Indexer] Offline indexing completed successfully!")

if __name__ == "__main__":
    build_index()
