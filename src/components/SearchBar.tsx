import { useState, FormEvent } from 'react';
import { Search, MapPin, Loader2 } from 'lucide-react';

const RADIUS_OPTIONS = [
  { label: '500m', value: 500 },
  { label: '1km', value: 1000 },
  { label: '2km', value: 2000 },
  { label: '3km', value: 3000 },
  { label: '5km', value: 5000 },
  { label: '10km', value: 10000 },
];

interface SearchBarProps {
  onSearch: (query: string, raioMetros: number) => void;
  onLocateMe: () => void;
  isSearching: boolean;
}

export default function SearchBar({ onSearch, onLocateMe, isSearching }: SearchBarProps) {
  const [query, setQuery] = useState('');
  const [raio, setRaio] = useState(2000);

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      onSearch(query.trim(), raio);
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-lg border border-slate-200 p-3 sm:p-4">
      <form onSubmit={handleSubmit} className="space-y-3">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Onde vais trabalhar? Ex: Altice Labs, Aveiro"
            className="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-lg text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-sky-500 focus:border-transparent transition"
          />
        </div>

        <div className="flex items-center gap-2 flex-wrap">
          <span className="text-xs text-slate-500 font-medium shrink-0">Raio:</span>
          <div className="flex gap-1 flex-wrap">
            {RADIUS_OPTIONS.map((opt) => (
              <button
                key={opt.value}
                type="button"
                onClick={() => setRaio(opt.value)}
                className={`px-2.5 py-1 rounded-full text-xs font-medium transition-colors ${
                  raio === opt.value
                    ? 'bg-sky-600 text-white'
                    : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                }`}
              >
                {opt.label}
              </button>
            ))}
          </div>
        </div>

        <div className="flex gap-2">
          <button
            type="submit"
            disabled={isSearching || !query.trim()}
            className="flex-1 flex items-center justify-center gap-2 px-4 py-2.5 bg-sky-600 hover:bg-sky-700 disabled:bg-slate-300 text-white rounded-lg text-sm font-semibold transition-colors"
          >
            {isSearching ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin" />
                A procurar...
              </>
            ) : (
              <>
                <Search className="w-4 h-4" />
                Procurar
              </>
            )}
          </button>
          <button
            type="button"
            onClick={onLocateMe}
            className="flex items-center gap-1.5 px-3 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg text-sm font-medium transition-colors"
            title="Usar minha localiza\u00e7\u00e3o"
          >
            <MapPin className="w-4 h-4" />
            <span className="hidden sm:inline">Minha localiza\u00e7\u00e3o</span>
          </button>
        </div>
      </form>
    </div>
  );
}
