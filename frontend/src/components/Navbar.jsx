import { useState } from "react";
import { Search, Menu, X, LayoutDashboard, BarChart3 } from "lucide-react";

export default function Navbar({ view, onChangeView }) {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <nav className="sticky top-0 z-50 border-b border-slate-200 bg-white/80 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-xl bg-primary-600 flex items-center justify-center text-white font-bold text-xs shadow-sm shadow-primary-500/30">
              MG
            </div>
            <span className="font-bold text-xl tracking-tight text-slate-900">
              Mesin<span className="text-primary-600">Pencari</span> Gadget
            </span>
          </div>

          <div className="hidden md:flex items-center gap-2">
            <button
              onClick={() => onChangeView("pencarian")}
              className={`rounded-xl px-4 py-2 text-sm font-medium transition-colors ${
                view === "pencarian"
                  ? "bg-primary-600 text-white shadow-sm shadow-primary-500/30"
                  : "text-slate-600 hover:bg-slate-100"
              }`}
            >
              Pencarian
            </button>
            <button
              onClick={() => onChangeView("evaluasi")}
              className={`rounded-xl px-4 py-2 text-sm font-medium transition-colors ${
                view === "evaluasi"
                  ? "bg-primary-600 text-white shadow-sm shadow-primary-500/30"
                  : "text-slate-600 hover:bg-slate-100"
              }`}
            >
              Evaluasi
            </button>
          </div>

          <div className="flex items-center gap-2">
            <button
              className="btn-ghost hidden sm:flex items-center gap-2"
              title="Mode tampilan"
            >
              <BarChart3 size={16} strokeWidth={1.5} />
              <span className="text-xs font-medium text-slate-600">Split View</span>
            </button>
            <button
              className="btn-ghost md:hidden"
              onClick={() => setMobileOpen(!mobileOpen)}
              aria-label="Buka menu"
            >
              {mobileOpen ? <X size={20} strokeWidth={2} /> : <Menu size={20} strokeWidth={2} />}
            </button>
          </div>
        </div>

        {mobileOpen && (
          <div className="md:hidden border-t border-slate-200 bg-white py-4">
            <button
              onClick={() => {
                onChangeView("pencarian");
                setMobileOpen(false);
              }}
              className={`w-full text-left px-4 py-2.5 text-sm font-medium transition-colors ${
                view === "pencarian"
                  ? "bg-primary-50 text-primary-700"
                  : "text-slate-600 hover:bg-slate-50"
              }`}
            >
              Pencarian
            </button>
            <button
              onClick={() => {
                onChangeView("evaluasi");
                setMobileOpen(false);
              }}
              className={`w-full text-left px-4 py-2.5 text-sm font-medium transition-colors ${
                view === "evaluasi"
                  ? "bg-primary-50 text-primary-700"
                  : "text-slate-600 hover:bg-slate-50"
              }`}
            >
              Evaluasi
            </button>
          </div>
        )}
      </div>
    </nav>
  );
}
