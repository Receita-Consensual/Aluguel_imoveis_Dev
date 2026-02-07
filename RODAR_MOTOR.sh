#!/bin/bash

echo "════════════════════════════════════════════════════════"
echo "🤖 INICIANDO MOTOR INFINITO"
echo "════════════════════════════════════════════════════════"
echo ""

# Instalar dependências
echo "📦 Instalando dependências..."
pip install -r motor_busca/requirements.txt

echo ""
echo "✅ Dependências instaladas!"
echo ""
echo "🚀 Iniciando motor em background..."
echo ""

# Rodar motor em background
nohup python3 motor_infinito.py > motor.log 2>&1 &

echo "✅ Motor rodando!"
echo ""
echo "📊 Para ver logs em tempo real:"
echo "   tail -f motor.log"
echo ""
echo "🛑 Para parar o motor:"
echo "   pkill -f motor_infinito.py"
echo ""
echo "════════════════════════════════════════════════════════"
