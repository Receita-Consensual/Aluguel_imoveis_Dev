# 🚀 Como Colocar o Motor para Rodar no Servidor Linux

## 📋 O Que Você Vai Fazer

1. Conectar no servidor via AnyDesk
2. Instalar Python e dependências
3. Copiar o código do motor
4. Configurar variáveis de ambiente
5. Testar o motor
6. Deixar rodando automaticamente

---

## 🔌 PASSO 1: Conectar no Servidor

1. Abrir AnyDesk
2. Conectar no servidor Linux
3. Abrir o Terminal

---

## 🐍 PASSO 2: Instalar Python e Dependências

```bash
# Atualizar sistema
sudo apt update
sudo apt upgrade -y

# Instalar Python 3 e pip
sudo apt install python3 python3-pip python3-venv -y

# Verificar instalação
python3 --version  # Deve mostrar Python 3.x
pip3 --version     # Deve mostrar pip
```

---

## 📁 PASSO 3: Criar Pasta e Copiar Código

### Opção A: Via Git (RECOMENDADO)

```bash
# Ir para home
cd ~

# Clonar repositório
git clone https://github.com/SEU_USUARIO/SEU_REPO.git lugar-motor
cd lugar-motor

# Ou se já tiver o repo:
cd lugar-motor
git pull origin main
```

### Opção B: Copiar Arquivos Manualmente

```bash
# Criar pasta
mkdir -p ~/lugar-motor
cd ~/lugar-motor

# Copiar arquivos via SFTP/SCP
# Você pode usar FileZilla ou WinSCP para isso
# Copie toda a pasta motor_busca/
```

---

## 🔐 PASSO 4: Configurar Variáveis de Ambiente

```bash
# Criar arquivo .env na pasta do motor
cd ~/lugar-motor
nano .env
```

Cole isto no arquivo (com SUAS keys reais):

```bash
# Supabase
SUPABASE_URL=https://zprocqmlefzjrepxtxko.supabase.co
SUPABASE_SERVICE_KEY=sua_service_key_aqui

# Google Geocoding
GOOGLE_GEOCODING_KEY=AIzaSyCws8dm1mPhPKdu4VUk7BTBEe25qGZDrb4
```

**Salvar:** `CTRL + O`, `ENTER`, `CTRL + X`

---

## 📦 PASSO 5: Instalar Dependências Python

```bash
cd ~/lugar-motor

# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências
pip install -r motor_busca/requirements.txt

# Se der erro, instalar manualmente:
pip install selenium beautifulsoup4 python-dotenv requests supabase geopy
```

---

## 🧪 PASSO 6: Testar o Motor

```bash
# Garantir que está na pasta certa
cd ~/lugar-motor

# Ativar ambiente virtual (se não estiver ativo)
source venv/bin/activate

# Rodar o motor manualmente (modo teste)
python3 motor_busca/motor.py
```

**O que deve acontecer:**
- ✅ Deve buscar demandas pendentes
- ✅ Scraping do Sapo e Idealista
- ✅ Salvar imóveis no banco
- ✅ Atualizar status das demandas

**Se der erro:**
```bash
# Verificar se tem ChromeDriver
# O Selenium precisa do ChromeDriver instalado

# Instalar Chrome/Chromium
sudo apt install chromium-browser chromium-chromedriver -y

# Ou baixar ChromeDriver manualmente:
wget https://chromedriver.storage.googleapis.com/LATEST_RELEASE
VERSION=$(cat LATEST_RELEASE)
wget https://chromedriver.storage.googleapis.com/$VERSION/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver
```

---

## 🔄 PASSO 7: Deixar Rodando Automaticamente

### Opção A: Cron (Simples - Rodar a cada hora)

```bash
# Editar crontab
crontab -e

# Adicionar esta linha no final:
0 * * * * cd /home/SEU_USUARIO/lugar-motor && /home/SEU_USUARIO/lugar-motor/venv/bin/python3 motor_busca/motor.py >> /home/SEU_USUARIO/motor.log 2>&1
```

**Explicação:**
- `0 * * * *` = Roda todo dia, toda hora (no minuto 0)
- `>> motor.log` = Salva logs em arquivo

**Para rodar a cada 30 minutos:**
```bash
*/30 * * * * cd /home/SEU_USUARIO/lugar-motor && /home/SEU_USUARIO/lugar-motor/venv/bin/python3 motor_busca/motor.py >> /home/SEU_USUARIO/motor.log 2>&1
```

### Opção B: Systemd (Profissional - Sempre rodando)

```bash
# Criar serviço
sudo nano /etc/systemd/system/lugar-motor.service
```

Cole isto:

```ini
[Unit]
Description=Motor de Busca Lugar
After=network.target

[Service]
Type=simple
User=SEU_USUARIO
WorkingDirectory=/home/SEU_USUARIO/lugar-motor
Environment="PATH=/home/SEU_USUARIO/lugar-motor/venv/bin"
ExecStart=/home/SEU_USUARIO/lugar-motor/venv/bin/python3 /home/SEU_USUARIO/lugar-motor/motor_busca/motor.py
Restart=always
RestartSec=3600

[Install]
WantedBy=multi-user.target
```

