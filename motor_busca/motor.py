"""
Motor de Busca - Lugar Portugal
===============================
Script que roda continuamente, varrendo Idealista e SAPO
para alimentar o banco Supabase com imoveis para arrendar.

USO:
  1. pip install -r requirements.txt
  2. export SUPABASE_SERVICE_KEY="sua_service_role_key_aqui"
  3. python motor.py

O motor faz dois tipos de busca:
  A) Varredura programada: percorre todas as cidades a cada ciclo
  B) Demandas sob pedido: processa buscas especificas feitas pelos usuarios
"""

import time
import traceback
from datetime import datetime

from config import (
    CIDADES_PORTUGAL,
    INTERVALO_ENTRE_CIDADES_SEG,
    INTERVALO_ENTRE_CICLOS_MIN,
)
from db import (
    get_client,
    upsert_imoveis,
    get_demandas_pendentes,
    marcar_demanda_processando,
    marcar_demanda_concluida,
)
from scraper_idealista import scrape_cidade as scrape_idealista
from scraper_sapo import scrape_cidade as scrape_sapo


def processar_cidade(client, cidade: str) -> int:
    print(f"\n--- {cidade} ---")
    total_inseridos = 0

    try:
        imoveis_idealista = scrape_idealista(cidade)
        n = upsert_imoveis(client, imoveis_idealista)
        total_inseridos += n
        print(f"  Idealista: {len(imoveis_idealista)} encontrados, {n} novos")
    except Exception as e:
        print(f"  Idealista ERRO: {e}")

    time.sleep(2)

    try:
        imoveis_sapo = scrape_sapo(cidade)
        n = upsert_imoveis(client, imoveis_sapo)
        total_inseridos += n
        print(f"  SAPO: {len(imoveis_sapo)} encontrados, {n} novos")
    except Exception as e:
        print(f"  SAPO ERRO: {e}")

    return total_inseridos


def processar_demandas(client):
    demandas = get_demandas_pendentes(client)
    if not demandas:
        return

    print(f"\n=== {len(demandas)} demandas pendentes ===")

    for demanda in demandas:
        termo = demanda.get("termo", "")
        demanda_id = demanda["id"]

        print(f"  Processando demanda: '{termo}'")
        marcar_demanda_processando(client, demanda_id)

        try:
            cidade = termo.split(",")[0].strip().title()

            imoveis_idealista = scrape_idealista(cidade)
            upsert_imoveis(client, imoveis_idealista)

            imoveis_sapo = scrape_sapo(cidade)
            upsert_imoveis(client, imoveis_sapo)

            total = len(imoveis_idealista) + len(imoveis_sapo)
            print(f"  Demanda '{termo}': {total} imoveis encontrados")

        except Exception as e:
            print(f"  Demanda ERRO: {e}")

        marcar_demanda_concluida(client, demanda_id)
        time.sleep(2)


def ciclo_completo(client):
    inicio = datetime.now()
    print(f"\n{'='*60}")
    print(f"CICLO INICIADO: {inicio.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")

    total_global = 0

    processar_demandas(client)

    for cidade in CIDADES_PORTUGAL:
        try:
            n = processar_cidade(client, cidade)
            total_global += n
        except Exception as e:
            print(f"  ERRO CRITICO em {cidade}: {e}")
            traceback.print_exc()

        time.sleep(INTERVALO_ENTRE_CIDADES_SEG)

        try:
            processar_demandas(client)
        except Exception:
            pass

    fim = datetime.now()
    duracao = (fim - inicio).total_seconds() / 60
    print(f"\n{'='*60}")
    print(f"CICLO CONCLUIDO: {fim.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Duracao: {duracao:.1f} min | Novos imoveis: {total_global}")
    print(f"{'='*60}")


def main():
    print("Motor de Busca - Lugar Portugal")
    print("Conectando ao Supabase...")

    client = get_client()

    count = client.table("imoveis").select("id", count="exact", head=True).execute()
    print(f"Imoveis no banco: {count.count}")
    print(f"Intervalo entre ciclos: {INTERVALO_ENTRE_CICLOS_MIN} min")
    print("Motor iniciado. Ctrl+C para parar.\n")

    while True:
        try:
            ciclo_completo(client)
        except KeyboardInterrupt:
            print("\nMotor parado pelo usuario.")
            break
        except Exception as e:
            print(f"\nERRO NO CICLO: {e}")
            traceback.print_exc()

        print(f"\nProximo ciclo em {INTERVALO_ENTRE_CICLOS_MIN} minutos...")
        try:
            time.sleep(INTERVALO_ENTRE_CICLOS_MIN * 60)
        except KeyboardInterrupt:
            print("\nMotor parado pelo usuario.")
            break


if __name__ == "__main__":
    main()
