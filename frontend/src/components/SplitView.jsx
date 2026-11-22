import { useState } from "react";
import { Cpu, Sparkles, Download } from "lucide-react";
import ResultCard from "./ResultCard.jsx";
import {
  buildExportFilename,
  buildSearchExport,
  downloadJson,
} from "../utils/exportResults.js";

const ENGINE_BM25 = "bm25";
const ENGINE_SBERT = "sbert";

export default function SplitView({
  bm25Results = [],
  sbertResults = [],
  bm25Latency,
  sbertLatency,
  query = "",
  onResultClick,
}) {
  const [activeEngine, setActiveEngine] = useState(ENGINE_BM25);
  const bm25MaxScore = bm25Results.reduce(
    (max, item) => Math.max(max, Number(item.score) || 0),
    0
  );
  const canExport = Boolean(
    query && (bm25Results.length > 0 || sbertResults.length > 0)
  );

  const handleExport = () => {
    if (!canExport) return;

    downloadJson(
      buildExportFilename(),
      buildSearchExport({
        query,
        bm25Results,
        sbertResults,
        bm25Latency,
        sbertLatency,
      })
    );
  };

  return (
    <section className="w-full">
      <div
        className="mb-3 grid grid-cols-2 gap-1 rounded-xl border border-slate-200 bg-slate-100 p-1 lg:hidden"
        role="group"
        aria-label="Pilih mesin pencari"
      >
        <button
          type="button"
          aria-pressed={activeEngine === ENGINE_BM25}
          onClick={() => setActiveEngine(ENGINE_BM25)}
          className={`inline-flex items-center justify-center gap-1.5 rounded-lg px-2 py-2 text-xs font-semibold transition-colors ${
            activeEngine === ENGINE_BM25
              ? "bg-white text-amber-700 shadow-sm"
              : "text-slate-600"
          }`}
        >
          <Cpu size={14} strokeWidth={1.75} />
          Okapi BM25 ({bm25Results.length})
        </button>
        <button
          type="button"
          aria-pressed={activeEngine === ENGINE_SBERT}
          onClick={() => setActiveEngine(ENGINE_SBERT)}
          className={`inline-flex items-center justify-center gap-1.5 rounded-lg px-2 py-2 text-xs font-semibold transition-colors ${
            activeEngine === ENGINE_SBERT
              ? "bg-white text-indigo-700 shadow-sm"
              : "text-slate-600"
          }`}
        >
          <Sparkles size={14} strokeWidth={1.75} />
          Sentence-BERT ({sbertResults.length})
        </button>
      </div>

      <div className="flex flex-col gap-4 lg:flex-row">
        <div
          className={`panel flex-1 p-4 sm:p-5 ${
            activeEngine === ENGINE_BM25 ? "" : "hidden"
          } lg:block`}
        >
          <div className="mb-4 flex flex-wrap items-center justify-between gap-2">
            <div className="flex items-center gap-2">
              <Cpu size={18} strokeWidth={1.5} className="text-amber-600" />
              <h3 className="font-semibold text-slate-900">Okapi BM25</h3>
            </div>
            <div className="text-right">
              <div className="text-xs font-mono text-slate-400">Latency</div>
              <div className="text-sm font-bold text-slate-900">
                {(Number(bm25Latency) || 0).toFixed(1)} ms
              </div>
            </div>
          </div>
          <div className="mb-2 text-xs font-medium uppercase tracking-wider text-slate-500">
            {bm25Results.length} hasil
          </div>
          <div className="space-y-2">
            {bm25Results.length === 0 ? (
              <div className="py-6 text-center text-sm text-slate-500">
                Tidak ada hasil untuk kata kunci ini.
              </div>
            ) : (
              bm25Results.map((item) => (
                <ResultCard
                  key={item.id}
                  item={item}
                  engine="bm25"
                  maxScore={bm25MaxScore}
                  onResultClick={onResultClick}
                />
              ))
            )}
          </div>
        </div>

        <div
          className={`panel flex-1 p-4 sm:p-5 ${
            activeEngine === ENGINE_SBERT ? "" : "hidden"
          } lg:block`}
        >
          <div className="mb-4 flex flex-wrap items-center justify-between gap-2">
            <div className="flex items-center gap-2">
              <Sparkles
                size={18}
                strokeWidth={1.5}
                className="text-indigo-600"
              />
              <h3 className="font-semibold text-slate-900">Sentence-BERT</h3>
            </div>
            <div className="text-right">
              <div className="text-xs font-mono text-slate-400">Latency</div>
              <div className="text-sm font-bold text-slate-900">
                {(Number(sbertLatency) || 0).toFixed(1)} ms
              </div>
            </div>
          </div>
          <div className="mb-2 text-xs font-medium uppercase tracking-wider text-slate-500">
            {sbertResults.length} hasil
          </div>
          <div className="space-y-2">
            {sbertResults.length === 0 ? (
              <div className="py-6 text-center text-sm text-slate-500">
                Tidak ada hasil untuk kata kunci ini.
              </div>
            ) : (
              sbertResults.map((item) => (
                <ResultCard
                  key={item.id}
                  item={item}
                  engine="sbert"
                  maxScore={1}
                  onResultClick={onResultClick}
                />
              ))
            )}
          </div>
        </div>
      </div>

      <div className="mt-6 flex flex-col items-stretch justify-end gap-2 sm:flex-row sm:items-center">
        <span className="mr-auto hidden text-xs text-slate-500 sm:block">
          Ekspor mencakup hasil kedua engine.
        </span>
        <button
          type="button"
          onClick={handleExport}
          disabled={!canExport}
          className="btn-primary text-sm disabled:pointer-events-none disabled:opacity-60"
          title={
            canExport
              ? "Unduh hasil pencarian dalam format JSON"
              : "Jalankan pencarian terlebih dahulu"
          }
        >
          <Download size={16} strokeWidth={1.75} className="mr-2" />
          Ekspor hasil JSON
        </button>
      </div>
    </section>
  );
}
