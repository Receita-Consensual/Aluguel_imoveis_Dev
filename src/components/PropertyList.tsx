import { useRef, useEffect } from 'react';
import { Loader2, SearchX } from 'lucide-react';
import PropertyCard from './PropertyCard';
import type { Imovel } from '../types/imovel';

interface PropertyListProps {
  imoveis: Imovel[];
  loading: boolean;
  polling: boolean;
  hasSearched: boolean;
  highlightedId: string | null;
  onHover: (id: string | null) => void;
  scrollToId: string | null;
}

export default function PropertyList({
  imoveis,
  loading,
  polling,
  hasSearched,
  highlightedId,
  onHover,
  scrollToId,
}: PropertyListProps) {
  const listRef = useRef<HTMLDivElement>(null);
  const cardRefs = useRef<Record<string, HTMLDivElement | null>>({});

  useEffect(() => {
    if (scrollToId && cardRefs.current[scrollToId]) {
      cardRefs.current[scrollToId]?.scrollIntoView({
        behavior: 'smooth',
        block: 'nearest',
      });
    }
  }, [scrollToId]);

  if (loading && !polling) {
    return (
      <div className="flex flex-col items-center justify-center py-12 text-slate-400">
        <Loader2 className="w-8 h-8 animate-spin mb-3" />
        <p className="text-sm">A procurar im\u00f3veis...</p>
      </div>
    );
  }

  if (hasSearched && imoveis.length === 0 && !polling) {
    return (
      <div className="flex flex-col items-center justify-center py-12 text-slate-400">
        <SearchX className="w-10 h-10 mb-3" />
        <p className="text-sm font-medium">Nenhum im\u00f3vel encontrado nesta zona</p>
        <p className="text-xs mt-1 text-center max-w-[240px]">
          Tenta aumentar o raio de busca ou procurar noutra zona
        </p>
      </div>
    );
  }

  if (!hasSearched) {
    return (
      <div className="flex flex-col items-center justify-center py-12 text-slate-400">
        <div className="w-16 h-16 bg-slate-100 rounded-2xl flex items-center justify-center mb-4">
          <SearchX className="w-8 h-8 text-slate-300" />
        </div>
        <p className="text-sm font-medium text-slate-500">Procura o teu pr\u00f3ximo lar</p>
        <p className="text-xs mt-1 text-center max-w-[240px]">
          Indica onde vais trabalhar e encontra apartamentos perto de ti
        </p>
      </div>
    );
  }

  return (
    <div ref={listRef} className="space-y-3">
      {polling && (
        <div className="flex items-center gap-2 px-3 py-2 bg-sky-50 border border-sky-200 rounded-lg">
          <Loader2 className="w-4 h-4 animate-spin text-sky-600" />
          <p className="text-xs text-sky-700">A procurar mais im\u00f3veis nesta zona...</p>
        </div>
      )}
      {imoveis.map((imovel) => (
        <div
          key={imovel.id}
          ref={(el) => { cardRefs.current[imovel.id] = el; }}
        >
          <PropertyCard
            imovel={imovel}
            isHighlighted={highlightedId === imovel.id}
            onHover={onHover}
          />
        </div>
      ))}
    </div>
  );
}
