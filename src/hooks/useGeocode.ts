import { useState, useCallback } from 'react';

interface GeocodeResult {
  lat: number;
  lon: number;
  displayName: string;
}

export function useGeocode() {
  const [geocoding, setGeocoding] = useState(false);

  const geocode = useCallback(async (query: string): Promise<GeocodeResult | null> => {
    setGeocoding(true);
    try {
      const encoded = encodeURIComponent(`${query}, Portugal`);
      const res = await fetch(
        `https://nominatim.openstreetmap.org/search?format=json&q=${encoded}&limit=1&countrycodes=pt`,
        { headers: { 'Accept-Language': 'pt' } }
      );
      const data = await res.json();

      if (data && data.length > 0) {
        return {
          lat: parseFloat(data[0].lat),
          lon: parseFloat(data[0].lon),
          displayName: data[0].display_name,
        };
      }
      return null;
    } catch {
      return null;
    } finally {
      setGeocoding(false);
    }
  }, []);

  return { geocode, geocoding };
}
