#!/usr/bin/env python3
"""Teste rápido de conexão com Supabase"""

import os
from supabase import create_client

print("="*60)
print("  TESTE DE CONEXÃO SUPABASE")
print("="*60)

# Carregar variáveis
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')

print(f"\nURL: {SUPABASE_URL}")
print(f"KEY: {SUPABASE_SERVICE_KEY[:20] if SUPABASE_SERVICE_KEY else 'NÃO ENCONTRADA'}...")

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    print("\n✗ ERRO: Configure as variáveis no .env")
    exit(1)

# Conectar
print("\nConectando...")
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# Testar
print("Testando tabelas...")
result = supabase.table('imoveis').select('id').limit(1).execute()
print(f"✓ Tabela imoveis: OK")

result = supabase.table('demandas').select('id').limit(1).execute()
print(f"✓ Tabela demandas: OK")

print("\n" + "="*60)
print("  ✓ SUCESSO! Sistema funcionando")
print("="*60)
