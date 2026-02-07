#!/bin/bash

echo "=========================================="
echo "  LUGAR PORTUGAL - INICIALIZAÇÃO RÁPIDA"
echo "=========================================="
echo ""

echo "1. Ativando ambiente virtual Python..."
source venv/bin/activate || python3 -m venv venv && source venv/bin/activate

echo "2. Instalando dependências Python..."
pip install -q -r motor_busca/requirements.txt

echo "3. Iniciando Motor Turbo em background..."
nohup python3 motor_turbo.py > motor_turbo.log 2>&1 &
MOTOR_PID=$!
echo "   Motor Turbo iniciado com PID: $MOTOR_PID"

echo "4. Servindo aplicação web na porta 8080..."
cd dist
echo ""
echo "=========================================="
echo "  TUDO PRONTO!"
echo "=========================================="
echo ""
echo "Aplicação rodando em: http://localhost:8080"
echo "Motor Turbo PID: $MOTOR_PID"
echo ""
echo "Comandos úteis:"
echo "  - Ver logs do motor: tail -f ../motor_turbo.log"
echo "  - Parar motor: kill $MOTOR_PID"
echo "  - Parar servidor: Ctrl+C"
echo ""
echo "Pressione Ctrl+C para parar o servidor web"
echo ""

python3 -m http.server 8080
