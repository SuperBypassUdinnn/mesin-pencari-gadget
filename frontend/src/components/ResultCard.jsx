import { ExternalLink, Cpu } from "lucide-react";
import { getSourceBadgeClass } from "../utils/sourceBadge.js";

export default function ResultCard({
  item,
  onResultClick,
  engine = "bm25",
  maxScore,
}) {
  const specs = item.specs || {};
  const specEntries = Object.entries(specs);
  const isSemantic = engine === "sbert";
  const score = Number(item.score);
  const hasScore = Number.isFinite(score);
  const referenceMax = isSemantic
    ? 1
    : Math.max(Number(maxScore) || 0, score || 0);
  const scorePercent =
    hasScore && referenceMax > 0
      ? Math.min(100, Math.max(0, (score / referenceMax) * 100))
      : 0;
  const scoreLabel = isSemantic ? "Cosine Sim" : "BM25 Score";
  const scoreHint = isSemantic
    ? "Kemiripan kosinus 0-1; makin dekat 1, makin mirip."
    : "Skor BM25 relatif terhadap hasil teratas pada kolom ini.";
  const scoreBarClass = isSemantic ? "bg-indigo-500" : "bg-amber-500";

  return (
    <article className="panel p-4 sm:p-5">
      <div className="mb-3 flex flex-wrap items-center gap-2">
        <span className={getSourceBadgeClass(item.source)}>
          [{item.source || "Sumber"}]
        </span>
        <div
          className="ml-auto flex items-center gap-2"
          title={scoreHint}
          aria-label={`${scoreLabel}: ${hasScore ? score.toFixed(2) : "tidak tersedia"}`}
        >
          <div className="text-right">
            <div className="text-[10px] font-semibold uppercase tracking-wider text-slate-400">
              {scoreLabel}
            </div>
            <div className="font-mono text-sm font-bold text-slate-800">
              {hasScore ? score.toFixed(2) : "-"}
            </div>
          </div>
          <div
            className="h-1.5 w-14 overflow-hidden rounded-full bg-slate-100"
            aria-hidden="true"
          >
            <div
              className={`h-full rounded-full ${scoreBarClass}`}
              style={{ width: `${scorePercent}%` }}
            />
          </div>
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
