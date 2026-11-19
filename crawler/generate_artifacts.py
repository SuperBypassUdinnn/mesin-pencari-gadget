import json
import math
import os
import sqlite3
from collections import Counter
from typing import Any, Dict, List

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from backend.app.db import get_all_documents


EXACT_QUERY_IDS = {"q01", "q02", "q03", "q04", "q05", "q06", "q07", "q08"}


def _setup_style() -> None:
    plt.rcParams.update(
        {
            "figure.facecolor": "white",
            "axes.facecolor": "#F8FAFC",
            "axes.edgecolor": "#CBD5E1",
            "axes.grid": True,
            "grid.color": "#E2E8F0",
            "grid.linestyle": "--",
            "grid.linewidth": 0.7,
            "font.sans-serif": ["DejaVu Sans", "Arial", "sans-serif"],
            "axes.titlesize": 12,
            "axes.titleweight": "bold",
            "axes.labelsize": 10,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
        }
    )


def generate_metrics_chart(summary: Dict[str, Any], out_path: str) -> None:
    bm25 = summary["bm25"]
    sbert = summary["sbert"]
    labels = ["P@5", "P@10", "R@5", "R@10", "F1@5", "F1@10", "MAP"]
    keys = ["mean_p5", "mean_p10", "mean_r5", "mean_r10", "mean_f1_5", "mean_f1_10", "map"]

    bm25_vals = [float(bm25[k]) for k in keys]
    sbert_vals = [float(sbert[k]) for k in keys]

    x = np.arange(len(labels))
    width = 0.36

    fig, ax = plt.subplots(figsize=(10.5, 5.5))
    bars1 = ax.bar(x - width / 2, bm25_vals, width, label="Okapi BM25", color="#2563EB", edgecolor="#1D4ED8")
    bars2 = ax.bar(x + width / 2, sbert_vals, width, label="Sentence-BERT (MiniLM-L12-v2)", color="#059669", edgecolor="#047857")

    ax.set_ylabel("Skor Metrik (0.0 - 1.0)")
    ax.set_title(f"Perbandingan Kinerja Okapi BM25 vs Sentence-BERT ({summary['queries_count']} Kueri Uji, 900 Dokumen)")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylim(0, max(bm25_vals + sbert_vals) * 1.18)
    ax.legend(frameon=True, facecolor="white", edgecolor="#CBD5E1")

    for bars in (bars1, bars2):
        for bar in bars:
            h = bar.get_height()
            ax.annotate(
                f"{h:.3f}",
                xy=(bar.get_x() + bar.get_width() / 2, h),
                xytext=(0, 4),
                textcoords="offset points",
                ha="center",
                va="bottom",
                fontsize=8,
                color="#1E293B",
            )

    fig.tight_layout()
    fig.savefig(out_path, dpi=300)
    plt.close(fig)


def generate_per_query_ap_chart(
    queries: List[Dict[str, Any]], summary: Dict[str, Any], out_path: str
) -> None:
    bm25_map = {r["query_id"]: r for r in summary["bm25"]["per_query_results"]}
    sbert_map = {r["query_id"]: r for r in summary["sbert"]["per_query_results"]}

    qids = [q["id"] for q in queries]
    x_labels = [
        f"{q['id']}\n({'Eksak' if q['id'] in EXACT_QUERY_IDS else 'Semantik'})"
        for q in queries
    ]
    bm25_aps = [float(bm25_map[qid]["ap"]) for qid in qids]
    sbert_aps = [float(sbert_map[qid]["ap"]) for qid in qids]

    x = np.arange(len(qids))
    width = 0.38

    fig, ax = plt.subplots(figsize=(13.5, 5.8))
    ax.bar(x - width / 2, bm25_aps, width, label="Okapi BM25 (AP)", color="#2563EB")
    ax.bar(x + width / 2, sbert_aps, width, label="Sentence-BERT (AP)", color="#059669")

    ax.axvline(x=7.5, color="#64748B", linestyle=":", linewidth=1.4)
    ax.text(3.5, 1.03, "Kueri Teknis Eksak (q01 - q08)", ha="center", fontsize=9.5, fontweight="bold", color="#334155")
    ax.text(11.0, 1.03, "Kueri Semantik / Niat (q09 - q15)", ha="center", fontsize=9.5, fontweight="bold", color="#334155")

    ax.set_ylabel("Average Precision (AP)")
    ax.set_title("Perbandingan Average Precision Per Kueri: Okapi BM25 vs Sentence-BERT")
    ax.set_xticks(x)
    ax.set_xticklabels(x_labels, fontsize=8)
    ax.set_ylim(0, 1.12)
    ax.legend(loc="upper right", frameon=True, facecolor="white", edgecolor="#CBD5E1")

    fig.tight_layout()
    fig.savefig(out_path, dpi=300)
    plt.close(fig)


