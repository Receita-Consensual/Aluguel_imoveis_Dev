import streamlit as st
import pandas as pd
import requests
from motor_busca.db import get_supabase_client

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Receita Consensual | Dashboard", layout="wide")

# --- ESTILIZAÇÃO CSS (Azul Claro e Cinza Slate) ---
st.markdown("""
    <style>
    /* Fundo e Fonte Geral */
    .main { background-color: #F8FAFC; font-family: 'Inter', sans-serif; }
    
    /* Customização da Sidebar */
    section[data-testid="stSidebar"] { background-color: #E2E8F0 !important; }
    
    /* Cartão de Imóvel Estilizado */
    .property-card {
        background-color: white;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        border: 1px solid #CBD5E1;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease-in-out;
    }
    .property-card:hover {
        transform: translateY(-4px);
        border-color: #3B82F6;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    .price { color: #1D4ED8; font-size: 22px; font-weight: 800; margin-bottom: 5px; }
    .details { color: #64748B; font-size: 14px; margin-bottom: 15px; }
    .btn-link {
        display: inline-block;
        background-color: #1D4ED8;
        color: white !important;
        padding: 8px 16px;
        border-radius: 6px;
        text-decoration: none;
        font-weight: 600;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# --- LOGICA GOOGLE AUTOCOMPLETE (Manual) ---
def get_google_suggestions(query, api_key):
    if not query or len(query) < 3: return []
    url = f"https://maps.googleapis.com/maps/api/place/autocomplete/json?input={query}&key={api_key}&language=pt-PT"
    try:
        response = requests.get(url).json()
        return [p['description'] for p in response.get('predictions', [])]
    except:
        return []

# --- INTERFACE ---
with st.sidebar:
    st.title("🏙️ Busca Avançada")
    st.write("Configure seus filtros abaixo:")
    
    # Busca de Local com Google
    api_key = "SUA_API_KEY_AQUI" # Insira sua chave do Google Maps aqui
    
    local_input = st.text_input("📍 Localização (Autocomplete Google)", placeholder="Ex: Aveiro, Portugal")
    
    # Sugestões aparecem aqui se o usuário digitar
    if local_input and api_key != "SUA_API_KEY_AQUI":
        sugestoes = get_google_suggestions(local_input, api_key)
        if sugestoes:
            local_selecionado = st.selectbox("Confirmar local:", [""] + sugestoes)

    st.divider()
    preco = st.slider("Orçamento Mensal (€)", 0, 3000, (600, 1200))
    quartos = st.segmented_control("Quartos", ["T0", "T1", "T2", "T3+"], default="T2")

# --- CABEÇALHO ---
st.title("🔭 Radar de Imóveis | Receita Consensual")
st.write(f"Exibindo resultados para: **{local_input if local_input else 'Portugal Todo'}**")

# --- GRID DE EXIBIÇÃO ---
# Aqui simulamos os dados que vêm do seu motor_infinito
# imoveis_df = carregar_dados_do_supabase()

col1, col2, col3 = st.columns(3)

# Exemplo de dados para não ficar vazio enquanto o motor trabalha
exemplo_dados = [
    {"titulo": "T2 Moderno com Varanda", "local": "Aveiro, Centro", "preco": 850, "link": "https://olx.pt"},
    {"titulo": "T1 Próximo à Universidade", "local": "Glória, Aveiro", "preco": 600, "link": "https://idealista.pt"},
    {"titulo": "Moradia Isolada T3", "local": "Ílhavo", "preco": 1100, "link": "https://custojusto.pt"}
]

for i, imovel in enumerate(exemplo_dados):
    target_col = [col1, col2, col3][i % 3]
    with target_col:
        st.markdown(f"""
            <div class="property-card">
                <div class="price">€ {imovel['preco']}</div>
                <div style="font-weight: 700; font-size: 18px; margin-bottom: 5px;">{imovel['titulo']}</div>
                <div class="location-tag">📍 {imovel['local']}</div>
                <div class="details">Disponível agora • Verificado pelo Motor</div>
                <a href="{imovel['link']}" class="btn-link" target="_blank">Ver Anúncio</a>
            </div>
        """, unsafe_allow_html=True)