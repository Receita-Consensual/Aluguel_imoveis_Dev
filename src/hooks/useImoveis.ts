import { useState, useCallback } from 'react';
import { supabase } from '../lib/supabase';
import type { Imovel, SearchFilters } from '../types/imovel';

export function useImoveis() {
  const [imoveis, setImoveis] = useState<Imovel[]>([]);
  const [loading, setLoading] = useState(false);
  const [polling, setPolling] = useState(false);

  const searchByRadius = useCallback(async (
    lat: number,
    lon: number,
    raioMetros: number
  ): Promise<Imovel[]> => {
    setLoading(true);
    const { data, error } = await supabase.rpc('imoveis_no_raio', {
      p_lat: lat,
      p_lon: lon,
      p_raio_metros: raioMetros,
    });

    setLoading(false);
    if (error) {
      console.error('Search error:', error);
      return [];
    }

    const results = (data || []) as Imovel[];
    setImoveis(results);
    return results;
  }, []);

  const searchByViewport = useCallback(async (
    minLat: number,
    minLon: number,
    maxLat: number,
    maxLon: number
  ) => {
    const { data, error } = await supabase.rpc('imoveis_na_viewport', {
      p_min_lat: minLat,
      p_min_lon: minLon,
      p_max_lat: maxLat,
      p_max_lon: maxLon,
    });

    if (error) {
      console.error('Viewport search error:', error);
      return;
    }

    setImoveis((data || []) as Imovel[]);
  }, []);

  const createDemanda = useCallback(async (
    termo: string,
    lat: number,
    lon: number,
    raioKm: number
  ) => {
    await supabase.from('demandas').insert({
      termo,
      lat_centro: lat,
      lon_centro: lon,
      raio_km: raioKm,
    });
  }, []);

  const pollForResults = useCallback(async (
    lat: number,
    lon: number,
    raioMetros: number,
    termo: string
  ) => {
    setPolling(true);
    await createDemanda(termo, lat, lon, raioMetros / 1000);

    let attempts = 0;
    const maxAttempts = 12;

    const poll = async (): Promise<void> => {
      attempts++;
      const results = await searchByRadius(lat, lon, raioMetros);

      if (results.length >= 3 || attempts >= maxAttempts) {
        setPolling(false);
        return;
      }

      return new Promise((resolve) => {
        setTimeout(async () => {
          resolve(await poll());
        }, 5000);
      });
    };

    await poll();
  }, [createDemanda, searchByRadius]);

  const filterImoveis = useCallback((items: Imovel[], filters: SearchFilters): Imovel[] => {
    return items.filter((item) => {
      if (filters.tipologias.length > 0) {
        const normalizedTipo = item.tipologia.toLowerCase().trim();
        if (!filters.tipologias.some(t => normalizedTipo.includes(t.toLowerCase()))) {
          return false;
        }
      }

      if (item.preco > 0) {
        if (item.preco < filters.precoMin || item.preco > filters.precoMax) {
          return false;
        }
      }

      if (filters.areaMin > 0 && item.area_m2 > 0 && item.area_m2 < filters.areaMin) {
        return false;
      }
      if (filters.areaMax < 500 && item.area_m2 > 0 && item.area_m2 > filters.areaMax) {
        return false;
      }

      if (filters.mobiliado === 'sim' && !item.mobiliado) return false;
      if (filters.mobiliado === 'nao' && item.mobiliado) return false;

      return true;
    });
  }, []);

  return {
    imoveis,
    loading,
    polling,
    searchByRadius,
    searchByViewport,
    pollForResults,
    filterImoveis,
    setImoveis,
  };
}
