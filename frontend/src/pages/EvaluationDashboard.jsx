import { useState, useEffect, useCallback } from "react";
import { RefreshCw, AlertCircle, BarChart3, Info } from "lucide-react";
import { api } from "../services/api.js";
import MetricsTable from "../components/MetricsTable.jsx";
import MetricsBarChart from "../components/MetricsBarChart.jsx";
import { getEvaluationQueryMeta } from "../data/evaluationQueries.js";

function StatCard({ label, value, caption }) {
  return (
    <div className="panel p-5">
      <div className="mb-1 text-xs font-semibold uppercase tracking-wider text-slate-500">
        {label}
      </div>
      <div className="text-2xl font-bold text-slate-900">{value}</div>
      <div className="mt-1 text-xs text-slate-500">{caption}</div>
    </div>
  );
}

function queryTypeClass(type) {
  if (type === "Eksak") {
    return "border border-blue-100 bg-blue-50 text-blue-700";
  }
  if (type === "Semantik") {
    return "border border-violet-100 bg-violet-50 text-violet-700";
  }
  return "border border-slate-200 bg-slate-100 text-slate-600";
}

export default function EvaluationDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchEvaluation = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await api.getEvaluation();
      setData(result);
    } catch (err) {
      setError("Gagal memuat data evaluasi. Pastikan backend berjalan di http://localhost:8000");
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchEvaluation();
  }, [fetchEvaluation]);

  if (loading) {
    return (
      <section className="panel flex min-h-[300px] flex-col items-center justify-center p-6">
        <div className="flex flex-col items-center gap-3">
          <div className="h-8 w-8 animate-spin rounded-full border-b-2 border-primary-600" />
          <p className="text-slate-600">Memuat data evaluasi...</p>
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section className="panel border border-red-200 bg-red-50 p-6 text-red-800">
        <div className="mb-2 flex items-center gap-2">
          <AlertCircle size={18} strokeWidth={1.75} />
          <span className="font-semibold">Gagal memuat evaluasi</span>
        </div>
        <p className="text-sm">{error}</p>
        <button
          onClick={fetchEvaluation}
          className="mt-4 inline-flex items-center gap-1 text-sm font-semibold text-primary-600 hover:underline"
        >
          <RefreshCw size={14} strokeWidth={2} />
          Muat ulang
        </button>
      </section>
    );
  }

  const bm25 = data.bm25 || {};
  const sbert = data.sbert || {};
  const testQueriesCount = data.test_queries_count || 0;
  const bm25Rows = bm25.per_query_results || [];
  const sbertRows = sbert.per_query_results || [];
  const sbertByQuery = new Map(
    sbertRows.map((row, index) => [row.query_id || `index-${index}`, row])
  );

  return (
    <section className="space-y-6">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-start sm:justify-between">
        <div className="min-w-0 flex-1">
          <div className="mb-1 flex items-center gap-2">
            <BarChart3 size={20} strokeWidth={1.75} className="text-primary-600" />
            <h1 className="text-xl font-bold tracking-tight text-slate-900 sm:text-2xl">
              Evaluasi IR
            </h1>
          </div>
          <p className="text-slate-600">
            Bandingkan metrik evaluasi Okapi BM25 dan Sentence-BERT pada{" "}
            {testQueriesCount} kueri uji.
          </p>
        </div>
        <button
          onClick={fetchEvaluation}
          className="btn-ghost flex shrink-0 items-center gap-2 self-start sm:self-auto"
          title="reload evaluation data"
        >
          <RefreshCw size={16} strokeWidth={2} />
          <span className="text-sm font-medium">Muat Ulang</span>
        </button>
      </div>

      <div className="panel grid grid-cols-1 gap-3 p-4 text-sm text-slate-600 sm:grid-cols-2 sm:p-5">
        <div className="flex gap-2">
          <Info size={16} strokeWidth={1.75} className="mt-0.5 shrink-0 text-amber-600" />
          <p>
            <span className="font-semibold text-slate-800">BM25:</span> skor
            leksikal tidak dibatasi. Perbandingan adil dilakukan lewat MAP/P@K
            (0-1), bukan angka skor mentah.
          </p>
        </div>
        <div className="flex gap-2">
          <Info size={16} strokeWidth={1.75} className="mt-0.5 shrink-0 text-indigo-600" />
          <p>
            <span className="font-semibold text-slate-800">Sentence-BERT:</span>{" "}
            cosine similarity 0-1. Nilai 0,87 berarti vektor kueri dan dokumen
            sangat mirip.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard
          label="MAP BM25"
          value={(bm25.map ?? 0).toFixed(3)}
          caption="0-1, makin tinggi makin baik"
        />
        <StatCard
          label="MAP S-BERT"
          value={(sbert.map ?? 0).toFixed(3)}
          caption="0-1, makin tinggi makin baik"
        />
        <StatCard
          label="Latency BM25"
          value={`${(bm25.avg_latency_ms ?? 0).toFixed(2)} ms`}
          caption="Rata-rata per kueri"
        />
        <StatCard
          label="Latency S-BERT"
          value={`${(sbert.avg_latency_ms ?? 0).toFixed(2)} ms`}
          caption="Rata-rata per kueri"
        />
      </div>

      <MetricsTable data={data} />
      <MetricsBarChart data={data} />

      <div className="panel p-4 sm:p-6">
        <div className="mb-1 flex flex-wrap items-center justify-between gap-2">
          <h2 className="text-lg font-semibold text-slate-900">Inspeksi Per Kueri</h2>
          <span className="text-xs font-medium uppercase tracking-wider text-slate-500">
            {bm25Rows.length} kueri uji
          </span>
        </div>
        <p className="mb-4 text-xs text-slate-500">
          Kueri eksak menargetkan istilah teknis atau model tertentu; kueri
          semantik menargetkan kebutuhan pengguna dalam bahasa alami.
        </p>
        <div className="overflow-x-auto">
          <table className="w-full min-w-[900px] border-collapse overflow-hidden rounded-xl border border-slate-200 text-left">
            <thead>
              <tr className="border-b border-slate-200 bg-slate-50">
                <th className="border-r border-slate-200 px-4 py-3 text-xs font-semibold uppercase text-slate-500">
                  Kueri
                </th>
                <th className="border-r border-slate-200 px-4 py-3 text-xs font-semibold uppercase text-slate-500">
                  Tipe
                </th>
                <th className="border-r border-slate-200 px-4 py-3 text-xs font-semibold uppercase text-slate-500">
                  P@5 BM25
                </th>
                <th className="border-r border-slate-200 px-4 py-3 text-xs font-semibold uppercase text-slate-500">
                  P@5 S-BERT
                </th>
                <th className="border-r border-slate-200 px-4 py-3 text-xs font-semibold uppercase text-slate-500">
                  Latency BM25 (ms)
                </th>
                <th className="px-4 py-3 text-xs font-semibold uppercase text-slate-500">
                  Latency S-BERT (ms)
                </th>
              </tr>
            </thead>
            <tbody>
              {bm25Rows.length === 0 ? (
                <tr className="border-b border-slate-100 last:border-0">
                  <td
                    colSpan={6}
                    className="px-4 py-6 text-center text-sm text-slate-500"
                  >
                    Data per kueri tidak tersedia.
                  </td>
                </tr>
              ) : (
                bm25Rows.map((row, index) => {
                  const queryId =
                    row.query_id || `q${String(index + 1).padStart(2, "0")}`;
                  const sbertRow =
                    sbertByQuery.get(row.query_id) ||
                    sbertRows[index] ||
                    {};
                  const meta = getEvaluationQueryMeta(queryId, row);

                  return (
                    <tr
                      key={queryId}
                      className="border-b border-slate-100 last:border-0"
                    >
                      <td className="border-r border-slate-200 px-4 py-3">
                        <div className="font-mono text-xs uppercase text-slate-400">
                          {queryId}
                        </div>
                        <div className="mt-0.5 min-w-[220px] max-w-[320px] text-sm font-medium text-slate-700">
                          {meta.text}
                        </div>
                      </td>
                      <td className="border-r border-slate-200 px-4 py-3">
                        <span className={`badge ${queryTypeClass(meta.type)}`}>
                          {meta.type}
                        </span>
                      </td>
                      <td className="border-r border-slate-200 px-4 py-3 font-mono text-sm text-slate-900">
                        {row["p@5"]?.toFixed(3) ?? "-"}
                      </td>
                      <td className="border-r border-slate-200 px-4 py-3 font-mono text-sm text-slate-900">
                        {sbertRow["p@5"]?.toFixed(3) ?? "-"}
                      </td>
                      <td className="border-r border-slate-200 px-4 py-3 font-mono text-sm text-slate-900">
                        {row.latency_ms?.toFixed(2) ?? "-"}
                      </td>
                      <td className="px-4 py-3 font-mono text-sm text-slate-900">
                        {sbertRow.latency_ms?.toFixed(2) ?? "-"}
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}
