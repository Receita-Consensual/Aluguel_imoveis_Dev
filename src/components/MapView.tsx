import { useState, useCallback, useRef, useEffect } from 'react';
import {
  GoogleMap,
  Marker,
  Circle,
  InfoWindow,
} from '@react-google-maps/api';
import type { Imovel } from '../types/imovel';

const PORTUGAL_CENTER = { lat: 40.63, lng: -8.65 };

const MAP_STYLES: google.maps.MapTypeStyle[] = [
  { elementType: 'geometry', stylers: [{ color: '#f5f5f5' }] },
  { elementType: 'labels.icon', stylers: [{ visibility: 'off' }] },
  { elementType: 'labels.text.fill', stylers: [{ color: '#616161' }] },
  { elementType: 'labels.text.stroke', stylers: [{ color: '#f5f5f5' }] },
  { featureType: 'administrative.land_parcel', elementType: 'labels.text.fill', stylers: [{ color: '#bdbdbd' }] },
  { featureType: 'poi', elementType: 'geometry', stylers: [{ color: '#eeeeee' }] },
  { featureType: 'poi', elementType: 'labels.text.fill', stylers: [{ color: '#757575' }] },
  { featureType: 'poi.park', elementType: 'geometry', stylers: [{ color: '#e5e5e5' }] },
  { featureType: 'poi.park', elementType: 'labels.text.fill', stylers: [{ color: '#9e9e9e' }] },
  { featureType: 'road', elementType: 'geometry', stylers: [{ color: '#ffffff' }] },
  { featureType: 'road.arterial', elementType: 'labels.text.fill', stylers: [{ color: '#757575' }] },
  { featureType: 'road.highway', elementType: 'geometry', stylers: [{ color: '#dadada' }] },
  { featureType: 'road.highway', elementType: 'labels.text.fill', stylers: [{ color: '#616161' }] },
  { featureType: 'road.local', elementType: 'labels.text.fill', stylers: [{ color: '#9e9e9e' }] },
  { featureType: 'transit.line', elementType: 'geometry', stylers: [{ color: '#e5e5e5' }] },
  { featureType: 'transit.station', elementType: 'geometry', stylers: [{ color: '#eeeeee' }] },
  { featureType: 'water', elementType: 'geometry', stylers: [{ color: '#c9d6e5' }] },
  { featureType: 'water', elementType: 'labels.text.fill', stylers: [{ color: '#8ea8c4' }] },
];

const MAP_OPTIONS: google.maps.MapOptions = {
  styles: MAP_STYLES,
  disableDefaultUI: true,
  zoomControl: true,
  zoomControlOptions: { position: 6 },
  mapTypeControl: false,
  streetViewControl: false,
  fullscreenControl: false,
  gestureHandling: 'greedy',
  minZoom: 7,
  maxZoom: 19,
  clickableIcons: false,
};

function getMarkerColor(tipologia: string): string {
  const t = tipologia.toLowerCase();
  if (t.includes('moradia') || t.includes('casa')) return '#059669';
  if (t.includes('quarto')) return '#d97706';
  return '#0284c7';
}

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

function buildMarkerSvg(color: string, isHighlighted: boolean): string {
  const size = isHighlighted ? 18 : 12;
  const stroke = isHighlighted ? '#0369a1' : '#ffffff';
  const strokeWidth = isHighlighted ? 3 : 2;
  const full = size + strokeWidth * 2;
  return `data:image/svg+xml,${encodeURIComponent(
    `<svg xmlns="http://www.w3.org/2000/svg" width="${full}" height="${full}"><circle cx="${full/2}" cy="${full/2}" r="${size}" fill="${color}" stroke="${stroke}" stroke-width="${strokeWidth}"/></svg>`
  )}`;
}

