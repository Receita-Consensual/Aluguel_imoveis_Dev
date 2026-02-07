import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Lugar | Imóveis em Portugal",
    page_icon="🏠",
    layout="wide"
)

# --- CSS PARA DEIXAR O SITE CLARO E PROFISSIONAL ---
st.markdown("""
    <style>
    /* Forçar fundo branco e texto escuro */
    .stApp {
        background-color: #FFFFFF !important;
        color: #1E293B !important;
    }
    
    /* Esconder elementos padrão do Streamlit */
    header {visibility: hidden;}
    footer {visibility: visible;}
    footer:after {
        content: 'Propriedade de Receita Consensual';
        display: block;
        position: relative;
        text-align: center;
        color: #64748B;
        padding: 10px;
    }

    /* Barra de busca estilo Idealista (Clara) */
    .search-container {
        background-color: #F8FAFC;
        padding: 30px;
        border-radius: 15px;
        border: 1px solid #E2E8F0;
        margin-bottom: 20px;
    }

    /* Título e Logo */
    .brand-title {
        color: #1E3A8A;
        font-size: 45px;
        font-weight: 900;
        margin-left: 15px;
    }

    /* Botão de Busca */
    .stButton > button {
        background-color: #2563EB;
        color: white;
        border-radius: 8px;
        height: 50px;
        width: 100%;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- CABEÇALHO (LOGO E NOME) ---
col_logo, col_name = st.columns([1, 8])
with col_logo:
    # Usando a sua logo carregada
    st.image("Gemini_Generated_Image_su6quisu6quisu6q.jpg", width=100)
with col_name:
    st.markdown('<h1 class="brand-title">Lugar</h1>', unsafe_allow_html=True)
    st.write("Encontre seu próximo lar em Portugal.")

st.divider()

# --- BARRA DE BUSCA COM PLACEHOLDER PARA AUTOCOMPLETE ---
with st.container():
    c1, c2, c3 = st.columns([3, 1, 1])
    with c1:
        # Aqui o usuário digita. O Autocomplete real exige a biblioteca do Google carregada.
        local = st.text_input("📍 Onde você quer viver?", placeholder="Ex: Aveiro, Glória e Vera Cruz...")
    with c2:
        tipo = st.selectbox("Tipo", ["Arrendar", "Comprar"])
    with c3:
        st.write("") # Espaçamento vertical
        st.write("") 
        st.button("🔍 PROCURAR")

# --- MAPA GIGANTE E CLARO (Google Maps Style) ---
st.subheader("🗺️ Explorar no Mapa")

# Usando Folium para garantir que o mapa seja CLARO (tiles='CartoDB positron')
# Isso evita o mapa escuro que você não gostou.
m = folium.Map(
    location=[40.6405, -8.6538], 
    zoom_start=13, 
    tiles='CartoDB positron', # Este é o estilo mais limpo e claro disponível
    control_scale=True
)

# Adicionando pontos de exemplo (depois ligamos ao seu banco de dados)
folium.Marker(
    [40.6445, -8.6588], 
    popup="Apartamento T2 - €850",
    icon=folium.Icon(color='blue', icon='home')
).add_to(m)

# Renderiza o mapa gigante
st_folium(m, width="100%", height=600)

# --- RODAPÉ ---
st.markdown("---")
st.caption("© 2026 Lugar - Uma plataforma gerida por **Receita Consensual**.")