import { useState, useCallback } from "react";
import { api } from "../services/api.js";
import SearchBar from "../components/SearchBar.jsx";
import SplitView from "../components/SplitView.jsx";
import SpecsModal from "../components/SpecsModal.jsx";
import { Search } from "lucide-react";

export default function SearchPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState({ bm25: [], sbert: [] });
  const [latency, setLatency] = useState({ bm25: 0, sbert: 0 });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [selectedDoc, setSelectedDoc] = useState(null);

  const handleSearch = useCallback(async (q) => {
    if (!q) {
      setResults({ bm25: [], sbert: [] });
      setLatency({ bm25: 0, sbert: 0 });
      setError(null);
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const data = await api.searchGadgets({ q, algo: "both", top_k: 10 });
      setResults({
        bm25: data.bm25?.results || [],
        sbert: data.sbert?.results || [],
      });
      setLatency({
        bm25: data.bm25?.latency_ms || 0,
        sbert: data.sbert?.latency_ms || 0,
      });
    } catch (err) {
      setError("Gagal memuat hasil pencarian. Pastikan backend berjalan di http://localhost:8000");
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, []);

  const handleResultClick = (docId) => {
    api.getDocument(docId).then(setSelectedDoc).catch(() => {
      setError("Gagal memuat detail dokumen.");
    });
  };

  return (
    <div className="space-y-6">
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-1">
            <Search size={20} strokeWidth={1.75} className="text-primary-600" />
            <h1 className="text-2xl font-bold text-slate-900 tracking-tight">
              Pencarian Gadget
            </h1>
          </div>
          <p className="text-slate-600">
            Bandingkan hasil Okapi BM25 dan Sentence-BERT secara sampingan untuk
            review gadget Indonesia.
          </p>
        </div>
      </div>

      <SearchBar
        value={query}
        onChange={setQuery}
        onSearch={handleSearch}
        loading={loading}
      />

      {error && (
        <div className="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-800">
          {error}
        </div>
      )}

      <SplitView
        bm25Results={results.bm25}
        sbertResults={results.sbert}
        bm25Latency={latency.bm25}
        sbertLatency={latency.sbert}
        onResultClick={handleResultClick}
      />

      <SpecsModal document={selectedDoc} onClose={() => setSelectedDoc(null)} />
    </div>
  );
}
