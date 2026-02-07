import { useState, useEffect, FormEvent } from 'react';
import { Crown, Check, Loader2, Users } from 'lucide-react';
import { supabase } from '../lib/supabase';

interface FounderSectionProps {
  visible: boolean;
  onClose: () => void;
}

export default function FounderSection({ visible, onClose }: FounderSectionProps) {
  const [email, setEmail] = useState('');
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [errorMsg, setErrorMsg] = useState('');
  const [count, setCount] = useState(0);

  useEffect(() => {
    if (visible) {
      supabase
        .from('alertas_fundador')
        .select('id', { count: 'exact', head: true })
        .then(({ count: c }) => {
          if (c != null) setCount(c);
        });
    }
  }, [visible]);

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    if (!email.trim()) return;

    setStatus('loading');
    setErrorMsg('');

    const { error } = await supabase
      .from('alertas_fundador')
      .insert({ email: email.trim().toLowerCase() });

    if (error) {
      if (error.code === '23505') {
        setErrorMsg('Este email j\u00e1 est\u00e1 registado.');
      } else {
        setErrorMsg('Ocorreu um erro. Tenta novamente.');
      }
      setStatus('error');
    } else {
      setStatus('success');
      setCount((c) => c + 1);
    }
  };

  if (!visible) return null;

  return (
    <div className="fixed inset-0 z-[2000] flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm" onClick={onClose}>
      <div
        className="bg-slate-900 rounded-2xl p-6 sm:p-8 max-w-md w-full shadow-2xl border border-slate-700 animate-fade-in"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 bg-amber-500 rounded-xl flex items-center justify-center">
            <Crown className="w-5 h-5 text-white" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-white">Membro Fundador</h2>
            <p className="text-xs text-slate-400">Acesso exclusivo e desconto vital\u00edcio</p>
          </div>
        </div>

        <div className="space-y-3 mb-6">
          <div className="flex items-start gap-2.5">
            <Check className="w-4 h-4 text-emerald-400 mt-0.5 shrink-0" />
            <p className="text-sm text-slate-300">20% de desconto vital\u00edcio em todos os planos</p>
          </div>
          <div className="flex items-start gap-2.5">
            <Check className="w-4 h-4 text-emerald-400 mt-0.5 shrink-0" />
            <p className="text-sm text-slate-300">Alertas priorit\u00e1rios de novos im\u00f3veis</p>
          </div>
          <div className="flex items-start gap-2.5">
            <Check className="w-4 h-4 text-emerald-400 mt-0.5 shrink-0" />
            <p className="text-sm text-slate-300">Acesso antecipado a novas funcionalidades</p>
          </div>
        </div>

        {status === 'success' ? (
          <div className="bg-emerald-900/30 border border-emerald-700 rounded-xl p-4 text-center">
            <Check className="w-8 h-8 text-emerald-400 mx-auto mb-2" />
            <p className="text-sm font-semibold text-emerald-300">Registado com sucesso!</p>
            <p className="text-xs text-emerald-400 mt-1">Vamos contactar-te em breve.</p>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="space-y-3">
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="O teu email"
              required
              className="w-full px-4 py-2.5 bg-slate-800 border border-slate-600 rounded-lg text-sm text-white placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-amber-500 focus:border-transparent"
            />
            {errorMsg && <p className="text-xs text-red-400">{errorMsg}</p>}
            <button
              type="submit"
              disabled={status === 'loading'}
              className="w-full flex items-center justify-center gap-2 px-4 py-2.5 bg-amber-500 hover:bg-amber-400 disabled:bg-slate-600 text-slate-900 rounded-lg text-sm font-bold transition-colors"
            >
              {status === 'loading' ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <>
                  <Crown className="w-4 h-4" />
                  Garantir 20% OFF Vital\u00edcio
                </>
              )}
            </button>
          </form>
        )}

        {count > 0 && (
          <div className="flex items-center justify-center gap-1.5 mt-4">
            <Users className="w-3.5 h-3.5 text-slate-400" />
            <span className="text-xs text-slate-400 font-medium">{count} fundadores registados</span>
          </div>
        )}

        <button
          onClick={onClose}
          className="w-full mt-4 text-xs text-slate-400 hover:text-white font-medium transition-colors"
        >
          Fechar
        </button>
      </div>
    </div>
  );
}
