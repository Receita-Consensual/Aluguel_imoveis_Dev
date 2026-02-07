#!/bin/bash

echo "=========================================="
echo "INSTALAÇÃO COMPLETA - MOTOR DE BUSCA"
echo "=========================================="
echo ""

# Ativar ambiente virtual
echo "1. Ativando ambiente virtual..."
source venv/bin/activate

# Criar arquivo .env
echo "2. Criando arquivo .env..."
cat > .env << 'ENVFILE'
VITE_SUPABASE_URL=https://zprocqmlefzjrepxtxko.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inpwcm9jcW1sZWZ6anJlcHh0eGtvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3Mzg5MDQ2MzksImV4cCI6MjA1NDQ4MDYzOX0.d8-tZf69tPDxYpQOIrJdX6_UG3v6AjEJ-o0ujO9Xv1U
VITE_GOOGLE_MAPS_API_KEY=AIzaSyCws8dm1mPhPKdu4VUk7BTBEe25qGZDrb4

SUPABASE_URL=https://zprocqmlefzjrepxtxko.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Inpwcm9jcW1sZWZ6anJlcHh0eGtvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTczODkwNDYzOSwiZXhwIjoyMDU0NDgwNjM5fQ.lkauygqUoMuZUsWd-S3H-qb4XGKWnOdz9i5lYHO9sZs
GOOGLE_GEOCODING_KEY=AIzaSyCws8dm1mPhPKdu4VUk7BTBEe25qGZDrb4
ENVFILE

echo "✓ Arquivo .env criado"

# Instalar pacotes Python
echo ""
echo "3. Instalando pacotes Python..."
pip install --quiet supabase
pip install --quiet selenium
pip install --quiet beautifulsoup4
pip install --quiet requests
pip install --quiet lxml
pip install --quiet python-dotenv

echo "✓ Pacotes instalados"

# Testar instalação
echo ""
echo "4. Testando instalação..."
python3 -c "import supabase; print('✓ supabase')"
python3 -c "from selenium import webdriver; print('✓ selenium')"
python3 -c "from bs4 import BeautifulSoup; print('✓ beautifulsoup4')"
python3 -c "import requests; print('✓ requests')"
python3 -c "import os; from dotenv import load_dotenv; load_dotenv(); print('✓ python-dotenv')"

echo ""
echo "=========================================="
echo "✓ INSTALAÇÃO CONCLUÍDA COM SUCESSO!"
echo "=========================================="
echo ""
echo "Próximos passos:"
echo ""
echo "1. Testar conexão:"
echo "   python3 teste_conexao.py"
echo ""
echo "2. Iniciar motor:"
echo "   nohup python3 motor_turbo.py > motor.log 2>&1 &"
echo ""
echo "3. Ver progresso:"
echo "   tail -f motor.log"
echo ""
