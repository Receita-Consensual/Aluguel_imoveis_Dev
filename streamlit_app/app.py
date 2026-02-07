import streamlit as st
import pandas as pd
import numpy as np

# --- CONFIGURAÇÃO DA PÁGINA (Modo Wide é essencial para o mapa grande) ---
st.set_page_config(
    page_title="Receita Consensual | Mapa de Imóveis",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="collapsed" # Esconde a sidebar para focar no principal
)

# --- CSS PROFISSIONAL E LIMPO ---
st.markdown("""
    <style>
    /* --- GERAL --- */
    .main {
        background-color: #F8FAFC; /* Fundo cinza muito claro */
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    h1, h2, h3 { color: #1E293B !important; font-weight: 700; }
    p { color: #475569; }

    /* Remove o cabeçalho padrão do Streamlit */
    header {visibility: hidden;}
    
    /* --- ÁREA DE BUSCA (HERO SECTION) --- */
    .hero-container {
        background-color: #EFF6FF; /* Azul clarinho muito suave para destacar o topo */
        padding: 40px 20px;
        border-bottom: 1px solid #DBEAFE;
        text-align: center;
        margin-top: -60px; /* Ajuste para colar no topo */
    }
    .hero-title {
        font-size: 3rem;
        color: #1E3A8A; /* Azul marinho profissional */
        margin-bottom: 10px;
    }
    .hero-subtitle {
        font-size: 1.2rem;
        color: #64748B;
        margin-bottom: 30px;
    }

    /* Estilo para os inputs da barra de busca parecerem uma coisa só */
    /* Isso requer um pouco de "hack" no Streamlit, vamos tentar deixar limpo */
    [data-testid="stForm"] {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid #E2E8F0;
        max-width: 900px;
        margin: 0 auto; /* Centraliza a barra */
    }

    /* Botão de Busca Estilo Idealista */
    .stButton > button {
        background-color: #DB2777; /* Um rosa/magenta profissional para destaque, ou mude para azul #2563EB */
        color: white;
        font-weight: 600;
        border-radius: 8px;
        height: 100%;
        width: 100%;
        border: none;
        transition: all 0.2s;
    }
    .stButton > button:hover {
        background-color: #BE185D; /* Cor um pouco mais escura no hover */
        box-shadow: 0 4px 12px rgba(219, 39, 119, 0.3);
    }

    /* --- MAPA GIGANTE --- */
    /* Força o mapa a ter uma altura mínima decente */
    [data-testid="stMapContainer"] {
        height: 600px;
        border-radius: 12px;
        overflow: hidden;
        border: 1px solid #CBD5E1;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }

    /* --- CARDS DE RESULTADO (Abaixo do mapa) --- */
    .prop-card {
        background: white; border-radius: 12px; padding: 20px; border: 1px solid #E2E8F0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05); transition: transform 0.2s;
    }
    .prop-card:hover { transform: translateY(-3px); border-color: #DB2777; }
    .price { color: #DB2777; font-weight: 800; font-size: 22px; }
    </style>
""", unsafe_allow_html=True)

# --- CABEÇALHO E BARRA DE BUSCA ---
# Usamos um container para aplicar o fundo colorido no topo
with st.container():
    st.markdown("""
        <div class="hero-container">
            <h1 class="hero-title">Receita Consensual</h1>
            <p class="hero-subtitle">A única plataforma com pesquisa grátis no mapa gigante.</p>
        </div>
    """, unsafe_allow_html=True)

    # Barra de busca centralizada (Usando st.form para agrupar)
    with st.form("search_form"):
        # Colunas para organizar: Local (grande) | Tipo (médio) | Botão (pequeno)
        col_local, col_tipo, col_btn = st.columns([3, 1, 1])
        
        with col_local:
            localizacao = st.text_input("📍 Onde quer viver?", placeholder="Ex: Aveiro, Glória, Praia da Barra...")
        with col_tipo:
            tipo_operacao = st.selectbox("🏠 Tipo", ["Arrendar", "Comprar"], index=0)
        with col_btn:
            # Espaço vazio para alinhar o botão verticalmente com os inputs
            st.write("") 
            st.write("")
            submitted = st.form_submit_button("🔍 PROCURAR")

# --- ÁREA PRINCIPAL: O MAPA GIGANTE ---
st.write("") # Espapçamento
st.subheader(f"🗺️ Explorar no Mapa {'em ' + localizacao if localizacao else ''}")

# DADOS DE EXEMPLO PARA O MAPA (Amanhã conectamos o Supabase)
# Gerando pontos aleatórios em volta de Aveiro para visualizar o mapa cheio
map_data = pd.DataFrame(
    np.random.randn(50, 2) / [50, 50] + [40.6405, -8.6538], # Coordenadas de Aveiro
    columns=['lat', 'lon'])

# O MAPA GIGANTE
st.map(map_data, zoom=12, use_container_width=True)

# --- RESULTADOS EM CARDS (Abaixo do mapa) ---
st.write("")
st.subheader("Destaques Encontrados")

col1, col2, col3 = st.columns(3)
# Exemplo simples de cards
for i in range(3):
    with [col1, col2, col3][i]:
        st.markdown(f"""
            <div class="prop-card">
                <div class="price">€ {850 + (i*150)}</div>
                <h3>Apartamento T2 Moderno</h3>
                <p>📍 Aveiro, Centro</p>
                <small>{tipo_operacao} • Disponível</small>
            </div>
        """, unsafe_allow_html=True)