**IMPORTANTE:** Trocar `SEU_USUARIO` pelo seu usuário real!

```bash
# Recarregar systemd
sudo systemctl daemon-reload

# Ativar serviço
sudo systemctl enable lugar-motor

# Iniciar serviço
sudo systemctl start lugar-motor

# Ver status
sudo systemctl status lugar-motor

# Ver logs
sudo journalctl -u lugar-motor -f
```

---

## 📊 PASSO 8: Monitorar o Motor

### Ver logs em tempo real:

```bash
# Se usar cron:
tail -f ~/motor.log

# Se usar systemd:
sudo journalctl -u lugar-motor -f
```

### Verificar se está funcionando:

```bash
# Ver processos Python rodando
ps aux | grep motor.py

# Ver última execução
ls -lh ~/motor.log
```

### Verificar banco de dados:

No Supabase Dashboard:
1. Ir em Table Editor
2. Abrir tabela `imoveis`
3. Verificar se novos imóveis foram adicionados
4. Checar timestamps em `criado_em`

---

## 🛠️ COMANDOS ÚTEIS

```bash
# Parar motor (se systemd)
sudo systemctl stop lugar-motor

# Reiniciar motor
sudo systemctl restart lugar-motor

# Ver logs das últimas 100 linhas
sudo journalctl -u lugar-motor -n 100

# Atualizar código do GitHub
cd ~/lugar-motor
git pull origin main
sudo systemctl restart lugar-motor

# Desativar cron
crontab -e  # Comentar linha com #

# Remover serviço systemd
sudo systemctl stop lugar-motor
sudo systemctl disable lugar-motor
sudo rm /etc/systemd/system/lugar-motor.service
```

---

## 🚨 TROUBLESHOOTING

### Erro: "No module named 'selenium'"

```bash
cd ~/lugar-motor
source venv/bin/activate
pip install selenium beautifulsoup4 python-dotenv requests supabase geopy
```

### Erro: "ChromeDriver not found"

```bash
sudo apt install chromium-browser chromium-chromedriver -y
```

### Erro: "Permission denied"

```bash
chmod +x motor_busca/motor.py
```

### Motor não está salvando no banco:

```bash
# Verificar variáveis de ambiente
cat .env

# Testar conexão Supabase
python3 -c "
from motor_busca.config import SUPABASE_URL, SUPABASE_SERVICE_KEY
print('URL:', SUPABASE_URL)
print('Key:', SUPABASE_SERVICE_KEY[:20] + '...')
"
```

### Erro 403 (Sites bloqueando):

Os sites podem bloquear IPs de servidores. Soluções:

```bash
# 1. Adicionar delays no scraper (já tem)
# 2. Rodar menos vezes (a cada 2-3 horas)
# 3. Usar proxies/VPN no servidor
```

---

## 📈 OTIMIZAÇÕES

### Rodar apenas em horários específicos:

```bash
# Cron: Segunda a Sexta, 9h às 18h, a cada hora
0 9-18 * * 1-5 cd /home/SEU_USUARIO/lugar-motor && ...

# Cron: Apenas à meia-noite
0 0 * * * cd /home/SEU_USUARIO/lugar-motor && ...
```

### Limitar recursos (CPU/RAM):

```bash
# No systemd, adicionar em [Service]:
CPUQuota=50%
MemoryLimit=512M
```

### Notificações por email quando der erro:

```bash
# Instalar mailutils
sudo apt install mailutils -y

# No cron, adicionar:
MAILTO=seu@email.com
```

---

## ✅ CHECKLIST FINAL

Antes de deixar rodando 24/7:

- [ ] Python 3 instalado
- [ ] Dependências instaladas (pip)
- [ ] ChromeDriver instalado
- [ ] Arquivo .env configurado
- [ ] Motor testado manualmente (funciona)
- [ ] Cron ou Systemd configurado
- [ ] Logs sendo gerados
- [ ] Verificado no Supabase (dados chegando)
- [ ] Monitoramento configurado

---

## 🎯 RECOMENDAÇÃO

Para um servidor de produção, use **Systemd** (Opção B).
Para testes ou servidor pessoal, use **Cron** (Opção A).

**Frequência ideal:**
- Desenvolvimento: A cada 2-3 horas
- Produção: A cada 1 hora
- Alta demanda: A cada 30 minutos

**IMPORTANTE:** Não rode muito frequente ou os sites vão bloquear seu IP!

---

## 📞 SUPORTE

Se algo der errado:

1. Verificar logs: `tail -f ~/motor.log`
2. Testar manualmente: `python3 motor_busca/motor.py`
3. Verificar variáveis: `cat .env`
4. Verificar processo: `ps aux | grep motor`

---

**Última atualização:** 2026-02-07
**Testado em:** Ubuntu 20.04, 22.04, Debian 11
