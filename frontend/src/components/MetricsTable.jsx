const METRIC_ROWS = [
  { key: "mean_p5", label: "P@5" },
  { key: "mean_p10", label: "P@10" },
  { key: "mean_r5", label: "R@5" },
  { key: "mean_r10", label: "R@10" },
  { key: "mean_f1_5", label: "F1@5" },
  { key: "mean_f1_10", label: "F1@10" },
  { key: "map", label: "MAP" },
  { key: "avg_latency_ms", label: "Latency (ms)" },
];

export default function MetricsTable({ data }) {
  const bm25 = data?.bm25 || {};
  const sbert = data?.sbert || {};

  return (
    <section className="panel p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-slate-900">Perbandingan Metrik Evaluasi</h2>
        <span className="text-xs font-medium text-slate-500 uppercase tracking-wider">
          Okapi BM25 vs Sentence-BERT
        </span>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse border border-slate-200 rounded-xl overflow-hidden">
          <thead>
            <tr className="bg-slate-50 border-b border-slate-200">
              <th className="px-4 py-3 text-xs font-semibold text-slate-500 uppercase border-r border-slate-200 last:border-0">
                Metrik
              </th>
              <th className="px-4 py-3 text-xs font-semibold text-slate-500 uppercase border-r border-slate-200 last:border-0">
                Okapi BM25
              </th>
              <th className="px-4 py-3 text-xs font-semibold text-slate-500 uppercase last:border-0">
                Sentence-BERT
              </th>
            </tr>
          </thead>
          <tbody>
            {METRIC_ROWS.map((row) => (
              <tr key={row.key} className="border-b border-slate-100 last:border-0">
                <td className="px-4 py-3 text-sm text-slate-600 font-medium border-r border-slate-200 last:border-0">
                  {row.label}
                </td>
                <td className="px-4 py-3 text-sm font-mono text-slate-900 border-r border-slate-200 last:border-0">
                  {row.key === "avg_latency_ms"
                    ? (bm25[row.key] ?? 0).toFixed(2)
                    : (bm25[row.key] ?? 0).toFixed(3)}
                </td>
                <td className="px-4 py-3 text-sm font-mono text-slate-900 last:border-0">
                  {row.key === "avg_latency_ms"
                    ? (sbert[row.key] ?? 0).toFixed(2)
                    : (sbert[row.key] ?? 0).toFixed(3)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
