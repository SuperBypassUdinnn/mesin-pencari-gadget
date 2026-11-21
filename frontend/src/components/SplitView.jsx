import { Cpu, Sparkles } from "lucide-react";
import ResultCard from "./ResultCard.jsx";

export default function SplitView({ bm25Results, sbertResults, bm25Latency, sbertLatency, onResultClick }) {
  return (
    <section className="w-full">
      <div className="flex flex-col gap-4 lg:flex-row">
        <div className="panel flex-1 p-4 sm:p-5">
          <div className="mb-4 flex flex-wrap items-center justify-between gap-2">
            <div className="flex items-center gap-2">
              <Cpu size={18} strokeWidth={1.5} className="text-amber-600" />
              <h3 className="font-semibold text-slate-900">Okapi BM25</h3>
            </div>
            <div className="text-right">
              <div className="text-xs font-mono text-slate-400">Latency</div>
              <div className="text-sm font-bold text-slate-900">
                {bm25Latency?.toFixed(1)} ms
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
                <ResultCard key={item.id} item={item} onResultClick={onResultClick} />
              ))
            )}
          </div>
        </div>

        <div className="panel flex-1 p-4 sm:p-5">
          <div className="mb-4 flex flex-wrap items-center justify-between gap-2">
            <div className="flex items-center gap-2">
              <Sparkles size={18} strokeWidth={1.5} className="text-indigo-600" />
              <h3 className="font-semibold text-slate-900">Sentence-BERT</h3>
            </div>
            <div className="text-right">
              <div className="text-xs font-mono text-slate-400">Latency</div>
              <div className="text-sm font-bold text-slate-900">
                {sbertLatency?.toFixed(1)} ms
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
                <ResultCard key={item.id} item={item} onResultClick={onResultClick} />
              ))
            )}
          </div>
        </div>
      </div>

      <div className="mt-6 flex flex-col justify-end gap-2 sm:flex-row">
        <button className="btn-ghost text-sm">Atur bobot gabungan</button>
        <button className="btn-primary text-sm">Ekspor hasil</button>
      </div>
    </section>
  );
}
