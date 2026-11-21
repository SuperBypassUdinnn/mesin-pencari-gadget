import { useEffect } from "react";
import { X, Layout } from "lucide-react";

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
          <div className="space-y-3">
            <div className="flex flex-wrap items-center gap-3">
              <span
                className={`badge ${doc.source === "Gadgetren" ? "badge-gadgetren" : doc.source === "Jagat Review" ? "badge-jagat" : "badge-droidlime"}`}
              >
                [{doc.source}]
              </span>
              <span className="text-xs font-mono text-slate-400">
                {doc.category}
              </span>
            </div>
            <p className="break-words text-sm text-slate-600">
              {doc.content || "Konten ulasan tidak tersedia."}
            </p>
            <p className="break-all text-xs text-slate-500">
              Sumber: <a href={doc.url} target="_blank" rel="noopener noreferrer" className="text-primary-600 hover:underline">{doc.url}</a>
            </p>
          </div>

          {specEntries.length > 0 && (
            <section>
              <h3 className="mb-2 flex items-center gap-2 text-sm font-semibold text-slate-700">
                <Layout size={16} strokeWidth={1.5} className="text-slate-500" />
                Spesifikasi Teknis
              </h3>
              <div className="overflow-x-auto">
                <table className="w-full min-w-[320px] border-collapse overflow-hidden rounded-xl border border-slate-200 text-left">
                  <thead>
                    <tr className="bg-slate-50">
                      <th className="border-b border-slate-200 px-4 py-2 text-xs font-semibold uppercase text-slate-500">
                        Aspek
                      </th>
                      <th className="border-b border-slate-200 px-4 py-2 text-xs font-semibold uppercase text-slate-500">
                        Nilai
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {specEntries.map(([key, value]) => (
                      <tr key={key} className="border-b border-slate-100 last:border-0">
                        <td className="px-4 py-3 text-sm font-medium text-slate-600">
                          {String(key).charAt(0).toUpperCase() + String(key).slice(1)}
                        </td>
                        <td className="break-words px-4 py-3 text-sm text-slate-900">
                          {value}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>
          )}
        </div>

        <div className="border-t border-slate-200 bg-slate-50 px-4 py-3 sm:px-6 sm:py-4">
          <button
            onClick={onClose}
            className="btn-primary w-full"
          >
            Tutup
          </button>
        </div>
      </div>
    </div>
  );
}
