#!/usr/bin/env python3
"""Verificar conexão com Supabase"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Carregar .env
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

# Pegar credenciais (com fallback para VITE_)
supabase_url = os.getenv("SUPABASE_URL") or os.getenv("VITE_SUPABASE_URL", "")
supabase_anon = os.getenv("SUPABASE_ANON_KEY") or os.getenv("VITE_SUPABASE_ANON_KEY", "")

print("\n🔍 VERIFICANDO CONEXÃO COM SUPABASE")
print("=" * 60)
print(f"URL: {supabase_url}")
print(f"Key: {supabase_anon[:30]}...")

try:
    from supabase import create_client
    supabase = create_client(supabase_url, supabase_anon)

    # Testar query
    result = supabase.table("imoveis").select("id, titulo, preco, cidade").limit(3).execute()

    if result and result.data:
        print(f"\n✅ CONEXÃO OK! Encontrados {len(result.data)} imóveis:")
        for item in result.data:
            print(f"\n  📍 {item.get('titulo', 'Sem título')}")
            print(f"     💰 {item.get('preco', 0):,.0f} €")
            print(f"     🏙️  {item.get('cidade', 'N/A')}")
    else:
        print("\n⚠️ Nenhum imóvel encontrado (tabela vazia ou RLS ativo)")

    print("\n" + "=" * 60)
    print("✅ Site funcionando em: http://localhost:8501")
    print("=" * 60 + "\n")

except Exception as e:
    print(f"\n❌ ERRO: {e}\n")
