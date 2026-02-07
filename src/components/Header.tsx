import { MapPin, Crown } from 'lucide-react';

interface HeaderProps {
  onFounderClick: () => void;
}

export default function Header({ onFounderClick }: HeaderProps) {
  return (
    <header className="fixed top-0 left-0 right-0 z-[1000] bg-gradient-to-r from-white via-cyan-50/30 to-blue-50/30 backdrop-blur-md border-b border-cyan-200/50 h-14 shadow-sm">
      <div className="h-full px-4 flex items-center justify-between max-w-screen-2xl mx-auto">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 bg-gradient-to-br from-cyan-500 via-blue-500 to-blue-600 rounded-lg flex items-center justify-center shadow-md shadow-blue-200">
            <MapPin className="w-5 h-5 text-white" strokeWidth={2.5} />
          </div>
          <div className="flex items-baseline gap-1.5">
            <span className="text-lg font-bold bg-gradient-to-r from-cyan-700 to-blue-700 bg-clip-text text-transparent tracking-tight">Lugar</span>
            <span className="text-[11px] text-blue-600 font-semibold tracking-wide uppercase">Portugal</span>
          </div>
        </div>

        <button
          onClick={onFounderClick}
          className="flex items-center gap-1.5 px-3.5 py-1.5 bg-gradient-to-r from-amber-100 to-yellow-100 hover:from-amber-200 hover:to-yellow-200 border border-amber-300/60 rounded-full text-amber-900 text-xs font-semibold transition-all hover:shadow-md shadow-amber-200/50"
        >
          <Crown className="w-3.5 h-3.5" />
          <span className="hidden sm:inline">Membro Fundador</span>
          <span className="sm:hidden">Fundador</span>
        </button>
      </div>
    </header>
  );
}
