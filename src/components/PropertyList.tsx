import { useRef, useEffect } from 'react';
import { Loader2, Search, MapPin } from 'lucide-react';
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
      <div className="flex flex-col items-center justify-center py-16 text-slate-400">
        <Loader2 className="w-8 h-8 animate-spin mb-3 text-teal-500" />
        <p className="text-sm font-medium text-slate-500">A procurar im\u00F3veis...</p>
      </div>
    );
  }

  if (hasSearched && imoveis.length === 0 && !polling) {
    return (
      <div className="flex flex-col items-center justify-center py-16 text-slate-400">
        <div className="w-14 h-14 bg-slate-100 rounded-2xl flex items-center justify-center mb-4">
          <Search className="w-7 h-7 text-slate-300" />
        </div>
        <p className="text-sm font-semibold text-slate-600">Nenhum im\u00F3vel encontrado</p>
        <p className="text-xs mt-1.5 text-center max-w-[240px] text-slate-400 leading-relaxed">
          Tenta aumentar o raio de busca ou procurar noutra zona
        </p>
      </div>
    );
  }

  if (!hasSearched) {
    return (
      <div className="flex flex-col items-center justify-center py-16 text-slate-400">
        <div className="w-16 h-16 bg-gradient-to-br from-teal-50 to-teal-100 rounded-2xl flex items-center justify-center mb-4">
          <MapPin className="w-8 h-8 text-teal-500" />
        </div>
        <p className="text-sm font-semibold text-slate-600">Procura o teu pr\u00F3ximo lar</p>
        <p className="text-xs mt-1.5 text-center max-w-[260px] text-slate-400 leading-relaxed">
          Indica onde vais trabalhar e encontra apartamentos perto de ti em todo Portugal
        </p>
      </div>
    );
  }

  return (
    <div ref={listRef} className="space-y-3">
      {polling && (
        <div className="flex items-center gap-2 px-3 py-2.5 bg-teal-50 border border-teal-200/60 rounded-xl">
          <Loader2 className="w-4 h-4 animate-spin text-teal-600" />
          <p className="text-xs text-teal-700 font-medium">A procurar mais im\u00F3veis nesta zona...</p>
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
