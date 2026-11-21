import { useState, useEffect, useCallback } from "react";
import { RefreshCw, AlertCircle, BarChart3 } from "lucide-react";
import { api } from "../services/api.js";
import MetricsTable from "../components/MetricsTable.jsx";
import MetricsBarChart from "../components/MetricsBarChart.jsx";

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

      <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <div className="panel p-5">
          <div className="mb-1 text-xs font-semibold uppercase tracking-wider text-slate-500">
            MAP BM25
          </div>
          <div className="text-2xl font-bold text-slate-900">
            {(bm25.map ?? 0).toFixed(3)}
          </div>
        </div>
        <div className="panel p-5">
          <div className="mb-1 text-xs font-semibold uppercase tracking-wider text-slate-500">
            MAP S-BERT
          </div>
          <div className="text-2xl font-bold text-slate-900">
            {(sbert.map ?? 0).toFixed(3)}
          </div>
        </div>
        <div className="panel p-5">
          <div className="mb-1 text-xs font-semibold uppercase tracking-wider text-slate-500">
            Rata-rata Latency
          </div>
          <div className="text-2xl font-bold text-slate-900">
            {Math.max(bm25.avg_latency_ms ?? 0, sbert.avg_latency_ms ?? 0).toFixed(2)} ms
          </div>
        </div>
      </div>

      <MetricsTable data={data} />
      <MetricsBarChart data={data} />

      <div className="panel p-4 sm:p-6">
        <div className="mb-4 flex flex-wrap items-center justify-between gap-2">
          <h2 className="text-lg font-semibold text-slate-900">Inspeksi Per Kueri</h2>
          <span className="text-xs font-medium uppercase tracking-wider text-slate-500">
            Detail per kueri uji
          </span>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full min-w-[720px] border-collapse overflow-hidden rounded-xl border border-slate-200 text-left">
            <thead>
              <tr className="border-b border-slate-200 bg-slate-50">
                <th className="border-r border-slate-200 px-4 py-3 text-xs font-semibold uppercase text-slate-500 last:border-0">
                  Kueri
                </th>
                <th className="border-r border-slate-200 px-4 py-3 text-xs font-semibold uppercase text-slate-500 last:border-0">
                  P@5 BM25
                </th>
                <th className="border-r border-slate-200 px-4 py-3 text-xs font-semibold uppercase text-slate-500 last:border-0">
                  P@5 S-BERT
                </th>
                <th className="border-r border-slate-200 px-4 py-3 text-xs font-semibold uppercase text-slate-500 last:border-0">
                  Latency BM25 (ms)
                </th>
                <th className="px-4 py-3 text-xs font-semibold uppercase text-slate-500 last:border-0">
                  Latency S-BERT (ms)
                </th>
              </tr>
            </thead>
            <tbody>
              {(bm25.per_query_results || []).map((row, index) => {
                const sbertRow = (sbert.per_query_results || [])[index] || {};
                return (
                  <tr key={row.query_id || index} className="border-b border-slate-100 last:border-0">
                    <td className="border-r border-slate-200 px-4 py-3 text-sm font-medium text-slate-600 last:border-0">
                      {row.query_id}
                    </td>
                    <td className="border-r border-slate-200 px-4 py-3 font-mono text-sm text-slate-900 last:border-0">
                      {row["p@5"]?.toFixed(3) ?? "-"}
                    </td>
                    <td className="border-r border-slate-200 px-4 py-3 font-mono text-sm text-slate-900 last:border-0">
                      {sbertRow["p@5"]?.toFixed(3) ?? "-"}
                    </td>
                    <td className="border-r border-slate-200 px-4 py-3 font-mono text-sm text-slate-900 last:border-0">
                      {row.latency_ms?.toFixed(2) ?? "-"}
                    </td>
                    <td className="px-4 py-3 font-mono text-sm text-slate-900 last:border-0">
                      {sbertRow.latency_ms?.toFixed(2) ?? "-"}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}
