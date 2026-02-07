import streamlit as st
import pandas as pd
import numpy as np

# --- CONFIGURAÇÃO DA PÁGINA (Modo Wide para o mapa gigante) ---
st.set_page_config(
    page_title="Receita Consensual | Imóveis",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CSS PROFISSIONAL: AZUL AGRADÁVEL E ESTILO IDEALISTA ---
st.markdown("""
    <style>
    /* --- GERAL --- */
    /* Força o tema claro e define a fonte */
    .stApp {
        background-color: #F8FAFC; /* Fundo cinza-azulado muito claro */
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        color: #1E293B; /* Cor de texto padrão (cinza escuro) */
    }
    h1, h2, h3 { color: #1E3A8A !important; font-weight: 800; } /* Títulos em azul marinho forte */
    p, small { color: #475569; } /* Textos secundários em cinza médio */

    /* Remove o cabeçalho padrão e a barra superior colorida do Streamlit */
    header {visibility: hidden;}
    .st-emotion-cache-12fmjuu { display: none; } /* Remove a barra colorida do topo */

    /* --- ÁREA DE BUSCA (HERO SECTION) --- */
    .hero-container {
        background: linear-gradient(135deg, #EFF6FF 0%, #DBEAFE 100%); /* Degradê azul suave */
        padding: 50px 20px 60px 20px; /* Mais espaço na parte inferior para a barra */
        text-align: center;
        margin-top: -70px; /* Cola no topo da tela */
        border-bottom: 1px solid #BFDBFE;
    }
    .hero-title {
        font-size: 3.5rem;
        color: #1E40AF; /* Azul vibrante */
        margin-bottom: 15px;
        text-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .hero-subtitle {
        font-size: 1.3rem;
        color: #4B5563;
        max-width: 700px;
        margin: 0 auto 30px auto;
    }

    /* --- BARRA DE BUSCA FLUTUANTE --- */
    /* Estiliza o formulário para parecer uma barra única e limpa */
    [data-testid="stForm"] {
        background-color: #FFFFFF;
        padding: 15px 25px;
        border-radius: 50px; /* Bordas bem redondas estilo Idealista */
        box-shadow: 0 10px 25px -5px rgba(30, 58, 138, 0.15); /* Sombra azulada suave */
        border: 1px solid #E2E8F0;
        max-width: 950px;
        margin: -40px auto 30px auto; /* Sobe para ficar sobre o hero */
        position: relative; /* Para ficar por cima */
        z-index: 10;
    }

    /* Ajusta os inputs para ficarem limpos dentro da barra */
    [data-testid="stForm"] div[data-baseweb="input"] {
        background-color: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    [data-testid="stForm"] input {
        font-size: 1.1rem;
        color: #1E293B;
    }
    /* Remove rótulos dos inputs para visual mais limpo */
    [data-testid="stForm"] label { display: none; }


    /* Botão de Busca Estilo Idealista (Azul Vibrante) */
    .stButton > button {
        background-color: #2563EB; /* Azul forte e agradável */
        color: white;
        font-weight: 700;
        font-size: 1.1rem;
        border-radius: 40px; /* Botão redondo */
        height: 55px;
        width: 100%;
        border: none;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(37, 99, 235, 0.2);
    }
    .stButton > button:hover {
        background-color: #1D4ED8; /* Azul um pouco mais escuro no hover */
        box-shadow: 0 8px 15px rgba(37, 99, 235, 0.3);
        transform: translateY(-2px);
    }

    /* --- MAPA GIGANTE --- */
    [data-testid="stMapContainer"] {
        height: 650px; /* Mapa bem alto */
        border-radius: 20px;
        overflow: hidden;
        border: 3px solid #FFFFFF; /* Borda branca grossa */
        box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.1); /* Sombra destacada */
        margin-top: 20px;
    }
    /* Força o mapa a ser claro (se possível pelo Streamlit) */
    [data-testid="stMapContainer"] canvas { filter: none !important; }


    /* --- CARDS DE RESULTADO --- */
    .prop-card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 24px;
        border: 1px solid #F1F5F9;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
        height: 100%; /* Para alinhamento */
    }
    .prop-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        border-color: #BFDBFE; /* Borda azul clara no hover */
    }
    .price {
        color: #DB2777; /* Rosa/Magenta para destaque do preço (contraste bonito com azul) */
        font-weight: 800;
        font-size: 26px;
        margin-bottom: 10px;
        display: block;
    }
    .badge {
        background-color: #EFF6FF;
        color: #1E40AF;
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 700;
        text-transform: uppercase;
        display: inline-block;
        margin-bottom: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# --- ÁREA DE BUSCA (HERO SECTION) ---
with st.container():
    st.markdown("""
        <div class="hero-container">
            <h1 class="hero-title">Receita Consensual</h1>
            <p class="hero-subtitle">Encontre o seu lugar ideal em Portugal. Pesquisa inteligente no mapa gigante.</p>
        </div>
    """, unsafe_allow_html=True)

    # Barra de busca unificada
    with st.form("search_form", clear_on_submit=False):
        col_local, col_tipo, col_btn = st.columns([4, 2, 1.5], gap="medium")
        
        with col_local:
            # Usamos label_visibility="collapsed" para esconder o rótulo e manter o layout limpo
            localizacao = st.text_input("Localização", placeholder="📍 Digite uma cidade, bairro ou zona...", label_visibility="collapsed")
        with col_tipo:
            tipo_operacao = st.selectbox("Tipo", ["🏡 Arrendar", "🔑 Comprar"], index=0, label_visibility="collapsed")
        with col_btn:
            # O botão ocupa a altura total da coluna para alinhar
            submitted = st.form_submit_button("🔍 BUSCAR")

# --- ÁREA PRINCIPAL: MAPA GIGANTE ---
st.write("") # Espaçamento
st.subheader(f"🗺️ Explorando {localizacao if localizacao else 'Portugal'}")

# DADOS DE EXEMPLO (Pontos em Aveiro para visualização)
# Amanhã conectamos isso ao seu Supabase!
map_data = pd.DataFrame(
    np.random.randn(80, 2) / [60, 60] + [40.6405, -8.6538],
    columns=['lat', 'lon'])

# O Mapa Gigante e Claro
st.map(map_data, zoom=12, use_container_width=True)

# --- RESULTADOS EM CARDS ---
st.write("")
st.write("")
st.subheader("✨ Destaques para você")

col1, col2, col3 = st.columns(3)
# Exemplo de cards com o novo visual
for i in range(3):
    with [col1, col2, col3][i]:
        st.markdown(f"""
            <div class="prop-card">
                <span class="badge">{tipo_operacao.split(' ')[1]}</span>
                <span class="price">€ {850 + (i*200)}/mês</span>
                <h3>Apartamento T{2+i} Luminoso</h3>
                <p style="margin-bottom: 20px;">📍 Glória e Vera Cruz, Aveiro</p>
                <small>📅 Disponível agora • 📏 {90+(i*30)}m²</small>
            </div>
        """, unsafe_allow_html=True)
st.write("")
st.write("")