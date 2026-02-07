import { useState, useRef, useCallback } from 'react';
import { Autocomplete } from '@react-google-maps/api';
import { Search, Loader2, Navigation } from 'lucide-react';

const RADIUS_OPTIONS = [
  { label: '500m', value: 500 },
  { label: '1km', value: 1000 },
  { label: '2km', value: 2000 },
  { label: '3km', value: 3000 },
  { label: '5km', value: 5000 },
  { label: '10km', value: 10000 },
];

interface SearchBarProps {
  onSearch: (lat: number, lng: number, raioMetros: number, placeName: string) => void;
  onLocateMe: () => void;
  isSearching: boolean;
}

export default function SearchBar({ onSearch, onLocateMe, isSearching }: SearchBarProps) {
  const [raio, setRaio] = useState(2000);
  const [inputValue, setInputValue] = useState('');
  const autocompleteRef = useRef<google.maps.places.Autocomplete | null>(null);

  const onAutocompleteLoad = useCallback((autocomplete: google.maps.places.Autocomplete) => {
    autocompleteRef.current = autocomplete;
  }, []);

  const onPlaceChanged = useCallback(() => {
    const autocomplete = autocompleteRef.current;
    if (!autocomplete) return;

    const place = autocomplete.getPlace();
    if (!place.geometry?.location) return;

    const lat = place.geometry.location.lat();
    const lng = place.geometry.location.lng();
    const name = place.formatted_address || place.name || inputValue;
    setInputValue(name);
    onSearch(lat, lng, raio, name);
  }, [raio, inputValue, onSearch]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
  };

  return (
    <div className="bg-white rounded-2xl shadow-lg border border-slate-100 p-4">
      <form onSubmit={handleSubmit} className="space-y-3">
        <div className="relative">
          <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400 pointer-events-none z-10" />
          <Autocomplete
            onLoad={onAutocompleteLoad}
            onPlaceChanged={onPlaceChanged}
            options={{
              componentRestrictions: { country: 'pt' },
              types: ['geocode', 'establishment'],
            }}
          >
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              placeholder="Onde vais trabalhar? Ex: Universidade de Aveiro"
              className="w-full pl-10 pr-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-sm text-slate-900 placeholder:text-slate-400 focus:outline-none focus:ring-2 focus:ring-sky-500/40 focus:border-sky-300 transition-all"
            />
          </Autocomplete>
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
                    ? 'bg-sky-600 text-white shadow-sm shadow-sky-200'
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
            <span className="hidden sm:inline">Minha localiza\u00e7\u00e3o</span>
          </button>
          {isSearching && (
            <div className="flex items-center gap-2 px-4 py-2.5 text-sky-600 text-sm font-medium">
              <Loader2 className="w-4 h-4 animate-spin" />
              A procurar...
            </div>
          )}
        </div>
      </form>
    </div>
  );
}
