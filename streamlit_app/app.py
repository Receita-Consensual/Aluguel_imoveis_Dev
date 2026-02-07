import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import os
import numpy as np
import time
from datetime import datetime

# ==========================================
# 1. CONFIGURAÇÕES DE NÍVEL EMPRESARIAL
# ==========================================
st.set_page_config(
    page_title="Lugar | Inteligência Imobiliária",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. GESTÃO DE ESTADO (LOGIN, SUBSCRITORES, FAVORITOS)
# ==========================================
if 'auth_state' not in st.session_state:
    st.session_state.auth_state = {
        'is_logged': False,
        'user_name': None,
        'plan': 'Visitante',  # Visitante, PRO, Enterprise
        'favorites': []
    }

if 'search_history' not in st.session_state:
    st.session_state.search_history = []

# ==========================================
# 3. ENGINE DE ESTILO (CSS CUSTOMIZADO - +150 LINHAS)
# ==========================================
st.markdown("""
    <style>
    /* Importação de fonte moderna */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');

    /* Reset Geral para Branco e Azul Profissional */
    .stApp {
        background-color: #FFFFFF;
        font-family: 'Inter', sans-serif;
        color: #1E293B;
    }
    header {visibility: hidden;}
    
    /* Sidebar Estilizada */
    [data-testid="stSidebar"] {
        background-color: #F8FAFC !important;
        border-right: 1px solid #E2E8F0;
    }

    /* Hero Section (A "Vida" do site) */
    .hero-section {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        padding: 80px 20px;
        text-align: center;
        border-radius: 0 0 50px 50px;
        margin-top: -100px;
        margin-bottom: 60px;
        box-shadow: 0 20px 40px rgba(30, 58, 138, 0.2);
    }
    .hero-section h1 {
        color: white !important;
        font-size: 4.5rem !important;
        font-weight: 800 !important;
        letter-spacing: -3px;
        margin-bottom: 10px;
    }
    .hero-section p {
        color: #DBEAFE;
        font-size: 1.4rem;
        font-weight: 300;
    }

    /* Barra de Busca Flutuante Style Idealista */
    .search-dock {
        background: white;
        padding: 35px;
        border-radius: 30px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.15);
        max-width: 1100px;
        margin: -80px auto 50px auto;
        border: 1px solid #F1F5F9;
        display: flex;
        gap: 15px;
        z-index: 1000;
    }

    /* Cards de Imóvel Premium */
    .prop-card {
        background-color: #FFFFFF;
        border-radius: 24px;
        padding: 0px;
        border: 1px solid #F1F5F9;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        margin-bottom: 30px;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }
    .prop-card:hover {
        transform: translateY(-12px);
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.1);
        border-color: #3B82F6;
    }
    .prop-content { padding: 25px; }
    .price-tag { color: #2563EB; font-size: 30px; font-weight: 800; }
    .location { color: #64748B; font-size: 14px; margin-bottom: 15px; }
    
    /* Badges de Status */
    .badge-new { background: #DCFCE7; color: #166534; padding: 6px 14px; border-radius: 12px; font-size: 11px; font-weight: 700; }
    .badge-ai { background: #EEF2FF; color: #4338CA; padding: 6px 14px; border-radius: 12px; font-size: 11px; font-weight: 700; border: 1px solid #C7D2FE; }

    /* Estilização do Mapa */
    [data-testid="stMapContainer"], .folium-map {
        border-radius: 35px !important;
        border: 10px solid white !important;
        box-shadow: 0 30px 60px -12px rgba(0, 0, 0, 0.2) !important;
    }

    /* Botão Primário */
    .stButton > button {
        background: #2563EB;
        color: white;
        border-radius: 15px;
        padding: 15px 30px;
        font-weight: 600;
        border: none;
        transition: all 0.3s;
        width: 100%;
    }
    .stButton > button:hover {
        background: #1E40AF;
        transform: scale(1.02);
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 4. TRATAMENTO ROBUSTO DE LOGO (FIX ERROR)
# ==========================================
def get_logo():
    # Nicolas, aqui buscamos a imagem em múltiplos lugares possíveis
    paths = [
        "Gemini_Generated_Image_su6quisu6quisu6q.jpg",
        "streamlit_app/Gemini_Generated_Image_su6quisu6quisu6q.jpg",
        "../Gemini_Generated_Image_su6quisu6quisu6q.jpg"
    ]
    for p in paths:
        if os.path.exists(p): return p
    return None

logo_oficial = get_logo()

# ==========================================
# 5. BARRA LATERAL (GESTÃO DE CONTA E MÉTRICAS)
# ==========================================
with st.sidebar:
    if logo_oficial:
        st.image(logo_oficial, width=180)
    else:
        st.markdown("<h1 style='color: #2563EB;'>LUGAR</h1>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    if not st.session_state.auth_state['is_logged']:
        st.subheader("🔑 Acesso Restrito")
        with st.form("login_form"):
            email = st.text_input("E-mail")
            senha = st.text_input("Senha", type="password")
            entrar = st.form_submit_button("Entrar no Painel PRO")
            if entrar:
                if email and senha:
                    st.session_state.auth_state['is_logged'] = True
                    st.session_state.auth_state['user_name'] = email.split('@')[0]
                    st.session_state.auth_state['plan'] = 'PRO'
                    st.success("Acesso liberado!")
                    time.sleep(1)
                    st.rerun()
    else:
        st.success(f"Olá, {st.session_state.auth_state['user_name']}!")
        st.info(f"Plano Ativo: {st.session_state.auth_state['plan']}")
        if st.button("Sair da Conta"):
            st.session_state.auth_state['is_logged'] = False
            st.rerun()

    st.markdown("---")
    st.subheader("📊 Market Analytics (Aveiro)")
    st.metric("Demanda de Arrendamento", "Alta", "+14%")
    st.metric("Yield Médio", "5.8%", "-0.2%")
    
    st.markdown("---")
    st.caption("© 2026 Lugar • By Receita Consensual")

# ==========================================
# 6. HEADER PRINCIPAL (HERO)
# ==========================================
st.markdown("""
    <div class="hero-section">
        <h1>Lugar</h1>
        <p>A nova era da busca imobiliária inteligente em Portugal.</p>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 7. BARRA DE BUSCA "IDEALISTA STYLE"
# ==========================================
with st.container():
    st.markdown('<div class="search-dock">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([3, 1, 1, 1])
    with c1:
        # Placeholder para Autocomplete
        local_input = st.text_input("Localização", placeholder="Cidade, freguesia ou rua...", label_visibility="collapsed")
    with c2:
        tipo_negocio = st.selectbox("Operação", ["Arrendar", "Comprar"], label_visibility="collapsed")
    with c3:
        tipologia = st.selectbox("Tipologia", ["T0/T1", "T2", "T3", "T4+"], label_visibility="collapsed")
    with c4:
        buscar = st.button("🔍 PROCURAR")
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 8. LAYOUT CENTRAL (MAPA + LISTAGEM + FILTROS)
# ==========================================
col_map, col_details = st.columns([2.5, 1])

with col_map:
    st.subheader("📍 Exploração por Mapa")
    
    # Mapa focado em Aveiro com estilo CLARO
    m = folium.Map(
        location=[40.6405, -8.6538], 
        zoom_start=14, 
        tiles='CartoDB positron',
        zoom_control=False
    )
    
    # Simulação de Dados Inteligentes (Supabase Mock)
    map_data = pd.DataFrame({
        'lat': [40.6445, 40.6380, 40.6410, 40.6480],
        'lon': [-8.6588, -8.6520, -8.6480, -8.6620],
        'preco': [850, 1100, 750, 2200],
        'tipo': ['Apartamento', 'Moradia', 'Apartamento', 'Penthouse']
    })

    for _, row in map_data.iterrows():
        color = '#2563EB' if row['preco'] < 1500 else '#1E3A8A'
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=12,
            popup=f"€{row['preco']}",
            color=color,
            fill=True,
            fill_opacity=0.8
        ).add_to(m)
    
    # Renderização do Mapa
    st_folium(m, width="100%", height=700, returned_objects=[])

with col_details:
    st.subheader("✨ Melhores Oportunidades")
    
    # Filtro Rápido
    filtro = st.radio("Ordenar por:", ["Melhor Preço", "Recentemente Adicionado"], horizontal=True)
    
    for i in range(3):
        # Lógica de Cartão com "Vida"
        is_ai_verified = True if i % 2 == 0 else False
        
        st.markdown(f"""
            <div class="prop-card">
                <div style="height: 180px; background: #E2E8F0; display: flex; align-items: center; justify-content: center;">
                    <span style="color: #94A3B8;">Foto do Imóvel {i+1}</span>
                </div>
                <div class="prop-content">
                    <div style="display: flex; gap: 8px; margin-bottom: 10px;">
                        <span class="badge-new">NOVO</span>
                        {"<span class='badge-ai'>IA VERIFIED</span>" if is_ai_verified else ""}
                    </div>
                    <div class="price-tag">€ {850 + (i*300)}<span style="font-size: 14px; font-weight: normal;">/mês</span></div>
                    <h4 style="margin: 0; font-size: 18px;">Apartamento T2 em Aveiro</h4>
                    <p class="location">📍 Vera Cruz, Distrito de Aveiro</p>
                    <div style="display: flex; justify-content: space-between; font-size: 12px; color: #475569; background: #F8FAFC; padding: 10px; border-radius: 12px;">
                        <span>📏 95m²</span>
                        <span>🏢 2º Andar</span>
                        <span>🛏️ T2</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Interação para subscritores
        if not st.session_state.auth_state['is_logged']:
            st.button("Ver Contato", key=f"btn_contact_{i}", help="Apenas assinantes PRO")
        else:
            st.button("Contactar Proprietário", key=f"btn_contact_pro_{i}")

# ==========================================
# 9. FERRAMENTAS EXCLUSIVAS (LINHAS EXTRAS PARA ROBUSTEZ)
# ==========================================
st.markdown("---")
c_tool1, c_tool2 = st.columns(2)

with c_tool1:
    st.subheader("🤖 IA Valuation Tool (Beta)")
    st.write("Calcule o preço justo de qualquer imóvel em segundos.")
    with st.expander("Abrir Calculadora de Preço"):
        sqm = st.number_input("Metros Quadrados", 10, 500, 80)
        zona = st.selectbox("Zona", ["Aveiro Centro", "Ílhavo", "Esgueira", "Glória"])
        if st.button("Estimar Preço"):
            est = sqm * 12.5 if zona == "Aveiro Centro" else sqm * 9.8
            st.success(f"O valor de mercado estimado é: € {est:,.2f}")

with c_tool2:
    st.subheader("📬 Alerta de Oportunidades")
    st.write("Não perca a próxima casa em Aveiro. O robô te avisa.")
    st.text_input("Seu melhor e-mail", placeholder="nicolas@exemplo.pt")
    st.button("Ativar Alerta Radar")

# ==========================================
# 10. RODAPÉ INSTITUCIONAL (LINHAS FINAIS)
# ==========================================
st.markdown("---")
st.markdown(f"""
    <div style="text-align: center; padding: 40px; color: #94A3B8;">
        <p><b>Lugar</b> é um produto de engenharia de dados desenvolvido por <b>Receita Consensual</b>.</p>
        <p>Aveiro, Portugal • {datetime.now().year} | Versão 3.0.4-Enterprise</p>
        <p style="font-size: 10px;">A plataforma Lugar utiliza algoritmos avançados de scraping e inteligência artificial para monitorar o mercado imobiliário em tempo real.</p>
    </div>
""", unsafe_allow_html=True)