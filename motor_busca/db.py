from supabase import create_client
from config import SUPABASE_URL, SUPABASE_SERVICE_KEY


def get_client():
    if not SUPABASE_SERVICE_KEY:
        raise ValueError(
            "SUPABASE_SERVICE_KEY nao definida. "
            "Exporta a variavel: export SUPABASE_SERVICE_KEY='sua_chave_aqui'"
        )
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


def upsert_imoveis(client, imoveis: list[dict]) -> int:
    if not imoveis:
        return 0

    inserted = 0
    for imovel in imoveis:
        try:
            existing = (
                client.table("imoveis")
                .select("id")
                .eq("link", imovel["link"])
                .maybe_single()
                .execute()
            )

            if existing.data:
                client.table("imoveis").update({
                    "preco": imovel["preco"],
                    "imagem_url": imovel["imagem_url"],
                    "descricao": imovel["descricao"],
                    "mobiliado": imovel["mobiliado"],
                }).eq("link", imovel["link"]).execute()
            else:
                location_value = None
                if imovel["lat"] != 0 and imovel["lon"] != 0:
                    location_value = f"POINT({imovel['lon']} {imovel['lat']})"

                client.table("imoveis").insert({
                    **imovel,
                    "location": location_value,
                }).execute()
                inserted += 1

        except Exception as e:
            if "duplicate" in str(e).lower() or "23505" in str(e):
                continue
            print(f"  [db] Erro ao inserir: {e}")

    return inserted


def get_demandas_pendentes(client) -> list[dict]:
    result = (
        client.table("demandas")
        .select("*")
        .eq("status", "pendente")
        .order("criado_em", desc=False)
        .limit(10)
        .execute()
    )
    return result.data or []


def marcar_demanda_processando(client, demanda_id: str):
    client.table("demandas").update(
        {"status": "processando"}
    ).eq("id", demanda_id).execute()


def marcar_demanda_concluida(client, demanda_id: str):
    client.table("demandas").update(
        {"status": "concluido"}
    ).eq("id", demanda_id).execute()
