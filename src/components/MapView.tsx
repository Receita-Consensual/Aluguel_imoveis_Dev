import { useState, useCallback, useEffect, useMemo } from 'react';
import { GoogleMap, useJsApiLoader, Marker, Circle, InfoWindow } from '@react-google-maps/api';
import { ExternalLink, Briefcase } from 'lucide-react';
import type { Imovel } from '../types/imovel';

const PORTUGAL_CENTER = { lat: 39.5, lng: -8.0 };
const GOOGLE_MAPS_API_KEY = import.meta.env.VITE_GOOGLE_MAPS_API_KEY || '';

function getMarkerColor(tipologia: string): string {
  const t = tipologia.toLowerCase();
  if (t.includes('moradia') || t.includes('casa')) return '#10b981';
  if (t.includes('quarto')) return '#f59e0b';
  return '#06b6d4';
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

const silverMapStyle = [
  {
    elementType: 'geometry',
    stylers: [{ color: '#f5f5f5' }],
  },
  {
    elementType: 'labels.icon',
    stylers: [{ visibility: 'off' }],
  },
  {
    elementType: 'labels.text.fill',
    stylers: [{ color: '#616161' }],
  },
  {
    elementType: 'labels.text.stroke',
    stylers: [{ color: '#f5f5f5' }],
  },
  {
    featureType: 'administrative.land_parcel',
    elementType: 'labels.text.fill',
    stylers: [{ color: '#bdbdbd' }],
  },
  {
    featureType: 'poi',
    elementType: 'geometry',
    stylers: [{ color: '#eeeeee' }],
  },
  {
    featureType: 'poi',
    elementType: 'labels.text.fill',
    stylers: [{ color: '#757575' }],
  },
  {
    featureType: 'poi.park',
    elementType: 'geometry',
    stylers: [{ color: '#e5e5e5' }],
  },
  {
    featureType: 'poi.park',
    elementType: 'labels.text.fill',
    stylers: [{ color: '#9e9e9e' }],
  },
  {
    featureType: 'road',
    elementType: 'geometry',
    stylers: [{ color: '#ffffff' }],
  },
  {
    featureType: 'road.arterial',
    elementType: 'labels.text.fill',
    stylers: [{ color: '#757575' }],
  },
  {
    featureType: 'road.highway',
    elementType: 'geometry',
    stylers: [{ color: '#dadada' }],
  },
  {
    featureType: 'road.highway',
    elementType: 'labels.text.fill',
    stylers: [{ color: '#616161' }],
  },
  {
    featureType: 'road.local',
    elementType: 'labels.text.fill',
    stylers: [{ color: '#9e9e9e' }],
  },
  {
    featureType: 'transit.line',
    elementType: 'geometry',
    stylers: [{ color: '#e5e5e5' }],
  },
  {
    featureType: 'transit.station',
    elementType: 'geometry',
    stylers: [{ color: '#eeeeee' }],
  },
  {
    featureType: 'water',
    elementType: 'geometry',
    stylers: [{ color: '#c9c9c9' }],
  },
  {
    featureType: 'water',
    elementType: 'labels.text.fill',
    stylers: [{ color: '#9e9e9e' }],
  },
];

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
  const [selectedImovel, setSelectedImovel] = useState<Imovel | null>(null);
  const [map, setMap] = useState<google.maps.Map | null>(null);

  const { isLoaded } = useJsApiLoader({
    id: 'google-map-script',
    googleMapsApiKey: GOOGLE_MAPS_API_KEY,
  });

  const center = searchCenter || PORTUGAL_CENTER;
  const zoom = searchCenter ? getZoomForRadius(raioMetros) : 7;

  const mapOptions = useMemo(
    () => ({
      styles: silverMapStyle,
      disableDefaultUI: true,
      zoomControl: true,
      mapTypeControl: false,
      streetViewControl: false,
      fullscreenControl: false,
    }),
    []
  );

  useEffect(() => {
    if (map && searchCenter) {
      map.panTo(searchCenter);
      map.setZoom(getZoomForRadius(raioMetros));
    }
  }, [map, searchCenter, raioMetros]);

  const handleMarkerClick = useCallback(
    (imovel: Imovel) => {
      setSelectedImovel(imovel);
      onMarkerClick(imovel.id);
    },
    [onMarkerClick]
  );

  const workLocationIcon = useMemo(() => {
    if (typeof window === 'undefined') return undefined;
    const svg = `
      <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 48 48">
        <circle cx="24" cy="24" r="22" fill="#0d9488" stroke="white" stroke-width="3"/>
        <circle cx="24" cy="24" r="18" fill="#0d9488" fill-opacity="0.3"/>
        <path d="M18 19h12v2H18zm0 4h12v2H18zm0 4h8v2h-8z" fill="white" stroke="white" stroke-width="1"/>
        <rect x="16" y="17" width="16" height="16" rx="1" fill="none" stroke="white" stroke-width="2"/>
      </svg>
    `;
    return {
      url: 'data:image/svg+xml;charset=UTF-8,' + encodeURIComponent(svg),
      scaledSize: new google.maps.Size(48, 48),
      anchor: new google.maps.Point(24, 24),
    };
  }, []);

  const createPropertyIcon = useCallback(
    (color: string, isHighlighted: boolean) => {
      if (typeof window === 'undefined') return undefined;
      const size = isHighlighted ? 24 : 16;
      const svg = `
        <svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="0 0 ${size} ${size}">
          <circle cx="${size / 2}" cy="${size / 2}" r="${size / 2 - 1}" fill="${color}" stroke="white" stroke-width="2"/>
          ${
            isHighlighted
              ? `<circle cx="${size / 2}" cy="${size / 2}" r="${size / 2 + 2}" fill="none" stroke="${color}" stroke-width="2" opacity="0.4"/>`
              : ''
          }
        </svg>
      `;
      return {
        url: 'data:image/svg+xml;charset=UTF-8,' + encodeURIComponent(svg),
        scaledSize: new google.maps.Size(size, size),
        anchor: new google.maps.Point(size / 2, size / 2),
      };
    },
    []
  );

  if (!isLoaded) {
    return (
      <div className="w-full h-full flex items-center justify-center bg-gradient-to-br from-cyan-50 to-blue-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-4 border-cyan-200 border-t-cyan-600 mx-auto"></div>
          <p className="mt-4 text-cyan-700 font-medium">Carregando mapa...</p>
        </div>
      </div>
    );
  }

  return (
    <GoogleMap
      mapContainerStyle={{ width: '100%', height: '100%' }}
      center={center}
      zoom={zoom}
      options={mapOptions}
      onLoad={setMap}
    >
      {searchCenter && (
        <>
          <Marker
            position={searchCenter}
            icon={workLocationIcon}
            zIndex={1000}
            title="LOCAL"
          />
          <Circle
            center={searchCenter}
            radius={raioMetros}
            options={{
              fillColor: '#06b6d4',
              fillOpacity: 0.08,
              strokeColor: '#06b6d4',
              strokeOpacity: 0.4,
              strokeWeight: 2,
            }}
          />
        </>
      )}

      {imoveis.map((imovel) => {
        const isHighlighted = highlightedId === imovel.id;
        const color = getMarkerColor(imovel.tipologia);
        return (
          <Marker
            key={imovel.id}
            position={{ lat: imovel.lat, lng: imovel.lon }}
            icon={createPropertyIcon(color, isHighlighted)}
            zIndex={isHighlighted ? 999 : 1}
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
        >
          <div className="font-sans max-w-xs">
            {selectedImovel.imagem_url && (
              <img
                src={selectedImovel.imagem_url}
                alt={selectedImovel.titulo}
                className="w-full h-32 object-cover rounded-lg mb-3"
              />
            )}
            <div className="text-sm font-semibold text-gray-900 leading-tight mb-2">
              {selectedImovel.titulo || 'Sem título'}
            </div>
            <div className="text-lg font-bold text-cyan-700 mb-2">
              {selectedImovel.preco > 0 ? `${selectedImovel.preco}€/mês` : 'Consultar'}
            </div>
            <div className="flex gap-3 mb-3 text-xs text-gray-600">
              {selectedImovel.tipologia && (
                <span className="uppercase font-semibold">{selectedImovel.tipologia}</span>
              )}
              {selectedImovel.area_m2 > 0 && <span>{selectedImovel.area_m2}m²</span>}
              {selectedImovel.dist_metros != null && (
                <span>{formatDistance(selectedImovel.dist_metros)}</span>
              )}
            </div>
            <a
              href={selectedImovel.link}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-cyan-600 to-blue-600 text-white rounded-lg text-sm font-semibold hover:from-cyan-700 hover:to-blue-700 transition-all no-underline shadow-md"
            >
              Ver Anúncio
              <ExternalLink className="w-4 h-4" />
            </a>
          </div>
        </InfoWindow>
      )}
    </GoogleMap>
  );
}
