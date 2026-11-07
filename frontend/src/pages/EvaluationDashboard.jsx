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
      <section className="panel p-6 flex flex-col items-center justify-center min-h-[300px]">
        <div className="flex flex-col items-center gap-3">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600" />
          <p className="text-slate-600">Memuat data evaluasi...</p>
        </div>
      </section>
    );
  }

  if (error) {
    return (
      <section className="panel p-6 border border-red-200 bg-red-50 text-red-800">
        <div className="flex items-center gap-2 mb-2">
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
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1">
            <BarChart3 size={20} strokeWidth={1.75} className="text-primary-600" />
            <h1 className="text-2xl font-bold text-slate-900 tracking-tight">
              Evaluasi IR
            </h1>
          </div>
          <p className="text-slate-600">
            Bandingkan metrik evaluasi Okapi BM25 dan Sentence-BERT across test
            queries ({testQueriesCount} kueri uji).
          </p>
        </div>
        <button
          onClick={fetchEvaluation}
          className="btn-ghost flex items-center gap-2"
          title="reload evaluation data"
        >
          <RefreshCw size={16} strokeWidth={2} />
          <span className="text-sm font-medium">Muat Ulang</span>
        </button>
      </div>

      {error && (
        <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-800">
          {error}
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="panel p-5">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">
            MAP BM25
          </div>
          <div className="text-2xl font-bold text-slate-900">
            {(bm25.map ?? 0).toFixed(3)}
          </div>
        </div>
        <div className="panel p-5">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">
            MAP S-BERT
          </div>
          <div className="text-2xl font-bold text-slate-900">
            {(sbert.map ?? 0).toFixed(3)}
          </div>
        </div>
        <div className="panel p-5">
          <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-1">
            Rata-rata Latency
          </div>
          <div className="text-2xl font-bold text-slate-900">
            {Math.max(bm25.avg_latency_ms ?? 0, sbert.avg_latency_ms ?? 0).toFixed(2)} ms
          </div>
        </div>
      </div>

      <MetricsTable data={data} />
      <MetricsBarChart data={data} />

      <div className="panel p-6">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold text-slate-900">Inspeksi Per Kueri</h2>
          <span className="text-xs font-medium text-slate-500 uppercase tracking-wider">
            Detail per kueri uji
          </span>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse border border-slate-200 rounded-xl overflow-hidden">
            <thead>
              <tr className="bg-slate-50 border-b border-slate-200">
                <th className="px-4 py-3 text-xs font-semibold text-slate-500 uppercase border-r border-slate-200 last:border-0">
                  Kueri
                </th>
                <th className="px-4 py-3 text-xs font-semibold text-slate-500 uppercase border-r border-slate-200 last:border-0">
                  P@5 BM25
                </th>
                <th className="px-4 py-3 text-xs font-semibold text-slate-500 uppercase border-r border-slate-200 last:border-0">
                  P@5 S-BERT
                </th>
                <th className="px-4 py-3 text-xs font-semibold text-slate-500 uppercase border-r border-slate-200 last:border-0">
                  Latency BM25 (ms)
                </th>
                <th className="px-4 py-3 text-xs font-semibold text-slate-500 uppercase last:border-0">
                  Latency S-BERT (ms)
                </th>
              </tr>
            </thead>
            <tbody>
              {(bm25.per_query_results || []).map((row, index) => {
                const sbertRow = (sbert.per_query_results || [])[index] || {};
                return (
                  <tr key={row.query_id || index} className="border-b border-slate-100 last:border-0">
                    <td className="px-4 py-3 text-sm text-slate-600 font-medium border-r border-slate-200 last:border-0">
                      {row.query_id}
                    </td>
                    <td className="px-4 py-3 text-sm font-mono text-slate-900 border-r border-slate-200 last:border-0">
                      {row["p@5"]?.toFixed(3) ?? "-"}
                    </td>
                    <td className="px-4 py-3 text-sm font-mono text-slate-900 border-r border-slate-200 last:border-0">
                      {sbertRow["p@5"]?.toFixed(3) ?? "-"}
                    </td>
                    <td className="px-4 py-3 text-sm font-mono text-slate-900 border-r border-slate-200 last:border-0">
                      {row.latency_ms?.toFixed(2) ?? "-"}
                    </td>
                    <td className="px-4 py-3 text-sm font-mono text-slate-900 last:border-0">
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
