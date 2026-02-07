#!/usr/bin/env python3
import os
from supabase import create_client

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')

print(f"URL: {SUPABASE_URL}")
print(f"KEY: {SUPABASE_SERVICE_KEY[:20] if SUPABASE_SERVICE_KEY else 'NOT SET'}...")

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    print("ERRO: Configure .env")
    exit(1)

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
result = supabase.table('imoveis').select('id').limit(1).execute()
print("OK - Conexão funcionando")
