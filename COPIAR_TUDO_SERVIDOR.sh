#!/bin/bash
# Script para copiar todos os arquivos necessários para o servidor

echo "📦 Copiando arquivos para o servidor..."

# Criar estrutura de diretórios
mkdir -p ~/Aluguel_imoveis_Dev/motor_busca

# Criar teste_rapido.py
cat > ~/Aluguel_imoveis_Dev/teste_rapido.py << 'EOF'
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
EOF

# Criar motor_busca/config.py
cat > ~/Aluguel_imoveis_Dev/motor_busca/config.py << 'EOF'
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_KEY = os.getenv('SUPABASE_SERVICE_KEY')
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')
EOF

# Criar motor_busca/db.py
cat > ~/Aluguel_imoveis_Dev/motor_busca/db.py << 'EOF'
from supabase import create_client, Client

def get_supabase_client(url: str, key: str) -> Client:
    return create_client(url, key)
EOF

# Criar motor_busca/geocoder.py
cat > ~/Aluguel_imoveis_Dev/motor_busca/geocoder.py << 'EOF'
import requests
from typing import Optional, Tuple
from .config import GOOGLE_MAPS_API_KEY

def get_coordinates(address: str) -> Optional[Tuple[float, float]]:
    """Obtém coordenadas geográficas de um endereço usando Google Maps API"""
    if not GOOGLE_MAPS_API_KEY:
        return None

    url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        'address': address,
        'key': GOOGLE_MAPS_API_KEY
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data['status'] == 'OK' and data['results']:
            location = data['results'][0]['geometry']['location']
            return (location['lat'], location['lng'])
    except Exception as e:
        print(f"Erro ao geocodificar {address}: {e}")

    return None
EOF

# Criar motor_busca/scraper_sapo.py
cat > ~/Aluguel_imoveis_Dev/motor_busca/scraper_sapo.py << 'EOF'
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import time

def scrape_sapo(cidade: str, num_quartos: Optional[int] = None, preco_max: Optional[float] = None) -> List[Dict]:
    """Scraper básico para Sapo.pt"""
    imoveis = []

    try:
        # URL base do Sapo
        url = f"https://casa.sapo.pt/Alugar/Apartamentos/{cidade}/"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Implementar lógica de scraping aqui
        print(f"Scraping Sapo.pt para {cidade}...")

    except Exception as e:
        print(f"Erro ao scraper Sapo: {e}")

    return imoveis
EOF

# Criar motor_busca/scraper_idealista.py
cat > ~/Aluguel_imoveis_Dev/motor_busca/scraper_idealista.py << 'EOF'
import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import time

def scrape_idealista(cidade: str, num_quartos: Optional[int] = None, preco_max: Optional[float] = None) -> List[Dict]:
    """Scraper básico para Idealista.pt"""
    imoveis = []

    try:
        # URL base do Idealista
        url = f"https://www.idealista.pt/arrendar-casas/{cidade.lower()}/"

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Implementar lógica de scraping aqui
        print(f"Scraping Idealista.pt para {cidade}...")

    except Exception as e:
        print(f"Erro ao scraper Idealista: {e}")

    return imoveis
EOF

# Criar motor_busca/motor.py
cat > ~/Aluguel_imoveis_Dev/motor_busca/motor.py << 'EOF'
from typing import List, Dict, Optional
from .scraper_sapo import scrape_sapo
from .scraper_idealista import scrape_idealista
from .geocoder import get_coordinates
from .db import get_supabase_client
from .config import SUPABASE_URL, SUPABASE_SERVICE_KEY

def buscar_imoveis(cidade: str, num_quartos: Optional[int] = None, preco_max: Optional[float] = None) -> List[Dict]:
    """Motor de busca principal que coordena todos os scrapers"""
    print(f"🔍 Iniciando busca em {cidade}...")

    todos_imoveis = []

    # Buscar em todas as fontes
    todos_imoveis.extend(scrape_sapo(cidade, num_quartos, preco_max))
    todos_imoveis.extend(scrape_idealista(cidade, num_quartos, preco_max))

    # Salvar no banco de dados
    if todos_imoveis:
        client = get_supabase_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        for imovel in todos_imoveis:
            try:
                client.table('imoveis').upsert(imovel).execute()
            except Exception as e:
                print(f"Erro ao salvar imóvel: {e}")

    print(f"✓ Encontrados {len(todos_imoveis)} imóveis")
    return todos_imoveis
EOF

# Criar motor_busca/requirements.txt
cat > ~/Aluguel_imoveis_Dev/motor_busca/requirements.txt << 'EOF'
supabase>=2.0.0
requests>=2.31.0
beautifulsoup4>=4.12.0
python-dotenv>=1.0.0
EOF

# Criar __init__.py
touch ~/Aluguel_imoveis_Dev/motor_busca/__init__.py

# Dar permissões de execução
chmod +x ~/Aluguel_imoveis_Dev/teste_rapido.py

echo "✓ Todos os arquivos foram criados!"
echo ""
echo "Próximos passos:"
echo "1. Edite o arquivo .env com suas credenciais"
echo "2. Execute: python3 teste_rapido.py"
