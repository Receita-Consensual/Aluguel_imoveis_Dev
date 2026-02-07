#!/bin/bash

# Script de Instalação Automática do Motor no Servidor Linux
# Execute: bash instalar_servidor.sh

set -e  # Para na primeira falha

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════╗"
echo "║                                                    ║"
echo "║     🚀 INSTALADOR DO MOTOR DE BUSCA LUGAR         ║"
echo "║                                                    ║"
echo "╚════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Verificar se está rodando como root
if [ "$EUID" -eq 0 ]; then
   echo -e "${RED}❌ NÃO execute este script como root (sudo)!${NC}"
   echo "Execute como usuário normal: bash instalar_servidor.sh"
   exit 1
fi

# 1. Verificar/Instalar Python
echo -e "\n${BLUE}[1/8]${NC} Verificando Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo -e "${GREEN}✅ Python já instalado: $PYTHON_VERSION${NC}"
else
    echo -e "${YELLOW}⚠️  Instalando Python 3...${NC}"
    sudo apt update
    sudo apt install -y python3 python3-pip python3-venv
fi

# 2. Verificar/Instalar ChromeDriver
echo -e "\n${BLUE}[2/8]${NC} Verificando ChromeDriver..."
if command -v chromedriver &> /dev/null; then
    echo -e "${GREEN}✅ ChromeDriver já instalado${NC}"
else
    echo -e "${YELLOW}⚠️  Instalando Chromium e ChromeDriver...${NC}"
    sudo apt install -y chromium-browser chromium-chromedriver
fi

# 3. Criar diretório
echo -e "\n${BLUE}[3/8]${NC} Criando diretório do projeto..."
INSTALL_DIR="$HOME/lugar-motor"
if [ -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}⚠️  Diretório já existe: $INSTALL_DIR${NC}"
    read -p "Deseja sobrescrever? (s/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        echo "Instalação cancelada."
        exit 1
    fi
    rm -rf "$INSTALL_DIR"
fi

mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"
echo -e "${GREEN}✅ Diretório criado: $INSTALL_DIR${NC}"

# 4. Copiar código
echo -e "\n${BLUE}[4/8]${NC} Configurando código..."
echo "Escolha como obter o código:"
echo "1) Git clone (recomendado)"
echo "2) Já copiei manualmente"
read -p "Opção (1 ou 2): " -n 1 -r CODE_OPTION
echo

if [[ $CODE_OPTION == "1" ]]; then
    read -p "URL do repositório Git: " REPO_URL
    if [ -z "$REPO_URL" ]; then
        echo -e "${RED}❌ URL vazia!${NC}"
        exit 1
    fi
    git clone "$REPO_URL" .
    echo -e "${GREEN}✅ Código clonado${NC}"
elif [[ $CODE_OPTION == "2" ]]; then
    echo -e "${YELLOW}⚠️  Certifique-se de ter copiado a pasta motor_busca/${NC}"
    if [ ! -d "motor_busca" ]; then
        echo -e "${RED}❌ Pasta motor_busca/ não encontrada!${NC}"
        echo "Copie os arquivos e execute o script novamente."
        exit 1
    fi
    echo -e "${GREEN}✅ Código encontrado${NC}"
else
    echo -e "${RED}❌ Opção inválida!${NC}"
    exit 1
fi

# 5. Criar ambiente virtual
echo -e "\n${BLUE}[5/8]${NC} Criando ambiente virtual Python..."
python3 -m venv venv
source venv/bin/activate
echo -e "${GREEN}✅ Ambiente virtual criado${NC}"

# 6. Instalar dependências
echo -e "\n${BLUE}[6/8]${NC} Instalando dependências Python..."
if [ -f "motor_busca/requirements.txt" ]; then
    pip install -r motor_busca/requirements.txt
elif [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo -e "${YELLOW}⚠️  requirements.txt não encontrado, instalando manualmente...${NC}"
    pip install selenium beautifulsoup4 python-dotenv requests supabase geopy
fi
echo -e "${GREEN}✅ Dependências instaladas${NC}"

# 7. Configurar .env
echo -e "\n${BLUE}[7/8]${NC} Configurando variáveis de ambiente..."
if [ -f ".env" ]; then
    echo -e "${YELLOW}⚠️  Arquivo .env já existe${NC}"
    read -p "Deseja sobrescrever? (s/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        echo "Mantendo .env existente"
    else
        rm .env
    fi
fi

if [ ! -f ".env" ]; then
    echo ""
    echo "Digite suas credenciais:"
    echo ""

    read -p "SUPABASE_URL: " SUPABASE_URL
    read -p "SUPABASE_SERVICE_KEY: " SUPABASE_SERVICE_KEY
    read -p "GOOGLE_GEOCODING_KEY: " GOOGLE_GEOCODING_KEY

    cat > .env << EOF
# Supabase
SUPABASE_URL=$SUPABASE_URL
SUPABASE_SERVICE_KEY=$SUPABASE_SERVICE_KEY

# Google Geocoding
GOOGLE_GEOCODING_KEY=$GOOGLE_GEOCODING_KEY
EOF

    echo -e "${GREEN}✅ Arquivo .env criado${NC}"
fi

# 8. Testar instalação
echo -e "\n${BLUE}[8/8]${NC} Testando instalação..."
echo "Teste rápido de importação..."
python3 << EOF
try:
    from motor_busca.config import SUPABASE_URL, SUPABASE_SERVICE_KEY, GOOGLE_GEOCODING_KEY
    print("✅ Configuração carregada")
    print(f"   URL: {SUPABASE_URL[:30]}...")
    print(f"   Key: {SUPABASE_SERVICE_KEY[:20]}...")
    print(f"   Google: {GOOGLE_GEOCODING_KEY[:20]}...")
except Exception as e:
    print(f"❌ Erro: {e}")
    exit(1)
EOF

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║                                                    ║${NC}"
echo -e "${GREEN}║          ✅ INSTALAÇÃO CONCLUÍDA COM SUCESSO!      ║${NC}"
echo -e "${GREEN}║                                                    ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════╝${NC}"
echo ""
echo "📍 Instalado em: $INSTALL_DIR"
echo ""
echo "🧪 Para testar manualmente:"
echo "   cd $INSTALL_DIR"
echo "   source venv/bin/activate"
echo "   python3 motor_busca/motor.py"
echo ""
echo "⏰ Para rodar automaticamente (escolha uma opção):"
echo ""
echo "   OPÇÃO A - Cron (a cada hora):"
echo "   crontab -e"
echo "   Adicionar: 0 * * * * cd $INSTALL_DIR && $INSTALL_DIR/venv/bin/python3 motor_busca/motor.py >> $HOME/motor.log 2>&1"
echo ""
echo "   OPÇÃO B - Systemd (sempre rodando):"
echo "   bash $INSTALL_DIR/criar_servico.sh"
echo ""
echo "📚 Documentação completa: INSTALAR_MOTOR_SERVIDOR.md"
echo ""
