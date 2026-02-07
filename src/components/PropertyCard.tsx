import { ExternalLink, MapPin, Maximize2, Armchair } from 'lucide-react';
import type { Imovel } from '../types/imovel';

const PLACEHOLDER_IMAGE = 'https://images.pexels.com/photos/1396122/pexels-photo-1396122.jpeg?auto=compress&cs=tinysrgb&w=600';

const FONTE_COLORS: Record<string, string> = {
  idealista: 'bg-emerald-50 text-emerald-700 border-emerald-200',
  sapo: 'bg-orange-50 text-orange-700 border-orange-200',
  olx: 'bg-sky-50 text-sky-700 border-sky-200',
};

function formatDistance(meters?: number): string {
  if (!meters) return '';
  if (meters < 1000) return `${Math.round(meters)}m`;
  return `${(meters / 1000).toFixed(1)}km`;
}

function getTipoBadgeColor(tipo: string): string {
  const t = tipo.toLowerCase();
  if (t.includes('moradia') || t.includes('casa')) return 'bg-blue-100 text-blue-800';
  if (t.includes('quarto')) return 'bg-slate-100 text-slate-800';
  return 'bg-sky-100 text-sky-800';
}

interface PropertyCardProps {
  imovel: Imovel;
  isHighlighted: boolean;
  onHover: (id: string | null) => void;
}

export default function PropertyCard({ imovel, isHighlighted, onHover }: PropertyCardProps) {
  const fonteClass = FONTE_COLORS[imovel.fonte?.toLowerCase()] || 'bg-slate-50 text-slate-600 border-slate-200';

  return (
    <div
      onMouseEnter={() => onHover(imovel.id)}
      onMouseLeave={() => onHover(null)}
      className={`group bg-white rounded-xl border overflow-hidden transition-all duration-200 hover:shadow-lg hover:shadow-slate-200/60 ${
        isHighlighted
          ? 'border-blue-400 shadow-lg shadow-blue-100/50 ring-1 ring-blue-200'
          : 'border-slate-200/80'
      }`}
    >
      <div className="relative h-36 sm:h-40 overflow-hidden bg-slate-100">
        <img
          src={imovel.imagem_url || PLACEHOLDER_IMAGE}
          alt={imovel.titulo}
          className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500 ease-out"
          onError={(e) => {
            (e.target as HTMLImageElement).src = PLACEHOLDER_IMAGE;
          }}
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
        <div className="absolute top-2 left-2 flex gap-1.5">
          {imovel.tipologia && (
            <span className={`px-2 py-0.5 rounded-md text-[11px] font-bold ${getTipoBadgeColor(imovel.tipologia)}`}>
              {imovel.tipologia.toUpperCase()}
            </span>
          )}
          {imovel.mobiliado && (
            <span className="px-1.5 py-0.5 rounded-md text-[11px] font-medium bg-white/90 text-slate-700 flex items-center gap-0.5 backdrop-blur-sm">
              <Armchair className="w-3 h-3" />
            </span>
          )}
        </div>
        {imovel.dist_metros != null && (
          <div className="absolute top-2 right-2 px-2 py-0.5 bg-slate-900/75 backdrop-blur-sm text-white text-[11px] font-semibold rounded-md flex items-center gap-1">
            <MapPin className="w-3 h-3" />
            {formatDistance(imovel.dist_metros)}
          </div>
        )}
      </div>

      <div className="p-3.5 space-y-2">
        <div className="flex items-start justify-between gap-2">
          <div className="min-w-0 flex-1">
            <h3 className="text-sm font-semibold text-slate-900 truncate leading-tight">
              {imovel.titulo || 'Sem t\u00EDtulo'}
            </h3>
            <p className="text-xs text-slate-500 truncate mt-0.5">
              {imovel.endereco || imovel.freguesia || imovel.cidade}
            </p>
          </div>
          <div className="text-right shrink-0">
            <span className="text-base font-bold text-blue-700">
              {imovel.preco > 0 ? `${imovel.preco}\u20AC` : 'Consultar'}
            </span>
            {imovel.preco > 0 && <span className="text-[11px] text-slate-400 block">/m\u00EAs</span>}
          </div>
        </div>

        <div className="flex items-center gap-3 text-xs text-slate-500">
          {imovel.area_m2 > 0 && (
            <span className="flex items-center gap-1">
              <Maximize2 className="w-3 h-3" />
              {imovel.area_m2}m\u00B2
            </span>
          )}
          {imovel.cidade && (
            <span className="flex items-center gap-1">
              <MapPin className="w-3 h-3" />
              {imovel.cidade}
            </span>
          )}
        </div>

        <div className="flex items-center justify-between pt-1">
          {imovel.fonte && (
            <span className={`px-2 py-0.5 rounded text-[10px] font-medium border ${fonteClass}`}>
              via {imovel.fonte}
            </span>
          )}
          <a
            href={imovel.link}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center gap-1 px-3 py-1.5 bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white rounded-lg text-xs font-semibold transition-all ml-auto shadow-md shadow-blue-200/50"
          >
            Ver An\u00FAncio
            <ExternalLink className="w-3 h-3" />
          </a>
        </div>
      </div>
    </div>
  );
}
