from collections import Counter
import json
import os
import time
from typing import Any, Dict, List
from backend.app.db import init_db, insert_document
from crawler.spiders.droidlime import DroidlimeSpider
from crawler.spiders.gadgetren import GadgetrenSpider
from crawler.spiders.hybrid import HybridSpider
from crawler.spiders.jagatreview import JagatReviewSpider
from crawler.spiders.yangcanggih import YangcanggihSpider


def _log(lines: List[str], message: str) -> None:
    print(message)
    lines.append(message)


def run_crawler(
    target_total: int = 900,
    db_path: str = "data/gadget.db",
    raw_json_path: str = "data/raw/documents.json",
    fresh: bool = True,
    log_path: str = "docs/screenshots/crawling/crawl_execution_log.txt",
) -> List[Dict[str, Any]]:
    """Run multi-source Indonesian gadget review spiders and persist to JSON + SQLite."""
    start_time = time.perf_counter()
    log_lines: List[str] = []

    os.makedirs(os.path.dirname(raw_json_path), exist_ok=True)
    if os.path.dirname(db_path):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
    if log_path and os.path.dirname(log_path):
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

    conn = init_db(db_path)
    if fresh:
        with conn:
            conn.execute("DELETE FROM documents")
        _log(log_lines, f"[MainCrawler] Cleared previous rows in {db_path} (fresh crawl mode).")

    all_documents: List[Dict[str, Any]] = []
    seen_urls = set()
    seen_titles = set()

    _log(
        log_lines,
        f"[MainCrawler] Starting multi-source Indonesian gadget crawler (target={target_total})...",
    )

    # Check Gadgetren availability first; respects HTTP 403 policy without bypass.
    gadgetren = GadgetrenSpider(delay_seconds=0.4)
    _log(log_lines, "[MainCrawler] Probing GadgetrenSpider...")
    try:
        g_docs = gadgetren.crawl(max_documents=int(target_total * 0.15))
        _log(log_lines, f"[MainCrawler] Gadgetren returned {len(g_docs)} documents.")
        for doc in g_docs:
            norm_u = doc["url"].rstrip("/").lower()
            norm_t = doc["title"].strip().lower()
            if norm_u not in seen_urls and norm_t not in seen_titles:
                seen_urls.add(norm_u)
                seen_titles.add(norm_t)
                insert_document(conn, doc)
                all_documents.append(doc)
    except Exception as e:
        _log(log_lines, f"[MainCrawler] Gadgetren check ended with notice: {e}")

    # Primary WP REST API spiders covering 100% of remaining target_total.
    remaining_target = max(0, target_total - len(all_documents))
    q_jagat = int(round(remaining_target * 0.33))
    q_yang = int(round(remaining_target * 0.33))
    q_droid = int(round(remaining_target * 0.20))
    q_hybrid = max(0, remaining_target - (q_jagat + q_yang + q_droid))

    spiders = [
        (JagatReviewSpider(delay_seconds=0.4), q_jagat),
        (YangcanggihSpider(delay_seconds=0.4), q_yang),
        (DroidlimeSpider(delay_seconds=0.4), q_droid),
        (HybridSpider(delay_seconds=0.4), q_hybrid),
    ]

    shortfall = 0
    for idx, (spider, quota) in enumerate(spiders):
        effective_quota = quota + shortfall
        if effective_quota <= 0:
            continue
        _log(
            log_lines,
            f"[MainCrawler] Launching {spider.name} (target quota: {effective_quota} docs)...",
        )
        try:
            docs = spider.crawl(max_documents=effective_quota)
            accepted = 0
            for doc in docs:
                norm_u = doc["url"].rstrip("/").lower()
                norm_t = doc["title"].strip().lower()
                if norm_u in seen_urls or norm_t in seen_titles:
                    continue
                seen_urls.add(norm_u)
                seen_titles.add(norm_t)
                insert_document(conn, doc)
                all_documents.append(doc)
                accepted += 1
            shortfall = max(0, effective_quota - accepted)
            _log(
                log_lines,
                f"[MainCrawler] {spider.name} extracted {len(docs)} docs, stored {accepted} unique docs.",
            )
        except Exception as e:
            shortfall = effective_quota
            _log(log_lines, f"[MainCrawler] Error running {spider.name}: {e}")

    with open(raw_json_path, "w", encoding="utf-8") as f:
        json.dump(all_documents, f, ensure_ascii=False, indent=2)

    elapsed = time.perf_counter() - start_time
    total_docs = len(all_documents)
    source_counts = Counter(doc["source"] for doc in all_documents)
    cat_counts = Counter(doc["category"] for doc in all_documents)
    with_specs = sum(1 for doc in all_documents if doc.get("specs"))
    avg_chars = (
        sum(len(doc["content"]) for doc in all_documents) / total_docs if total_docs else 0.0
    )
    avg_words = (
        sum(len(doc["content"].split()) for doc in all_documents) / total_docs if total_docs else 0.0
    )
    specs_pct = (with_specs / total_docs * 100.0) if total_docs else 0.0

    _log(log_lines, "=" * 60)
    _log(log_lines, "[MainCrawler] CRAWL SUMMARY")
    _log(log_lines, f"Total unique documents : {total_docs}")
    _log(log_lines, f"Elapsed time           : {elapsed:.2f} s")
    _log(log_lines, f"Average content length : {avg_chars:.1f} chars ({avg_words:.1f} words)")
    _log(log_lines, f"Specs extraction rate  : {with_specs}/{total_docs} ({specs_pct:.1f}%)")
    _log(log_lines, "Distribution by source :")
    for src, cnt in sorted(source_counts.items(), key=lambda x: -x[1]):
        _log(log_lines, f"  - {src}: {cnt}")
    _log(log_lines, "Distribution by category:")
    for cat, cnt in sorted(cat_counts.items(), key=lambda x: -x[1]):
        _log(log_lines, f"  - {cat}: {cnt}")
    _log(log_lines, f"Saved raw JSON         : {raw_json_path}")
    _log(log_lines, f"Saved SQLite DB        : {db_path}")
    _log(log_lines, "=" * 60)

    if log_path:
        with open(log_path, "w", encoding="utf-8") as lf:
            lf.write("\n".join(log_lines) + "\n")

    conn.close()
    return all_documents


if __name__ == "__main__":
    run_crawler()
