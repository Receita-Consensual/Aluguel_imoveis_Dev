import { Home, Building2, DoorOpen, Castle } from 'lucide-react';
import type { SearchFilters } from '../types/imovel';

const TIPOLOGIAS = [
  { label: 'T0', value: 't0', icon: DoorOpen },
  { label: 'T1', value: 't1', icon: DoorOpen },
  { label: 'T2', value: 't2', icon: Building2 },
  { label: 'T3', value: 't3', icon: Building2 },
  { label: 'T4', value: 't4', icon: Home },
  { label: 'T5+', value: 't5', icon: Home },
  { label: 'Moradia', value: 'moradia', icon: Castle },
  { label: 'Quarto', value: 'quarto', icon: DoorOpen },
];

interface FiltersProps {
  filters: SearchFilters;
  onChange: (filters: SearchFilters) => void;
  resultCount: number;
  raioLabel: string;
}

export default function Filters({ filters, onChange, resultCount, raioLabel }: FiltersProps) {
  const toggleTipologia = (value: string) => {
    const updated = filters.tipologias.includes(value)
      ? filters.tipologias.filter((t) => t !== value)
      : [...filters.tipologias, value];
    onChange({ ...filters, tipologias: updated });
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-slate-200/80 p-3 sm:p-4 space-y-3">
      <div className="flex items-center justify-between">
        <span className="text-sm font-semibold text-slate-900">Filtros</span>
        <span className="text-xs text-slate-500">
          {resultCount} {resultCount === 1 ? 'im\u00F3vel' : 'im\u00F3veis'} {raioLabel && `num raio de ${raioLabel}`}
        </span>
      </div>

      <div>
        <span className="text-xs text-slate-500 font-medium mb-1.5 block">Tipologia</span>
        <div className="flex flex-wrap gap-1.5">
          {TIPOLOGIAS.map(({ label, value, icon: Icon }) => (
            <button
              key={value}
              onClick={() => toggleTipologia(value)}
              className={`flex items-center gap-1 px-2.5 py-1.5 rounded-lg text-xs font-medium transition-all ${
                filters.tipologias.includes(value)
                  ? 'bg-teal-600 text-white shadow-sm'
                  : 'bg-slate-50 text-slate-600 hover:bg-slate-100 border border-slate-200'
              }`}
            >
              <Icon className="w-3 h-3" />
              {label}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className="text-xs text-slate-500 font-medium mb-1 block">
            Pre\u00E7o min ({filters.precoMin}\u20AC)
          </label>
          <input
            type="range"
            min={0}
            max={3000}
            step={50}
            value={filters.precoMin}
            onChange={(e) => onChange({ ...filters, precoMin: Number(e.target.value) })}
            className="w-full h-1.5 bg-slate-200 rounded-full appearance-none cursor-pointer accent-teal-600"
          />
        </div>
        <div>
          <label className="text-xs text-slate-500 font-medium mb-1 block">
            Pre\u00E7o m\u00E1x ({filters.precoMax}\u20AC)
          </label>
          <input
            type="range"
            min={0}
            max={3000}
            step={50}
            value={filters.precoMax}
            onChange={(e) => onChange({ ...filters, precoMax: Number(e.target.value) })}
            className="w-full h-1.5 bg-slate-200 rounded-full appearance-none cursor-pointer accent-teal-600"
          />
        </div>
      </div>

      <div className="grid grid-cols-2 gap-3">
        <div>
          <label className="text-xs text-slate-500 font-medium mb-1 block">
            \u00C1rea min ({filters.areaMin}m\u00B2)
          </label>
          <input
            type="range"
            min={0}
            max={500}
            step={10}
            value={filters.areaMin}
            onChange={(e) => onChange({ ...filters, areaMin: Number(e.target.value) })}
            className="w-full h-1.5 bg-slate-200 rounded-full appearance-none cursor-pointer accent-teal-600"
          />
        </div>
        <div>
          <label className="text-xs text-slate-500 font-medium mb-1 block">
            \u00C1rea m\u00E1x ({filters.areaMax}m\u00B2)
          </label>
          <input
            type="range"
            min={0}
            max={500}
            step={10}
            value={filters.areaMax}
            onChange={(e) => onChange({ ...filters, areaMax: Number(e.target.value) })}
            className="w-full h-1.5 bg-slate-200 rounded-full appearance-none cursor-pointer accent-teal-600"
          />
        </div>
      </div>

      <div>
        <span className="text-xs text-slate-500 font-medium mb-1.5 block">Mobiliado</span>
        <div className="flex gap-1.5">
          {(['todos', 'sim', 'nao'] as const).map((opt) => (
            <button
              key={opt}
              onClick={() => onChange({ ...filters, mobiliado: opt })}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                filters.mobiliado === opt
                  ? 'bg-teal-600 text-white shadow-sm'
                  : 'bg-slate-50 text-slate-600 hover:bg-slate-100 border border-slate-200'
              }`}
            >
              {opt === 'todos' ? 'Todos' : opt === 'sim' ? 'Sim' : 'N\u00E3o'}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