const WORK_MARKER_SVG = `data:image/svg+xml,${encodeURIComponent(
  `<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40"><circle cx="20" cy="20" r="16" fill="#0369a1" stroke="#ffffff" stroke-width="3"/><rect x="13" y="16" width="14" height="10" rx="1.5" fill="none" stroke="#ffffff" stroke-width="1.5"/><path d="M17 16v-2a3 3 0 016 0v2" fill="none" stroke="#ffffff" stroke-width="1.5"/></svg>`
)}`;

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
  const mapRef = useRef<google.maps.Map | null>(null);
  const [selectedImovel, setSelectedImovel] = useState<Imovel | null>(null);

  const onLoad = useCallback((map: google.maps.Map) => {
    mapRef.current = map;
  }, []);

  useEffect(() => {
    if (mapRef.current && searchCenter) {
      mapRef.current.panTo(searchCenter);
      mapRef.current.setZoom(getZoomForRadius(raioMetros));
    }
  }, [searchCenter, raioMetros]);

  const handleMarkerClick = useCallback((imovel: Imovel) => {
    setSelectedImovel(imovel);
    onMarkerClick(imovel.id);
  }, [onMarkerClick]);

  return (
    <GoogleMap
      mapContainerStyle={{ width: '100%', height: '100%' }}
      center={searchCenter || PORTUGAL_CENTER}
      zoom={searchCenter ? getZoomForRadius(raioMetros) : 13}
      options={MAP_OPTIONS}
      onLoad={onLoad}
    >
      {searchCenter && (
        <>
          <Marker
            position={searchCenter}
            icon={{
              url: WORK_MARKER_SVG,
              scaledSize: new google.maps.Size(40, 40),
              anchor: new google.maps.Point(20, 20),
            }}
            zIndex={1000}
          />
          <Circle
            center={searchCenter}
            radius={raioMetros}
            options={{
              fillColor: '#0284c7',
              fillOpacity: 0.06,
              strokeColor: '#0284c7',
              strokeOpacity: 0.4,
              strokeWeight: 2,
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
            position={{ lat: imovel.lat, lng: imovel.lon }}
            icon={{
              url: buildMarkerSvg(color, isHl),
              scaledSize: new google.maps.Size(isHl ? 40 : 28, isHl ? 40 : 28),
              anchor: new google.maps.Point(isHl ? 20 : 14, isHl ? 20 : 14),
            }}
            zIndex={isHl ? 999 : 1}
            onMouseOver={() => onMarkerHover(imovel.id)}
            onMouseOut={() => onMarkerHover(null)}
            onClick={() => handleMarkerClick(imovel)}
          />
        );
      })}

      {selectedImovel && (
        <InfoWindow
          position={{ lat: selectedImovel.lat, lng: selectedImovel.lon }}
          onCloseClick={() => setSelectedImovel(null)}
          options={{ pixelOffset: new google.maps.Size(0, -14), maxWidth: 280 }}
        >
          <div style={{ fontFamily: 'Inter, system-ui, sans-serif', minWidth: 220 }}>
            {selectedImovel.imagem_url && (
              <img
                src={selectedImovel.imagem_url}
                alt={selectedImovel.titulo}
                style={{ width: '100%', height: 100, objectFit: 'cover', borderRadius: 8, marginBottom: 8 }}
              />
            )}
            <div style={{ fontSize: 14, fontWeight: 600, color: '#1e293b', lineHeight: 1.3 }}>
              {selectedImovel.titulo || 'Sem titulo'}
            </div>
            <div style={{ fontSize: 16, fontWeight: 700, color: '#0284c7', marginTop: 4 }}>
              {selectedImovel.preco > 0 ? `${selectedImovel.preco}\u20ac/mes` : 'Consultar'}
            </div>
            <div style={{ display: 'flex', gap: 12, marginTop: 6, fontSize: 12, color: '#64748b' }}>
              {selectedImovel.tipologia && (
                <span style={{ textTransform: 'uppercase', fontWeight: 600 }}>{selectedImovel.tipologia}</span>
              )}
              {selectedImovel.area_m2 > 0 && <span>{selectedImovel.area_m2}m2</span>}
              {selectedImovel.dist_metros != null && (
                <span style={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                  {formatDistance(selectedImovel.dist_metros)}
                </span>
              )}
            </div>
            <a
              href={selectedImovel.link}
              target="_blank"
              rel="noopener noreferrer"
              style={{
                display: 'inline-flex', alignItems: 'center', gap: 4,
                marginTop: 8, padding: '6px 14px',
                backgroundColor: '#0284c7', color: '#ffffff',
                borderRadius: 8, fontSize: 12, fontWeight: 600,
                textDecoration: 'none',
              }}
            >
              Ver Anuncio
            </a>
          </div>
        </InfoWindow>
      )}
    </GoogleMap>
  );
}
