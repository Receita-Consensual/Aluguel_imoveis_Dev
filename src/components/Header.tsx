import { MapPin, Crown } from 'lucide-react';

interface HeaderProps {
  onFounderClick: () => void;
}

export default function Header({ onFounderClick }: HeaderProps) {
  return (
    <header className="fixed top-0 left-0 right-0 z-[1000] bg-white/95 backdrop-blur-md border-b border-slate-200/80 h-14">
      <div className="h-full px-4 flex items-center justify-between max-w-screen-2xl mx-auto">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 bg-gradient-to-br from-teal-500 to-teal-700 rounded-lg flex items-center justify-center shadow-sm shadow-teal-200">
            <MapPin className="w-5 h-5 text-white" strokeWidth={2.5} />
          </div>
          <div className="flex items-baseline gap-1.5">
            <span className="text-lg font-bold text-slate-900 tracking-tight">Lugar</span>
            <span className="text-[11px] text-teal-600 font-semibold tracking-wide uppercase">Portugal</span>
          </div>
        </div>

        <button
          onClick={onFounderClick}
          className="flex items-center gap-1.5 px-3.5 py-1.5 bg-amber-50 hover:bg-amber-100 border border-amber-200/80 rounded-full text-amber-800 text-xs font-semibold transition-all hover:shadow-sm"
        >
          <Crown className="w-3.5 h-3.5" />
          <span className="hidden sm:inline">Membro Fundador</span>
          <span className="sm:hidden">Fundador</span>
        </button>
      </div>
    </header>
  );
}
