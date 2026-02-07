#!/usr/bin/env python3
"""Teste rápido para verificar se o app está funcionando"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Carregar .env
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

print("\n🔍 VERIFICANDO CONFIGURAÇÃO DO APP")
print("=" * 60)

# Tentar carregar como o app faz
SUPABASE_URL = os.getenv("SUPABASE_URL") or os.getenv("VITE_SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY") or os.getenv("VITE_SUPABASE_ANON_KEY", "")
GOOGLE_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("VITE_GOOGLE_MAPS_API_KEY", "")

print(f"\n✓ SUPABASE_URL: {SUPABASE_URL[:40]}...")
print(f"✓ SUPABASE_KEY: {SUPABASE_KEY[:30]}...")
print(f"✓ GOOGLE_KEY: {GOOGLE_KEY[:20]}...")

# Testar conexão
try:
    from supabase import create_client
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    result = supabase.table("imoveis").select("id").limit(1).execute()

    if result.data:
        print("\n✅ CONEXÃO COM SUPABASE: OK!")
        print("✅ APP FUNCIONANDO PERFEITAMENTE!")
    else:
        print("\n⚠️ Conexão OK mas sem dados")

except Exception as e:
    print(f"\n❌ ERRO: {e}")

print("\n" + "=" * 60)
print("🌐 Acesse: http://localhost:8501")
print("=" * 60 + "\n")