def generate_latency_chart(
    queries: List[Dict[str, Any]], summary: Dict[str, Any], out_path: str
) -> None:
    bm25_map = {r["query_id"]: r for r in summary["bm25"]["per_query_results"]}
    sbert_map = {r["query_id"]: r for r in summary["sbert"]["per_query_results"]}

    steady_qids = [q["id"] for q in queries if q["id"] != "q01"]
    bm25_lat = [float(bm25_map[qid]["latency_ms"]) for qid in steady_qids]
    sbert_lat = [float(sbert_map[qid]["latency_ms"]) for qid in steady_qids]

    bm25_steady_mean = float(np.mean(bm25_lat))
    sbert_steady_mean = float(np.mean(sbert_lat))
    cold_q01 = float(sbert_map["q01"]["latency_ms"])

    x = np.arange(len(steady_qids))
    width = 0.38

    fig, ax = plt.subplots(figsize=(12.5, 5.5))
    ax.bar(x - width / 2, bm25_lat, width, label=f"Okapi BM25 (steady avg: {bm25_steady_mean:.2f} ms)", color="#2563EB")
    ax.bar(x + width / 2, sbert_lat, width, label=f"Sentence-BERT (steady avg: {sbert_steady_mean:.2f} ms)", color="#F59E0B")

    ax.axhline(bm25_steady_mean, color="#1D4ED8", linestyle="--", linewidth=1.1)
    ax.axhline(sbert_steady_mean, color="#D97706", linestyle="--", linewidth=1.1)

    ax.set_ylabel("Latensi Eksekusi Kueri (ms)")
    ax.set_title(
        "Perbandingan Latensi Steady-State Per Kueri (q02 - q15)\n"
        f"[Catatan: q01 mencakup cold-start loading model S-BERT sebesar {cold_q01:.1f} ms; total mean: BM25 {summary['bm25']['avg_latency_ms']:.2f} ms vs S-BERT {summary['sbert']['avg_latency_ms']:.2f} ms]"
    )
    ax.set_xticks(x)
    ax.set_xticklabels(steady_qids)
    ax.set_ylim(0, max(sbert_lat) * 1.25)
    ax.legend(frameon=True, facecolor="white", edgecolor="#CBD5E1")

    fig.tight_layout()
    fig.savefig(out_path, dpi=300)
    plt.close(fig)


