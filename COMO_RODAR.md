# 🚀 Como Rodar o Lugar

## ⚡ Método Rápido (Recomendado)

```bash
./rodar_streamlit.sh
```

Esse script faz tudo automaticamente:
- Verifica o arquivo `.env`
- Cria o arquivo `.streamlit/secrets.toml` se necessário
- Instala as dependências
- Inicia o Streamlit

---

## 🧪 Testar Conexão Antes de Rodar

Para verificar se está tudo configurado corretamente:

```bash
python3 teste_streamlit.py
```

Este teste vai:
- ✅ Verificar se as variáveis de ambiente estão carregadas
- ✅ Testar a conexão com o Supabase
- ✅ Buscar imóveis de exemplo

---

## 📝 Método Manual

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar credenciais

Certifique-se de que o arquivo `.env` existe e contém:

```env
SUPABASE_URL=https://zprocqmlefzjrepxtxko.supabase.co
SUPABASE_ANON_KEY=sua_key_aqui
GOOGLE_API_KEY=sua_key_google_aqui
```

### 3. Rodar Streamlit

```bash
streamlit run app.py
```

---

## 🌐 Frontend React (Alternativo)

Se preferir rodar o frontend React ao invés do Streamlit:

```bash
npm install
npm run dev
```

O React abrirá em `http://localhost:5173`

---

## ❓ Problemas Comuns

### Erro: "SUPABASE_URL não encontrada"

**Solução:** Certifique-se de que o arquivo `.env` existe na raiz do projeto com as credenciais corretas.

### Erro: "Module not found"

**Solução:** Instale as dependências:
```bash
pip install -r requirements.txt
```

### Erro: "No data returned"

**Solução:** Verifique se:
1. As credenciais do Supabase estão corretas
2. Existem imóveis na tabela `imoveis`
3. As políticas RLS (Row Level Security) estão configuradas corretamente

---

## 📊 Banco de Dados

O projeto usa Supabase com as seguintes tabelas:

- **imoveis**: Armazena os imóveis encontrados
- **demandas**: Armazena as buscas dos usuários
- **alertas_fundador**: Cadastro de membros fundadores

Para ver os dados no Supabase:
👉 https://supabase.com/dashboard/project/zprocqmlefzjrepxtxko

---

## 🎨 Duas Versões Disponíveis

### 🔷 Streamlit (app.py)
- Interface Python moderna
- Gradiente roxo/rosa
- Mapa interativo com Folium
- Ideal para MVP e testes rápidos

### ⚛️ React (src/)
- Interface TypeScript/React
- Design azul claro e cinza
- Google Maps integrado
- Ideal para produção

---

## 📦 Motor de Busca (Opcional)

Para rodar o motor que busca imóveis automaticamente:

```bash
python3 motor_turbo.py
```

Este script busca imóveis nos sites:
- 🏠 Sapo.pt
- 🏠 Idealista.pt

E salva no Supabase automaticamente.

---

**Dúvidas?** Veja os logs no terminal quando rodar o Streamlit.
