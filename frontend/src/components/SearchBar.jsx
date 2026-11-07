import { useState } from "react";
import { Search, X, Plus } from "lucide-react";

const QUICK_SUGGESTIONS = [
  "HP Kamera Low-light",
  "Laptop Coding 10 Jutaan",
  "Fast Charging 120W",
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
    <div className="w-full max-w-3xl mx-auto">
      <form onSubmit={handleSubmit} className="relative group">
        <div className="flex items-center gap-2">
          <div className="relative flex-1">
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
                className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 transition-colors"
              >
                <X size={18} strokeWidth={2.25} />
              </button>
            )}
          </div>

          <button
            type="submit"
            disabled={loading || inputValue.trim().length === 0}
            className="btn-primary disabled:opacity-60 disabled:pointer-events-none"
          >
            {loading ? (
              <>
                <Plus size={16} strokeWidth={2} className="animate-spin" />
                <span className="ml-2 text-xs font-semibold">Memuat</span>
              </>
            ) : (
              "Cari"
            )}
          </button>
        </div>

        {!loading && inputValue.trim().length === 0 && (
          <div className="mt-4 px-1">
            <p className="text-xs font-medium text-slate-500 mb-2 ml-1">Cepat cari</p>
            <div className="flex flex-wrap gap-2">
              {QUICK_SUGGESTIONS.map((suggestion) => (
                <button
                  key={suggestion}
                  type="button"
                  onClick={() => handleSuggestion(suggestion)}
                  className="btn-ghost whitespace-nowrap"
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
