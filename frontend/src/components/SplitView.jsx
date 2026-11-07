import { Cpu, Sparkles } from "lucide-react";

export default function SplitView({ bm25Results, sbertResults, bm25Latency, sbertLatency, onResultClick }) {
  return (
    <section className="w-full">
      <div className="flex flex-col lg:flex-row gap-4">
        <div className="flex-1 panel p-5">
          <div className="flex items-center justify-between mb-4">
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
          <div className="text-xs font-medium text-slate-500 mb-2 uppercase tracking-wider">
            {bm25Results.length} hasil
          </div>
          <div className="space-y-2">
            {bm25Results.length === 0 ? (
              <div className="text-center py-6 text-slate-500 text-sm">
                Tidak ada hasil untuk kata kunci ini.
              </div>
            ) : (
              bm25Results.map((item) => (
                <ResultCard key={item.id} item={item} source="bm25" onResultClick={onResultClick} />
              ))
            )}
          </div>
        </div>

        <div className="flex-1 panel p-5">
          <div className="flex items-center justify-between mb-4">
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
          <div className="text-xs font-medium text-slate-500 mb-2 uppercase tracking-wider">
            {sbertResults.length} hasil
          </div>
          <div className="space-y-2">
            {sbertResults.length === 0 ? (
              <div className="text-center py-6 text-slate-500 text-sm">
                Tidak ada hasil untuk kata kunci ini.
              </div>
            ) : (
              sbertResults.map((item) => (
                <ResultCard key={item.id} item={item} source="sbert" onResultClick={onResultClick} />
              ))
            )}
          </div>
        </div>
      </div>

      <div className="mt-6 flex justify-end gap-2">
        <button className="btn-ghost text-sm">Atur bobot gabungan</button>
        <button className="btn-primary text-sm">Ekspor hasil</button>
      </div>
    </section>
  );
}
