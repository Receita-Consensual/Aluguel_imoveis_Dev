# Instruções para Rodar no Servidor Linux

## Aplicação Completa: Lugar Portugal

Sistema de busca de imóveis com Google Maps + Motor de Scraping Infinito

---

## 1. Pré-requisitos no Servidor

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python 3 e pip
sudo apt install python3 python3-pip python3-venv -y

# Instalar Node.js e npm (se necessário para servir a aplicação)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
```

---

## 2. Transferir Arquivos para o Servidor

```bash
# No seu computador local, compactar o projeto
tar -czf lugar-portugal.tar.gz motor_busca/ motor_turbo.py dist/ .env

# Enviar para o servidor via scp
scp lugar-portugal.tar.gz usuario@seu-servidor.com:/home/usuario/

# No servidor, descompactar
cd /home/usuario/
tar -xzf lugar-portugal.tar.gz
```

---

## 3. Configurar o Motor de Scraping (Python)

```bash
# Criar ambiente virtual
cd /home/usuario/
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências
pip install -r motor_busca/requirements.txt
```

---

## 4. Configurar Variáveis de Ambiente

Edite o arquivo `.env` com suas credenciais:

```bash
nano .env
```

Conteúdo necessário:
```
VITE_SUPABASE_URL=sua-url-do-supabase
VITE_SUPABASE_ANON_KEY=sua-chave-anonima
VITE_GOOGLE_MAPS_API_KEY=sua-chave-do-google-maps
SUPABASE_SERVICE_KEY=sua-chave-de-servico
```

---

## 5. Rodar o Motor Turbo em Background

### Opção A: Usando nohup (simples)

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Rodar em background
nohup python3 motor_turbo.py > motor_turbo.log 2>&1 &

# Ver o processo rodando
ps aux | grep motor_turbo

# Ver os logs em tempo real
tail -f motor_turbo.log
```

### Opção B: Usando systemd (recomendado para produção)

```bash
# Criar serviço systemd
sudo nano /etc/systemd/system/motor-turbo.service
```

Conteúdo do serviço:
```ini
[Unit]
Description=Motor Turbo - Scraping Infinito de Imóveis
After=network.target

[Service]
Type=simple
User=usuario
WorkingDirectory=/home/usuario
Environment="PATH=/home/usuario/venv/bin"
ExecStart=/home/usuario/venv/bin/python3 /home/usuario/motor_turbo.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Recarregar systemd
sudo systemctl daemon-reload

# Iniciar o serviço
sudo systemctl start motor-turbo

# Habilitar para iniciar automaticamente no boot
sudo systemctl enable motor-turbo

# Ver status
sudo systemctl status motor-turbo

# Ver logs
sudo journalctl -u motor-turbo -f
```

---

## 6. Servir a Aplicação Web (Frontend)

### Opção A: Usando Python HTTP Server (simples)

```bash
cd /home/usuario/dist
python3 -m http.server 8080
```

### Opção B: Usando Nginx (recomendado para produção)

```bash
# Instalar Nginx
sudo apt install nginx -y

# Copiar arquivos para o diretório do Nginx
sudo cp -r dist/* /var/www/html/

# Configurar Nginx
sudo nano /etc/nginx/sites-available/default
```

Configuração básica:
```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    root /var/www/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }
}
```

```bash
# Reiniciar Nginx
sudo systemctl restart nginx

# Habilitar no boot
sudo systemctl enable nginx
```

---

## 7. Comandos Úteis

### Parar o Motor Turbo

```bash
# Se usando nohup
ps aux | grep motor_turbo
kill [PID]

# Se usando systemd
sudo systemctl stop motor-turbo
```

### Ver Logs do Motor

```bash
# Se usando nohup
tail -f motor_turbo.log

# Se usando systemd
sudo journalctl -u motor-turbo -f
```

### Verificar Status

```bash
# Motor turbo
sudo systemctl status motor-turbo

# Nginx
sudo systemctl status nginx

# Ver processos Python
ps aux | grep python
```

---

## 8. Testar a Aplicação

1. Abra o navegador e acesse: `http://seu-servidor.com`
2. Faça uma busca por um local em Portugal
3. O sistema irá:
   - Criar uma demanda no banco de dados
   - O motor turbo irá processar a demanda
   - Resultados aparecerão no mapa automaticamente

---

## 9. Monitoramento

### Ver quantas demandas estão sendo processadas

```bash
# Conectar ao Supabase via psql ou dashboard web
# Executar:
SELECT status, COUNT(*) FROM demandas GROUP BY status;
```

### Ver últimos imóveis adicionados

```bash
SELECT COUNT(*), fonte FROM imoveis GROUP BY fonte;
```

---

## 10. Backup e Manutenção

```bash
# Fazer backup do banco de dados (via Supabase Dashboard)
# Ou via SQL:
pg_dump -h [host] -U [user] -d [database] > backup.sql

# Limpar logs antigos
truncate -s 0 motor_turbo.log

# Atualizar código
git pull origin main  # se estiver usando git
sudo systemctl restart motor-turbo
```

---

## Pronto!

Sua aplicação está rodando:
- Frontend: `http://seu-servidor.com`
- Motor de scraping: Rodando em background processando demandas a cada 5-10 minutos
- Modal do fundador: Aparece automaticamente após 30 segundos de navegação

**Divirta-se e descanse!**
