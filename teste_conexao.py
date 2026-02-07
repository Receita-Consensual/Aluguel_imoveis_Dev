#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "motor_busca"))

print("="*60)
print("  TESTE DE CONEXÃO")
print("="*60)

print("\n1. Testando imports...")
try:
    from supabase import create_client
    print("   ✓ supabase")
except Exception as e:
    print(f"   ✗ supabase: {e}")
    sys.exit(1)

try:
    from selenium import webdriver
    print("   ✓ selenium")
except Exception as e:
    print(f"   ✗ selenium: {e}")
    sys.exit(1)

try:
    from bs4 import BeautifulSoup
    print("   ✓ beautifulsoup4")
except Exception as e:
    print(f"   ✗ beautifulsoup4: {e}")
    sys.exit(1)

print("\n2. Testando configurações...")
try:
    from motor_busca.config import SUPABASE_URL, SUPABASE_SERVICE_KEY

    if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
        print("   ✗ Credenciais vazias")
        sys.exit(1)

    print(f"   ✓ SUPABASE_URL: {SUPABASE_URL}")
    print(f"   ✓ KEY: {SUPABASE_SERVICE_KEY[:20]}...")
except Exception as e:
    print(f"   ✗ Erro: {e}")
    sys.exit(1)

print("\n3. Testando conexão...")
try:
    from motor_busca.db import get_supabase_client
    supabase = get_supabase_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    response = supabase.table('imoveis').select('id').limit(1).execute()
    print("   ✓ Conexão OK")
except Exception as e:
    print(f"   ✗ Erro: {e}")
    sys.exit(1)

print("\n4. Verificando tabelas...")
try:
    supabase.table('demandas').select('count', count='exact').execute()
    print("   ✓ Tabela demandas")
    supabase.table('imoveis').select('count', count='exact').execute()
    print("   ✓ Tabela imoveis")
except Exception as e:
    print(f"   ✗ Erro: {e}")
    sys.exit(1)

print("\n" + "="*60)
print("  ✓ TUDO OK! Sistema pronto")
print("="*60)
print("\nExecute: python3 motor_turbo.py\n")
