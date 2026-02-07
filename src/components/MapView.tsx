import { useEffect, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle, useMap } from 'react-leaflet';
import L from 'leaflet';
import type { Imovel } from '../types/imovel';

const APARTMENT_ICON = new L.Icon({
  iconUrl: 'https://cdn.jsdelivr.net/npm/@mdi/svg@7.4.47/svg/map-marker.svg',
  iconSize: [28, 28],
  iconAnchor: [14, 28],
  popupAnchor: [0, -28],
  className: 'map-marker-apartment',
});

const WORK_ICON = new L.DivIcon({
  html: `<div style="width:36px;height:36px;background:#0369a1;border:3px solid white;border-radius:50%;display:flex;align-items:center;justify-content:center;box-shadow:0 2px 8px rgba(0,0,0,0.3)">
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>
  </div>`,
  iconSize: [36, 36],
  iconAnchor: [18, 18],
  className: '',
});

function createPropertyIcon(tipologia: string, isHighlighted: boolean): L.DivIcon {
  const t = tipologia.toLowerCase();
  let color = '#0284c7';
  if (t.includes('moradia') || t.includes('casa')) color = '#059669';
  if (t.includes('quarto')) color = '#d97706';

  const size = isHighlighted ? 32 : 24;
  const border = isHighlighted ? '3px solid #0284c7' : '2px solid white';

  return new L.DivIcon({
    html: `<div style="width:${size}px;height:${size}px;background:${color};border:${border};border-radius:50%;box-shadow:0 2px 6px rgba(0,0,0,0.3);transition:all 0.2s"></div>`,
    iconSize: [size, size],
    iconAnchor: [size / 2, size / 2],
    className: '',
  });
}

function formatDistance(meters?: number): string {
  if (!meters) return '';
  if (meters < 1000) return `${Math.round(meters)}m`;
  return `${(meters / 1000).toFixed(1)}km`;
}

function MapUpdater({ center, zoom }: { center: [number, number] | null; zoom: number }) {
  const map = useMap();
  const hasFlown = useRef(false);

  useEffect(() => {
    if (center && !hasFlown.current) {
      map.flyTo(center, zoom, { duration: 1.5 });
      hasFlown.current = true;
    } else if (center) {
      map.flyTo(center, zoom, { duration: 1 });
    }
  }, [center, zoom, map]);

  return null;
}

interface MapViewProps {
  imoveis: Imovel[];
  searchCenter: [number, number] | null;
  raioMetros: number;
  highlightedId: string | null;
  onMarkerHover: (id: string | null) => void;
  onMarkerClick: (id: string) => void;
}

export default function MapView({
  imoveis,
  searchCenter,
  raioMetros,
  highlightedId,
  onMarkerHover,
  onMarkerClick,
}: MapViewProps) {
  const defaultCenter: [number, number] = [40.63, -8.65];
  const defaultZoom = 13;

  const getZoomForRadius = (radius: number): number => {
    if (radius <= 500) return 16;
    if (radius <= 1000) return 15;
    if (radius <= 2000) return 14;
    if (radius <= 3000) return 13;
    if (radius <= 5000) return 12;
    return 11;
  };

  return (
    <MapContainer
      center={searchCenter || defaultCenter}
      zoom={defaultZoom}
      className="w-full h-full"
      zoomControl={false}
    >
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      <MapUpdater
        center={searchCenter}
        zoom={getZoomForRadius(raioMetros)}
      />

      {searchCenter && (
        <>
          <Marker position={searchCenter} icon={WORK_ICON}>
            <Popup>
              <span className="text-sm font-semibold">Ponto de refer\u00eancia</span>
            </Popup>
          </Marker>
          <Circle
            center={searchCenter}
            radius={raioMetros}
            pathOptions={{
              color: '#0284c7',
              fillColor: '#0284c7',
              fillOpacity: 0.08,
              weight: 2,
              dashArray: '6 4',
            }}
          />
        </>
      )}

      {imoveis.map((imovel) => (
        <Marker
          key={imovel.id}
          position={[imovel.lat, imovel.lon]}
          icon={createPropertyIcon(imovel.tipologia, highlightedId === imovel.id)}
          eventHandlers={{
            mouseover: () => onMarkerHover(imovel.id),
            mouseout: () => onMarkerHover(null),
            click: () => onMarkerClick(imovel.id),
          }}
        >
          <Popup>
            <div className="min-w-[200px]">
              {imovel.imagem_url && (
                <img
                  src={imovel.imagem_url}
                  alt={imovel.titulo}
                  className="w-full h-24 object-cover rounded mb-2"
                />
              )}
              <p className="font-semibold text-sm">{imovel.titulo || 'Sem t\u00edtulo'}</p>
              <p className="text-sky-700 font-bold text-sm mt-1">
                {imovel.preco > 0 ? `${imovel.preco}\u20ac/m\u00eas` : 'Consultar'}
              </p>
              {imovel.tipologia && <p className="text-xs text-slate-500 mt-0.5">{imovel.tipologia.toUpperCase()}</p>}
              {imovel.dist_metros != null && (
                <p className="text-xs text-slate-500">{formatDistance(imovel.dist_metros)} de dist\u00e2ncia</p>
              )}
              <a
                href={imovel.link}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-block mt-2 px-3 py-1 bg-sky-600 text-white text-xs font-semibold rounded hover:bg-sky-700 transition-colors"
              >
                Ver An\u00fancio
              </a>
            </div>
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}

export { APARTMENT_ICON };
