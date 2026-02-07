import { useState, useCallback, useMemo } from 'react';
import Header from './components/Header';
import SearchBar from './components/SearchBar';
import Filters from './components/Filters';
import MapView from './components/MapView';
import PropertyList from './components/PropertyList';
import FounderSection from './components/FounderSection';
import MobileDrawer from './components/MobileDrawer';
import { useImoveis } from './hooks/useImoveis';
import { useGeocode } from './hooks/useGeocode';
import type { SearchFilters } from './types/imovel';

const DEFAULT_FILTERS: SearchFilters = {
  tipologias: [],
  precoMin: 0,
  precoMax: 3000,
  areaMin: 0,
  areaMax: 500,
  mobiliado: 'todos',
};

const RADIUS_LABELS: Record<number, string> = {
  500: '500m',
  1000: '1km',
  2000: '2km',
  3000: '3km',
  5000: '5km',
  10000: '10km',
};

function App() {
  const [searchCenter, setSearchCenter] = useState<[number, number] | null>(null);
  const [raioMetros, setRaioMetros] = useState(2000);
  const [filters, setFilters] = useState<SearchFilters>(DEFAULT_FILTERS);
  const [highlightedId, setHighlightedId] = useState<string | null>(null);
  const [scrollToId, setScrollToId] = useState<string | null>(null);
  const [hasSearched, setHasSearched] = useState(false);
  const [showFounder, setShowFounder] = useState(false);
  const [isSearching, setIsSearching] = useState(false);

  const { imoveis, loading, polling, searchByRadius, pollForResults, filterImoveis } = useImoveis();
  const { geocode, geocoding } = useGeocode();

  const filteredImoveis = useMemo(
    () => filterImoveis(imoveis, filters),
    [imoveis, filters, filterImoveis]
  );

  const handleSearch = useCallback(async (query: string, raio: number) => {
    setIsSearching(true);
    setRaioMetros(raio);
    setHasSearched(true);

    const result = await geocode(query);
    if (!result) {
      setIsSearching(false);
      return;
    }

    setSearchCenter([result.lat, result.lon]);
    const results = await searchByRadius(result.lat, result.lon, raio);
    setIsSearching(false);

    if (results.length < 3) {
      pollForResults(result.lat, result.lon, raio, query);
    }
  }, [geocode, searchByRadius, pollForResults]);

  const handleLocateMe = useCallback(() => {
    if (!navigator.geolocation) return;

    navigator.geolocation.getCurrentPosition(
      async (pos) => {
        const { latitude, longitude } = pos.coords;
        setSearchCenter([latitude, longitude]);
        setRaioMetros(2000);
        setHasSearched(true);
        setIsSearching(true);

        const results = await searchByRadius(latitude, longitude, 2000);
        setIsSearching(false);

        if (results.length < 3) {
          pollForResults(latitude, longitude, 2000, 'Minha localiza\u00e7\u00e3o');
        }
      },
      () => {},
      { enableHighAccuracy: true }
    );
  }, [searchByRadius, pollForResults]);

  const handleMarkerClick = useCallback((id: string) => {
    setHighlightedId(id);
    setScrollToId(id);
    setTimeout(() => setScrollToId(null), 100);
  }, []);

  return (
    <div className="h-screen flex flex-col bg-slate-50">
      <Header onFounderClick={() => setShowFounder(true)} />

      <div className="flex-1 pt-14 flex flex-col lg:flex-row overflow-hidden">
        <aside className="hidden lg:flex lg:w-[420px] xl:w-[460px] flex-col border-r border-slate-200 bg-white overflow-hidden">
          <div className="p-3 space-y-3 overflow-y-auto flex-1">
            <SearchBar
              onSearch={handleSearch}
              onLocateMe={handleLocateMe}
              isSearching={isSearching || geocoding}
            />
            {hasSearched && (
              <Filters
                filters={filters}
                onChange={setFilters}
                resultCount={filteredImoveis.length}
                raioLabel={RADIUS_LABELS[raioMetros] || `${raioMetros}m`}
              />
            )}
            <PropertyList
              imoveis={filteredImoveis}
              loading={loading}
              polling={polling}
              hasSearched={hasSearched}
              highlightedId={highlightedId}
              onHover={setHighlightedId}
              scrollToId={scrollToId}
            />
          </div>
        </aside>

        <main className="flex-1 relative">
          <div className="lg:hidden absolute top-3 left-3 right-3 z-[999]">
            <SearchBar
              onSearch={handleSearch}
              onLocateMe={handleLocateMe}
              isSearching={isSearching || geocoding}
            />
          </div>

          <MapView
            imoveis={filteredImoveis}
            searchCenter={searchCenter}
            raioMetros={raioMetros}
            highlightedId={highlightedId}
            onMarkerHover={setHighlightedId}
            onMarkerClick={handleMarkerClick}
          />

          <MobileDrawer resultCount={filteredImoveis.length}>
            {hasSearched && (
              <Filters
                filters={filters}
                onChange={setFilters}
                resultCount={filteredImoveis.length}
                raioLabel={RADIUS_LABELS[raioMetros] || `${raioMetros}m`}
              />
            )}
            <div className="mt-3">
              <PropertyList
                imoveis={filteredImoveis}
                loading={loading}
                polling={polling}
                hasSearched={hasSearched}
                highlightedId={highlightedId}
                onHover={setHighlightedId}
                scrollToId={scrollToId}
              />
            </div>
          </MobileDrawer>
        </main>
      </div>

      <FounderSection visible={showFounder} onClose={() => setShowFounder(false)} />
    </div>
  );
}

export default App;
