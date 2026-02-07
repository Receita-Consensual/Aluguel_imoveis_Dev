#!/bin/bash

echo "📋 Copiando arquivos corretos para o servidor..."

# Copiar motor_busca/db.py
cat > ~/Aluguel_imoveis_Dev/motor_busca/db.py << 'DBPY'
import json
from supabase import create_client
from config import SUPABASE_URL, SUPABASE_SERVICE_KEY


def get_client():
    key = SUPABASE_SERVICE_KEY
    if not key:
        raise ValueError(
            "SUPABASE_SERVICE_KEY nao definida. "
            "Exporta a variavel: export SUPABASE_SERVICE_KEY='sua_chave_aqui'"
        )
    return create_client(SUPABASE_URL, key)

# Alias para compatibilidade
get_supabase_client = lambda url=None, key=None: get_client()


def upsert_imoveis(client, imoveis: list[dict]) -> int:
    if not imoveis:
        return 0

    inserted = 0
    for imovel in imoveis:
        try:
            result = client.rpc("upsert_imovel", {
                "p_titulo": imovel.get("titulo", ""),
                "p_link": imovel["link"],
                "p_endereco": imovel.get("endereco", ""),
                "p_cidade": imovel.get("cidade", ""),
                "p_freguesia": imovel.get("freguesia", ""),
                "p_tipologia": imovel.get("tipologia", ""),
                "p_preco": imovel.get("preco", 0),
                "p_area_m2": imovel.get("area_m2", 0),
                "p_imagem_url": imovel.get("imagem_url", ""),
                "p_lat": imovel.get("lat", 0),
                "p_lon": imovel.get("lon", 0),
                "p_mobiliado": imovel.get("mobiliado", False),
                "p_fonte": imovel.get("fonte", ""),
                "p_descricao": imovel.get("descricao", ""),
            }).execute()
            if result.data == "inserted":
                inserted += 1
        except Exception as e:
            if "duplicate" in str(e).lower() or "23505" in str(e):
                continue
            print(f"  [db] Erro ao inserir: {e}")

    return inserted


def get_demandas_pendentes(client) -> list[dict]:
    result = client.rpc("get_demandas_pendentes_rpc").execute()
    return result.data or []


def marcar_demanda_processando(client, demanda_id: str):
    client.rpc("atualizar_demanda_status", {
        "p_id": demanda_id,
        "p_status": "processando",
    }).execute()


def marcar_demanda_concluida(client, demanda_id: str):
    client.rpc("atualizar_demanda_status", {
        "p_id": demanda_id,
        "p_status": "concluido",
    }).execute()
DBPY

echo "✅ Arquivo motor_busca/db.py corrigido!"
echo ""
echo "Agora execute o teste:"
echo "cd ~/Aluguel_imoveis_Dev && python3 teste_rapido.py"
