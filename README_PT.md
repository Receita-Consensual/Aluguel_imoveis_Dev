# 🏠 Lugar - Plataforma de Busca de Imóveis em Portugal

## 📋 O que é?

O **Lugar** é uma plataforma inteligente que busca imóveis para arrendar em Portugal de forma automatizada. O sistema tem 2 partes:

1. **Site (Streamlit)** - Interface bonita onde os usuários buscam imóveis
2. **Motor Infinito (Python)** - Robô que busca imóveis 24/7 automaticamente

## 🚀 Como colocar no ar?

### Passo 1: Site (Streamlit Cloud)

1. Acesse https://share.streamlit.io/
2. Faça login com GitHub
3. Clique em "New app"
4. Selecione o arquivo `app.py`
5. Clique em "Deploy"

### Passo 2: Motor (Sua máquina)

```bash
# Instalar dependências
pip install -r motor_busca/requirements.txt

# Rodar o motor
./RODAR_MOTOR.sh
```

## 📁 Estrutura do Projeto

```
projeto/
├── app.py                    # Site Streamlit (PRINCIPAL)
├── motor_infinito.py         # Robô que busca imóveis 24/7
├── motor_busca/              # Módulos do motor
│   ├── config.py            # Configurações
│   ├── db.py                # Conexão com Supabase
│   ├── geocoder.py          # Geocodificação de endereços
│   ├── scraper_sapo.py      # Scraper do SAPO
│   └── scraper_idealista.py # Scraper do Idealista
├── .env                      # Credenciais (NÃO COMMITAR)
├── LEIA_AQUI_PRIMEIRO.txt   # Início rápido
├── TUTORIAL_COMPLETO.txt    # Tutorial detalhado
└── TESTE_RAPIDO.sh          # Script de verificação
```

## 🔧 Como funciona?

1. **Usuário busca** no site por "Porto"
2. **Site cria demanda** no banco Supabase
3. **Motor detecta** a demanda
4. **Motor busca** imóveis no SAPO e Idealista
5. **Motor salva** imóveis no Supabase
6. **Site mostra** os imóveis no mapa

## 🛠️ Tecnologias

- **Frontend**: Streamlit + Folium (mapas)
- **Backend**: Python + Supabase (PostgreSQL)
- **Scraping**: BeautifulSoup + httpx
- **Deploy**: Streamlit Cloud + sua máquina (motor)

## 📊 Banco de Dados (Supabase)

Tabelas principais:
- `imoveis` - Armazena os imóveis encontrados
- `demandas` - Armazena buscas dos usuários
- `logs_pesquisas` - Log de buscas
- `logs_cliques` - Log de cliques
- `alertas_clientes` - Emails de membros fundadores

## 🐛 Solução de Problemas

### Motor não roda
```bash
# Verifique se as dependências estão instaladas
pip install -r motor_busca/requirements.txt

# Verifique se o .env existe
ls -la .env

# Rode o teste
./TESTE_RAPIDO.sh
```

### Site não carrega
- Aguarde 2-3 minutos após deploy
- Recarregue a página
- Verifique os logs no Streamlit Cloud

### Sem imóveis no mapa
- Faça uma busca no site (ex: "Porto")
- Aguarde 10-15 minutos
- Recarregue o site

## 📝 Comandos Úteis

```bash
# Ver se o motor está rodando
ps aux | grep motor_infinito

# Ver logs do motor
tail -f motor.log

# Parar o motor
pkill -f motor_infinito.py

# Testar tudo
./TESTE_RAPIDO.sh
```

## 🎯 Próximos Passos

1. ✅ Colocar site no ar (Streamlit)
2. ✅ Rodar motor (sua máquina)
3. ⏳ Aguardar primeiras buscas
4. 🎉 Ver imóveis no mapa!

## 📧 Contato

Dúvidas? Abra uma issue ou leia os arquivos:
- `LEIA_AQUI_PRIMEIRO.txt`
- `TUTORIAL_COMPLETO.txt`

---

**Feito com ❤️ para ajudar você a encontrar seu lar em Portugal**
