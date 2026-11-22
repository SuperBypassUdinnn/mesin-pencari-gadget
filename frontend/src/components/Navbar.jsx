import { useState } from "react";
import { Menu, X, BarChart3 } from "lucide-react";

export default function Navbar({ view, onChangeView }) {
  const [mobileOpen, setMobileOpen] = useState(false);

  return (
    <nav className="sticky top-0 z-50 border-b border-slate-200 bg-white/80 backdrop-blur-md">
      <div className="mx-auto max-w-7xl px-3 sm:px-4">
        <div className="flex h-16 items-center justify-between gap-2">
          <div className="flex min-w-0 items-center gap-3">
            <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-xl bg-primary-600 text-xs font-bold text-white shadow-sm shadow-primary-500/30">
              MG
            </div>
            <span className="truncate text-base font-bold tracking-tight text-slate-900 sm:text-xl">
              Mesin<span className="text-primary-600">Pencari</span> Gadget
            </span>
          </div>

          <div className="hidden items-center gap-2 md:flex">
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

          <div className="flex shrink-0 items-center gap-2">
            <button
              type="button"
              onClick={() => onChangeView("pencarian")}
              className={`btn-ghost hidden items-center gap-2 sm:flex ${
                view === "pencarian" ? "text-primary-700" : ""
              }`}
              title="Buka tampilan komparasi Split View"
              aria-label="Buka tampilan Split View"
              aria-pressed={view === "pencarian"}
            >
              <BarChart3 size={16} strokeWidth={1.5} />
              <span className="text-xs font-medium">Split View</span>
            </button>
            <button
              className="btn-ghost md:hidden"
              onClick={() => setMobileOpen(!mobileOpen)}
              aria-label="Buka menu"
              aria-expanded={mobileOpen}
            >
              {mobileOpen ? <X size={20} strokeWidth={2} /> : <Menu size={20} strokeWidth={2} />}
            </button>
          </div>
        </div>

        {mobileOpen && (
          <div className="border-t border-slate-200 bg-white py-4 md:hidden">
            <button
              onClick={() => {
                onChangeView("pencarian");
                setMobileOpen(false);
              }}
              className={`w-full px-4 py-2.5 text-left text-sm font-medium transition-colors ${
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
              className={`w-full px-4 py-2.5 text-left text-sm font-medium transition-colors ${
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
