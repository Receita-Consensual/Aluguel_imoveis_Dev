import { MapPin, Crown } from 'lucide-react';

interface HeaderProps {
  onFounderClick: () => void;
}

export default function Header({ onFounderClick }: HeaderProps) {
  return (
    <header className="fixed top-0 left-0 right-0 z-[1000] bg-white/95 backdrop-blur-sm border-b border-slate-200 h-14">
      <div className="h-full px-4 flex items-center justify-between max-w-screen-2xl mx-auto">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 bg-sky-600 rounded-lg flex items-center justify-center">
            <MapPin className="w-5 h-5 text-white" strokeWidth={2.5} />
          </div>
          <span className="text-lg font-bold text-slate-900 tracking-tight">Lugar</span>
          <span className="hidden sm:inline text-xs text-slate-400 font-medium ml-1 mt-0.5">Portugal</span>
        </div>

        <button
          onClick={onFounderClick}
          className="flex items-center gap-1.5 px-3 py-1.5 bg-amber-50 hover:bg-amber-100 border border-amber-200 rounded-full text-amber-800 text-xs font-semibold transition-colors"
        >
          <Crown className="w-3.5 h-3.5" />
          <span className="hidden sm:inline">Membro Fundador</span>
          <span className="sm:hidden">Fundador</span>
        </button>
      </div>
    </header>
  );
}
