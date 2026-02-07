#!/usr/bin/env python3
"""
🤖 MOTOR INFINITO - Sistema Automatizado de Scraping
Monitora demandas e busca imóveis continuamente em background
"""

import sys
import time
import random
from pathlib import Path
from datetime import datetime

# Adicionar motor_busca ao path
sys.path.insert(0, str(Path(__file__).parent / "motor_busca"))

from motor_busca.config import SUPABASE_URL, SUPABASE_SERVICE_KEY
from motor_busca.db import get_supabase_client
from motor_busca.geocoder import geocode_place
from motor_busca.scraper_sapo import scrape_sapo
from motor_busca.motor import upsert_imoveis_supabase

def print_header(texto):
    """Imprime cabeçalho formatado"""
    print("\n" + "="*70)
    print(f"  {texto}")
    print("="*70)

def print_status(emoji, mensagem):
    """Imprime status formatado"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {emoji} {mensagem}")

def processar_demandas_pendentes():
    """
    Busca e processa todas as demandas com status 'pendente'
    """
    try:
        supabase = get_supabase_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

        # Buscar demandas pendentes
        response = supabase.table('demandas').select('*').eq('status', 'pendente').execute()
        demandas = response.data

        if not demandas:
            print_status("💤", "Nenhuma demanda pendente no momento")
            return 0

        print_status("📋", f"Encontradas {len(demandas)} demanda(s) pendente(s)")

        processadas = 0

        for idx, demanda in enumerate(demandas, 1):
            demanda_id = demanda['id']
            termo_busca = demanda.get('termo', demanda.get('termo_busca', ''))
            lat = demanda.get('lat', 0)
            lng = demanda.get('lng', 0)
            raio_metros = demanda.get('raio_metros', 10000)

            print_header(f"DEMANDA {idx}/{len(demandas)}: {termo_busca}")

            # Marcar como processando
            try:
                supabase.table('demandas').update({
                    'status': 'processando'
                }).eq('id', demanda_id).execute()
            except:
                pass

            try:
                # Scraping SAPO
                print_status("🔍", f"Iniciando scraping no SAPO...")
                imoveis = scrape_sapo(termo_busca, raio_metros)
                print_status("✅", f"Encontrados {len(imoveis)} imóveis")

                if imoveis:
                    # Geocodificar imóveis sem coordenadas
                    print_status("🗺️", "Geocodificando endereços...")
                    for imovel in imoveis:
                        if not imovel.get('lat') or not imovel.get('lon'):
                            endereco = f"{imovel.get('endereco', '')}, {imovel.get('cidade', '')}, Portugal"
                            coords = geocode_place(endereco)
                            if coords:
                                imovel['lat'] = coords['lat']
                                imovel['lon'] = coords['lon']

                        # Calcular distância do ponto de busca
                        if imovel.get('lat') and imovel.get('lon') and lat and lng:
                            from math import radians, sin, cos, sqrt, atan2
                            R = 6371000  # Raio da Terra em metros

                            lat1, lon1 = radians(lat), radians(lng)
                            lat2, lon2 = radians(imovel['lat']), radians(imovel['lon'])

                            dlat = lat2 - lat1
                            dlon = lon2 - lon1

                            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
                            c = 2 * atan2(sqrt(a), sqrt(1-a))
                            distancia = int(R * c)

                            imovel['dist_metros'] = distancia

                    # Salvar no banco
                    print_status("💾", "Salvando imóveis no banco de dados...")
                    upsert_imoveis_supabase(supabase, imoveis)
                    print_status("✅", "Imóveis salvos com sucesso!")

                # Marcar como concluído
                supabase.table('demandas').update({
                    'status': 'concluido',
                    'num_resultados': len(imoveis)
                }).eq('id', demanda_id).execute()

                print_status("🎉", f"Demanda '{termo_busca}' processada com sucesso!")
                processadas += 1

                # Pausa entre demandas
                if idx < len(demandas):
                    pausa = random.uniform(3, 7)
                    print_status("⏸️", f"Pausando {pausa:.1f}s antes da próxima demanda...")
                    time.sleep(pausa)

            except Exception as e:
                print_status("❌", f"Erro ao processar demanda: {e}")
                try:
                    supabase.table('demandas').update({
                        'status': 'erro'
                    }).eq('id', demanda_id).execute()
                except:
                    pass
                continue

        return processadas

    except Exception as e:
        print_status("❌", f"Erro geral no processamento: {e}")
        return 0

def main():
    """
    Loop principal do motor infinito
    """
    print_header("🤖 MOTOR INFINITO - SISTEMA DE SCRAPING AUTOMATIZADO")
    print_status("🚀", "Motor iniciado em modo loop infinito")
    print_status("⚠️", "Pressione Ctrl+C para parar")

    ciclo = 0

    try:
        while True:
            ciclo += 1

            print_header(f"CICLO #{ciclo} - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

            processadas = processar_demandas_pendentes()

            if processadas > 0:
                print_status("📊", f"Ciclo finalizado: {processadas} demanda(s) processada(s)")
            else:
                print_status("💤", "Nenhuma demanda processada neste ciclo")

            # Intervalo aleatório entre 5-10 minutos
            intervalo_segundos = random.randint(300, 600)
            minutos = intervalo_segundos // 60
            segundos = intervalo_segundos % 60

            print_status("⏰", f"Próximo ciclo em {minutos}min {segundos}s")
            print("="*70 + "\n")

            time.sleep(intervalo_segundos)

    except KeyboardInterrupt:
        print_header("🛑 MOTOR INFINITO INTERROMPIDO PELO USUÁRIO")
        print_status("📊", f"Total de ciclos executados: {ciclo}")
        print_status("👋", "Até logo!")
        sys.exit(0)

    except Exception as e:
        print_header("💥 ERRO FATAL NO MOTOR INFINITO")
        print_status("❌", f"Erro: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
