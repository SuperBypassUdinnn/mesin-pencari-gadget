import { ExternalLink, Cpu, Battery } from "lucide-react";

const SOURCE_BADGE_STYLE = {
  Gadgetren: "badge-gadgetren",
  "Jagat Review": "badge-jagat",
  Droidlime: "badge-droidlime",
};

const DEFAULT_SPEC_CHIPS = ["chipset", "ram", "layar", "baterai", "kamera"];

export default function ResultCard({ item, source = "both", onResultClick }) {
  const specs = item.specs || {};
  const specEntries = Object.entries(specs);

  return (
    <article className="panel p-5">
      <div className="flex items-start justify-between gap-3 mb-3">
        <div className="flex items-center gap-2">
          <span
            className={`badge ${SOURCE_BADGE_STYLE[item.source] || "bg-slate-100 text-slate-700 border-slate-200"}`}
          >
            [{item.source}]
          </span>
          {source === "both" && (
            <span className="badge bg-slate-50 text-slate-600 border-slate-200 text-[10px]">
              {item.source === "Gadgetren" ? "BM25" : "S-BERT"}
            </span>
          )}
        </div>
        <span className="text-xs font-mono text-slate-400">
          {item.latency_ms?.toFixed(1)} ms
        </span>
        <span className="text-xs font-bold text-slate-700 bg-slate-100 px-2 py-0.5 rounded">
          Score {item.score?.toFixed(2) ?? "-"}
        </span>
      </div>

      <h3
        onClick={() => onResultClick && onResultClick(item)}
        className="text-lg font-bold text-slate-900 leading-snug mb-1 cursor-pointer hover:text-primary-600 transition-colors"
      >
        {item.title}
      </h3>
      <div className="flex items-center gap-1.5 text-xs text-slate-500 mb-3">
        <span className="flex items-center gap-1">
          <Cpu size={12} strokeWidth={1.5} />
          {item.category}
        </span>
        <span className="px-1.5 py-0.5 rounded bg-slate-100 text-slate-600">
          {item.date || "-"}
        </span>
      </div>

      <p className="text-sm text-slate-600 leading-relaxed mb-4">
        {item.snippet}
      </p>

      {specEntries.length > 0 && (
        <div className="flex flex-wrap gap-2 mb-4">
          {specEntries.map(([key, value]) => (
            <span key={key} className="chip">
              {String(key).charAt(0).toUpperCase() + String(key).slice(1)}:
              {value}
            </span>
          ))}
        </div>
      )}

      <div className="flex items-center justify-between pt-2 border-t border-slate-100">
        <button
          type="button"
          onClick={() => onResultClick && onResultClick(item)}
          className="text-xs font-semibold text-slate-700 hover:text-primary-600 transition-colors bg-slate-100 hover:bg-slate-200 px-2.5 py-1 rounded"
        >
          Lihat Spesifikasi
        </button>
        <a
          href={item.url}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-1 text-sm font-semibold text-primary-600 hover:text-primary-700 hover:underline transition-colors"
        >
          Buka ulasan lengkap{" "}
          <ExternalLink size={14} strokeWidth={1.75} />
        </a>
      </div>
    </article>
  );
}
