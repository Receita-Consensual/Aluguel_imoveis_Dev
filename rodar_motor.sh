#!/bin/bash

echo "========================================"
echo "INICIANDO MOTOR DE BUSCA"
echo "========================================"

# Ativar ambiente virtual
source venv/bin/activate

# Verificar se .env existe
if [ ! -f .env ]; then
    echo "ERRO: Arquivo .env não encontrado!"
    echo "Crie o arquivo .env com suas credenciais do Supabase"
    exit 1
fi

# Rodar motor
echo "Iniciando motor_turbo.py..."
python3 motor_turbo.py
