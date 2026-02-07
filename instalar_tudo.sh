#!/bin/bash

echo "========================================"
echo "INSTALAÇÃO COMPLETA - ALUGUEL IMÓVEIS"
echo "========================================"
echo ""

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 1. Atualizar sistema
echo -e "${YELLOW}[1/6] Atualizando sistema...${NC}"
sudo apt update

# 2. Instalar Python e dependências do sistema
echo -e "${YELLOW}[2/6] Instalando Python e dependências...${NC}"
sudo apt install -y python3 python3-pip python3-venv python3-dev build-essential

# 3. Criar ambiente virtual
echo -e "${YELLOW}[3/6] Criando ambiente virtual...${NC}"
if [ -d "venv" ]; then
    echo "Removendo ambiente virtual antigo..."
    rm -rf venv
fi
python3 -m venv venv

# 4. Ativar ambiente virtual
echo -e "${YELLOW}[4/6] Ativando ambiente virtual...${NC}"
source venv/bin/activate

# 5. Instalar dependências Python
echo -e "${YELLOW}[5/6] Instalando dependências Python...${NC}"
pip install --upgrade pip
pip install -r motor_busca/requirements.txt
pip install -r requirements.txt

# 6. Verificar instalação
echo -e "${YELLOW}[6/6] Verificando instalação...${NC}"
python3 -c "import dotenv; import supabase; import selenium; import bs4; print('Todas as bibliotecas instaladas com sucesso!')"

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}========================================"
    echo -e "INSTALAÇÃO CONCLUÍDA COM SUCESSO!"
    echo -e "========================================${NC}"
    echo ""
    echo -e "${YELLOW}PRÓXIMOS PASSOS:${NC}"
    echo "1. Configure o arquivo .env com suas credenciais"
    echo "2. Ative o ambiente virtual: source venv/bin/activate"
    echo "3. Teste o motor: python3 motor_turbo.py"
    echo ""
else
    echo -e "${RED}Erro na instalação. Verifique as mensagens acima.${NC}"
    exit 1
fi
