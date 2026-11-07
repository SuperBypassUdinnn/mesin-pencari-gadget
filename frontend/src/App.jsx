import { useState } from "react";
import Navbar from "./components/Navbar.jsx";
import SearchPage from "./pages/SearchPage.jsx";

export default function App() {
  const [view, setView] = useState("pencarian");

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <Navbar view={view} onChangeView={setView} />
      <main className="max-w-7xl mx-auto px-4 py-6">
        {view === "evaluasi" ? (
          <section className="panel p-6">
            <h2 className="text-xl font-semibold text-slate-900 mb-4">Evaluasi</h2>
            <p className="text-slate-600">
              Halaman evaluasi perbandingan metrik Okapi BM25 dan Sentence-BERT.
            </p>
          </section>
        ) : (
          <SearchPage />
        )}
      </main>
    </div>
  );
}
