import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import os

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(
    page_title="Lugar | Imóveis em Portugal",
    page_icon="🏠",
    layout="wide"
)

# --- TRATAMENTO DA LOGO (Evita o erro de fechar o site) ---
# Busca o caminho real da pasta onde o script está
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
caminho_logo = os.path.join(diretorio_atual, "Gemini_Generated_Image_su6quisu6quisu6q.jpg")

# --- CSS: ESTILO IDEALISTA CLARO E AZUL ---
st.markdown("""
    <style>
    /* Forçar tema claro */
    .stApp { background-color: #FFFFFF !important; color: #1E293B !important; }
    header {visibility: hidden;}
    
    /* Título Azul Vibrante */
    .brand-title { color: #2563EB; font-size: 50px; font-weight: 900; margin-bottom: 0; }
    
    /* Barra de busca estilo Idealista */
    [data-testid="stForm"] {
        background-color: #F1F5F9;
        border-radius: 50px;
        padding: 10px 30px;
        border: 1px solid #E2E8F0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    
    /* Botão de Busca Rosa/Vibrante */
    .stButton > button {
        background-color: #EC4899; /* Rosa vibrante para destaque */
        color: white;
        border-radius: 30px;
        font-weight: bold;
        border: none;
        height: 45px;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# --- CABEÇALHO ---
col_logo, col_titulo = st.columns([1, 6])
with col_logo:
    if os.path.exists(caminho_logo):
        st.image(caminho_logo, width=80)
    else:
        st.warning("Logo não encontrada") # Não trava o site se a imagem sumir
with col_titulo:
    st.markdown('<h1 class="brand-title">Lugar</h1>', unsafe_allow_html=True)
    st.write("Propriedade de Receita Consensual")

# --- BARRA DE BUSCA (IDEALISTA STYLE) ---
with st.form("search_bar"):
    c1, c2, c3 = st.columns([4, 1, 1])
    with c1:
        # Placeholder para o Autocomplete do Google
        busca = st.text_input("📍 Onde você quer viver?", placeholder="Digite uma cidade ou bairro de Portugal...", label_visibility="collapsed")
    with c2:
        tipo = st.selectbox("Tipo", ["Arrendar", "Comprar"], label_visibility="collapsed")
    with c3:
        st.form_submit_button("PROCURAR")

# --- MAPA GIGANTE E CLARO ---
st.subheader("🗺️ Mapa de Oportunidades")

# Criando mapa claro (tiles='CartoDB positron' imita o Google Maps Light)
m = folium.Map(
    location=[40.6405, -8.6538], # Aveiro
    zoom_start=13, 
    tiles='CartoDB positron'
)

# Renderiza o mapa gigante
st_folium(m, width="100%", height=600, returned_objects=[])

st.divider()
st.info("💡 No 'Lugar', a pesquisa no mapa é sempre gratuita.")