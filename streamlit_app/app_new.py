import streamlit as st
import streamlit.components.v1 as components

# Configuração da página
st.set_page_config(
    page_title="Lugar | Imóveis no Mapa 🇵🇹",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Meta Tags para SEO
URL_DA_FOTO = "https://i.imgur.com/placeholder.jpg"
st.markdown(
    f"""
    <head>
        <meta property="og:title" content="Lugar | Encontre sua casa no mapa 🤖">
        <meta property="og:description" content="O robô inteligente que varre a internet para encontrar seu próximo lar em Portugal e no Brasil.">
        <meta property="og:image" content="{URL_DA_FOTO}">
        <meta property="og:image:width" content="1200">
        <meta property="og:image:height" content="630">
        <meta property="og:url" content="https://aluguelimoveis-queo6rsnzidypueducznxq.streamlit.app/">
        <meta property="og:type" content="website">
    </head>
    """,
    unsafe_allow_html=True
)

# Esconder elementos do Streamlit
st.markdown("""
    <style>
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    .stDeployButton,
    footer,
    #MainMenu {
        display: none !important;
    }
    .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    iframe {
        border: none;
    }
    </style>
    """, unsafe_allow_html=True)

# Servir a aplicação React
# Você precisa fazer o deploy da pasta /dist em um servidor estático
# Opções: Vercel, Netlify, GitHub Pages, etc.
# Substitua a URL abaixo pela URL do seu deploy
REACT_APP_URL = "http://localhost:5173"  # Mude para a URL de produção

components.iframe(REACT_APP_URL, height=800, scrolling=True)

# Instruções de deploy
st.sidebar.markdown("""
## 🚀 Deploy da Aplicação React

Para fazer o deploy completo:

1. **Build da aplicação:**
   ```bash
   npm run build
   ```

2. **Deploy da pasta /dist:**
   - **Vercel:** `vercel --prod`
   - **Netlify:** Arraste a pasta `dist` para netlify.com/drop
   - **GitHub Pages:** Configure no repositório

3. **Atualize a URL:**
   - Substitua `REACT_APP_URL` no código acima
   - Faça commit no Streamlit

4. **Credenciais já configuradas:**
   - ✅ Supabase: https://zprocqmlefzjrepxtxko.supabase.co
   - ✅ Google Maps API Key configurada
   - ✅ Mesmo banco de dados do Streamlit antigo
""")
