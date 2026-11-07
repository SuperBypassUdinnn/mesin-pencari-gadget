import json
import os
from typing import List, Dict, Any
from backend.app.db import init_db, insert_document
from crawler.spiders.gadgetren import GadgetrenSpider
from crawler.spiders.jagatreview import JagatReviewSpider
from crawler.spiders.droidlime import DroidlimeSpider

def run_crawler(target_total: int = 800, db_path: str = "data/gadget.db", raw_json_path: str = "data/raw/documents.json"):
    os.makedirs(os.path.dirname(raw_json_path), exist_ok=True)
    conn = init_db(db_path)
    all_documents: List[Dict[str, Any]] = []

    print("[MainCrawler] Starting multi-source tech gadget crawler...")
    spiders = [
        (GadgetrenSpider(delay_seconds=0.8), int(target_total * 0.45)),   # ~360
        (JagatReviewSpider(delay_seconds=0.8), int(target_total * 0.35)), # ~280
        (DroidlimeSpider(delay_seconds=0.8), int(target_total * 0.20))    # ~160
    ]

    for spider, quota in spiders:
        print(f"[MainCrawler] Launching {spider.name} (target: {quota} docs)...")
        try:
            docs = spider.crawl(max_documents=quota)
            print(f"[MainCrawler] {spider.name} successfully extracted {len(docs)} documents.")
            for doc in docs:
                insert_document(conn, doc)
                all_documents.append(doc)
        except Exception as e:
            print(f"[MainCrawler] Error running {spider.name}: {e}")

    # Write unified JSON
    with open(raw_json_path, "w", encoding="utf-8") as f:
        json.dump(all_documents, f, ensure_ascii=False, indent=2)

    print(f"[MainCrawler] Crawl complete. Total {len(all_documents)} documents saved to {raw_json_path} and SQLite {db_path}.")

if __name__ == "__main__":
    run_crawler()
