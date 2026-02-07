import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import os
import numpy as np
import time
from datetime import datetime

# ==========================================
# 1. CONFIGURAÇÕES
# ==========================================
st.set_page_config(
    page_title="Lugar | Inteligência Imobiliária",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. GESTÃO DE ESTADO
# ==========================================
if 'auth_state' not in st.session_state:
    st.session_state.auth_state = {'is_logged': False, 'user_name': None, 'plan': 'Visitante'}

# ==========================================
# 3. ENGINE DE ESTILO VIBRANTE (CSS COM VIDA)
# ==========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800;900&display=swap');

    .stApp {
        background-color: #FFFFFF;
        font-family: 'Inter', sans-serif;
        color: #0F172A;
    }
    header {visibility: hidden;}
    [data-testid="stSidebar"] { background-color: #F8FAFC !important; border-right: 1px solid #E2E8F0; }

    /* Hero Section Elétrica */
    .hero-section {
        background: linear-gradient(120deg, #2563EB, #1D4ED8, #3B82F6); /* Azul mais vivo e dinâmico */
        padding: 85px 20px;
        text-align: center;
        border-radius: 0 0 60px 60px;
        margin-top: -100px;
        margin-bottom: 70px;
        box-shadow: 0 25px 50px -12px rgba(37, 99, 235, 0.4); /* Sombra azulada vibrante */
    }
    .hero-section h1 {
        color: white !important; font-size: 5rem !important; font-weight: 900 !important;
        letter-spacing: -3px; margin-bottom: 15px;
        text-shadow: 2px 4px 8px rgba(0,0,0,0.2); /* Texto salta da tela */
    }
    .hero-section p { color: #EFF6FF; font-size: 1.5rem; font-weight: 500; }

    /* Barra de Busca Flutuante com Luz */
    .search-dock {
        background: white; padding: 40px; border-radius: 35px;
        box-shadow: 0 35px 70px -15px rgba(37, 99, 235, 0.25); /* Sombra com cor */
        max-width: 1100px; margin: -90px auto 60px auto; border: 1px solid #EFF6FF;
        z-index: 1000;
    }

    /* Cards de Imóvel Cheios de Vida */
    .prop-card {
        background-color: #FFFFFF; border-radius: 28px; padding: 0px;
        border: 2px solid #F1F5F9; transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        margin-bottom: 35px; overflow: hidden;
        box-shadow: 0 10px 20px -5px rgba(0, 0, 0, 0.05);
    }
    .prop-card:hover {
        transform: translateY(-15px) scale(1.02);
        box-shadow: 0 30px 60px -12px rgba(37, 99, 235, 0.3); /* Sombra azul vibrante no hover */
        border-color: #60A5FA;
    }
    /* Placeholder de imagem com degradê em vez de cinza chato */
    .prop-img-placeholder {
        height: 200px;
        background: linear-gradient(to top right, #DBEAFE, #F0F9FF);
        display: flex; align-items: center; justify-content: center; color: #3B82F6; font-weight: 600;
    }
    
    /* Badges Vibrantes (Cores sólidas que estouram) */
    .badge-new { background: #22C55E; color: white; padding: 8px 16px; border-radius: 14px; font-size: 12px; font-weight: 800; box-shadow: 0 4px 10px rgba(34, 197, 94, 0.3); }
    .badge-ai { background: #6366F1; color: white; padding: 8px 16px; border-radius: 14px; font-size: 12px; font-weight: 800; box-shadow: 0 4px 10px rgba(99, 102, 241, 0.3); }

    .price-tag { color: #2563EB; font-size: 34px; font-weight: 900; letter-spacing: -1px; }

    /* Botões com Gradiente */
    .stButton > button {
        background: linear-gradient(to right, #2563EB, #1D4ED8);
        color: white; border-radius: 18px; padding: 18px 36px; font-weight: 700; border: none;
        box-shadow: 0 10px 20px -5px rgba(37, 99, 235, 0.4); transition: all 0.3s;
    }
    .stButton > button:hover { transform: translateY(-3px); box-shadow: 0 15px 30px -5px rgba(37, 99, 235, 0.6); }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 4. LÓGICA E SIDEBAR
# ==========================================
def get_logo():
    paths = ["Gemini_Generated_Image_su6quisu6quisu6q.jpg", "streamlit_app/Gemini_Generated_Image_su6quisu6quisu6q.jpg"]
    for p in paths:
        if os.path.exists(p): return p
    return None
logo_oficial = get_logo()

with st.sidebar:
    if logo_oficial: st.image(logo_oficial, width=200)
    else: st.markdown("<h1 style='color: #2563EB; font-size: 40px;'>LUGAR</h1>", unsafe_allow_html=True)
    st.markdown("---")
    if not st.session_state.auth_state['is_logged']:
        st.subheader("🚀 Acesso PRO")
        with st.form("login"):
            st.text_input("Email"); st.text_input("Senha", type="password")
            if st.form_submit_button("Desbloquear Painel"):
                st.session_state.auth_state.update({'is_logged': True, 'user_name': 'Admin', 'plan': 'Enterprise'})
                st.rerun()
    else:
        st.success(f"Logado: {st.session_state.auth_state['user_name']} ({st.session_state.auth_state['plan']})")
        if st.button("Sair"): st.session_state.auth_state['is_logged'] = False; st.rerun()
    st.markdown("---")
    st.markdown("### 🎯 Radar Aveiro")
    st.metric("Novos Hoje", "32", "+5")

# ==========================================
# 5. CORPO DA PÁGINA (HERO + BUSCA)
# ==========================================
st.markdown("""
    <div class="hero-section">
        <h1>Lugar</h1>
        <p>Inteligência imobiliária. Mais cor, mais vida, mais resultados.</p>
    </div>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="search-dock">', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([3, 1.2, 1.2, 1])
    with c1: st.text_input("Localização", placeholder="Onde queres viver?", label_visibility="collapsed")
    with c2: st.selectbox("Operação", ["Arrendar", "Comprar"], label_visibility="collapsed")
    with c3: st.selectbox("Tipologia", ["T1", "T2", "T3+"], label_visibility="collapsed")
    with c4: st.button("🔍 BUSCAR AGORA")
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================
# 6. MAPA E CARDS VIBRANTES
# ==========================================
col_map, col_details = st.columns([2, 1.2])

with col_map:
    m = folium.Map(location=[40.6405, -8.6538], zoom_start=14, tiles='CartoDB positron', zoom_control=False)
    folium.CircleMarker([40.6445, -8.6588], radius=15, color='#2563EB', fill=True, fill_opacity=0.9, popup="€850").add_to(m)
    folium.CircleMarker([40.6380, -8.6520], radius=15, color='#6366F1', fill=True, fill_opacity=0.9, popup="€1200").add_to(m)
    st_folium(m, width="100%", height=750, returned_objects=[])

with col_details:
    st.subheader("🔥 Oportunidades Quentes")
    for i in range(2):
        st.markdown(f"""
            <div class="prop-card">
                <div class="prop-img-placeholder">📸 Foto Vibrante do Imóvel {i+1}</div>
                <div style="padding: 30px;">
                    <div style="display: flex; gap: 10px; margin-bottom: 15px;">
                        <span class="badge-new">NOVO HOJE</span>
                        <span class="badge-ai">IA VALIDADO</span>
                    </div>
                    <div class="price-tag">€ {850 + (i*350)}<span style="font-size: 16px; font-weight: 600;">/mês</span></div>
                    <h3 style="margin: 10px 0; font-size: 22px;">T{i+2} de Luxo em Aveiro</h3>
                    <p style="color: #64748B; font-weight: 500;">📍 Glória, Aveiro Centro</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if not st.session_state.auth_state['is_logged']:
            st.button(f"🔒 Desbloquear Contato {i+1}", disabled=True)
        else:
            st.button(f"📞 Ligar Agora {i+1}")