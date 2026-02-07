#!/bin/bash

echo "════════════════════════════════════════════════"
echo "🧪 TESTE RÁPIDO - Verificando se está tudo OK"
echo "════════════════════════════════════════════════"
echo ""

# Verificar se Python está instalado
echo "1️⃣ Verificando Python..."
if command -v python3 &> /dev/null; then
    echo "   ✅ Python instalado: $(python3 --version)"
else
    echo "   ❌ Python NÃO instalado!"
    exit 1
fi

echo ""

# Verificar se pip está instalado
echo "2️⃣ Verificando pip..."
if command -v pip &> /dev/null || command -v pip3 &> /dev/null; then
    echo "   ✅ pip instalado"
else
    echo "   ❌ pip NÃO instalado!"
    exit 1
fi

echo ""

# Verificar se o .env existe
echo "3️⃣ Verificando arquivo .env..."
if [ -f ".env" ]; then
    echo "   ✅ Arquivo .env existe"
else
    echo "   ❌ Arquivo .env NÃO encontrado!"
    exit 1
fi

echo ""

# Verificar se as credenciais estão no .env
echo "4️⃣ Verificando credenciais Supabase..."
if grep -q "SUPABASE_SERVICE_KEY" .env; then
    echo "   ✅ SUPABASE_SERVICE_KEY encontrada"
else
    echo "   ❌ SUPABASE_SERVICE_KEY não encontrada no .env!"
    exit 1
fi

echo ""

# Verificar se motor_infinito.py existe
echo "5️⃣ Verificando motor_infinito.py..."
if [ -f "motor_infinito.py" ]; then
    echo "   ✅ motor_infinito.py existe"
else
    echo "   ❌ motor_infinito.py NÃO encontrado!"
    exit 1
fi

echo ""

# Verificar se app.py existe
echo "6️⃣ Verificando app.py (Streamlit)..."
if [ -f "app.py" ]; then
    echo "   ✅ app.py existe"
else
    echo "   ❌ app.py NÃO encontrado!"
    exit 1
fi

echo ""

# Verificar se as dependências estão instaladas
echo "7️⃣ Verificando dependências Python..."
if python3 -c "import supabase" 2>/dev/null; then
    echo "   ✅ supabase instalado"
else
    echo "   ⚠️  supabase NÃO instalado - Execute: pip install -r motor_busca/requirements.txt"
fi

echo ""
echo "════════════════════════════════════════════════"
echo "✅ VERIFICAÇÃO CONCLUÍDA!"
echo "════════════════════════════════════════════════"
echo ""
echo "📝 Próximos passos:"
echo "   1. Se há ⚠️ ou ❌, corrija os problemas"
echo "   2. Execute: ./RODAR_MOTOR.sh"
echo "   3. Coloque o site no ar: https://share.streamlit.io/"
echo ""