def generate_corpus_distribution_chart(docs: List[Dict[str, Any]], out_path: str) -> None:
    src_counts = Counter(d["source"] for d in docs)
    cat_counts = Counter(d["category"] for d in docs)

    src_items = sorted(src_counts.items(), key=lambda x: -x[1])
    cat_items = sorted(cat_counts.items(), key=lambda x: -x[1])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.0, 5.2))

    # Panel 1: Source portal distribution
    src_names = [s[0] for s in src_items]
    src_vals = [s[1] for s in src_items]
    colors_src = ["#2563EB", "#059669", "#7C3AED", "#EA580C", "#0891B2"]
    b1 = ax1.barh(src_names[::-1], src_vals[::-1], color=colors_src[: len(src_names)][::-1])
    ax1.set_title("Distribusi Dokumen Berdasarkan Portal Sumber (n=900)")
    ax1.set_xlabel("Jumlah Artikel")
    ax1.set_xlim(0, max(src_vals) * 1.22)
    for bar in b1:
        w = bar.get_width()
        pct = w / len(docs) * 100.0
        ax1.text(w + 4, bar.get_y() + bar.get_height() / 2, f"{int(w)} ({pct:.1f}%)", va="center", fontsize=9)

    # Panel 2: Gadget category distribution
    cat_names = [c[0].capitalize() for c in cat_items]
    cat_vals = [c[1] for c in cat_items]
    b2 = ax2.barh(cat_names[::-1], cat_vals[::-1], color="#0F766E")
    ax2.set_title("Distribusi Dokumen Berdasarkan Kategori Gadget (n=900)")
    ax2.set_xlabel("Jumlah Artikel")
    ax2.set_xlim(0, max(cat_vals) * 1.22)
    for bar in b2:
        w = bar.get_width()
        pct = w / len(docs) * 100.0
        ax2.text(w + 6, bar.get_y() + bar.get_height() / 2, f"{int(w)} ({pct:.1f}%)", va="center", fontsize=9)

    fig.tight_layout()
    fig.savefig(out_path, dpi=300)
    plt.close(fig)


def generate_zipf_chart(inverted_index: Dict[str, Any], out_path: str) -> Dict[str, Any]:
    term_freqs = []
    for term, postings in inverted_index.items():
        total_tf = sum(int(tf) for tf in postings.values())
        term_freqs.append((term, total_tf))
    term_freqs.sort(key=lambda x: -x[1])

    ranks = np.arange(1, len(term_freqs) + 1, dtype=np.float64)
    freqs = np.array([tf for _, tf in term_freqs], dtype=np.float64)

    log_r = np.log10(ranks)
    log_f = np.log10(freqs)
    slope, intercept = np.polyfit(log_r, log_f, 1)
    pred = slope * log_r + intercept
    ss_res = float(np.sum((log_f - pred) ** 2))
    ss_tot = float(np.sum((log_f - np.mean(log_f)) ** 2))
    r2 = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else 0.0

    fig, ax = plt.subplots(figsize=(9.5, 5.5))
    ax.loglog(ranks, freqs, marker=".", markersize=2.5, linestyle="none", color="#2563EB", alpha=0.65, label="Frekuensi Empiris Korpus")
    ax.loglog(ranks, 10 ** pred, color="#DC2626", linewidth=2.0, label=f"Regresi Power-Law (slope={slope:.3f}, R^2={r2:.4f})")

    for idx in (0, 1, 2, 9, 49, 199):
        if idx < len(term_freqs):
            t_lbl, tf_val = term_freqs[idx]
            ax.annotate(
                f"#{idx+1} '{t_lbl}' ({tf_val})",
                xy=(ranks[idx], freqs[idx]),
                xytext=(8, 6),
                textcoords="offset points",
                fontsize=8,
                color="#0F172A",
            )

    ax.set_xlabel("Peringkat Istilah / Rank (skala log10)")
    ax.set_ylabel("Frekuensi Kemunculan Total (skala log10)")
    ax.set_title(f"Distribusi Hukum Zipf Korpus Ulasan Gadget (Kosakata = {len(term_freqs):,} Term Unik)")
    ax.legend(frameon=True, facecolor="white", edgecolor="#CBD5E1")

    fig.tight_layout()
    fig.savefig(out_path, dpi=300)
    plt.close(fig)

    return {
        "zipf_slope": round(float(slope), 4),
        "zipf_r2": round(float(r2), 4),
        "top_terms": [{"rank": i + 1, "term": t, "frequency": c} for i, (t, c) in enumerate(term_freqs[:25])],
    }


