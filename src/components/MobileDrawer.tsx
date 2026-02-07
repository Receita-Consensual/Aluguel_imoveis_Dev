import { useState, useRef, useEffect } from 'react';
import { ChevronUp, ChevronDown, List } from 'lucide-react';

interface MobileDrawerProps {
  children: React.ReactNode;
  resultCount: number;
}

export default function MobileDrawer({ children, resultCount }: MobileDrawerProps) {
  const [isOpen, setIsOpen] = useState(false);
  const drawerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (resultCount > 0 && !isOpen) {
      setIsOpen(true);
    }
  }, [resultCount]);

  return (
    <>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="lg:hidden fixed bottom-4 left-1/2 -translate-x-1/2 z-[1001] flex items-center gap-2 px-5 py-2.5 bg-teal-600 shadow-lg shadow-teal-200/50 rounded-full text-sm font-semibold text-white hover:bg-teal-700 transition-all active:scale-95"
      >
        <List className="w-4 h-4" />
        {resultCount > 0 ? `${resultCount} im\u00f3veis` : 'Ver lista'}
        {isOpen ? <ChevronDown className="w-4 h-4" /> : <ChevronUp className="w-4 h-4" />}
      </button>

      <div
        ref={drawerRef}
        className={`lg:hidden fixed bottom-0 left-0 right-0 z-[1000] bg-white rounded-t-2xl shadow-2xl border-t border-slate-200 transition-transform duration-300 ease-out ${
          isOpen ? 'translate-y-0' : 'translate-y-full'
        }`}
        style={{ maxHeight: '60vh' }}
      >
        <div className="flex justify-center pt-2.5 pb-1">
          <div className="w-10 h-1 bg-slate-300 rounded-full" />
        </div>
        <div className="overflow-y-auto px-3 pb-16" style={{ maxHeight: 'calc(60vh - 24px)' }}>
          {children}
        </div>
      </div>
    </>
  );
}
