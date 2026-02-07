#!/bin/bash
# Script para instalar CORRETAMENTE todas as dependências

echo "============================================"
echo "  INSTALAÇÃO CORRETA DO MOTOR DE BUSCA"
echo "============================================"
echo ""

cd ~/Aluguel_imoveis_Dev

# Ativar ambiente virtual
echo "1. Ativando ambiente virtual..."
source venv/bin/activate

# Instalar pacotes CORRETOS (minúsculos)
echo ""
echo "2. Instalando pacotes Python..."
echo "   IMPORTANTE: 'supabase' em MINÚSCULO!"
pip install supabase selenium beautifulsoup4 requests lxml

# Criar motor_turbo.py correto
echo ""
echo "3. Criando motor_turbo.py..."
cat > ~/Aluguel_imoveis_Dev/motor_turbo.py << 'EOF'
#!/usr/bin/env python3
"""
Motor Turbo - Loop Infinito de Scraping de Imóveis
Executa continuamente, verificando demandas pendentes e realizando scraping
"""

import sys
import time
import random
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "motor_busca"))

from motor_busca.config import SUPABASE_URL, SUPABASE_SERVICE_KEY
from motor_busca.db import get_supabase_client
from motor_busca.geocoder import geocode_address
from motor_busca.scraper_sapo import scrape_sapo
from motor_busca.motor import upsert_imoveis_supabase

def processar_demandas_pendentes():
    """Processa todas as demandas pendentes na tabela"""
    try:
        supabase = get_supabase_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

        response = supabase.table('demandas').select('*').eq('status', 'pendente').execute()
        demandas = response.data

        if not demandas:
            print("Nenhuma demanda pendente no momento.")
            return 0

        print(f"\n{'='*60}")
        print(f"Encontradas {len(demandas)} demandas pendentes")
        print(f"{'='*60}\n")

        processadas = 0
        for demanda in demandas:
            demanda_id = demanda['id']
            termo_busca = demanda['termo_busca']
            lat = demanda['lat']
            lng = demanda['lng']
            raio_metros = demanda['raio_metros']

            print(f"Processando: {termo_busca} (raio: {raio_metros}m)")

            supabase.table('demandas').update({
                'status': 'processando'
            }).eq('id', demanda_id).execute()

            try:
                print(f"  Fazendo scraping no SAPO...")
                imoveis = scrape_sapo(termo_busca, raio_metros)
                print(f"  Encontrados {len(imoveis)} imóveis no SAPO")

                if imoveis:
                    print(f"  Geocodificando e calculando distâncias...")
                    for imovel in imoveis:
                        if not imovel.get('lat') or not imovel.get('lon'):
                            endereco = f"{imovel.get('endereco', '')}, {imovel.get('cidade', '')}, Portugal"
                            coords = geocode_address(endereco)
                            if coords:
                                imovel['lat'] = coords[0]
                                imovel['lon'] = coords[1]

                        if imovel.get('lat') and imovel.get('lon'):
                            from math import radians, sin, cos, sqrt, atan2
                            R = 6371000
                            lat1, lon1 = radians(lat), radians(lng)
                            lat2, lon2 = radians(imovel['lat']), radians(imovel['lon'])
                            dlat = lat2 - lat1
                            dlon = lon2 - lon1
                            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
                            c = 2 * atan2(sqrt(a), sqrt(1-a))
                            imovel['dist_metros'] = int(R * c)

                    print(f"  Salvando imóveis no banco de dados...")
                    upsert_imoveis_supabase(supabase, imoveis)
                    print(f"  Imóveis salvos com sucesso!")

                supabase.table('demandas').update({
                    'status': 'concluido',
                    'num_resultados': len(imoveis)
                }).eq('id', demanda_id).execute()

                print(f"  Demanda concluída com sucesso!\n")
                processadas += 1

                time.sleep(random.uniform(2, 5))

            except Exception as e:
                print(f"  Erro ao processar demanda: {e}")
                supabase.table('demandas').update({
                    'status': 'erro'
                }).eq('id', demanda_id).execute()
                continue

        return processadas

    except Exception as e:
        print(f"Erro geral ao processar demandas: {e}")
        return 0

def main():
    """Loop principal do motor turbo"""
    print("\n" + "="*60)
    print("  MOTOR TURBO - SISTEMA DE SCRAPING CONTÍNUO")
    print("="*60)
    print("\nIniciando motor em modo loop infinito...")
    print("Pressione Ctrl+C para parar\n")

    ciclo = 0

    try:
        while True:
            ciclo += 1
            print(f"\n{'='*60}")
            print(f"CICLO #{ciclo} - {time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"{'='*60}")

            processadas = processar_demandas_pendentes()

            if processadas > 0:
                print(f"\nCiclo concluído: {processadas} demandas processadas")

            intervalo = random.randint(300, 600)
            print(f"\nAguardando {intervalo//60} minutos e {intervalo%60} segundos até o próximo ciclo...")
            print(f"{'='*60}\n")

            time.sleep(intervalo)

    except KeyboardInterrupt:
        print("\n\nMotor turbo interrompido pelo usuário.")
        print(f"Total de ciclos executados: {ciclo}")
        print("Até logo!\n")
        sys.exit(0)
    except Exception as e:
        print(f"\nErro fatal no motor turbo: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
EOF

chmod +x ~/Aluguel_imoveis_Dev/motor_turbo.py

# Testar instalação
echo ""
echo "4. Testando instalação..."
python3 -c "from supabase import create_client; print('✓ Supabase OK')"
python3 -c "from selenium import webdriver; print('✓ Selenium OK')"
python3 -c "from bs4 import BeautifulSoup; print('✓ BeautifulSoup OK')"

echo ""
echo "============================================"
echo "  INSTALAÇÃO CONCLUÍDA!"
echo "============================================"
echo ""
echo "Para rodar o motor:"
echo "  python3 motor_turbo.py"
echo ""
