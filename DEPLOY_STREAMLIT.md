# 🚀 Deploy da Nova Versão no Streamlit

## ✅ O que já está feito:

1. **Supabase atualizado** → Usando o mesmo banco do Streamlit antigo
2. **Google Maps configurado** → Chave instalada
3. **"LOCAL" personalizado** → Marcador do mapa mostra "LOCAL"
4. **Build criado** → Pasta `/dist` pronta para deploy

---

## 📦 Opção 1: Deploy Rápido (Recomendado)

### 1. Deploy da Aplicação React no Vercel

```bash
# Instalar Vercel CLI
npm i -g vercel

# Fazer deploy da pasta dist
cd dist
vercel --prod
```

### 2. Atualizar o Streamlit

Após o deploy, você receberá uma URL tipo: `https://seu-app.vercel.app`

No arquivo `streamlit_app/app_new.py`, linha 56:
```python
REACT_APP_URL = "https://seu-app.vercel.app"  # Sua URL do Vercel
```

### 3. Fazer deploy do Streamlit

No seu terminal do Streamlit Cloud:
- Substitua `app.py` por `app_new.py` ou
- Configure `app_new.py` como entrypoint no dashboard

---

## 📦 Opção 2: Deploy no Netlify (Mais Fácil)

### 1. Deploy via Drag & Drop

1. Acesse: https://app.netlify.com/drop
2. Arraste a pasta `/dist` para a página
3. Copie a URL gerada (ex: `https://seu-app.netlify.app`)

### 2. Atualizar Streamlit

Mesmos passos da Opção 1, passo 2 e 3.

---

## 📦 Opção 3: Substituir Completamente o Streamlit

Se preferir usar APENAS a nova versão React (sem Streamlit):

### 1. Deploy no Vercel

```bash
vercel --prod
```

### 2. Configure domínio personalizado

No dashboard do Vercel:
- Settings → Domains
- Adicione: `aluguelimoveis.vercel.app` (ou seu domínio)

### 3. Redirecionar Streamlit (opcional)

No `streamlit_app/app.py`:
```python
import streamlit as st
st.markdown("""
<meta http-equiv="refresh" content="0; url=https://seu-app.vercel.app">
""", unsafe_allow_html=True)
```

---

## 🔑 Credenciais Configuradas

✅ **Supabase URL:** `https://zprocqmlefzjrepxtxko.supabase.co`
✅ **Google Maps API:** `AIzaSyCws8dm1mPhPKdu4VUk7BTBEe25qGZDrb4`
✅ **Banco de dados:** Mesmo do Streamlit antigo

---

## 🧪 Testar Localmente

```bash
npm run preview -- --host 0.0.0.0 --port 5173
```

Acesse: `http://localhost:5173`

---

## 📝 Notas Importantes

1. **Build está na pasta `/dist`** → É essa pasta que você faz deploy
2. **Não precisa do Node.js em produção** → É apenas HTML/CSS/JS estático
3. **Credenciais já estão no código** → Builded com as variáveis corretas
4. **Compatível com o Streamlit** → Usa o mesmo Supabase

---

## 🆘 Ajuda

Se tiver problemas, rode:
```bash
npm run build && npm run preview
```

E teste em `http://localhost:5173` antes de fazer deploy.