def generate_crawling_proof_image(
    log_path: str, docs: List[Dict[str, Any]], stats: Dict[str, Any], out_path: str
) -> None:
    with open(log_path, "r", encoding="utf-8") as lf:
        log_text = lf.read().strip()

    sample_doc = next((d for d in docs if d.get("specs")), docs[0])
    sample_preview = {
        "id": sample_doc["id"],
        "title": sample_doc["title"],
        "source": sample_doc["source"],
        "category": sample_doc["category"],
        "date": sample_doc["date"],
        "url": sample_doc["url"],
        "specs": sample_doc["specs"],
        "content_excerpt": sample_doc["content"][:220] + "...",
    }
    sample_json = json.dumps(sample_preview, ensure_ascii=False, indent=2)

    fig = plt.figure(figsize=(13.5, 8.0), facecolor="#0F172A")
    ax = fig.add_axes([0.02, 0.02, 0.96, 0.96], facecolor="#0F172A")
    ax.axis("off")

    ax.text(
        0.01,
        0.96,
        "BUKTI EKSEKUSI CRAWLER & PENYIMPANAN SQLITE (data/gadget.db)",
        color="#38BDF8",
        fontsize=13,
        fontweight="bold",
        family="monospace",
        va="top",
    )
    ax.text(
        0.01,
        0.91,
        log_text,
        color="#E2E8F0",
        fontsize=8.2,
        family="monospace",
        va="top",
    )

    right_text = (
        "SQLITE SCHEMA & CORPUS INTEGRITY\n"
        "--------------------------------------------------\n"
        f"Database File   : data/gadget.db\n"
        f"Table           : documents (id, title, source, url,\n"
        f"                  category, date, specs_json, content)\n"
        f"Total Rows      : {stats['total_documents']}\n"
        f"Specs Coverage  : {stats['docs_with_specs']}/{stats['total_documents']} ({stats['specs_coverage_pct']:.1f}%)\n"
        f"Vocabulary Size : {stats['vocabulary_size']} unique stemmed tokens\n"
        f"Avg Doc Length  : {stats['avg_words']:.1f} words ({stats['avg_chars']:.1f} chars)\n\n"
        "SAMPLE STRUCTURED DOCUMENT RECORD (JSON)\n"
        "--------------------------------------------------\n"
        + sample_json
    )
    ax.text(
        0.52,
        0.91,
        right_text,
        color="#A7F3D0",
        fontsize=8.0,
        family="monospace",
        va="top",
    )

    fig.savefig(out_path, dpi=220, facecolor="#0F172A")
    plt.close(fig)


