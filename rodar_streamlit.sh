#!/bin/bash

echo "=========================================="
echo "🚀 LUGAR - Iniciando aplicação Streamlit"
echo "=========================================="
echo ""

# Verificar se o .env existe
if [ ! -f ".env" ]; then
    echo "❌ Arquivo .env não encontrado!"
    echo "   Crie um arquivo .env com as credenciais do Supabase"
    exit 1
fi

echo "✓ Arquivo .env encontrado"

# Verificar se o secrets.toml existe
if [ ! -f ".streamlit/secrets.toml" ]; then
    echo "⚠️ Arquivo .streamlit/secrets.toml não encontrado"
    echo "   Criando automaticamente a partir do .env..."

    # Ler variáveis do .env
    source .env

    # Criar secrets.toml
    cat > .streamlit/secrets.toml << EOF
# Configuração do Streamlit
SUPABASE_URL = "$SUPABASE_URL"
SUPABASE_ANON_KEY = "$SUPABASE_ANON_KEY"
GOOGLE_API_KEY = "$GOOGLE_API_KEY"
EOF
    echo "✓ Arquivo secrets.toml criado"
fi

echo ""
echo "=========================================="
echo "📦 Instalando dependências..."
echo "=========================================="

# Instalar dependências
pip3 install -q -r requirements.txt 2>/dev/null || pip install -q -r requirements.txt

echo "✓ Dependências instaladas"
echo ""
echo "=========================================="
echo "🌐 Iniciando Streamlit..."
echo "=========================================="
echo ""
echo "📱 A aplicação abrirá em: http://localhost:8501"
echo "⏹️  Para parar: Ctrl+C"
echo ""

# Rodar Streamlit
streamlit run app.py
