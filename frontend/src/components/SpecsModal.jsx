import { useState } from "react";
import { X, Cpu, Battery, Layout } from "lucide-react";

export default function SpecsModal({ document: doc, onClose }) {
  const isOpen = !!doc;
  if (!isOpen) return null;

  const specs = doc.specs || {};
  const specEntries = Object.entries(specs);

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center"
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
        className="relative w-full max-w-2xl max-h-[90vh] flex flex-col panel overflow-hidden"
        onClick={(event) => event.stopPropagation()}
      >
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-200 bg-slate-50">
          <h2 className="text-lg font-bold text-slate-900">
            Spesifikasi: {doc.title}
          </h2>
          <button
            onClick={onClose}
            className="rounded-lg p-1.5 text-slate-400 hover:bg-slate-200 hover:text-slate-900 transition-colors"
            aria-label="Tutup modal"
          >
            <X size={20} strokeWidth={2.25} />
          </button>
        </div>

        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          <div className="space-y-3">
            <div className="flex items-center gap-3">
              <span
                className={`badge ${doc.source === "Gadgetren" ? "badge-gadgetren" : doc.source === "Jagat Review" ? "badge-jagat" : "badge-droidlime"}`}
              >
                [{doc.source}]
              </span>
              <span className="text-xs font-mono text-slate-400">
                {doc.category}
              </span>
            </div>
            <p className="text-sm text-slate-600">
              {doc.content || "Konten ulasan tidak tersedia."}
            </p>
            <p className="text-xs text-slate-500">
              Sumber: <a href={doc.url} target="_blank" rel="noopener noreferrer" className="text-primary-600 hover:underline">{doc.url}</a>
            </p>
          </div>

          {specEntries.length > 0 && (
            <section>
              <h3 className="text-sm font-semibold text-slate-700 mb-2 flex items-center gap-2">
                <Layout size={16} strokeWidth={1.5} className="text-slate-500" />
                Spesifikasi Teknis
              </h3>
              <table className="w-full text-left border-collapse border border-slate-200 rounded-xl overflow-hidden">
                <thead>
                  <tr className="bg-slate-50">
                    <th className="px-4 py-2 text-xs font-semibold text-slate-500 uppercase border-b border-slate-200">
                      Aspek
                    </th>
                    <th className="px-4 py-2 text-xs font-semibold text-slate-500 uppercase border-b border-slate-200">
                      Nilai
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {specEntries.map(([key, value]) => (
                    <tr key={key} className="border-b border-slate-100 last:border-0">
                      <td className="px-4 py-3 text-sm text-slate-600 font-medium">
                        {String(key).charAt(0).toUpperCase() + String(key).slice(1)}
                      </td>
                      <td className="px-4 py-3 text-sm text-slate-900">
                        {value}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </section>
          )}
        </div>

        <div className="px-6 py-4 border-t border-slate-200 bg-slate-50">
          <button
            onClick={onClose}
            className="w-full btn-primary"
          >
            Tutup
          </button>
        </div>
      </div>
    </div>
  );
}
