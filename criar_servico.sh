#!/bin/bash

# Script para criar serviço systemd do Motor
# Execute: bash criar_servico.sh

set -e

# Cores
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
echo "╔═══════════════════════════════════════════════╗"
echo "║   🔧 Configurador de Serviço Systemd         ║"
echo "╚═══════════════════════════════════════════════╝"
echo -e "${NC}"

# Detectar usuário e diretório
CURRENT_USER=$(whoami)
INSTALL_DIR="$HOME/lugar-motor"

# Verificar se a instalação existe
if [ ! -d "$INSTALL_DIR/motor_busca" ]; then
    echo -e "${RED}❌ Motor não encontrado em $INSTALL_DIR${NC}"
    echo "Execute primeiro: bash instalar_servidor.sh"
    exit 1
fi

# Verificar se venv existe
if [ ! -d "$INSTALL_DIR/venv" ]; then
    echo -e "${RED}❌ Ambiente virtual não encontrado${NC}"
    echo "Execute primeiro: bash instalar_servidor.sh"
    exit 1
fi

echo -e "${BLUE}[1/4]${NC} Configurando serviço..."
echo "   Usuário: $CURRENT_USER"
echo "   Diretório: $INSTALL_DIR"
echo ""

# Perguntar intervalo
echo "Com que frequência deseja rodar o motor?"
echo "1) A cada 1 hora (recomendado)"
echo "2) A cada 2 horas"
echo "3) A cada 3 horas"
echo "4) A cada 6 horas"
echo "5) Uma vez por dia (meia-noite)"
read -p "Opção (1-5): " -n 1 -r FREQ_OPTION
echo ""

case $FREQ_OPTION in
    1) RESTART_SEC=3600; FREQ_DESC="1 hora" ;;
    2) RESTART_SEC=7200; FREQ_DESC="2 horas" ;;
    3) RESTART_SEC=10800; FREQ_DESC="3 horas" ;;
    4) RESTART_SEC=21600; FREQ_DESC="6 horas" ;;
    5) RESTART_SEC=86400; FREQ_DESC="24 horas" ;;
    *) echo -e "${RED}❌ Opção inválida!${NC}"; exit 1 ;;
esac

echo -e "${GREEN}✅ Frequência: $FREQ_DESC${NC}"

# Criar arquivo de serviço
SERVICE_FILE="/tmp/lugar-motor.service"

cat > $SERVICE_FILE << EOF
[Unit]
Description=Motor de Busca de Imóveis Lugar
After=network.target

[Service]
Type=oneshot
User=$CURRENT_USER
WorkingDirectory=$INSTALL_DIR
Environment="PATH=$INSTALL_DIR/venv/bin:/usr/local/bin:/usr/bin:/bin"
ExecStart=$INSTALL_DIR/venv/bin/python3 $INSTALL_DIR/motor_busca/motor.py
StandardOutput=append:$HOME/motor.log
StandardError=append:$HOME/motor-error.log

[Install]
WantedBy=multi-user.target
EOF

# Criar timer
TIMER_FILE="/tmp/lugar-motor.timer"

cat > $TIMER_FILE << EOF
[Unit]
Description=Timer para Motor de Busca Lugar
Requires=lugar-motor.service

[Timer]
OnBootSec=5min
OnUnitActiveSec=$RESTART_SEC

[Install]
WantedBy=timers.target
EOF

echo -e "${BLUE}[2/4]${NC} Instalando serviço no systemd..."
sudo cp $SERVICE_FILE /etc/systemd/system/
sudo cp $TIMER_FILE /etc/systemd/system/
sudo systemctl daemon-reload
echo -e "${GREEN}✅ Arquivos instalados${NC}"

echo -e "${BLUE}[3/4]${NC} Ativando serviço..."
sudo systemctl enable lugar-motor.timer
echo -e "${GREEN}✅ Serviço ativado${NC}"

echo -e "${BLUE}[4/4]${NC} Iniciando timer..."
sudo systemctl start lugar-motor.timer
echo -e "${GREEN}✅ Timer iniciado${NC}"

# Executar primeira vez agora
echo ""
read -p "Deseja executar o motor agora (primeira vez)? (S/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    echo -e "${YELLOW}⚠️  Executando motor...${NC}"
    sudo systemctl start lugar-motor.service
    sleep 2
fi

# Mostrar status
echo ""
echo -e "${GREEN}╔═══════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║        ✅ SERVIÇO CONFIGURADO COM SUCESSO!    ║${NC}"
echo -e "${GREEN}╚═══════════════════════════════════════════════╝${NC}"
echo ""
echo "📊 STATUS DO SERVIÇO:"
sudo systemctl status lugar-motor.timer --no-pager -l
echo ""
echo "🔍 COMANDOS ÚTEIS:"
echo ""
echo "Ver status do timer:"
echo "  sudo systemctl status lugar-motor.timer"
echo ""
echo "Ver logs do motor:"
echo "  tail -f $HOME/motor.log"
echo ""
echo "Ver erros:"
echo "  tail -f $HOME/motor-error.log"
echo ""
echo "Parar motor:"
echo "  sudo systemctl stop lugar-motor.timer"
echo ""
echo "Reiniciar motor:"
echo "  sudo systemctl restart lugar-motor.timer"
echo ""
echo "Executar agora (força execução):"
echo "  sudo systemctl start lugar-motor.service"
echo ""
echo "Ver próxima execução:"
echo "  systemctl list-timers | grep lugar"
echo ""
echo "Desabilitar motor:"
echo "  sudo systemctl stop lugar-motor.timer"
echo "  sudo systemctl disable lugar-motor.timer"
echo ""
echo -e "⏰ Próxima execução: ${GREEN}daqui $FREQ_DESC${NC}"
echo ""
