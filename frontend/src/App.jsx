import { useState } from "react";
import Navbar from "./components/Navbar.jsx";
import SearchPage from "./pages/SearchPage.jsx";
import EvaluationDashboard from "./pages/EvaluationDashboard.jsx";

export default function App() {
  const [view, setView] = useState("pencarian");

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <Navbar view={view} onChangeView={setView} />
      <main className="max-w-7xl mx-auto px-4 py-6">
        {view === "evaluasi" ? (
          <EvaluationDashboard />
        ) : (
          <SearchPage />
        )}
      </main>
    </div>
  );
}
