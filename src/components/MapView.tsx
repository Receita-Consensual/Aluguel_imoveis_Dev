import { useState, useCallback, useRef, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Circle, useMap } from 'react-leaflet';
import L from 'leaflet';
import { ExternalLink } from 'lucide-react';
import type { Imovel } from '../types/imovel';
import 'leaflet/dist/leaflet.css';

const PORTUGAL_CENTER: [number, number] = [39.5, -8.0];

function getMarkerColor(tipologia: string): string {
  const t = tipologia.toLowerCase();
  if (t.includes('moradia') || t.includes('casa')) return '#059669';
  if (t.includes('quarto')) return '#d97706';
  return '#0d9488';
}

function createPropertyIcon(color: string, isHighlighted: boolean): L.DivIcon {
  const size = isHighlighted ? 20 : 12;
  const border = isHighlighted ? '3px solid #0f766e' : '2px solid #ffffff';
  const shadow = isHighlighted
    ? '0 0 0 4px rgba(13,148,136,0.2), 0 2px 8px rgba(0,0,0,0.3)'
    : '0 1px 4px rgba(0,0,0,0.3)';
  return L.divIcon({
    className: '',
    iconSize: [size, size],
    iconAnchor: [size / 2, size / 2],
    html: `<div style="width:${size}px;height:${size}px;border-radius:50%;background:${color};border:${border};box-shadow:${shadow};transition:all 0.15s ease;"></div>`,
  });
}

const WORK_ICON = L.divIcon({
  className: '',
  iconSize: [44, 44],
  iconAnchor: [22, 22],
  html: `<div style="width:44px;height:44px;border-radius:50%;background:#0f766e;border:3px solid #fff;box-shadow:0 0 0 4px rgba(15,118,110,0.25),0 4px 12px rgba(0,0,0,0.25);display:flex;align-items:center;justify-content:center;">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 7V5a4 4 0 0 0-8 0v2"/></svg>
  </div>`,
});

function formatDistance(meters?: number): string {
  if (!meters) return '';
  if (meters < 1000) return `${Math.round(meters)}m`;
  return `${(meters / 1000).toFixed(1)}km`;
}

function getZoomForRadius(radius: number): number {
  if (radius <= 500) return 16;
  if (radius <= 1000) return 15;
  if (radius <= 2000) return 14;
  if (radius <= 3000) return 13;
  if (radius <= 5000) return 12;
  return 11;
}

function MapUpdater({ center, zoom }: { center: [number, number] | null; zoom: number }) {
  const map = useMap();
  useEffect(() => {
    if (center) {
      map.flyTo(center, zoom, { duration: 1.2 });
    }
  }, [center, zoom, map]);
  return null;
}

interface MapViewProps {
  imoveis: Imovel[];
  searchCenter: { lat: number; lng: number } | null;
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
  const [, setSelectedImovel] = useState<Imovel | null>(null);
  const markersRef = useRef<Record<string, L.Marker>>({});

  const handleMarkerClick = useCallback(
    (imovel: Imovel) => {
      setSelectedImovel(imovel);
      onMarkerClick(imovel.id);
    },
    [onMarkerClick]
  );

  const center: [number, number] | null = searchCenter
    ? [searchCenter.lat, searchCenter.lng]
    : null;

  return (
    <MapContainer
      center={PORTUGAL_CENTER}
      zoom={7}
      className="w-full h-full"
      zoomControl={false}
      attributionControl={false}
    >
      <TileLayer url="https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png" />
      <MapUpdater center={center} zoom={searchCenter ? getZoomForRadius(raioMetros) : 7} />

      {searchCenter && (
        <>
          <Marker position={[searchCenter.lat, searchCenter.lng]} icon={WORK_ICON} zIndexOffset={1000}>
            <Popup>
              <span className="text-sm font-semibold text-teal-800">Local de trabalho</span>
            </Popup>
          </Marker>
          <Circle
            center={[searchCenter.lat, searchCenter.lng]}
            radius={raioMetros}
            pathOptions={{
              fillColor: '#0d9488',
              fillOpacity: 0.06,
              color: '#0d9488',
              opacity: 0.35,
              weight: 2,
            }}
          />
        </>
      )}

      {imoveis.map((imovel) => {
        const isHl = highlightedId === imovel.id;
        const color = getMarkerColor(imovel.tipologia);
        return (
          <Marker
            key={imovel.id}
            position={[imovel.lat, imovel.lon]}
            icon={createPropertyIcon(color, isHl)}
            zIndexOffset={isHl ? 999 : 1}
            ref={(ref) => {
              if (ref) markersRef.current[imovel.id] = ref;
            }}
            eventHandlers={{
              mouseover: () => onMarkerHover(imovel.id),
              mouseout: () => onMarkerHover(null),
              click: () => handleMarkerClick(imovel),
            }}
          >
            <Popup maxWidth={280} minWidth={220}>
              <div className="font-sans">
                {imovel.imagem_url && (
                  <img
                    src={imovel.imagem_url}
                    alt={imovel.titulo}
                    className="w-full h-24 object-cover rounded-lg mb-2"
                  />
                )}
                <div className="text-sm font-semibold text-slate-900 leading-tight">
                  {imovel.titulo || 'Sem titulo'}
                </div>
                <div className="text-base font-bold text-teal-700 mt-1">
                  {imovel.preco > 0 ? `${imovel.preco}\u20AC/m\u00EAs` : 'Consultar'}
                </div>
                <div className="flex gap-3 mt-1.5 text-xs text-slate-500">
                  {imovel.tipologia && <span className="uppercase font-semibold">{imovel.tipologia}</span>}
                  {imovel.area_m2 > 0 && <span>{imovel.area_m2}m\u00B2</span>}
                  {imovel.dist_metros != null && <span>{formatDistance(imovel.dist_metros)}</span>}
                </div>
                <a
                  href={imovel.link}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-flex items-center gap-1 mt-2 px-3 py-1.5 bg-teal-600 text-white rounded-lg text-xs font-semibold no-underline"
                >
                  Ver An\u00FAncio
                  <ExternalLink className="w-3 h-3" />
                </a>
              </div>
            </Popup>
          </Marker>
        );
      })}
    </MapContainer>
  );
}
