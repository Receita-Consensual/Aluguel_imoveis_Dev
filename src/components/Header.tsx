import { Crown } from 'lucide-react';

interface HeaderProps {
  onFounderClick: () => void;
}

export default function Header({ onFounderClick }: HeaderProps) {
  return (
    <header className="fixed top-0 left-0 right-0 z-[1000] bg-gradient-to-r from-white via-slate-50/50 to-blue-50/40 backdrop-blur-md border-b border-slate-200/60 h-14 shadow-sm">
      <div className="h-full px-4 flex items-center justify-between max-w-screen-2xl mx-auto">
        <div className="flex items-center gap-2.5">
          <img
            src="/gemini_generated_image_su6quisu6quisu6q.png"
            alt="Lugar Portugal Logo"
            className="w-10 h-10 object-contain drop-shadow-md"
          />
          <div className="flex items-baseline gap-1.5">
            <span className="text-lg font-bold bg-gradient-to-r from-slate-700 to-blue-600 bg-clip-text text-transparent tracking-tight">Lugar</span>
            <span className="text-[11px] text-slate-600 font-semibold tracking-wide uppercase">Portugal</span>
          </div>
        </div>

        <button
          onClick={onFounderClick}
          className="flex items-center gap-1.5 px-3.5 py-1.5 bg-gradient-to-r from-amber-50 to-yellow-50 hover:from-amber-100 hover:to-yellow-100 border border-amber-200/60 rounded-full text-amber-800 text-xs font-semibold transition-all hover:shadow-md shadow-slate-200/50"
        >
          <Crown className="w-3.5 h-3.5" />
          <span className="hidden sm:inline">Membro Fundador</span>
          <span className="sm:hidden">Fundador</span>
        </button>
      </div>
    </header>
  );
}
