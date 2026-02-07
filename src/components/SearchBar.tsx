import { useState, useRef, useEffect, useCallback } from 'react';
import { Search, Loader2, Navigation, MapPin, X } from 'lucide-react';

const RADIUS_OPTIONS = [
  { label: '500m', value: 500 },
  { label: '1km', value: 1000 },
  { label: '2km', value: 2000 },
  { label: '3km', value: 3000 },
  { label: '5km', value: 5000 },
  { label: '10km', value: 10000 },
];

interface NominatimResult {
  display_name: string;
  lat: string;
  lon: string;
}

interface SearchBarProps {
  onSearch: (lat: number, lng: number, raioMetros: number, placeName: string) => void;
  onLocateMe: () => void;
  isSearching: boolean;
}

export default function SearchBar({ onSearch, onLocateMe, isSearching }: SearchBarProps) {
  const [raio, setRaio] = useState(2000);
  const [inputValue, setInputValue] = useState('');
  const [suggestions, setSuggestions] = useState<NominatimResult[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const debounceRef = useRef<ReturnType<typeof setTimeout>>();
  const wrapperRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (wrapperRef.current && !wrapperRef.current.contains(e.target as Node)) {
        setShowSuggestions(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  const searchPlaces = useCallback(async (query: string) => {
    if (query.length < 3) {
      setSuggestions([]);
      return;
    }
    setIsLoading(true);
    try {
      const params = new URLSearchParams({
        q: `${query}, Portugal`,
        format: 'json',
        limit: '5',
        countrycodes: 'pt',
        'accept-language': 'pt',
        addressdetails: '1',
      });
      const resp = await fetch(`https://nominatim.openstreetmap.org/search?${params}`, {
        headers: { 'User-Agent': 'LugarPortugal/1.0' },
      });
      const data: NominatimResult[] = await resp.json();
      setSuggestions(data);
      setShowSuggestions(data.length > 0);
    } catch {
      setSuggestions([]);
    }
    setIsLoading(false);
  }, []);

  const handleInputChange = (value: string) => {
    setInputValue(value);
    if (debounceRef.current) clearTimeout(debounceRef.current);
    debounceRef.current = setTimeout(() => searchPlaces(value), 350);
  };

  const handleSelect = (result: NominatimResult) => {
    const lat = parseFloat(result.lat);
    const lon = parseFloat(result.lon);
    const name = result.display_name.split(',').slice(0, 3).join(',');
    setInputValue(name);
    setSuggestions([]);
    setShowSuggestions(false);
    onSearch(lat, lon, raio, name);
  };

  const handleClear = () => {
    setInputValue('');
    setSuggestions([]);
    setShowSuggestions(false);
  };

  return (
    <div className="bg-white rounded-2xl shadow-lg shadow-slate-200/60 border border-slate-100 p-4">
      <div className="space-y-3">
        <div ref={wrapperRef} className="relative">
          <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400 pointer-events-none z-10" />
          <input
            type="text"
            value={inputValue}
            onChange={(e) => handleInputChange(e.target.value)}
            onFocus={() => suggestions.length > 0 && setShowSuggestions(true)}
            placeholder="Onde vais trabalhar? Ex: Universidade de Aveiro"
            className="w-full pl-10 pr-10 py-3 bg-slate-50 border border-slate-200 rounded-xl text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-400/30 focus:border-blue-300 transition-all"
          />
          {inputValue && (
            <button
              onClick={handleClear}
              className="absolute right-3 top-1/2 -translate-y-1/2 w-5 h-5 flex items-center justify-center text-slate-400 hover:text-slate-600 transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          )}

          {showSuggestions && (
            <div className="absolute top-full left-0 right-0 mt-1.5 bg-white border border-slate-200 rounded-xl shadow-xl shadow-slate-200/50 z-50 overflow-hidden">
              {suggestions.map((s, i) => (
                <button
                  key={i}
                  onClick={() => handleSelect(s)}
                  className="w-full flex items-start gap-2.5 px-3.5 py-2.5 hover:bg-blue-50 text-left transition-colors border-b border-slate-100 last:border-0"
                >
                  <MapPin className="w-4 h-4 text-blue-500 mt-0.5 shrink-0" />
                  <span className="text-sm text-slate-700 leading-snug line-clamp-2">
                    {s.display_name}
                  </span>
                </button>
              ))}
            </div>
          )}
        </div>

        <div className="flex items-center gap-2 flex-wrap">
          <span className="text-xs text-slate-500 font-medium shrink-0">Raio:</span>
          <div className="flex gap-1.5 flex-wrap">
            {RADIUS_OPTIONS.map((opt) => (
              <button
                key={opt.value}
                type="button"
                onClick={() => setRaio(opt.value)}
                className={`px-3 py-1.5 rounded-full text-xs font-semibold transition-all ${
                  raio === opt.value
                    ? 'bg-blue-500 text-white shadow-sm shadow-blue-200'
                    : 'bg-slate-100 text-slate-500 hover:bg-slate-200 hover:text-slate-700'
                }`}
              >
                {opt.label}
              </button>
            ))}
          </div>
        </div>

        <div className="flex gap-2">
          <button
            type="button"
            onClick={onLocateMe}
            disabled={isSearching}
            className="flex items-center gap-1.5 px-4 py-2.5 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-xl text-sm font-medium transition-all"
          >
            <Navigation className="w-4 h-4" />
            <span className="hidden sm:inline">Minha localiza\u00E7\u00E3o</span>
          </button>
          {(isSearching || isLoading) && (
            <div className="flex items-center gap-2 px-4 py-2.5 text-blue-600 text-sm font-medium">
              <Loader2 className="w-4 h-4 animate-spin" />
              A procurar...
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
