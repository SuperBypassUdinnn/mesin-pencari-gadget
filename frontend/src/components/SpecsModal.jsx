import { useEffect } from "react";
import { X, Layout, FileText, ChevronDown } from "lucide-react";
import { getSourceBadgeClass } from "../utils/sourceBadge.js";

function formatSpecLabel(key) {
  return String(key)
    .replace(/_/g, " ")
    .replace(/\b\w/g, (character) => character.toUpperCase());
}

export default function SpecsModal({ document: doc, onClose }) {
  useEffect(() => {
    if (!doc) return;
    const handleKeyDown = (event) => {
      if (event.key === "Escape") onClose();
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [doc, onClose]);

  if (!doc) return null;

  const specs = doc.specs || {};
  const specEntries = Object.entries(specs);
  const reviewText = doc.content || "";
  const reviewWordCount = reviewText.trim()
    ? reviewText.trim().split(/\s+/).length
    : 0;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4"
      role="dialog"
      aria-modal="true"
      aria-label="Spesifikasi teknis"
    >
      <div
        className="fixed inset-0 bg-slate-900/40 backdrop-blur-sm"
        onClick={onClose}
        aria-hidden="true"
      />
      <div
        className="relative flex max-h-[90vh] w-full max-w-2xl flex-col overflow-hidden panel"
        onClick={(event) => event.stopPropagation()}
      >
        <div className="flex items-start justify-between gap-3 border-b border-slate-200 bg-slate-50 px-4 py-3 sm:px-6 sm:py-4">
          <h2 className="min-w-0 break-words pr-2 text-base font-bold text-slate-900 sm:text-lg">
            Spesifikasi: {doc.title}
          </h2>
          <button
            onClick={onClose}
            className="shrink-0 rounded-lg p-1.5 text-slate-400 transition-colors hover:bg-slate-200 hover:text-slate-900"
            aria-label="Tutup modal"
          >
            <X size={20} strokeWidth={2.25} />
          </button>
        </div>

        <div className="flex-1 space-y-6 overflow-y-auto p-4 sm:p-6">
          <div className="flex flex-wrap items-center gap-2">
            <span className={getSourceBadgeClass(doc.source)}>
              [{doc.source || "Sumber"}]
            </span>
            <span className="badge border border-slate-200 bg-slate-100 text-slate-600">
              {doc.category || "Gadget"}
            </span>
            <span className="text-xs text-slate-500">{doc.date || "-"}</span>
          </div>

          <section>
            <div className="mb-2 flex flex-wrap items-center justify-between gap-2">
              <h3 className="flex items-center gap-2 text-sm font-semibold text-slate-700">
                <Layout size={16} strokeWidth={1.5} className="text-slate-500" />
                Spesifikasi Teknis
              </h3>
              <span className="text-xs text-slate-400">
                {specEntries.length} atribut
              </span>
            </div>

            {specEntries.length > 0 ? (
              <dl className="grid grid-cols-1 gap-2 sm:grid-cols-2">
                {specEntries.map(([key, value]) => (
                  <div
                    key={key}
                    className="rounded-xl border border-slate-200 bg-slate-50 px-3 py-2.5"
                  >
                    <dt className="text-[10px] font-semibold uppercase tracking-wider text-slate-500">
                      {formatSpecLabel(key)}
                    </dt>
                    <dd className="mt-0.5 break-words text-sm font-medium leading-snug text-slate-900">
                      {String(value)}
                    </dd>
                  </div>
                ))}
              </dl>
            ) : (
              <p className="rounded-xl border border-dashed border-slate-300 bg-slate-50 px-4 py-3 text-sm text-slate-500">
                Spesifikasi teknis belum terekstrak untuk dokumen ini.
              </p>
            )}
          </section>

          <section>
            <details className="group overflow-hidden rounded-xl border border-slate-200 bg-white">
              <summary className="flex cursor-pointer list-none items-center justify-between gap-3 px-3 py-3 transition-colors hover:bg-slate-50 [&::-webkit-details-marker]:hidden sm:px-4">
                <span className="flex items-center gap-2 text-sm font-semibold text-slate-700">
                  <FileText
                    size={16}
                    strokeWidth={1.5}
                    className="text-slate-500"
                  />
                  Ulasan Lengkap
                </span>
                <span className="flex items-center gap-2 text-xs text-slate-400">
                  {reviewWordCount > 0
                    ? `${reviewWordCount} kata`
                    : "Tidak tersedia"}
                  <ChevronDown
                    size={16}
                    strokeWidth={1.75}
                    className="transition-transform group-open:rotate-180"
                  />
                </span>
              </summary>
              <div className="border-t border-slate-100 px-3 py-3 sm:px-4">
                <p className="whitespace-pre-line break-words text-sm leading-relaxed text-slate-600">
                  {reviewText || "Konten ulasan tidak tersedia."}
                </p>
              </div>
            </details>

            <p className="mt-3 break-all text-xs text-slate-500">
              Sumber:{" "}
              <a
                href={doc.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-primary-600 hover:underline"
              >
                {doc.url}
              </a>
            </p>
          </section>
        </div>

        <div className="border-t border-slate-200 bg-slate-50 px-4 py-3 sm:px-6 sm:py-4">
          <button onClick={onClose} className="btn-primary w-full">
            Tutup
          </button>
        </div>
      </div>
    </div>
  );
}
