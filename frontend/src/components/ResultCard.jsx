import { ExternalLink, Cpu } from "lucide-react";

const SOURCE_BADGE_STYLE = {
  Gadgetren: "badge-gadgetren",
  "Jagat Review": "badge-jagat",
  Droidlime: "badge-droidlime",
  Yangcanggih: "badge-yangcanggih",
  Hybrid: "badge-hybrid",
};

export default function ResultCard({ item, onResultClick }) {
  const specs = item.specs || {};
  const specEntries = Object.entries(specs);

  return (
    <article className="panel p-4 sm:p-5">
      <div className="mb-3 flex flex-wrap items-center gap-2">
        <span
          className={`badge ${SOURCE_BADGE_STYLE[item.source] || "bg-slate-100 text-slate-700 border-slate-200"}`}
        >
          [{item.source}]
        </span>
        <div className="ml-auto flex items-center gap-2">
          <span className="font-mono text-xs text-slate-400">
            {item.latency_ms?.toFixed(1)} ms
          </span>
          <span className="rounded bg-slate-100 px-2 py-0.5 text-xs font-bold text-slate-700">
            Score {item.score?.toFixed(2) ?? "-"}
          </span>
        </div>
      </div>

      <h3
        onClick={() => onResultClick && onResultClick(item.id)}
        className="mb-1 cursor-pointer break-words text-lg font-bold leading-snug text-slate-900 transition-colors hover:text-primary-600"
      >
        {item.title}
      </h3>
      <div className="mb-3 flex flex-wrap items-center gap-1.5 text-xs text-slate-500">
        <span className="flex items-center gap-1">
          <Cpu size={12} strokeWidth={1.5} />
          {item.category}
        </span>
        <span className="rounded bg-slate-100 px-1.5 py-0.5 text-slate-600">
          {item.date || "-"}
        </span>
      </div>

      <p className="mb-4 break-words text-sm leading-relaxed text-slate-600">
        {item.snippet}
      </p>

      {specEntries.length > 0 && (
        <div className="mb-4 flex flex-wrap gap-2">
          {specEntries.map(([key, value]) => (
            <span key={key} className="chip max-w-full break-words">
              {String(key).charAt(0).toUpperCase() + String(key).slice(1)}:
              {value}
            </span>
          ))}
        </div>
      )}

      <div className="flex flex-col gap-2 border-t border-slate-100 pt-2 sm:flex-row sm:items-center sm:justify-between">
        <button
          type="button"
          onClick={() => onResultClick && onResultClick(item.id)}
          className="rounded bg-slate-100 px-2.5 py-1 text-xs font-semibold text-slate-700 transition-colors hover:bg-slate-200 hover:text-primary-600"
        >
          Lihat Spesifikasi
        </button>
        <a
          href={item.url}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center gap-1 break-words text-sm font-semibold text-primary-600 transition-colors hover:text-primary-700 hover:underline"
        >
          Buka ulasan lengkap{" "}
          <ExternalLink size={14} strokeWidth={1.75} />
        </a>
      </div>
    </article>
  );
}