def generate_all() -> Dict[str, Any]:
    _setup_style()
    os.makedirs("evaluation_results/charts", exist_ok=True)
    os.makedirs("docs/screenshots/crawling", exist_ok=True)

    conn = sqlite3.connect("data/gadget.db")
    conn.row_factory = sqlite3.Row
    docs = get_all_documents(conn)
    conn.close()

    with open("data/processed/inverted_index.json", "r", encoding="utf-8") as f:
        inv_data = json.load(f)
    with open("data/ground_truth/test_queries.json", "r", encoding="utf-8") as f:
        queries = json.load(f)
    with open("data/ground_truth/relevance_judgments.json", "r", encoding="utf-8") as f:
        truth = json.load(f)
    with open("evaluation_results/metrics_summary.json", "r", encoding="utf-8") as f:
        summary = json.load(f)

    generate_metrics_chart(summary, "evaluation_results/charts/bm25_vs_sbert_metrics.png")
    generate_per_query_ap_chart(queries, summary, "evaluation_results/charts/per_query_ap_comparison.png")
    generate_latency_chart(queries, summary, "evaluation_results/charts/latency_comparison.png")
    generate_corpus_distribution_chart(docs, "evaluation_results/charts/corpus_distribution.png")
    zipf_info = generate_zipf_chart(inv_data["inverted_index"], "evaluation_results/charts/zipf_distribution.png")

    word_counts = [len(d["content"].split()) for d in docs]
    char_counts = [len(d["content"]) for d in docs]
    specs_key_counts = Counter()
    for d in docs:
        for k in d.get("specs", {}):
            specs_key_counts[k] += 1

    with_specs = sum(1 for d in docs if d.get("specs"))
    bm25_res = {r["query_id"]: r for r in summary["bm25"]["per_query_results"]}
    sbert_res = {r["query_id"]: r for r in summary["sbert"]["per_query_results"]}

    steady_bm25_lat = [bm25_res[q["id"]]["latency_ms"] for q in queries if q["id"] != "q01"]
    steady_sbert_lat = [sbert_res[q["id"]]["latency_ms"] for q in queries if q["id"] != "q01"]

    per_query_summary = []
    for q in queries:
        qid = q["id"]
        per_query_summary.append(
            {
                "id": qid,
                "query": q["query"],
                "type": "exact" if qid in EXACT_QUERY_IDS else "semantic",
                "relevant_count": len(truth.get(qid, [])),
                "bm25_p5": round(bm25_res[qid]["p@5"], 4),
                "sbert_p5": round(sbert_res[qid]["p@5"], 4),
                "bm25_ap": round(bm25_res[qid]["ap"], 4),
                "sbert_ap": round(sbert_res[qid]["ap"], 4),
                "bm25_latency_ms": round(bm25_res[qid]["latency_ms"], 3),
                "sbert_latency_ms": round(sbert_res[qid]["latency_ms"], 3),
            }
        )

    stats: Dict[str, Any] = {
        "total_documents": len(docs),
        "source_distribution": dict(sorted(Counter(d["source"] for d in docs).items(), key=lambda x: -x[1])),
        "category_distribution": dict(sorted(Counter(d["category"] for d in docs).items(), key=lambda x: -x[1])),
        "docs_with_specs": with_specs,
        "specs_coverage_pct": round(with_specs / len(docs) * 100.0, 2) if docs else 0.0,
        "specs_key_distribution": dict(specs_key_counts.most_common()),
        "avg_words": round(float(np.mean(word_counts)), 2),
        "median_words": int(np.median(word_counts)),
        "min_words": int(min(word_counts)),
        "max_words": int(max(word_counts)),
        "avg_chars": round(float(np.mean(char_counts)), 2),
        "vocabulary_size": len(inv_data["inverted_index"]),
        "bm25_avgdl": round(float(inv_data["avgdl"]), 2),
        "zipf_slope": zipf_info["zipf_slope"],
        "zipf_r2": zipf_info["zipf_r2"],
        "top_terms": zipf_info["top_terms"],
        "evaluation": {
            "queries_count": len(queries),
            "bm25": {k: round(float(v), 4) for k, v in summary["bm25"].items() if k != "per_query_results"},
            "sbert": {k: round(float(v), 4) for k, v in summary["sbert"].items() if k != "per_query_results"},
            "steady_state_latency_ms": {
                "bm25_q02_to_q15_avg": round(float(np.mean(steady_bm25_lat)), 4),
                "sbert_q02_to_q15_avg": round(float(np.mean(steady_sbert_lat)), 4),
                "sbert_q01_cold_start_ms": round(float(sbert_res["q01"]["latency_ms"]), 4),
            },
            "per_query": per_query_summary,
        },
    }

    stats_path = "docs/screenshots/crawling/corpus_stats.json"
    with open(stats_path, "w", encoding="utf-8") as sf:
        json.dump(stats, sf, ensure_ascii=False, indent=2)

    generate_crawling_proof_image(
        "docs/screenshots/crawling/crawl_execution_log.txt",
        docs,
        stats,
        "docs/screenshots/crawling/corpus_sqlite_summary.png",
    )

    print("[Artifacts] Generated 6 PNG charts/proofs and corpus_stats.json successfully.")
    return stats


if __name__ == "__main__":
    generate_all()
