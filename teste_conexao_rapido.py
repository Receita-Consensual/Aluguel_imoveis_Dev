#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

url = os.getenv("SUPABASE_URL")
key = os.getenv("SUPABASE_SERVICE_KEY")

print(f"URL: {url}")
print(f"Key length: {len(key) if key else 0}")

try:
    supabase = create_client(url, key)
    result = supabase.table("imoveis").select("id").limit(1).execute()
    print(f"✓ Conexão OK! Encontrados registros na tabela imoveis")
    print(f"  Total de registros testados: {len(result.data)}")
except Exception as e:
    print(f"✗ Erro na conexão: {e}")
