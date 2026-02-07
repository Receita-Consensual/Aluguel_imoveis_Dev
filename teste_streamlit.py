#!/usr/bin/env python3
"""Teste rápido de conexão com Supabase para Streamlit"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Carregar .env
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

print("=" * 60)
print("🔍 TESTE DE CONFIGURAÇÃO STREAMLIT")
print("=" * 60)

# Verificar variáveis de ambiente
supabase_url = os.getenv("SUPABASE_URL", "")
supabase_anon = os.getenv("SUPABASE_ANON_KEY", "")
google_key = os.getenv("GOOGLE_API_KEY", "")

print(f"\n📌 SUPABASE_URL: {'✓ OK' if supabase_url else '✗ NÃO ENCONTRADA'}")
if supabase_url:
    print(f"   {supabase_url}")

print(f"\n📌 SUPABASE_ANON_KEY: {'✓ OK' if supabase_anon else '✗ NÃO ENCONTRADA'}")
if supabase_anon:
    print(f"   {supabase_anon[:50]}... (length: {len(supabase_anon)})")

print(f"\n📌 GOOGLE_API_KEY: {'✓ OK' if google_key else '✗ NÃO ENCONTRADA'}")
if google_key:
    print(f"   {google_key[:30]}... (length: {len(google_key)})")

# Tentar conectar ao Supabase
if supabase_url and supabase_anon:
    print("\n" + "=" * 60)
    print("🔌 TESTANDO CONEXÃO COM SUPABASE...")
    print("=" * 60)
    try:
        from supabase import create_client
        supabase = create_client(supabase_url, supabase_anon)

        # Testar query simples
        result = supabase.table("imoveis").select("id").limit(5).execute()

        if result and result.data:
            print(f"\n✅ CONEXÃO OK! Encontrados {len(result.data)} imóveis de teste")
            print("\n📋 Primeiros registros:")
            for idx, item in enumerate(result.data, 1):
                print(f"   {idx}. ID: {item['id']}")
        else:
            print("\n⚠️ Conexão estabelecida, mas nenhum dado retornado")
            print("   Isso pode ser por causa das políticas RLS (Row Level Security)")

    except Exception as e:
        print(f"\n❌ ERRO NA CONEXÃO: {e}")
else:
    print("\n❌ Não é possível testar conexão - variáveis de ambiente faltando")

print("\n" + "=" * 60)
print("✅ Teste concluído!")
print("=" * 60)
print("\nSe tudo estiver OK, rode o Streamlit com:")
print("  streamlit run app.py\n")
