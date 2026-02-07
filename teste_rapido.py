#!/usr/bin/env python3
import sys
sys.path.insert(0, 'motor_busca')

from motor_busca.config import SUPABASE_URL, SUPABASE_SERVICE_KEY
from motor_busca.db import get_supabase_client

try:
    client = get_supabase_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    result = client.table('imoveis').select('id').limit(1).execute()
    print('✓ Conexão OK!')
except Exception as e:
    print(f'✗ Erro: {e}')
