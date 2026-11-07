import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";

const METRIC_SERIES = [
  { key: "map", label: "MAP" },
  { key: "mean_p5", label: "P@5" },
  { key: "mean_r5", label: "R@5" },
  { key: "mean_f1_5", label: "F1@5" },
];

export default function MetricsBarChart({ data }) {
  const bm25 = data?.bm25 || {};
  const sbert = data?.sbert || {};

  const chartData = METRIC_SERIES.map((series) => ({
    metric: series.label,
    "Okapi BM25": bm25[series.key] ?? 0,
    "Sentence-BERT": sbert[series.key] ?? 0,
  }));

  return (
    <section className="panel p-6">
      <h2 className="text-lg font-semibold text-slate-900 mb-4">
        Visualisasi Perbandingan Metrik
      </h2>
      <div className="h-64 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData}>
            <XAxis dataKey="metric" />
            <YAxis domain={[0, 1]} />
            <Tooltip />
            <Legend />
            <Bar dataKey="Okapi BM25" fill="#3b82f6" radius={[4, 4, 0, 0]} />
            <Bar dataKey="Sentence-BERT" fill="#6366f1" radius={[4, 4, 0, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
      <p className="mt-3 text-xs text-slate-500 text-center">
        Skor dinamormalisasi ke rentang 0 hingga 1 untuk membandingkan performa
        Okapi BM25 dengan Sentence-BERT.
      </p>
    </section>
  );
}
