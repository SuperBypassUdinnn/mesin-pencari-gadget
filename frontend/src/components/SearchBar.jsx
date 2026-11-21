import { useState } from "react";
import { Search, X, Loader2 } from "lucide-react";

const QUICK_SUGGESTIONS = [
  "ASUS Zenbook Intel OLED",
  "smartphone MediaTek Dimensity 5G",
  "HP baterai tahan lama seharian tanpa sering cas",
];

export default function SearchBar({ value, onChange, onSearch, loading }) {
  const [inputValue, setInputValue] = useState(value || "");

  const handleSubmit = (event) => {
    event.preventDefault();
    onSearch(inputValue.trim());
  };

  const handleClear = () => {
    setInputValue("");
    onChange("");
    onSearch("");
  };

  const handleSuggestion = (suggestion) => {
    setInputValue(suggestion);
    onChange(suggestion);
    onSearch(suggestion);
  };

  return (
    <div className="mx-auto w-full max-w-3xl">
      <form onSubmit={handleSubmit} className="group relative">
        <div className="flex items-center gap-2">
          <div className="relative min-w-0 flex-1">
            <div className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400">
              <Search size={18} strokeWidth={1.5} />
            </div>
            <input
              type="search"
              value={inputValue}
              onChange={(event) => {
                setInputValue(event.target.value);
                onChange(event.target.value);
              }}
              onBlur={(event) => setInputValue(event.target.value)}
              placeholder="Cari review gadget…"
              className="input-field pl-11"
              autoComplete="off"
              spellCheck={false}
            />
            {inputValue.length > 0 && !loading && (
              <button
                type="button"
                onClick={handleClear}
                aria-label="Hapus pencarian"
                className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 transition-colors hover:text-slate-600"
              >
                <X size={18} strokeWidth={2.25} />
              </button>
            )}
          </div>

          <button
            type="submit"
            disabled={loading || inputValue.trim().length === 0}
            className="btn-primary shrink-0 disabled:pointer-events-none disabled:opacity-60"
          >
            {loading ? (
              <>
                <Loader2 size={16} strokeWidth={2} className="animate-spin" />
                <span className="ml-2 hidden text-xs font-semibold sm:inline">
                  Memuat
                </span>
              </>
            ) : (
              "Cari"
            )}
          </button>
        </div>

        {!loading && inputValue.trim().length === 0 && (
          <div className="mt-4 px-1">
            <p className="mb-2 ml-1 text-xs font-medium text-slate-500">
              Cepat cari
            </p>
            <div className="flex flex-col gap-2 sm:flex-row sm:flex-wrap">
              {QUICK_SUGGESTIONS.map((suggestion) => (
                <button
                  key={suggestion}
                  type="button"
                  onClick={() => handleSuggestion(suggestion)}
                  className="inline-flex w-full items-center rounded-xl border border-slate-200 bg-white px-3 py-2 text-left text-xs font-medium leading-snug text-slate-700 shadow-sm transition-colors hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-slate-300 focus:ring-offset-1 active:scale-95 sm:w-auto sm:text-sm"
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        )}
      </form>
    </div>
  );
}
