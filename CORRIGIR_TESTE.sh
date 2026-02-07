#!/bin/bash
cd ~/Aluguel_imoveis_Dev

echo "Removendo arquivo corrompido..."
rm -f teste_conexao.py

echo "Criando novo arquivo..."
cat > teste_conexao.py << 'ENDOFFILE'
#!/usr/bin/env python3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "motor_busca"))

print("="*60)
print("  TESTE DE CONEXAO")
print("="*60)

print("\n1. Testando imports...")
try:
    from supabase import create_client
    print("   OK supabase")
except Exception as e:
    print(f"   ERRO supabase: {e}")
    sys.exit(1)

try:
    from selenium import webdriver
    print("   OK selenium")
except Exception as e:
    print(f"   ERRO selenium: {e}")
    sys.exit(1)

try:
    from bs4 import BeautifulSoup
    print("   OK beautifulsoup4")
except Exception as e:
    print(f"   ERRO beautifulsoup4: {e}")
    sys.exit(1)

print("\n2. Testando configuracoes...")
try:
    from motor_busca.config import SUPABASE_URL, SUPABASE_SERVICE_KEY

    if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
        print("   ERRO Credenciais vazias")
        sys.exit(1)

    print(f"   OK SUPABASE_URL: {SUPABASE_URL}")
    print(f"   OK KEY: {SUPABASE_SERVICE_KEY[:20]}...")
except Exception as e:
    print(f"   ERRO: {e}")
    sys.exit(1)

print("\n3. Testando conexao...")
try:
    from motor_busca.db import get_supabase_client
    supabase = get_supabase_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    response = supabase.table('imoveis').select('id').limit(1).execute()
    print("   OK Conexao")
except Exception as e:
    print(f"   ERRO: {e}")
    sys.exit(1)

print("\n4. Verificando tabelas...")
try:
    supabase.table('demandas').select('count', count='exact').execute()
    print("   OK Tabela demandas")
    supabase.table('imoveis').select('count', count='exact').execute()
    print("   OK Tabela imoveis")
except Exception as e:
    print(f"   ERRO: {e}")
    sys.exit(1)

print("\n" + "="*60)
print("  TUDO OK! Sistema pronto")
print("="*60)
print("\nExecute: python3 motor_turbo.py\n")
ENDOFFILE

chmod +x teste_conexao.py
echo "Arquivo criado com sucesso!"
echo ""
echo "Executando teste..."
python3 teste_conexao.py
